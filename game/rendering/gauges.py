"""
rendering/gauges.py - WWII-style analog submarine gauges with drawn elements.

Renders authentic-looking submarine instrument gauges for:
- Depth gauge (0-600+ ft)
- Speed gauge (0-20+ kts)
- Heading indicator (0-359°)
- Bow trim indicator
- Battery level
"""

import math
import pygame


def draw_depth_gauge(surface: pygame.Surface, x: int, y: int, 
                    current_depth: float, max_depth: float = 600.0, 
                    crush_depth: float = 600.0, size: int = 100):
    """Draw a circular depth gauge with needle."""
    # Outer circle (brass-colored)
    pygame.draw.circle(surface, (184, 134, 11), (x, y), size, 3)
    
    # Face
    pygame.draw.circle(surface, (30, 30, 30), (x, y), size - 3)
    
    # Scale markings
    for i in range(0, int(max_depth) + 100, 100):
        angle = (i / max_depth) * math.pi - math.pi / 2
        r1 = size - 15
        r2 = size - 5
        x1 = x + r1 * math.cos(angle)
        y1 = y + r1 * math.sin(angle)
        x2 = x + r2 * math.cos(angle)
        y2 = y + r2 * math.sin(angle)
        color = (255, 100, 100) if i >= crush_depth else (100, 200, 100)
        pygame.draw.line(surface, color, (x1, y1), (x2, y2), 2)
    
    # Red zone above crush depth
    crush_angle = (crush_depth / max_depth) * math.pi - math.pi / 2
    end_angle = crush_angle + math.pi * 0.5
    pygame.draw.arc(surface, (150, 0, 0), (x - size + 5, y - size + 5, (size - 5) * 2, (size - 5) * 2),
                   crush_angle, end_angle, 3)
    
    # Needle
    depth_ratio = min(1.0, current_depth / max_depth)
    needle_angle = depth_ratio * math.pi - math.pi / 2
    needle_len = size - 25
    nx = x + needle_len * math.cos(needle_angle)
    ny = y + needle_len * math.sin(needle_angle)
    pygame.draw.line(surface, (200, 200, 200), (x, y), (nx, ny), 2)
    
    # Center circle
    pygame.draw.circle(surface, (200, 200, 200), (x, y), 4)
    
    # Label
    font_small = pygame.font.SysFont("consolas", 12)
    label = font_small.render(f"{int(current_depth)} ft", True, (100, 200, 100))
    surface.blit(label, (x - label.get_width() // 2, y + size + 10))


def draw_speed_gauge(surface: pygame.Surface, x: int, y: int, 
                    current_speed: float, max_speed: float = 20.0, size: int = 100):
    """Draw a circular speed gauge with needle."""
    # Outer circle
    pygame.draw.circle(surface, (184, 134, 11), (x, y), size, 3)
    
    # Face
    pygame.draw.circle(surface, (30, 30, 30), (x, y), size - 3)
    
    # Scale markings (0, 5, 10, 15, 20 knots)
    for i in range(0, int(max_speed) + 5, 5):
        angle = (i / max_speed) * math.pi - math.pi / 2
        r1 = size - 15
        r2 = size - 5
        x1 = x + r1 * math.cos(angle)
        y1 = y + r1 * math.sin(angle)
        x2 = x + r2 * math.cos(angle)
        y2 = y + r2 * math.sin(angle)
        pygame.draw.line(surface, (100, 200, 100), (x1, y1), (x2, y2), 2)
        
        # Label
        if i % 10 == 0:
            font_tiny = pygame.font.SysFont("consolas", 10)
            label = font_tiny.render(str(i), True, (100, 200, 100))
            lx = x + (size - 8) * math.cos(angle)
            ly = y + (size - 8) * math.sin(angle)
            surface.blit(label, (int(lx - label.get_width() // 2), int(ly - label.get_height() // 2)))
    
    # Needle
    speed_ratio = min(1.0, current_speed / max_speed)
    needle_angle = speed_ratio * math.pi - math.pi / 2
    needle_len = size - 25
    nx = x + needle_len * math.cos(needle_angle)
    ny = y + needle_len * math.sin(needle_angle)
    pygame.draw.line(surface, (200, 200, 200), (x, y), (nx, ny), 2)
    
    # Center circle
    pygame.draw.circle(surface, (200, 200, 200), (x, y), 4)
    
    # Label
    font_small = pygame.font.SysFont("consolas", 12)
    label = font_small.render(f"{current_speed:.1f} kts", True, (100, 200, 100))
    surface.blit(label, (x - label.get_width() // 2, y + size + 10))


def draw_heading_indicator(surface: pygame.Surface, x: int, y: int, 
                          current_heading: float, size: int = 100):
    """Draw a circular heading indicator."""
    # Outer circle
    pygame.draw.circle(surface, (184, 134, 11), (x, y), size, 3)
    
    # Face
    pygame.draw.circle(surface, (30, 30, 30), (x, y), size - 3)
    
    # Cardinal directions
    cardinals = [(0, "N"), (90, "E"), (180, "S"), (270, "W")]
    for heading, label in cardinals:
        angle = math.radians(heading)
        r = size - 15
        lx = x + r * math.sin(angle)
        ly = y - r * math.cos(angle)
        font_small = pygame.font.SysFont("consolas", 14, bold=True)
        text = font_small.render(label, True, (150, 200, 150))
        surface.blit(text, (int(lx - text.get_width() // 2), int(ly - text.get_height() // 2)))
    
    # Degree ticks every 10 degrees
    for deg in range(0, 360, 10):
        angle = math.radians(deg)
        r1 = size - 10
        r2 = size - 5
        x1 = x + r1 * math.sin(angle)
        y1 = y - r1 * math.cos(angle)
        x2 = x + r2 * math.sin(angle)
        y2 = y - r2 * math.cos(angle)
        pygame.draw.line(surface, (100, 150, 100), (x1, y1), (x2, y2), 1)
    
    # Heading marker at top
    pygame.draw.polygon(surface, (200, 200, 200), [(x, y - size + 5), (x - 5, y - size + 12), (x + 5, y - size + 12)])
    
    # Center circle
    pygame.draw.circle(surface, (200, 200, 200), (x, y), 4)
    
    # Label
    font_small = pygame.font.SysFont("consolas", 12)
    label = font_small.render(f"{int(current_heading)}°", True, (100, 200, 100))
    surface.blit(label, (x - label.get_width() // 2, y + size + 10))


def draw_battery_gauge(surface: pygame.Surface, x: int, y: int, 
                      battery_fraction: float, width: int = 80, height: int = 20):
    """Draw a battery level bar."""
    # Outer frame
    pygame.draw.rect(surface, (184, 134, 11), (x - width // 2, y - height // 2, width, height), 2)
    
    # Background
    pygame.draw.rect(surface, (20, 20, 20), (x - width // 2 + 2, y - height // 2 + 2, width - 4, height - 4))
    
    # Charge level (green to red gradient)
    charge_width = int((width - 4) * battery_fraction)
    if battery_fraction > 0.5:
        color = (100, 200, 100)
    elif battery_fraction > 0.25:
        color = (200, 200, 100)
    else:
        color = (200, 100, 100)
    
    pygame.draw.rect(surface, color, (x - width // 2 + 2, y - height // 2 + 2, charge_width, height - 4))
    
    # Label
    font_tiny = pygame.font.SysFont("consolas", 10)
    label = font_tiny.render(f"{battery_fraction * 100:.0f}%", True, (100, 200, 100))
    surface.blit(label, (x - label.get_width() // 2, y + height + 5))


def draw_trim_indicator(surface: pygame.Surface, x: int, y: int, 
                       bow_trim: float, width: int = 100, height: int = 20):
    """Draw bow trim indicator (positive = bow up, negative = bow down)."""
    # Frame
    pygame.draw.rect(surface, (184, 134, 11), (x - width // 2, y - height // 2, width, height), 2)
    
    # Background
    pygame.draw.rect(surface, (20, 20, 20), (x - width // 2 + 2, y - height // 2 + 2, width - 4, height - 4))
    
    # Center line (neutral trim)
    center_x = x
    pygame.draw.line(surface, (100, 100, 100), (center_x, y - height // 2 + 2), (center_x, y + height // 2 - 2), 1)
    
    # Trim indicator (clamped to +/- 30 degrees)
    trim_ratio = max(-1.0, min(1.0, bow_trim / 30.0))
    indicator_x = int(center_x + trim_ratio * (width // 2 - 5))
    pygame.draw.polygon(surface, (200, 200, 200), [
        (indicator_x, y - 5),
        (indicator_x - 3, y),
        (indicator_x + 3, y)
    ])
    
    # Label
    font_tiny = pygame.font.SysFont("consolas", 10)
    label = font_tiny.render("Trim", True, (100, 200, 100))
    surface.blit(label, (x - label.get_width() // 2, y + height + 5))


def draw_submarine_status_panel(surface: pygame.Surface, submarine, x: int, y: int, 
                               panel_width: int = 320, panel_height: int = 240):
    """Draw a complete submarine status panel with all gauges."""
    # Panel background
    pygame.draw.rect(surface, (20, 20, 30), (x, y, panel_width, panel_height))
    pygame.draw.rect(surface, (100, 100, 100), (x, y, panel_width, panel_height), 2)
    
    # Title
    font = pygame.font.SysFont("consolas", 14, bold=True)
    title = font.render("SUBMARINE STATUS", True, (200, 200, 100))
    surface.blit(title, (x + 10, y + 5))
    
    # Gauges (2x2 layout)
    gauge_size = 60
    gauge_x1 = x + 45
    gauge_x2 = x + 170
    gauge_y1 = y + 40
    gauge_y2 = y + 140
    
    # Depth
    draw_depth_gauge(surface, gauge_x1, gauge_y1, submarine.depth, 
                    submarine.spec["max_depth"], 600, gauge_size)
    
    # Speed
    draw_speed_gauge(surface, gauge_x2, gauge_y1, submarine.speed, 20, gauge_size)
    
    # Heading
    draw_heading_indicator(surface, gauge_x1, gauge_y2, submarine.course, gauge_size)
    
    # Battery
    draw_battery_gauge(surface, gauge_x2, gauge_y2, 
                      submarine.battery / 10000.0, 60, 15)
    
    # Status text
    font_small = pygame.font.SysFont("consolas", 11)
    status_y = y + panel_height - 50
    
    status_lines = [
        f"Depth: {submarine.depth:.0f} ft",
        f"Speed: {submarine.speed:.1f} kts",
        f"Course: {submarine.course:.0f}°",
        f"Battery: {submarine.battery:.0f}",
    ]
    
    for i, line in enumerate(status_lines):
        color = (200, 100, 100) if submarine.depth >= 600 else (100, 200, 100)
        text = font_small.render(line, True, color)
        surface.blit(text, (x + 10, status_y + i * 14))
