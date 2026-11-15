# Personal AI Work System (PAWS) v1.0

> **Start here**
>
> 1. Open this folder in the AI app or command-line tool you want to use. It needs to read and save files here.
> 2. Paste this line: **You are the Architect. Please set up this workspace by following Setup/SETUP.md.**
> 3. Answer the few questions it asks. When setup ends you are already working.

PAWS gives your AI helpers set jobs, one place for projects and dates, and a written record that a later session can pick up. It is a folder of plain Markdown files. Nothing runs in the background and nothing connects to your accounts.

Use of this starter is covered by the [PAWS Public Starter License](LICENSE.md). Names and credits are in the [NOTICE](NOTICE.md).

## What setup does

The Architect runs setup as itself, in a real first session. It shows you what the Builder already saved, asks only what is missing, and lets you skip the extras. It also asks what your helpers may do without asking you, and writes that on [Boundaries](Boundaries.md). Those are instructions your helpers are asked to follow, not a lock, so keep backups of anything that matters. Anything you mention along the way, like an idea, a project or a date, goes straight into the [Daily Note](Daily%20Note.md) and is still there when setup ends. When you say finish, it saves the changes and carries on with your first real job. There is no second session.

## Your units

- `Executive Unit/`: the executive unit. It keeps the shared rules, with the Architect.
- `Hub Unit/`: the hub unit. It keeps projects, the calendar and the Daily Note, with the Secretary.
- `Example Unit/`: one unit for a subject you choose, with its unit lead.

Every unit has the same standard rooms, listed in the layout part of Workspace Settings. Folder names come from your choices, and [Workspace Settings](Workspace%20Settings.md) keeps the mapping by stable ID.

## Every day after setup

To start: **You are the Architect. Please begin a session by reading Workspace Settings.md and following the executive unit's 00 Start Here/Start Here.md.**

To work with a different lead, use their name or title from the Staff Directory instead.

To finish: **Please end the session by following the executive unit's 00 Start Here/End Session.md.**

[AGENTS.md](AGENTS.md) and `CLAUDE.md` point hosts that read them to the same places. They don't start a session on their own. [Start Here](Executive%20Unit/00%20Start%20Here/Start%20Here.md) owns Begin Session and [End Session](Executive%20Unit/00%20Start%20Here/End%20Session.md) owns the end of a session.

## Find your way

- [Boundaries](Boundaries.md), what helpers may do without asking
- [Workspace Settings](Workspace%20Settings.md#layout) for the layout, and the [Staff Directory](Executive%20Unit/00%20Start%20Here/Section%201/Staff%20Directory.md)
- [Daily Note](Daily%20Note.md), the one place to drop anything new
- [Projects Base](Projects%20Base.md), [Next Actions](Next%20Actions.md) and [Owner decisions](Needs%20the%20Owner%27s%20Decision.md)
- [Calendar of record](Hub%20Unit/30%20Calendar/Calendar%20Appointments.md), with the Hub's reminders on the same page
- [Procedures](Executive%20Unit/80%20SOPs/SOP%20Index.md)
- Optional reading: [Getting started with Obsidian, Markdown and AI hosts](Setup/Getting%20Started%20with%20Obsidian%2C%20Markdown%20and%20AI%20Hosts.md)
- [Release notes](Package/Release%20Notes.md)

No folder access? Use [Guest Start](Executive%20Unit/00%20Start%20Here/Guest%20Start.md) to hand a packet to a chat tool and save its edits yourself. Read the packet before you upload it anywhere.

## Other readers and formats

Any Markdown reader works, and Obsidian is welcome but not needed. Links are ordinary relative links, so a plain text editor can follow them by hand. To move the layout to another note app, keep the folder names and the links, and check them with `Setup/Tools/check_package.py`.

## Set up again

Say: **Please set up this workspace again by following Setup/SETUP.md.** It shows your current answers and asks whether to keep them or start fresh. Neither choice deletes your work. If setup was put away in the Basement, the [Setup Archive](Executive%20Unit/00%20Start%20Here/Section%201/Setup%20Archive.md) page brings it back first.

Help writing as yourself is on the [Voice Sheet](Executive%20Unit/00%20Start%20Here/Section%201/Owner%27s%20Voice/Voice%20Sheet.md) whenever you want it. Begin Session doesn't need it.
