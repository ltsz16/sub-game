"""
screens/system_status_screen.py - Comprehensive system status display.

Shows all submarine systems and their operational status.
"""

import pygame
from game.state_manager import BaseScreen
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, COMPARTMENTS
from game.screens.combat_shared import update_combat_tick


class SystemStatusScreen(BaseScreen):
    def on_enter(self, manager, **kwargs):
        self.manager = manager
        self.font = pygame.font.SysFont("consolas", 12)
        self.font_small = pygame.font.SysFont("consolas", 10)
        self.font_tiny = pygame.font.SysFont("consolas", 9)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                from game.screens.nav_chart import NavChartScreen
                self.manager.switch(NavChartScreen())
            elif event.key == pygame.K_F2:
                from game.screens.periscope_view import PeriscopeViewScreen
                self.manager.switch(PeriscopeViewScreen())
            elif event.key == pygame.K_F3:
                from game.screens.bridge_view import BridgeViewScreen
                self.manager.switch(BridgeViewScreen())
            elif event.key == pygame.K_F4:
                from game.screens.damage_control_detail import DamageControlDetailScreen
                self.manager.switch(DamageControlDetailScreen())
            elif event.key == pygame.K_F5:
                from game.screens.torpedo_room import TorpedoRoomScreen
                self.manager.switch(TorpedoRoomScreen())
            elif event.key == pygame.K_ESCAPE:
                from game.screens.strategic_map import StrategicMapScreen
                self.manager.switch(StrategicMapScreen())

    def update(self, dt):
        update_combat_tick(self.manager, dt)
        
        state = self.manager.game_state.get("combat")
        if state and state["convoy"].is_destroyed:
            from game.screens.patrol_report import PatrolReportScreen
            self.manager.switch(PatrolReportScreen())

    def draw(self, surface):
        surface.fill((10, 15, 20))
        
        sub = self.manager.game_state.get("submarine")
        
        # Title
        title_font = pygame.font.SysFont("consolas", 16, bold=True)
        title = title_font.render("SYSTEM STATUS MONITOR", True, (200, 200, 100))
        surface.blit(title, (20, 15))
        
        y_pos = 50
        col1_x = 20
        col2_x = 350
        col3_x = 680
        
        # ─── PROPULSION SYSTEMS ───────────────────────────────────────────
        self._draw_section_header(surface, "PROPULSION SYSTEMS", col1_x, y_pos)
        y_pos += 25
        
        # Diesel engines
        engine_damage = sub.damage.get("Engine Room", 0.0)
        engine_status = self._get_status_text(engine_damage)
        engine_color = self._get_status_color(engine_damage)
        self._draw_system_row(surface, "Diesel Engines", engine_status, engine_color, col1_x, y_pos)
        y_pos += 22
        
        # Main battery
        battery_damage = sub.damage.get("Aft Batteries", 0.0)
        battery_status = self._get_status_text(battery_damage)
        battery_color = self._get_status_color(battery_damage)
        self._draw_system_row(surface, "Main Battery", battery_status, battery_color, col1_x, y_pos)
        y_pos += 22
        
        # Current battery level
        battery_pct = sub.battery_pct
        battery_bar_color = self._get_battery_color(battery_pct)
        self._draw_status_bar(surface, f"Battery Charge: {battery_pct * 100:.0f}%", 
                             battery_pct, battery_bar_color, col1_x, y_pos)
        y_pos += 22
        
        # ─── TORPEDO SYSTEMS ──────────────────────────────────────────────
        y_pos += 10
        self._draw_section_header(surface, "TORPEDO SYSTEMS", col1_x, y_pos)
        y_pos += 25
        
        # Fore tubes
        ready_fore = sum(1 for t in sub.tubes_fore if t.ready)
        t = self.font_small.render(f"Fore Tubes: {ready_fore}/{len(sub.tubes_fore)} ready", True, (150, 200, 100))
        surface.blit(t, (col1_x, y_pos))
        y_pos += 22
        
        # Aft tubes
        ready_aft = sum(1 for t in sub.tubes_aft if t.ready)
        t = self.font_small.render(f"Aft Tubes: {ready_aft}/{len(sub.tubes_aft)} ready", True, (150, 200, 100))
        surface.blit(t, (col1_x, y_pos))
        y_pos += 22
        
        # Torpedo count
        t = self.font_small.render(f"Torpedoes: {sub.torpedo_count} loaded", True, (150, 200, 100))
        surface.blit(t, (col1_x, y_pos))
        y_pos += 22
        
        # ─── SONAR & DETECTION ────────────────────────────────────────────
        y_pos += 10
        self._draw_section_header(surface, "SONAR & DETECTION", col1_x, y_pos)
        y_pos += 25
        
        sonar_status = "PASSIVE" if sub.silent_running else "ACTIVE"
        sonar_color = (150, 150, 50) if sub.silent_running else (100, 200, 100)
        self._draw_system_row(surface, "Sonar Mode", sonar_status, sonar_color, col1_x, y_pos)
        y_pos += 22
        
        radar_status = "ACTIVE" if sub.radar_on else "INACTIVE"
        radar_color = (100, 200, 100) if sub.radar_on else (100, 100, 100)
        self._draw_system_row(surface, "Radar", radar_status, radar_color, col1_x, y_pos)
        y_pos += 22
        
        periscope_status = "UP" if sub.periscope_up else "DOWN"
        periscope_color = (100, 200, 100) if sub.periscope_up else (100, 100, 100)
        self._draw_system_row(surface, "Periscope", periscope_status, periscope_color, col1_x, y_pos)
        
        # ─── COLUMN 2: HULL & COMPARTMENTS ────────────────────────────────
        y_pos = 50
        self._draw_section_header(surface, "HULL INTEGRITY", col2_x, y_pos)
        y_pos += 25
        
        # Overall integrity
        integrity = sub.hull_integrity
        integrity_pct = integrity * 100
        integrity_color = (200, 100, 100) if integrity < 0.5 else (200, 150, 50) if integrity < 0.8 else (100, 200, 100)
        self._draw_status_bar(surface, f"Overall: {integrity_pct:.1f}%", 
                             integrity, integrity_color, col2_x, y_pos)
        y_pos += 25
        
        # Critical systems health
        self._draw_section_header(surface, "CRITICAL COMPARTMENTS", col2_x, y_pos)
        y_pos += 25
        
        critical_comps = ["Engine Room", "Aft Batteries", "Forward Torpedo Room", "Control Room"]
        for comp in critical_comps:
            if comp in COMPARTMENTS:
                damage = sub.damage.get(comp, 0.0)
                flooding = sub.flooding.get(comp, 0.0)
                status = self._get_compartment_status(damage, flooding)
                color = self._get_status_color(damage) if damage > 0 else self._get_status_color(flooding * 0.5)
                
                status_line = f"{comp}: {status}"
                if flooding > 0:
                    status_line += f" (Flood: {flooding * 100:.0f}%)"
                
                t = self.font_small.render(status_line, True, color)
                surface.blit(t, (col2_x, y_pos))
                y_pos += 20
        
        # ─── COLUMN 3: RESOURCES & STATUS ─────────────────────────────────
        y_pos = 50
        self._draw_section_header(surface, "RESOURCES", col3_x, y_pos)
        y_pos += 25
        
        # Fuel
        fuel_pct = sub.fuel_pct
        fuel_color = (200, 100, 100) if fuel_pct < 0.2 else (200, 150, 50) if fuel_pct < 0.5 else (100, 150, 200)
        self._draw_status_bar(surface, f"Fuel: {fuel_pct * 100:.0f}%", 
                             fuel_pct, fuel_color, col3_x, y_pos)
        y_pos += 25
        
        # Crew
        crew_healthy = sub.crew - sub.crew_casualties
        crew_pct = crew_healthy / max(1, sub.crew)
        crew_color = (200, 50, 50) if sub.crew_casualties > 5 else (200, 150, 50) if sub.crew_casualties > 0 else (100, 200, 100)
        self._draw_status_bar(surface, f"Crew: {crew_healthy}/{sub.crew}", 
                             crew_pct, crew_color, col3_x, y_pos)
        y_pos += 25
        
        # Decoys
        t = self.font_small.render(f"Decoys: {sub.decoys}", True, (150, 200, 150))
        surface.blit(t, (col3_x, y_pos))
        y_pos += 22
        
        # ─── OPERATIONAL STATUS ───────────────────────────────────────────
        y_pos += 10
        self._draw_section_header(surface, "OPERATIONAL STATUS", col3_x, y_pos)
        y_pos += 25
        
        # Submersion state
        sub_state = "SURFACED" if sub.surfaced else "SUBMERGED"
        sub_color = (100, 150, 200) if sub.surfaced else (150, 100, 200)
        t = self.font_small.render(f"State: {sub_state}", True, sub_color)
        surface.blit(t, (col3_x, y_pos))
        y_pos += 20
        
        # Depth mode
        from game.constants import DEPTH_PERISCOPE, DEPTH_SHALLOW
        if sub.depth <= DEPTH_PERISCOPE and not sub.surfaced:
            mode = "PERISCOPE"
            mode_color = (100, 200, 100)
        elif sub.depth <= DEPTH_SHALLOW:
            mode = "SHALLOW"
            mode_color = (200, 200, 100)
        elif sub.depth >= sub.spec["max_depth"] - 50:
            mode = "CRUSH DEPTH!"
            mode_color = (200, 50, 50)
        else:
            mode = "DEEP"
            mode_color = (100, 150, 200)
        
        t = self.font_small.render(f"Depth Mode: {mode}", True, mode_color)
        surface.blit(t, (col3_x, y_pos))
        y_pos += 20
        
        # Silent running
        silent_text = "SILENT RUNNING ACTIVE" if sub.silent_running else "Normal operations"
        silent_color = (150, 150, 50) if sub.silent_running else (100, 100, 100)
        t = self.font_small.render(silent_text, True, silent_color)
        surface.blit(t, (col3_x, y_pos))
        
        # Bottom instructions
        instructions = "F1-F5: Switch views | Esc: Map"
        t = self.font_small.render(instructions, True, (100, 100, 100))
        surface.blit(t, (20, SCREEN_HEIGHT - 20))

    def _draw_section_header(self, surface: pygame.Surface, title: str, x: int, y: int):
        """Draw a section header with line."""
        t = self.font.render(title, True, (200, 200, 100))
        surface.blit(t, (x, y))
        pygame.draw.line(surface, (100, 100, 80), (x + 200, y + 12), (x + 280, y + 12), 1)

    def _draw_system_row(self, surface: pygame.Surface, system_name: str, 
                        status: str, color: tuple, x: int, y: int):
        """Draw a system status row."""
        name_text = self.font_small.render(f"{system_name}: ", True, (150, 150, 150))
        surface.blit(name_text, (x, y))
        
        status_text = self.font_small.render(status, True, color)
        surface.blit(status_text, (x + 150, y))

    def _draw_status_bar(self, surface: pygame.Surface, label: str, 
                        value: float, color: tuple, x: int, y: int):
        """Draw a labeled status bar."""
        t = self.font_small.render(label, True, (150, 150, 150))
        surface.blit(t, (x, y))
        
        bar_width = 150
        bar_height = 12
        bar_x = x + 120
        bar_y = y
        
        pygame.draw.rect(surface, (30, 30, 30), (bar_x, bar_y, bar_width, bar_height))
        filled_width = int(bar_width * max(0, min(1, value)))
        pygame.draw.rect(surface, color, (bar_x, bar_y, filled_width, bar_height))
        pygame.draw.rect(surface, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height), 1)

    def _get_status_text(self, damage: float) -> str:
        """Get status text based on damage."""
        if damage >= 1.0:
            return "DESTROYED"
        elif damage >= 0.75:
            return "CRITICAL"
        elif damage >= 0.5:
            return "DAMAGED"
        elif damage >= 0.25:
            return "WARN"
        else:
            return "OPERATIONAL"

    def _get_status_color(self, damage: float) -> tuple:
        """Get color based on damage."""
        if damage >= 1.0:
            return (200, 50, 50)
        elif damage >= 0.75:
            return (200, 100, 50)
        elif damage >= 0.5:
            return (200, 150, 50)
        elif damage >= 0.25:
            return (200, 200, 50)
        else:
            return (100, 200, 100)

    def _get_battery_color(self, pct: float) -> tuple:
        """Get color based on battery percentage."""
        if pct > 0.5:
            return (50, 200, 50)
        elif pct > 0.25:
            return (200, 200, 50)
        else:
            return (200, 50, 50)

    def _get_compartment_status(self, damage: float, flooding: float) -> str:
        """Get compartment status text."""
        if damage >= 0.75:
            return "CRITICAL"
        elif flooding > 0.5:
            return "FLOODED"
        elif flooding > 0:
            return "LEAKING"
        elif damage > 0:
            return "DAMAGED"
        else:
            return "OK"
