"""Redact spoiler terms from parsed transcripts.

Reads build/parsed/*.json (and build/parsed/subagents/*.json), applies
case-insensitive whole-word matching against tools/spoilers.json's terms
(and their variants), replacing each match with a category-only marker
``⟦redacted: <category>⟦``. Topic regexes (hard, structural spoilers such
as Edwin's death or the plague) redact the whole sentence containing the
match instead, as ``⟦redacted sentence: <topic>⟦``.

Scene numbers above 40 mentioned as "scene 57" / "ch 57" / in filenames are
left visible but get an ``⟦unpublished⟦`` tag appended, as do paths under
the configured unpublished path prefixes.

Writes build/redacted/ in the same directory shape as build/parsed/, plus
build/redaction-report.json with per-file redaction counts by category and
density (redacted chars / total chars), flagging anything over 15%.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SPOILERS_PATH = REPO_ROOT / "tools" / "spoilers.json"
PARSED_DIR = REPO_ROOT / "build" / "parsed"
REDACTED_DIR = REPO_ROOT / "build" / "redacted"
REPORT_PATH = REPO_ROOT / "build" / "redaction-report.json"

DENSITY_THRESHOLD = 0.15

CHAR_MARK = "⟦"  # ⟦
CHAR_MARK_CLOSE = "⟧"  # ⟧

# A "sentence" boundary for whole-sentence topic redaction. Deliberately
# simple: split on ., !, ? followed by whitespace/EOL, or newlines.
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+|\n+")

_SCENE_NUM_RE = re.compile(
    r"\b(scene|ch(?:apter)?)\s*0*([0-9]{1,3})\b", re.IGNORECASE
)
_SCENE_FILENAME_RE = re.compile(r"\b0*([0-9]{2,3})-[a-z0-9-]+\.md\b", re.IGNORECASE)


def _word_pattern(term: str) -> re.Pattern:
    """Whole-word, case-insensitive pattern for a term/variant.

    Escapes the term then relaxes escaped spaces to \\s+ so multi-word
    terms still match across incidental whitespace differences, and uses
    word boundaries at both ends (falling back to lookaround for terms
    that start/end with a non-word character, e.g. "[Wayfaring]").
    """
    escaped = re.escape(term.strip())
    escaped = escaped.replace(r"\ ", r"\s+")
    starts_word = term[0:1].isalnum()
    ends_word = term[-1:].isalnum() if term else False
    prefix = r"\b" if starts_word else r"(?<!\w)"
    suffix = r"\b" if ends_word else r"(?!\w)"
    return re.compile(prefix + escaped + suffix, re.IGNORECASE)


@dataclass
class TermRule:
    term: str
    category: str
    variants: list[str] = field(default_factory=list)
    patterns: list[re.Pattern] = field(default_factory=list)

    def all_names(self) -> list[str]:
        return [self.term] + list(self.variants)


@dataclass
class TopicRule:
    topic: str
    pattern: re.Pattern


@dataclass
class Spoilers:
    terms: list[TermRule]
    topics: list[TopicRule]
    path_prefixes: list[str]
    scene_threshold: int

    @classmethod
    def load(cls, path: Path = SPOILERS_PATH) -> "Spoilers":
        raw = json.loads(path.read_text())
        terms = []
        for t in raw["terms"]:
            names = [t["term"]] + list(t.get("variants", []))
            patterns = [_word_pattern(n) for n in names if n.strip()]
            terms.append(
                TermRule(
                    term=t["term"],
                    category=t["category"],
                    variants=list(t.get("variants", [])),
                    patterns=patterns,
                )
            )
        # Longer terms first, so multi-word terms take priority over any
        # single-word term/variant that happens to be a substring of them.
        terms.sort(key=lambda tr: -len(tr.term))
        topics = [
            TopicRule(topic=t["topic"], pattern=re.compile(t["pattern"], re.IGNORECASE))
            for t in raw.get("topic_regexes", [])
        ]
        rules = raw.get("unpublished_path_rules", {})
        return cls(
            terms=terms,
            topics=topics,
            path_prefixes=list(rules.get("path_prefixes", [])),
            scene_threshold=int(rules.get("scene_number_threshold", 40)),
        )


@dataclass
class RedactionCounts:
    by_category: dict = field(default_factory=dict)
    redacted_chars: int = 0
    total_chars: int = 0
    unpublished_tags: int = 0

    def add_category(self, category: str, n: int = 1) -> None:
        self.by_category[category] = self.by_category.get(category, 0) + n

    def merge(self, other: "RedactionCounts") -> None:
        for k, v in other.by_category.items():
            self.by_category[k] = self.by_category.get(k, 0) + v
        self.redacted_chars += other.redacted_chars
        self.total_chars += other.total_chars
        self.unpublished_tags += other.unpublished_tags

    def density(self) -> float:
        if self.total_chars == 0:
            return 0.0
        return self.redacted_chars / self.total_chars


def _mark_scene_numbers(text: str, spoilers: Spoilers, counts: RedactionCounts) -> str:
    """Tag scene numbers / scene filenames above the published threshold."""

    def repl_num(m: re.Match) -> str:
        n = int(m.group(2))
        if n > spoilers.scene_threshold:
            counts.unpublished_tags += 1
            return f"{m.group(0)} {CHAR_MARK}unpublished{CHAR_MARK_CLOSE}"
        return m.group(0)

    def repl_fname(m: re.Match) -> str:
        n = int(m.group(1))
        if n > spoilers.scene_threshold:
            counts.unpublished_tags += 1
            return f"{m.group(0)} {CHAR_MARK}unpublished{CHAR_MARK_CLOSE}"
        return m.group(0)

    text = _SCENE_NUM_RE.sub(repl_num, text)
    text = _SCENE_FILENAME_RE.sub(repl_fname, text)
    return text


def _mark_unpublished_paths(text: str, spoilers: Spoilers, counts: RedactionCounts) -> str:
    for prefix in spoilers.path_prefixes:
        # find literal occurrences of the prefix and tag the token containing it
        idx = 0
        while True:
            i = text.find(prefix, idx)
            if i == -1:
                break
            # extend to the end of the path token (no whitespace)
            j = i
            while j < len(text) and not text[j].isspace() and text[j] not in ")\"'":
                j += 1
            already_tagged = text[j:].startswith(f" {CHAR_MARK}unpublished{CHAR_MARK_CLOSE}")
            if not already_tagged:
                tag = f" {CHAR_MARK}unpublished{CHAR_MARK_CLOSE}"
                text = text[:j] + tag + text[j:]
                counts.unpublished_tags += 1
                idx = j + len(tag)
            else:
                idx = j
    return text


def _redact_terms(text: str, spoilers: Spoilers, counts: RedactionCounts) -> str:
    for rule in spoilers.terms:
        for pattern in rule.patterns:
            def repl(m: re.Match, rule=rule) -> str:
                counts.add_category(rule.category)
                counts.redacted_chars += len(m.group(0))
                return f"{CHAR_MARK}redacted: {rule.category}{CHAR_MARK_CLOSE}"

            text = pattern.sub(repl, text)
    return text


def _redact_topic_sentences(text: str, spoilers: Spoilers, counts: RedactionCounts) -> str:
    if not spoilers.topics:
        return text
    # Split into sentences (keeping separators out; we rejoin with a single
    # space / newline choice below is not needed since we operate in-place
    # on spans instead, to preserve original whitespace/formatting).
    spans = []
    pos = 0
    for m in _SENTENCE_SPLIT_RE.finditer(text):
        spans.append((pos, m.start()))
        pos = m.end()
    spans.append((pos, len(text)))

    out = []
    last_end = 0
    for start, end in spans:
        sentence = text[start:end]
        matched_topic = None
        for topic in spoilers.topics:
            if topic.pattern.search(sentence):
                matched_topic = topic.topic
                break
        out.append(text[last_end:start])
        if matched_topic and sentence.strip():
            counts.add_category(f"topic:{matched_topic}")
            counts.redacted_chars += len(sentence)
            out.append(f"{CHAR_MARK}redacted sentence: {matched_topic}{CHAR_MARK_CLOSE}")
        else:
            out.append(sentence)
        last_end = end
    out.append(text[last_end:])
    return "".join(out)


def redact_text(text: str, spoilers: Spoilers, counts: RedactionCounts) -> str:
    if not text:
        return text
    counts.total_chars += len(text)
    # Topic (sentence-level) redaction first, so a redacted sentence's
    # contents don't also get double-counted by term redaction; term
    # redaction then still catches things outside those sentences.
    text = _redact_topic_sentences(text, spoilers, counts)
    text = _redact_terms(text, spoilers, counts)
    text = _mark_unpublished_paths(text, spoilers, counts)
    text = _mark_scene_numbers(text, spoilers, counts)
    return text


TEXT_BLOCK_FIELDS = {
    "text": ["text"],
    "thinking": ["text"],
    "tool_use": ["command", "description", "prompt", "file", "url", "query", "input",
                 "workflow_name", "workflow_description"],
    "tool_result": ["error"],
    "command": ["name"],
}


def _redact_value(value, spoilers: Spoilers, counts: RedactionCounts):
    if isinstance(value, str):
        return redact_text(value, spoilers, counts)
    if isinstance(value, list):
        return [_redact_value(v, spoilers, counts) for v in value]
    if isinstance(value, dict):
        return {k: _redact_value(v, spoilers, counts) for k, v in value.items()}
    return value


def redact_block(block: dict, spoilers: Spoilers, counts: RedactionCounts) -> dict:
    block = dict(block)
    kind = block.get("kind")
    fields = TEXT_BLOCK_FIELDS.get(kind, [])
    for field_name in fields:
        if field_name in block and block[field_name] is not None:
            block[field_name] = _redact_value(block[field_name], spoilers, counts)
    if kind == "tool_result" and "stdout_preview" in block and block["stdout_preview"]:
        block["stdout_preview"] = [
            redact_text(line, spoilers, counts) for line in block["stdout_preview"]
        ]
    return block


def redact_transcript(doc: dict, spoilers: Spoilers) -> tuple[dict, RedactionCounts]:
    counts = RedactionCounts()
    doc = dict(doc)
    turns = []
    for turn in doc.get("turns", []):
        turn = dict(turn)
        turn["blocks"] = [redact_block(b, spoilers, counts) for b in turn.get("blocks", [])]
        turns.append(turn)
    doc["turns"] = turns
    return doc, counts


def _iter_parsed_files():
    for p in sorted(PARSED_DIR.glob("*.json")):
        if p.name == "index.json":
            continue
        yield p, REDACTED_DIR / p.name
    subdir = PARSED_DIR / "subagents"
    if subdir.is_dir():
        for p in sorted(subdir.glob("*.json")):
            yield p, REDACTED_DIR / "subagents" / p.name


def main() -> None:
    spoilers = Spoilers.load()
    REDACTED_DIR.mkdir(parents=True, exist_ok=True)
    (REDACTED_DIR / "subagents").mkdir(parents=True, exist_ok=True)

    report = {"files": {}, "over_threshold": [], "threshold": DENSITY_THRESHOLD}
    total_counts = RedactionCounts()

    for src, dst in _iter_parsed_files():
        doc = json.loads(src.read_text())
        redacted, counts = redact_transcript(doc, spoilers)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(json.dumps(redacted, indent=1))

        rel = str(dst.relative_to(REDACTED_DIR))
        density = counts.density()
        report["files"][rel] = {
            "by_category": counts.by_category,
            "redacted_chars": counts.redacted_chars,
            "total_chars": counts.total_chars,
            "unpublished_tags": counts.unpublished_tags,
            "density": density,
        }
        if density > DENSITY_THRESHOLD:
            report["over_threshold"].append(rel)
        total_counts.merge(counts)

    # copy index.json through untouched (it has no free text worth redacting
    # beyond first_user_prompt, which we do redact)
    index_src = PARSED_DIR / "index.json"
    if index_src.is_file():
        index = json.loads(index_src.read_text())
        idx_counts = RedactionCounts()
        for s in index.get("sessions", []):
            if "first_user_prompt" in s:
                s["first_user_prompt"] = redact_text(s["first_user_prompt"], spoilers, idx_counts)
        (REDACTED_DIR / "index.json").write_text(json.dumps(index, indent=1))
        total_counts.merge(idx_counts)

    report["totals"] = {
        "by_category": total_counts.by_category,
        "redacted_chars": total_counts.redacted_chars,
        "total_chars": total_counts.total_chars,
        "density": total_counts.density(),
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2))
    print(f"redacted {len(report['files'])} files; {len(report['over_threshold'])} over "
          f"{DENSITY_THRESHOLD:.0%} density")


if __name__ == "__main__":
    main()
