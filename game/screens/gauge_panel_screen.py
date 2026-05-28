"""
screens/gauge_panel_screen.py - Dedicated comprehensive gauge display.

All instruments on one screen like Silent Service II.
"""

import pygame
from game.state_manager import BaseScreen
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game.rendering.gauge_panel import (
    draw_main_gauge_panel,
    draw_secondary_instruments,
    draw_compass_rose,
    draw_depth_indicator,
    draw_rudder_indicator,
)
from game.screens.combat_shared import update_combat_tick


class GaugePanelScreen(BaseScreen):
    def on_enter(self, manager, **kwargs):
        self.manager = manager
        self.font = pygame.font.SysFont("consolas", 14)
        self.font_small = pygame.font.SysFont("consolas", 10)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                from game.screens.nav_chart import NavChartScreen
                self.manager.switch(NavChartScreen())
            elif event.key == pygame.K_F2:
                from game.screens.periscope_view import PeriscopeViewScreen
                self.manager.switch(PeriscopeViewScreen())
            elif event.key == pygame.K_F3:
                from game.screens.bridge_view import BridgeViewScreen
                self.manager.switch(BridgeViewScreen())
            elif event.key == pygame.K_F4:
                from game.screens.damage_control_detail import DamageControlDetailScreen
                self.manager.switch(DamageControlDetailScreen())
            elif event.key == pygame.K_F5:
                from game.screens.torpedo_room import TorpedoRoomScreen
                self.manager.switch(TorpedoRoomScreen())
            elif event.key == pygame.K_g:  # G for Gauges (alternate)
                pass  # Already here
            elif event.key == pygame.K_ESCAPE:
                from game.screens.strategic_map import StrategicMapScreen
                self.manager.switch(StrategicMapScreen())

    def update(self, dt):
        update_combat_tick(self.manager, dt)
        
        state = self.manager.game_state.get("combat")
        if state and state["convoy"].is_destroyed:
            from game.screens.patrol_report import PatrolReportScreen
            self.manager.switch(PatrolReportScreen())

    def draw(self, surface):
        surface.fill((15, 15, 25))
        
        sub = self.manager.game_state.get("submarine")
        
        # Title
        title_font = pygame.font.SysFont("consolas", 16, bold=True)
        title = title_font.render("INSTRUMENT PANEL", True, (200, 200, 100))
        surface.blit(title, (15, 10))
        
        # Main gauge cluster (2x2)
        draw_main_gauge_panel(surface, sub, x=20, y=40, panel_width=420, panel_height=280)
        
        # Secondary instruments (right side)
        draw_secondary_instruments(surface, sub, x=450, y=40, width=320, height=155)
        
        # Compass rose (large, bottom right)
        draw_compass_rose(surface, sub, x=670, y=230, size=100)
        
        # Left side detail displays
        # Large depth indicator
        draw_depth_indicator(surface, sub, x=20, y=330, width=200, height=80)
        
        # Rudder indicator
        draw_rudder_indicator(surface, sub, x=230, y=330, width=180, height=50)
        
        # Status text
        status_y = 370
        status_font = pygame.font.SysFont("consolas", 10)
        
        status_lines = [
            f"Position: {sub.lat:.4f}° N, {sub.lon:.4f}° E",
            f"Hull Integrity: {sub.hull_integrity * 100:.1f}%",
            f"Status: {'SURFACED' if sub.surfaced else 'SUBMERGED'}",
            f"Silent Running: {'ON' if sub.silent_running else 'OFF'}",
        ]
        
        for i, line in enumerate(status_lines):
            t = status_font.render(line, True, (100, 180, 100))
            surface.blit(t, (450, status_y + i * 16))
        
        # Bottom instructions
        instructions = "F1-F5: Switch views | G: Gauges | Esc: Map"
        t = self.font_small.render(instructions, True, (100, 100, 100))
        surface.blit(t, (15, SCREEN_HEIGHT - 20))
