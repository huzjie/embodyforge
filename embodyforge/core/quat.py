# -*- coding: utf-8 -*-
"""Quaternions (w, x, y, z) for 3D rotation -- correct and self-contained.

The humanoid kinematics need clean 3D rotations for joint axes that are not
axis-aligned. Quaternions avoid gimbal lock and compose/slerp cleanly. A
quaternion ``q`` represents rotation by angle ``a`` around axis ``(x,y,z)``
(normalized) as ``q = (cos(a/2), sin(a/2) x, sin(a/2) y, sin(a/2) z)``.
"""
import math


def Quat(w=1.0, x=0.0, y=0.0, z=0.0):
    return [w, x, y, z]


def quat_identity():
    return Quat(1.0, 0.0, 0.0, 0.0)


def quat_from_axis_angle(axis, angle):
    ax = normed3(axis)
    s = math.sin(angle / 2.0)
    return Quat(math.cos(angle / 2.0), ax[0] * s, ax[1] * s, ax[2] * s)


def quat_mul(a, b):
    w1, x1, y1, z1 = a
    w2, x2, y2, z2 = b
    return Quat(
        w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
        w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
        w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
        w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
    )


def _norm4(q):
    return math.sqrt(q[0] * q[0] + q[1] * q[1] + q[2] * q[2] + q[3] * q[3])


def quat_conjugate(q):
    return [q[0], -q[1], -q[2], -q[3]]


def quat_rotate(q, v):
    """Rotate vector v by quaternion q:  q * [0,v] * conj(q)."""
    vq = Quat(0.0, v[0], v[1], v[2])
    r = quat_mul(quat_mul(q, vq), quat_conjugate(q))
    return [r[1], r[2], r[3]]


def quat_slerp(a, b, t):
    """Spherical linear interpolation between unit quaternions a and b."""
    dot = a[0] * b[0] + a[1] * b[1] + a[2] * b[2] + a[3] * b[3]
    if dot < 0.0:
        b = [-b[0], -b[1], -b[2], -b[3]]
        dot = -dot
    dot = max(-1.0, min(1.0, dot))
    theta = math.acos(dot)
    if theta < 1e-6:
        # near-parallel: linear interpolation + renormalize
        out = [a[i] + (b[i] - a[i]) * t for i in range(4)]
        n = _norm4(out) or 1.0
        return [out[i] / n for i in range(4)]
    s = math.sin(theta)
    wa = math.sin((1.0 - t) * theta) / s
    wb = math.sin(t * theta) / s
    return [wa * a[i] + wb * b[i] for i in range(4)]


def quat_to_matrix(q):
    w, x, y, z = q
    return [
        [1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
        [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
        [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)],
    ]


def normed3(v):
    n = math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
    if n < 1e-12:
        return [0.0, 0.0, 0.0]
    return [v[0] / n, v[1] / n, v[2] / n]
