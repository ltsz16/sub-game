"""
entities/convoy.py — Convoy formation manager.
"""

import math
import random
from game.entities.ship import Ship
from game.data.ships import SHIP_BY_ID


class Convoy:
    """
    Manages a group of ships traveling together.
    Merchants in columns, escorts on the flanks.
    """

    FORMATION_SPACING = 0.05  # degrees (~3 nm) between ships in formation

    def __init__(self, template: list, center_lon: float, center_lat: float,
                 course: float = None):
        if course is None:
            course = random.uniform(0, 360)
        self.course  = course
        self.speed   = 10.0
        self.lon     = center_lon
        self.lat     = center_lat
        self.ships: list[Ship] = []
        self.detected_by_player = False

        # Build ships from template
        merchants = []
        escorts   = []
        for ship_id, count in template:
            spec = SHIP_BY_ID.get(ship_id)
            if not spec:
                continue
            for i in range(count):
                ship = Ship(spec, center_lon, center_lat, course)
                if spec["category"] in ("warship", "escort"):
                    escorts.append(ship)
                else:
                    merchants.append(ship)

        # Arrange in formation
        all_ships = merchants + escorts
        self.ships = all_ships
        self._set_formation_positions()

        # Give each ship a patrol waypoint cycle roughly following the convoy
        self._assign_waypoints()

    def _set_formation_positions(self):
        """Spread ships in a rough grid around convoy center."""
        n = len(self.ships)
        cols = max(1, math.ceil(math.sqrt(n)))
        for i, ship in enumerate(self.ships):
            row = i // cols
            col = i  % cols
            # Offset perpendicular and along course
            perp_rad = math.radians(self.course + 90)
            fwd_rad  = math.radians(self.course)
            sp = self.FORMATION_SPACING
            dx = (col - cols / 2.0) * sp
            dy = (row - 0.5) * sp
            ship.lon = self.lon + dx * math.cos(perp_rad) + dy * math.cos(fwd_rad)
            ship.lat = self.lat + dx * math.sin(perp_rad) + dy * math.sin(fwd_rad)
            ship.course = self.course
            ship.speed  = self.speed

    def _assign_waypoints(self):
        """Give each ship waypoints so they patrol loosely together."""
        for ship in self.ships:
            # Two waypoints: ahead and behind, drifting slowly
            offset = random.uniform(0.3, 0.8)
            rad = math.radians(self.course)
            wp1 = (self.lon + math.sin(rad) * offset,
                   self.lat + math.cos(rad) * offset)
            wp2 = (self.lon - math.sin(rad) * offset,
                   self.lat - math.cos(rad) * offset)
            ship.waypoints = [wp1, wp2]
            ship.waypoint_idx = 0

    @property
    def alive_ships(self) -> list:
        from game.entities.ship import ShipState
        return [s for s in self.ships if s.state not in (ShipState.SUNK,)]

    @property
    def is_destroyed(self) -> bool:
        return len(self.alive_ships) == 0

    def alert_all(self, sub_lon: float, sub_lat: float):
        """Alert entire convoy to submarine presence."""
        for ship in self.alive_ships:
            ship.alert(sub_lon, sub_lat)
        self.detected_by_player = True

    def update(self, dt: float):
        # Update convoy center (weighted average of alive ship positions)
        alive = self.alive_ships
        if alive:
            self.lon = sum(s.lon for s in alive) / len(alive)
            self.lat = sum(s.lat for s in alive) / len(alive)

        for ship in self.ships:
            ship.update(dt)

    def total_tonnage(self) -> int:
        from game.entities.ship import ShipState
        return sum(s.tonnage for s in self.ships if s.state == ShipState.SUNK)

    def score(self) -> float:
        from game.entities.ship import ShipState
        return sum(s.score_value * s.tonnage / 1000.0
                   for s in self.ships if s.state == ShipState.SUNK)
