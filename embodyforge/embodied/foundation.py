# -*- coding: utf-8 -*-
"""Embodied foundation model.

Composes perception + action: encode the scene, pick the action, then look up
the motion clip in the skill library. This is the single entry point the serving
API and benchmarks call.
"""
from .perception import PerceptionEncoder
from .action import ActionHead
from .skill import SkillLibrary
from ..config import EmbodiedConfig


class EmbodiedFoundationModel:
    def __init__(self, cfg=None):
        self.cfg = cfg or EmbodiedConfig()
        self.encoder = PerceptionEncoder(self.cfg.obs_dim)
        self.head = ActionHead(self.cfg.n_primitives, self.cfg.temperature)
        self.library = SkillLibrary()

    def perceive(self, scene_id):
        return self.encoder.encode(scene_id)

    def act(self, scene_id, skill=1.0, sample=False):
        latent = self.perceive(scene_id)
        return self.head.act(latent, scene_id, skill=skill, sample=sample)

    def solve(self, task, skill=1.0):
        """task: an object with .scene_id and .required_primitive. Returns
        (chosen_primitive, success)."""
        latent = self.perceive(task.scene_id)
        chosen = self.head.act(latent, task.scene_id, skill=skill)
        return chosen, (chosen == task.required_primitive)

    def n_params(self):
        return self.cfg.n_skills * self.cfg.n_primitives
