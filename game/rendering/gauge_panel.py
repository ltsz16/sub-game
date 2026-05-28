"""
rendering/gauge_panel.py - Comprehensive gauge display similar to Silent Service II.

All submarine instrumentation on one dedicated view.
"""

import pygame
from game.rendering.gauges import (
    draw_depth_gauge,
    draw_speed_gauge,
    draw_heading_indicator,
    draw_battery_gauge,
)


def draw_main_gauge_panel(surface: pygame.Surface, submarine, x: int = 50, y: int = 50,
                         panel_width: int = 400, panel_height: int = 300):
    """
    Draw main gauge cluster with depth, speed, heading, and battery.
    2x2 gauge layout like a real submarine control room.
    """
    # Panel background
    pygame.draw.rect(surface, (20, 20, 30), (x, y, panel_width, panel_height))
    pygame.draw.rect(surface, (100, 100, 120), (x, y, panel_width, panel_height), 2)
    
    # Title
    font_title = pygame.font.SysFont("consolas", 14, bold=True)
    title = font_title.render("MAIN GAUGES", True, (200, 200, 100))
    surface.blit(title, (x + 15, y + 10))
    
    # Gauge positions (2x2 grid)
    gauge_size = 70
    gap = 40
    
    top_y = y + 35
    
    # Top row
    left_x = x + 30
    right_x = x + panel_width // 2 + 20
    
    # Top-left: Depth
    draw_depth_gauge(surface, left_x + gauge_size // 2, top_y + gauge_size // 2,
                     submarine.depth, submarine.spec["max_depth"], size=gauge_size - 10)
    
    # Top-right: Speed
    draw_speed_gauge(surface, right_x + gauge_size // 2, top_y + gauge_size // 2,
                     submarine.speed, max_speed=20, size=gauge_size - 10)
    
    # Bottom row
    bottom_y = top_y + gauge_size + gap + 10
    
    # Bottom-left: Heading
    draw_heading_indicator(surface, left_x + gauge_size // 2, bottom_y + gauge_size // 2,
                          submarine.course, size=gauge_size - 10)
    
    # Bottom-right: Battery
    draw_battery_gauge(surface, right_x + gauge_size // 2, bottom_y + gauge_size // 2,
                      submarine.battery_pct, width=gauge_size - 20, height=gauge_size - 30)


def draw_secondary_instruments(surface: pygame.Surface, submarine,
                              x: int, y: int, width: int = 300, height: int = 150):
    """
    Draw secondary instruments: temperature, pressure, trim, RPM, etc.
    """
    font_small = pygame.font.SysFont("consolas", 11)
    font_tiny = pygame.font.SysFont("consolas", 9)
    
    # Background
    pygame.draw.rect(surface, (15, 15, 25), (x, y, width, height))
    pygame.draw.rect(surface, (100, 100, 100), (x, y, width, height), 2)
    
    # Title
    title = font_small.render("SECONDARY GAUGES", True, (150, 200, 150))
    surface.blit(title, (x + 10, y + 5))
    
    # Data rows
    line_y = y + 25
    line_height = 18
    
    # Dive angle/trim
    dive_angle = "+" if submarine.target_depth > submarine.depth else "-" if submarine.target_depth < submarine.depth else "="
    trim_text = f"Trim: {dive_angle} | Depth Δ: {abs(submarine.target_depth - submarine.depth):.0f} ft"
    t = font_tiny.render(trim_text, True, (150, 180, 200))
    surface.blit(t, (x + 10, line_y))
    
    # Fuel
    line_y += line_height
    fuel_color = (200, 100, 100) if submarine.fuel_pct < 0.2 else (200, 150, 50) if submarine.fuel_pct < 0.5 else (100, 150, 200)
    fuel_text = f"Fuel: {submarine.fuel_pct * 100:.1f}% ({int(submarine.fuel)} units)"
    t = font_tiny.render(fuel_text, True, fuel_color)
    surface.blit(t, (x + 10, line_y))
    
    # Battery drain rate
    line_y += line_height
    if not submarine.surfaced and submarine.speed > 0:
        drain_rate = submarine.speed / max(0.01, submarine.spec["speed_submerged"]) * 10.0
        drain_text = f"Battery Drain: {drain_rate:.1f} units/sec"
    else:
        drain_rate = 0
        drain_text = "Battery Drain: Recharging" if submarine.surfaced else "Battery Drain: 0 (stopped)"
    t = font_tiny.render(drain_text, True, (150, 180, 150))
    surface.blit(t, (x + 10, line_y))
    
    # Torpedo status
    line_y += line_height
    ready_fore = sum(1 for t in submarine.tubes_fore if t.ready)
    ready_aft = sum(1 for t in submarine.tubes_aft if t.ready)
    torp_text = f"Torpedoes: Fore {ready_fore}/{len(submarine.tubes_fore)}  Aft {ready_aft}/{len(submarine.tubes_aft)}"
    t = font_tiny.render(torp_text, True, (150, 180, 150))
    surface.blit(t, (x + 10, line_y))
    
    # Sonar/Radar
    line_y += line_height
    sonar_status = "ACTIVE" if not submarine.silent_running else "PASSIVE"
    sonar_text = f"Sonar: {sonar_status} | Silent: {'ON' if submarine.silent_running else 'OFF'}"
    sonar_color = (200, 150, 50) if submarine.silent_running else (100, 200, 100)
    t = font_tiny.render(sonar_text, True, sonar_color)
    surface.blit(t, (x + 10, line_y))


def draw_compass_rose(surface: pygame.Surface, submarine,
                     x: int, y: int, size: int = 80):
    """
    Draw a detailed compass rose showing current heading.
    """
    font_tiny = pygame.font.SysFont("consolas", 8)
    
    # Draw circle
    pygame.draw.circle(surface, (30, 30, 30), (x, y), size)
    pygame.draw.circle(surface, (100, 100, 100), (x, y), size, 2)
    
    # Draw compass points
    import math
    for deg in range(0, 360, 30):
        angle = math.radians(deg)
        x1 = x + (size - 5) * math.sin(angle)
        y1 = y - (size - 5) * math.cos(angle)
        x2 = x + size * math.sin(angle)
        y2 = y - size * math.cos(angle)
        
        color = (200, 100, 100) if deg % 90 == 0 else (150, 150, 150)
        pygame.draw.line(surface, color, (x1, y1), (x2, y2), 2 if deg % 90 == 0 else 1)
    
    # Cardinal directions
    cardinals = [
        (0, "N"),
        (90, "E"),
        (180, "S"),
        (270, "W"),
    ]
    for heading, label in cardinals:
        angle = math.radians(heading)
        label_x = x + (size - 15) * math.sin(angle)
        label_y = y - (size - 15) * math.cos(angle)
        t = font_tiny.render(label, True, (200, 150, 100))
        surface.blit(t, (int(label_x - 3), int(label_y - 4)))
    
    # Current heading needle
    heading_angle = math.radians(submarine.course)
    needle_len = size - 15
    needle_x = x + needle_len * math.sin(heading_angle)
    needle_y = y - needle_len * math.cos(heading_angle)
    pygame.draw.line(surface, (200, 50, 50), (x, y), (needle_x, needle_y), 3)
    
    # Center circle
    pygame.draw.circle(surface, (200, 200, 200), (x, y), 4)


def draw_depth_indicator(surface: pygame.Surface, submarine,
                        x: int, y: int, width: int = 150, height: int = 40):
    """
    Draw a large, prominent depth indicator.
    Warns if approaching crush depth.
    """
    font_large = pygame.font.SysFont("consolas", 20, bold=True)
    font_small = pygame.font.SysFont("consolas", 10)
    
    # Color based on depth relative to crush depth
    crush_depth = submarine.spec["max_depth"]
    depth_ratio = submarine.depth / crush_depth
    
    if depth_ratio >= 0.9:
        bg_color = (100, 30, 30)  # Dark red
        text_color = (255, 50, 50)
    elif depth_ratio >= 0.75:
        bg_color = (80, 60, 30)  # Orange
        text_color = (255, 150, 50)
    elif submarine.depth < 50:
        bg_color = (30, 60, 100)  # Blue - shallow
        text_color = (100, 200, 255)
    else:
        bg_color = (30, 40, 30)  # Dark green
        text_color = (100, 200, 100)
    
    # Background
    pygame.draw.rect(surface, bg_color, (x, y, width, height))
    pygame.draw.rect(surface, text_color, (x, y, width, height), 2)
    
    # Depth value
    depth_text = f"{submarine.depth:.0f} ft"
    t = font_large.render(depth_text, True, text_color)
    surface.blit(t, (x + 10, y + 3))
    
    # Crush depth warning
    if depth_ratio >= 0.85:
        warning_text = f"MAX: {crush_depth:.0f}"
        t = font_small.render(warning_text, True, (255, 100, 100))
        surface.blit(t, (x + 10, y + 26))


def draw_rudder_indicator(surface: pygame.Surface, submarine,
                         x: int, y: int, width: int = 100, height: int = 30):
    """Draw rudder/course change indicator."""
    font_tiny = pygame.font.SysFont("consolas", 9)
    
    # Background
    pygame.draw.rect(surface, (20, 20, 30), (x, y, width, height))
    pygame.draw.rect(surface, (100, 100, 100), (x, y, width, height), 1)
    
    # Current course vs target
    course_text = f"Course: {submarine.course:.0f}°"
    t = font_tiny.render(course_text, True, (150, 180, 200))
    surface.blit(t, (x + 5, y + 5))
    
    # Rudder position (simplified)
    rudder_text = "Rudder: Amidship"
    t = font_tiny.render(rudder_text, True, (100, 150, 100))
    surface.blit(t, (x + 5, y + 17))
