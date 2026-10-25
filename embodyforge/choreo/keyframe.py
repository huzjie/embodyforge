# -*- coding: utf-8 -*-
"""Keyframes and motion clips.

A ``Keyframe`` is a named pose: a dict of ``{joint_name: angle}`` at a point in
time. A ``MotionClip`` is a time-ordered list of keyframes. Interpolation uses
linear interpolation for joint angles (rotation quaternions use slerp where a
pose stores quaternions, but the reference stores Euler angles for clarity).
"""
from ..utils.random import stable_vector


class Keyframe:
    def __init__(self, name, pose, time=0.0):
        self.name = name
        self.pose = dict(pose)     # {joint_name: angle}
        self.time = time

    def to_dict(self):
        return {"name": self.name, "time": self.time, "pose": self.pose}


class MotionClip:
    def __init__(self, name, keyframes):
        self.name = name
        self.keyframes = sorted(keyframes, key=lambda k: k.time)
        self.joints = sorted({j for k in self.keyframes for j in k.pose})

    def duration(self):
        if not self.keyframes:
            return 0.0
        return self.keyframes[-1].time

    def pose_at(self, t):
        """Linear-interpolate the clip pose at time t (clamps to ends)."""
        kfs = self.keyframes
        if not kfs:
            return {}
        if t <= kfs[0].time:
            return dict(kfs[0].pose)
        if t >= kfs[-1].time:
            return dict(kfs[-1].pose)
        for i in range(len(kfs) - 1):
            a, b = kfs[i], kfs[i + 1]
            if a.time <= t <= b.time:
                span = (b.time - a.time) or 1e-9
                u = (t - a.time) / span
                out = {}
                for j in self.joints:
                    va = a.pose.get(j, 0.0)
                    vb = b.pose.get(j, 0.0)
                    out[j] = va + (vb - va) * u
                return out
        return dict(kfs[-1].pose)


def interpolate_clip(clip, t):
    return clip.pose_at(t)
