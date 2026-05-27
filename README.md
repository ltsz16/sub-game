# Pacific Patrol 1941

Pacific Patrol 1941 is a Python WWII submarine campaign game inspired by classic Pacific-theater sub simulators.

You command a US submarine through a full Pacific war career, navigate a strategic map, engage enemy convoys, manage damage, fire torpedoes, and track tonnage, medals, and promotions.

## Features

- Strategic Pacific campaign map with time acceleration
- Dynamic convoy contacts and combat transitions
- **Submarine class selection with historical specifications and class images**
- Multiple combat views with integrated WWII-style gauges:
	- Chart Room (tactical overhead)
	- Periscope View
	- Bridge View
	- Damage Control
	- Torpedo Room
- **Full submarine control system:**
	- Depth management (dive/surface/periscope depth)
	- Speed control (0-3 knots equivalent settings)
	- Course heading adjustment
	- Crush depth safety (automatic sinking below 600 ft)
- **Improved torpedo system** with depth, speed, and fuse settings
- **Enhanced depth charge mechanics** with realistic distance-based damage calculations
- Compartment damage and flooding with repair management
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
2. **Select a submarine class** (view specifications and class image)
3. Enter strategic map and assign patrol area
4. Trigger/encounter enemy convoy contact
5. Review XO briefing with target information
6. Fight from chart/periscope/bridge/damage/torpedo views
7. Complete patrol and review patrol report with medals/promotions
8. Return to strategic map and continue war career

### Submarine Selection

When starting a new career, choose from 12 historical US submarine classes:
- View detailed specs (tonnage, speed, depth rating, torpedo capacity)
- See historical class photo
- Each class has different combat characteristics and crush depth limits

### Battle System

Once in combat:
- **Depth management**: Use D/S keys to dive/surface at 30 ft/sec approach rate
- **Speed control**: Arrow keys adjust speed setting (affects battery drain and noise)
- **Course heading**: Adjust bearing to aim at targets
- **View switching**: F1-F5 cycles between specialized combat views
- **Depth charges**: Enemy escorts drop patterns when you're detected; closer detonations cause more damage
- **Damage cascades**: Hull breaches, fires, and flooding require damage control attention

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

**Navigation & Depth Control (all views):**
- F1: Chart Room
- F2: Periscope View
- F3: Bridge View
- F4: Damage Control
- F5: Torpedo Room

**Depth/Speed/Course (all views):**
- D: Dive (+50 ft)
- S: Surface (0 ft)

### Chart Room (Tactical)

- Left / Right: course changes (±5°)
- Up / Down: speed setting changes (0-3)
- D / S: dive/surface
- Space: fire fore torpedo
- F1-F5: switch views

### Periscope View

- Left / Right: fine course adjustment (±2°)
- Up / Down: speed setting changes (0-3)
- D / S: dive/surface (includes deeper dive)
- Space: fire fore torpedo
- F1-F5: switch views

### Bridge View

- Left / Right: course changes (±3°)
- Up / Down: speed setting changes (0-3)
- D / S: dive/surface
- F1-F5: switch views

### Navigation Chart

- Left / Right: coarse course changes (±5°)
- Up / Down: speed setting changes (0-3)
- D / S: dive/surface
- Space: fire fore torpedo
- F1-F5: switch views

### Damage Control

- 1-5: assign repair team to compartment (higher number = more repair capacity)
- 0: clear repair assignment
- View compartment damage, flooding rate, and repair progress

**Emergency procedures:**
- Critical flooding in 2+ compartments: submarine sinks
- Depth below crush limit (600 ft): automatic sinking
- Monitor hull status continuously during damage

### Torpedo Room

- R: reload empty tubes
- T: toggle torpedo speed (high/low)
- F: toggle fuse type (contact/magnetic)
- [: decrease torpedo depth
- ]: increase torpedo depth
- D / S: dive/surface (during combat prep)

## Submarine Status Display

During combat, all views display submarine operational data with **WWII-style analog gauges**:
- **Depth gauge**: Current depth with crush depth warning zone (red area at 600+ ft)
- **Speed gauge**: Current speed in knots (0-20+ range)
- **Heading indicator**: Compass with cardinal directions
- **Battery indicator**: Power level for submerged operations
- **Trim indicator**: Bow up/down position during maneuvers

This immersive display provides authentic 1940s submarine aesthetic while conveying critical operational data at a glance.

## Depth Charge Mechanics

**When detected by enemy escorts:**
- Warships estimate your depth and drop depth charge patterns
- Multiple charges spread across 100-yard area sink toward estimated depth
- Detonation calculated based on proximity (3D distance)
- **Damage zones:**
  - Lethal (within ~60 ft): 1.0 damage per charge
  - Damaging (~210 ft): 0.5 max damage per charge
  - Beyond: no damage
- Damage spreads to 1-3 random compartments
- Hull breaches increase flooding rate significantly

**Tactics:**
- Change depth frequently to break enemy targeting estimate
- Increase speed to move out of blast zone
- Use decoys or evasive maneuvers if available
- Repair damage immediately to prevent cascade flooding

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

## Technical Notes

- **Sprite-based rendering**: PNG asset support with procedural fallback for dynamic generation
- **WWII-style gauges**: Drawn with Pygame primitives (circles, lines, polygons) for authentic 1940s aesthetic
- **Physics simulation**: Full submarine depth approach, speed ramping, and course navigation
- **Distance-based damage**: 3D proximity calculations for realistic depth charge effects
- **Procedurally generated sound**: Runtime sine wave synthesis for combat effects
- **Save/load system**: Complete campaign state preservation with full submarine and combat data

## Balancing & Configuration

Tune gameplay through configuration in:
- `game/constants.py` - Depth limits, damage radii, control rates, key bindings
- `game/data/ships.py` - Escort warship capabilities and depth charge patterns
- `game/data/submarines.py` - Submarine class specs, tonnage, and max depths
- `game/systems/combat.py` - Combat mechanics, damage calculations, and detection probabilities
