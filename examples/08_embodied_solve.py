# -*- coding: utf-8 -*-
"""Embodied foundation model: solve tasks at different skills."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from embodyforge.embodied.foundation import EmbodiedFoundationModel
from embodyforge.data.synth import synth_tasks

model = EmbodiedFoundationModel()
tasks = synth_tasks(50)
for skill in (0.5, 0.75, 1.0):
    hits = sum(1 for t in tasks if model.solve(t, skill=skill)[1])
    print("skill=%.2f  recall@1 = %.3f (%d/%d)" % (skill, hits / len(tasks), hits, len(tasks)))
