"""
save_load.py — JSON save/load for campaign state.
"""

import json
import os
from datetime import date

from game.constants import SAVE_DIR


def _ensure_save_dir():
    os.makedirs(SAVE_DIR, exist_ok=True)


def save_game(path, career, sub):
    _ensure_save_dir()
    data = {
        "career": {
            "commander_name": career.commander_name,
            "current_date": career.current_date.isoformat(),
            "rank_index": career.rank_index,
            "current_port": career.current_port,
            "open_ports": list(career.open_ports),
            "open_areas": list(career.open_areas),
            "total_tonnage_sunk": career.total_tonnage_sunk,
            "total_ships_sunk": career.total_ships_sunk,
            "total_score": career.total_score,
            "medals": career.medals,
            "triggered_events": list(career.triggered_events),
            "enemy_density_mult": career.enemy_density_mult,
            "enemy_warship_mult": career.enemy_warship_mult,
            "patrol_number": career.patrol_number,
        },
        "submarine": {
            "spec_id": sub.spec["id"],
            "lon": sub.lon,
            "lat": sub.lat,
            "course": sub.course,
            "speed_setting": sub.speed_setting,
            "depth": sub.depth,
            "target_depth": sub.target_depth,
            "battery": sub.battery,
            "fuel": sub.fuel,
            "torpedo_count": sub.torpedo_count,
            "decoys": sub.decoys,
            "damage": sub.damage,
            "flooding": sub.flooding,
            "flooding_rate": sub.flooding_rate,
            "crew_casualties": sub.crew_casualties,
            "torp_speed_high": sub.torp_speed_high,
            "torp_depth": sub.torp_depth,
            "torp_fuse": sub.torp_fuse,
            "torpedo_type": sub.torpedo_type,
        },
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_game(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
