"""
Mission briefing screen before combat.
"""

import pygame

from game.state_manager import BaseScreen
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, DARK_NAVY, PANEL_BG, PANEL_BORDER, AMBER_BRIGHT, PHOSPHOR_BRIGHT, LIGHT_GRAY


class MissionBriefingScreen(BaseScreen):
    def on_enter(self, manager, **kwargs):
        self.manager = manager
        self.area = kwargs.get("area")
        self.contact = kwargs.get("contact")
        self.font_head = pygame.font.SysFont("georgia", 42, bold=True)
        self.font = pygame.font.SysFont("consolas", 20)
        self.font_small = pygame.font.SysFont("consolas", 16)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                from game.screens.nav_chart import NavChartScreen
                self.manager.switch(NavChartScreen())
            elif event.key == pygame.K_e:
                from game.screens.strategic_map import StrategicMapScreen
                self.manager.switch(StrategicMapScreen())
            elif event.key == pygame.K_ESCAPE:
                from game.screens.strategic_map import StrategicMapScreen
                self.manager.switch(StrategicMapScreen())

    def draw(self, surface):
        surface.fill(DARK_NAVY)
        panel = pygame.Rect(100, 90, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 180)
        pygame.draw.rect(surface, PANEL_BG, panel)
        pygame.draw.rect(surface, PANEL_BORDER, panel, 2)

        title = self.font_head.render("XO Briefing", True, AMBER_BRIGHT)
        surface.blit(title, (panel.x + 24, panel.y + 24))

        area_name = self.area["name"] if self.area else "Unknown Area"
        lines = [
            f"Patrol Area: {area_name}",
            "",
            "Contact Report:",
            "- Enemy convoy detected in assigned patrol zone.",
            "- Estimated composition: merchant traffic with possible escorts.",
            "- Visibility: fair. Sea state: moderate.",
            "",
            "Executive Officer Estimate:",
            "- Enemy visual detection range (surfaced): 6-8 nm.",
            "- Enemy sonar effectiveness increases with your speed.",
            "- Recommend submerged approach to periscope depth before attack.",
            "",
            "Tactical Recommendation:",
            "- Attack from beam angle, 90° AoB where possible.",
            "- Fire spread of 2-4 torpedoes against high-value targets.",
            "- Dive deep and deploy decoy when escorts counter-attack.",
        ]

        y = panel.y + 100
        for line in lines:
            color = PHOSPHOR_BRIGHT if line.endswith(":") else LIGHT_GRAY
            txt = self.font.render(line, True, color)
            surface.blit(txt, (panel.x + 24, y))
            y += 26

        hint = self.font_small.render("A: Attack now    E: Evade and continue patrol    Esc: return", True, PHOSPHOR_BRIGHT)
        surface.blit(hint, (panel.x + 24, panel.bottom - 30))
