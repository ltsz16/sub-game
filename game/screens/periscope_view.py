"""
Periscope combat view.
"""

import math
import pygame

from game.state_manager import BaseScreen
from game.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SKY_MID,
    OCEAN_SURFACE,
    PHOSPHOR_BRIGHT,
    AMBER_BRIGHT,
    LIGHT_GRAY,
    KEY_VIEW_CHART,
    KEY_VIEW_PERISCOPE,
    KEY_VIEW_BRIDGE,
    KEY_VIEW_DAMAGE,
    KEY_VIEW_TORPEDO,
    KEY_FIRE_TORPEDO,
)
from game.rendering.hud import draw_horizon
from game.rendering.sprites import draw_ship_side_sprite
from game.entities.torpedo import Torpedo
from game.screens.combat_shared import update_combat_tick, cycle_to_view


class PeriscopeViewScreen(BaseScreen):
    def on_enter(self, manager, **kwargs):
        self.manager = manager
        self.font = pygame.font.SysFont("consolas", 16)

    def _bearing_and_range(self, sub, ship):
        dlon = (ship.lon - sub.lon) * math.cos(math.radians(sub.lat)) * 60.0
        dlat = (ship.lat - sub.lat) * 60.0
        rng = math.sqrt(dlon ** 2 + dlat ** 2)
        brg = math.degrees(math.atan2(dlon, dlat)) % 360
        return brg, rng

    def handle_event(self, event):
        sub = self.manager.game_state.get("submarine")
        combat = self.manager.game_state.get("combat")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                sub.course = (sub.course - 2) % 360
            elif event.key == pygame.K_RIGHT:
                sub.course = (sub.course + 2) % 360
            elif event.key == KEY_FIRE_TORPEDO:
                if sub.fire_fore():
                    torp = Torpedo(sub.lon, sub.lat, sub.course, depth=sub.torp_depth, high_speed=sub.torp_speed_high, fuse=sub.torp_fuse)
                    combat["torpedoes"].append(torp)
                    combat["shots_fired"] += 1
                    combat["messages"].append("Periscope shot fired.")
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
        update_combat_tick(self.manager, dt)

        state = self.manager.game_state.get("combat")
        if state and state["convoy"].is_destroyed:
            from game.screens.patrol_report import PatrolReportScreen
            self.manager.switch(PatrolReportScreen())

    def draw(self, surface):
        sub = self.manager.game_state.get("submarine")
        state = self.manager.game_state.get("combat")
        convoy = state["convoy"]

        draw_horizon(surface, SKY_MID, OCEAN_SURFACE, SCREEN_HEIGHT // 2)

        # Periscope circular mask look
        center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        radius = 330
        mask = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        mask.fill((0, 0, 0, 230))
        pygame.draw.circle(mask, (0, 0, 0, 0), center, radius)
        surface.blit(mask, (0, 0))

        # Crosshair
        pygame.draw.line(surface, PHOSPHOR_BRIGHT, (center[0] - radius, center[1]), (center[0] + radius, center[1]), 1)
        pygame.draw.line(surface, PHOSPHOR_BRIGHT, (center[0], center[1] - radius), (center[0], center[1] + radius), 1)

        # Ships in field of view if near current bearing
        for ship in convoy.alive_ships:
            brg, rng = self._bearing_and_range(sub, ship)
            rel = ((brg - sub.course + 540) % 360) - 180
            if abs(rel) <= 42:  # approx field of view
                x = int(center[0] + (rel / 42.0) * (radius - 40))
                y = SCREEN_HEIGHT // 2 + 30
                # Increased scale for better visibility
                scale = max(3.5, 18.0 - rng * 1.2)
                color = (240, 200, 160) if ship.is_warship else (190, 190, 190)
                draw_ship_side_sprite(surface, ship.ship_id, x, y, scale=scale, color=color)
                # Ship label below image
                txt = self.font.render(f"{ship.name} {rng:.1f}nm BRG {brg:03.0f}", True, LIGHT_GRAY)
                surface.blit(txt, (x - txt.get_width() // 2, y + 60))

        # HUD text
        hud = [
            f"PERISCOPE VIEW",
            f"Depth: {sub.depth:.0f} ft",
            f"Course: {sub.course:.0f}°",
            f"Speed: {sub.speed:.1f} kts",
            f"Torpedoes: {sub.torpedo_count}",
        ]
        for i, line in enumerate(hud):
            t = self.font.render(line, True, AMBER_BRIGHT if i == 0 else PHOSPHOR_BRIGHT)
            surface.blit(t, (18, 18 + i * 20))

        hint = self.font.render("Space Fire  F1 Chart  F2 Periscope  F3 Bridge  F4 Damage  F5 Torpedo", True, PHOSPHOR_BRIGHT)
        surface.blit(hint, (18, SCREEN_HEIGHT - 26))
