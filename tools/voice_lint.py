#!/usr/bin/env python3
"""Mechanical voice lint for autoroad-howto site pages.

Ported from hegel-blog-post/.claude/skills/voice-pass/voice_lint.py (the
regex/metric tiers) and autoroad/tools/lint/rules.json (the regex tier),
adapted to notes/voice-devices.md — this site's own catalogue of devices to
hunt, since the narrator here is the pipeline in the third person, not
David in the first person. See notes/voice-devices.md for the rationale
behind each rule and which devices are judgement-only (not attempted here).

Deterministic checks only. Judgement calls (cadence, structure-level
devices like a paragraph opening by announcing its point, a too-neat
closing recontextualisation) are explicitly out of scope; see
notes/voice-devices.md for those.

Usage:
  python3 tools/voice_lint.py <file.md> [<file.md> ...]
  python3 tools/voice_lint.py --all      # every page under site/src/

Output tiers:
  FAIL   - fix outright (zero-tolerance vocabulary, banned constructions)
  REVIEW - often fine, sometimes a tell; eyeball each hit
  INFO   - statistics for a human/model pass to interpret

Prose only: fenced code blocks, inline code spans, and link targets are
stripped before matching.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SITE_SRC = REPO_ROOT / "site" / "src"

PAGES_UNDER_CHECK = [
    SITE_SRC / "introduction.md",
    SITE_SRC / "about.md",
    *sorted((SITE_SRC / "howto").glob("*.md")),
    *sorted((SITE_SRC / "workflow").glob("*.md")),
    *sorted((SITE_SRC / "chronicle").glob("*.md")),
]

# ---------------------------------------------------------------------------
# Rule tiers. See notes/voice-devices.md for the device catalogue each rule
# corresponds to (device numbers referenced in comments).
# ---------------------------------------------------------------------------

FAIL_PATTERNS = [
    # Zero-tolerance vocabulary (voice.md §7 / llm-tells.md / rules.json).
    (r"\bdelv(e|es|ed|ing) into\b", "LLM staple ('delve into')"),
    (r"\btapestry\b", "LLM staple"),
    (r"\btestament to\b", "LLM staple"),
    (r"\bin today's\b", "LLM staple"),
    (r"\bnavigat\w* the \w+ landscape\b", "LLM staple"),
    (r"\bgame.chang\w+\b", "LLM staple"),
    (r"\bseamless\w*\b", "LLM staple"),
    (r"\belevat\w+ your\b", "LLM staple"),
    (r"\bkey takeaways?\b", "LLM staple"),
    (r"\bintricate\b", "LLM staple"),
    (r"\bpivotal\b", "LLM staple"),
    (r"\bunderscore[sd]?\b", "LLM staple (verb use)"),
    (r"\bnestled\b", "LLM staple"),
    (r"\bvibrant\b", "LLM staple"),
    (r"\bprofound(ly)?\b", "LLM staple"),
    (r"\bmyriad\b", "LLM staple"),
    (r"\bearn\w* (?:its|their|his|her|your|our) keep\b",
     "stock idiom of justification (device 14)"),
    (r"\bannounc\w+ (?:it|him|her|them|itself|themselves)\b",
     "dramatised absence of signal (device 13)"),
    (r"\bserves? as (?=(a|an|the)\b)|\bstands? as (?=(a|an|the)\b)"
     r"|\bboasts?\b|\bfeatures (?=(a|an|the|two|three|four|five|six|several|some)\b)",
     "copula avoidance / marketing verb, 'is'/'has' would do (device 10)"),
    (r"\bin the plain sense\b", "hedge-qualifier that adds nothing (device 6)"),
    (r"\bwhich is most of why\b", "hedge-qualifier construction (device 7)"),
]

REVIEW_PATTERNS = [
    # Words that are sometimes fine but are also LLM staples; eyeball each.
    (r"\bleverag\w+\b", "usually 'use' works instead"),
    (r"\brobust\w*\b", "LLM staple unless technically load-bearing"),
    (r"\bcrucial\w*\b", "consider 'important' or showing it instead"),
    (r"\bnotably\b|\bimportantly\b|\bit'?s worth not(?:ing|icing)\b"
     r"|\bworth not(?:ing|icing)\b",
     "importance-narration; make the statement instead (device 5)"),
    (r"\bload.bearing\b|\bdoing all the work\b|\bdoes the heavy lifting\b",
     "meta-dramatising importance (device 4)"),
    (r"\bhere'?s? (?:what|the thing)\b|\bhere is what\b",
     "staged-reveal framing (device 9)"),
    (r"\bthis is the part\b|\bthis is where\b",
     "'This is the part that...' announces significance (device 19)"),
    (r"\barguably\b",
     "'arguably' needs at least a gesture at the argument, same sentence"),
    (r"\b(arguably|probably|possibly) (worse|better|harder|easier) than\b",
     "hedged comparison — check the argument is gestured at, not just the hedge"),
    (r"\b(?:not\s+[^,.;:!?]{2,45},\s*but\s+(?!(he|she|it|they|we|i|you|there|the)\b))",
     "negative parallelism 'not X, but Y' (device 2)"),
    (r"\b(It|That|This|He|She|They)\s+(wasn't|isn't|weren't|aren't|was not"
     r"|is not|were not)\b[^.?!]{1,70}[.]\s+\1\s+(was|is|were|are)\b",
     "negative parallelism, split-sentence form (device 2)"),
    (r"—", "em dash — budget a couple per page at most (device 11)"),
    (r";", "semicolon — recast as two sentences or join with and/but (device 12)"),
    (r"\bsilently\b|\bnever announced itself\b|\bquietly collapsed\b",
     "dramatised absence of signal (device 13)"),
    (r"\bas (?:mentioned|noted) (?:above|earlier)\b",
     "self-quotation callback (device 23)"),
    (r"\bthere are (?:two|three|four|five) reasons\b"
     r"|\b(?:two|three|four|five) things (?:go wrong|happen)\b",
     "over-signposting the structure (device 22)"),
    (r"(?:^|(?<=[.!?] ))(Measured|Tested|Simulated|Sampled|Verified|Run|Ran),?\s",
     "possible verbless report fragment; give it a subject and finite verb (device 25)"),
    (r"\bhonest (?:account|list|inquiry|diagram|disagreement|answer)\b",
     "narrator-approval tic ('honest [noun]')"),
    (r",\s*which\s+(was|is|were|had been)\s+(new|good|the mistake|a mistake"
     r"|not nothing|something|the point|tact)\b"
     r"|,\s*which\s+took some doing"
     r"|,\s*which\s+cost\s+(?:him|her|them|it)\s+something",
     "sentence-final verdict clause (device 3)"),
]

# Note: "introduction" is deliberately excluded — this site uses it as a
# literal, legitimate page title (site/src/introduction.md), unlike a blog
# post's throwaway "## Introduction" section header.
GENERIC_HEADERS = re.compile(
    r"^#{2,6}\s*(conclusion|summary|final thoughts|key takeaways)\s*$",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Prose stripping and matching
# ---------------------------------------------------------------------------

def strip_prose(text: str) -> list[str]:
    """Return prose lines: code fences, inline code, and link targets blanked."""
    out = []
    in_fence = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            out.append("")
            continue
        if in_fence:
            out.append("")
            continue
        line = re.sub(r"`[^`]*`", "`_`", line)
        line = re.sub(r"\]\([^)]*\)", "](_)", line)
        out.append(line)
    return out


def matches(pattern: str, lines: list[str]) -> list[tuple[int, str, str]]:
    rx = re.compile(pattern, re.IGNORECASE)
    hits = []
    for i, line in enumerate(lines, 1):
        for m in rx.finditer(line):
            hits.append((i, m.group(0), line.strip()))
    return hits


@dataclass
class Finding:
    tier: str
    line: int
    fragment: str
    note: str
    quote: str


@dataclass
class PageReport:
    path: Path
    findings: list[Finding] = field(default_factory=list)
    info: list[str] = field(default_factory=list)
    failed: bool = False


def lint_text(path: Path, text: str) -> PageReport:
    report = PageReport(path=path)
    prose = strip_prose(text)
    prose_text = "\n".join(prose)
    words = re.findall(r"[A-Za-z']+", prose_text)
    n_words = len(words)

    def add(tier: str, hits: list[tuple[int, str, str]], note: str) -> None:
        if not hits:
            return
        if tier == "FAIL":
            report.failed = True
        for lineno, frag, line in hits:
            report.findings.append(Finding(tier, lineno, frag, note, line[:160]))

    for pat, note in FAIL_PATTERNS:
        add("FAIL", matches(pat, prose), note)

    # Chronicle pages use a bold lede line as a deliberate section-header
    # convention (device 20) — REVIEW tier, not FAIL, pending a human call on
    # whether that convention itself is a tell. Bold elsewhere in running
    # prose (not a whole-sentence lede) is the tell voice.md actually means.
    add("REVIEW", matches(r"\*\*[^*\n]+\*\*", prose),
        "bold emphasis; check whether this is prose-emphasis (a tell — italics "
        "only) or a chronicle lede-line convention (device 20)")

    for i, line in enumerate(prose, 1):
        if GENERIC_HEADERS.match(line):
            add("FAIL", [(i, line.strip(), line.strip())], "generic header")

    for pat, note in REVIEW_PATTERNS:
        add("REVIEW", matches(pat, prose), note)

    # Rule-of-three: parenthetical with two commas and no "and" before the
    # last item (device 21), approximate and REVIEW-tier by design.
    add("REVIEW", matches(r"\([^()]+,[^()]+,[^()]+\)", prose),
        "parenthetical list of three — check it isn't padded for cadence "
        "(device 21)")

    # Triad-with-swerve at sentence scale: three comma-separated clauses
    # ending a sentence (device 1), approximate and REVIEW-tier.
    add("REVIEW",
        matches(r"[A-Za-z][^,.;:!?()]{3,40},\s*[A-Za-z][^,.;:!?()]{3,40},"
                r"\s*(?:and\s+)?[A-Za-z][^,.;:!?()]{3,40}[.!?]", prose),
        "possible rule-of-three sentence — check the items are substantively "
        "distinct, not rhythm padding (device 1)")

    # INFO statistics.
    dashes = len(re.findall(r"—", prose_text))
    semicolons = prose_text.count(";")
    hyph = len(re.findall(r"[A-Za-z]-[A-Za-z]", prose_text))
    adverbs = len(re.findall(r"\b\w+ly\b", prose_text, re.IGNORECASE))
    sentences = [s.strip() for s in re.split(r"[.!?]+\s", prose_text) if s.strip()]
    slens = [len(re.findall(r"[A-Za-z']+", s)) for s in sentences]
    slens = [n for n in slens if n > 0]

    report.info.append(
        f"words: {n_words}; em dashes: {dashes} "
        f"({dashes * 1000 / max(n_words, 1):.1f}/1000w)")
    report.info.append(
        f"semicolons: {semicolons} ({semicolons * 1000 / max(n_words, 1):.1f}/1000w)")
    report.info.append(
        f"hyphen-compounds: {hyph} ({hyph * 1000 / max(n_words, 1):.1f}/1000w) "
        f"(device 26)")
    report.info.append(
        f"-ly adverbs: {adverbs} ({adverbs * 1000 / max(n_words, 1):.1f}/1000w) "
        f"(device 27)")
    if slens:
        short = sum(1 for n in slens if n <= 4)
        report.info.append(
            f"sentences: {len(slens)}, mean {sum(slens) / len(slens):.1f} words, "
            f"{short} of <=4 words")

    return report


def lint_file(path: Path) -> PageReport:
    return lint_text(path, path.read_text(encoding="utf-8"))


def print_report(report: PageReport) -> None:
    rel = report.path
    try:
        rel = report.path.relative_to(REPO_ROOT)
    except ValueError:
        pass
    print(f"=== {rel} ===")
    for f in report.findings:
        print(f"{f.tier}  L{f.line}: '{f.fragment}' ({f.note})")
        print(f"       > {f.quote}")
    for line in report.info:
        print(f"INFO  {line}")
    if not any(f.tier == "FAIL" for f in report.findings):
        print("OK    no FAIL-tier findings")
    print()


def main(argv: list[str]) -> int:
    if not argv or argv == ["--all"]:
        paths = PAGES_UNDER_CHECK
    else:
        paths = [Path(a) for a in argv]

    any_failed = False
    for path in paths:
        report = lint_file(path)
        print_report(report)
        if report.failed:
            any_failed = True
    return 1 if any_failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
