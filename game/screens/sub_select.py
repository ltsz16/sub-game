"""
Submarine selection screen.
"""

import pygame

from game.state_manager import BaseScreen
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, DARK_NAVY, PANEL_BG, PANEL_BORDER, PHOSPHOR_BRIGHT, AMBER_BRIGHT, LIGHT_GRAY
from game.data.submarines import SUBMARINES
from game.entities.submarine import Submarine
from game.systems.career import CareerState
from game.rendering.sprites import draw_ship_side_sprite


class SubSelectScreen(BaseScreen):
    def on_enter(self, manager, **kwargs):
        self.manager = manager
        self.index = 0
        self.font_title = pygame.font.SysFont("georgia", 42, bold=True)
        self.font = pygame.font.SysFont("consolas", 20)
        self.font_small = pygame.font.SysFont("consolas", 16)

    def _wrap_text(self, text, max_width_chars=60):
        """Wrap text to fit within character width."""
        words = text.split()
        lines = []
        line = []
        for w in words:
            test_line = line + [w]
            test_str = " ".join(test_line)
            if len(test_str) > max_width_chars:
                if line:
                    lines.append(" ".join(line))
                line = [w]
            else:
                line = test_line
        if line:
            lines.append(" ".join(line))
        return lines

    def _draw_submarine_image(self, surface, sub_id, cx, cy):
        """Load and draw submarine class image from us_subs directory."""
        import os
        from pathlib import Path
        
        # Convert underscore to hyphen for filename (s_class -> s-class)
        filename = sub_id.replace("_", "-")
        image_path = Path("game/assets/images/side/us_subs") / f"{filename}.png"
        
        # Try to load the submarine-specific image
        if image_path.exists():
            try:
                img = pygame.image.load(str(image_path)).convert_alpha()
                
                # Scale to fit (target height ~180px to leave room)
                target_height = 180
                scale = target_height / img.get_height()
                new_width = int(img.get_width() * scale)
                new_height = int(img.get_height() * scale)
                img = pygame.transform.scale(img, (new_width, new_height))
                
                # Position at center
                rect = img.get_rect(center=(cx, cy))
                surface.blit(img, rect)
                return
            except Exception as e:
                print(f"Warning: Failed to load submarine image {sub_id}: {e}")
        
        # Fallback to generic submarine sprite if image not found
        draw_ship_side_sprite(surface, "submarine", cx, cy, scale=5.5, color=(100, 200, 240))

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

        # Draw submarine class image from us_subs directory (positioned on left-center)
        self._draw_submarine_image(surface, spec["id"], card.x + 150, card.y + 200)

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

        x = card.x + 280
        y = card.y + 80
        for i, line in enumerate(lines):
            txt = self.font.render(line, True, LIGHT_GRAY)
            surface.blit(txt, (x, y + i * 28))

        # Wrap and render description (moved to right side with specs)
        desc_lines = self._wrap_text(spec["description"], max_width_chars=65)
        desc_y = card.y + 290
        for desc_line in desc_lines[:3]:  # max 3 lines
            desc_txt = self.font_small.render(desc_line, True, (185, 205, 220))
            surface.blit(desc_txt, (card.x + 280, desc_y))
            desc_y += 18

        hint = self.font_small.render("Left/Right: choose submarine    Enter: begin career    Esc: back", True, LIGHT_GRAY)
        surface.blit(hint, (card.x + 24, card.bottom - 32))
