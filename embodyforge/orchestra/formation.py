# -*- coding: utf-8 -*-
"""Formation control.

Assigns each robot a target slot (grid / circle / line) and steers it toward that
slot with a simple proportional controller. The skill maps to the tracking
accuracy: at skill=1.0 every robot is exactly on its slot.
"""
import math
from ..core.linalg import vec3, sub3, mul3, add3, norm


def _slots(n, pattern="grid"):
    if pattern == "circle":
        r = 1.0
        return [vec3(r * math.cos(2 * math.pi * i / n),
                     r * math.sin(2 * math.pi * i / n), 0.0) for i in range(n)]
    if pattern == "line":
        return [vec3(0.0, 0.5 * (i - (n - 1) / 2.0), 0.0) for i in range(n)]
    # grid
    side = int(math.ceil(math.sqrt(n)))
    return [vec3(0.6 * (i % side), 0.6 * (i // side), 0.0) for i in range(n)]


class FormationController:
    def __init__(self, pattern="grid", gain=0.5):
        self.pattern = pattern
        self.gain = gain

    def targets(self, n):
        return _slots(n, self.pattern)

    def command(self, position, target, skill=1.0):
        err = sub3(target, position)
        # skill scales the tracking gain (unskilled robots lag behind)
        return mul3(err, self.gain * (0.5 + 0.5 * skill))

    def tracking_error(self, positions, targets, skill=1.0):
        errs = [norm(sub3(t, p)) for p, t in zip(positions, targets)]
        # residual error grows as skill drops
        return sum(e * (1.0 + (1.0 - skill)) for e in errs) / max(len(errs), 1)
