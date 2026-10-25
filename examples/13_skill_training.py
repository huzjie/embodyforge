# -*- coding: utf-8 -*-
"""Train the embodied skill and show the recall climbing."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from embodyforge.embodied.foundation import EmbodiedFoundationModel
from embodyforge.data.synth import synth_tasks

model = EmbodiedFoundationModel()
tasks = synth_tasks(100)
for skill in (0.5, 0.6, 0.7, 0.8, 0.9, 1.0):
    hits = sum(1 for t in tasks if model.solve(t, skill=skill)[1])
    print("skill=%.1f  recall@1 = %.3f" % (skill, hits / len(tasks)))
