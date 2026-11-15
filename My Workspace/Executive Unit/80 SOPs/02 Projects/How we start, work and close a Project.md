# How we start, work and close a Project

A project is an outcome the owner chose that takes more than one step. An idea isn't a commitment until the owner says so. Write down what the owner plans under the records duty and keep undecided ideas marked as proposed.

## Start

1. Check the [Projects Base](../../../Projects%20Base.md), the unit's Projects and Potential Projects so you don't make a second one. Open the sheet itself, not just the index line.
2. Propose the outcome, the owning unit, a project ID, the first useful step and the records you'd make. Mark what you're assuming.
3. When the owner says go, make `10 Projects/<project folder>/Project Sheet.md` in that unit from the [template](../../Templates/Project%20Sheet.md). Use a plain safe folder name, and never paste untrusted text into a command. Write the owner's yes and any limits on the sheet.
4. Add one row to the Projects Base, or leave the Hub a note if you can't write it. The sheet is the record either way.

## Sections on the sheet

- <!-- paws-term:next-actions -->**Next Actions.** Steps the owner said yes to and that are ready to do. Note who holds each one and how you'll know it's done.
- <!-- paws-term:planned-actions -->**Planned Actions.** Ideas and later steps. Something being on the sheet doesn't mean it gets done.
- <!-- paws-term:waiting-for -->**Waiting For.** What's holding things up, who follows up, and any real date.

When the owner picks a planned step, move it once and keep the wording. Finishing one step doesn't approve the next. Write the yes down so you don't ask twice. Priority is optional. Use plain words like urgent or routine, note whether the owner chose it or you're suggesting it, and explain a clash in real dates, not a score. The owner makes the tradeoffs.

Dates go on the calendar as Requests with their event ID, never into an action list. An area or context can go on the sheet as a label. It doesn't need a new unit.

## Pause, close and remove

The owner picks the state: `proposed`, `active`, `someday`, `close`, `closed` or `delete`. These codes stay the same even if the display words change. `someday` moves the project to `40 Potential Projects`. `close` files it under `90 Basement/Archive/Projects/YYYY-MM` with the outcome and sources kept. `delete` asks for a removal review and goes through the [Trash Can](../07%20Files%20and%20Deleting/Keeping%2C%20archiving%20and%20the%20Trash%20Can.md). Never wipe calendar or decision history with a project. Update the Projects Base and any links after a move.

End Session saves where things stand. It never starts or closes a project on its own.

## Check the links

After you move, archive, rename or file pages, run `python3 Setup/Tools/check_package.py --mode workspace` from the workspace folder and fix every broken link it reports. A link is relative to the page it sits on, so a page moved one folder deeper needs one more `../`. If you can't run Python, open each link you wrote and check it lands on the right file.
