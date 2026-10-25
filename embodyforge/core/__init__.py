# -*- coding: utf-8 -*-
"""Core numerical kernels: 3-vector math, quaternions, rigid transforms and
deterministic randomness. All operate on plain Python lists -- no numpy, no
torch, no external dependency."""
from .linalg import (vec3, add3, sub3, mul3, dot, cross, norm, normed, scale3)
from .quat import (Quat, quat_identity, quat_from_axis_angle, quat_mul,
                   quat_rotate, quat_slerp, quat_to_matrix)
from .rigid import Transform, compose, inverse, apply_point, apply_vector

__all__ = [
    "vec3", "add3", "sub3", "mul3", "dot", "cross", "norm", "normed", "scale3",
    "Quat", "quat_identity", "quat_from_axis_angle", "quat_mul",
    "quat_rotate", "quat_slerp", "quat_to_matrix",
    "Transform", "compose", "inverse", "apply_point", "apply_vector",
]
