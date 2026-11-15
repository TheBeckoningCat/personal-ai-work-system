# Getting started with Obsidian, Markdown and AI hosts

## What PAWS is

PAWS is a folder of plain text instructions and records that helps an AI pick up where the last session left off. Your AI reads it, does the job in its profile and saves what happened. Obsidian makes the folder easy to browse, but any Markdown reader works. The folder doesn't run an AI or anything in the background.

1. **Architect** helps design and look after the workspace so it fits how you work. Changes to the rules stay your call.
2. <!-- paws-term:reminders -->**Secretary** handles capture, mail between helpers, the calendar, reminders and keeping things moving.
3. **Unit Leads** look after one area of your life or work each. The starter includes one subject Unit whose purpose you choose.

The core duties are on from the start. Helpers handle their own mail, sort captures, keep their records and note dates without asking you each time. You can turn any of them off in [Workspace Settings](../Workspace%20Settings.md#core-duties). What needs your yes is on [Boundaries](../Boundaries.md). Names, rooms, units, duties and words can all change later. Just ask the Architect. Nothing here connects to an outside account.

Keep the unzipped folder together. Markdown is ordinary text in `.md` files, so you can change readers and your words still work.

## Markdown in a minute

```text
# Heading
- A list item
- [ ] An unfinished task
- [x] A finished task
[Open a page](../README.md)

| Item | State |
| --- | --- |
| Practice | Draft |
```

Headings organize a page, lists collect items, links open files, checkboxes show completion and tables compare records. Reading view formats the text. Source view shows the marks. No special database or plugin is required.

## Open the folder

In Obsidian, choose Open folder as vault and select the whole unzipped workspace folder. Find README in the file list, follow its links and use search to find a phrase. The graph shows connected pages. It is optional navigation, not a task system. A screenshot would show the file list on the left and README in the main pane. No screenshot is supplied here.

Settings live in the vault's `.obsidian` folder. You can leave Sync off and work locally. If you choose Obsidian Sync, set it up deliberately in your version's settings and check its service and privacy terms first. PAWS does not enable it or upload files. Keep a separate backup. Any Markdown reader or plain editor can open the same files.

Check these for your version: menu names, search shortcuts, graph controls, Sync plans and settings. See [Obsidian Help](https://help.obsidian.md/).

## Choose a host

The first line for any host that can read and save files here is **You are the Architect. Please set up this workspace by following Setup/SETUP.md.** After setup, the daily line is **You are the Architect. Please begin a session by reading Workspace Settings.md and following the executive unit's 00 Start Here/Start Here.md.** Use any name from the Staff Directory in place of the Architect. Workspace Settings gives the folder, so don't guess it.

| Host | Open the workspace | Start line | What to verify |
| --- | --- | --- | --- |
| Grok CLI | Use your installed CLI's working-folder controls or start it from this folder | Use the first line above, then the daily line | Several tools use this name. Verify your exact tool can read whole files, save and read a clock. No specific command is assumed |
| Codex | Open this folder as its project. For an existing CLI installation, launch `codex` from the folder | Use the first line above, then the daily line | Local reading and editing depend on granted access. A remote environment needs the files made available |
| Claude Code | With an existing installation, open a terminal in this folder and launch `claude` | Use the first line above, then the daily line | Verify file permissions and saved changes. Account access alone does not prove folder access |
| Editor agents | Open the whole folder as the editor workspace | Use the first line above, then the daily line | Enable only the tools and file scope you intend. Verify actual writes |
| App agents with file tools | Select this local folder using that app's project or folder controls | Use the first line above, then the daily line | Verify full reads and writes. An uploaded snapshot may not update the original |
| Web chatbots without local files | They cannot open a local folder from a pasted path. Use the Guest Start route linked from README and provide only an approved packet | “Follow the supplied Guest Start packet. Return exact edits for me to save.” | They can suggest edits to supplied text. You or an authorized helper must save them |

Check these for your version: installation, launch commands, folder controls, permissions and model limits. This guide installs nothing. Official references are [Codex CLI](https://developers.openai.com/codex/cli/) and [Claude Code quickstart](https://code.claude.com/docs/en/quickstart). A product name is not proof of access.

## Work side by side

Open the same folder in Obsidian and the AI host. Obsidian displays saved edits. The AI reads the files rather than your unsaved editor buffer. Let one writer finish a shared page before another saves. If both edited it, preserve both versions, reread the current file and merge only the agreed changes. Session IDs identify work. They do not lock files.

## First-day practice

Setup leaves you in a working session. Capture a harmless note in Daily Note and watch the Unit Lead sort it with a source pointer. State an appointment's date and time zone. Your Unit Lead records a Request and the Secretary checks and confirms it in Markdown without another permission question. Then End Session once and check the Session Log row, the Work Log line and the Desk note. Use [First Hour](First%20Hour.md) for a fresh-chat resume test.

## Common problems

| Problem | What to do |
| --- | --- |
| The AI says it cannot open a file | Confirm it has the whole folder. Use Guest Start if it only accepts pasted text |
| A link no longer opens | Preserve the files. Read the Unit mapping in Workspace Settings and repair the link through an approved rename plan |
| Edits do not appear | Check the exact folder and file, save the editor buffer and reopen the file before claiming a write |
| Two sessions overlap | Claim paths and arrange one writer. Preserve both versions if they conflict |
| <!-- paws-term:reminders --> No notification arrived | Markdown reminders are records reviewed during sessions, not an installed alert service |
| The AI keeps asking to file | Check the Core duties row and owner limits. If it is on, follow the current duty and report any conflicting page |

For plain-text migration, keep the records and profiles separate and update every link when changing file formats. For a document service, map stable IDs to documents and test its real sharing and edit permissions. Local file rules do not install a connector or authorize uploads.
