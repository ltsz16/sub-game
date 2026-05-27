"""
constants.py — Global constants for Pacific Patrol 1941
"""

import pygame

# ─── Screen ────────────────────────────────────────────────────────────────────
SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 800
FPS           = 60
TITLE         = "PACIFIC PATROL 1941"
SAVE_DIR      = "saves"

# ─── Color Palette ─────────────────────────────────────────────────────────────
# Dark naval theme with phosphor-green instruments, amber text
BLACK         = (0,   0,   0)
NEAR_BLACK    = (5,   8,  12)
DARK_NAVY     = (8,  16,  32)
NAVY          = (12,  24,  48)
DARK_BLUE     = (10,  30,  60)
OCEAN_DEEP    = (0,   20,  45)
OCEAN_MID     = (0,   40,  80)
OCEAN_SURFACE = (0,   60, 110)
OCEAN_BRIGHT  = (20,  90, 140)
OCEAN_FOAM    = (80, 160, 200)
SKY_DARK      = (20,  30,  50)
SKY_MID       = (50,  80, 130)
SKY_HORIZON   = (100,140, 180)

WHITE         = (255, 255, 255)
LIGHT_GRAY    = (200, 200, 200)
GRAY          = (128, 128, 128)
DARK_GRAY     = (64,  64,  64)

# Phosphor green (instruments, map overlays)
PHOSPHOR_BRIGHT  = (0,  255, 100)
PHOSPHOR_MID     = (0,  200,  80)
PHOSPHOR_DIM     = (0,  140,  55)
PHOSPHOR_DARK    = (0,   60,  25)

# Amber (text, warnings)
AMBER_BRIGHT  = (255, 200,  50)
AMBER_MID     = (220, 160,  20)
AMBER_DIM     = (160, 110,  10)

# Status colors
GREEN_GOOD    = (0,   220,  80)
YELLOW_WARN   = (255, 220,   0)
ORANGE_CAUTION= (255, 140,   0)
RED_DANGER    = (220,  30,  30)
RED_BRIGHT    = (255,  50,  50)
DARK_RED      = (100,   0,   0)

# UI chrome
PANEL_BG      = (15,  20,  30)
PANEL_BORDER  = (40,  70, 100)
PANEL_DARK    = (10,  15,  22)

# Explosion / fire
FIRE_ORANGE   = (255, 120,   0)
FIRE_YELLOW   = (255, 240,  60)
SMOKE_GRAY    = (100,  90,  80)

# ─── Key Bindings ──────────────────────────────────────────────────────────────
KEY_VIEW_CHART     = pygame.K_F1
KEY_VIEW_PERISCOPE = pygame.K_F2
KEY_VIEW_BRIDGE    = pygame.K_F3
KEY_VIEW_DAMAGE    = pygame.K_F4
KEY_VIEW_TORPEDO   = pygame.K_F5

KEY_FIRE_TORPEDO   = pygame.K_SPACE
KEY_DIVE           = pygame.K_d
KEY_SURFACE        = pygame.K_s
KEY_SILENT_RUN     = pygame.K_r
KEY_DEPTH_PERISCOPE = pygame.K_p
KEY_DEPTH_SHALLOW  = pygame.K_a
KEY_DEPTH_CRUSH    = pygame.K_m
KEY_SPEED_UP       = pygame.K_EQUALS   # + key
KEY_SPEED_DOWN     = pygame.K_MINUS
KEY_COURSE_LEFT    = pygame.K_LEFT
KEY_COURSE_RIGHT   = pygame.K_RIGHT
KEY_LAUNCH_DECOY   = pygame.K_x
KEY_TIME_ACCEL_1   = pygame.K_1
KEY_TIME_ACCEL_2   = pygame.K_2
KEY_TIME_ACCEL_3   = pygame.K_3
KEY_TIME_ACCEL_4   = pygame.K_4
KEY_PAUSE          = pygame.K_p
KEY_ESCAPE         = pygame.K_ESCAPE

# ─── Gameplay Constants ─────────────────────────────────────────────────────────
# Time acceleration multipliers (for strategic map)
TIME_ACCEL_LEVELS  = [1, 10, 100, 1000]

# Map / geography (Pacific bounding box in degrees)
MAP_LON_MIN   = 100.0   # East longitude min
MAP_LON_MAX   = 200.0   # Wraps past 180 → effectively -160W
MAP_LAT_MIN   = -40.0
MAP_LAT_MAX   =  55.0

# Knots → pixels per second conversion on strategic map (at zoom=1)
KNOTS_TO_PX_PER_SEC = 0.05

# Max depth limits (feet)
DEPTH_PERISCOPE = 60      # ft — max for scope use
DEPTH_SHALLOW   = 200
DEPTH_DEEP      = 400
DEPTH_CRUSH     = 600     # instant death beyond this

# Battery / fuel
BATTERY_FULL    = 10000   # arbitrary units; drained when submerged
FUEL_FULL       = 100000  # arbitrary units

# ─── Compartment names ─────────────────────────────────────────────────────────
COMPARTMENTS = [
    "Forward Torpedo Room",
    "Battery / Control Room",
    "Engine Room",
    "Conning Tower",
    "Aft Torpedo Room",
]

# ─── Medal names & order ────────────────────────────────────────────────────────
MEDALS = [
    "Medal of Honor",
    "Navy Cross",
    "Silver Star",
    "Bronze Star",
    "Navy Commendation Medal",
]

RANKS = [
    "Ensign",
    "Lieutenant JG",
    "Lieutenant",
    "Lieutenant Commander",
    "Commander",
    "Captain",
    "Rear Admiral",
]

# ─── Font sizes ────────────────────────────────────────────────────────────────
FONT_LARGE  = 36
FONT_MEDIUM = 24
FONT_SMALL  = 18
FONT_TINY   = 14

# ─── Custom events ─────────────────────────────────────────────────────────────
EVENT_CHANGE_SCREEN   = pygame.USEREVENT + 1
EVENT_COMBAT_START    = pygame.USEREVENT + 2
EVENT_PATROL_END      = pygame.USEREVENT + 3
EVENT_HIST_EVENT      = pygame.USEREVENT + 4
