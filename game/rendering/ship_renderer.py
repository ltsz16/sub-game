"""
rendering/ship_renderer.py — Draw ship silhouettes using pygame polygons.

Each ship type has:
    side_poly   : side-view polygon vertices (for periscope/bridge view)
                  normalized to ship_scale × 100 px unit
    top_poly    : top-down polygon vertices (for nav chart / strategic map)

Vertices are relative to the ship center, x=right, y=up on screen (will be flipped).
Scale the vertices by `scale` before drawing.
"""

import math
import pygame


# ─── Ship silhouette definitions ─────────────────────────────────────────────
# Side view: (x, y) tuples, center at (0,0), ship facing right (+x)
# y positive = up on screen
# Units are scaled at render time

_SIDE_SHIP_POLYS: dict[str, list[tuple]] = {

    "small_freighter": [
        (-50, 0), (-45, 8), (-20, 10), (0, 12), (20, 12),
        (35, 10), (45, 6), (48, 0), (48, -4), (-50, -4),
        # Bridge/superstructure
        # (hull done above — superstructure drawn separately)
    ],
    "large_freighter": [
        (-60, 0), (-55, 8), (-30, 12), (0, 14), (30, 14),
        (45, 10), (58, 5), (60, 0), (60, -5), (-60, -5),
    ],
    "tanker": [
        (-65, 0), (-60, 8), (-40, 11), (0, 12), (40, 11),
        (55, 8), (65, 3), (65, 0), (65, -5), (-65, -5),
    ],
    "ammo_ship": [
        (-45, 0), (-40, 9), (-20, 12), (10, 12), (30, 10),
        (42, 6), (44, 0), (44, -4), (-45, -4),
    ],
    "troop_transport": [
        (-70, 0), (-65, 10), (-40, 16), (0, 18), (40, 16),
        (60, 10), (68, 4), (70, 0), (70, -6), (-70, -6),
    ],
    "passenger_cargo": [
        (-65, 0), (-60, 12), (-35, 18), (0, 20), (35, 18),
        (55, 12), (64, 4), (65, 0), (65, -6), (-65, -6),
    ],
    "escort": [
        (-40, 0), (-38, 5), (-20, 7), (10, 7),
        (35, 5), (42, 1), (40, 0), (40, -3), (-40, -3),
    ],
    "destroyer": [
        (-50, 0), (-48, 5), (-30, 7), (10, 7),
        (40, 5), (50, 1), (50, 0), (50, -3), (-50, -3),
    ],
    "light_cruiser": [
        (-60, 0), (-58, 7), (-35, 10), (0, 11),
        (35, 10), (52, 7), (60, 2), (60, 0), (60, -4), (-60, -4),
    ],
    "heavy_cruiser": [
        (-70, 0), (-68, 9), (-45, 13), (0, 14),
        (40, 13), (60, 9), (68, 3), (68, 0), (68, -5), (-70, -5),
    ],
    "battleship": [
        (-100, 0), (-95, 10), (-60, 16), (-20, 18), (20, 18),
        (60, 16), (85, 10), (95, 4), (100, 0), (100, -7), (-100, -7),
    ],
    "carrier": [
        (-90, 0), (-88, 8), (-60, 11), (0, 12), (60, 11),
        (80, 8), (90, 3), (90, 0), (90, -5), (-90, -5),
        # Flight deck extension (top) handled by superstructure
    ],
    # Submarine (player) side view
    "submarine": [
        (-70, -2), (-65, 4), (-50, 8), (0, 9), (50, 8),
        (65, 4), (70, -2), (60, -6), (0, -8), (-60, -6),
    ],
}

# Top-down view polygons (x=right, y=forward/up on screen; ship pointing right)
_TOP_SHIP_POLYS: dict[str, list[tuple]] = {
    "small_freighter":  [(-20, -6), (20, -6), (22, 0), (20, 6), (-20, 6)],
    "large_freighter":  [(-28, -7), (28, -7), (30, 0), (28, 7), (-28, 7)],
    "tanker":           [(-32, -7), (32, -7), (34, 0), (32, 7), (-32, 7)],
    "ammo_ship":        [(-22, -6), (22, -6), (24, 0), (22, 6), (-22, 6)],
    "troop_transport":  [(-34, -8), (34, -8), (36, 0), (34, 8), (-34, 8)],
    "passenger_cargo":  [(-32, -8), (32, -8), (35, 0), (32, 8), (-32, 8)],
    "escort":           [(-18, -4), (18, -4), (22, 0), (18, 4), (-18, 4)],
    "destroyer":        [(-22, -4), (22, -4), (28, 0), (22, 4), (-22, 4)],
    "light_cruiser":    [(-28, -5), (28, -5), (32, 0), (28, 5), (-28, 5)],
    "heavy_cruiser":    [(-34, -6), (34, -6), (38, 0), (34, 6), (-34, 6)],
    "battleship":       [(-50, -9), (50, -9), (55, 0), (50, 9), (-50, 9)],
    "carrier":          [(-45, -7), (45, -7), (48, 0), (45, 7), (-45, 7)],
    "submarine":        [(-30, -3), (30, -3), (35, 0), (30, 3), (-30, 3)],
}

# Superstructure overlays (drawn on top of hull polygon, side view)
# Each entry: list of polygon dicts with keys: poly, offset_x, offset_y
_SUPERSTRUCTURES: dict[str, list[dict]] = {
    "large_freighter": [
        {"poly": [(-8, 0), (8, 0), (8, 14), (-8, 14)], "ox": -20, "oy": 12},
        {"poly": [(-6, 0), (6, 0), (4, 12), (-4, 12)], "ox": 20,  "oy": 12},
    ],
    "tanker": [
        {"poly": [(-6, 0), (6, 0), (6, 10), (-6, 10)], "ox": 50, "oy": 12},
    ],
    "troop_transport": [
        {"poly": [(-10, 0), (10, 0), (8, 20), (-8, 20)], "ox": 0,  "oy": 18},
        {"poly": [(-6,  0), (6,  0), (4, 12), (-4, 12)], "ox": -35,"oy": 12},
    ],
    "passenger_cargo": [
        {"poly": [(-12, 0), (12, 0), (10, 24), (-10, 24)], "ox": 0,  "oy": 20},
        {"poly": [(-6,  0), (6,  0), (4, 12), (-4, 12)],   "ox": -30,"oy": 14},
    ],
    "carrier": [
        # Island superstructure to starboard
        {"poly": [(-4, 0), (8, 0), (8, 14), (-4, 14)], "ox": 55, "oy": 12},
        # Flight deck extension (top flat deck)
        {"poly": [(-88, 0), (88, 0), (88, 4), (-88, 4)], "ox": 0, "oy": 14},
    ],
    "battleship": [
        {"poly": [(-8, 0), (8, 0), (6, 18), (-6, 18)],  "ox": 0,  "oy": 18},
        {"poly": [(-6, 0), (6, 0), (4, 12), (-4, 12)],  "ox": -50,"oy": 12},
        {"poly": [(-6, 0), (6, 0), (4, 12), (-4, 12)],  "ox": 50, "oy": 12},
    ],
    "destroyer": [
        {"poly": [(-4, 0), (4, 0), (3, 10), (-3, 10)], "ox": -10, "oy": 7},
    ],
    "submarine": [
        # Conning tower (sail)
        {"poly": [(-6, 0), (6, 0), (5, 18), (-5, 18)], "ox": -5, "oy": 9},
    ],
}


def _rotate_poly(poly: list, angle_deg: float) -> list:
    """Rotate a polygon's points around origin by angle_deg."""
    rad = math.radians(angle_deg)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    return [(x * cos_a - y * sin_a, x * sin_a + y * cos_a) for x, y in poly]


def _translate_poly(poly: list, cx: float, cy: float) -> list:
    return [(x + cx, y + cy) for x, y in poly]


def _scale_poly(poly: list, scale: float) -> list:
    return [(x * scale, y * scale) for x, y in poly]


def draw_ship_side(surface: pygame.Surface, ship_id: str, cx: int, cy: int,
                   scale: float = 1.0, color=None, facing_right: bool = True,
                   tilt_deg: float = 0.0):
    """
    Draw a ship's side-view silhouette on surface centered at (cx, cy).
    scale=1.0 → nominal size; facing_right → mirror if False.
    tilt_deg  → apply sinking tilt (rotate CW).
    """
    if color is None:
        from game.constants import DARK_GRAY
        color = DARK_GRAY

    hull_poly = _SIDE_SHIP_POLYS.get(ship_id, _SIDE_SHIP_POLYS["small_freighter"])
    structs   = _SUPERSTRUCTURES.get(ship_id, [])

    # Scale
    hull = _scale_poly(hull_poly, scale * 0.01)

    # Flip for facing
    if not facing_right:
        hull = [(-x, y) for x, y in hull]

    # Tilt (sinking)
    if tilt_deg:
        hull = _rotate_poly(hull, tilt_deg)

    # Translate to screen
    hull_pts = _translate_poly(hull, cx, cy)

    # Flip y for pygame (y increases downward)
    hull_pts = [(x, cy - (y - cy)) for x, y in hull_pts]

    pygame.draw.polygon(surface, color, [(int(x), int(y)) for x, y in hull_pts])
    # Outline
    darker = tuple(max(0, c - 40) for c in color)
    pygame.draw.polygon(surface, darker, [(int(x), int(y)) for x, y in hull_pts], 1)

    # Superstructures
    for s in structs:
        sp = _scale_poly(s["poly"], scale * 0.01)
        ox = s["ox"] * scale * 0.01
        oy = s["oy"] * scale * 0.01
        sp = _translate_poly(sp, ox, oy)
        if not facing_right:
            sp = [(-x, y) for x, y in sp]
        if tilt_deg:
            sp = _rotate_poly(sp, tilt_deg)
        sp = _translate_poly(sp, cx, cy)
        sp = [(x, cy - (y - cy)) for x, y in sp]
        pygame.draw.polygon(surface, color, [(int(x), int(y)) for x, y in sp])
        pygame.draw.polygon(surface, darker, [(int(x), int(y)) for x, y in sp], 1)


def draw_ship_top(surface: pygame.Surface, ship_id: str, cx: int, cy: int,
                  scale: float = 1.0, color=None, course_deg: float = 0.0):
    """
    Draw a ship's top-down silhouette on surface centered at (cx, cy).
    course_deg: 0=up (north), 90=right (east).
    """
    if color is None:
        from game.constants import DARK_GRAY
        color = DARK_GRAY

    poly = _TOP_SHIP_POLYS.get(ship_id, _TOP_SHIP_POLYS["small_freighter"])
    poly = _scale_poly(poly, scale * 0.3)
    # Rotate: default poly faces right (+x); convert course to rotation
    rotation = course_deg - 90  # 0° course (north) needs -90° rotation
    poly = _rotate_poly(poly, rotation)
    poly = _translate_poly(poly, cx, cy)
    pygame.draw.polygon(surface, color, [(int(x), int(y)) for x, y in poly])
    darker = tuple(max(0, c - 40) for c in color)
    pygame.draw.polygon(surface, darker, [(int(x), int(y)) for x, y in poly], 1)
