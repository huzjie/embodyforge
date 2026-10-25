# -*- coding: utf-8 -*-
"""Gait phase: a periodic scalar in [0, 1) plus swing/stance classification.

The phase is the fundamental clock of the walk cycle. ``stance_ratio`` controls
how much of the cycle each foot spends on the ground (stance) versus swinging
forward (swing).
"""
import math


class GaitPhase:
    def __init__(self, stance_ratio=0.6):
        self.stance_ratio = stance_ratio

    def phase(self, t, cadence=1.2):
        return (t * cadence) % 1.0

    def is_stance(self, t, cadence=1.2, foot="left"):
        p = self.phase(t, cadence)
        # left and right are half a cycle out of phase
        if foot == "right":
            p = (p + 0.5) % 1.0
        return p < self.stance_ratio


def phase_from_time(t, cadence=1.2):
    return (t * cadence) % 1.0
