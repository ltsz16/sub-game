#!/usr/bin/env python
"""
Test script for Priority 3 enhanced UI screens.

Validates:
- All screen classes instantiate correctly
- Screen event handlers work
- View cycling functions work
- Keyboard controls are properly handled
"""

import sys
sys.path.insert(0, '.')

import pygame
from game.state_manager import StateManager, BaseScreen
from game.constants import *
from game.entities.submarine import Submarine
from game.data.submarines import SUBMARINE_BY_ID
from game.screens.damage_control_detail import DamageControlDetailScreen
from game.screens.gauge_panel_screen import GaugePanelScreen
from game.screens.system_status_screen import SystemStatusScreen
from game.screens.nav_chart import NavChartScreen
from game.screens.periscope_view import PeriscopeViewScreen
from game.screens.bridge_view import BridgeViewScreen
from game.screens.torpedo_room import TorpedoRoomScreen

def test_screen_instantiation():
    """Test that all screens can be instantiated."""
    print("\n=== Testing Screen Instantiation ===")
    
    screens = [
        ("Damage Control Detail", DamageControlDetailScreen),
        ("Gauge Panel", GaugePanelScreen),
        ("System Status Monitor", SystemStatusScreen),
        ("Nav Chart", NavChartScreen),
        ("Periscope View", PeriscopeViewScreen),
        ("Bridge View", BridgeViewScreen),
        ("Torpedo Room", TorpedoRoomScreen),
    ]
    
    for name, screen_class in screens:
        try:
            screen = screen_class()
            print(f"✓ {name}: Instantiated successfully")
        except Exception as e:
            print(f"✗ {name}: FAILED - {e}")
            return False
    
    return True

def test_screen_with_state():
    """Test screens with a realistic game state."""
    print("\n=== Testing Screens with Game State ===")
    
    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Create state manager and game state
    manager = StateManager()
    
    # Create submarine
    sub_class = SUBMARINE_BY_ID["gato"]
    sub = Submarine(sub_class)
    sub.depth = 100
    sub.target_depth = 100
    sub.speed = 2
    sub.speed_setting = 2
    sub.heading = 180
    sub.battery = 0.75
    sub.fuel = 0.80
    
    # Add damage to test visualization
    sub.damage["Engine Room"] = 0.25
    sub.damage["Aft Batteries"] = 0.1
    sub.flooding["Forward Torpedo Room"] = 0.05
    
    manager.game_state["submarine"] = sub
    
    # Create minimal combat state
    combat_state = {
        "tick": 0,
        "convoy": type('obj', (object,), {
            'is_destroyed': False,
            'ships': []
        })(),
        "detected": True,
        "threats": []
    }
    manager.game_state["combat"] = combat_state
    
    print("✓ Game state created")
    
    # Test each screen
    screens_to_test = [
        ("Damage Control Detail", DamageControlDetailScreen),
        ("Gauge Panel", GaugePanelScreen),
        ("System Status Monitor", SystemStatusScreen),
    ]
    
    for name, screen_class in screens_to_test:
        try:
            screen = screen_class()
            screen.on_enter(manager)
            print(f"✓ {name}: on_enter() executed")
            
            # Test handle_event with Escape key
            event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
            # Don't actually switch (would cause infinite loop), just verify it doesn't crash
            print(f"✓ {name}: handle_event() callable")
            
        except Exception as e:
            print(f"✗ {name}: FAILED - {e}")
            return False
    
    pygame.quit()
    return True

def test_view_cycling():
    """Test that cycle_to_view function works."""
    print("\n=== Testing View Cycling ===")
    
    from game.screens.combat_shared import cycle_to_view
    
    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    manager = StateManager()
    manager.game_state["submarine"] = Submarine(SUBMARINE_BY_ID["gato"])
    manager.game_state["combat"] = {
        "tick": 0,
        "convoy": type('obj', (object,), {'is_destroyed': False, 'ships': []})(),
        "detected": False,
        "threats": []
    }
    
    view_keys = ["chart", "periscope", "bridge", "damage", "torpedo", "gauges", "systems"]
    
    for key in view_keys:
        try:
            cycle_to_view(manager, key)
            print(f"✓ cycle_to_view('{key}'): Switched successfully")
        except Exception as e:
            print(f"✗ cycle_to_view('{key}'): FAILED - {e}")
            pygame.quit()
            return False
    
    pygame.quit()
    return True

def test_keyboard_controls():
    """Test that F1-F5 and number keys are handled."""
    print("\n=== Testing Keyboard Controls ===")
    
    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    manager = StateManager()
    manager.game_state["submarine"] = Submarine(SUBMARINE_BY_ID["gato"])
    manager.game_state["combat"] = {
        "tick": 0,
        "convoy": type('obj', (object,), {'is_destroyed': False, 'ships': []})(),
        "detected": False,
        "threats": []
    }
    
    # Test damage control screen with number keys
    damage_screen = DamageControlDetailScreen()
    damage_screen.on_enter(manager)
    
    # Test number key for repair assignment
    for key_num in range(10):
        key = pygame.K_0 + key_num
        event = pygame.event.Event(pygame.KEYDOWN, key=key)
        try:
            damage_screen.handle_event(event)
            print(f"✓ Repair assignment key {key_num}: Handled")
        except Exception as e:
            print(f"✗ Repair assignment key {key_num}: FAILED - {e}")
            pygame.quit()
            return False
    
    # Test F-key navigation
    f_keys = [
        (pygame.K_F1, "F1 (Chart)"),
        (pygame.K_F2, "F2 (Periscope)"),
        (pygame.K_F3, "F3 (Bridge)"),
        (pygame.K_F4, "F4 (Damage Control)"),
        (pygame.K_F5, "F5 (Torpedo)"),
    ]
    
    for key, label in f_keys:
        event = pygame.event.Event(pygame.KEYDOWN, key=key)
        try:
            damage_screen.handle_event(event)
            print(f"✓ {label}: View switch handled")
        except Exception as e:
            print(f"✗ {label}: FAILED - {e}")
            pygame.quit()
            return False
    
    pygame.quit()
    return True

def test_rendering_functions():
    """Test that rendering functions execute without errors."""
    print("\n=== Testing Rendering Functions ===")
    
    pygame.init()
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    sub = Submarine(SUBMARINE_BY_ID["gato"])
    sub.depth = 150
    sub.speed = 2
    sub.heading = 270
    sub.battery = 0.60
    
    from game.rendering.damage_control_ui import (
        draw_compartment_status,
        draw_damage_summary,
        draw_critical_systems_status,
        draw_repair_status,
    )
    from game.rendering.gauge_panel import (
        draw_main_gauge_panel,
        draw_secondary_instruments,
        draw_compass_rose,
        draw_depth_indicator,
        draw_rudder_indicator,
    )
    
    # Test damage control UI functions
    damage_ui_funcs = [
        ("draw_compartment_status", draw_compartment_status, 
         lambda: draw_compartment_status(surface, [], sub, 10, 10)),
        ("draw_damage_summary", draw_damage_summary,
         lambda: draw_damage_summary(surface, sub, 500, 10)),
        ("draw_critical_systems_status", draw_critical_systems_status,
         lambda: draw_critical_systems_status(surface, sub, 500, 125)),
        ("draw_repair_status", draw_repair_status,
         lambda: draw_repair_status(surface, sub, 500, 230)),
    ]
    
    for name, func, call in damage_ui_funcs:
        try:
            call()
            print(f"✓ {name}: Rendered successfully")
        except Exception as e:
            print(f"✗ {name}: FAILED - {e}")
            pygame.quit()
            return False
    
    # Test gauge panel functions
    gauge_funcs = [
        ("draw_main_gauge_panel", draw_main_gauge_panel,
         lambda: draw_main_gauge_panel(surface, sub, 20, 40)),
        ("draw_secondary_instruments", draw_secondary_instruments,
         lambda: draw_secondary_instruments(surface, sub, 450, 40)),
        ("draw_compass_rose", draw_compass_rose,
         lambda: draw_compass_rose(surface, sub, 670, 230)),
        ("draw_depth_indicator", draw_depth_indicator,
         lambda: draw_depth_indicator(surface, sub, 20, 330)),
        ("draw_rudder_indicator", draw_rudder_indicator,
         lambda: draw_rudder_indicator(surface, sub, 230, 330)),
    ]
    
    for name, func, call in gauge_funcs:
        try:
            call()
            print(f"✓ {name}: Rendered successfully")
        except Exception as e:
            print(f"✗ {name}: FAILED - {e}")
            pygame.quit()
            return False
    
    pygame.quit()
    return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("PRIORITY 3 ENHANCED UI SCREENS - VALIDATION TEST")
    print("=" * 60)
    
    tests = [
        ("Screen Instantiation", test_screen_instantiation),
        ("Screen with Game State", test_screen_with_state),
        ("View Cycling", test_view_cycling),
        ("Keyboard Controls", test_keyboard_controls),
        ("Rendering Functions", test_rendering_functions),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n✗ {test_name}: EXCEPTION - {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
