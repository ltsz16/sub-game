"""
screens/damage_control_detail.py - Enhanced graphical damage control view.

Inspired by Silent Service II compartment schematic display.
"""

import pygame
from game.state_manager import BaseScreen
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, COMPARTMENTS, KEY_VIEW_DAMAGE
from game.rendering.damage_control_ui import (
    draw_compartment_status,
    draw_damage_summary,
    draw_critical_systems_status,
    draw_repair_status,
)
from game.screens.combat_shared import update_combat_tick


class DamageControlDetailScreen(BaseScreen):
    def on_enter(self, manager, **kwargs):
        self.manager = manager
        self.font = pygame.font.SysFont("consolas", 14)
        self.font_small = pygame.font.SysFont("consolas", 11)

    def handle_event(self, event):
        sub = self.manager.game_state.get("submarine")
        if event.type == pygame.KEYDOWN:
            # Repair assignment with number keys
            if pygame.K_0 <= event.key <= pygame.K_9:
                key_num = event.key - pygame.K_0
                if key_num < len(COMPARTMENTS):
                    comp_name = COMPARTMENTS[key_num]
                    if sub.repair_assignment == comp_name:
                        sub.repair_assignment = None
                    else:
                        sub.repair_assignment = comp_name
            
            # Navigation
            elif event.key == pygame.K_F1:
                from game.screens.nav_chart import NavChartScreen
                self.manager.switch(NavChartScreen())
            elif event.key == pygame.K_F2:
                from game.screens.periscope_view import PeriscopeViewScreen
                self.manager.switch(PeriscopeViewScreen())
            elif event.key == pygame.K_F3:
                from game.screens.bridge_view import BridgeViewScreen
                self.manager.switch(BridgeViewScreen())
            elif event.key == pygame.K_F4:
                pass  # Already here
            elif event.key == pygame.K_F5:
                from game.screens.torpedo_room import TorpedoRoomScreen
                self.manager.switch(TorpedoRoomScreen())
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
        surface.fill((10, 15, 20))
        
        sub = self.manager.game_state.get("submarine")
        
        # Draw compartment schematic
        draw_compartment_status(surface, [], sub, x_offset=10, y_offset=10)
        
        # Draw status panels on the right side
        right_x = SCREEN_WIDTH - 270
        
        # Damage summary
        draw_damage_summary(surface, sub, right_x, 10, width=250, height=110)
        
        # Critical systems
        draw_critical_systems_status(surface, sub, right_x, 125, width=250, height=100)
        
        # Repair status
        draw_repair_status(surface, sub, right_x, 230, width=250, height=80)
        
        # Instructions
        instructions = [
            "0-9: Assign repair to compartment (press same # to cancel)",
            "F1-F5: Switch views",
            "Esc: Return to map"
        ]
        
        for i, instr in enumerate(instructions):
            t = self.font_small.render(instr, True, (100, 100, 100))
            surface.blit(t, (10, SCREEN_HEIGHT - 65 + i * 18))
