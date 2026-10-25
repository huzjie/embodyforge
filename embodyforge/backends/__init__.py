# -*- coding: utf-8 -*-
"""Pluggable backends.

Five backends implement the same ``EmbodiedBackend`` interface (``solve``,
``balance``, ``sync``, ``train_step``). The ``mock`` backend is fully
deterministic and trainable (it is what the benchmarks use); ``cpu`` runs a
real forward pass; ``openai`` / ``vllm`` / ``transformers`` delegate to a
real model if configured, otherwise they fall back to ``cpu``.
"""
from .base import EmbodiedBackend, register_backend, get_backend, list_backends
from . import mock, cpu, openai, vllm, transformers  # noqa: F401  (trigger registration)

__all__ = [
    "EmbodiedBackend", "register_backend", "get_backend", "list_backends",
    "mock", "cpu", "openai", "vllm", "transformers",
]
