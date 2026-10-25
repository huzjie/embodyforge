# -*- coding: utf-8 -*-
"""Collision avoidance: count collisions among a tight cluster vs skill."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from embodyforge.orchestra.collision import CollisionAvoidance
from embodyforge.core.linalg import vec3

ca = CollisionAvoidance(0.6, 0.5)
# 8 robots packed in a tight grid
positions = [vec3(0.2 * (i % 4), 0.2 * (i // 4), 0.0) for i in range(8)]
for skill in (0.5, 1.0):
    n = ca.count_collisions(positions, skill=skill)
    print("skill=%.1f  collisions = %d" % (skill, n))
