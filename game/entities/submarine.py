"""
entities/submarine.py — Player submarine state.
"""

import math
from dataclasses import dataclass, field
from typing import List, Dict

from game.constants import (
    BATTERY_FULL, FUEL_FULL, COMPARTMENTS,
    DEPTH_PERISCOPE, DEPTH_SHALLOW, DEPTH_CRUSH,
)


@dataclass
class TorpedoTube:
    """State of one torpedo tube."""
    loaded: bool = True
    torpedo_type: str = "mk14"   # mk10, mk14, mk18
    reload_timer: float = 0.0    # seconds remaining (0 = ready)
    RELOAD_TIME: float = 90.0    # seconds to reload

    @property
    def ready(self) -> bool:
        return self.loaded and self.reload_timer <= 0.0

    def fire(self):
        self.loaded = False
        self.reload_timer = 0.0

    def start_reload(self, torpedo_type: str = "mk14"):
        self.torpedo_type = torpedo_type
        self.loaded = False
        self.reload_timer = self.RELOAD_TIME

    def update(self, dt: float):
        if self.reload_timer > 0:
            self.reload_timer = max(0.0, self.reload_timer - dt)
            if self.reload_timer == 0.0:
                self.loaded = True


class Submarine:
    """All runtime state for the player's submarine."""

    def __init__(self, spec: dict):
        self.spec = spec                    # from data/submarines.py
        self.name = spec["name"]

        # ─── Position & motion ──────────────────────────────────────────────
        self.lon: float = 0.0             # position in degrees
        self.lat: float = 0.0
        self.course: float = 0.0          # heading 0-359 degrees (0=N)
        self.speed: float = 0.0           # current speed in knots (0-max)
        self.speed_setting: int = 0       # 0=stop,1=slow,2=standard,3=full
        self.depth: float = 0.0           # current depth in feet (0=surface)
        self.target_depth: float = 0.0   # ordered depth

        # ─── Resources ───────────────────────────────────────────────────────
        self.battery: float = BATTERY_FULL
        self.fuel: float = FUEL_FULL
        self.torpedo_count: int = spec["torpedo_capacity"]
        self.decoys: int = 6

        # ─── Torpedo tubes ────────────────────────────────────────────────────
        fore_count = spec["tubes_fore"]
        aft_count  = spec["tubes_aft"]
        self.tubes_fore: List[TorpedoTube] = [TorpedoTube() for _ in range(fore_count)]
        self.tubes_aft:  List[TorpedoTube] = [TorpedoTube() for _ in range(aft_count)]
        # Default torpedo type assigned by game year
        self.torpedo_type: str = "mk14"
        # Torpedo settings
        self.torp_speed_high: bool = True
        self.torp_depth: float = 10.0       # ft
        self.torp_fuse: str = "contact"     # "contact" | "magnetic"

        # ─── Damage (0.0=intact, 1.0=destroyed) ─────────────────────────────
        self.damage: Dict[str, float] = {c: 0.0 for c in COMPARTMENTS}
        self.flooding: Dict[str, float] = {c: 0.0 for c in COMPARTMENTS}
        # flooding rate (0=no flood, >0=water/sec entering)
        self.flooding_rate: Dict[str, float] = {c: 0.0 for c in COMPARTMENTS}

        # ─── Crew ────────────────────────────────────────────────────────────
        self.crew: int = spec["crew"]
        self.crew_casualties: int = 0

        # ─── Repair state ─────────────────────────────────────────────────────
        self.repair_assignment: str | None = None  # compartment being repaired

        # ─── Tactical state ──────────────────────────────────────────────────
        self.surfaced: bool = True
        self.periscope_up: bool = False
        self.silent_running: bool = False
        self.radar_on: bool = False
        self.decoy_active: bool = False
        self.decoy_timer: float = 0.0

        # ─── Status flags ────────────────────────────────────────────────────
        self.is_sunk: bool = False

    # ─── Convenience properties ───────────────────────────────────────────────

    @property
    def max_speed(self) -> float:
        if self.surfaced:
            return self.spec["speed_surface"]
        return self.spec["speed_submerged"]

    @property
    def max_depth(self) -> float:
        return float(self.spec["max_depth"])

    @property
    def hull_integrity(self) -> float:
        """0.0 (destroyed) – 1.0 (pristine), averaged across compartments."""
        vals = [1.0 - self.damage[c] for c in COMPARTMENTS]
        return sum(vals) / len(vals)

    @property
    def battery_pct(self) -> float:
        return self.battery / BATTERY_FULL

    @property
    def fuel_pct(self) -> float:
        return self.fuel / FUEL_FULL

    @property
    def can_fire_fore(self) -> bool:
        return any(t.ready for t in self.tubes_fore)

    @property
    def can_fire_aft(self) -> bool:
        return any(t.ready for t in self.tubes_aft)

    @property
    def is_periscope_depth(self) -> bool:
        return self.depth <= DEPTH_PERISCOPE and not self.surfaced

    # ─── Speed helpers ────────────────────────────────────────────────────────

    SPEED_FRACTIONS = [0.0, 0.33, 0.67, 1.0]  # stop, slow, standard, full

    def set_speed(self, setting: int):
        self.speed_setting = max(0, min(3, setting))

    def target_speed(self) -> float:
        return self.max_speed * self.SPEED_FRACTIONS[self.speed_setting]

    # ─── Tube helpers ─────────────────────────────────────────────────────────

    def get_ready_fore_tube(self) -> TorpedoTube | None:
        for t in self.tubes_fore:
            if t.ready:
                return t
        return None

    def get_ready_aft_tube(self) -> TorpedoTube | None:
        for t in self.tubes_aft:
            if t.ready:
                return t
        return None

    def fire_fore(self) -> bool:
        """Fire one fore tube. Returns True if successful."""
        tube = self.get_ready_fore_tube()
        if tube and self.torpedo_count > 0:
            tube.fire()
            self.torpedo_count -= 1
            return True
        return False

    def fire_aft(self) -> bool:
        tube = self.get_ready_aft_tube()
        if tube and self.torpedo_count > 0:
            tube.fire()
            self.torpedo_count -= 1
            return True
        return False

    def reload_fore(self):
        for tube in self.tubes_fore:
            if not tube.loaded and tube.reload_timer <= 0:
                tube.start_reload(self.torpedo_type)
                break

    def reload_aft(self):
        for tube in self.tubes_aft:
            if not tube.loaded and tube.reload_timer <= 0:
                tube.start_reload(self.torpedo_type)
                break

    # ─── Damage helpers ───────────────────────────────────────────────────────

    def apply_damage(self, compartment: str, amount: float):
        if compartment in self.damage:
            self.damage[compartment] = min(1.0, self.damage[compartment] + amount)
            if self.damage[compartment] > 0.7:
                self.flooding_rate[compartment] = (self.damage[compartment] - 0.7) * 0.01

    def apply_flooding(self, dt: float):
        for comp in COMPARTMENTS:
            if self.flooding_rate[comp] > 0:
                self.flooding[comp] = min(1.0, self.flooding[comp] + self.flooding_rate[comp] * dt)
                if self.flooding[comp] > 0.5:
                    # Flooding worsens damage
                    self.damage[comp] = min(1.0, self.damage[comp] + 0.0005 * dt)

    def repair_tick(self, dt: float):
        if self.repair_assignment and self.repair_assignment in self.damage:
            comp = self.repair_assignment
            # Slow repair
            if self.damage[comp] > 0:
                self.damage[comp] = max(0.0, self.damage[comp] - 0.002 * dt)
            if self.flooding_rate[comp] > 0:
                self.flooding_rate[comp] = max(0.0, self.flooding_rate[comp] - 0.0005 * dt)

    def launch_decoy(self) -> bool:
        if self.decoys > 0 and not self.decoy_active:
            self.decoys -= 1
            self.decoy_active = True
            self.decoy_timer = 45.0  # decoy lasts 45 seconds
            return True
        return False

    # ─── Update ──────────────────────────────────────────────────────────────

    def update(self, dt: float):
        # Speed approach
        target = self.target_speed()
        diff = target - self.speed
        accel = 0.5 * dt  # knots per second approach rate
        if abs(diff) < accel:
            self.speed = target
        else:
            self.speed += math.copysign(accel, diff)

        # Depth approach
        d_diff = self.target_depth - self.depth
        dive_rate = 30.0 * dt  # feet per second
        if abs(d_diff) < dive_rate:
            self.depth = self.target_depth
        else:
            self.depth += math.copysign(dive_rate, d_diff)
        self.surfaced = (self.depth <= 0.0)
        self.periscope_up = self.is_periscope_depth and not self.surfaced

        # Move position
        if self.speed > 0:
            # Convert knots to degrees/second (1 knot ≈ 0.000278 deg/s lat)
            speed_deg_s = self.speed * (1.0 / 3600.0)  # degrees per second at equator
            rad = math.radians(self.course)
            self.lat += math.cos(rad) * speed_deg_s * dt
            self.lon += math.sin(rad) * speed_deg_s * dt / max(0.1, math.cos(math.radians(self.lat)))

        # Battery drain when submerged
        if not self.surfaced:
            drain_rate = self.speed / max(0.01, self.spec["speed_submerged"]) * 10.0
            self.battery = max(0.0, self.battery - drain_rate * dt)
            if self.battery <= 0:
                self.speed_setting = 0  # forced stop
        else:
            # Recharge on surface (engine)
            self.battery = min(BATTERY_FULL, self.battery + 20.0 * dt)
            # Fuel drain (surface only)
            fuel_rate = self.speed * 2.0
            self.fuel = max(0.0, self.fuel - fuel_rate * dt)

        # Flooding
        self.apply_flooding(dt)
        self.repair_tick(dt)

        # Decoy
        if self.decoy_active:
            self.decoy_timer -= dt
            if self.decoy_timer <= 0:
                self.decoy_active = False

        # Tube reloads
        for tube in self.tubes_fore + self.tubes_aft:
            tube.update(dt)

        # Crush depth check
        if self.depth >= DEPTH_CRUSH:
            self.is_sunk = True

        # Flooding check
        critical_flood = sum(1 for v in self.flooding.values() if v >= 1.0)
        if critical_flood >= 2:
            self.is_sunk = True

    def reset_for_patrol(self):
        """Refuel, rearm, and repair for next patrol."""
        self.torpedo_count = self.spec["torpedo_capacity"]
        self.fuel = FUEL_FULL
        self.battery = BATTERY_FULL
        self.decoys = 6
        self.damage = {c: 0.0 for c in COMPARTMENTS}
        self.flooding = {c: 0.0 for c in COMPARTMENTS}
        self.flooding_rate = {c: 0.0 for c in COMPARTMENTS}
        self.crew_casualties = 0
        self.is_sunk = False
        self.depth = 0.0
        self.target_depth = 0.0
        self.surfaced = True
        self.speed = 0.0
        self.speed_setting = 0
        for tube in self.tubes_fore + self.tubes_aft:
            tube.loaded = True
            tube.reload_timer = 0.0

    def surface_status_text(self) -> list[str]:
        lines = [
            f"Boat: {self.name}",
            f"Depth: {self.depth:.0f} ft  Target: {self.target_depth:.0f} ft",
            f"Speed: {self.speed:.1f} kts (Sett {self.speed_setting})",
            f"Course: {self.course:.0f}°",
            f"Battery: {self.battery_pct*100:.0f}%",
            f"Fuel: {self.fuel_pct*100:.0f}%",
            f"Torpedoes: {self.torpedo_count}",
            f"Decoys: {self.decoys}",
        ]
        return lines
