# Setup Archive

This note stays here after setup is put away. Workspace Settings names the current setup folder. Open that folder's Setup State to see whether setup is complete. The starter uses `Setup/`. An archived copy lives in `Executive Unit/90 Basement/Archive/Setup/`. If you find both, ask the owner which one is current.

## Put setup away

This is optional. Once setup is complete and the checks pass, show the owner a plan to move the whole Setup folder into the executive unit's Archive. Show the old and new paths, the links that change and the new current folder line. Ask for a yes. If they say no, leave Setup where it is. It works fine there.

After a yes, move it without overwriting anything, fix every link inside and outside the folder, update `Current setup folder` in Workspace Settings and run the link check. Guest Start, Terms and Markers and the Personalization Map stay where they are.

If a move stopped partway, look at both places before doing anything. If both copies exist or they differ, keep both and ask.

## Bring it back

Show the reverse plan and get a yes. Move the folder back to `Setup/` without overwriting, repair its links and set `Current setup folder` back to `Setup`. Then follow SETUP. Setting up again never deletes the owner's projects, mail, logs or samples.

`Setup/Tools/check_package.py --mode workspace` checks the links after either move. It travels with the Setup folder, so run it from wherever the folder is now.
