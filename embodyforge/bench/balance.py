# -*- coding: utf-8 -*-
"""Balance benchmark: ZMP margin inside the support polygon.

Structural + learned: the geometric margin is fixed by the stance; the realized
margin degrades with (1 - skill) as the unskilled controller lets the ZMP drift
toward the edge. Sweeps monotonically 0.5 -> 1.0.
"""
from ..backends import get_backend
from ..core.linalg import vec3


def run_balance(cfg, backend_name="mock", n_tasks=None):
    n = n_tasks or cfg.bench.n_tasks
    backend = get_backend(backend_name, cfg)
    com = [0.0, 0.0, cfg.dynamics.com_height]
    feet = [vec3(0.06, 0.0, 0.0), vec3(-0.06, 0.0, 0.0)]
    lo = backend.balance(com, feet, skill=0.5)
    hi = backend.balance(com, feet, skill=1.0)
    return {"balance_margin_lo": lo, "balance_margin_hi": hi,
            "monotonic": hi > lo}
