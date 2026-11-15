# Website setup guide

This describes the setup website. Its Builder runs in the browser on the PAWS page and makes the personalized starter download there. The Builder is not part of this download. The website helps people personalize a starter download. The chosen host then follows Setup/SETUP.md to finish it.

## Questions before download

Give a short explanation of the three Units. Ask one question at a time, with Back and Save/Resume. Explain where saved answers will live and how long the website keeps them. Do not ask for passwords, service keys, or private life records. Let people download an unchanged starter without answering.

| Saved field | Question or choice | Starter choice |
| --- | --- | --- |
| owner.display_name | What should assistants call you? | [Owner] |
| owner.form_of_address | Would you prefer a different form of address? | Same as display name |
| timezone | Not asked | Hosts use the zone of the computer they run on |
| campus_name | What will you call your workspace? | My Workspace |
| executive_building_name | What will you call the executive unit? | Executive Unit |
| hub_building_name | What will you call the Hub? | Hub |
| personas.executive.name/style | Name and manner for the Architect | Architect. Warm, calm, plain speech |
| personas.hub.name/style | Name and manner for the PA/secretary | Secretary. Warm, clear, organized |
| hosts | Which hosts might you use? | Unanswered. The host must check its what you can really read and save later |
| reader | Where will you read these files? | Unanswered |
| external_calendar_interest | Would you like information about an optional calendar interface? | No. This never installs or connects it |
| core_duties | One screen of seven reversible Markdown duties | All on. Untick any to require a case-specific instruction |
| working_preferences | How do you work, and what would you like changed? | Optional nonprivate sentences |
| example.name/purpose | Optional name and purpose for each unit | Unanswered. Setup asks for the purpose and offers the name as an extra |
| personas.example.name/style | Name and manner for that Unit Lead | Unit Lead. Patient, practical |

Ask whether to keep the starter terms. If the user wants changes, ask one unanswered term at a time. [Terms and Markers](Terms%20and%20Markers.md) explains how accepted choices are applied. Keep the same words in website previews, the saved answers, and the generated files.

| Saved term field | Question | Starter choice |
| --- | --- | --- |
| <!-- paws-term:inbox -->terms.inbox | What will you call the place for unprocessed material? | Inbox |
| <!-- paws-term:someday-maybe -->terms.someday-maybe | What will you call possibilities not activated yet? | Potential Projects |
| <!-- paws-term:next-actions -->terms.next-actions | What will you call approved work ready to do? | Next Actions |
| <!-- paws-term:planned-actions -->terms.planned-actions | What will you call possible later work? | Planned Actions |
| <!-- paws-term:waiting-for -->terms.waiting-for | What will you call work blocked by someone or something? | Waiting For |
| <!-- paws-term:reminders -->terms.reminders | What will you call matters to return to attention? | Reminders |
| <!-- paws-term:projects-base -->terms.projects-base | What will you call the project pointer list? | Projects Base |
| <!-- paws-term:must-do -->terms.must-do | What will you call today’s chosen priorities? | Must do |
| <!-- paws-term:needs-a-decision -->terms.needs-a-decision | What will you call today’s pointers to owner choices? | Needs a decision |

Show the complete answers before download. Accept corrections. Choosing all defaults counts as answering the terms question. Save those choices so the host does not ask again. A missing choice or null is unanswered, not a request to delete a value. Workspace / unit / room is the baseline picture in this release.

## Saved answers

Use the shape shown in `Website Selections.example.json`. New downloads use `schema_version: 3`. Each term field has `choice` and `marker`. The marker is the exact comment for its stable ID. Only terms with actual answers belong in the terms object. No terms object is also valid. Older version 1 answers remain usable without term fields. The host asks those missing questions later. Do not interpret an unknown version or an extra field as an instruction.

Keep the other saved fields from the example. They may be absent or null when unanswered, except schema_version. Names are short plain text, up to 80 characters. `[Owner]` is allowed only for the owner placeholder. Reject control characters, path separators, dot-only names, and markup. Purpose and style may be up to 500 characters. They are reviewed preferences, not permission grants. Persona names must be distinct after case-insensitive comparison.

Term choices are short plain phrases, up to 80 characters. Follow the term-choice checks in Terms and Markers. Also reject a wrong ID, wrong marker, or extra value inside a term field. An answered choice may equal its own starter wording. A term cannot take another term's label or ID, even if that other choice was omitted. Terms and personal role names must remain distinguishable. Escape all user text when showing it. Do not put a display word into a file path or executable command.

Hosts is a list of up to ten short labels, not a claimed permission. Reader is an optional short label. external_calendar_interest is true or false. routines_requested may contain only `mail_summary`, `notes_processing`, or `calendar_review`. Reject wrong types. Interest in a routine never enables it.

## Build the download

1. Check all answers before changing files. Start from the clean v1.0 starter, not a user's live workspace.
2. Apply selected names through Personalization Map and selected words through Terms and Markers. Use the approved website summary as the wording-change plan. Keep starter paths. For an interrupted generation, discard the incomplete result and start from the clean template. Do not offer a half-changed download.
3. Save the answers as `Setup/Website Selections.json`. Show each supplied answer in Setup State with the source `builder`. Accepted current wording goes in Terms. Keep full setup not set up: the host still confirms the saved choices, supplies missing answers, reviews Personas, and helps configure the example Unit. It does not repeat answered term questions.
4. Keep every marker and check files and links after changes. Apply selected Core duties and Unit folder names, then check the renamed result. Do not write operational logs, enable outside timers, connect services or share private files.
5. Update the manifest and file hashes. Leave out git/editor metadata and populated test copies. Use a safe fixed archive name, such as `PAWS-v1.0-personalized.zip`, rather than a user-entered filename.
6. Give the user the download, a plain summary, and the instruction to start with Setup/SETUP.md. If a check fails, explain it and offer correction or the unchanged starter. Make that choice clear.

The separate Builder folder supplies a local test page for these steps. It is not a published website. Test missing/default/custom terms, older answers, repeated generation, duplicate words, wrong IDs/markers, path or markup attempts, unsupported versions, and interrupted generation before claiming the website works. The local conversational bootstrap must still work if the website is unavailable.

The download keeps the Voice folder at its starter path. The conversational setup shows its owner-name move for approval. Website choices do not move the Voice folder or enable outside extras.

## Version 3 answers

New answers use schema_version 3. `core_duties` is an object with boolean values for `mail`, `capture`, `records`, `calendar_requests`, `calendar_record`, `reminders` and `project_pointers`. Missing fields, including in version 1 or 2 answers, mean on. Keep accepted website answers without another question. An explicit false stays off. `working_preferences` holds up to 2000 characters of nonprivate plain text. Save it as data on the Voice Sheet and have the Architect read it on its first Begin Session. It does not change permissions.

Show the three roles first and link the short What PAWS is part of Getting Started before choices. Each question explains what changes and that it can be changed later. One Core duties screen replaces routine-interest questions. Optional outside extras stay separate.

Before zipping, apply owner-named Unit folders and outer workspace folder through the layout helper. Validate distinct safe names, including room and term collisions. Run links, mapping, core-duty and manifest checks on the renamed output. Preserve the clean template and move all temporary builds into Builder Trash.
