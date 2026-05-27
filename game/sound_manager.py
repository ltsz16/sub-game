"""
Sound manager with lightweight procedural tone generation.
"""

import math
import array
import pygame


class SoundManager:
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.sounds = {}
        if not self.enabled:
            return
        self._build_sounds()

    def _tone(self, hz=440, ms=180, vol=0.35, noise=False):
        sample_rate = 44100
        n = int(sample_rate * (ms / 1000.0))
        buf = array.array("h")
        for i in range(n):
            t = i / sample_rate
            if noise:
                # pseudo-noise from mixed harmonics
                v = (
                    math.sin(2 * math.pi * hz * t)
                    + 0.5 * math.sin(2 * math.pi * (hz * 1.9) * t)
                    + 0.25 * math.sin(2 * math.pi * (hz * 2.7) * t)
                ) / 1.75
            else:
                v = math.sin(2 * math.pi * hz * t)
            env = 1.0 - (i / n)
            sample = int(max(-1.0, min(1.0, v * env * vol)) * 32767)
            buf.append(sample)
            buf.append(sample)
        return pygame.mixer.Sound(buffer=buf.tobytes())

    def _build_sounds(self):
        self.sounds["sonar_ping"] = self._tone(1450, 220, 0.4)
        self.sounds["torpedo_fire"] = self._tone(180, 180, 0.45, noise=True)
        self.sounds["explosion"] = self._tone(90, 420, 0.55, noise=True)
        self.sounds["depth_charge"] = self._tone(70, 520, 0.6, noise=True)

    def play(self, name):
        if not self.enabled:
            return
        s = self.sounds.get(name)
        if s:
            s.play()
