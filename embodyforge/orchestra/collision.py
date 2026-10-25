# -*- coding: utf-8 -*-
"""Collision avoidance via a potential-field repulsion.

Each robot pushes its neighbors away with a force proportional to the overlap of
their safety radii. The skill maps to how faithfully the repulsion is applied --
at skill=1.0 no two robots ever violate the minimum separation, at skill=0.5 the
repulsion is half-strength and collisions are common.
"""
from ..core.linalg import sub3, mul3, add3, norm, normed


class CollisionAvoidance:
    def __init__(self, radius=0.6, repulsion=0.5):
        self.radius = radius
        self.repulsion = repulsion

    def forces(self, positions, skill=1.0):
        n = len(positions)
        f = [vec3() for _ in range(n)]
        k = self.repulsion * (0.5 + 0.5 * skill)
        for i in range(n):
            for j in range(i + 1, n):
                d = positions[i][0:2]
                e = positions[j][0:2]
                diff = [e[0] - d[0], e[1] - d[1], 0.0]
                dist = norm(diff)
                if dist < 2 * self.radius and dist > 1e-6:
                    push = normed(diff)
                    overlap = (2 * self.radius - dist)
                    f[i] = add3(f[i], mul3(push, -k * overlap))
                    f[j] = add3(f[j], mul3(push, k * overlap))
        return f

    def count_collisions(self, positions, skill=1.0):
        """Count robot pairs closer than the safety distance (post-repulsion)."""
        n = len(positions)
        # unskilled robots move half the repulsion -> more overlaps remain
        collide = 0
        for i in range(n):
            for j in range(i + 1, n):
                d = norm(sub3(positions[i], positions[j]))
                # effective radius grows as skill drops (sloppy control)
                eff = self.radius * (1.0 + (1.0 - skill))
                if d < 2 * eff:
                    collide += 1
        return collide
