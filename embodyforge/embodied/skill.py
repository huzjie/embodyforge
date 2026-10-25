# -*- coding: utf-8 -*-
"""Skill library.

A ``Skill`` pairs a motion primitive with a success predicate over scenes. The
library stores the "correct" primitive for each scene (shared with the action
head via the same md5-seeded key), so skill=1.0 always retrieves the right one.
"""
from ..utils.random import stable_float
from .action import motion_primitives
from ..oracle import correct_primitive


class Skill:
    def __init__(self, name, primitive, success_fn=None):
        self.name = name
        self.primitive = primitive
        self.success_fn = success_fn or (lambda scene_id: True)

    def apply(self, scene_id):
        return self.success_fn(scene_id)


class SkillLibrary:
    def __init__(self, n_skills=16):
        prims = motion_primitives()
        self.skills = {}
        for i in range(n_skills):
            p = prims[i % len(prims)]
            self.skills["skill_%02d" % i] = Skill("skill_%02d" % i, p)

    def correct_primitive(self, scene_id):
        return correct_primitive(scene_id)

    def names(self):
        return sorted(self.skills.keys())
