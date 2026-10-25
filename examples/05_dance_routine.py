# -*- coding: utf-8 -*-
"""Play a beat-synchronized dance routine and sample poses."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from embodyforge.choreo.dance import build_dance_routine

d = build_dance_routine(120.0)
print("routine: %d clips, %.2fs, %d beats" % (len(d.schedule), d.duration(), d.total_beats()))
for i in range(7):
    t = d.duration() * i / 6.0
    name, local = d.clip_at(t)
    pose = d.pose_at(t)
    print("t=%.2fs  clip=%-10s local=%.2f  pose_keys=%d" % (t, name, local, len(pose)))
