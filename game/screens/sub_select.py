"""
Submarine selection screen.
"""

import pygame

from game.state_manager import BaseScreen
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, DARK_NAVY, PANEL_BG, PANEL_BORDER, PHOSPHOR_BRIGHT, AMBER_BRIGHT, LIGHT_GRAY
from game.data.submarines import SUBMARINES
from game.entities.submarine import Submarine
from game.systems.career import CareerState
from game.rendering.ship_renderer import draw_ship_side


class SubSelectScreen(BaseScreen):
    def on_enter(self, manager, **kwargs):
        self.manager = manager
        self.index = 0
        self.font_title = pygame.font.SysFont("georgia", 42, bold=True)
        self.font = pygame.font.SysFont("consolas", 20)
        self.font_small = pygame.font.SysFont("consolas", 16)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.index = (self.index - 1) % len(SUBMARINES)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.index = (self.index + 1) % len(SUBMARINES)
            elif event.key == pygame.K_RETURN:
                spec = SUBMARINES[self.index]
                career = CareerState("Commander", spec)
                sub = Submarine(spec)

                # Spawn sub at selected home port coordinates.
                port = next(p for p in career.available_ports() if p["id"] == career.current_port)
                lon = port["lon"] if port["lon"] >= 0 else 360 + port["lon"]
                sub.lon = lon
                sub.lat = port["lat"]

                self.manager.game_state["career"] = career
                self.manager.game_state["submarine"] = sub

                from game.screens.strategic_map import StrategicMapScreen
                self.manager.switch(StrategicMapScreen())
            elif event.key == pygame.K_ESCAPE:
                from game.screens.main_menu import MainMenuScreen
                self.manager.switch(MainMenuScreen())

    def draw(self, surface):
        surface.fill(DARK_NAVY)
        title = self.font_title.render("Select Submarine", True, AMBER_BRIGHT)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))

        spec = SUBMARINES[self.index]

        # Card panel
        card = pygame.Rect(140, 120, SCREEN_WIDTH - 280, SCREEN_HEIGHT - 180)
        pygame.draw.rect(surface, PANEL_BG, card)
        pygame.draw.rect(surface, PANEL_BORDER, card, 2)

        name = self.font_title.render(spec["name"], True, PHOSPHOR_BRIGHT)
        surface.blit(name, (card.x + 24, card.y + 24))

        draw_ship_side(surface, "submarine", card.x + 280, card.y + 260, scale=6.5, color=(80, 92, 110))

        lines = [
            f"Year Available: {spec['year_available']}",
            f"Max Depth: {spec['max_depth']} ft",
            f"Speed (Surface): {spec['speed_surface']} kts",
            f"Speed (Submerged): {spec['speed_submerged']} kts",
            f"Tubes: {spec['tubes_fore']} fore / {spec['tubes_aft']} aft",
            f"Torpedoes Carried: {spec['torpedo_capacity']}",
            f"Crew: {spec['crew']}",
            f"Displacement: {spec['displacement']} tons",
        ]

        x = card.x + 520
        y = card.y + 170
        for i, line in enumerate(lines):
            txt = self.font.render(line, True, LIGHT_GRAY)
            surface.blit(txt, (x, y + i * 28))

        desc = self.font_small.render(spec["description"], True, (185, 205, 220))
        surface.blit(desc, (card.x + 24, card.bottom - 70))

        hint = self.font_small.render("Left/Right: choose submarine    Enter: begin career    Esc: back", True, LIGHT_GRAY)
        surface.blit(hint, (card.x + 24, card.bottom - 32))
