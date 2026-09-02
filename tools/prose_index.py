"""Build a shingle index of unpublished (and published) story prose.

Term/topic redaction in ``redact.py`` catches specific spoiler names and
regex patterns, but it can't catch a transcript that quotes a verbatim
*sentence* from a story file that was never published, without naming any
of the spoiler terms. This module builds a deterministic index of hashed
7-word "shingles" (normalised: lowercase, strip punctuation, collapse
whitespace) drawn from every unpublished story text we know about, plus a
separate index of the same shingles drawn from the *published* scenes
(1-40), so ``redact.py`` can distinguish "quotes published prose" (fine)
from "quotes unpublished prose" (must be redacted).

Unpublished sources indexed:

- ``draft/book-01/scenes/`` numbered above 40 (current working tree)
- everything under ``plans/`` (current working tree)
- ``notes/theme.md``, ``notes/concept.md``, ``notes/premise.md``,
  ``notes/canon/**`` (current working tree)
- ``summaries/`` (current working tree)
- every ``*.md`` blob that ever existed under the now-deleted ``chapters/``,
  ``rewrite/`` and ``draft/book-01/rejected-act2/`` trees, enumerated from
  git history (``git rev-list --all --objects``) and read with
  ``git show`` / ``git cat-file`` -- these paths don't exist in the working
  tree at all, only as historical blobs.

Published source indexed separately:

- ``draft/book-01/scenes/`` numbered 1-40 (current working tree)

The index stores only hashes of normalised shingles -- never the story text
itself -- so it's safe to pickle into ``build/`` (gitignored) without
leaking prose into this repo.

Run directly to (re)build ``build/prose-index.pkl``. Invoke via ``-c`` rather
than ``-m`` so the pickled ``ProseIndex`` class records its real module path
(``tools.prose_index``) rather than ``__main__``, which would make it
unloadable from any other module::

    uv run python -c "from tools.prose_index import main; main()"
"""
from __future__ import annotations

import hashlib
import pickle
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = REPO_ROOT / "build"
INDEX_PATH = BUILD_DIR / "prose-index.pkl"

AUTOROAD_ROOT = Path("/Users/drmaciver/Projects/autoroad")

SHINGLE_SIZE = 7  # words; sentences under this many words can't match.

SCENE_THRESHOLD = 40
SCENES_DIR = AUTOROAD_ROOT / "draft" / "book-01" / "scenes"
SCENE_FILE_RE = re.compile(r"^0*([0-9]{1,4})-.*\.md$")

# Working-tree paths (relative to AUTOROAD_ROOT) indexed as unpublished.
UNPUBLISHED_TREE_GLOBS = [
    "plans/**/*.md",
    "notes/theme.md",
    "notes/concept.md",
    "notes/premise.md",
    "notes/canon/**/*.md",
    "summaries/**/*.md",
]

# Trees that no longer exist in the working tree at all -- only reachable
# via git history -- enumerated by blob.
DELETED_TREE_PREFIXES = [
    "chapters/",
    "rewrite/",
    "draft/book-01/rejected-act2/",
]

_PUNCT_RE = re.compile(r"[^\w\s]", re.UNICODE)
_WS_RE = re.compile(r"\s+")


def normalise(text: str) -> str:
    text = text.lower()
    text = _PUNCT_RE.sub(" ", text)
    text = _WS_RE.sub(" ", text)
    return text.strip()


def shingle_hashes(text: str, n: int = SHINGLE_SIZE) -> set[bytes]:
    """Normalise `text` and return the set of hashed n-word shingles."""
    words = normalise(text).split(" ")
    words = [w for w in words if w]
    if len(words) < n:
        return set()
    out = set()
    for i in range(len(words) - n + 1):
        shingle = " ".join(words[i : i + n])
        out.add(hashlib.blake2b(shingle.encode("utf-8"), digest_size=8).digest())
    return out


@dataclass
class ProseIndex:
    shingle_size: int
    unpublished: set = field(default_factory=set)
    published: set = field(default_factory=set)
    # bookkeeping only, for reporting -- no story text.
    unpublished_source_count: int = 0
    published_source_count: int = 0

    def save(self, path: Path = INDEX_PATH) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as fh:
            pickle.dump(self, fh)

    @classmethod
    def load(cls, path: Path = INDEX_PATH) -> "ProseIndex":
        with open(path, "rb") as fh:
            return pickle.load(fh)


def _scene_number(name: str) -> int | None:
    m = SCENE_FILE_RE.match(name)
    if not m:
        return None
    return int(m.group(1))


def _iter_current_scenes() -> tuple[list[Path], list[Path]]:
    """Return (published_paths, unpublished_paths) from the working tree."""
    published, unpublished = [], []
    if not SCENES_DIR.is_dir():
        return published, unpublished
    for p in sorted(SCENES_DIR.glob("*.md")):
        n = _scene_number(p.name)
        if n is None:
            continue
        if n <= SCENE_THRESHOLD:
            published.append(p)
        else:
            unpublished.append(p)
    return published, unpublished


def _iter_unpublished_tree_files() -> list[Path]:
    out: list[Path] = []
    seen: set[Path] = set()
    for pattern in UNPUBLISHED_TREE_GLOBS:
        for p in sorted(AUTOROAD_ROOT.glob(pattern)):
            if p.is_file() and p not in seen:
                seen.add(p)
                out.append(p)
    return out


def _iter_deleted_tree_blobs() -> list[tuple[str, str]]:
    """Return [(path, blob_sha)] for every distinct .md blob that ever
    existed under DELETED_TREE_PREFIXES, across all commits in the
    autoroad repo's full history. Deduped by (path, blob_sha) pair as
    emitted by git (which is already content-addressed, so re-added
    identical content across commits collapses automatically)."""
    cmd = [
        "git",
        "-C",
        str(AUTOROAD_ROOT),
        "rev-list",
        "--all",
        "--objects",
        "--",
        *DELETED_TREE_PREFIXES,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    out: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for line in result.stdout.splitlines():
        parts = line.split(" ", 1)
        if len(parts) != 2:
            continue  # a tree/commit object printed with no path, or root
        sha, path = parts
        if not path.endswith(".md"):
            continue
        if not any(path.startswith(prefix) for prefix in DELETED_TREE_PREFIXES):
            continue
        key = (path, sha)
        if key in seen:
            continue
        seen.add(key)
        out.append(key)
    return out


def _read_blob(sha: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(AUTOROAD_ROOT), "cat-file", "-p", sha],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def build_index(n: int = SHINGLE_SIZE) -> ProseIndex:
    index = ProseIndex(shingle_size=n)

    published_paths, unpublished_scene_paths = _iter_current_scenes()
    for p in published_paths:
        index.published |= shingle_hashes(p.read_text(errors="replace"), n)
        index.published_source_count += 1

    for p in unpublished_scene_paths:
        index.unpublished |= shingle_hashes(p.read_text(errors="replace"), n)
        index.unpublished_source_count += 1

    for p in _iter_unpublished_tree_files():
        index.unpublished |= shingle_hashes(p.read_text(errors="replace"), n)
        index.unpublished_source_count += 1

    for _path, sha in _iter_deleted_tree_blobs():
        try:
            text = _read_blob(sha)
        except subprocess.CalledProcessError:
            continue
        index.unpublished |= shingle_hashes(text, n)
        index.unpublished_source_count += 1

    return index


def main() -> None:
    index = build_index()
    index.save()
    print(
        f"prose index: {index.unpublished_source_count} unpublished sources -> "
        f"{len(index.unpublished)} shingles; {index.published_source_count} "
        f"published sources -> {len(index.published)} shingles "
        f"(shingle size {index.shingle_size}); saved to {INDEX_PATH}"
    )


if __name__ == "__main__":
    main()
