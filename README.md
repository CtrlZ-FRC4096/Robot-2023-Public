# Ctrl-Z FRC Team 4096 - Robot Code 2023

The codebase for Siren-Z, the Ctrl-Z robot used in FRC 2023 Charged Up competition season.

## Overview

The code is written in Python 3, using the [robotpy](http://robotpy.readthedocs.io/en/latest/) libraries. It uses a coroutine version of command-based.
## Layout

- `/robot/robot.py` - Boilerplate and subsystem initialization
- `/robot/oi.py` - Joystick button bindings
- `/robot/const.py` - Constants for swerve drive
- `/robot/autoroutines.py` - All autoroutines
- `/robot/subsystems` - Subsystems
- `/robot/swerve` - Python port of 364's Base Falcon Swerve
- 
- `/robot/limelight.py` - Object oriented Python port of the Limelight Helper Lib
- `/robot/wpilibextra` - Extra functionality on top of wpilib. Includes coroutine commands implementation, decorator based xbox controller wrapper, PIDD2 controller (unused), Remote repl, and dynamic view only robot object creator (unused).
- `robot/remote_shell_ds.py` - Client side of the remote repl tool. More info/usage at https://github.com/TheTripleV/robotpy-remoterepl

- `/rpi` - LED code running on a Raspberry Pi. Deprecated. LED control was moved to rio.

- `/vscodeextension` - VSCode extension that live traces robot code execution and highlights all currently running commands and lines of code in vscode.


## Questions?

Feel free to email us:
contact@team4096.org

[Ctrl-Z website](http://team4096.org/)
