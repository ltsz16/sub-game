"""
Torpedo room management screen.
"""

import pygame

from game.state_manager import BaseScreen
from game.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    DARK_NAVY,
    PANEL_BG,
    PANEL_BORDER,
    PHOSPHOR_BRIGHT,
    AMBER_BRIGHT,
    LIGHT_GRAY,
    KEY_VIEW_CHART,
    KEY_VIEW_PERISCOPE,
    KEY_VIEW_BRIDGE,
    KEY_VIEW_DAMAGE,
    KEY_VIEW_TORPEDO,
)
from game.screens.combat_shared import update_combat_tick, cycle_to_view


class TorpedoRoomScreen(BaseScreen):
    def on_enter(self, manager, **kwargs):
        self.manager = manager
        self.font_title = pygame.font.SysFont("georgia", 38, bold=True)
        self.font = pygame.font.SysFont("consolas", 18)

    def handle_event(self, event):
        sub = self.manager.game_state.get("submarine")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                sub.reload_fore()
                sub.reload_aft()
            elif event.key == pygame.K_t:
                sub.torp_speed_high = not sub.torp_speed_high
            elif event.key == pygame.K_f:
                sub.torp_fuse = "magnetic" if sub.torp_fuse == "contact" else "contact"
            elif event.key == pygame.K_LEFTBRACKET:
                sub.torp_depth = max(1.0, sub.torp_depth - 1.0)
            elif event.key == pygame.K_RIGHTBRACKET:
                sub.torp_depth = min(45.0, sub.torp_depth + 1.0)
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

    def _draw_tubes(self, surface, x, y, tubes, label):
        title = self.font.render(label, True, AMBER_BRIGHT)
        surface.blit(title, (x, y))
        for i, tube in enumerate(tubes):
            r = pygame.Rect(x, y + 26 + i * 42, 300, 34)
            pygame.draw.rect(surface, (20, 28, 40), r)
            pygame.draw.rect(surface, (70, 90, 120), r, 1)
            status = "READY" if tube.ready else (f"RELOAD {tube.reload_timer:4.0f}s" if tube.reload_timer > 0 else "EMPTY")
            color = (80, 240, 140) if tube.ready else (230, 180, 80)
            txt = self.font.render(f"Tube {i+1:02d}  {status}", True, color)
            surface.blit(txt, (r.x + 10, r.y + 8))

    def draw(self, surface):
        sub = self.manager.game_state.get("submarine")
        surface.fill(DARK_NAVY)

        title = self.font_title.render("Torpedo Room", True, AMBER_BRIGHT)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 18))

        panel = pygame.Rect(40, 80, SCREEN_WIDTH - 80, SCREEN_HEIGHT - 120)
        pygame.draw.rect(surface, PANEL_BG, panel)
        pygame.draw.rect(surface, PANEL_BORDER, panel, 2)

        self._draw_tubes(surface, panel.x + 24, panel.y + 20, sub.tubes_fore, "Fore Tubes")
        self._draw_tubes(surface, panel.x + panel.width - 324, panel.y + 20, sub.tubes_aft, "Aft Tubes")

        settings = [
            f"Torpedoes remaining: {sub.torpedo_count}",
            f"Speed setting: {'HIGH' if sub.torp_speed_high else 'LOW'}",
            f"Depth setting: {sub.torp_depth:.0f} ft",
            f"Fuse type: {sub.torp_fuse.upper()}",
            "",
            "R reload empty tubes",
            "T toggle torpedo speed",
            "F toggle fuse (contact/magnetic)",
            "[ and ] adjust depth",
            "F1 Chart  F2 Periscope  F3 Bridge  F4 Damage",
        ]

        y = panel.y + 350
        for line in settings:
            color = PHOSPHOR_BRIGHT if line else LIGHT_GRAY
            txt = self.font.render(line, True, color)
            surface.blit(txt, (panel.x + 24, y))
            y += 24
