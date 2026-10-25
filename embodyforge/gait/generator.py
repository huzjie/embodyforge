# -*- coding: utf-8 -*-
"""Walk-cycle generator.

Turns a gait phase into reference joint angles for the two legs. The reference
uses a simple parameterized gait: a sinusoidal hip-pitch and knee-pitch with a
swing/stance gate, which is enough to animate a stable-looking walk and to
exercise the whole FK -> ZMP -> control pipeline.
"""
import math
from .phase import GaitPhase


class WalkCycle:
    def __init__(self, cfg=None):
        from ..config import GaitConfig
        self.cfg = cfg or GaitConfig()
        self.phase = GaitPhase(self.cfg.stance_ratio)

    def _leg_angles(self, p, sign):
        # p in [0,1); sign=+1 left, -1 right (out of phase)
        hip_amp = 0.35
        knee_amp = 0.7
        # swing raises the foot: stance keeps it planted
        swing = 1.0 if p >= self.cfg.stance_ratio else 0.0
        hip_pitch = sign * hip_amp * math.sin(2 * math.pi * p)
        knee_pitch = knee_amp * swing * math.sin(2 * math.pi * p)
        # 6-DoF leg: hip_yaw, hip_roll, hip_pitch, knee_pitch, ankle_pitch, ankle_roll
        return [0.0, 0.0, hip_pitch, knee_pitch, -0.5 * hip_pitch, 0.0]

    def angles_at(self, t):
        """Return {chain_name: [angles]} for the two legs at time t."""
        p = self.phase.phase(t, self.cfg.cadence)
        pr = (p + 0.5) % 1.0
        return {
            "left_leg": self._leg_angles(p, +1.0),
            "right_leg": self._leg_angles(pr, -1.0),
        }


def generate_walk_cycle(t, cadence=1.2, stance_ratio=0.6):
    from ..config import GaitConfig
    cfg = GaitConfig(cadence=cadence, stance_ratio=stance_ratio)
    return WalkCycle(cfg).angles_at(t)
