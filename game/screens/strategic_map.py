"""
Strategic Pacific map screen.
"""

import random
import json
import pygame

from game.state_manager import BaseScreen
from game.constants import (
    KEY_COURSE_LEFT,
    KEY_COURSE_RIGHT,
    KEY_SPEED_UP,
    KEY_SPEED_DOWN,
    KEY_TIME_ACCEL_1,
    KEY_TIME_ACCEL_2,
    KEY_TIME_ACCEL_3,
    KEY_TIME_ACCEL_4,
    KEY_PAUSE,
    KEY_ESCAPE,
)
from game.rendering.map_renderer import MapRenderer
from game.entities.convoy import Convoy
from game.save_load import default_save_path, save_game, load_game_state


class StrategicMapScreen(BaseScreen):
    def on_enter(self, manager, **kwargs):
        self.manager = manager
        self.map_renderer = MapRenderer()
        self.font = pygame.font.SysFont("consolas", 16)

        self.career = self.manager.game_state.get("career")
        self.sub = self.manager.game_state.get("submarine")

        self.paused = False
        self.time_accel = 10
        self.contact_roll_timer = 0.0
        self.selected_area_idx = 0
        self.status_message = ""
        self.status_timer = 0.0

        self.viewport = [self.sub.lon, self.sub.lat, 1.0]

        self.available_areas = self.career.available_areas(self.career.current_port)
        if not self.available_areas:
            self.available_areas = self.career.available_areas()

    def _selected_area(self):
        if not self.available_areas:
            return None
        return self.available_areas[self.selected_area_idx % len(self.available_areas)]

    def _maybe_trigger_contact(self):
        area = self._selected_area()
        if area is None:
            return

        # Contact chance rises if we're in selected patrol area vicinity.
        dist = ((self.sub.lon - area["center_lon"]) ** 2 + (self.sub.lat - area["center_lat"]) ** 2) ** 0.5
        proximity = 1.0 if dist < area["radius_deg"] * 1.4 else 0.2
        # Increased base probability 10x and add guaranteed contact after 10 min in area
        base = 0.12 * area["convoy_density"] * self.career.enemy_density_mult * proximity
        # Guaranteed contact if player has been in patrol area for 10+ minutes real-time
        if proximity >= 1.0:
            if not hasattr(self, '_area_entry_time'):
                self._area_entry_time = 0.0
            self._area_entry_time += self._last_dt if hasattr(self, '_last_dt') else 0.01
            if self._area_entry_time > 600.0:
                base = 1.0  # guarantee
        elif hasattr(self, '_area_entry_time'):
            self._area_entry_time = 0.0

        if random.random() < base:
            self.career.start_patrol(area["id"])
            template = self.career.generate_convoy(area)
            convoy = Convoy(template, area["center_lon"], area["center_lat"], course=random.uniform(0, 360))
            self.manager.game_state["combat"] = {
                "convoy": convoy,
                "torpedoes": [],
                "dc_patterns": [],
                "messages": ["Enemy convoy contact established."],
                "area": area,
                "patrol_start_date": self.career.current_date,
                "shots_fired": 0,
                "shots_hit": 0,
                "depth_charges_taken": 0,
            }
            from game.screens.mission_briefing import MissionBriefingScreen
            self.manager.switch(MissionBriefingScreen(), area=area, contact=convoy)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_COURSE_LEFT:
                self.sub.course = (self.sub.course - 5) % 360
            elif event.key == KEY_COURSE_RIGHT:
                self.sub.course = (self.sub.course + 5) % 360
            elif event.key == KEY_SPEED_UP:
                self.sub.set_speed(min(3, self.sub.speed_setting + 1))
            elif event.key == KEY_SPEED_DOWN:
                self.sub.set_speed(max(0, self.sub.speed_setting - 1))
            elif event.key == KEY_TIME_ACCEL_1:
                self.time_accel = 1
            elif event.key == KEY_TIME_ACCEL_2:
                self.time_accel = 10
            elif event.key == KEY_TIME_ACCEL_3:
                self.time_accel = 100
            elif event.key == KEY_TIME_ACCEL_4:
                self.time_accel = 1000
            elif event.key == KEY_PAUSE:
                self.paused = not self.paused
            elif event.key == pygame.K_TAB:
                if self.available_areas:
                    self.selected_area_idx = (self.selected_area_idx + 1) % len(self.available_areas)
            elif event.key == pygame.K_c:
                self._maybe_trigger_contact()
            elif event.key == pygame.K_h:
                # Show latest event if available
                events = self.career.check_events()
                if events:
                    from game.screens.historical_events import HistoricalEventScreen
                    self.manager.switch(HistoricalEventScreen(), event=events[-1], return_to=StrategicMapScreen())
            elif event.key == pygame.K_F9:
                path = default_save_path()
                save_game(path, self.career, self.sub)
                self.status_message = f"Saved campaign to {path}"
                self.status_timer = 4.0
            elif event.key == pygame.K_F10:
                path = default_save_path()
                try:
                    career, sub = load_game_state(path)
                    self.manager.game_state["career"] = career
                    self.manager.game_state["submarine"] = sub
                    self.manager.switch(StrategicMapScreen())
                    return
                except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
                    self.status_message = "Load failed. No valid save found."
                    self.status_timer = 4.0
            elif event.key == KEY_ESCAPE:
                from game.screens.main_menu import MainMenuScreen
                self.manager.switch(MainMenuScreen())

    def update(self, dt):
        self._last_dt = dt
        
        if self.paused:
            return

        # Strategic movement
        self.sub.update(dt * self.time_accel)

        # Advance campaign date
        events = self.career.advance_time(dt, self.time_accel)
        if events:
            from game.screens.historical_events import HistoricalEventScreen
            self.manager.switch(HistoricalEventScreen(), event=events[0], return_to=StrategicMapScreen())
            return

        # Contact rolls every ~2 sec real-time
        self.contact_roll_timer += dt
        if self.contact_roll_timer >= 2.0:
            self.contact_roll_timer = 0.0
            self._maybe_trigger_contact()

        # Keep map centered on player
        self.viewport[0] = self.sub.lon
        self.viewport[1] = self.sub.lat

        if self.status_timer > 0:
            self.status_timer -= dt
            if self.status_timer <= 0:
                self.status_message = ""

    def draw(self, surface):
        self.map_renderer.draw_map(surface, self.viewport)
        self.map_renderer.draw_patrol_areas(surface, self.available_areas, self.viewport, selected_area_id=(self._selected_area() or {}).get("id"))
        self.map_renderer.draw_submarine(surface, self.sub.lon, self.sub.lat, self.sub.course, self.viewport)

        area = self._selected_area()
        lines = [
            f"Date: {self.career.current_date.isoformat()}",
            f"Time Accel: {self.time_accel}x{' (PAUSED)' if self.paused else ''}",
            f"Course: {self.sub.course:.0f}°",
            f"Speed: {self.sub.speed:.1f} kts (setting {self.sub.speed_setting})",
            f"Battery: {self.sub.battery_pct*100:.0f}%  Fuel: {self.sub.fuel_pct*100:.0f}%",
            f"Area: {area['name'] if area else 'None'}",
            "",
            "Arrows: course  +/-: speed  1-4: time accel  P: pause",
            "Tab: cycle patrol area  C: force contact  H: show event",
            "F9: save campaign  F10: load campaign",
            "Esc: main menu",
        ]
        if self.status_message:
            lines.append(self.status_message)
        self.map_renderer.draw_overlay_text(surface, lines)
