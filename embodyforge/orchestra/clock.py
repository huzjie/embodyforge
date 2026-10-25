# -*- coding: utf-8 -*-
"""Logical clock synchronization.

Robots do not share a physical clock, so each keeps a logical clock with an
offset and a drift. ``sync_clocks`` runs NTP-style averaging rounds: each robot
adopts the mean offset of its peers, which makes all clocks converge to a common
time reference -- the prerequisite for beat-synchronized dancing.
"""
from ..utils.random import stable_float


class LogicalClock:
    def __init__(self, offset=0.0, drift=1.0, name="robot"):
        self.offset = offset
        self.drift = drift
        self.name = name

    def now(self, real_time):
        return self.drift * real_time + self.offset


def sync_clocks(clocks, rounds=5, coupling=0.5):
    """Average-offset synchronization. Returns the final clocks (in place)."""
    for _ in range(rounds):
        mean_off = sum(c.offset for c in clocks) / max(len(clocks), 1)
        for c in clocks:
            c.offset += coupling * (mean_off - c.offset)
    return clocks


def make_robot_clocks(n, seed="clk"):
    return [LogicalClock(offset=stable_float("%s:%d" % (seed, i), -0.5, 0.5),
                         drift=stable_float("%s:d:%d" % (seed, i), 0.99, 1.01),
                         name="robot_%d" % i)
            for i in range(n)]
