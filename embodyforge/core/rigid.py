# -*- coding: utf-8 -*-
"""Rigid transforms: a rotation (quaternion) + a translation (3-vector).

Composing transforms is how forward kinematics walks a kinematic chain from the
root out to an end-effector. A transform ``T = (q, p)`` maps a point ``x`` to
``rot(q, x) + p``.
"""
from .quat import quat_mul, quat_rotate, quat_conjugate
from .linalg import add3, sub3


def Transform(q=(1.0, 0.0, 0.0, 0.0), p=(0.0, 0.0, 0.0)):
    return [q, p]


def compose(a, b):
    """Apply a then b:  T_ab = T_a * T_b."""
    qa, pa = a
    qb, pb = b
    return [quat_mul(qa, qb), add3(pa, quat_rotate(qa, pb))]


def inverse(t):
    q, p = t
    qc = quat_conjugate(q)
    return [qc, quat_rotate(qc, [-p[0], -p[1], -p[2]])]


def apply_point(t, x):
    q, p = t
    return add3(quat_rotate(q, x), p)


def apply_vector(t, v):
    q, _ = t
    return quat_rotate(q, v)
