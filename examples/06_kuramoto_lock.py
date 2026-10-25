# -*- coding: utf-8 -*-
"""Kuramoto phase-locking: order parameter vs skill."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from embodyforge.orchestra.phaselock import KuramotoLock

for skill in (0.5, 1.0):
    lock = KuramotoLock(8, coupling=0.3)
    for _ in range(40):
        lock.step(dt=0.05, skill=skill)
    print("skill=%.1f  order parameter r=%.4f  phase_error=%.4f rad" % (
        skill, lock.order_parameter(), lock.phase_error()))
