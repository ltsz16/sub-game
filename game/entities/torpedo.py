"""
entities/torpedo.py — Torpedo entity.
"""

import math


class Torpedo:
    # Speed in knots for high/low settings
    SPEED_HIGH = 46.0
    SPEED_LOW  = 31.0
    # Range in nautical miles
    RANGE_HIGH = 4.5
    RANGE_LOW  = 9.0
    # Kill radius in nm
    KILL_RADIUS     = 0.02
    DAMAGE_RADIUS   = 0.05

    def __init__(self, lon: float, lat: float, course: float,
                 depth: float = 10.0, high_speed: bool = True,
                 fuse: str = "contact"):
        self.lon      = lon
        self.lat      = lat
        self.course   = course        # degrees
        self.depth    = depth         # ft
        self.high_speed = high_speed
        self.fuse     = fuse          # "contact" | "magnetic"
        self.speed    = self.SPEED_HIGH if high_speed else self.SPEED_LOW
        self.max_range = self.RANGE_LOW if high_speed else self.RANGE_HIGH
        self.distance_run = 0.0       # nm
        self.active   = True
        self.exploded = False
        # Wake trail for rendering
        self.trail: list[tuple] = []

    def update(self, dt: float):
        if not self.active:
            return
        # Advance position
        speed_nm_s = self.speed / 3600.0
        dist_this_tick = speed_nm_s * dt
        self.distance_run += dist_this_tick

        rad = math.radians(self.course)
        # Convert nm to degrees (approx)
        deg_per_nm = 1.0 / 60.0
        self.lat += math.cos(rad) * dist_this_tick * deg_per_nm
        self.lon += math.sin(rad) * dist_this_tick * deg_per_nm / max(
            0.01, math.cos(math.radians(self.lat))
        )

        # Trail
        self.trail.append((self.lon, self.lat))
        if len(self.trail) > 60:
            self.trail.pop(0)

        # Ran out of fuel
        if self.distance_run >= self.max_range:
            self.active = False

    def distance_to(self, lon: float, lat: float) -> float:
        """Distance in nm to a point."""
        dlon = (lon - self.lon) * math.cos(math.radians(self.lat)) * 60.0
        dlat = (lat - self.lat) * 60.0
        return math.sqrt(dlon ** 2 + dlat ** 2)

    def check_hit(self, ship) -> bool:
        """Returns True if torpedo hits the ship."""
        if not self.active:
            return False
        dist = self.distance_to(ship.lon, ship.lat)
        if self.fuse == "magnetic":
            # Magnetic detonates within damage radius regardless of exact hull hit
            return dist <= self.DAMAGE_RADIUS
        else:
            return dist <= self.KILL_RADIUS

    def detonate(self):
        self.active = False
        self.exploded = True
