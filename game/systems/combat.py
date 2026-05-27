"""
systems/combat.py — Combat resolution: torpedo hits, gun fire, depth charges, sinking.
"""

import random
import math
from game.entities.ship import ShipState
from game.entities.depth_charge import DCPattern
from game.constants import COMPARTMENTS


def check_torpedo_hits(torpedoes: list, convoys: list) -> list:
    """
    Check all active torpedoes against all ships in convoys.
    Returns list of (torpedo, ship, convoy) for each hit.
    """
    hits = []
    for torp in torpedoes:
        if not torp.active:
            continue
        for convoy in convoys:
            for ship in convoy.alive_ships:
                if torp.check_hit(ship):
                    hits.append((torp, ship, convoy))
                    torp.detonate()
                    break
    return hits


def resolve_torpedo_hit(ship, game_year: int = 1943) -> dict:
    """
    Apply torpedo damage to a ship.
    Early-war Mark 14 had notorious dud problems.

    Returns dict with: dud (bool), sinking (bool), message (str)
    """
    # Mark 14 dud rate: ~70% early war (1941-1943), fixed later
    dud_chance = 0.0
    if game_year < 1943:
        dud_chance = 0.40   # 40% dud pre-fix
    elif game_year == 1943:
        dud_chance = 0.15

    if random.random() < dud_chance:
        return {
            "dud": True,
            "sinking": False,
            "message": "TORPEDO DUD! No detonation.",
        }

    # Ammo ship special: massive explosion
    if ship.ship_id == "ammo_ship" and random.random() < 0.8:
        sinking = ship.hit(ship.max_hp)  # instant kill
        return {
            "dud": False,
            "sinking": True,
            "message": "MASSIVE EXPLOSION — Ammunition ship destroyed!",
        }

    # Normal hit
    sinking = ship.hit(1)
    if sinking:
        msg = f"{ship.name} SINKING!"
    else:
        msg = f"HIT! {ship.name} — {ship.hp}/{ship.max_hp} HP remaining."

    return {"dud": False, "sinking": sinking, "message": msg}


def deck_gun_fire(sub_lon: float, sub_lat: float,
                  ship, aim_error_deg: float = 5.0) -> dict:
    """
    Resolve a deck gun shot at a surface target.

    aim_error_deg: random aim error in degrees
    Returns hit/miss dict with message.
    """
    # Distance to target in nm
    dlon = (ship.lon - sub_lon) * math.cos(math.radians(sub_lat)) * 60.0
    dlat = (ship.lat - sub_lat) * 60.0
    dist = math.sqrt(dlon**2 + dlat**2)

    # Hit probability: 100% at 0.5 nm, drops off
    base_hit = max(0.0, 1.0 - dist / 3.0)
    if random.random() > base_hit:
        return {"hit": False, "message": f"MISS — shell fell {'short' if random.random() < 0.5 else 'long'}."}

    sinking = ship.hit(1)
    if sinking:
        msg = f"DECK GUN HIT — {ship.name} is SINKING!"
    else:
        msg = f"DECK GUN HIT — {ship.name} ({ship.hp}/{ship.max_hp} HP)"
    return {"hit": True, "sinking": sinking, "message": msg}


def apply_depth_charge_damage(dc_pattern: DCPattern, submarine,
                               convoys: list) -> dict:
    """
    Evaluate depth charge damage on the submarine from a pattern.
    Applies damage to random compartments based on blast proximity.
    Returns a dict with total_damage and messages.
    """
    damage = dc_pattern.evaluate_damage(submarine.lon, submarine.lat, submarine.depth)
    messages = []

    if damage <= 0.0:
        return {"damage": 0.0, "messages": ["Depth charges — no damage."]}

    # Spread damage across compartments
    num_hit = max(1, int(damage * 3))
    hit_comps = random.sample(COMPARTMENTS, min(num_hit, len(COMPARTMENTS)))
    per_comp  = damage / max(1, len(hit_comps))

    for comp in hit_comps:
        submarine.apply_damage(comp, per_comp)
        sev = "CRITICAL" if per_comp > 0.5 else "DAMAGE"
        messages.append(f"{sev}: {comp}")

    # Alert all escort ships to sub's current position
    for convoy in convoys:
        for ship in convoy.alive_ships:
            if ship.is_warship:
                ship.alert(submarine.lon, submarine.lat)

    return {"damage": damage, "messages": messages}


def generate_dc_pattern(attacking_ship, submarine) -> DCPattern:
    """Build a depth charge pattern from an escort attacking the sub."""
    dcs, _ = attacking_ship.dc_patterns
    return DCPattern(
        center_lon=submarine.lon + random.uniform(-0.02, 0.02),
        center_lat=submarine.lat + random.uniform(-0.02, 0.02),
        count=dcs,
        est_sub_depth=submarine.depth + random.uniform(-80, 80),
    )
