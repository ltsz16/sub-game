"""
Bridge surface view.
"""

import math
import pygame

from game.state_manager import BaseScreen
from game.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SKY_HORIZON,
    OCEAN_BRIGHT,
    PHOSPHOR_BRIGHT,
    AMBER_BRIGHT,
    LIGHT_GRAY,
    KEY_VIEW_CHART,
    KEY_VIEW_PERISCOPE,
    KEY_VIEW_BRIDGE,
    KEY_VIEW_DAMAGE,
    KEY_VIEW_TORPEDO,
)
from game.rendering.hud import draw_horizon
from game.rendering.ship_renderer import draw_ship_side
from game.screens.combat_shared import update_combat_tick, cycle_to_view


class BridgeViewScreen(BaseScreen):
    def on_enter(self, manager, **kwargs):
        self.manager = manager
        self.font = pygame.font.SysFont("consolas", 16)

    def _bearing_range(self, sub, ship):
        dlon = (ship.lon - sub.lon) * math.cos(math.radians(sub.lat)) * 60.0
        dlat = (ship.lat - sub.lat) * 60.0
        rng = math.sqrt(dlon ** 2 + dlat ** 2)
        brg = math.degrees(math.atan2(dlon, dlat)) % 360
        return brg, rng

    def handle_event(self, event):
        sub = self.manager.game_state.get("submarine")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                sub.course = (sub.course - 3) % 360
            elif event.key == pygame.K_RIGHT:
                sub.course = (sub.course + 3) % 360
            elif event.key == pygame.K_UP:
                sub.set_speed(min(3, sub.speed_setting + 1))
            elif event.key == pygame.K_DOWN:
                sub.set_speed(max(0, sub.speed_setting - 1))
            elif event.key == KEY_VIEW_CHART:
                cycle_to_view(self.manager, "chart")
            elif event.key == KEY_VIEW_PERISCOPE:
                cycle_to_view(self.manager, "periscope")
            elif event.key == KEY_VIEW_BRIDGE:
                cycle_to_view(self.manager, "bridge")
            elif event.key == KEY_VIEW_DAMAGE:
                cycle_to_view(self.manager, "damage")
            elif event.key == KEY_VIEW_TORPEDO:
                cycle_to_view(self.manager, "torpedo")

    def update(self, dt):
        # Bridge implies surfaced.
        sub = self.manager.game_state.get("submarine")
        sub.target_depth = 0
        update_combat_tick(self.manager, dt)

        state = self.manager.game_state.get("combat")
        if state and state["convoy"].is_destroyed:
            from game.screens.patrol_report import PatrolReportScreen
            self.manager.switch(PatrolReportScreen())

    def draw(self, surface):
        sub = self.manager.game_state.get("submarine")
        state = self.manager.game_state.get("combat")
        convoy = state["convoy"]

        draw_horizon(surface, SKY_HORIZON, OCEAN_BRIGHT, SCREEN_HEIGHT // 2)

        # Wave bands
        for i in range(10):
            y = SCREEN_HEIGHT // 2 + 30 + i * 18
            col = (30, 100 + i * 8, 155 + i * 5)
            pygame.draw.line(surface, col, (0, y), (SCREEN_WIDTH, y), 1)

        # Horizon contacts
        for ship in convoy.alive_ships:
            brg, rng = self._bearing_range(sub, ship)
            rel = ((brg - sub.course + 540) % 360) - 180
            if abs(rel) <= 60:
                x = int(SCREEN_WIDTH // 2 + rel * 7)
                y = SCREEN_HEIGHT // 2 + 18
                scale = max(1.8, 10.0 - rng * 0.8)
                color = (220, 200, 170) if ship.is_warship else (170, 170, 170)
                draw_ship_side(surface, ship.ship_id, x, y, scale=scale, color=color)

        hdr = [
            "BRIDGE VIEW",
            f"Course {sub.course:.0f}°",
            f"Speed {sub.speed:.1f} kts",
            f"Depth {sub.depth:.0f} ft (surfacing)",
            f"Enemy ships: {len(convoy.alive_ships)}",
        ]
        for i, line in enumerate(hdr):
            t = self.font.render(line, True, AMBER_BRIGHT if i == 0 else PHOSPHOR_BRIGHT)
            surface.blit(t, (18, 18 + i * 20))

        hint = self.font.render("F1 Chart  F2 Periscope  F4 Damage  F5 Torpedo Room", True, LIGHT_GRAY)
        surface.blit(hint, (18, SCREEN_HEIGHT - 26))
