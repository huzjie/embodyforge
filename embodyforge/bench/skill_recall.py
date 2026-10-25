# -*- coding: utf-8 -*-
"""Embodied skill-retrieval benchmark: recall@1 of the foundation model.

At skill=0.5 the correct primitive gets no boost, so the model picks among
``n_primitives`` at random (recall ~ 1/n_primitives). At skill=1.0 the correct
primitive always wins. Clean monotonic sweep.
"""
from ..embodied.foundation import EmbodiedFoundationModel
from ..data.synth import synth_tasks


def run_skill_recall(cfg, n_tasks=None):
    n = n_tasks or cfg.bench.n_tasks
    model = EmbodiedFoundationModel(cfg.embodied)
    tasks = synth_tasks(n)

    def _recall(skill):
        hits = sum(1 for t in tasks
                   if model.solve(t, skill=skill)[1])
        return hits / n

    lo = _recall(0.5)
    hi = _recall(1.0)
    return {"skill_recall_lo": lo, "skill_recall_hi": hi,
            "monotonic": hi > lo}
