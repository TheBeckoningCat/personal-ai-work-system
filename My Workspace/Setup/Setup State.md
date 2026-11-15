# Setup State

Status: not started
Run by: the Architect (stable ID `executive`)
Persona review: not done
Setup session: none yet
Plan: none shown yet
Next question: What should your assistants call you?
Progress: Four choices left. Everything else keeps its default unless the owner raises it.

This is the current record, one row per choice. History, plans and the step ledger are in the [Setup Log](Setup%20Log.md). [paws_setup.py](Tools/paws_setup.py) reads this page and works out the next question from the rows.

## Choices

| Field | Value | Source | Stage | Ask |
| --- | --- | --- | --- | --- |
| owner.display_name | [Owner] | default | default | choice |
| workspace.name | My Workspace | default | default | no |
| workspace.folder | keep the current folder | default | default | no |
| executive.unit | Executive Unit | default | default | no |
| executive.title | Architect | default | default | no |
| hub.unit | Hub Unit | default | default | no |
| hub.title | Secretary | default | default | no |
| example.name | Example Unit | default | default | no |
| example.lead_title | Unit Lead | default | default | no |
| example.purpose | General work. Purpose to be set later. | default | default | choice |
| boundaries | the defaults on Boundaries.md | default | default | choice |
| work_folders | this workspace folder only | default | default | choice |
| personas.review | the titles and the starter manner | default | default | extra |
| hosts | the app you are using now | default | default | extra |
| reader | any Markdown reader | default | default | extra |
| calendar | none. The Markdown calendar is the record | default | default | extra |
| writing_samples | later, from the Voice Sheet | default | default | extra |
| work_preferences | none | default | default | extra |
| core_duties | all on | default | default | no |
| terms | the starter words | default | default | no |

Stage goes from `default` or `selected` to `approved`, `applied` and `verified`. Source is `builder`, `owner` or `default`. Ask is `choice` for a question setup asks, `extra` for one that keeps its default unless the owner raises it, `done` or `skipped` once settled, and `no` for a default it only mentions.

## Do later

Nothing yet. A skipped extra can be picked up any time.
