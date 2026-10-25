# -*- coding: utf-8 -*-
"""Synchronization benchmark: Kuramoto order parameter.

Higher skill = stronger coupling = faster and tighter phase-locking. The order
parameter r -> 1 as the swarm locks. Sweeps monotonically 0.5 -> 1.0.
"""
from ..orchestra.phaselock import KuramotoLock
from ..config import OrchestraConfig


def run_sync(cfg, n_robots=None, steps=60):
    n = n_robots or cfg.orchestra.n_robots
    oc = OrchestraConfig()

    def _order(skill):
        lock = KuramotoLock(n, coupling=oc.coupling)
        for _ in range(steps):
            lock.step(dt=0.05, skill=skill)
        return lock.order_parameter()

    lo = _order(0.5)
    hi = _order(1.0)
    return {"sync_order_lo": lo, "sync_order_hi": hi, "monotonic": hi > lo}
