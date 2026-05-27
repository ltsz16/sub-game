"""
Tactical chart room view (combat overhead).
"""

import math
import pygame

from game.state_manager import BaseScreen
from game.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    DARK_NAVY,
    PHOSPHOR_BRIGHT,
    PHOSPHOR_DIM,
    AMBER_BRIGHT,
    LIGHT_GRAY,
    KEY_COURSE_LEFT,
    KEY_COURSE_RIGHT,
    KEY_SPEED_UP,
    KEY_SPEED_DOWN,
    KEY_FIRE_TORPEDO,
    KEY_VIEW_CHART,
    KEY_VIEW_PERISCOPE,
    KEY_VIEW_BRIDGE,
    KEY_VIEW_DAMAGE,
    KEY_VIEW_TORPEDO,
    KEY_DIVE,
    KEY_SURFACE,
    KEY_SILENT_RUN,
    KEY_DEPTH_PERISCOPE,
    KEY_DEPTH_SHALLOW,
    KEY_DEPTH_CRUSH,
    DEPTH_SHALLOW,
)
from game.rendering.ship_renderer import draw_ship_top
from game.rendering.sprites import draw_ship_top_sprite
from game.rendering.hud import HUD
from game.rendering.effects import ExplosionEffect
from game.entities.torpedo import Torpedo
from game.screens.combat_shared import update_combat_tick, cycle_to_view


class NavChartScreen(BaseScreen):
    def on_enter(self, manager, **kwargs):
        self.manager = manager
        self.hud = HUD()
        self.font = pygame.font.SysFont("consolas", 16)
        self.effects = []

    def _world_to_chart(self, sub_lon, sub_lat, lon, lat):
        # 20nm radius tactical chart mapped to screen center area
        dlon_nm = (lon - sub_lon) * math.cos(math.radians(sub_lat)) * 60.0
        dlat_nm = (lat - sub_lat) * 60.0
        scale = 14  # px per nm
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        x = int(cx + dlon_nm * scale)
        y = int(cy - dlat_nm * scale)
        return x, y

    def handle_event(self, event):
        sub = self.manager.game_state.get("submarine")
        combat = self.manager.game_state.get("combat")
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_COURSE_LEFT:
                sub.course = (sub.course - 5) % 360
            elif event.key == KEY_COURSE_RIGHT:
                sub.course = (sub.course + 5) % 360
            elif event.key == KEY_SPEED_UP:
                sub.set_speed(min(3, sub.speed_setting + 1))
            elif event.key == KEY_SPEED_DOWN:
                sub.set_speed(max(0, sub.speed_setting - 1))
            elif event.key == KEY_DIVE:
                sub.target_depth = min(sub.spec["max_depth"], sub.target_depth + 50)
            elif event.key == KEY_SURFACE:
                sub.target_depth = 0
            elif event.key == KEY_SILENT_RUN:
                sub.silent_running = not sub.silent_running
            elif event.key == KEY_DEPTH_PERISCOPE:
                # From chart, go to periscope depth
                from game.constants import DEPTH_PERISCOPE
                sub.target_depth = DEPTH_PERISCOPE
            elif event.key == KEY_DEPTH_SHALLOW:
                sub.target_depth = DEPTH_SHALLOW
            elif event.key == KEY_DEPTH_CRUSH:
                sub.target_depth = sub.spec["max_depth"]
            elif event.key == KEY_FIRE_TORPEDO:
                if sub.fire_fore():
                    torp = Torpedo(sub.lon, sub.lat, sub.course, depth=sub.torp_depth, high_speed=sub.torp_speed_high, fuse=sub.torp_fuse)
                    combat["torpedoes"].append(torp)
                    combat["shots_fired"] += 1
                    combat["messages"].append("Fore tube fired.")
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
            elif event.key == pygame.K_ESCAPE:
                from game.screens.strategic_map import StrategicMapScreen
                self.manager.switch(StrategicMapScreen())

    def update(self, dt):
        update_combat_tick(self.manager, dt)

        # End combat if convoy destroyed
        state = self.manager.game_state.get("combat")
        if state and state["convoy"].is_destroyed:
            from game.screens.patrol_report import PatrolReportScreen
            self.manager.switch(PatrolReportScreen())
            return

        for fx in self.effects:
            fx.update(dt)
        self.effects = [fx for fx in self.effects if fx.alive]

    def draw(self, surface):
        surface.fill(DARK_NAVY)

        sub = self.manager.game_state.get("submarine")
        state = self.manager.game_state.get("combat")
        convoy = state["convoy"]

        # Chart rings (nm)
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        for nm in (5, 10, 15, 20):
            pygame.draw.circle(surface, PHOSPHOR_DIM, (cx, cy), nm * 14, 1)

        # Draw sub using sprite
        draw_ship_top_sprite(surface, "submarine", cx, cy, scale=1.1, color=(140, 220, 180), course_deg=sub.course)

        # Draw convoy ships
        for ship in convoy.alive_ships:
            sx, sy = self._world_to_chart(sub.lon, sub.lat, ship.lon, ship.lat)
            color = (240, 180, 80) if ship.is_warship else (180, 180, 180)
            # Draw ship using sprite
            draw_ship_top_sprite(surface, ship.ship_id, sx, sy, scale=1.0, color=color, course_deg=ship.course)

        # Torpedo tracks
        for torp in state["torpedoes"]:
            tx, ty = self._world_to_chart(sub.lon, sub.lat, torp.lon, torp.lat)
            pygame.draw.circle(surface, AMBER_BRIGHT, (tx, ty), 2)

        for fx in self.effects:
            fx.draw(surface)

        # Side status panel
        panel = pygame.Rect(18, 16, 330, 220)
        self.hud.draw_panel(surface, panel, "Chart Room")
        status = [
            f"Depth: {sub.depth:.0f} ft",
            f"Speed: {sub.speed:.1f} kts",
            f"Course: {sub.course:.0f}°",
            f"Torpedoes: {sub.torpedo_count}",
            f"Convoy Ships Remaining: {len(state['convoy'].alive_ships)}",
            f"Shots: {state['shots_fired']}  Hits: {state['shots_hit']}",
        ]
        self.hud.draw_status_lines(surface, panel.x + 10, panel.y + 34, status)

        log_panel = pygame.Rect(18, 250, 430, 180)
        self.hud.draw_panel(surface, log_panel, "Combat Log")
        y = log_panel.y + 34
        for line in state["messages"][-8:]:
            txt = self.font.render(line, True, LIGHT_GRAY)
            surface.blit(txt, (log_panel.x + 10, y))
            y += 20

        hint = self.font.render("F1 Chart  F2 Periscope  F3 Bridge  F4 Damage  F5 Torpedo", True, PHOSPHOR_DIM)
        surface.blit(hint, (18, SCREEN_HEIGHT - 28))
