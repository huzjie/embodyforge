# -*- coding: utf-8 -*-
"""Benchmarks. Each returns a dict of metrics; learning metrics are monotonic
in skill (random baseline at 0.5 -> optimum at 1.0)."""
from .balance import run_balance
from .sync import run_sync
from .gait import run_gait
from .skill_recall import run_skill_recall
from .speedup import run_speedup
from .run import run_all

__all__ = [
    "run_balance", "run_sync", "run_gait", "run_skill_recall",
    "run_speedup", "run_all",
]
