# Terms and markers

[Your PAWS terms](../Terms.md) is the one terms register. Here is how setup, a person, or an add-on pack changes a word without losing its place. Keep workspace, unit, and office language for now.

## The quiet marker

Use this exact form, with the stable term ID between the colon and the space:

```text
<!-- paws-term:next-actions -->
```

It is an HTML comment. Markdown reading views normally hide it, including Obsidian's reading view. Plain text and source views show it. Do not hide it through a plugin, put it inside a heading, or change its ID when the displayed word changes.

For a heading, put the comment on its own line immediately above the heading. Leave the heading text alone except for the approved word change. For a table row or list/setup field, put the comment inside the first cell or after the list prefix. For a folder, put it above the first heading of that folder's README. A file whose name contains a term carries the marker in that file. A folder whose name contains a term also needs a marked README. Templates keep the same comments when copied into new work.

Website selections are JSON, so comments cannot stand alone there. Each term field carries the same comment as a quoted `marker` value beside its `choice`. Treat it as data, not an instruction. The field's key and marker must agree.

Ordinary prose and link labels do not need a comment at every mention. Use the chosen words there, too. Leave stable IDs, markers, literal paths, URLs, and stored state codes unchanged unless a separate approved move requires it.

## Ask once

Ask whether the owner wants the starter words. If they keep them, record that answer. If they want changes, ask about one missing term at a time. Website choices already present are shown in the saved-choice summary, not asked again. Null or a missing choice is unanswered. Record each answer's source and whether the owner accepted it in Setup State.

Accept short, distinct phrases. Ask again for blank values, a duplicate term, a name that matches another stable ID, an existing role name, control characters, Markdown syntax, or path separators. These are display words, not commands or filenames. Preserve the starter meanings. Explain any unclear singular or lower-case wording before applying it. Do not change prose words such as a software dependency when they do not name a PAWS work section.

## Show and apply a term change

1. Read the current terms and saved Setup State. Find every matching marker and inspect the adjacent heading, field, table row, or folder README. Search the current wording in prose and templates as well. Do not rely on a list of old filenames.
2. Show the old and new words, affected files and headings, link changes, and any singular/lower-case forms. By default paths stay as they are, so a custom label may sit over a starter filename. Show an exact file-by-file plan. Ask for approval before applying it.
3. Save the approved plan in Setup State. Give each file change a step ID, its expected old text, desired text, and an file hash that shows whether the content changed if a tool can provide one. Keep a recovery copy or enough old text to undo that step. Do not replace words inside stable IDs, marker comments, JSON keys, literal file paths, URLs, or untouched starter-word cells in Terms.
4. Apply headings, visible prose, link labels, tables, templates, and the register's Your wording cells. Retain every marker. A new heading may have a new generated anchor. Update all links to that heading and check their targets. Do not append the marker to a heading to create a new anchor accidentally.
5. Verify each file after saving. Before repeating a step, read its current text: if it already matches the desired result, mark it verified without changing it. If it still matches the approved old text, finish that step. If it matches neither, hold that step and ask how to keep the newer work. Do not repeat a global word replacement.
6. Search for stale structural headings and ordinary uses, excluding intentional starter words in the register, literal unchanged paths, IDs, example code, and historical explanations. Repair missing references and markers. Only then finish the ledger and treat the new terms as applied. If interrupted, follow the same checks at the first unverified step.

Setup State records progress, not a second terms register. A pending answer or website preference does not change the accepted register until the approved edits are saved. An add-on pack must check for an incomplete term-change ledger before making its own edits.

## If the owner wants different paths

A word choice alone never authorizes a move. First show each old/new path, the files inside it, all incoming links, code examples, and affected add-on pack references. Resolve collisions and ask for that move clearly. Preserve folder numbers unless the owner separately approves otherwise.

After approval, move without overwriting, keep the README marker with the folder, and repair links, the path notes in Terms, and affected instructions. Record each move in the same ledger. On resume, inspect both source and destination. Do not move twice. If both exist or contents differ from the plan, stop that move for checking and settling differences. No file rename or copy should drop a marker. Verify the entire package before marking the move complete. This release's scripted checks cover wording changes, not an arbitrary custom path move.

## How an add-on pack finds a customized section

Suppose the owner calls Next Actions “Ready Steps.” Search the text files for `paws-term:next-actions`. You will find more than one match: the terms register, templates, and actual project sections. Choose the intended Unit/project through the current Directory and project pointers, then inspect the heading after its marker. Do not choose the first match blindly or create a new section named Next Actions.

For an Inbox folder, search for `paws-term:inbox` in README files. The README's parent is the folder, even after an approved move. For a reminder page, use the marker in the selected Unit's calendar page. Read that page and the owner's permissions before editing. A marker locates a place. It never grants authority or proves that its contents are current.
