"""
Shared combat update helpers for combat view screens.
"""

import random

from game.systems.combat import (
    check_torpedo_hits,
    resolve_torpedo_hit,
    generate_dc_pattern,
    apply_depth_charge_damage,
)
from game.systems.detection import convoy_detection_check


def update_combat_tick(manager, dt):
    state = manager.game_state.get("combat")
    if not state:
        return

    sub = manager.game_state.get("submarine")
    career = manager.game_state.get("career")
    convoy = state["convoy"]

    sub.update(dt)
    convoy.update(dt)

    # Torpedo updates and hit checks
    for torp in state["torpedoes"]:
        torp.update(dt)
    hits = check_torpedo_hits(state["torpedoes"], [convoy])
    for torp, ship, _ in hits:
        state["shots_hit"] += 1
        result = resolve_torpedo_hit(ship, game_year=career.current_date.year)
        state["messages"].append(result["message"])

    # Purge dead torpedoes from list after some time
    state["torpedoes"] = [t for t in state["torpedoes"] if t.active or (not t.active and not t.exploded)]

    # Enemy detection and depth-charge attack
    detected = convoy_detection_check(sub, convoy, is_day=True, sea_state=2)
    if detected:
        convoy.alert_all(sub.lon, sub.lat)
        state["messages"].append("Escort sonar contact!")

    # Random ASW pattern from nearby warship
    for ship in convoy.alive_ships:
        if ship.is_warship and random.random() < 0.004:
            dc = generate_dc_pattern(ship, sub)
            state["dc_patterns"].append(dc)
            state["messages"].append(f"{ship.name} dropping depth charges!")
            break

    for pat in state["dc_patterns"]:
        pat.update(dt)
        dmg = apply_depth_charge_damage(pat, sub, [convoy])
        if dmg["damage"] > 0:
            state["depth_charges_taken"] += 1
            state["messages"].extend(dmg["messages"])
    state["dc_patterns"] = [p for p in state["dc_patterns"] if not p.done]

    # Keep message log short
    if len(state["messages"]) > 12:
        state["messages"] = state["messages"][-12:]


def cycle_to_view(manager, key):
    # Late imports avoid circular dependencies.
    if key == "chart":
        from game.screens.nav_chart import NavChartScreen
        manager.switch(NavChartScreen())
    elif key == "periscope":
        from game.screens.periscope_view import PeriscopeViewScreen
        manager.switch(PeriscopeViewScreen())
    elif key == "bridge":
        from game.screens.bridge_view import BridgeViewScreen
        manager.switch(BridgeViewScreen())
    elif key == "damage":
        from game.screens.damage_control import DamageControlScreen
        manager.switch(DamageControlScreen())
    elif key == "torpedo":
        from game.screens.torpedo_room import TorpedoRoomScreen
        manager.switch(TorpedoRoomScreen())
