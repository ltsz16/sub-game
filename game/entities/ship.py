"""
entities/ship.py — Enemy ship entity.
"""

import math
import random
from enum import Enum, auto


class ShipState(Enum):
    PATROL   = auto()   # following normal route
    ALERTED  = auto()   # aware of sub, searching
    HUNTING  = auto()   # actively prosecuting contact
    EVADING  = auto()   # merchant running away
    SINKING  = auto()   # taking on water, going down
    SUNK     = auto()   # gone


class Ship:
    def __init__(self, spec: dict, lon: float, lat: float, course: float):
        self.spec = spec
        self.ship_id: str   = spec["id"]
        self.name:    str   = spec["name"]
        self.category: str  = spec["category"]

        # ─── Position & motion ────────────────────────────────────────────────
        self.lon: float     = lon
        self.lat: float     = lat
        self.course: float  = course      # degrees, 0=N
        self.speed: float   = spec["speed"]
        self.base_speed: float = spec["speed"]

        # ─── Health ───────────────────────────────────────────────────────────
        self.hp: int        = spec["hp"]
        self.max_hp: int    = spec["hp"]

        # ─── State machine ────────────────────────────────────────────────────
        self.state: ShipState = ShipState.PATROL
        self.alert_timer: float = 0.0    # seconds remaining in alert state
        self.hunt_target_lon: float = lon
        self.hunt_target_lat: float = lat

        # ─── DC attack state (escorts/warships) ───────────────────────────────
        self.dc_cooldown: float = 0.0
        self.attack_run_timer: float = 0.0
        self.attack_run_active: bool = False
        self.drops_remaining: int = 0

        # ─── Visual / sinking animation ─────────────────────────────────────
        self.sinking_timer: float = 0.0
        self.sinking_tilt: float  = 0.0   # degrees list/pitch
        self.smoke_intensity: float = 0.0
        self.fire_intensity: float  = 0.0

        # ─── Waypoints (patrol route) ────────────────────────────────────────
        self.waypoints: list = []
        self.waypoint_idx: int = 0

    # ─── Properties ───────────────────────────────────────────────────────────

    @property
    def is_warship(self) -> bool:
        return self.category in ("warship", "escort")

    @property
    def tonnage(self) -> int:
        return self.spec["tonnage"]

    @property
    def score_value(self) -> float:
        return self.spec["score_value"]

    @property
    def sonar_range(self) -> float:
        return self.spec["sonar_range"]

    @property
    def visual_range(self) -> float:
        return self.spec["visual_range"]

    @property
    def dc_patterns(self):
        return self.spec["dc_patterns"]

    # ─── Damage ───────────────────────────────────────────────────────────────

    def hit(self, damage: int = 1) -> bool:
        """Apply damage. Returns True if ship is now sinking."""
        self.hp -= damage
        self.smoke_intensity = min(1.0, self.smoke_intensity + 0.4)
        if self.hp <= 0:
            self.begin_sinking()
            return True
        # Alert on being hit
        self.set_state(ShipState.HUNTING if self.is_warship else ShipState.EVADING)
        return False

    def begin_sinking(self):
        self.state = ShipState.SINKING
        self.sinking_timer = random.uniform(30.0, 90.0)  # seconds to sink
        self.fire_intensity = 0.8
        self.speed = 0.0

    # ─── State transitions ────────────────────────────────────────────────────

    def set_state(self, new_state: ShipState):
        self.state = new_state
        if new_state == ShipState.ALERTED:
            self.alert_timer = 120.0
            self.speed = self.base_speed * 1.1
        elif new_state == ShipState.HUNTING:
            self.alert_timer = 300.0
            self.speed = self.base_speed
        elif new_state == ShipState.EVADING:
            self.alert_timer = 180.0
            self.speed = self.base_speed * 1.15  # run faster
            # Turn away from threat
            self.course = (self.course + 90 + random.uniform(-30, 30)) % 360

    def alert(self, sub_lon: float, sub_lat: float):
        """Called when this ship detects the submarine."""
        self.hunt_target_lon = sub_lon
        self.hunt_target_lat = sub_lat
        if self.is_warship:
            self.set_state(ShipState.HUNTING)
        else:
            self.set_state(ShipState.EVADING)

    # ─── Movement ────────────────────────────────────────────────────────────

    def _bearing_to(self, lon: float, lat: float) -> float:
        """Bearing in degrees from self to (lon, lat)."""
        dlon = lon - self.lon
        dlat = lat - self.lat
        angle = math.degrees(math.atan2(dlon, dlat)) % 360
        return angle

    def _distance_nm(self, lon: float, lat: float) -> float:
        dlon = (lon - self.lon) * math.cos(math.radians(self.lat)) * 60.0
        dlat = (lat - self.lat) * 60.0
        return math.sqrt(dlon ** 2 + dlat ** 2)

    def _steer_toward(self, lon: float, lat: float, dt: float, turn_rate: float = 3.0):
        """Gradually turn toward a target coordinate."""
        bearing = self._bearing_to(lon, lat)
        diff = (bearing - self.course + 540) % 360 - 180
        max_turn = turn_rate * dt
        self.course = (self.course + max(min(diff, max_turn), -max_turn)) % 360

    def update(self, dt: float):
        if self.state == ShipState.SUNK:
            return

        if self.state == ShipState.SINKING:
            self.sinking_timer -= dt
            self.sinking_tilt += dt * 2.0
            if self.sinking_timer <= 0:
                self.state = ShipState.SUNK
            return

        # Alert timer decay
        if self.state in (ShipState.ALERTED, ShipState.HUNTING, ShipState.EVADING):
            self.alert_timer -= dt
            if self.alert_timer <= 0:
                self.state = ShipState.PATROL
                self.speed = self.base_speed

        # DC cooldown
        if self.dc_cooldown > 0:
            self.dc_cooldown -= dt
        if self.attack_run_timer > 0:
            self.attack_run_timer -= dt
            if self.attack_run_timer <= 0:
                self.attack_run_active = False

        # Movement
        if self.state == ShipState.HUNTING and self.is_warship:
            self._steer_toward(self.hunt_target_lon, self.hunt_target_lat, dt)
        elif self.state == ShipState.PATROL and self.waypoints:
            wp = self.waypoints[self.waypoint_idx]
            if self._distance_nm(*wp) < 0.5:
                self.waypoint_idx = (self.waypoint_idx + 1) % len(self.waypoints)
            else:
                self._steer_toward(*wp, dt)

        # Advance position
        speed_deg_s = self.speed * (1.0 / 3600.0)
        rad = math.radians(self.course)
        self.lat += math.cos(rad) * speed_deg_s * dt
        self.lon += math.sin(rad) * speed_deg_s * dt / max(0.1, math.cos(math.radians(self.lat)))

        # Smoke / fire decay
        self.smoke_intensity = max(0.0, self.smoke_intensity - 0.01 * dt)
        self.fire_intensity  = max(0.0, self.fire_intensity  - 0.005 * dt)

    def start_attack_run(self, sub_lon: float, sub_lat: float):
        """Begin depth-charge attack run toward sub's last known position."""
        if self.dc_cooldown <= 0 and self.is_warship:
            self.hunt_target_lon = sub_lon
            self.hunt_target_lat = sub_lat
            self.attack_run_active = True
            self.attack_run_timer = 60.0   # run lasts 60 seconds
            dcs, _ = self.dc_patterns
            self.drops_remaining = dcs
            self.dc_cooldown = 90.0
