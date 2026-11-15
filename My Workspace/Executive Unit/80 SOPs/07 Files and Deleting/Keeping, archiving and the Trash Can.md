# Keeping, archiving and the Trash Can

## What to keep

Keep raw sources, the main project, decision and calendar records, and useful references. A summary or snapshot points back to its source with the path and date. It never replaces the source. Keep the nuance, doubts and specialist detail. Someone should be able to trace any commitment back to where it came from, not just to a helper's short version. Don't make a second live copy of a project or calendar.

## Archive

When work is closed and the owner says so, move it to the unit's `90 Basement/Archive/` without overwriting anything, with a note saying where it came from and why. Make the folder the first time. Useful reference goes in `90 Basement/Resources/`. Fix every link that pointed to the old place.

## Trash Can

Move things to `Executive Unit/90 Basement/Trash Can/<Unit>/` instead of deleting them. Under the records duty you can move your own finished, throwaway items there. Anything else needs the owner's yes. Write down the original path, the date, the reason, the owner's yes and how to put it back. Use a name that isn't taken, never overwrite and don't use `rm`. Check for links and open work first. Putting something back is a move too, after checking nothing is in the way.

Nobody empties the Trash Can on a timer, and no amount of time makes it okay. Permanent deletion is the owner's call, every time. See [Boundaries](../../../Boundaries.md).

## Backups

Before a big change, suggest the owner make a backup with their own tools. Check where it goes and don't upload or set up sync. A backup isn't proven until someone tries a restore, so write down what was copied and when.

## Check the links

After you move, archive, rename or file pages, run `python3 Setup/Tools/check_package.py --mode workspace` from the workspace folder and fix every broken link it reports. A link is relative to the page it sits on, so a page moved one folder deeper needs one more `../`. If you can't run Python, open each link you wrote and check it lands on the right file.
