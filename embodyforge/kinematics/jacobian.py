# -*- coding: utf-8 -*-
"""Numeric Jacobian of a chain's end-effector w.r.t. joint angles.

The numeric Jacobian is a 3 x n_dof matrix J where J[i][j] = d(ee_i)/d(angle_j),
computed by central differences. It is the workhorse for the damped
least-squares inverse-kinematics solver (analytic Jacobians for arbitrary
revolute chains are more code for no reference-value gain).
"""
from .fk import fk_chain


def numeric_jacobian(chain, angles, eps=1e-5):
    n = len(angles)
    _, ee0 = fk_chain(chain, angles)
    J = [[0.0] * n for _ in range(3)]
    for j in range(n):
        up = list(angles)
        dn = list(angles)
        up[j] += eps
        dn[j] -= eps
        _, eeu = fk_chain(chain, up)
        _, eed = fk_chain(chain, dn)
        for i in range(3):
            J[i][j] = (eeu[i] - eed[i]) / (2.0 * eps)
    return J, ee0
