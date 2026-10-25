# -*- coding: utf-8 -*-
"""Zero-moment point (ZMP).

The ZMP is the point on the ground where the horizontal moment of the ground
reaction is zero. A biped is statically stable while the ZMP stays inside the
support polygon (the convex hull of the feet). Using the point-mass LIPM
approximation with CoM height ``h``::

    p_zmp = com - (h / g) * com_ddot

The balance controller keeps this point inside the support polygon by steering
the CoM acceleration.
"""
from ..core.linalg import vec3, sub3, mul3


def zmp_from_com(com, com_ddot, height, gravity=9.81):
    """com/com_ddot are 3-vectors; returns the ZMP 3-vector (z = 0)."""
    p = sub3(com, mul3(com_ddot, height / gravity))
    return vec3(p[0], p[1], 0.0)


def zmp_3d(com, com_ddot, height, gravity=9.81):
    return zmp_from_com(com, com_ddot, height, gravity)
