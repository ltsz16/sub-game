"""
rendering/sprites.py - Generate and cache ship sprite images at startup.

Converts procedural polygon rendering to sprite-based rendering.
Sprites can be loaded from PNG files or procedurally generated as fallback.
Sprites are cached as Pygame Surfaces for fast rendering.
"""

import os
import pygame
from pathlib import Path
from game.rendering.ship_renderer import _SIDE_SHIP_POLYS, _TOP_SHIP_POLYS


class SpriteCache:
    """Generate and cache ship sprites for fast rendering."""
    
    def __init__(self):
        self.side_sprites = {}  # {(ship_id, scale, color_tuple): Surface}
        self.top_sprites = {}   # {(ship_id, scale, color_tuple): Surface}
        self.asset_dir = Path("game/assets/images")
    
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
        
        # Try to load PNG file first
        sprite = self._load_side_image(ship_id, scale, color)
        if sprite is None:
            # Fallback to procedural generation
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
        
        # Try to load PNG file first
        sprite = self._load_top_image(ship_id, scale, color)
        if sprite is None:
            # Fallback to procedural generation
            sprite = self._generate_top_sprite(ship_id, scale, color)
        
        self.top_sprites[key] = sprite
        return sprite
    
    def _load_side_image(self, ship_id: str, scale: float, color) -> pygame.Surface | None:
        """Load a side-view PNG image if it exists."""
        image_path = self.asset_dir / "side" / f"{ship_id}.png"
        if not image_path.exists():
            return None
        
        try:
            img = pygame.image.load(str(image_path)).convert_alpha()
            
            # Images face left, flip to face right for consistency
            img = pygame.transform.flip(img, True, False)
            
            # Scale the image
            if scale != 1.0:
                new_width = int(img.get_width() * scale)
                new_height = int(img.get_height() * scale)
                img = pygame.transform.scale(img, (new_width, new_height))
            
            # Colorize based on the color parameter (tint the image)
            img = self._colorize_image(img, color)
            
            return img
        except Exception as e:
            print(f"Warning: Failed to load side image for {ship_id}: {e}")
            return None
    
    def _load_top_image(self, ship_id: str, scale: float, color) -> pygame.Surface | None:
        """Load a top-down PNG image if it exists."""
        image_path = self.asset_dir / "top" / f"{ship_id}.png"
        if not image_path.exists():
            return None
        
        try:
            img = pygame.image.load(str(image_path)).convert_alpha()
            
            # Scale the image
            if scale != 1.0:
                new_width = int(img.get_width() * scale)
                new_height = int(img.get_height() * scale)
                img = pygame.transform.scale(img, (new_width, new_height))
            
            # Colorize based on the color parameter
            img = self._colorize_image(img, color)
            
            return img
        except Exception as e:
            print(f"Warning: Failed to load top image for {ship_id}: {e}")
            return None
    
    def _colorize_image(self, surface: pygame.Surface, color) -> pygame.Surface:
        """Apply a color tint to an image while preserving alpha."""
        # Create a colored overlay
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill(color + (200,))  # Semi-transparent tint
        
        # Blend the overlay onto the image
        result = surface.copy()
        result.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return result
    
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


def generate_placeholder_images():
    """
    Generate placeholder PNG images for all ship types.
    Use this to create initial images that you can then customize.
    Creates game/assets/images/side/ and game/assets/images/top/ directories.
    """
    import os
    from pathlib import Path
    
    # Create directories
    side_dir = Path("game/assets/images/side")
    top_dir = Path("game/assets/images/top")
    side_dir.mkdir(parents=True, exist_ok=True)
    top_dir.mkdir(parents=True, exist_ok=True)
    
    # Ship types
    ships = [
        "submarine", "small_freighter", "large_freighter", "tanker", "ammo_ship",
        "troop_transport", "passenger_cargo", "minelayer", "destroyer", "cruiser",
        "battleship", "carrier"
    ]
    
    for ship_id in ships:
        # Generate side-view placeholder
        side_sprite = _generate_placeholder_side(ship_id)
        side_path = side_dir / f"{ship_id}.png"
        pygame.image.save(side_sprite, str(side_path))
        print(f"Generated placeholder: {side_path}")
        
        # Generate top-down placeholder
        top_sprite = _generate_placeholder_top(ship_id)
        top_path = top_dir / f"{ship_id}.png"
        pygame.image.save(top_sprite, str(top_path))
        print(f"Generated placeholder: {top_path}")


def _generate_placeholder_side(ship_id: str) -> pygame.Surface:
    """Generate a simple side-view placeholder image."""
    # Get base polygon
    poly = _SIDE_SHIP_POLYS.get(ship_id, _SIDE_SHIP_POLYS["small_freighter"])
    
    # Calculate bounds
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    # Scale up for visibility
    scale = 1.5
    scaled_poly = [(x * scale * 0.01, y * scale * 0.01) for x, y in poly]
    xs = [p[0] for p in scaled_poly]
    ys = [p[1] for p in scaled_poly]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    width = max(int(max_x - min_x) + 20, 100)
    height = max(int(max_y - min_y) + 20, 80)
    
    # Create surface with transparency
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))  # Transparent background
    
    # Draw polygon
    offset_x = -min_x + 10
    offset_y = -min_y + 10
    points = [(int(x + offset_x), int(y + offset_y)) for x, y in scaled_poly]
    
    # Use a neutral gray color
    color = (100, 120, 140)
    pygame.draw.polygon(surface, color, points)
    darker = tuple(max(0, c - 50) for c in color)
    pygame.draw.polygon(surface, darker, points, 2)
    
    return surface


def _generate_placeholder_top(ship_id: str) -> pygame.Surface:
    """Generate a simple top-down placeholder image."""
    # Get base polygon
    poly = _TOP_SHIP_POLYS.get(ship_id, _TOP_SHIP_POLYS["small_freighter"])
    
    # Scale for visibility
    scale = 1.0
    scaled_poly = [(x * scale * 0.3, y * scale * 0.3) for x, y in poly]
    xs = [p[0] for p in scaled_poly]
    ys = [p[1] for p in scaled_poly]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    width = max(int(max_x - min_x) + 20, 80)
    height = max(int(max_y - min_y) + 20, 80)
    
    # Create surface with transparency
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))  # Transparent background
    
    # Draw polygon
    offset_x = -min_x + 10
    offset_y = -min_y + 10
    points = [(int(x + offset_x), int(y + offset_y)) for x, y in scaled_poly]
    
    # Use a neutral gray color
    color = (100, 120, 140)
    pygame.draw.polygon(surface, color, points)
    darker = tuple(max(0, c - 50) for c in color)
    pygame.draw.polygon(surface, darker, points, 2)
    
    return surface


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
