# -*- coding: utf-8 -*-
"""HumanoidRobot: robot state, FK and the whole-body forward pass.

The robot keeps joint angles for all its chains, runs forward kinematics, and
exposes the end-effector / foot positions that the dynamics and control layers
consume.
"""
from .kinematics.chain import build_humanoid_chains
from .kinematics.fk import fk_all
from .core.linalg import vec3


class HumanoidRobot:
    def __init__(self, cfg=None):
        from .config import Config
        cfg = cfg or Config()
        self.cfg = cfg
        self.chains = build_humanoid_chains()
        self.joint_angles = {name: [0.0] * c.n_dof
                             for name, c in self.chains.items()}

    def set_angles(self, name, angles):
        if name in self.joint_angles:
            self.joint_angles[name] = list(angles)

    def set_all(self, angle_map):
        for name, angles in angle_map.items():
            self.set_angles(name, angles)

    def forward(self):
        return fk_all(self.chains, self.joint_angles)

    def foot_positions(self):
        fk = self.forward()
        feet = []
        for leg in ("left_leg", "right_leg"):
            if leg in fk:
                feet.append(fk[leg][1])
        return feet

    def end_effectors(self):
        fk = self.forward()
        return {name: ee for name, (_, ee) in fk.items()}

    @property
    def n_dof(self):
        return sum(c.n_dof for c in self.chains.values())
