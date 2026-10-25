# -*- coding: utf-8 -*-
"""EmbodiedModel: the whole-body model that ties robot + control + gait together.

This is the reference "brain": it runs one control step -- pick the walk-cycle
or dance pose for the current time, run FK, estimate CoM/ZMP, command balance
and detect falls. Declared scale (110 robots, 40 DoF) lives in ``Config.declared``.
"""
from .robot import HumanoidRobot
from .dynamics.com import center_of_mass
from .gait.generator import WalkCycle
from .choreo.dance import build_dance_routine
from .control.balance import ZMPPreviewController
from .control.fall import FallDetector


class EmbodiedModel:
    def __init__(self, cfg=None):
        from .config import Config
        self.cfg = cfg or Config()
        self.robot = HumanoidRobot(self.cfg)
        self.walk = WalkCycle(self.cfg.gait)
        self.dance = build_dance_routine()
        self.balance = ZMPPreviewController(self.cfg.control)
        self.fall = FallDetector(self.cfg.control.fall_margin)

    def step(self, t, skill=1.0):
        """One control step at time t. Returns a dict of state."""
        self.robot.set_all(self.walk.angles_at(t))
        feet = self.robot.foot_positions()
        fk = self.robot.forward()
        com = center_of_mass({
            "torso": [0.0, 0.0, self.cfg.dynamics.com_height],
            "feet": feet,
            "masses": {"torso": self.cfg.dynamics.mass_kg, "foot": 1.0},
        })
        margin = self.balance.margin(com, [0.0, 0.0, 0.0], feet, skill=skill)
        fallen, _ = self.fall.detect(com, feet)
        return {
            "time": t, "com": com, "feet": feet,
            "balance_margin": margin, "fallen": fallen,
            "n_dof": self.robot.n_dof,
        }

    def n_params(self):
        """Declared parameter/dof count (informational)."""
        return self.cfg.declared.n_robots * self.cfg.declared.dof_per_robot
