"""
Damage control screen.
"""

import pygame

from game.state_manager import BaseScreen
from game.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PANEL_BG,
    PANEL_BORDER,
    DARK_NAVY,
    PHOSPHOR_BRIGHT,
    AMBER_BRIGHT,
    GREEN_GOOD,
    YELLOW_WARN,
    ORANGE_CAUTION,
    RED_DANGER,
    COMPARTMENTS,
    KEY_VIEW_CHART,
    KEY_VIEW_PERISCOPE,
    KEY_VIEW_BRIDGE,
    KEY_VIEW_DAMAGE,
    KEY_VIEW_TORPEDO,
)
from game.screens.combat_shared import update_combat_tick, cycle_to_view


class DamageControlScreen(BaseScreen):
    def on_enter(self, manager, **kwargs):
        self.manager = manager
        self.font_title = pygame.font.SysFont("georgia", 40, bold=True)
        self.font = pygame.font.SysFont("consolas", 18)

    def handle_event(self, event):
        sub = self.manager.game_state.get("submarine")
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5):
                idx = int(event.unicode) - 1 if event.unicode.isdigit() else -1
                if 0 <= idx < len(COMPARTMENTS):
                    sub.repair_assignment = COMPARTMENTS[idx]
            elif event.key == pygame.K_0:
                sub.repair_assignment = None
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

    def _status_color(self, damage):
        if damage < 0.25:
            return GREEN_GOOD
        if damage < 0.5:
            return YELLOW_WARN
        if damage < 0.75:
            return ORANGE_CAUTION
        return RED_DANGER

    def draw(self, surface):
        sub = self.manager.game_state.get("submarine")
        surface.fill(DARK_NAVY)

        title = self.font_title.render("Damage Control", True, AMBER_BRIGHT)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))

        panel = pygame.Rect(120, 100, SCREEN_WIDTH - 240, SCREEN_HEIGHT - 180)
        pygame.draw.rect(surface, PANEL_BG, panel)
        pygame.draw.rect(surface, PANEL_BORDER, panel, 2)

        # Sub hull outline
        hull = pygame.Rect(panel.x + 70, panel.y + 120, panel.width - 140, 220)
        pygame.draw.rect(surface, (45, 55, 70), hull, border_radius=25)
        pygame.draw.rect(surface, (70, 90, 120), hull, 2, border_radius=25)

        comp_w = hull.width // 5
        for i, comp in enumerate(COMPARTMENTS):
            x = hull.x + i * comp_w
            r = pygame.Rect(x + 3, hull.y + 6, comp_w - 6, hull.height - 12)
            damage = sub.damage[comp]
            flooding = sub.flooding[comp]
            color = self._status_color(damage)
            pygame.draw.rect(surface, (18, 22, 30), r)

            fill_h = int((r.height - 8) * max(damage, flooding))
            pygame.draw.rect(surface, color, (r.x + 4, r.bottom - 4 - fill_h, r.width - 8, fill_h))
            pygame.draw.rect(surface, color, r, 2)

            label = self.font.render(f"{i+1}", True, PHOSPHOR_BRIGHT)
            surface.blit(label, (r.centerx - 5, r.y - 22))

            short = comp.split(" ")[0]
            txt = self.font.render(short, True, PHOSPHOR_BRIGHT)
            surface.blit(txt, (r.centerx - txt.get_width() // 2, r.bottom + 8))

            pct = self.font.render(f"{damage*100:3.0f}%", True, PHOSPHOR_BRIGHT)
            surface.blit(pct, (r.centerx - pct.get_width() // 2, r.bottom + 30))

        assign = sub.repair_assignment or "None"
        info = [
            f"Hull Integrity: {sub.hull_integrity*100:.0f}%",
            f"Flooded Compartments: {sum(1 for v in sub.flooding.values() if v > 0.2)}",
            f"Repair Team Assigned: {assign}",
            "Keys 1-5 assign repair teams, 0 clears assignment",
            "F1 Chart  F2 Periscope  F3 Bridge  F5 Torpedo Room",
        ]
        y = panel.y + panel.height - 105
        for line in info:
            t = self.font.render(line, True, PHOSPHOR_BRIGHT)
            surface.blit(t, (panel.x + 22, y))
            y += 20
