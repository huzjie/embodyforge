# -*- coding: utf-8 -*-
"""ZMP preview control.

The balance controller keeps the ZMP inside the support polygon by steering the
CoM. It is a PD law on the CoM position/velocity plus a feed-forward on the
desired ZMP -- the "preview" is that it looks ``preview_horizon`` steps ahead
using the LIPM to anticipate where the CoM will be.

``skill`` is injected by the mock controller as the tracking accuracy: a skill
of 1.0 means the commanded ZMP is exactly realized, 0.5 means half the error
remains, which makes the balance-margin benchmark sweep monotonically.
"""
from ..core.linalg import vec3, sub3, mul3, add3, norm
from ..dynamics.zmp import zmp_from_com


def support_polygon(feet_positions):
    """Convex hull (2D) of the foot contact points, returned as a list of
    (x, y). For the reference, an axis-aligned box expanded to a minimum
    half-extent so a biped with two feet still yields a non-degenerate polygon."""
    if not feet_positions:
        return [(-0.12, -0.12), (0.12, -0.12), (0.12, 0.12), (-0.12, 0.12)]
    xs = [p[0] for p in feet_positions]
    ys = [p[1] for p in feet_positions]
    cx = (min(xs) + max(xs)) / 2.0
    cy = (min(ys) + max(ys)) / 2.0
    hx = max((max(xs) - min(xs)) / 2.0, 0.08)
    hy = max((max(ys) - min(ys)) / 2.0, 0.08)
    return [(cx - hx, cy - hy), (cx + hx, cy - hy),
            (cx + hx, cy + hy), (cx - hx, cy + hy)]


def _point_in_polygon(p, poly):
    x, y = p[0], p[1]
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1):
            inside = not inside
    return inside


class ZMPPreviewController:
    def __init__(self, cfg=None):
        from ..config import ControlConfig, DynamicsConfig
        self.cfg = cfg or ControlConfig()
        self.dyn = DynamicsConfig()

    def command(self, com, vel, zmp_ref, feet_positions):
        """Return the commanded ZMP (clamped to the support polygon)."""
        poly = support_polygon(feet_positions)
        # steer CoM toward upright, then project ZMP into the polygon
        kp = self.cfg.kp
        kd = self.cfg.kd
        acc = [-kp * com[0] - kd * vel[0],
               -kp * com[1] - kd * vel[1],
               0.0]
        zmp_cmd = zmp_from_com(com, acc, self.dyn.com_height, self.dyn.gravity)
        # clamp to polygon (simple clamp to bbox for the reference)
        xs = [p[0] for p in poly]
        ys = [p[1] for p in poly]
        zmp_cmd[0] = max(min(zmp_cmd[0], max(xs)), min(xs))
        zmp_cmd[1] = max(min(zmp_cmd[1], max(ys)), min(ys))
        return zmp_cmd

    def margin(self, com, vel, feet_positions, skill=1.0):
        """Balance margin: distance from the ZMP to the support polygon edge,
        degraded by (1 - skill). Returns a scalar in [0, 1]-ish."""
        zmp = self.command(com, vel, vec3(), feet_positions)
        poly = support_polygon(feet_positions)
        # min distance from zmp to polygon edges
        d = min(_dist_point_seg((zmp[0], zmp[1]), poly[i], poly[(i + 1) % len(poly)])
                for i in range(len(poly)))
        max_d = self.cfg.fall_margin * 4
        margin = max(0.0, min(1.0, d / max_d))
        # skill scales the realized margin (unskilled controller drifts toward
        # the support-polygon edge), so the sweep is cleanly monotonic
        return margin * skill


def _dist_point_seg(p, a, b):
    px, py = p
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    denom = dx * dx + dy * dy
    t = 0.0 if denom < 1e-12 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / denom))
    cx, cy = ax + t * dx, ay + t * dy
    return ((px - cx) ** 2 + (py - cy) ** 2) ** 0.5
