"""
systems/career.py — Career state and patrol management.
"""

import datetime
import random
import math
from game.data.historical_events import EVENTS
from game.data.patrol_areas import PATROL_AREAS, PORTS, AREA_BY_ID, PORT_BY_ID
from game.data.ships import CONVOY_TEMPLATES


class PatrolResult:
    """Summary of a completed patrol."""
    def __init__(self):
        self.patrol_number: int = 0
        self.start_date: datetime.date = None
        self.end_date:   datetime.date = None
        self.area_name:  str = ""
        self.base_name:  str = ""
        self.ships_sunk: list = []       # list of dicts {name, tonnage, score_value, ship_id}
        self.total_tonnage: int = 0
        self.total_score:   float = 0.0
        self.torpedoes_fired: int = 0
        self.torpedoes_hit:   int = 0
        self.depth_charges_taken: int = 0
        self.crew_lost: int = 0
        self.sub_survived: bool = True
        self.medals_awarded: list = []
        self.promoted_to: str | None = None


class CareerState:
    """Complete career state."""

    GAME_START = datetime.date(1941, 12, 7)
    GAME_END   = datetime.date(1945, 8, 15)
    # Seconds of real time per game day in strategic map (at 1× speed)
    SECS_PER_GAME_DAY = 20.0

    def __init__(self, commander_name: str, sub_spec: dict):
        self.commander_name  = commander_name
        self.sub_spec        = sub_spec
        self.rank_index      = 2         # 0=Ensign…6=Rear Admiral; start as Lieutenant
        self.patrol_number   = 0
        self.current_date    = datetime.date(1941, 12, 7)

        # Home port / patrol area
        self.current_port    = "pearl_harbor"
        self.patrol_area     = None     # id of current patrol zone

        # Open ports and areas (updated by historical events)
        self.open_ports = {p["id"] for p in PORTS if p["available"]}
        self.open_areas = set()
        self._apply_initial_events()

        # Career totals
        self.total_tonnage_sunk: int  = 0
        self.total_ships_sunk:   int  = 0
        self.kills_by_type: dict      = {}   # ship_id → count
        self.total_score:    float    = 0.0
        self.medals:         list     = []   # list of medal name strings
        self.patrols:        list     = []   # list of PatrolResult

        # Events already triggered
        self.triggered_events: set = set()

        # Enemy density multiplier (modified by events)
        self.enemy_density_mult:  float = 1.0
        self.enemy_warship_mult:  float = 1.0

        # In-game time tracking
        self._time_accumulator: float = 0.0

    # ─── Events ───────────────────────────────────────────────────────────────

    def _apply_initial_events(self):
        """Open areas that are available from the start."""
        self.open_areas = {
            "luzon_strait", "south_china_sea", "formosa",
            "empire_waters", "marianas", "palau",
        }

    def check_events(self) -> list:
        """Return list of newly triggered events for the current date."""
        triggered = []
        for i, event in enumerate(EVENTS):
            if i in self.triggered_events:
                continue
            ev_date = datetime.date(*event["date"])
            if self.current_date >= ev_date:
                self.triggered_events.add(i)
                self._apply_event(event)
                triggered.append(event)
        return triggered

    def _apply_event(self, event: dict):
        impact = event["impact"]
        for area_id in impact.get("patrol_areas_opened", []):
            self.open_areas.add(area_id)
        for area_id in impact.get("patrol_areas_blocked", []):
            self.open_areas.discard(area_id)
        for port_id, action in impact.get("base_changes", {}).items():
            if action == "open":
                self.open_ports.add(port_id)
            else:
                self.open_ports.discard(port_id)
        self.enemy_density_mult  = impact.get("enemy_density_mult",  self.enemy_density_mult)
        self.enemy_warship_mult  = impact.get("enemy_warship_mult",  self.enemy_warship_mult)

    # ─── Time ─────────────────────────────────────────────────────────────────

    def advance_time(self, real_seconds: float, accel: int) -> list:
        """
        Advance game time. Returns list of triggered historical events.
        accel: 1, 10, 100, or 1000
        """
        game_seconds = real_seconds * accel
        self._time_accumulator += game_seconds
        new_events = []
        while self._time_accumulator >= self.SECS_PER_GAME_DAY:
            self._time_accumulator -= self.SECS_PER_GAME_DAY
            self.current_date += datetime.timedelta(days=1)
            new_events.extend(self.check_events())
            if self.current_date >= self.GAME_END:
                break
        return new_events

    @property
    def is_war_over(self) -> bool:
        return self.current_date >= self.GAME_END

    # ─── Patrol management ────────────────────────────────────────────────────

    def start_patrol(self, area_id: str):
        self.patrol_area  = area_id
        self.patrol_number += 1

    def end_patrol(self, result: PatrolResult):
        result.patrol_number = self.patrol_number
        result.end_date      = self.current_date

        # Update career totals
        self.total_tonnage_sunk += result.total_tonnage
        self.total_ships_sunk   += len(result.ships_sunk)
        self.total_score        += result.total_score
        for s in result.ships_sunk:
            sid = s.get("ship_id", "unknown")
            self.kills_by_type[sid] = self.kills_by_type.get(sid, 0) + 1

        self.patrols.append(result)
        self.patrol_area = None

    # ─── Available options ────────────────────────────────────────────────────

    def available_ports(self) -> list:
        return [p for p in PORTS if p["id"] in self.open_ports]

    def available_areas(self, port_id: str = None) -> list:
        pid = port_id or self.current_port
        return [
            a for a in PATROL_AREAS
            if a["id"] in self.open_areas
            and (pid in a.get("accessible_from", []) or not a.get("accessible_from"))
        ]

    # ─── Convoy generation ────────────────────────────────────────────────────

    def generate_convoy(self, area: dict):
        """Return a random convoy template appropriate for the area and time."""
        import random
        density = area["convoy_density"] * self.enemy_density_mult
        warship_prob = area["warship_density"] * self.enemy_warship_mult

        templates = list(CONVOY_TEMPLATES)
        # Weight toward warship templates if warship_prob is high
        if warship_prob < 0.3:
            templates = templates[:5]   # merchant-heavy templates only
        elif warship_prob > 0.6:
            templates = templates        # all templates

        return random.choice(templates)

    # ─── Torpedo type by year ─────────────────────────────────────────────────

    def torpedo_type_for_year(self) -> str:
        year = self.current_date.year
        if year >= 1943:
            return "mk18"   # Electric, no wake, reliable
        elif year >= 1942:
            return "mk14"   # Steam, wake visible, magnetic dud issues
        return "mk10"       # Oldest type, most reliable but shortest range
