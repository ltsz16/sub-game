# Pacific Patrol 1941

Pacific Patrol 1941 is a Python WWII submarine campaign game inspired by classic Pacific-theater sub simulators.

You command a US submarine through a full Pacific war career, navigate a strategic map, engage enemy convoys, manage damage, fire torpedoes, and track tonnage, medals, and promotions.

## Features

- Strategic Pacific campaign map with time acceleration
- Dynamic convoy contacts and combat transitions
- Multiple combat views:
	- Chart Room (tactical overhead)
	- Periscope View
	- Bridge View
	- Damage Control
	- Torpedo Room
- Torpedo firing, reload, depth/fuse/speed settings
- Depth charge attacks and compartment damage/flooding
- Patrol report with sinkings, tonnage, medals, and rank progression
- Historical event popups across the 1941-1945 campaign timeline
- Save/load campaign support

## Requirements

- Python 3.11+
- Windows, Linux, or macOS

Python dependencies are listed in requirements.txt:

- pygame-ce
- numpy

## Installation

1. Create and activate a virtual environment (recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

From the repository root:

```bash
python main.py
```

## Core Flow

1. Main Menu
2. Select a submarine class
3. Enter strategic map and patrol
4. Trigger/encounter contact
5. Review XO briefing
6. Fight from chart/periscope/bridge/damage/torpedo views
7. Complete patrol and review patrol report
8. Return to strategic map and continue war career

## Controls

### Main Menu

- Up / Down: menu selection
- Enter / Space: confirm
- Esc: quit

### Strategic Map

- Left / Right: adjust course
- + / -: speed setting up/down
- 1 / 2 / 3 / 4: time acceleration (1x, 10x, 100x, 1000x)
- P: pause
- Tab: cycle selected patrol area
- C: force contact roll
- H: show pending historical event (if available)
- F9: save campaign
- F10: load campaign
- Esc: back to main menu

### Combat Views

- F1: Chart Room
- F2: Periscope View
- F3: Bridge View
- F4: Damage Control
- F5: Torpedo Room

### Chart Room

- Left / Right: course changes
- + / -: speed setting changes
- Space: fire fore torpedo

### Periscope View

- Left / Right: fine course adjustment
- Space: fire fore torpedo

### Bridge View

- Left / Right: course changes
- Up / Down: speed setting changes

### Damage Control

- 1-5: assign repair team to compartment
- 0: clear repair assignment

### Torpedo Room

- R: reload empty tubes
- T: toggle torpedo speed (high/low)
- F: toggle fuse type (contact/magnetic)
- [: decrease torpedo depth
- ]: increase torpedo depth

## Save and Continue

- Save file location: saves/career_save.json
- Main menu automatically offers Continue Career when a save exists

## Project Structure

```text
main.py
requirements.txt
game/
	constants.py
	state_manager.py
	save_load.py
	sound_manager.py
	data/
	entities/
	systems/
	rendering/
	screens/
```

## Notes

- This is a gameplay-focused prototype with stylized procedural visuals.
- Sound is generated procedurally at runtime.
- Balancing and AI behavior can be tuned in the systems/ and data/ modules.
