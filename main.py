"""
Pacific Patrol 1941 - Entry point.
"""

import os
import pygame

from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE
from game.state_manager import StateManager
from game.screens.main_menu import MainMenuScreen
from game.sound_manager import SoundManager


def run():
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=2)

    os.makedirs("saves", exist_ok=True)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    manager = StateManager()
    manager.game_state["sound"] = SoundManager(enabled=True)
    manager.switch(MainMenuScreen())

    while manager.running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                manager.quit()
                break
            manager.handle_event(event)

        manager.update(dt)
        manager.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run()
