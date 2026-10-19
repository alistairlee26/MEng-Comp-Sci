# ENGF0034 Assignment 2

Welcome to your debugging assignment! This repository contains three implementations of the classic Bomber game that need your debugging skills.

## Quick Start

1. Clone or download this repository to your local machine
2. Test one of the games: `python3 bomber_oo.py`
3. Read the full assignment instructions in `assignment2.pdf`

## Prerequisites

- Python 3
- tkinter (usually included with Python)

## Game Files

Choose one of the three implementations to debug:
- `bomber_oo.py` - Object-oriented version
- `bomber_proc.py` - Procedural version  
- `bomber_bigloop.py` - Big loop version

All three games should behave identically but contain **at least five bugs** that make them unplayable!

## Submission Guidelines

Please submit your bug reports as one file (txt or PDF) and your fixed python source code as a second file.  No need to zip them, multiple files can be uploaded.

Upload your completed files directly to Moodle:
👉 [Moodle Assignment 2 Submission Point](https://moodle.ucl.ac.uk/mod/assign/view.php?id=9108700)

## Game Controls

- **SPACE**: Drop bomb
- **Q**: Quit game  
- **R**: Restart game
- **N**: Next level (after winning)

## Your Task

1. Play the game and find bugs (there are at least 5!)
2. Write detailed bug reports for each bug
3. Identify the root causes
4. Fix the bugs in **one** of the three versions
5. Upload your solution files directly to Moodle before the deadline

## Deadline

Tuesday 20th October at 12 noon (midday)

## Troubleshooting

### tkinter Issues
If you get tkinter import errors:
- **Ubuntu/Debian:** `sudo apt-get install python3-tk`
- **CentOS/RHEL:** `sudo yum install tkinter`
- **Arch Linux:** `sudo pacman -S tk`
- **macOS/Windows:** tkinter should be included with Python

### Testing tkinter
Test tkinter availability: `python3 -c "import tkinter; print('tkinter works!')"`