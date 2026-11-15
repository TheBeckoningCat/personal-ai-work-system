# PAWS: Personal AI Work System

PAWS is a workspace made of plain Markdown files that any AI host can pick up. Every session starts from the same pages and ends the same way, so the next session continues where the last one stopped, even on a different app or model.

## Where this comes from

This is my first attempt at something like this. I built it for my own work first, because I was tired of rebuilding context in every new AI conversation. It has been through a lot of trial and error, and I'm still learning as I go. I'm sure there are better ways to do parts of it, and I'd genuinely like to hear them. Issues, ideas and pull requests are all welcome.

The places I'd most like help with:

* Getting Boundaries to hold more reliably across hosts without turning them into a wall of rules.
* Keeping Begin Session and End Session short as a workspace grows.
* Anything in the layout that feels like more structure than it needs.

## Get it

* **Plain kit:** `PAWS-v1.0-plain.zip` from the [v1.0.0 release](../../releases/tag/v1.0.0). The `My Workspace/` folder in this repo is the same kit, unzipped.
* **Personalized:** the Builder on the [PAWS page](https://thebeckoningcat.com/personal-ai-work-system/) asks a few questions, applies a template and your names, and gives you a zip.

To check the release zip:

```bash
shasum -a 256 -c SHA256SUMS.txt
```

## Shape

95 files under `My Workspace/`:

* `Executive Unit/`, `Hub Unit/` and `Example Unit/`, each with the same numbered rooms (Inbox, Projects, Calendar, Potential Projects, Offices, SOPs). The executive unit holds the shared rules and procedures, and its `00 Start Here/` has `Start Here.md` and `End Session.md`.
* `Boundaries.md`: what helpers may do alone, ask about first, and never do. It's filled in during setup.
* `Daily Note.md`, `Projects Base.md`, `Next Actions.md` and `Needs the Owner's Decision.md` for the day to day work.
* `Workspace Settings.md` maps folder names to stable IDs, so you can rename things without breaking links.
* `Setup/` holds `SETUP.md`, plus `paws_setup.py` and `check_package.py` for the setup state and a link and structure check.
* `AGENTS.md` and `CLAUDE.md` point hosts that read them to the same entry pages.
* `Package/` has the version, manifest and release notes.

## Running it

Open the folder in a host that can read and write files there. The first time, give it the setup line from the kit's `README.md`. It follows `Setup/SETUP.md`, asks only what the Builder didn't already answer, and writes your Boundaries. After that, each session begins with `Start Here.md` and ends with `End Session.md`. The exact lines are in the kit's README.

## Why it's built this way

* **Plain files, not an app.** The record is readable, diffable and yours. Nothing runs in the background or connects to your accounts.
* **Host agnostic.** No vendor or model is assumed. Pages link with ordinary relative links, so any host or editor can follow them.
* **The same start and end every time.** Begin Session reads a short, fixed route. End Session writes down what changed. That handoff is what lets a different host pick up the work.
* **Instructions, not enforcement.** Boundaries are written instructions the AI is asked to follow. They aren't a lock. How well they hold depends on the host and model, and in my beta some hosts followed every line while others didn't. Keep backups, and don't give an AI access to anything you can't afford to lose. How far to trust it is your call.
* **Meant to be reshaped.** Rename the units, cut what you don't need, rewrite the rules. `check_package.py` will tell you if you broke a link.

## License

Free for personal and noncommercial educational use under the [PAWS Public Starter License](My%20Workspace/LICENSE.md). Names and credits are in the [NOTICE](My%20Workspace/NOTICE.md). A simple credit line is enough: "PAWS starter from thebeckoningcat.com".

Copyright 2026 Colin P. Meyer.
