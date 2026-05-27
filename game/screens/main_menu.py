"""
Main menu screen.
"""

import os
import json
import pygame

from game.state_manager import BaseScreen
from game.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    TITLE,
    DARK_NAVY,
    OCEAN_MID,
    PHOSPHOR_BRIGHT,
    AMBER_BRIGHT,
    LIGHT_GRAY,
)
from game.rendering.ship_renderer import draw_ship_side
from game.save_load import default_save_path, load_game_state


class MainMenuScreen(BaseScreen):
    def on_enter(self, manager, **kwargs):
        self.manager = manager
        self.font_title = pygame.font.SysFont("georgia", 58, bold=True)
        self.font_menu = pygame.font.SysFont("consolas", 28)
        self.font_help = pygame.font.SysFont("consolas", 18)
        self.save_path = default_save_path()
        self.options = ["Start Career"]
        if os.path.exists(self.save_path):
            self.options.append("Continue Career")
        self.options.append("Quit")
        self.selection = 0
        self.anim_x = -200
        self.message = ""

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selection = (self.selection - 1) % len(self.options)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selection = (self.selection + 1) % len(self.options)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                chosen = self.options[self.selection]
                if chosen == "Start Career":
                    from game.screens.sub_select import SubSelectScreen
                    self.manager.switch(SubSelectScreen())
                elif chosen == "Continue Career":
                    try:
                        career, sub = load_game_state(self.save_path)
                        self.manager.game_state["career"] = career
                        self.manager.game_state["submarine"] = sub
                        from game.screens.strategic_map import StrategicMapScreen
                        self.manager.switch(StrategicMapScreen())
                    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
                        self.message = "Could not load save. Start a new career instead."
                else:
                    self.manager.quit()
            elif event.key == pygame.K_ESCAPE:
                self.manager.quit()

    def update(self, dt):
        self.anim_x += 60 * dt
        if self.anim_x > SCREEN_WIDTH + 200:
            self.anim_x = -200

    def draw(self, surface):
        surface.fill(DARK_NAVY)
        pygame.draw.rect(surface, OCEAN_MID, (0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2))

        title = self.font_title.render(TITLE, True, AMBER_BRIGHT)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 90))

        subtitle = self.font_help.render("WWII Pacific Submarine Campaign", True, LIGHT_GRAY)
        surface.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 160))

        for i, opt in enumerate(self.options):
            color = PHOSPHOR_BRIGHT if i == self.selection else LIGHT_GRAY
            text = self.font_menu.render(opt, True, color)
            surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 280 + i * 48))

        draw_ship_side(surface, "submarine", int(self.anim_x), SCREEN_HEIGHT - 90, scale=3.2, color=(35, 45, 60))

        help1 = self.font_help.render("Arrow keys: select", True, LIGHT_GRAY)
        help2 = self.font_help.render("Enter: confirm", True, LIGHT_GRAY)
        surface.blit(help1, (20, SCREEN_HEIGHT - 52))
        surface.blit(help2, (20, SCREEN_HEIGHT - 30))

        if self.message:
            msg = self.font_help.render(self.message, True, AMBER_BRIGHT)
            surface.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, SCREEN_HEIGHT - 34))
