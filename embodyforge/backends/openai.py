# -*- coding: utf-8 -*-
"""OpenAI backend: delegates to a hosted model when configured, else CPU."""
from .base import EmbodiedBackend, register_backend
from .cpu import CpuBackend


@register_backend("openai")
class OpenAIBackend(CpuBackend):
    name = "openai"

    def __init__(self, cfg=None):
        super().__init__(cfg)
        self._fallback = CpuBackend(cfg)

    def solve(self, task, skill=1.0):
        # hosted models would be called here; the reference falls back to CPU
        return self._fallback.solve(task, skill=skill)
