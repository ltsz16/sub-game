"""
rendering/hud.py — Shared HUD widgets for multiple screens.
"""

import math
import pygame

from game.constants import (
    PHOSPHOR_BRIGHT,
    PHOSPHOR_DIM,
    AMBER_BRIGHT,
    PANEL_BG,
    PANEL_BORDER,
    RED_DANGER,
    GREEN_GOOD,
    YELLOW_WARN,
    FONT_SMALL,
    FONT_TINY,
)


class HUD:
    def __init__(self):
        self.font_small = pygame.font.SysFont("consolas", FONT_SMALL)
        self.font_tiny = pygame.font.SysFont("consolas", FONT_TINY)

    def draw_panel(self, surface, rect, title=""):
        pygame.draw.rect(surface, PANEL_BG, rect)
        pygame.draw.rect(surface, PANEL_BORDER, rect, 2)
        if title:
            txt = self.font_small.render(title, True, AMBER_BRIGHT)
            surface.blit(txt, (rect.x + 8, rect.y + 6))

    def draw_compass(self, surface, cx, cy, radius, course_deg):
        pygame.draw.circle(surface, PHOSPHOR_DIM, (cx, cy), radius, 2)
        for ang in range(0, 360, 30):
            rad = math.radians(ang)
            x1 = cx + int(math.sin(rad) * (radius - 8))
            y1 = cy - int(math.cos(rad) * (radius - 8))
            x2 = cx + int(math.sin(rad) * radius)
            y2 = cy - int(math.cos(rad) * radius)
            pygame.draw.line(surface, PHOSPHOR_DIM, (x1, y1), (x2, y2), 1)

        labels = [(0, "N"), (90, "E"), (180, "S"), (270, "W")]
        for ang, label in labels:
            rad = math.radians(ang)
            tx = cx + int(math.sin(rad) * (radius + 10)) - 6
            ty = cy - int(math.cos(rad) * (radius + 10)) - 8
            t = self.font_tiny.render(label, True, PHOSPHOR_BRIGHT)
            surface.blit(t, (tx, ty))

        # Course needle
        rad = math.radians(course_deg)
        nx = cx + int(math.sin(rad) * (radius - 12))
        ny = cy - int(math.cos(rad) * (radius - 12))
        pygame.draw.line(surface, AMBER_BRIGHT, (cx, cy), (nx, ny), 3)
        txt = self.font_small.render(f"{course_deg:03.0f}", True, AMBER_BRIGHT)
        surface.blit(txt, (cx - txt.get_width() // 2, cy + radius + 14))

    def draw_depth_gauge(self, surface, x, y, w, h, depth, max_depth):
        pygame.draw.rect(surface, PHOSPHOR_DIM, (x, y, w, h), 2)
        pct = 0 if max_depth <= 0 else max(0.0, min(1.0, depth / max_depth))
        fill_h = int((h - 4) * pct)
        color = GREEN_GOOD if pct < 0.6 else (YELLOW_WARN if pct < 0.85 else RED_DANGER)
        pygame.draw.rect(surface, color, (x + 2, y + h - 2 - fill_h, w - 4, fill_h))
        txt = self.font_tiny.render(f"{depth:.0f} ft", True, AMBER_BRIGHT)
        surface.blit(txt, (x, y - 18))

    def draw_speed_indicator(self, surface, x, y, w, h, speed, max_speed):
        pygame.draw.rect(surface, PHOSPHOR_DIM, (x, y, w, h), 2)
        pct = 0 if max_speed <= 0 else max(0.0, min(1.0, speed / max_speed))
        fill_w = int((w - 4) * pct)
        pygame.draw.rect(surface, PHOSPHOR_BRIGHT, (x + 2, y + 2, fill_w, h - 4))
        txt = self.font_tiny.render(f"{speed:.1f} / {max_speed:.1f} kts", True, AMBER_BRIGHT)
        surface.blit(txt, (x, y - 18))

    def draw_status_lines(self, surface, x, y, lines):
        for i, line in enumerate(lines):
            txt = self.font_tiny.render(line, True, PHOSPHOR_BRIGHT)
            surface.blit(txt, (x, y + i * 18))


def draw_horizon(surface, sky_color, sea_color, horizon_y):
    w, h = surface.get_size()
    pygame.draw.rect(surface, sky_color, (0, 0, w, horizon_y))
    pygame.draw.rect(surface, sea_color, (0, horizon_y, w, h - horizon_y))

    # Simple shimmer lines
    for i in range(8):
        yy = horizon_y + 20 + i * 20
        alpha = 40 + i * 8
        col = (min(255, sea_color[0] + alpha), min(255, sea_color[1] + alpha), min(255, sea_color[2] + alpha))
        pygame.draw.line(surface, col, (0, yy), (w, yy), 1)
