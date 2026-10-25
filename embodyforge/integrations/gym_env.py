# -*- coding: utf-8 -*-
"""A minimal Gym-style locomotion environment.

Exposes the standard ``reset()`` / ``step(action)`` API on top of the
``EmbodiedModel``. Reward is the balance margin plus a forward-progress bonus,
so an RL loop can use it unchanged.
"""
from ..model import EmbodiedModel


class LocomotionEnv:
    def __init__(self, cfg=None, max_steps=200):
        self.model = EmbodiedModel(cfg)
        self.max_steps = max_steps
        self.t = 0.0
        self.dt = 0.05
        self._steps = 0

    def reset(self, skill=0.5):
        self.t = 0.0
        self._steps = 0
        self.skill = skill
        return self._obs()

    def _obs(self):
        st = self.model.step(self.t, skill=self.skill)
        return {"com": st["com"], "balance_margin": st["balance_margin"]}

    def step(self, action):
        self.t += self.dt
        self._steps += 1
        st = self.model.step(self.t, skill=self.skill)
        reward = st["balance_margin"]
        done = st["fallen"] or self._steps >= self.max_steps
        return self._obs(), reward, done, {}
