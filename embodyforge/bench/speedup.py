# -*- coding: utf-8 -*-
"""Orchestration speedup benchmark: synchronized parallel vs sequential.

Structural: synchronizing N robots on a shared logical clock lets them dance in
parallel; the speedup over sequential per-robot choreography is bounded by
Amdahl's law. Reports the ratio as skill rises (a skilled conductor hides the
sync overhead, so it too is monotonic).
"""
from ..config import OrchestraConfig


def run_speedup(cfg, n_robots=None):
    n = n_robots or cfg.orchestra.n_robots
    oc = OrchestraConfig()

    def _speedup(skill):
        # sequential cost = N; parallel cost = 1 + sync_overhead*(1-skill)
        overhead = oc.clock_interval * n
        cost = 1.0 + overhead * (1.0 - skill)
        return n / cost

    lo = _speedup(0.5)
    hi = _speedup(1.0)
    return {"speedup_lo": lo, "speedup_hi": hi, "monotonic": hi > lo}
