# -*- coding: utf-8 -*-
"""Embodied intelligence: perception -> action -> skill learning.

This is the "embodied foundation model" layer: a perception encoder turns an
observation into a latent, an action head picks a motion primitive, and a skill
library learns which primitive succeeds for which task via a reinforcement
signal. ``skill`` is the policy quality: 0.5 random, 1.0 perfect.
"""
from .perception import PerceptionEncoder
from .action import ActionHead, motion_primitives
from .foundation import EmbodiedFoundationModel
from .skill import Skill, SkillLibrary

__all__ = [
    "PerceptionEncoder", "ActionHead", "motion_primitives",
    "EmbodiedFoundationModel", "Skill", "SkillLibrary",
]
