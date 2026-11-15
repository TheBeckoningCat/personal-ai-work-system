# Setup Tools

Two small Python scripts. They use only the standard library and run on Python 3.8 or later. Setup works without them, but they save a lot of careful hand editing.

- [paws_setup.py](paws_setup.py) reads Setup State, lists what is still open, saves answers, writes the full plan to Setup Plan.md, applies only what the owner approved with a prior copy of each file, checks the result and picks up after an interruption. It also renames a unit folder and repairs every link.
- [check_package.py](check_package.py) checks the workspace. Use `--mode workspace` for a folder in use and `--mode release` for a fresh download. Every problem it finds comes with a suggested fix.

Run them from the workspace folder, for example `python3 Setup/Tools/paws_setup.py status`. If your host can't run Python, follow SETUP.md by hand. The result is the same.
