# -*- coding: utf-8 -*-
"""Formation: place 9 robots on a grid and report the tracking error vs skill."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from embodyforge.orchestra.formation import FormationController

f = FormationController("grid")
targets = f.targets(9)
# simulate robots lagging behind their slots
positions = [t for t in targets]
for skill in (0.5, 1.0):
    err = f.tracking_error(positions, targets, skill=skill)
    print("skill=%.1f  formation tracking error = %.3f" % (skill, err))
