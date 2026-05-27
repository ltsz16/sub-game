"""
systems/detection.py — Visual and sonar detection logic.
"""

import math
import random


# ─── Visual detection ─────────────────────────────────────────────────────────

def visual_detection_range(sub_depth: float, sea_state: int, is_day: bool) -> float:
    """
    Range (nm) at which the sub can be visually spotted.
    sub_depth : 0 = surfaced
    sea_state : 0 (calm) – 5 (storm)
    is_day    : True if daytime
    """
    if sub_depth > 0:
        # Submerged — periscope feather only
        if sub_depth > 60:
            return 0.0  # no periscope wake visible
        base = 1.5   # periscope wake visible to sharp-eyed lookout
    else:
        base = 8.0   # surfaced conning tower

    # Weather reduces visibility
    weather_factor = max(0.3, 1.0 - sea_state * 0.15)
    # Night halves range
    day_factor = 1.0 if is_day else 0.4
    return base * weather_factor * day_factor


def sonar_detection_check(sub, escort, is_day: bool) -> bool:
    """
    Returns True if escort's sonar detects the submarine.
    Factors: sub speed (noise), sub depth (propagation), decoy, escort sonar range.
    """
    if sub.depth <= 0:
        return False  # surfaced subs are visible, not sonar targets

    # Base detection probability at sonar range
    dist = _distance_nm(escort.lon, escort.lat, sub.lon, sub.lat)
    if dist > escort.sonar_range:
        return False

    # Probability based on distance (closer = higher)
    base_prob = 0.8 * (1.0 - dist / escort.sonar_range)

    # Speed increases noise
    speed_noise = (sub.speed / max(1.0, sub.spec["speed_submerged"])) ** 2
    base_prob *= (0.3 + 0.7 * speed_noise)

    # Deep depth helps (thermal layer, noise absorption)
    depth_factor = 1.0
    if sub.depth > 200:
        depth_factor = 0.6
    elif sub.depth > 300:
        depth_factor = 0.3
    base_prob *= depth_factor

    # Silent running drastically reduces detection
    if sub.silent_running:
        base_prob *= 0.25

    # Active decoy confuses sonar
    if sub.decoy_active:
        base_prob *= 0.15

    return random.random() < base_prob


def visual_check(sub, ship, is_day: bool, sea_state: int) -> bool:
    """True if ship visually spots the submarine."""
    dist = _distance_nm(ship.lon, ship.lat, sub.lon, sub.lat)
    vis_range = visual_detection_range(sub.depth, sea_state, is_day)
    if dist > vis_range:
        return False
    # Higher probability when closer
    prob = 0.9 * (1.0 - dist / max(0.1, vis_range))
    return random.random() < prob


def convoy_detection_check(sub, convoy, is_day: bool, sea_state: int) -> bool:
    """
    Returns True if the convoy (any ship) detects the submarine.
    Checks both sonar (escorts) and visual.
    """
    for ship in convoy.alive_ships:
        if ship.is_warship:
            if sonar_detection_check(sub, ship, is_day):
                return True
        if visual_check(sub, ship, is_day, sea_state):
            return True
    return False


def player_visual_contact(sub, convoy, is_day: bool, sea_state: int) -> bool:
    """
    Can the player's submarine detect the convoy?
    Surfaced lookout or periscope observation.
    """
    for ship in convoy.alive_ships:
        dist = _distance_nm(sub.lon, sub.lat, ship.lon, ship.lat)
        if sub.surfaced or sub.is_periscope_depth:
            # Surfaced: up to 10 nm clear weather / day
            max_vis = 10.0 if is_day else 4.0
            max_vis *= max(0.3, 1.0 - sea_state * 0.15)
            if sub.is_periscope_depth and not sub.surfaced:
                max_vis *= 0.5  # periscope limits view
            if dist <= max_vis:
                return True
    return False


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _distance_nm(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    dlon = (lon2 - lon1) * math.cos(math.radians(lat1)) * 60.0
    dlat = (lat2 - lat1) * 60.0
    return math.sqrt(dlon**2 + dlat**2)
