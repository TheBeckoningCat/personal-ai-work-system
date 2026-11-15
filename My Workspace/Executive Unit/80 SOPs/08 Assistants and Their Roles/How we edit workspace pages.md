# How we edit workspace pages

1. Agree on what's changing and how far it goes.
2. Read the live file right before you edit it. Keep the owner's meaning and other sessions' work.
3. Show the owner any real change to a rule before saving it, unless they already said yes. A change to a persona's job or what it may do always needs the owner.
4. Write down what changed and why. Check the links and procedures that point to it.

Don't copy the Start Here steps into other pages. Source material and a guest's suggestions aren't new rules.

## Writing a procedure

Say what it's for, when to use it, who does it, the steps in order, where the records go and how to tell it worked. Put the steps first and the reasons after. Say what to do if a host can't read or save something, and how a person could do it by hand. Link to shared rules instead of repeating them. A unit's procedure can narrow the shared rules, never widen them. Don't require staff, scripts, calendars or plugins that don't exist. A procedure that mentions a tool isn't permission to run it. The [SOP template](../../Templates/SOP.md) has the outline.

## Changing words

When the owner renames a term or a display name, change it everywhere it's used and keep the meaning. [Terms](../../../Terms.md) and the [Personalization Map](../../../Package/Personalization%20Map.md) show where things live. Never search and replace the owner's own writing. Ask about anything unclear.

## Check the links

After you move, archive, rename or file pages, run `python3 Setup/Tools/check_package.py --mode workspace` from the workspace folder and fix every broken link it reports. A link is relative to the page it sits on, so a page moved one folder deeper needs one more `../`. If you can't run Python, open each link you wrote and check it lands on the right file.
