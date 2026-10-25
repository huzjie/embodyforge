# -*- coding: utf-8 -*-
"""Center of mass (CoM) computation.

For the reference the humanoid is modeled as a small set of point masses (torso
plus the two feet), which is the standard reduced-order treatment used by the
inverted-pendulum balance controller. ``point_mass_com`` is the mass-weighted
average; ``center_of_mass`` wraps it over the robot state.
"""
from ..core.linalg import vec3, mul3, add3


def point_mass_com(masses, positions):
    """masses: [m0, m1, ...] ; positions: [[x,y,z], ...]. Returns the CoM."""
    total = sum(masses) or 1.0
    acc = vec3()
    for m, p in zip(masses, positions):
        acc = add3(acc, mul3(p, m))
    return mul3(acc, 1.0 / total)


def center_of_mass(robot_state):
    """robot_state: {torso: [x,y,z], feet: [[x,y,z], ...], masses: {...}}."""
    masses = robot_state.get("masses", {})
    torso = robot_state.get("torso", vec3())
    feet = robot_state.get("feet", [])
    positions = [torso] + feet
    ms = [masses.get("torso", 1.0)] + [masses.get("foot", 0.1) for _ in feet]
    return point_mass_com(ms, positions)
