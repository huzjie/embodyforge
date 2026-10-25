# -*- coding: utf-8 -*-
"""Motion library.

A library of named motion clips (idle, wave, squat, step-touch, spin, ...). It
is the reusable vocabulary from which dance routines are assembled -- the same
idea as a robot "skill library" but for locomotion/choreography primitives.
"""
from .keyframe import Keyframe, MotionClip


def build_default_library():
    """Return a small deterministic library of dance primitives."""
    clips = {}

    def _clip(name, poses):
        clips[name] = MotionClip(name, [
            Keyframe(name + "_%d" % i, pose, time=float(i))
            for i, pose in enumerate(poses)
        ])

    # idle: neutral pose
    _clip("idle", [
        {"l_arm_shoulder_pitch": 0.0, "r_arm_shoulder_pitch": 0.0},
        {"l_arm_shoulder_pitch": 0.0, "r_arm_shoulder_pitch": 0.0},
    ])
    # wave: raise one arm
    _clip("wave", [
        {"l_arm_shoulder_pitch": -0.3, "l_arm_elbow_pitch": 0.2},
        {"l_arm_shoulder_pitch": -0.9, "l_arm_elbow_pitch": 0.5},
        {"l_arm_shoulder_pitch": -0.3, "l_arm_elbow_pitch": 0.2},
    ])
    # squat: bend knees
    _clip("squat", [
        {"l_leg_knee_pitch": 0.2, "r_leg_knee_pitch": 0.2},
        {"l_leg_knee_pitch": 0.9, "r_leg_knee_pitch": 0.9},
        {"l_leg_knee_pitch": 0.2, "r_leg_knee_pitch": 0.2},
    ])
    # step-touch: lateral step
    _clip("step_touch", [
        {"l_leg_hip_roll": 0.0, "r_leg_hip_roll": 0.0},
        {"l_leg_hip_roll": 0.4, "r_leg_hip_roll": -0.4},
        {"l_leg_hip_roll": 0.0, "r_leg_hip_roll": 0.0},
    ])
    # spin: torso yaw
    _clip("spin", [
        {"torso_yaw": 0.0},
        {"torso_yaw": 0.8},
        {"torso_yaw": 1.6},
        {"torso_yaw": 0.0},
    ])
    return MotionLibrary(clips)


class MotionLibrary:
    def __init__(self, clips=None):
        self.clips = clips or {}

    def add(self, clip):
        self.clips[clip.name] = clip

    def get(self, name):
        return self.clips.get(name)

    def names(self):
        return sorted(self.clips.keys())
