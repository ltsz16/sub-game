"""
rendering/effects.py — Lightweight particle effects.
"""

import random
import pygame

from game.constants import FIRE_ORANGE, FIRE_YELLOW, SMOKE_GRAY, OCEAN_FOAM


class Particle:
    def __init__(self, x, y, vx, vy, life, color, size):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.color = color
        self.size = size

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 20 * dt
        self.life -= dt

    def draw(self, surface):
        if self.life <= 0:
            return
        alpha = max(0, min(255, int(255 * (self.life / self.max_life))))
        c = (*self.color, alpha)
        r = max(1, int(self.size * (self.life / self.max_life)))
        s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, c, (r, r), r)
        surface.blit(s, (self.x - r, self.y - r))


class ExplosionEffect:
    def __init__(self, x, y, strength=1.0):
        self.particles = []
        count = int(30 + strength * 40)
        for _ in range(count):
            ang = random.uniform(0, 6.283)
            spd = random.uniform(30, 160) * strength
            vx = spd * __import__("math").cos(ang)
            vy = spd * __import__("math").sin(ang)
            life = random.uniform(0.3, 1.1)
            color = random.choice([FIRE_ORANGE, FIRE_YELLOW, SMOKE_GRAY])
            size = random.randint(2, 5)
            self.particles.append(Particle(x, y, vx, vy, life, color, size))

    @property
    def alive(self):
        return any(p.life > 0 for p in self.particles)

    def update(self, dt):
        for p in self.particles:
            p.update(dt)

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)


class WakeEffect:
    def __init__(self):
        self.points = []

    def add_point(self, x, y):
        self.points.append((x, y, 1.0))
        if len(self.points) > 120:
            self.points.pop(0)

    def update(self, dt):
        new_pts = []
        for x, y, life in self.points:
            life -= dt * 0.7
            if life > 0:
                new_pts.append((x, y, life))
        self.points = new_pts

    def draw(self, surface):
        for x, y, life in self.points:
            a = int(200 * life)
            s = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(s, (*OCEAN_FOAM, a), (3, 3), 2)
            surface.blit(s, (x - 3, y - 3))


def draw_bubble_trail(surface, points):
    for i, (x, y) in enumerate(points[-40:]):
        a = max(40, 200 - i * 4)
        s = pygame.Surface((4, 4), pygame.SRCALPHA)
        pygame.draw.circle(s, (200, 230, 255, a), (2, 2), 1)
        surface.blit(s, (x - 2, y - 2))
