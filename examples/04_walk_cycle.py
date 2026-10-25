# -*- coding: utf-8 -*-
"""Print leg angles over one walk cycle."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from embodyforge.gait.generator import WalkCycle

w = WalkCycle()
print("time   left_hip_pitch  left_knee_pitch  right_hip_pitch  right_knee_pitch")
for i in range(8):
    t = i / 8.0
    a = w.angles_at(t)
    l, r = a["left_leg"], a["right_leg"]
    print("%.2f   %+.3f          %+.3f           %+.3f            %+.3f" % (
        t, l[2], l[3], r[2], r[3]))
