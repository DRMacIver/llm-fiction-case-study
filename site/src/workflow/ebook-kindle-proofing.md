# The ebook and Kindle proofing loop

Before a chapter goes anywhere near Royal Road, David reads it, and for a project this size he reads a fair amount of it on a Kindle rather than on a screen. Getting a current draft onto the device turned out to need its own small pipeline, mostly because the obvious approach, dropping a fresh file on the Kindle and reading from the start, throws away reading position every time the book changes underneath the reader.

## Collating and building

The chapter files live as individual scene and chapter markdown files, so the first step gathers them into a single ordered sequence. That's `collate_book.py`: it validates that chapter numbering has no gaps or duplicates, counts body words after stripping author's notes and headings, and writes an index file summarising word counts by arc.

`build_ebook.py` then takes the collated chapters and produces both an EPUB and a Kindle-native AZW3 file, using pandoc for the format conversion and Calibre for the Kindle-specific step. Along the way it inserts arc headings, formats author's notes distinctly from story text, and applies CSS so that scene breaks render as centred asterisks rather than as a raw HTML rule.

AZW3 is used rather than the older MOBI format, because MOBI pagination is known to freeze on the device's current firmware when a book is updated in place. So AZW3 was built in from the start rather than kept as a fallback for when MOBI caused trouble.

## Carrying reading position across an edit

Most edits during a live draft change some earlier chapter too, not just the part being actively written. The Kindle stores a reading position as a byte offset into the book file, which becomes meaningless the moment a single word changes anywhere before that point.

`kindle_position.py` handles this by falling back through four levels, each one used only if the one before it fails. First it tries to find an exact, unique span of at least 300 characters of unchanged text around the stored position, and uses its new offset. If the surrounding chapter has changed too much for that, it diffs the old and new chapter text and remaps the byte offset through the diff, as long as the chapter is still similar enough overall. If the chapter itself is gone or transformed past recognition, it falls back to the start of the chapter with the same title, and if even that is gone, to the start of the book.

The whole read-and-remap step happens before anything gets written to the device, so a failure partway through leaves the Kindle in its previous working state. `update-kindle.py` ties the pieces together: convert, write the new file to the device, regenerate the pagination index that the device itself relies on for page-turn timing (a stale index is the other common cause of freezes), carry the reading position across using the remapping logic, and clean up the stray filesystem artefacts that macOS leaves behind when writing to an external volume.

The pipeline started as a single script, built in one sitting once the need for it became obvious, and grew afterwards into the separate collating, building, and position-carrying steps described above: [2026-08-25, syncing the book to a Kindle](../transcripts/92c486ed-62f3-40a9-8d7d-b9dd6554d07e.md).
