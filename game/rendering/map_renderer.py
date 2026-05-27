"""
rendering/map_renderer.py — Strategic Pacific map and overlays.
"""

import pygame

from game.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    DARK_NAVY,
    OCEAN_DEEP,
    OCEAN_MID,
    PHOSPHOR_DIM,
    PHOSPHOR_BRIGHT,
    AMBER_BRIGHT,
    MAP_LAT_MAX,
    MAP_LAT_MIN,
)


class MapRenderer:
    def __init__(self):
        self.font = pygame.font.SysFont("consolas", 16)
        self._coast_polys = self._build_coast_polys()

    def world_to_screen(self, lon, lat, viewport):
        cx_lon, cx_lat, zoom = viewport
        # Base degrees visible at zoom=1
        vis_lon = 120.0 / zoom
        vis_lat = 80.0 / zoom
        sx = int(((lon - (cx_lon - vis_lon / 2)) / vis_lon) * SCREEN_WIDTH)
        sy = int(((MAP_LAT_MAX - lat) / vis_lat) * SCREEN_HEIGHT + ((cx_lat - MAP_LAT_MAX + vis_lat / 2) / vis_lat) * SCREEN_HEIGHT)
        return sx, sy

    def draw_map(self, surface, viewport):
        w, h = surface.get_size()
        surface.fill(DARK_NAVY)
        pygame.draw.rect(surface, OCEAN_DEEP, (0, 0, w, h))
        pygame.draw.rect(surface, OCEAN_MID, (0, 0, w, h), 2)

        # Grid lines (lat/lon)
        for lon in range(100, 201, 10):
            x, _ = self.world_to_screen(lon, 0, viewport)
            pygame.draw.line(surface, (12, 45, 75), (x, 0), (x, h), 1)
        for lat in range(-40, 61, 10):
            _, y = self.world_to_screen(140, lat, viewport)
            pygame.draw.line(surface, (12, 45, 75), (0, y), (w, y), 1)

        # Coast polygons
        for poly in self._coast_polys:
            pts = [self.world_to_screen(lon, lat, viewport) for lon, lat in poly]
            if len(pts) >= 3:
                pygame.draw.polygon(surface, (20, 70, 45), pts)
                pygame.draw.polygon(surface, (30, 100, 60), pts, 1)

    def draw_submarine(self, surface, lon, lat, course, viewport):
        x, y = self.world_to_screen(lon, lat, viewport)
        pygame.draw.circle(surface, PHOSPHOR_BRIGHT, (x, y), 5)
        # heading line
        import math
        rad = math.radians(course)
        hx = x + int(math.sin(rad) * 15)
        hy = y - int(math.cos(rad) * 15)
        pygame.draw.line(surface, AMBER_BRIGHT, (x, y), (hx, hy), 2)

    def draw_patrol_areas(self, surface, areas, viewport, selected_area_id=None):
        for area in areas:
            x, y = self.world_to_screen(area["center_lon"], area["center_lat"], viewport)
            # rough radius projection
            rx, _ = self.world_to_screen(area["center_lon"] + area["radius_deg"], area["center_lat"], viewport)
            r = max(8, abs(rx - x))
            color = AMBER_BRIGHT if area["id"] == selected_area_id else PHOSPHOR_DIM
            pygame.draw.circle(surface, color, (x, y), r, 1)
            name = self.font.render(area["name"], True, color)
            surface.blit(name, (x + 6, y - 8))

    def draw_contacts(self, surface, contacts, viewport):
        for c in contacts:
            x, y = self.world_to_screen(c["lon"], c["lat"], viewport)
            pygame.draw.circle(surface, (255, 180, 50), (x, y), 4)

    def draw_overlay_text(self, surface, lines):
        for i, line in enumerate(lines):
            txt = self.font.render(line, True, PHOSPHOR_BRIGHT)
            surface.blit(txt, (12, 12 + i * 18))

    def _build_coast_polys(self):
        # Simplified stylized Pacific landmasses
        japan = [(130, 31), (132, 35), (136, 39), (142, 45), (146, 42), (142, 37), (138, 33), (134, 30)]
        philippines = [(118, 6), (120, 12), (122, 16), (124, 18), (126, 13), (124, 9), (122, 5)]
        australia = [(112, -39), (114, -34), (122, -26), (132, -16), (144, -14), (152, -20), (154, -30), (148, -38), (136, -42), (122, -43)]
        new_guinea = [(141, -10), (145, -6), (152, -5), (153, -8), (149, -10), (144, -11)]
        marianas = [(143, 13), (144, 15), (146, 16), (146, 14)]
        hawaii = [(-160, 18), (-158, 20), (-156, 21), (-155, 19), (-157, 18)]

        # Convert negative lon to 0..360-like representation for easier map wrap
        polys = []
        for poly in [japan, philippines, australia, new_guinea, marianas, hawaii]:
            fixed = []
            for lon, lat in poly:
                if lon < 0:
                    lon = 360 + lon
                fixed.append((lon, lat))
            polys.append(fixed)
        return polys
