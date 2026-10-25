# -*- coding: utf-8 -*-
"""Footstep planning.

Generates the alternating left/right footstep positions along a heading. Each
footstep is a 3-vector on the ground (z = 0). The planner keeps the steps on a
regular grid so the ZMP preview controller has a well-defined support polygon
at every phase.
"""
from ..core.linalg import vec3
import math


class FootstepPlanner:
    def __init__(self, step_len=0.2, step_width=0.15):
        self.step_len = step_len
        self.step_width = step_width

    def plan(self, n_steps, heading=0.0):
        dx = math.cos(heading) * self.step_len
        dy = math.sin(heading) * self.step_len
        steps = []
        x = 0.0
        y = 0.0
        for i in range(n_steps):
            # alternate left/right lateral offset
            lat = self.step_width if i % 2 == 0 else -self.step_width
            # lateral offset perpendicular to heading
            px = x - math.sin(heading) * lat
            py = y + math.cos(heading) * lat
            steps.append(vec3(px, py, 0.0))
            x += dx
            y += dy
        return steps


def footstep_sequence(n_steps, step_len=0.2, heading=0.0):
    return FootstepPlanner(step_len).plan(n_steps, heading)
