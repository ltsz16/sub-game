"""
Historical event popup screen.
"""

import pygame

from game.state_manager import BaseScreen
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, DARK_NAVY, PANEL_BG, PANEL_BORDER, PHOSPHOR_BRIGHT, AMBER_BRIGHT, LIGHT_GRAY


class HistoricalEventScreen(BaseScreen):
    def on_enter(self, manager, **kwargs):
        self.manager = manager
        self.event = kwargs.get("event", {})
        self.return_to = kwargs.get("return_to")
        self.font_head = pygame.font.SysFont("georgia", 40, bold=True)
        self.font_body = pygame.font.SysFont("consolas", 20)
        self.font_hint = pygame.font.SysFont("consolas", 16)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
            if self.return_to is not None:
                self.manager.switch(self.return_to)
            else:
                self.manager.pop()

    def _wrap(self, text, width_chars=78):
        words = text.split()
        lines = []
        line = []
        for w in words:
            line.append(w)
            if len(" ".join(line)) >= width_chars:
                lines.append(" ".join(line))
                line = []
        if line:
            lines.append(" ".join(line))
        return lines

    def draw(self, surface):
        surface.fill(DARK_NAVY)
        panel = pygame.Rect(90, 70, SCREEN_WIDTH - 180, SCREEN_HEIGHT - 140)
        pygame.draw.rect(surface, PANEL_BG, panel)
        pygame.draw.rect(surface, PANEL_BORDER, panel, 2)

        title = self.font_head.render(self.event.get("title", "Historical Event"), True, AMBER_BRIGHT)
        surface.blit(title, (panel.x + 24, panel.y + 24))

        date_tuple = self.event.get("date")
        date_str = ""
        if date_tuple:
            date_str = f"{date_tuple[0]:04d}-{date_tuple[1]:02d}-{date_tuple[2]:02d}"
        date_txt = self.font_body.render(date_str, True, PHOSPHOR_BRIGHT)
        surface.blit(date_txt, (panel.x + 24, panel.y + 78))

        lines = self._wrap(self.event.get("body", ""), 84)
        y = panel.y + 130
        for line in lines[:18]:
            txt = self.font_body.render(line, True, LIGHT_GRAY)
            surface.blit(txt, (panel.x + 24, y))
            y += 28

        hint = self.font_hint.render("Press Enter to continue", True, PHOSPHOR_BRIGHT)
        surface.blit(hint, (panel.x + 24, panel.bottom - 32))
