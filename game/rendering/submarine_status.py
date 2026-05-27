"""
rendering/submarine_status.py - Enhanced submarine status display with warnings.

Displays battery, fuel, silent running, detection status, and depth mode info.
"""

import pygame
from game.constants import DEPTH_PERISCOPE, DEPTH_SHALLOW, DEPTH_CRUSH


def draw_battery_bar(surface: pygame.Surface, x: int, y: int, 
                     battery_pct: float, width: int = 120, height: int = 16):
    """Draw battery charge bar with color coding."""
    # Frame
    pygame.draw.rect(surface, (100, 100, 100), (x, y, width, height), 2)
    
    # Background
    pygame.draw.rect(surface, (20, 20, 20), (x + 2, y + 2, width - 4, height - 4))
    
    # Charge level with color gradient
    charge_width = int((width - 4) * battery_pct)
    if battery_pct > 0.5:
        color = (50, 200, 50)  # Green
    elif battery_pct > 0.25:
        color = (200, 200, 50)  # Yellow
    else:
        color = (200, 50, 50)  # Red (critical)
    
    pygame.draw.rect(surface, color, (x + 2, y + 2, charge_width, height - 4))
    
    # Percentage text
    font = pygame.font.SysFont("consolas", 10)
    label = font.render(f"{battery_pct * 100:.0f}%", True, (200, 200, 200))
    text_x = x + width // 2 - label.get_width() // 2
    text_y = y + height // 2 - label.get_height() // 2
    surface.blit(label, (text_x, text_y))


def draw_fuel_bar(surface: pygame.Surface, x: int, y: int, 
                  fuel_pct: float, width: int = 120, height: int = 16):
    """Draw fuel reserve bar."""
    # Frame
    pygame.draw.rect(surface, (100, 100, 100), (x, y, width, height), 2)
    
    # Background
    pygame.draw.rect(surface, (20, 20, 20), (x + 2, y + 2, width - 4, height - 4))
    
    # Fuel level with color gradient
    fuel_width = int((width - 4) * fuel_pct)
    if fuel_pct > 0.5:
        color = (100, 150, 200)  # Blue
    elif fuel_pct > 0.25:
        color = (200, 200, 50)  # Yellow
    else:
        color = (200, 100, 50)  # Orange (critical)
    
    pygame.draw.rect(surface, color, (x + 2, y + 2, fuel_width, height - 4))
    
    # Percentage text
    font = pygame.font.SysFont("consolas", 10)
    label = font.render(f"{fuel_pct * 100:.0f}%", True, (200, 200, 200))
    text_x = x + width // 2 - label.get_width() // 2
    text_y = y + height // 2 - label.get_height() // 2
    surface.blit(label, (text_x, text_y))


def draw_submarine_status_hud(surface: pygame.Surface, submarine, combat_state,
                              x: int = 10, y: int = 10):
    """
    Draw compact submarine status display.
    Shows depth, speed, battery, fuel, silent running status, and detection warnings.
    """
    font_small = pygame.font.SysFont("consolas", 11)
    font_tiny = pygame.font.SysFont("consolas", 10)
    
    # Background panel
    panel_width = 280
    panel_height = 110
    pygame.draw.rect(surface, (10, 10, 20), (x, y, panel_width, panel_height))
    pygame.draw.rect(surface, (80, 80, 100), (x, y, panel_width, panel_height), 2)
    
    # Line 1: Depth and Mode
    depth_color = (200, 100, 100) if submarine.depth >= DEPTH_CRUSH else (100, 200, 100)
    depth_text = f"Depth: {submarine.depth:.0f} ft"
    
    # Determine depth mode
    if submarine.surfaced:
        mode = "SURFACE"
        mode_color = (150, 150, 200)
    elif submarine.depth <= DEPTH_PERISCOPE:
        mode = "PERISCOPE"
        mode_color = (150, 200, 150)
    elif submarine.depth <= DEPTH_SHALLOW:
        mode = "SHALLOW"
        mode_color = (200, 200, 100)
    elif submarine.depth >= DEPTH_CRUSH - 50:
        mode = "CRUSH!"
        mode_color = (200, 50, 50)
    else:
        mode = "DEEP"
        mode_color = (100, 150, 200)
    
    t = font_small.render(f"{depth_text}  [{mode}]", True, depth_color)
    surface.blit(t, (x + 10, y + 8))
    
    # Line 2: Speed and Silent Running
    silent_text = " [SILENT]" if submarine.silent_running else ""
    speed_text = f"Speed: {submarine.speed:.1f} kts{silent_text}"
    color = (150, 150, 50) if submarine.silent_running else (150, 200, 150)
    t = font_small.render(speed_text, True, color)
    surface.blit(t, (x + 10, y + 24))
    
    # Line 3: Course
    t = font_small.render(f"Course: {submarine.course:.0f}°", True, (150, 200, 150))
    surface.blit(t, (x + 10, y + 40))
    
    # Line 4: Battery
    t = font_tiny.render("Battery:", True, (150, 150, 150))
    surface.blit(t, (x + 10, y + 56))
    draw_battery_bar(surface, x + 80, y + 54, submarine.battery_pct, width=90, height=14)
    
    # Line 5: Fuel
    t = font_tiny.render("Fuel:", True, (150, 150, 150))
    surface.blit(t, (x + 10, y + 74))
    draw_fuel_bar(surface, x + 80, y + 72, submarine.fuel_pct, width=90, height=14)
    
    # Detection warning if being hunted
    if combat_state and combat_state.get("detected"):
        warning = "⚠ DETECTED BY SONAR ⚠"
        t = font_small.render(warning, True, (200, 50, 50))
        surface.blit(t, (x + 10, y + 90))


def draw_depth_preset_buttons(surface: pygame.Surface, submarine,
                              x: int, y: int):
    """
    Draw quick-access depth mode buttons.
    Shows Periscope, Shallow, Crush, and Current Target.
    """
    font_tiny = pygame.font.SysFont("consolas", 9)
    
    button_width = 55
    button_height = 16
    
    presets = [
        ("P", "PERIS", DEPTH_PERISCOPE, (100, 180, 100)),
        ("S", "SHAL", DEPTH_SHALLOW, (180, 180, 100)),
        ("M", "MAX", submarine.spec["max_depth"], (100, 150, 180)),
    ]
    
    for i, (key, label, depth, color) in enumerate(presets):
        bx = x + i * (button_width + 5)
        
        # Button background
        pygame.draw.rect(surface, (30, 30, 40), (bx, y, button_width, button_height))
        pygame.draw.rect(surface, color, (bx, y, button_width, button_height), 1)
        
        # Text
        t = font_tiny.render(f"{key}:{label}", True, color)
        surface.blit(t, (bx + 3, y + 3))
    
    # Target depth indicator
    target_label = f"TGT: {submarine.target_depth:.0f} ft"
    t = font_tiny.render(target_label, True, (150, 180, 200))
    surface.blit(t, (x + 175, y + 3))


def draw_detection_status(surface: pygame.Surface, detection_range: float,
                         is_detected: bool, silent_running: bool,
                         x: int, y: int):
    """
    Draw sonar/detection status display.
    Shows current detection range and whether being hunted.
    """
    font_tiny = pygame.font.SysFont("consolas", 10)
    
    # Background
    pygame.draw.rect(surface, (10, 10, 20), (x, y, 200, 35))
    pygame.draw.rect(surface, (100, 80, 80), (x, y, 200, 35), 1)
    
    # Detection state
    if is_detected:
        status = "ACTIVE SONAR CONTACT"
        status_color = (200, 50, 50)
    elif silent_running:
        status = "SILENT RUNNING"
        status_color = (100, 200, 100)
    else:
        status = "READY"
        status_color = (150, 180, 200)
    
    t = font_tiny.render(f"Status: {status}", True, status_color)
    surface.blit(t, (x + 5, y + 3))
    
    # Sonar range
    range_text = f"Sonar Range: {detection_range:.2f} nm"
    t = font_tiny.render(range_text, True, (150, 150, 150))
    surface.blit(t, (x + 5, y + 17))


def get_battery_time_remaining(submarine) -> str:
    """Calculate and format time remaining on battery at current speed."""
    if submarine.surfaced or submarine.battery <= 0:
        return "∞ (surface)"
    
    # Drain rate when submerged
    drain_rate = submarine.speed / max(0.01, submarine.spec["speed_submerged"]) * 10.0
    if drain_rate <= 0:
        return "∞"
    
    seconds_remaining = submarine.battery / drain_rate
    hours = int(seconds_remaining / 3600)
    minutes = int((seconds_remaining % 3600) / 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"


def get_fuel_range_remaining(submarine) -> str:
    """Calculate and format distance remaining on fuel at current speed."""
    if submarine.battery <= 0 or submarine.speed <= 0:
        return "0 nm"
    
    # Fuel drain rate (surface only)
    if not submarine.surfaced:
        return "N/A (sub)"
    
    fuel_rate = submarine.speed * 2.0
    if fuel_rate <= 0:
        return "∞"
    
    nm_remaining = submarine.fuel / fuel_rate
    return f"{nm_remaining:.0f} nm"
