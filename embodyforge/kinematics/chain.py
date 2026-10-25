# -*- coding: utf-8 -*-
"""A kinematic chain of revolute joints.

Each ``Link`` is a revolute joint: it rotates around ``axis`` (a unit vector in
the parent frame) by ``angle`` radians, then translates along ``offset`` to the
next joint. The chain ends at an end-effector.

``build_humanoid_chains`` assembles the standard many-DoF humanoid: two legs
(hip yaw/roll/pitch, knee pitch, ankle pitch/roll) and two arms (shoulder
yaw/pitch/roll, elbow pitch, wrist pitch/roll/yaw).
"""
from ..core.linalg import vec3


class Link:
    def __init__(self, name, axis, offset):
        self.name = name
        self.axis = axis          # unit vector [x, y, z]
        self.offset = offset      # link vector [x, y, z] (after rotation)

    def to_dict(self):
        return {"name": self.name, "axis": self.axis, "offset": self.offset}


class Chain:
    def __init__(self, name, root, links):
        self.name = name
        self.root = root          # root position [x, y, z]
        self.links = links        # list of Link

    @property
    def n_dof(self):
        return len(self.links)

    def to_dict(self):
        return {"name": self.name, "root": self.root,
                "links": [lk.to_dict() for lk in self.links]}


def _leg(name, hip_pos):
    # order: hip yaw (z), hip roll (x), hip pitch (y), knee pitch (y),
    #        ankle pitch (y), ankle roll (x)
    thigh = 0.4
    shin = 0.4
    links = [
        Link(name + "_hip_yaw", vec3(0, 0, 1), vec3(0, 0, 0)),
        Link(name + "_hip_roll", vec3(1, 0, 0), vec3(0, 0, 0)),
        Link(name + "_hip_pitch", vec3(0, 1, 0), vec3(0, 0, -thigh)),
        Link(name + "_knee_pitch", vec3(0, 1, 0), vec3(0, 0, -shin)),
        Link(name + "_ankle_pitch", vec3(0, 1, 0), vec3(0, 0, 0)),
        Link(name + "_ankle_roll", vec3(1, 0, 0), vec3(0, 0, 0)),
    ]
    return Chain(name, hip_pos, links)


def _arm(name, shoulder_pos, side=1.0):
    # order: shoulder yaw (z), shoulder pitch (y), shoulder roll (x),
    #        elbow pitch (y), wrist pitch (y), wrist roll (x), wrist yaw (z)
    upper = 0.3
    fore = 0.25
    links = [
        Link(name + "_shoulder_yaw", vec3(0, 0, 1), vec3(0, 0, 0)),
        Link(name + "_shoulder_pitch", vec3(0, 1, 0), vec3(0, 0, 0)),
        Link(name + "_shoulder_roll", vec3(1, 0, 0), vec3(side * upper, 0, 0)),
        Link(name + "_elbow_pitch", vec3(0, 1, 0), vec3(side * fore, 0, 0)),
        Link(name + "_wrist_pitch", vec3(0, 1, 0), vec3(0, 0, 0)),
        Link(name + "_wrist_roll", vec3(1, 0, 0), vec3(0, 0, 0)),
        Link(name + "_wrist_yaw", vec3(0, 0, 1), vec3(0, 0, 0)),
    ]
    return Chain(name, shoulder_pos, links)


def build_humanoid_chains():
    """Return a dict of named chains for a standard humanoid (A3-like)."""
    torso = 0.5
    hip = vec3(0, 0, -torso)
    shoulder = vec3(0, 0, 0)
    chains = {
        "left_leg": _leg("l_leg", vec3(0.08, 0, -torso)),
        "right_leg": _leg("r_leg", vec3(-0.08, 0, -torso)),
        "left_arm": _arm("l_arm", vec3(0.18, 0, 0), side=1.0),
        "right_arm": _arm("r_arm", vec3(-0.18, 0, 0), side=-1.0),
    }
    return chains
