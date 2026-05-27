"""
Patrol report screen: tonnage, medals, promotion.
"""

import pygame

from game.state_manager import BaseScreen
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, DARK_NAVY, PANEL_BG, PANEL_BORDER, AMBER_BRIGHT, PHOSPHOR_BRIGHT, LIGHT_GRAY
from game.systems.career import PatrolResult
from game.systems.medals import evaluate_patrol, rank_name
from game.entities.ship import ShipState


class PatrolReportScreen(BaseScreen):
    def on_enter(self, manager, **kwargs):
        self.manager = manager
        self.font_title = pygame.font.SysFont("georgia", 40, bold=True)
        self.font = pygame.font.SysFont("consolas", 18)
        self.font_small = pygame.font.SysFont("consolas", 16)

        self.career = manager.game_state.get("career")
        self.combat = manager.game_state.get("combat")
        self.sub = manager.game_state.get("submarine")

        self.result = self._build_result()
        eval_result = evaluate_patrol(self.result, self.career)
        self.result.medals_awarded = eval_result["medals"]
        self.result.promoted_to = eval_result["promoted"]
        self.messages = eval_result["messages"]

        self.career.end_patrol(self.result)

    def _build_result(self):
        convoy = self.combat["convoy"]
        r = PatrolResult()
        r.start_date = self.combat.get("patrol_start_date", self.career.current_date)
        r.end_date = self.career.current_date
        r.area_name = self.combat.get("area", {}).get("name", "Unknown Area")
        r.base_name = self.career.current_port
        r.torpedoes_fired = self.combat.get("shots_fired", 0)
        r.torpedoes_hit = self.combat.get("shots_hit", 0)
        r.depth_charges_taken = self.combat.get("depth_charges_taken", 0)
        r.crew_lost = self.sub.crew_casualties
        r.sub_survived = not self.sub.is_sunk

        for ship in convoy.ships:
            if ship.state == ShipState.SUNK or ship.state == ShipState.SINKING:
                entry = {
                    "name": ship.name,
                    "ship_id": ship.ship_id,
                    "tonnage": ship.tonnage,
                    "score_value": ship.score_value,
                }
                r.ships_sunk.append(entry)

        r.total_tonnage = sum(s["tonnage"] for s in r.ships_sunk)
        r.total_score = sum((s["tonnage"] / 1000.0) * s["score_value"] for s in r.ships_sunk)
        return r

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                from game.screens.strategic_map import StrategicMapScreen
                # Clear combat state and return to campaign map.
                self.manager.game_state.pop("combat", None)
                self.manager.switch(StrategicMapScreen())

    def draw(self, surface):
        surface.fill(DARK_NAVY)

        panel = pygame.Rect(70, 55, SCREEN_WIDTH - 140, SCREEN_HEIGHT - 110)
        pygame.draw.rect(surface, PANEL_BG, panel)
        pygame.draw.rect(surface, PANEL_BORDER, panel, 2)

        title = self.font_title.render("Patrol Report", True, AMBER_BRIGHT)
        surface.blit(title, (panel.x + 24, panel.y + 16))

        summary = [
            f"Date: {self.career.current_date.isoformat()}",
            f"Area: {self.result.area_name}",
            f"Commander Rank: {rank_name(self.career)}",
            f"Ships Sunk: {len(self.result.ships_sunk)}",
            f"Total Tonnage: {self.result.total_tonnage:,} tons",
            f"Torpedoes Fired: {self.result.torpedoes_fired}  Hits: {self.result.torpedoes_hit}",
            f"Depth Charge Runs Survived: {self.result.depth_charges_taken}",
        ]

        y = panel.y + 84
        for line in summary:
            txt = self.font.render(line, True, PHOSPHOR_BRIGHT)
            surface.blit(txt, (panel.x + 24, y))
            y += 24

        y += 8
        medal_header = self.font.render("Awards and Commendations", True, AMBER_BRIGHT)
        surface.blit(medal_header, (panel.x + 24, y))
        y += 28
        if self.messages:
            for line in self.messages[:5]:
                txt = self.font.render(line, True, LIGHT_GRAY)
                surface.blit(txt, (panel.x + 24, y))
                y += 22

        y += 12
        sunk_header = self.font.render("Confirmed Sinkings", True, AMBER_BRIGHT)
        surface.blit(sunk_header, (panel.x + 24, y))
        y += 28

        for s in self.result.ships_sunk[:8]:
            line = f"{s['name']:<28} {s['tonnage']:>6,} tons"
            txt = self.font_small.render(line, True, LIGHT_GRAY)
            surface.blit(txt, (panel.x + 24, y))
            y += 20

        hint = self.font_small.render("Press Enter to return to Strategic Map", True, PHOSPHOR_BRIGHT)
        surface.blit(hint, (panel.x + 24, panel.bottom - 28))
