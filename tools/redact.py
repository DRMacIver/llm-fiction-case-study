"""Redact spoiler terms from parsed transcripts.

Reads build/parsed/*.json (and build/parsed/subagents/*.json), applies
case-insensitive whole-word matching against tools/spoilers.json's terms
(and their variants), replacing each match with a category-only marker
``⟦redacted⟧`` (no category or reason shown: the reason itself would be a spoiler). Topic regexes (hard, structural spoilers such
as Edwin's death or the plague) redact the whole sentence containing the
match instead, as ``⟦redacted sentence⟧``. Only "private" and "unpublished prose" are labelled.

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
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SPOILERS_PATH = REPO_ROOT / "tools" / "spoilers.json"
PARSED_DIR = REPO_ROOT / "build" / "parsed"
REDACTED_DIR = REPO_ROOT / "build" / "redacted"
REPORT_PATH = REPO_ROOT / "build" / "redaction-report.json"
PROSE_INDEX_PATH = REPO_ROOT / "build" / "prose-index.pkl"

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

# Local, private-machine identifiers that leak operational/filesystem detail
# (never a story spoiler, but never the site's business to show either):
# absolute paths under the user's Claude Code project-storage directory or
# this tool's own scratch directory (session ids, subagent/workflow paths,
# memory-file paths all live under these), plus bare tool-use/task ids that
# appear outside of a path (e.g. quoted alone in prose).
_PRIVATE_PATH_RE = re.compile(
    r"(?:/Users/[a-zA-Z0-9_.-]+/\.claude/|/private/tmp/claude-501/)[^\s<>`\"')]*"
)
# Broader variant used for the "meta" source profile (this project's own
# transcripts): unlike the novel's transcripts, whose only private-path
# leakage is Claude Code project storage / the scratch dir (the literal
# "/Users/drmaciver/Projects/autoroad" repo path is instead a spoiler `term`
# in spoilers.json), this project's transcripts can mention *any* local
# "/Users/<user>/..." path (this repo's own cwd, a sibling project's repo,
# a home-directory file, ...) -- so every such path is redacted outright
# rather than only the two known-sensitive prefixes.
_PRIVATE_PATH_RE_BROAD = re.compile(
    r"/Users/[a-zA-Z0-9_.-]+(?:/[^\s<>`\"')]*)?"
)
_PRIVATE_ID_RE = re.compile(
    r"\btoolu_[A-Za-z0-9]+\b"
    r"|\bwf_[0-9a-f]{6,10}-[0-9a-f]{3}\b"
    r"|\bfeedback-[a-z0-9-]+\.md\b"
)

# Matches an already-inserted redaction marker verbatim, e.g.
# "⟦redacted: character⟧" or "⟦redacted sentence: plague/epidemic⟧". Used to
# protect earlier passes' output from being re-scanned (and corrupted) by
# later passes -- e.g. a topic-sentence marker whose *topic name* itself
# contains a word a later term rule matches (a marker for the "Edwin's
# death/mortality" topic contains the literal text "Edwin's death", which
# the "Edwin's death" term rule would otherwise also match and blank out,
# producing a nested "⟦redacted sentence: ⟦redacted: event⟧/mortality⟧").
_MARKER_RE = re.compile(re.escape(CHAR_MARK) + r"[^" + CHAR_MARK + CHAR_MARK_CLOSE + r"]*" + re.escape(CHAR_MARK_CLOSE))


def _apply_outside_markers(text: str, fn) -> str:
    """Run ``fn`` (str -> str) only on the spans of ``text`` that aren't
    already an inserted ``⟦...⟧`` redaction marker, leaving markers from
    earlier passes untouched."""
    if CHAR_MARK not in text:
        return fn(text)
    out = []
    last_end = 0
    for m in _MARKER_RE.finditer(text):
        out.append(fn(text[last_end : m.start()]))
        out.append(m.group(0))
        last_end = m.end()
    out.append(fn(text[last_end:]))
    return "".join(out)


def _word_pattern(term: str) -> re.Pattern:
    """Whole-word, case-insensitive pattern for a term/variant.

    Escapes the term then relaxes escaped spaces to \\s+ so multi-word
    terms still match across incidental whitespace differences, and uses
    word boundaries at both ends (falling back to lookaround for terms
    that start/end with a non-word character, e.g. "[Wayfaring]").

    A term that looks like an absolute filesystem path (starts with "/")
    gets no left-boundary check at all: it's already a long, distinctive
    literal, so a boundary there buys no protection against false
    positives, but it does cause false *negatives* -- text that survived
    an inner layer of JSON-escaping can carry a literal two-character
    "\\n" (backslash then the letter n) immediately before the path
    instead of a real newline, and the trailing "n" is a word character
    that `(?<!\\w)` then wrongly treats as "mid-word", so the path slips
    through unredacted right next to other, correctly-redacted copies of
    the same literal path a few characters later in the same text.
    """
    escaped = re.escape(term.strip())
    escaped = escaped.replace(r"\ ", r"\s+")
    starts_word = term[0:1].isalnum()
    ends_word = term[-1:].isalnum() if term else False
    if term.startswith("/"):
        prefix = ""
    else:
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
    premise_revealed_at: datetime | None = None

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
        premise_revealed_at = None
        ts = raw.get("premise_revealed_at")
        if ts:
            premise_revealed_at = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return cls(
            terms=terms,
            topics=topics,
            path_prefixes=list(rules.get("path_prefixes", [])),
            scene_threshold=int(rules.get("scene_number_threshold", 40)),
            premise_revealed_at=premise_revealed_at,
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


def _redact_private_paths(text: str, counts: RedactionCounts, broad: bool = False) -> str:
    """Blank local filesystem paths / tool-use ids that leak operational
    detail (Claude Code project storage, this tool's scratch dir, toolu_
    ids). Not a story spoiler category -- always the generic "private"
    marker, matching the existing literal /Users/.../autoroad term's
    category in spoilers.json. ``broad=True`` (the "meta" source profile)
    redacts any "/Users/<user>/..." path, not just the two known-sensitive
    prefixes -- see `_PRIVATE_PATH_RE_BROAD`.
    """

    def repl(m: re.Match) -> str:
        counts.add_category("private")
        counts.redacted_chars += len(m.group(0))
        return f"{CHAR_MARK}redacted: private{CHAR_MARK_CLOSE}"

    text = (_PRIVATE_PATH_RE_BROAD if broad else _PRIVATE_PATH_RE).sub(repl, text)
    text = _PRIVATE_ID_RE.sub(repl, text)
    return text


def build_anonymize_patterns(terms: list[str]) -> list[re.Pattern]:
    """Compile an ordered list of whole-word(ish) patterns for the "meta"
    source's anonymisation map (see tools/sources.json's `anonymize` list).
    Longest terms first, so e.g. "hegel-blog-post" is matched (and
    replaced) whole before the later, bare "hegel" pattern would otherwise
    also match the "hegel" inside it."""
    ordered = sorted(terms, key=len, reverse=True)
    return [_word_pattern(t) for t in ordered]


def _anonymize(
    text: str, patterns: list[re.Pattern], placeholder: str, counts: RedactionCounts
) -> str:
    if not patterns:
        return text

    def repl(m: re.Match) -> str:
        counts.add_category("anonymized")
        return placeholder

    for pattern in patterns:
        text = pattern.sub(repl, text)
    return text


def _redact_terms(text: str, spoilers: Spoilers, counts: RedactionCounts) -> str:
    for rule in spoilers.terms:
        for pattern in rule.patterns:
            def repl(m: re.Match, rule=rule) -> str:
                counts.add_category(rule.category)
                counts.redacted_chars += len(m.group(0))
                return f"{CHAR_MARK}redacted{CHAR_MARK_CLOSE}"

            text = pattern.sub(repl, text)
    return text


def load_prose_index(path: Path = PROSE_INDEX_PATH):
    """Load the shingle index built by tools/prose_index.py, if present.

    Returns an object with a precomputed ``unpublished_only`` attribute (the
    unpublished shingle set minus anything that also appears in the
    published-scenes shingle set, so quoting a sentence that happens to also
    appear in the published run isn't flagged) plus ``shingle_size``. Returns
    None (guard disabled) if the index hasn't been built yet.
    """
    if not path.is_file():
        return None
    from tools.prose_index import ProseIndex  # local import: keeps redact.py

    index = ProseIndex.load(path)
    if not hasattr(index, "unpublished_only"):
        index.unpublished_only = index.unpublished - index.published
    return index


def _redact_unpublished_prose_sentences(
    text: str, prose_index, counts: RedactionCounts
) -> str:
    """Sentence-level guard against quoted unpublished story prose.

    Deterministic backstop for term/topic redaction: splits `text` into
    sentences and, for each one, hashes its 7-word shingles (same
    normalisation as the index) and checks them against shingles that occur
    in unpublished story sources but never in the published scenes. Any hit
    replaces the whole sentence. Sentences shorter than the shingle size
    can't produce a shingle at all and so can never match -- acceptable,
    per the design: this is a backstop for verbatim-ish quoting, not a
    general spoiler detector.
    """
    if prose_index is None or not prose_index.unpublished_only:
        return text
    from tools.prose_index import shingle_hashes

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
        out.append(text[last_end:start])
        hashes = shingle_hashes(sentence, prose_index.shingle_size)
        if hashes and not hashes.isdisjoint(prose_index.unpublished_only):
            counts.add_category("prose_guard:unpublished_quote")
            counts.redacted_chars += len(sentence)
            out.append(f"{CHAR_MARK}redacted sentence: unpublished prose{CHAR_MARK_CLOSE}")
        else:
            out.append(sentence)
        last_end = end
    out.append(text[last_end:])
    return "".join(out)


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
            out.append(f"{CHAR_MARK}redacted sentence{CHAR_MARK_CLOSE}")
        else:
            out.append(sentence)
        last_end = end
    out.append(text[last_end:])
    return "".join(out)


_BOLD_TOKEN_RE = re.compile(r"\*\*")
_BACKTICK_RUN_RE = re.compile(r"`+")


def _drop_last_match(text: str, matches: list[re.Match]) -> str:
    last = matches[-1]
    return text[: last.start()] + text[last.end() :]


def _strip_unbalanced_markdown_tokens(text: str) -> str:
    """A `**bold**` or `` `code` `` span can lose one of its two delimiters
    when the matching half fell inside a sentence/term that got swapped for
    a ``⟦redacted...⟧`` marker by one of the passes above, leaving a single
    stray ``**`` or backtick that renders as literal punctuation instead of
    real emphasis/code formatting. Deterministic best-effort cleanup, run
    outside already-inserted markers: if ``**`` appears an odd number of
    times, or a lone backtick (never a ```` ``` ````-style fence) does, the
    last stray one is dropped so the page never shows unmatched markdown
    syntax. Only ever removes punctuation, never redacted content."""

    def _drop_bold(s: str) -> str:
        matches = list(_BOLD_TOKEN_RE.finditer(s))
        return _drop_last_match(s, matches) if len(matches) % 2 else s

    def _drop_backtick(s: str) -> str:
        # Only lone backticks are inline-code delimiters; runs of 3+ are a
        # fenced-code-block marker and are left alone entirely.
        matches = [m for m in _BACKTICK_RUN_RE.finditer(s) if len(m.group(0)) == 1]
        return _drop_last_match(s, matches) if len(matches) % 2 else s

    text = _apply_outside_markers(text, _drop_bold)
    text = _apply_outside_markers(text, _drop_backtick)
    return text


def redact_text(
    text: str,
    spoilers: Spoilers,
    counts: RedactionCounts,
    prose_index=None,
    full: bool = True,
    enable_paths_and_scenes: bool = True,
    broad_private_paths: bool = False,
    anonymize_patterns: list[re.Pattern] | None = None,
    anonymize_placeholder: str = "",
) -> str:
    """Redact ``text``.

    When ``full`` is False (block predates the premise reveal), only the
    private-information pass runs: term, topic, scene-number, unpublished-
    path and prose-guard passes are all skipped, since nothing before the
    premise reveal is a story spoiler.

    ``enable_paths_and_scenes=False`` (the "meta" source profile) skips the
    unpublished-path/scene-number *tagging* passes entirely -- they only
    make sense against the novel's own scene numbering and plans/ tree.
    ``broad_private_paths`` widens the private-path redaction to any
    "/Users/<user>/..." path (see `_redact_private_paths`). ``anonymize_*``
    apply an unrelated-project anonymisation map (see
    `build_anonymize_patterns`) before every other pass, everywhere.
    """
    if not text:
        return text
    counts.total_chars += len(text)
    if anonymize_patterns:
        text = _anonymize(text, anonymize_patterns, anonymize_placeholder, counts)
    if not full:
        text = _apply_outside_markers(
            text, lambda t: _redact_private_paths(t, counts, broad=broad_private_paths)
        )
        text = _strip_unbalanced_markdown_tokens(text)
        return text
    # Topic (sentence-level) redaction first, so a redacted sentence's
    # contents don't also get double-counted by term redaction; term
    # redaction then still catches things outside those sentences.
    text = _redact_topic_sentences(text, spoilers, counts)
    # Every pass below runs after topic-sentence redaction may have already
    # inserted "⟦...⟧" markers into `text`; keep those spans untouched so
    # a marker's own wording (e.g. a topic name) can't be re-matched and
    # corrupted into a nested marker.
    text = _apply_outside_markers(
        text, lambda t: _redact_private_paths(t, counts, broad=broad_private_paths)
    )
    text = _apply_outside_markers(text, lambda t: _redact_terms(t, spoilers, counts))
    if enable_paths_and_scenes:
        text = _apply_outside_markers(text, lambda t: _mark_unpublished_paths(t, spoilers, counts))
        text = _apply_outside_markers(text, lambda t: _mark_scene_numbers(t, spoilers, counts))
    # Deterministic quoted-unpublished-prose guard, last: a backstop for
    # whatever term/topic redaction above didn't catch. No-op when
    # `prose_index` is None (never built/loaded for the "meta" profile).
    text = _apply_outside_markers(
        text, lambda t: _redact_unpublished_prose_sentences(t, prose_index, counts)
    )
    text = _strip_unbalanced_markdown_tokens(text)
    return text


TEXT_BLOCK_FIELDS = {
    "text": ["text"],
    "thinking": ["text"],
    "tool_use": ["command", "description", "prompt", "file", "url", "query", "input",
                 "workflow_name", "workflow_description"],
    "tool_result": ["error"],
    "command": ["name", "output"],
    "system_note": ["summary"],
}


def _redact_value(
    value,
    spoilers: Spoilers,
    counts: RedactionCounts,
    prose_index=None,
    full: bool = True,
    **kw,
):
    if isinstance(value, str):
        return redact_text(value, spoilers, counts, prose_index, full=full, **kw)
    if isinstance(value, list):
        return [_redact_value(v, spoilers, counts, prose_index, full=full, **kw) for v in value]
    if isinstance(value, dict):
        return {
            k: _redact_value(v, spoilers, counts, prose_index, full=full, **kw)
            for k, v in value.items()
        }
    return value


def redact_block(
    block: dict,
    spoilers: Spoilers,
    counts: RedactionCounts,
    prose_index=None,
    full: bool = True,
    **kw,
) -> dict:
    block = dict(block)
    kind = block.get("kind")
    fields = TEXT_BLOCK_FIELDS.get(kind, [])
    for field_name in fields:
        if field_name in block and block[field_name] is not None:
            block[field_name] = _redact_value(
                block[field_name], spoilers, counts, prose_index, full=full, **kw
            )
    if kind == "tool_result" and "stdout_preview" in block and block["stdout_preview"]:
        block["stdout_preview"] = [
            redact_text(line, spoilers, counts, prose_index, full=full, **kw)
            for line in block["stdout_preview"]
        ]
    return block


def _parse_ts(ts: str | None) -> datetime | None:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None


def redact_transcript(
    doc: dict,
    spoilers: Spoilers,
    prose_index=None,
    is_subagent: bool = False,
    premise_cutoff_enabled: bool = True,
    enable_paths_and_scenes: bool = True,
    broad_private_paths: bool = False,
    anonymize_patterns: list[re.Pattern] | None = None,
    anonymize_placeholder: str = "",
) -> tuple[dict, RedactionCounts]:
    counts = RedactionCounts()
    doc = dict(doc)
    cutoff = spoilers.premise_revealed_at if premise_cutoff_enabled else None
    turns = []

    kw = dict(
        enable_paths_and_scenes=enable_paths_and_scenes,
        broad_private_paths=broad_private_paths,
        anonymize_patterns=anonymize_patterns,
        anonymize_placeholder=anonymize_placeholder,
    )

    subagent_pre_cutoff = None
    if is_subagent and cutoff is not None:
        first_ts = _parse_ts(doc.get("start"))
        if first_ts is None:
            for turn in doc.get("turns", []):
                first_ts = _parse_ts(turn.get("timestamp"))
                if first_ts is not None:
                    break
        subagent_pre_cutoff = first_ts is not None and first_ts < cutoff

    for turn in doc.get("turns", []):
        turn = dict(turn)
        if cutoff is None:
            full = True
        elif is_subagent:
            full = not subagent_pre_cutoff
        else:
            ts = _parse_ts(turn.get("timestamp"))
            full = ts is None or ts >= cutoff
        turn["blocks"] = [
            redact_block(b, spoilers, counts, prose_index, full=full, **kw)
            for b in turn.get("blocks", [])
        ]
        turns.append(turn)
    doc["turns"] = turns
    return doc, counts


def _iter_parsed_files(parsed_dir: Path):
    for p in sorted(parsed_dir.glob("*.json")):
        if p.name == "index.json":
            continue
        yield p, p.name, False
    subdir = parsed_dir / "subagents"
    if subdir.is_dir():
        for p in sorted(subdir.glob("*.json")):
            yield p, Path("subagents") / p.name, True


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="autoroad", help="source name from tools/sources.json")
    args = ap.parse_args()

    from tools.sources import load_source

    src_cfg = load_source(args.source)
    parsed_dir = src_cfg.parsed_dir
    redacted_dir = src_cfg.redacted_dir
    report_path = src_cfg.out_dir / "redaction-report.json"
    profile = src_cfg.profile  # "full" | "meta"
    enable_paths_and_scenes = profile == "full"
    broad_private_paths = profile != "full"
    premise_cutoff_enabled = src_cfg.premise_cutoff
    anonymize_patterns = build_anonymize_patterns(src_cfg.anonymize) if src_cfg.anonymize else None

    spoilers = Spoilers.load()
    # The unpublished-prose sentence guard is a backstop against quoting the
    # novel's own unpublished prose verbatim -- meaningless (and never
    # built) for a source that isn't the novel's own transcripts.
    prose_index = load_prose_index() if profile == "full" else None
    if profile == "full" and prose_index is None:
        print(
            "warning: no build/prose-index.pkl found (run `uv run python -m "
            "tools.prose_index` first) -- unpublished-prose sentence guard disabled"
        )
    redacted_dir.mkdir(parents=True, exist_ok=True)
    (redacted_dir / "subagents").mkdir(parents=True, exist_ok=True)

    report = {"files": {}, "over_threshold": [], "threshold": DENSITY_THRESHOLD}
    total_counts = RedactionCounts()

    redact_kw = dict(
        premise_cutoff_enabled=premise_cutoff_enabled,
        enable_paths_and_scenes=enable_paths_and_scenes,
        broad_private_paths=broad_private_paths,
        anonymize_patterns=anonymize_patterns,
        anonymize_placeholder=src_cfg.anonymize_placeholder,
    )

    for src, rel, is_subagent in _iter_parsed_files(parsed_dir):
        doc = json.loads(src.read_text())
        redacted, counts = redact_transcript(
            doc, spoilers, prose_index, is_subagent=is_subagent, **redact_kw
        )
        dst = redacted_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(json.dumps(redacted, indent=1))

        rel_str = str(rel)
        density = counts.density()
        report["files"][rel_str] = {
            "by_category": counts.by_category,
            "redacted_chars": counts.redacted_chars,
            "total_chars": counts.total_chars,
            "unpublished_tags": counts.unpublished_tags,
            "density": density,
        }
        if density > DENSITY_THRESHOLD:
            report["over_threshold"].append(rel_str)
        total_counts.merge(counts)

    # copy index.json through untouched (it has no free text worth redacting
    # beyond first_user_prompt, which we do redact)
    index_src = parsed_dir / "index.json"
    if index_src.is_file():
        index = json.loads(index_src.read_text())
        idx_counts = RedactionCounts()
        for s in index.get("sessions", []):
            if "first_user_prompt" in s:
                s["first_user_prompt"] = redact_text(
                    s["first_user_prompt"], spoilers, idx_counts, prose_index, **redact_kw_no_cutoff(redact_kw)
                )
        (redacted_dir / "index.json").write_text(json.dumps(index, indent=1))
        total_counts.merge(idx_counts)

    report["totals"] = {
        "by_category": total_counts.by_category,
        "redacted_chars": total_counts.redacted_chars,
        "total_chars": total_counts.total_chars,
        "density": total_counts.density(),
    }
    report_path.write_text(json.dumps(report, indent=2))
    print(f"redacted {len(report['files'])} files; {len(report['over_threshold'])} over "
          f"{DENSITY_THRESHOLD:.0%} density")


def redact_kw_no_cutoff(redact_kw: dict) -> dict:
    """`redact_text` doesn't take `premise_cutoff_enabled` (that only
    applies at the per-turn level in `redact_transcript`) -- strip it for
    the direct `redact_text` call on `first_user_prompt`."""
    return {k: v for k, v in redact_kw.items() if k != "premise_cutoff_enabled"}


if __name__ == "__main__":
    main()
