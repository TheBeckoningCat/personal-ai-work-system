<!-- paws-term:inbox -->
# How we Capture

Everything new goes in the [Daily Note](../../../Daily%20Note.md) first. It's the one capture point for the owner and every persona. A unit's `01 Inbox` holds files and handoffs for that unit, not a second list. Keep the owner's own words, where it came from and why. No forms or tags needed.

After your Session Log row is saved, sort what came in under the capture duty in [Workspace Settings](../../../Workspace%20Settings.md#core-duties).

1. Work out what each thing is: a plan the owner stated, an idea, an existing commitment, a deadline or reference.
2. File clear items where they belong: a project, an action section, Potential Projects, a reminder or a reference folder. Write down a plan the owner stated without asking again. Leave undecided ideas marked as proposed.
3. Ask when the meaning or the place really isn't clear. A deadline in a source can become a calendar Request or a reminder. It doesn't mean the owner took on something new.
4. Keep the original and add a short note on where it went. Another unit gets a short note in its Incoming, not an edit to its desk. Leave anything unfinished where people can see it.
5. Move only your own finished, throwaway items to the Trash Can. Anything else follows [Boundaries](../../../Boundaries.md).

When a capture is really a job for a unit, file it there as a project sheet or a page in its Projects room, and leave a one line pointer in the Daily Note. Tell the owner which unit and page. Keep the owner's own names for things unless they agree to a change.

If there's too much to sort well, do a smaller batch and say so. Don't squash detail to fit.

## Check the links

After you move, archive, rename or file pages, run `python3 Setup/Tools/check_package.py --mode workspace` from the workspace folder and fix every broken link it reports. A link is relative to the page it sits on, so a page moved one folder deeper needs one more `../`. If you can't run Python, open each link you wrote and check it lands on the right file.
