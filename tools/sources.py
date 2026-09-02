"""Shared source-profile config for the transcript pipeline.

tools/sources.json describes each transcript source the pipeline knows how
to process: where its raw Claude Code jsonl transcripts live, where its
parsed/redacted/rendered output should go, and a small "profile" switch
(``full`` vs ``meta``) that tools/redact.py uses to decide which redaction
passes apply.

- ``autoroad``: the novel project's own transcripts. Unchanged behaviour --
  full redaction profile (terms, hard-spoiler topics, scene-number and
  unpublished-path tagging, the unpublished-prose guard, the premise-reveal
  cutoff that keeps full pre-cutoff tool content).
- ``meta``: this project's own transcripts (site/src/meta/transcripts).
  Lighter profile -- private-information redaction plus the term list and
  the hard-spoiler topic regexes (both fire rarely here), but no prose
  guard, no scene-number/unpublished-path tagging, no premise cutoff
  (everything here postdates the novel's premise reveal), and file
  contents are never kept. An anonymisation map is also applied first,
  everywhere in this source, replacing a short list of unrelated-project
  identifiers with a placeholder token.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent
SOURCES_PATH = TOOLS_DIR / "sources.json"

DEFAULT_ANON_PLACEHOLDER = "«OTHER-PROJECT»"


@dataclass
class SourceConfig:
    name: str
    transcripts_dir: Path
    repo_root: str
    out_dir: Path
    site_dir: Path
    summary_marker: str
    summary_prefix: str
    profile: str  # "full" | "meta"
    premise_cutoff: bool
    keep_file_contents: bool
    user_label: str = "David"
    anonymize: list[str] = field(default_factory=list)
    anonymize_placeholder: str = DEFAULT_ANON_PLACEHOLDER

    @property
    def parsed_dir(self) -> Path:
        return self.out_dir / "parsed"

    @property
    def redacted_dir(self) -> Path:
        return self.out_dir / "redacted"


def _expand(p: str) -> Path:
    return Path(p).expanduser()


def load_sources(path: Path = SOURCES_PATH) -> dict[str, SourceConfig]:
    raw = json.loads(path.read_text())
    out: dict[str, SourceConfig] = {}
    for name, cfg in raw["sources"].items():
        out[name] = SourceConfig(
            name=name,
            transcripts_dir=_expand(cfg["transcripts_dir"]),
            repo_root=cfg["repo_root"],
            out_dir=(REPO_ROOT / cfg["out_dir"]),
            site_dir=(REPO_ROOT / cfg["site_dir"]),
            summary_marker=cfg["summary_marker"],
            summary_prefix=cfg.get("summary_prefix", ""),
            profile=cfg.get("profile", "full"),
            premise_cutoff=bool(cfg.get("premise_cutoff", True)),
            keep_file_contents=bool(cfg.get("keep_file_contents", True)),
            user_label=cfg.get("user_label", "David"),
            anonymize=list(cfg.get("anonymize", [])),
            anonymize_placeholder=cfg.get("anonymize_placeholder", DEFAULT_ANON_PLACEHOLDER),
        )
    return out


def load_source(name: str, path: Path = SOURCES_PATH) -> SourceConfig:
    sources = load_sources(path)
    if name not in sources:
        raise KeyError(f"unknown source {name!r}; known sources: {sorted(sources)}")
    return sources[name]
