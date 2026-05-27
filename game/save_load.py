"""
save_load.py — JSON save/load for campaign state.
"""

import json
import os
from datetime import date

from game.constants import SAVE_DIR
from game.data.submarines import SUBMARINE_BY_ID
from game.systems.career import CareerState
from game.entities.submarine import Submarine


def _ensure_save_dir():
    os.makedirs(SAVE_DIR, exist_ok=True)


def default_save_path():
    _ensure_save_dir()
    return os.path.join(SAVE_DIR, "career_save.json")


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
            "tubes_fore": [
                {
                    "loaded": t.loaded,
                    "torpedo_type": t.torpedo_type,
                    "reload_timer": t.reload_timer,
                }
                for t in sub.tubes_fore
            ],
            "tubes_aft": [
                {
                    "loaded": t.loaded,
                    "torpedo_type": t.torpedo_type,
                    "reload_timer": t.reload_timer,
                }
                for t in sub.tubes_aft
            ],
        },
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_game(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_game_state(path):
    """Load and rehydrate CareerState and Submarine from a save file."""
    data = load_game(path)

    c = data["career"]
    s = data["submarine"]

    spec = SUBMARINE_BY_ID[s["spec_id"]]
    career = CareerState(c.get("commander_name", "Commander"), spec)
    career.current_date = date.fromisoformat(c["current_date"])
    career.rank_index = c.get("rank_index", career.rank_index)
    career.current_port = c.get("current_port", career.current_port)
    career.open_ports = set(c.get("open_ports", list(career.open_ports)))
    career.open_areas = set(c.get("open_areas", list(career.open_areas)))
    career.total_tonnage_sunk = c.get("total_tonnage_sunk", 0)
    career.total_ships_sunk = c.get("total_ships_sunk", 0)
    career.total_score = c.get("total_score", 0.0)
    career.medals = list(c.get("medals", []))
    career.triggered_events = set(c.get("triggered_events", []))
    career.enemy_density_mult = c.get("enemy_density_mult", 1.0)
    career.enemy_warship_mult = c.get("enemy_warship_mult", 1.0)
    career.patrol_number = c.get("patrol_number", 0)

    sub = Submarine(spec)
    sub.lon = s.get("lon", sub.lon)
    sub.lat = s.get("lat", sub.lat)
    sub.course = s.get("course", sub.course)
    sub.set_speed(s.get("speed_setting", sub.speed_setting))
    sub.depth = s.get("depth", sub.depth)
    sub.target_depth = s.get("target_depth", sub.target_depth)
    sub.battery = s.get("battery", sub.battery)
    sub.fuel = s.get("fuel", sub.fuel)
    sub.torpedo_count = s.get("torpedo_count", sub.torpedo_count)
    sub.decoys = s.get("decoys", sub.decoys)
    sub.damage.update(s.get("damage", {}))
    sub.flooding.update(s.get("flooding", {}))
    sub.flooding_rate.update(s.get("flooding_rate", {}))
    sub.crew_casualties = s.get("crew_casualties", 0)
    sub.torp_speed_high = s.get("torp_speed_high", sub.torp_speed_high)
    sub.torp_depth = s.get("torp_depth", sub.torp_depth)
    sub.torp_fuse = s.get("torp_fuse", sub.torp_fuse)
    sub.torpedo_type = s.get("torpedo_type", sub.torpedo_type)

    for tube_state, tube in zip(s.get("tubes_fore", []), sub.tubes_fore):
        tube.loaded = tube_state.get("loaded", tube.loaded)
        tube.torpedo_type = tube_state.get("torpedo_type", tube.torpedo_type)
        tube.reload_timer = tube_state.get("reload_timer", tube.reload_timer)

    for tube_state, tube in zip(s.get("tubes_aft", []), sub.tubes_aft):
        tube.loaded = tube_state.get("loaded", tube.loaded)
        tube.torpedo_type = tube_state.get("torpedo_type", tube.torpedo_type)
        tube.reload_timer = tube_state.get("reload_timer", tube.reload_timer)

    return career, sub
