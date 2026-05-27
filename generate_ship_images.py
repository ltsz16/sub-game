#!/usr/bin/env python3
"""
generate_ship_images.py - Create placeholder PNG images for all ship types.

Run this script to generate placeholder images in:
  - game/assets/images/side/ (side-view sprites)
  - game/assets/images/top/ (top-down tactical view sprites)

You can then replace these placeholders with your own custom artwork.
Images should be PNG format with transparent background (RGBA).
"""

import pygame
from game.rendering.sprites import generate_placeholder_images

if __name__ == "__main__":
    pygame.init()
    
    print("Generating placeholder ship images...")
    print("Creating: game/assets/images/side/*.png (side-view sprites)")
    print("Creating: game/assets/images/top/*.png (top-down sprites)")
    print()
    
    generate_placeholder_images()
    
    print()
    print("✓ Placeholder images created!")
    print()
    print("Next steps:")
    print("1. Review the generated PNG files in game/assets/images/")
    print("2. Edit or replace them with your own custom ship artwork")
    print("3. PNG format with transparent background recommended")
    print("4. Run 'python main.py' to see your custom images in the game")
