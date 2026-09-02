# The commenter tool

Reading a chapter draft in a terminal and reading it as prose are different activities, and the project built a small local web app, launched from `tools/commenter/server.py`, specifically so David could do the second one properly: a three-pane page with a file list on the left, rendered prose in the middle, and comment threads on the right, running entirely on his own machine.

## Anchoring comments to text that keeps changing

The obvious hard problem for a tool like this is that the prose it's commenting on isn't static. A comment left on a specific sentence needs to still point at that sentence after the sentence has been edited, possibly more than once, in response to that very comment or to something else entirely. The commenter stores each comment with a redundant anchor: a line and column position, the exact text that was originally selected, and about 160 characters of surrounding context on each side, rather than relying on any single one of these being enough.

When prose is edited, an anchor is re-resolved against the current text using a tiered strategy: try an exact match first, then look for the quoted text having moved elsewhere in the file with its surrounding context intact, then a fuzzy match that ignores whitespace differences, and finally mark the comment as orphaned if none of these work. A specific bug surfaced during the project and got fixed with a dedicated regression test: short selections were relocating to the wrong occurrence of the same short phrase elsewhere in the file, because the original matching logic treated context as all-or-nothing rather than scoring how much of the stored context actually survived around each candidate location. The fix scores matches per character, so an edit far away from the original quote costs the match little, while an edit right next to it costs a lot, which is closer to how a human would judge whether a comment still applies to the same spot.

## How comments flow back into drafting

Comments are stored as JSON, one file per chapter, each entry carrying a creation timestamp, the comment body, a resolved flag, and its anchor. A drafting session checks for unresolved comments with a small utility that acknowledges them as read, works through each one, and marks it resolved once addressed. After every edit made in response to a comment, the session is expected to re-read the surrounding lines for consequences the edit might have caused elsewhere in the same passage.

One rule the project settled on partway through is that a comment left twice on the same passage, even reworded, is a verdict on the underlying device rather than on its phrasing: rewording the sentence won't satisfy a second comment in the same place, because the actual construction needs restructuring or removing, not polishing. This distinguishes a comment tool used as a line-edit checklist from one used, as here, as a running record of which craft decisions actually held up under a real read.
