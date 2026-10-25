# -*- coding: utf-8 -*-
"""vLLM backend: high-throughput serving stub -> CPU fallback."""
from .base import EmbodiedBackend, register_backend
from .cpu import CpuBackend


@register_backend("vllm")
class VllmBackend(CpuBackend):
    name = "vllm"

    def __init__(self, cfg=None):
        super().__init__(cfg)
        self._fallback = CpuBackend(cfg)

    def solve(self, task, skill=1.0):
        return self._fallback.solve(task, skill=skill)
