"""
systems/tdc.py — Torpedo Data Computer.

The TDC computes the correct gyro angle to send to the torpedo so it leads
the target and intercepts it.

Lead angle formula (simplified):
    sin(gyro_angle) = (v_target / v_torpedo) * sin(angle_on_bow)

Where:
    v_target     = target speed in knots
    v_torpedo    = torpedo speed in knots
    angle_on_bow = angle between target's course and bearing from sub to target
                   (0° = target heading toward you, 180° = away)

The result gyro_angle is added to the bearing to get the torpedo course.
"""

import math


class TDC:
    """Torpedo Data Computer — computes firing solution."""

    def __init__(self):
        # Inputs (set by player)
        self.target_bearing: float  = 0.0    # degrees, bearing to target from sub
        self.target_range:   float  = 2.0    # nautical miles
        self.target_speed:   float  = 10.0   # knots
        self.angle_on_bow:   float  = 90.0   # degrees (0=head-on, 90=beam, 180=tail)
        self.torp_speed:     float  = 46.0   # torpedo speed setting

        # Computed outputs
        self.gyro_angle:     float  = 0.0    # degrees to offset torpedo course
        self.torpedo_course: float  = 0.0    # absolute course for torpedo
        self.solution_quality: float = 0.0   # 0.0–1.0 (1.0=perfect)
        self.time_to_impact:  float  = 0.0   # seconds

        # Tracking errors (simulate imperfect data)
        self._bearing_error: float  = 0.0
        self._speed_error:   float  = 0.0

    def set_bearing(self, bearing: float):
        self.target_bearing = bearing % 360
        self._recalculate()

    def set_range(self, range_nm: float):
        self.target_range = max(0.1, range_nm)
        self._recalculate()

    def set_target_speed(self, speed: float):
        self.target_speed = max(0.0, min(40.0, speed))
        self._recalculate()

    def set_angle_on_bow(self, aob: float):
        self.angle_on_bow = aob % 360
        self._recalculate()

    def set_torp_speed(self, high: bool):
        from game.entities.torpedo import Torpedo
        self.torp_speed = Torpedo.SPEED_HIGH if high else Torpedo.SPEED_LOW
        self._recalculate()

    def update_from_target(self, sub_lon: float, sub_lat: float,
                           sub_course: float,
                           target_lon: float, target_lat: float,
                           target_course: float, target_speed: float):
        """Auto-update TDC from known target data (for training/easy mode)."""
        # Calculate bearing and range
        dlon = (target_lon - sub_lon) * math.cos(math.radians(sub_lat)) * 60.0
        dlat = (target_lat - sub_lat) * 60.0
        self.target_range   = math.sqrt(dlon**2 + dlat**2)
        self.target_bearing = math.degrees(math.atan2(dlon, dlat)) % 360
        self.target_speed   = target_speed

        # AoB: angle between target course and bearing from target to sub
        bearing_from_target = (self.target_bearing + 180) % 360
        self.angle_on_bow   = (target_course - bearing_from_target + 360) % 360
        self._recalculate()

    def _recalculate(self):
        """Recompute gyro angle from current inputs."""
        aob_rad = math.radians(self.angle_on_bow)
        ratio   = (self.target_speed / max(1.0, self.torp_speed)) * math.sin(aob_rad)
        # Clamp to valid domain for arcsin
        ratio   = max(-1.0, min(1.0, ratio))
        self.gyro_angle     = math.degrees(math.asin(ratio))
        self.torpedo_course = (self.target_bearing + self.gyro_angle) % 360

        # Time to impact (approximate: straight-line intercept)
        if self.target_range > 0 and self.torp_speed > 0:
            # Simplified: range / torpedo speed
            torp_nm_per_s = self.torp_speed / 3600.0
            self.time_to_impact = self.target_range / torp_nm_per_s
        else:
            self.time_to_impact = 999.0

        # Solution quality: how good is our data?
        # Degrades with long range and poor angle-on-bow estimate
        range_factor  = max(0.0, 1.0 - self.target_range / 6.0)
        # Best AoB is 90 degrees (beam shot, easiest lead angle)
        aob_factor    = math.sin(aob_rad) ** 0.5
        self.solution_quality = min(1.0, range_factor * 0.5 + aob_factor * 0.5)

    def get_torpedo_course(self) -> float:
        return self.torpedo_course

    def display_dict(self) -> dict:
        return {
            "Bearing":     f"{self.target_bearing:5.1f}°",
            "Range":       f"{self.target_range:5.2f} nm",
            "Tgt Speed":   f"{self.target_speed:4.1f} kts",
            "AoB":         f"{self.angle_on_bow:5.1f}°",
            "Gyro Angle":  f"{self.gyro_angle:+5.1f}°",
            "Torp Course": f"{self.torpedo_course:5.1f}°",
            "Time":        f"{self.time_to_impact:5.0f}s",
            "Quality":     f"{self.solution_quality*100:3.0f}%",
        }
