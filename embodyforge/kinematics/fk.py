# -*- coding: utf-8 -*-
"""Forward kinematics.

Walks a chain from its root, composing per-link transforms (rotation about the
joint axis followed by the link offset). Returns every link's world position and
the end-effector position.
"""
from ..core.rigid import Transform, compose
from ..core.quat import quat_identity, quat_from_axis_angle
from ..core.linalg import vec3


def fk_chain(chain, angles):
    """Return (link_positions, end_effector) for a chain and its joint angles.

    link_positions[i] is the world position of the joint after applying the
    rotation of link i (i.e. the origin of link i+1). The final element is the
    end-effector position.
    """
    t = Transform(quat_identity(), list(chain.root))
    positions = []
    for link, angle in zip(chain.links, angles):
        q = quat_from_axis_angle(link.axis, angle)
        t = compose(t, Transform(q, vec3(0, 0, 0)))
        positions.append(list(t[1]))
        t = compose(t, Transform(quat_identity(), list(link.offset)))
    end_effector = list(t[1])
    return positions, end_effector


def fk_all(chains, joint_angles):
    """Forward kinematics over all chains. ``joint_angles`` maps chain name to
    a list of angles. Returns {chain_name: (positions, end_effector)}."""
    out = {}
    for name, chain in chains.items():
        angles = joint_angles.get(name, [0.0] * chain.n_dof)
        out[name] = fk_chain(chain, angles)
    return out
