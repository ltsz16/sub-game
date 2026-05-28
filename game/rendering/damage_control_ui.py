"""
rendering/damage_control_ui.py - Enhanced graphical damage control display.

Shows submarine compartments in a schematic layout with status indicators.
"""

import pygame
from game.constants import COMPARTMENTS


class CompartmentBox:
    """Represents a visual compartment in the schematic."""
    
    def __init__(self, name: str, x: int, y: int, width: int = 60, height: int = 40):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.damage = 0.0
        self.flooding = 0.0
        self.repairing = False


def draw_compartment_status(surface: pygame.Surface, compartment_boxes: list,
                           submarine, x_offset: int = 10, y_offset: int = 10):
    """
    Draw compartment grid showing damage and flooding status.
    Inspired by Silent Service II damage control schematic.
    """
    font_small = pygame.font.SysFont("consolas", 10, bold=True)
    font_tiny = pygame.font.SysFont("consolas", 8)
    
    # Draw title
    font_title = pygame.font.SysFont("consolas", 14, bold=True)
    title = font_title.render("DAMAGE CONTROL SCHEMATIC", True, (100, 200, 100))
    surface.blit(title, (x_offset, y_offset))
    
    # Organize compartments into a 2D grid layout (8 across, 2 down for 16 compartments)
    cell_width = 75
    cell_height = 50
    grid_x_start = x_offset
    grid_y_start = y_offset + 25
    
    for idx, comp_name in enumerate(COMPARTMENTS):
        # Calculate grid position (8 columns)
        grid_x = idx % 8
        grid_y = idx // 8
        
        box_x = grid_x_start + grid_x * (cell_width + 3)
        box_y = grid_y_start + grid_y * (cell_height + 3)
        
        # Get compartment status
        damage = submarine.damage.get(comp_name, 0.0)
        flooding = submarine.flooding.get(comp_name, 0.0)
        repairing = submarine.repair_assignment == comp_name
        
        # Determine box color based on status
        if damage >= 1.0:
            color = (100, 50, 50)  # Dark red - destroyed
            status_text = "DESTROYED"
            status_color = (200, 50, 50)
        elif damage >= 0.75:
            color = (100, 80, 50)  # Orange - critical
            status_text = "CRITICAL"
            status_color = (200, 150, 50)
        elif damage >= 0.5:
            color = (80, 80, 80)  # Gray - damaged
            status_text = "DAMAGED"
            status_color = (150, 150, 150)
        else:
            color = (50, 100, 50)  # Green - intact
            status_text = "INTACT"
            status_color = (100, 200, 100)
        
        # Add flooding overlay
        if flooding > 0.5:
            color = (30, 80, 120)  # Blue tint for heavy flooding
            status_text = "FLOODED"
            status_color = (100, 150, 200)
        elif flooding > 0.0:
            # Light blue tint for light flooding
            color = tuple(int(c * 0.7 + 30 * 0.3) for c in color)
            status_text = "LEAKING"
            status_color = (150, 180, 200)
        
        # Repair highlight
        if repairing:
            color = tuple(int(c * 0.8 + 150 * 0.2) for c in color)
        
        # Draw box
        pygame.draw.rect(surface, color, (box_x, box_y, cell_width, cell_height))
        pygame.draw.rect(surface, (200, 200, 200), (box_x, box_y, cell_width, cell_height), 1)
        
        # Draw compartment name
        name_text = font_small.render(comp_name[:12], True, (200, 200, 200))
        surface.blit(name_text, (box_x + 3, box_y + 3))
        
        # Draw status
        status_label = font_tiny.render(status_text, True, status_color)
        surface.blit(status_label, (box_x + 3, box_y + 18))
        
        # Draw damage percentage
        damage_pct = int(damage * 100)
        damage_text = font_tiny.render(f"{damage_pct}%", True, (200, 150, 150))
        surface.blit(damage_text, (box_x + 3, box_y + 28))
        
        # Draw flooding indicator
        if flooding > 0:
            flood_pct = int(flooding * 100)
            flood_text = font_tiny.render(f"F:{flood_pct}%", True, (100, 150, 200))
            surface.blit(flood_text, (box_x + 35, box_y + 28))
        
        # Repair indicator
        if repairing:
            repair_text = font_tiny.render("REPAIR", True, (200, 200, 100))
            surface.blit(repair_text, (box_x + 3, box_y + 38))


def draw_damage_summary(surface: pygame.Surface, submarine, 
                       x: int, y: int, width: int = 250, height: int = 120):
    """Draw summary of overall submarine damage status."""
    font_small = pygame.font.SysFont("consolas", 11)
    font_tiny = pygame.font.SysFont("consolas", 9)
    
    # Background
    pygame.draw.rect(surface, (15, 15, 25), (x, y, width, height))
    pygame.draw.rect(surface, (100, 80, 80), (x, y, width, height), 2)
    
    # Title
    title = font_small.render("HULL STATUS", True, (200, 100, 100))
    surface.blit(title, (x + 10, y + 5))
    
    # Overall integrity
    integrity = submarine.hull_integrity
    integrity_color = (200, 100, 100) if integrity < 0.5 else (150, 150, 100) if integrity < 0.8 else (100, 200, 100)
    
    line_y = y + 25
    integrity_text = f"Integrity: {integrity * 100:.1f}%"
    t = font_small.render(integrity_text, True, integrity_color)
    surface.blit(t, (x + 10, line_y))
    
    # Critical damages count
    line_y += 18
    critical = sum(1 for v in submarine.damage.values() if v >= 0.75)
    critical_color = (200, 50, 50) if critical >= 2 else (200, 150, 50) if critical >= 1 else (100, 200, 100)
    critical_text = f"Critical Damage: {critical}"
    t = font_small.render(critical_text, True, critical_color)
    surface.blit(t, (x + 10, line_y))
    
    # Flooding compartments
    line_y += 18
    flooding_comps = sum(1 for v in submarine.flooding.values() if v > 0)
    flood_color = (200, 50, 50) if flooding_comps >= 2 else (150, 150, 50) if flooding_comps >= 1 else (100, 150, 200)
    flood_text = f"Flooding: {flooding_comps} compartments"
    t = font_small.render(flood_text, True, flood_color)
    surface.blit(t, (x + 10, line_y))
    
    # Crew status
    line_y += 18
    crew_text = f"Crew: {submarine.crew - submarine.crew_casualties}/{submarine.crew}"
    crew_color = (200, 50, 50) if submarine.crew_casualties > 5 else (200, 150, 50) if submarine.crew_casualties > 0 else (100, 200, 100)
    t = font_small.render(crew_text, True, crew_color)
    surface.blit(t, (x + 10, line_y))


def draw_critical_systems_status(surface: pygame.Surface, submarine,
                                x: int, y: int, width: int = 250, height: int = 100):
    """Draw status of critical submarine systems."""
    font_small = pygame.font.SysFont("consolas", 10)
    font_tiny = pygame.font.SysFont("consolas", 8)
    
    # Background
    pygame.draw.rect(surface, (15, 15, 25), (x, y, width, height))
    pygame.draw.rect(surface, (80, 100, 80), (x, y, width, height), 2)
    
    # Title
    title = font_small.render("CRITICAL SYSTEMS", True, (100, 200, 100))
    surface.blit(title, (x + 10, y + 5))
    
    systems = [
        ("Engines", submarine.damage.get("Engine Room", 0.0)),
        ("Reactor", submarine.damage.get("Reactor", 0.0) if "Reactor" in submarine.damage else submarine.damage.get("Engines", 0.0)),
        ("Torpedo", submarine.damage.get("Aft Torpedo Room", 0.0)),
        ("Batteries", submarine.damage.get("Aft Batteries", 0.0)),
    ]
    
    line_y = y + 20
    for sys_name, damage in systems:
        if damage > 0.5:
            color = (200, 50, 50)
            status = "DAMAGED"
        elif damage > 0.0:
            color = (200, 150, 50)
            status = "WARN"
        else:
            color = (100, 200, 100)
            status = "OK"
        
        t = font_tiny.render(f"{sys_name}: {status}", True, color)
        surface.blit(t, (x + 10, line_y))
        line_y += 14


def draw_repair_status(surface: pygame.Surface, submarine,
                      x: int, y: int, width: int = 250, height: int = 80):
    """Draw current repair status and progress."""
    font_small = pygame.font.SysFont("consolas", 10)
    font_tiny = pygame.font.SysFont("consolas", 8)
    
    # Background
    pygame.draw.rect(surface, (15, 15, 25), (x, y, width, height))
    pygame.draw.rect(surface, (100, 100, 80), (x, y, width, height), 2)
    
    # Title
    title = font_small.render("REPAIR STATUS", True, (200, 200, 100))
    surface.blit(title, (x + 10, y + 5))
    
    if submarine.repair_assignment:
        comp_name = submarine.repair_assignment
        damage = submarine.damage.get(comp_name, 0.0)
        
        t = font_small.render(f"Repairing: {comp_name}", True, (200, 200, 100))
        surface.blit(t, (x + 10, y + 23))
        
        # Progress bar
        bar_width = width - 25
        progress = max(0, 1.0 - damage)  # Inverse of damage
        bar_filled = int(bar_width * progress)
        
        pygame.draw.rect(surface, (30, 30, 30), (x + 10, y + 40, bar_width, 12))
        pygame.draw.rect(surface, (50, 150, 50), (x + 10, y + 40, bar_filled, 12))
        pygame.draw.rect(surface, (100, 100, 100), (x + 10, y + 40, bar_width, 12), 1)
        
        # Progress percentage
        pct_text = f"{progress * 100:.0f}%"
        t = font_tiny.render(pct_text, True, (150, 200, 150))
        surface.blit(t, (x + 15, y + 43))
    else:
        t = font_small.render("No repair assigned", True, (150, 150, 150))
        surface.blit(t, (x + 10, y + 23))
