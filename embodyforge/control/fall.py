# -*- coding: utf-8 -*-
"""Fall detection.

A biped is considered fallen when its ZMP leaves the support polygon (or, in
the point-mass model, when the CoM tilts too far). The detector flags a fall and
reports the margin. This is the safety net that lets a dancing robot stop
gracefully instead of toppling.
"""
from ..core.linalg import norm, vec3


class FallDetector:
    def __init__(self, fall_margin=0.05):
        self.fall_margin = fall_margin

    def detect(self, com, feet_positions):
        """Return (fallen: bool, margin: float)."""
        from .balance import support_polygon, _point_in_polygon
        poly = support_polygon(feet_positions)
        zmp_xy = (com[0], com[1])
        inside = _point_in_polygon(zmp_xy, poly)
        return (not inside, self.fall_margin)

    def should_stop(self, com, feet_positions):
        fallen, _ = self.detect(com, feet_positions)
        return fallen
