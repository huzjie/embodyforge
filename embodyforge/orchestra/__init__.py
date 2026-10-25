# -*- coding: utf-8 -*-
"""Orchestration: multi-robot synchronization.

The Guinness record is as much a distributed-systems problem as a controls one:
110 robots must stay in phase, keep formation and not collide. Four primitives:

  * clock      - logical clock synchronization (NTP-style averaging).
  * phaselock  - Kuramoto oscillators converge to a common phase.
  * formation  - target-position assignment and formation tracking.
  * collision  - potential-field repulsion keeps neighbors apart.
"""
from .clock import LogicalClock, sync_clocks
from .phaselock import KuramotoLock
from .formation import FormationController
from .collision import CollisionAvoidance

__all__ = [
    "LogicalClock", "sync_clocks", "KuramotoLock",
    "FormationController", "CollisionAvoidance",
]
