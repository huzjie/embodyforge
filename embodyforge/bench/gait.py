# -*- coding: utf-8 -*-
"""Gait benchmark: walking stability = 1 - fall rate.

The oracle labels each task as a fall with probability (1 - skill), so stability
sweeps monotonically from ~0.5 (random) to 1.0 (never falls).
"""
from ..oracle import fall_label


def run_gait(cfg, n_tasks=None):
    n = n_tasks or cfg.bench.n_tasks

    def _stability(skill):
        falls = sum(1 for i in range(n) if fall_label("task:%d" % i, skill))
        return 1.0 - falls / n

    lo = _stability(0.5)
    hi = _stability(1.0)
    return {"gait_stability_lo": lo, "gait_stability_hi": hi,
            "monotonic": hi > lo}
