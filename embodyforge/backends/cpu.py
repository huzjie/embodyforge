# -*- coding: utf-8 -*-
"""CPU backend: a real forward pass through the reference model."""
from .base import EmbodiedBackend, register_backend
from ..model import EmbodiedModel
from ..embodied.foundation import EmbodiedFoundationModel
from ..config import Config


@register_backend("cpu")
class CpuBackend(EmbodiedBackend):
    name = "cpu"

    def __init__(self, cfg=None):
        self.cfg = cfg if cfg is not None else Config()
        self.model = EmbodiedModel(self.cfg)
        self.foundation = EmbodiedFoundationModel(self.cfg.embodied)

    def solve(self, task, skill=1.0):
        return self.foundation.solve(task, skill=skill)

    def balance(self, com, feet, skill=1.0):
        return self.model.balance.margin(com, [0.0, 0.0, 0.0], feet, skill=skill)

    def train_step(self, skill, lr=0.2):
        return skill + lr * (1.0 - skill)
