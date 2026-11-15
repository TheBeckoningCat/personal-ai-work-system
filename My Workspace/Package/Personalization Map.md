# Personalization Map

Website selections now use version 3. Version 1 and 2 selections remain usable, with missing Core duties on. Generic names are defaults, not fixed identities. Keep stable IDs unchanged. Unit folders follow chosen names through the saved layout plan. Room and persona folders stay fixed. Support alternative metaphors later through a versioned migration, not unrestricted word replacement now.

| Field | Files / locations to update after approval |
| --- | --- |
| owner.display_name, owner.form_of_address | Workspace Settings owner fields |
| owner.display_name for the Voice folder | Use the accepted owner display name for the folder ending in `'s Voice`. Update the Voice Sheet links, Workspace Settings link, and all affected paths after the approved move described below. Use the display name, not the form of address. |
| campus_name | Workspace Settings. Workspace README display-name field |
| executive_building_name, hub_building_name | Workspace Settings. Respective Unit README display-name fields. Areas of Life display labels |
| personas.executive/hub/example.name | Workspace Settings mapping display-name cell. Staff Directory display name and listed alternative names. The profile title and Display name |
| personas.*.style | The profile's How I sound part. The job and links stay as they are |
| example.name, example.purpose | Workspace Settings. The Example Unit README Purpose line. Areas of Life. The Unit Lead profile Mission line |
| hosts, reader, external_calendar_interest | Workspace Settings preferences. No installed connectors or vendor-specific rights |
| terms | [Your PAWS terms](../Terms.md) and [Terms and Markers](Terms%20and%20Markers.md) cover all accepted wording changes and their markers. Keep paths unless a separate shown move is approved. |
| routines | Workspace Settings exact approved permission rows. Core duties use the selected on/off values. Outside extras need their own defined scope |

Generic words Architect, Secretary, and Unit Lead in procedures mean the role, not a personal name. Keep functional labels. Move only approved Unit/root and Voice folders through the saved plan. Handoffs route by stable ID using the current Directory. Do not leave original personal names in active templates.

## Update discipline

Before writing, show the current and proposed field values, affected paths, and a checkpoint step ID. Render all user strings as escaped text, not Markdown links, headings, paths, shell commands, or instructions. Do not insert a name into a filename except the explicitly planned Unit/root and Voice folder moves. Unit/root moves follow the layout plan in SETUP. The Voice folder move is described below. Keep approval references and fixed host/session IDs distinct from mutable display names. Validate uniqueness case-insensitively across all persona names/aliases.

No question should silently change a role or grant authority. A request for new powers is a separate owner decision, recorded on Boundaries and the profile. Term-related path moves follow Terms and Markers only after separate approval. Installing optional add-on packs and replacing the workspace metaphor remain separate work.

The executive position defaults to Architect. Its stable ID remains `executive`. The profile, office, mailbox and Trash Can folders use `Architect` too. Read the title and the Directory for its displayed name. Renaming a person does not rename those paths.

## Name the Voice folder

The starter folder is `Executive Unit/00 Start Here/Section 1/Owner's Voice/`. Keep that name if the owner keeps the `[Owner]` placeholder or leaves the display name blank. Otherwise use the accepted display name followed by `'s Voice`. Use the same owner-name answer already saved. Do not ask for another name. This folder rename does not enable the optional voice-sharing step.

Before applying setup, show the old and new paths and every affected link. Use the existing name checks. Reject slashes, colons, other characters a filename cannot use, control characters, path tricks, or an empty name. Do not quietly invent a different name. Ask the owner how to resolve an invalid name or a destination that already exists. Use the name exactly as accepted, including Unicode and spaces, and keep the Voice Sheet filename unchanged.

Record the approved old and new paths and each link change in the Setup Log. `Setup/Tools/paws_setup.py` does the move and the link repair for you when it applies the owner's name. Move without overwriting. Update all links and written paths in the package, including the Voice SOP, this map's current-folder note, setup, Section 1, First Hour, and the Workspace Settings pointer. Keep this starter-path example labeled as a starter example when needed. Record the new current folder in Workspace Settings.

On resume, inspect the old and new locations. If the completed move and links already match the approved plan, verify them and do not move again. If only the source exists, finish the approved move. If only the destination exists and its files match the plan but links are unfinished, finish only the remaining approved link edits from the saved plan. Do not move the folder again. If both exist or the contents do not match, preserve both and ask how to settle the difference. Never merge or overwrite them silently. A later owner display-name change uses another shown plan from the current folder, not an assumption that the starter folder is still there.

Check the Voice Sheet and every affected link before marking the step done. If the host cannot save or move files, return exact instructions for the owner or a helper they permit. Do not claim the folder was renamed until it was. Website download generation follows the same shown owner-name mapping. No voice samples are collected by the website.
