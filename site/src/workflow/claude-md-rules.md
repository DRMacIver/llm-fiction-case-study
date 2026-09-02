# The CLAUDE.md rule system

Every Claude Code session in the autoroad project starts by reading a `CLAUDE.md` file at the project root, which is Claude Code's convention for standing instructions that load automatically. Autoroad's version is short but pointed: it lists, in order, which files a session must read before writing any fiction at all, and it says why the order matters.

The list starts with the voice exemplars and the prose the model is meant to imitate, not the rules describing that prose, on the reasoning that rules alone let a session satisfy the letter of a constraint while still sounding like default machine-written prose. Only after the exemplars come the working voice rules, the LLM-tells catalogue, the story's premise and hard limits, and the canon files. A separate section, "start here after a context loss," points at `plans/NEXT.md` as the place a fresh session should read to recover where the project stands, since Claude Code sessions don't retain memory between conversations.

The file also carries structural facts that would otherwise have to be rediscovered every session: where the current draft lives, that older drafts were deleted from the working tree but remain in git history for the [overlap checker](overlap-checking.md) to read, and where the claim-level conventions for [canon](canon-and-claim-levels.md) are defined.

## Why a file, not a person repeating instructions

A one-off instruction given in conversation only binds that conversation. Claude Code sessions do not share memory, so a rule that matters for every session, not just the current one, has to live somewhere a fresh session will read it unprompted. `CLAUDE.md` is that place. The file is committed to the repository like any other project asset, and edits to it show up in git history the same way edits to the prose do.

This also makes the rule system itself an artefact of the project's own revision process. Several of `CLAUDE.md`'s current rules exist because an earlier session got something wrong in a way worth preventing permanently. The instruction that sealed answers to unresolved mysteries may only be written by a subagent, for instance, and never disclosed to David except on request, is a direct response to a specific failure: a mystery got introduced on the page with no written answer behind it, evidence accumulated around it across several chapters, and nobody had actually decided what the answer was. The fix wasn't "write better next time," it was a standing rule that the state the earlier session had drifted into is no longer reachable at all.

## Layering with other rule files

`CLAUDE.md` is deliberately thin. It points at longer files rather than restating them: the voice rules live in `notes/voices.md`, the tells catalogue in `notes/llm-tells.md`, the farming policy in `notes/farming.md`, the binding draft method in `draft/book-01/VOICE.md`. This keeps the entry point readable while letting each subsystem's rules grow and get amended independently, with their own dated rulings at the bottom of the file recording when and why something changed. The pattern recurs throughout the project: a short binding pointer file, and longer working documents underneath it that the pointer names in the order they need to be read.

The session that set the project's premise and much of the initial `CLAUDE.md` structure is [2026-08-24, finding the voice and starting the draft](../transcripts/0c653b33-1efd-45bb-b7ab-26ed3dca981e.md).
