"""Mechanical pre-pass checks over the site's prose pages.

Checks performed:
  1. Every relative markdown link resolves to an existing file.
  2. Every number (digit or number word) is extracted with its sentence and
     page; sentences that mention commits/sessions/turns/tool uses/subagents/
     scenes/chapters/dates are cross-checked against ground-truth sources.
  3. Every date mentioned lies within 2026-08-24..2026-09-02, or is flagged.
  4. No page contains a spoiler term, an em dash, a semicolon, a private
     path, or a disallowed URL.

Run as a script to (re)generate build/writing-check/prepass.md.
"""

from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
SITE_SRC = REPO_ROOT / "site" / "src"
AUTOROAD_ROOT = REPO_ROOT.parent / "autoroad"

PAGES_UNDER_CHECK = [
    SITE_SRC / "introduction.md",
    SITE_SRC / "about.md",
    *sorted((SITE_SRC / "howto").glob("*.md")),
    *sorted((SITE_SRC / "workflow").glob("*.md")),
    *sorted((SITE_SRC / "chronicle").glob("*.md")),
]

ALLOWED_URL_HOSTS = {
    "royalroad.com",
    "www.royalroad.com",
    "github.com",
    "www.github.com",
    "claude.ai",
    "claude.com",
    "code.claude.com",
    "git-scm.com",
}

NUMBER_WORDS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
    "nineteen": 19, "twenty": 20,
    "dozen": 12, "dozens": 12, "hundred": 100, "hundreds": 100,
}

TOPIC_KEYWORDS = [
    "commit", "commits", "session", "sessions", "turn", "turns",
    "tool use", "tool uses", "subagent", "subagents", "scene", "scenes",
    "chapter", "chapters", "date", "dates",
]

MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5,
    "june": 6, "july": 7, "august": 8, "september": 9, "october": 10,
    "november": 11, "december": 12,
}

PRIVATE_PATH_PATTERNS = [
    re.compile(r"/Users/"),
    re.compile(r"\.claude/projects"),
]

URL_RE = re.compile(r"https?://[^\s)>\]\"']+")
LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
# Sentence splitter: split on . ! ? followed by whitespace/newline, keep it simple.
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z(\[])|\n{2,}")


@dataclass
class LinkResult:
    page: str
    line: int
    text: str
    target: str
    ok: bool
    reason: str = ""


@dataclass
class NumberMention:
    page: str
    sentence: str
    raw: str
    value: int
    topics: list[str]
    note: str = ""
    status: str = "info"  # ok / mismatch / info


@dataclass
class DateMention:
    page: str
    sentence: str
    raw: str
    ok: bool
    reason: str = ""


@dataclass
class BannedHit:
    page: str
    line: int
    kind: str
    detail: str


def read_pages() -> dict[str, str]:
    out = {}
    for p in PAGES_UNDER_CHECK:
        out[str(p.relative_to(REPO_ROOT))] = p.read_text()
    return out


# ---------------------------------------------------------------------------
# 1. Link checking
# ---------------------------------------------------------------------------

def check_links(pages: dict[str, str]) -> list[LinkResult]:
    results = []
    for rel_path, text in pages.items():
        page_path = REPO_ROOT / rel_path
        for lineno, line in enumerate(text.splitlines(), start=1):
            for m in LINK_RE.finditer(line):
                link_text, target = m.group(1), m.group(2)
                if target.startswith("#"):
                    continue  # in-page anchor
                if re.match(r"^[a-zA-Z][a-zA-Z0-9+.\-]*://", target):
                    continue  # absolute URL, handled by URL check
                if target.startswith("mailto:"):
                    continue
                target_no_anchor = target.split("#", 1)[0]
                if not target_no_anchor:
                    continue
                resolved = (page_path.parent / target_no_anchor).resolve()
                ok = resolved.exists()
                reason = "" if ok else "target file does not exist"
                results.append(LinkResult(rel_path, lineno, link_text, target, ok, reason))
    return results


# ---------------------------------------------------------------------------
# 2 & 3. Number and date extraction
# ---------------------------------------------------------------------------

def strip_link_targets(text: str) -> str:
    """Replace markdown link targets with nothing, keeping the visible text.

    Link targets often contain UUIDs, dates and other digit strings (transcript
    filenames, URLs) that are not numbers an author wrote in prose, so they must
    not be fed to the number/date extractors.
    """
    return LINK_RE.sub(lambda m: m.group(1), text)


def split_sentences(text: str) -> list[str]:
    # Strip code fences and inline code to avoid false positives.
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`]*`", "", text)
    text = strip_link_targets(text)
    paragraphs = re.split(r"\n{2,}", text)
    sentences = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        parts = SENTENCE_RE.split(para)
        sentences.extend(s.strip() for s in parts if s.strip())
    return sentences


DATE_PATTERNS = [
    # "24 August" / "24 August 2026"
    re.compile(
        r"\b(\d{1,2})\s+(January|February|March|April|May|June|July|August|"
        r"September|October|November|December)(?:\s+(\d{4}))?\b", re.I,
    ),
    # "August 24" / "August 24, 2026"
    re.compile(
        r"\b(January|February|March|April|May|June|July|August|"
        r"September|October|November|December)\s+(\d{1,2})(?:,?\s+(\d{4}))?\b", re.I,
    ),
    # ISO "2026-08-24"
    re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b"),
]

NUMBER_TOKEN_RE = re.compile(
    r"\b(\d[\d,]*\.?\d*)\b|\b(" +
    "|".join(sorted(NUMBER_WORDS, key=len, reverse=True)) + r")\b",
    re.I,
)


def extract_dates(sentence: str, page: str) -> list[DateMention]:
    found = []
    for pat in DATE_PATTERNS:
        for m in pat.finditer(sentence):
            groups = m.groups()
            try:
                if pat is DATE_PATTERNS[0]:
                    day = int(groups[0])
                    month = MONTHS[groups[1].lower()]
                    year = int(groups[2]) if groups[2] else 2026
                elif pat is DATE_PATTERNS[1]:
                    month = MONTHS[groups[0].lower()]
                    day = int(groups[1])
                    year = int(groups[2]) if groups[2] else 2026
                else:
                    year, month, day = int(groups[0]), int(groups[1]), int(groups[2])
            except (KeyError, ValueError):
                continue
            try:
                from datetime import date
                d = date(year, month, day)
            except ValueError:
                found.append(DateMention(page, sentence, m.group(0), False, "invalid calendar date"))
                continue
            ok = date(2026, 8, 24) <= d <= date(2026, 9, 2)
            reason = "" if ok else "outside 2026-08-24..2026-09-02"
            found.append(DateMention(page, sentence, m.group(0), ok, reason))
    return found


def sentence_topics(sentence: str) -> list[str]:
    low = sentence.lower()
    return [kw for kw in TOPIC_KEYWORDS if kw in low]


def parse_number(raw: str) -> int | None:
    raw_clean = raw.strip()
    if re.match(r"^[\d,]+\.?\d*$", raw_clean):
        try:
            if "." in raw_clean:
                return None  # skip decimals, not relevant for count comparisons
            return int(raw_clean.replace(",", ""))
        except ValueError:
            return None
    return NUMBER_WORDS.get(raw_clean.lower())


def extract_numbers(pages: dict[str, str]) -> tuple[list[NumberMention], list[DateMention]]:
    number_mentions = []
    date_mentions = []
    for rel_path, text in pages.items():
        for sentence in split_sentences(text):
            date_mentions.extend(extract_dates(sentence, rel_path))
            topics = sentence_topics(sentence)
            for m in NUMBER_TOKEN_RE.finditer(sentence):
                raw = m.group(0)
                value = parse_number(raw)
                if value is None:
                    continue
                # Skip numbers that are actually part of an already-matched date
                # (e.g. "24" in "24 August", or year "2026").
                if any(raw == dm.raw or raw in dm.raw for dm in date_mentions if dm.sentence == sentence):
                    continue
                if value == 2026:
                    continue
                number_mentions.append(
                    NumberMention(rel_path, sentence, raw, value, topics)
                )
    return number_mentions, date_mentions


# ---------------------------------------------------------------------------
# Ground truth loading
# ---------------------------------------------------------------------------

def load_ground_truth() -> dict:
    gt: dict = {}
    index_path = REPO_ROOT / "build" / "parsed" / "index.json"
    titles_path = SITE_SRC / "transcripts" / "titles.json"
    chapters_path = AUTOROAD_ROOT / "publishing" / "chapters.json"

    sessions = json.loads(index_path.read_text())["sessions"]
    gt["num_sessions"] = len(sessions)
    gt["sessions"] = sessions

    total_user_turns = sum(s.get("user_turns", 0) for s in sessions)
    gt["total_user_turns"] = total_user_turns

    tool_totals = Counter()
    subagent_calls_via_tool = 0
    for s in sessions:
        for tool, count in s.get("tool_counts", {}).items():
            tool_totals[tool] += count
    gt["tool_totals"] = dict(tool_totals)
    gt["total_tool_uses"] = sum(tool_totals.values())

    if titles_path.exists():
        gt["titles"] = json.loads(titles_path.read_text())
        gt["num_transcripts"] = len(gt["titles"])
    else:
        gt["titles"] = {}
        gt["num_transcripts"] = None

    if chapters_path.exists():
        chapters = json.loads(chapters_path.read_text())
        gt["chapters"] = chapters
        gt["num_chapters"] = len(chapters)
        gt["num_scenes"] = max(
            max(c["scenes"]) for c in chapters.values()
        )
    else:
        gt["chapters"] = {}
        gt["num_chapters"] = None
        gt["num_scenes"] = None

    # Subagent count: count files under build/parsed/subagents
    subagents_dir = REPO_ROOT / "build" / "parsed" / "subagents"
    if subagents_dir.exists():
        gt["num_subagent_files"] = len(list(subagents_dir.glob("*.json")))
    else:
        gt["num_subagent_files"] = None

    # git log commit counts per day, UTC and local
    gt["commits_utc"] = git_commit_counts(utc=True)
    gt["commits_local"] = git_commit_counts(utc=False)
    gt["total_commits"] = sum(gt["commits_utc"].values())

    return gt


def git_commit_counts(utc: bool) -> dict[str, int]:
    if not (AUTOROAD_ROOT / ".git").exists():
        return {}
    fmt = "%cd"
    tz = ["--date=format-local:%Y-%m-%d"] if utc else ["--date=format:%Y-%m-%d"]
    env = {"TZ": "UTC"} if utc else None
    import os
    full_env = os.environ.copy()
    if env:
        full_env.update(env)
    result = subprocess.run(
        ["git", "-C", str(AUTOROAD_ROOT), "log", f"--pretty={fmt}", *tz],
        capture_output=True, text=True, env=full_env, check=True,
    )
    counts = Counter(line.strip() for line in result.stdout.splitlines() if line.strip())
    return dict(sorted(counts.items()))


def cross_check_numbers(mentions: list[NumberMention], gt: dict) -> None:
    for nm in mentions:
        if not nm.topics:
            nm.status = "info"
            continue
        topics = set(nm.topics)
        matched = False
        notes = []
        if {"session", "sessions"} & topics:
            candidates = {gt.get("num_sessions"), gt.get("total_user_turns")}
            if nm.value in candidates:
                matched = True
            notes.append(f"num_sessions={gt.get('num_sessions')}")
        if {"turn", "turns"} & topics:
            if nm.value == gt.get("total_user_turns"):
                matched = True
            notes.append(f"total_user_turns={gt.get('total_user_turns')}")
        if {"tool use", "tool uses"} & topics:
            if nm.value == gt.get("total_tool_uses"):
                matched = True
            notes.append(f"total_tool_uses={gt.get('total_tool_uses')}")
        if {"subagent", "subagents"} & topics:
            if nm.value == gt.get("num_subagent_files") or nm.value == gt.get("tool_totals", {}).get("Agent"):
                matched = True
            notes.append(
                f"subagent_files={gt.get('num_subagent_files')}, "
                f"Agent tool calls={gt.get('tool_totals', {}).get('Agent')}"
            )
        if {"scene", "scenes"} & topics:
            if nm.value == gt.get("num_scenes"):
                matched = True
            notes.append(f"num_scenes={gt.get('num_scenes')}")
        if {"chapter", "chapters"} & topics:
            if nm.value == gt.get("num_chapters"):
                matched = True
            notes.append(f"num_chapters={gt.get('num_chapters')}")
        if {"commit", "commits"} & topics:
            if nm.value == gt.get("total_commits"):
                matched = True
            for day, c in gt.get("commits_utc", {}).items():
                if nm.value == c:
                    matched = True
            for day, c in gt.get("commits_local", {}).items():
                if nm.value == c:
                    matched = True
            notes.append(f"total_commits={gt.get('total_commits')} (see per-day tables)")
        if {"date", "dates"} & topics:
            notes.append("date topic (see date checks)")

        nm.note = "; ".join(notes)
        nm.status = "ok" if matched else "check"


# ---------------------------------------------------------------------------
# 4. Banned content checks
# ---------------------------------------------------------------------------

def load_spoilers() -> list[str]:
    data = json.loads((REPO_ROOT / "tools" / "spoilers.json").read_text())
    terms = []
    for entry in data.get("terms", []):
        terms.append(entry["term"])
        terms.extend(entry.get("variants", []))
    return terms


def check_banned(pages: dict[str, str], spoiler_terms: list[str]) -> list[BannedHit]:
    hits = []
    # Build case-sensitive-ish regex for spoiler terms (word-boundary where sensible)
    spoiler_patterns = []
    for term in spoiler_terms:
        if not term:
            continue
        pat = re.compile(r"(?<![A-Za-z])" + re.escape(term) + r"(?![A-Za-z])")
        spoiler_patterns.append((term, pat))

    for rel_path, text in pages.items():
        for lineno, line in enumerate(text.splitlines(), start=1):
            for term, pat in spoiler_patterns:
                if pat.search(line):
                    hits.append(BannedHit(rel_path, lineno, "spoiler", term))
            if "—" in line:
                hits.append(BannedHit(rel_path, lineno, "em dash", line.strip()[:80]))
            if ";" in line:
                hits.append(BannedHit(rel_path, lineno, "semicolon", line.strip()[:80]))
            for pat in PRIVATE_PATH_PATTERNS:
                if pat.search(line):
                    hits.append(BannedHit(rel_path, lineno, "private path", line.strip()[:80]))
            for m in URL_RE.finditer(line):
                url = m.group(0).rstrip(".,;:!?)")
                host_m = re.match(r"https?://([^/]+)", url)
                host = host_m.group(1).lower() if host_m else ""
                if host not in ALLOWED_URL_HOSTS:
                    hits.append(BannedHit(rel_path, lineno, "disallowed URL", url))
    return hits


# ---------------------------------------------------------------------------
# Report rendering
# ---------------------------------------------------------------------------

def render_report(
    pages: dict[str, str],
    link_results: list[LinkResult],
    number_mentions: list[NumberMention],
    date_mentions: list[DateMention],
    banned_hits: list[BannedHit],
    gt: dict,
) -> str:
    lines = ["# Prose pre-pass report", ""]

    # --- Links ---
    broken = [r for r in link_results if not r.ok]
    lines.append(f"## Links ({len(link_results)} checked, {len(broken)} broken)")
    lines.append("")
    if broken:
        lines.append("| page | line | text | target | issue |")
        lines.append("|---|---|---|---|---|")
        for r in broken:
            lines.append(f"| {r.page} | {r.line} | {r.text} | {r.target} | {r.reason} |")
    else:
        lines.append("All relative links resolve.")
    lines.append("")

    # --- Dates ---
    bad_dates = [d for d in date_mentions if not d.ok]
    lines.append(f"## Dates ({len(date_mentions)} found, {len(bad_dates)} out of range)")
    lines.append("")
    if date_mentions:
        lines.append("| page | date | in range | sentence |")
        lines.append("|---|---|---|---|")
        for d in date_mentions:
            snippet = d.sentence.replace("\n", " ")[:140]
            lines.append(f"| {d.page} | {d.raw} | {'yes' if d.ok else 'NO — ' + d.reason} | {snippet} |")
    lines.append("")

    # --- Numbers ---
    topical = [n for n in number_mentions if n.topics]
    mismatches = [n for n in topical if n.status == "check"]
    lines.append(
        f"## Numbers with tracked topics ({len(topical)} found, "
        f"{len(mismatches)} need manual check)"
    )
    lines.append("")
    if topical:
        lines.append("| page | value | topics | status | ground truth | sentence |")
        lines.append("|---|---|---|---|---|---|")
        for n in topical:
            snippet = n.sentence.replace("\n", " ")[:140]
            status = "OK" if n.status == "ok" else "CHECK"
            lines.append(
                f"| {n.page} | {n.raw} | {', '.join(n.topics)} | {status} | {n.note} | {snippet} |"
            )
    lines.append("")

    other_numbers = [n for n in number_mentions if not n.topics]
    lines.append(f"## Other numbers found ({len(other_numbers)}, informational only)")
    lines.append("")
    lines.append("<details><summary>expand</summary>")
    lines.append("")
    lines.append("| page | value | sentence |")
    lines.append("|---|---|---|")
    for n in other_numbers:
        snippet = n.sentence.replace("\n", " ")[:140]
        lines.append(f"| {n.page} | {n.raw} | {snippet} |")
    lines.append("")
    lines.append("</details>")
    lines.append("")

    # --- Ground truth reference tables ---
    lines.append("## Ground truth reference")
    lines.append("")
    lines.append(f"- num_sessions (index.json): {gt.get('num_sessions')}")
    lines.append(f"- num_transcripts (titles.json): {gt.get('num_transcripts')}")
    lines.append(f"- total_user_turns (sum over sessions): {gt.get('total_user_turns')}")
    lines.append(f"- total_tool_uses (sum over sessions): {gt.get('total_tool_uses')}")
    lines.append(f"- num_subagent_files (build/parsed/subagents/*.json): {gt.get('num_subagent_files')}")
    lines.append(f"- num_chapters (chapters.json): {gt.get('num_chapters')}")
    lines.append(f"- num_scenes (max scene in chapters.json): {gt.get('num_scenes')}")
    lines.append(f"- total_commits (git log, autoroad repo): {gt.get('total_commits')}")
    lines.append("")
    lines.append("### Commits per day (UTC)")
    lines.append("")
    lines.append("| date | commits |")
    lines.append("|---|---|")
    for day, c in gt.get("commits_utc", {}).items():
        lines.append(f"| {day} | {c} |")
    lines.append("")
    lines.append("### Commits per day (local time of this machine)")
    lines.append("")
    lines.append("| date | commits |")
    lines.append("|---|---|")
    for day, c in gt.get("commits_local", {}).items():
        lines.append(f"| {day} | {c} |")
    lines.append("")

    # --- Banned content ---
    lines.append(f"## Banned content ({len(banned_hits)} hits)")
    lines.append("")
    if banned_hits:
        lines.append("| page | line | kind | detail |")
        lines.append("|---|---|---|---|")
        for h in banned_hits:
            lines.append(f"| {h.page} | {h.line} | {h.kind} | {h.detail} |")
    else:
        lines.append("No spoilers, em dashes, semicolons, private paths, or disallowed URLs found.")
    lines.append("")

    return "\n".join(lines) + "\n"


def run() -> str:
    pages = read_pages()
    link_results = check_links(pages)
    number_mentions, date_mentions = extract_numbers(pages)
    gt = load_ground_truth()
    cross_check_numbers(number_mentions, gt)
    spoiler_terms = load_spoilers()
    banned_hits = check_banned(pages, spoiler_terms)
    report = render_report(pages, link_results, number_mentions, date_mentions, banned_hits, gt)
    out_path = REPO_ROOT / "build" / "writing-check" / "prepass.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report)
    return report


if __name__ == "__main__":
    print(run())
