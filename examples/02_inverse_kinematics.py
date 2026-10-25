# -*- coding: utf-8 -*-
"""Solve IK to place the left foot at a target and report the residual."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from embodyforge.kinematics.chain import build_humanoid_chains
from embodyforge.kinematics.fk import fk_chain
from embodyforge.kinematics.ik import ik_chain
from embodyforge.core.linalg import norm, sub3

leg = build_humanoid_chains()["left_leg"]
target = [0.35, 0.0, -0.9]
q = ik_chain(leg, target)
_, ee = fk_chain(leg, q or [0.0] * leg.n_dof)
print("target:", target)
print("solved angles:", [round(a, 3) for a in (q or [])])
print("end-effector:", [round(x, 4) for x in ee])
print("residual: %.4f m" % norm(sub3(ee, target)))
