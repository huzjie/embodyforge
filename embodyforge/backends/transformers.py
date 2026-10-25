# -*- coding: utf-8 -*-
"""Transformers backend: HF pipeline stub -> CPU fallback."""
from .base import EmbodiedBackend, register_backend
from .cpu import CpuBackend


@register_backend("transformers")
class TransformersBackend(CpuBackend):
    name = "transformers"

    def __init__(self, cfg=None):
        super().__init__(cfg)
        self._fallback = CpuBackend(cfg)

    def solve(self, task, skill=1.0):
        return self._fallback.solve(task, skill=skill)
