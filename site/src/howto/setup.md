# Setting up: Claude Code, a folder, and a repository

This page is for readers who have never opened a terminal and would like to try what the rest of this section describes. It assumes nothing. If you already use Claude Code, skip to [the next page](voice-first.md).

## What David actually used

David ran everything from the command line on a Mac, in a terminal window, using the Claude Code command-line tool on a Claude Max subscription. His novel was a folder of plain text files in Markdown format, kept under git version control, and every conversation in the transcripts on this site happened inside that folder. That is the setup the transcripts show. It is not the only one that works, and for most people starting today it is probably not the easiest.

## The easier route: the desktop app

Claude Code also comes as a desktop application for macOS and Windows, with a Linux version in beta at the time of writing. It runs the same engine as the command-line tool, so everything on this site applies to it, but it does not require a terminal. You open a project folder in it, type in a chat panel, and review the changes it makes to your files visually. It can handle git for you if you ask. For someone whose interest is the writing rather than the tooling, this is the version to start with. It is available from https://claude.ai/code.

The one thing you give up is that the command line makes it slightly easier to run the small scripts described in the [checks page](checks.md). In practice the model writes and runs those for you either way, so the difference is smaller than it sounds.

## What you need

An account with Claude Code access. At the time of writing that means a Claude Pro or Max subscription, a Team or Enterprise plan, or pay-as-you-go API credits through the Claude Console. The free tier does not include it. Plan names and limits change, so check https://claude.com/pricing rather than trusting this page. Usage is metered in rolling windows, and a project like this one runs through a good deal of it, which is why David was on the largest individual plan and still watched his budget.

A computer with a folder you can dedicate to the project. Nothing else. Git, the version-control tool, is usually already present on a Mac and can be installed on Windows from https://git-scm.com. If it is missing, Claude Code will tell you and can usually talk you through installing it.

## Steps

1. Install Claude Code. For the desktop app, download it from https://claude.ai/code and sign in. For the command line, the current recommended installers are documented at https://code.claude.com/docs/en/setup and are a single command pasted into a terminal. On a Mac, the terminal is the application called Terminal, found with Spotlight search.

2. Make a folder for the project and open Claude Code in it. In the desktop app that means choosing the folder. In a terminal it means typing `cd` followed by the folder's path, then `claude`. Everything the model does happens inside this folder unless you say otherwise, which is the point of having one.

3. Have your first conversation. Say what you want to make and ask the model to set the project up as a git repository with a short instructions file. Claude Code's built-in `/init` command will draft that file, called `CLAUDE.md`, for you. The [write it down page](write-it-down.md) explains what should go in it. You do not need to know any git commands. Asking "commit what we have so far with a sensible message" is enough, and the model will do it.

4. Learn the permission prompt. Claude Code asks before it changes files or runs commands, and in its default mode on a subscription plan it approves the obviously safe actions itself and asks about the rest. If you find yourself approving everything, that is normal at first. A plan mode also exists in which the model describes what it would do without doing it, which is useful while you are learning to trust it. The modes are switched with Shift and Tab together, and documented at https://code.claude.com/docs/en/permission-modes.

5. Learn how to come back. Sessions end when you close the window. To pick one up later, the `/resume` command lists previous conversations, and from a terminal `claude -c` continues the most recent one in that folder. Even so, do not rely on this. The project's habit of writing state into files exists because a resumed conversation is not the same as a remembered one, and the [handoff page](../workflow/next-md-handoff.md) describes how to make a fresh session productive in a minute.

## Where the transcripts on this site came from

Claude Code keeps a record of every session on your own computer, in a hidden folder in your home directory called `.claude`. The transcripts published here were generated from David's copy of that folder by scripts, redacted, and rendered. If you want to do the same thing for your own project, the model can build the scripts for you, and the source of this site is public at https://github.com/DRMacIver/llm-fiction-case-study as a worked example. Be careful: those records contain everything, including the full text of every file the model wrote, so publish them only after checking what is in them.

## If you get stuck

Ask the model. That sounds glib but it is the honest answer and the one the transcripts show David using. Claude Code can explain what a terminal is, why a command failed, and what a permission prompt means, and asking it costs nothing but a little of your usage. The first hour is the hardest, and most of the difficulty is the unfamiliarity of the surroundings rather than anything about the writing.
