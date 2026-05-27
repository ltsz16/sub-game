"""
entities/depth_charge.py — Depth charge entity and pattern.
"""

import math
import random


class DepthCharge:
    """A single depth charge dropped in the water."""

    LETHAL_RADIUS  = 0.008   # nm — instant kill zone
    DAMAGE_RADIUS  = 0.025   # nm — damage zone
    SINK_RATE      = 8.0     # feet per second descent rate

    def __init__(self, lon: float, lat: float, detonation_depth: float):
        self.lon = lon
        self.lat = lat
        self.detonation_depth = detonation_depth
        self.current_depth = 0.0    # starts at surface
        self.active = True
        self.exploded = False
        self.explosion_timer = 0.0  # seconds explosion visual lasts

    def update(self, dt: float):
        if not self.active:
            if self.explosion_timer > 0:
                self.explosion_timer -= dt
            return
        # Sink toward detonation depth
        self.current_depth += self.SINK_RATE * dt
        if self.current_depth >= self.detonation_depth:
            self.active = False
            self.exploded = True
            self.explosion_timer = 2.0

    def distance_to_sub(self, sub_lon: float, sub_lat: float, sub_depth: float) -> float:
        """3D distance (nm) from charge to submarine."""
        dlon = (sub_lon - self.lon) * math.cos(math.radians(self.lat)) * 60.0
        dlat = (sub_lat - self.lat) * 60.0
        # Depth difference in nm (1 nm ≈ 6076 ft)
        ddepth = (sub_depth - self.current_depth) / 6076.0
        return math.sqrt(dlon ** 2 + dlat ** 2 + ddepth ** 2)

    def check_damage(self, sub_lon: float, sub_lat: float, sub_depth: float) -> float:
        """
        Returns damage fraction 0.0–1.0 based on proximity.
        Only meaningful when exploded.
        """
        if not self.exploded:
            return 0.0
        dist = self.distance_to_sub(sub_lon, sub_lat, sub_depth)
        if dist <= self.LETHAL_RADIUS:
            return 1.0
        elif dist <= self.DAMAGE_RADIUS:
            # Linear falloff
            frac = 1.0 - (dist - self.LETHAL_RADIUS) / (self.DAMAGE_RADIUS - self.LETHAL_RADIUS)
            return frac * 0.5  # max 0.5 damage at edge
        return 0.0


class DCPattern:
    """
    A full depth-charge pattern dropped by one escort pass.
    Generates individual charges in a spread pattern.
    """

    def __init__(self, center_lon: float, center_lat: float,
                 count: int, est_sub_depth: float, spread_nm: float = 0.03):
        self.charges: list[DepthCharge] = []
        # Vary detonation depths around estimate
        for _ in range(count):
            jitter_lon = center_lon + random.uniform(-spread_nm / 60, spread_nm / 60)
            jitter_lat = center_lat + random.uniform(-spread_nm / 60, spread_nm / 60)
            depth_offset = random.uniform(-50, 50)
            det_depth = max(50.0, est_sub_depth + depth_offset)
            self.charges.append(DepthCharge(jitter_lon, jitter_lat, det_depth))
        self.done = False

    def update(self, dt: float):
        all_done = True
        for charge in self.charges:
            charge.update(dt)
            if charge.active or charge.explosion_timer > 0:
                all_done = False
        self.done = all_done

    def evaluate_damage(self, sub_lon: float, sub_lat: float, sub_depth: float) -> float:
        """Total damage from all charges in this pattern."""
        total = 0.0
        for charge in self.charges:
            if charge.exploded:
                total += charge.check_damage(sub_lon, sub_lat, sub_depth)
        return min(1.0, total)
