# ENGF0034 Assignment 3

Welcome to your next debugging assignment! This repository contains an implementation of the classic Frogger game that needs your debugging skills.

## Quick Start

1. Clone or download this repository to your local machine
2. Test the game: `python3 frogger.py`
3. Read the full assignment instructions in `assignment3.pdf`

## Prerequisites

- Python 3
- tkinter (usually included with Python)

## Game Files

The Frogger game implementation follows a Model/View/Controller design pattern:
- `frogger.py` - Main game launcher
- `fr_controller.py` - Game controller logic
- `fr_model.py` - Game model and state management
- `fr_view.py` - Game display and graphics
- `fr_settings.py` - Game configuration settings
- Various `.gif` and `.png` files for game sprites

The game contains **at least five bugs** that make it unplayable!

## Game Objective

Cross the road avoiding cars, cross the river by jumping on logs or turtles, and make it to one of the five frog homes at the top of the screen. You start with seven lives and a time limit. Get frogs to all five homes before time runs out to advance to the next level.

## Submission Guidelines

Please submit your bug reports as one file (txt or PDF) and your fixed python source code file(s). No need to zip them, multiple files can be uploaded.

Upload your completed files directly to Moodle:
👉 [Moodle Assignment 3 Submission Point](https://moodle.ucl.ac.uk/mod/assign/view.php?id=9108708)

## Your Task

1. Play the game and find bugs (there are at least 5!)
2. Write detailed bug reports for each bug including:
   - One sentence summary
   - What happens vs what should happen
   - Instructions to reproduce the bug
3. Identify the root causes by examining and instrumenting the code
4. Fix the bugs (simple fixes, mostly 1-3 lines each)
5. Upload your solution files directly to Moodle before the deadline

## Deadline

Monday 2nd November at 12 noon (midday)

## Debugging Tips

- Use `print()` statements to instrument the code and understand program flow
- Look carefully at the code - one bug requires very careful reading
- Consider temporarily simplifying code to make bugs easier to reproduce
- Understand what the program is actually doing before attempting fixes

## Assessment

This assignment is not formally assessed but serves as valuable debugging practice. You may work with peers if desired.

## Optional Extension

Experienced programmers may consider extending the game after fixing bugs:
- Add turtle submersion mechanics
- Include crocodiles and other hazards  
- Improve level progression difficulty
- Other creative enhancements

You can upload your extended game to Moodle:
👉 [Moodle Optional Extension Submission Point](https://moodle.ucl.ac.uk/mod/assign/view.php?id=9108709)

You won't get any extra marks, but we are curious what you can achieve.

## Troubleshooting

### tkinter Issues
If you get tkinter import errors:
- **Ubuntu/Debian:** `sudo apt-get install python3-tk`
- **CentOS/RHEL:** `sudo yum install tkinter`
- **Arch Linux:** `sudo pacman -S tk`
- **macOS/Windows:** tkinter should be included with Python

### Testing tkinter
Test tkinter availability: `python3 -c "import tkinter; print('tkinter works!')"`

### Python Version
Ensure you're using Python 3: `python3 --version`
