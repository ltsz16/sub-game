"""
rendering/sprites.py - Generate and cache ship sprite images at startup.

Converts procedural polygon rendering to sprite-based rendering.
Sprites are pre-generated as Pygame Surfaces and cached for fast rendering.
"""

import pygame
from game.rendering.ship_renderer import _SIDE_SHIP_POLYS, _TOP_SHIP_POLYS


class SpriteCache:
    """Generate and cache ship sprites for fast rendering."""
    
    def __init__(self):
        self.side_sprites = {}  # {(ship_id, scale, color_tuple): Surface}
        self.top_sprites = {}   # {(ship_id, scale, color_tuple): Surface}
    
    def _color_to_key(self, color):
        """Convert color tuple to hashable key."""
        return tuple(color) if color else (128, 128, 128)
    
    def get_side_sprite(self, ship_id: str, scale: float = 1.0, color=None) -> pygame.Surface:
        """Get or generate a side-view sprite for a ship."""
        if color is None:
            color = (120, 120, 120)
        color_key = self._color_to_key(color)
        key = (ship_id, round(scale, 1), color_key)
        
        if key in self.side_sprites:
            return self.side_sprites[key]
        
        # Generate sprite
        sprite = self._generate_side_sprite(ship_id, scale, color)
        self.side_sprites[key] = sprite
        return sprite
    
    def get_top_sprite(self, ship_id: str, scale: float = 1.0, color=None) -> pygame.Surface:
        """Get or generate a top-down sprite for a ship."""
        if color is None:
            color = (120, 120, 120)
        color_key = self._color_to_key(color)
        key = (ship_id, round(scale, 1), color_key)
        
        if key in self.top_sprites:
            return self.top_sprites[key]
        
        # Generate sprite
        sprite = self._generate_top_sprite(ship_id, scale, color)
        self.top_sprites[key] = sprite
        return sprite
    
    def _generate_side_sprite(self, ship_id: str, scale: float, color) -> pygame.Surface:
        """Generate a side-view sprite by rendering polygon to surface."""
        poly = _SIDE_SHIP_POLYS.get(ship_id, _SIDE_SHIP_POLYS["small_freighter"])
        
        # Calculate bounds
        xs = [p[0] for p in poly]
        ys = [p[1] for p in poly]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        # Scale polygon
        scaled_poly = [(x * scale * 0.01, y * scale * 0.01) for x, y in poly]
        xs = [p[0] for p in scaled_poly]
        ys = [p[1] for p in scaled_poly]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        width = int(max_x - min_x) + 10
        height = int(max_y - min_y) + 10
        
        # Create surface
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Draw polygon
        offset_x = -min_x + 5
        offset_y = -min_y + 5
        points = [(int(x + offset_x), int(y + offset_y)) for x, y in scaled_poly]
        
        pygame.draw.polygon(surface, color, points)
        darker = tuple(max(0, c - 40) for c in color)
        pygame.draw.polygon(surface, darker, points, 1)
        
        return surface
    
    def _generate_top_sprite(self, ship_id: str, scale: float, color) -> pygame.Surface:
        """Generate a top-down sprite by rendering polygon to surface."""
        poly = _TOP_SHIP_POLYS.get(ship_id, _TOP_SHIP_POLYS["small_freighter"])
        
        # Scale polygon
        scaled_poly = [(x * scale * 0.3, y * scale * 0.3) for x, y in poly]
        xs = [p[0] for p in scaled_poly]
        ys = [p[1] for p in scaled_poly]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        width = int(max_x - min_x) + 10
        height = int(max_y - min_y) + 10
        
        # Create surface
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Draw polygon
        offset_x = -min_x + 5
        offset_y = -min_y + 5
        points = [(int(x + offset_x), int(y + offset_y)) for x, y in scaled_poly]
        
        pygame.draw.polygon(surface, color, points)
        darker = tuple(max(0, c - 40) for c in color)
        pygame.draw.polygon(surface, darker, points, 1)
        
        return surface
    
    def clear_cache(self):
        """Clear all cached sprites."""
        self.side_sprites.clear()
        self.top_sprites.clear()


# Global sprite cache instance
_sprite_cache = SpriteCache()


def get_side_sprite(ship_id: str, scale: float = 1.0, color=None) -> pygame.Surface:
    """Get a side-view sprite."""
    return _sprite_cache.get_side_sprite(ship_id, scale, color)


def get_top_sprite(ship_id: str, scale: float = 1.0, color=None) -> pygame.Surface:
    """Get a top-down sprite."""
    return _sprite_cache.get_top_sprite(ship_id, scale, color)


def draw_ship_side_sprite(surface: pygame.Surface, ship_id: str, cx: int, cy: int,
                          scale: float = 1.0, color=None, facing_right: bool = True,
                          rotation: float = 0.0):
    """Draw a ship from a cached sprite (side view)."""
    sprite = get_side_sprite(ship_id, scale, color)
    
    # Flip if needed
    if not facing_right:
        sprite = pygame.transform.flip(sprite, True, False)
    
    # Rotate if needed
    if rotation != 0:
        sprite = pygame.transform.rotate(sprite, rotation)
    
    # Get rect and position at center
    rect = sprite.get_rect(center=(cx, cy))
    surface.blit(sprite, rect)


def draw_ship_top_sprite(surface: pygame.Surface, ship_id: str, cx: int, cy: int,
                         scale: float = 1.0, color=None, course_deg: float = 0.0):
    """Draw a ship from a cached sprite (top-down view)."""
    sprite = get_top_sprite(ship_id, scale, color)
    
    # Rotate based on course
    if course_deg != 0:
        rotation = course_deg - 90  # 0° course (north) needs -90° rotation
        sprite = pygame.transform.rotate(sprite, -rotation)
    
    # Get rect and position at center
    rect = sprite.get_rect(center=(cx, cy))
    surface.blit(sprite, rect)
