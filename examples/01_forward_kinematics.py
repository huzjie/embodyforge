# -*- coding: utf-8 -*-
"""Walk the left leg with zero angles and print the end-effector position."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from embodyforge.kinematics.chain import build_humanoid_chains
from embodyforge.kinematics.fk import fk_chain

chains = build_humanoid_chains()
leg = chains["left_leg"]
_, ee = fk_chain(leg, [0.0] * leg.n_dof)
print("left_leg end-effector (neutral):", [round(x, 4) for x in ee])
print("expected: [0.08, 0.0, -1.3] (hip 0.08/-0.5, thigh 0.4, shin 0.4)")
