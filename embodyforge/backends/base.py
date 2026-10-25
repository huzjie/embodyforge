# -*- coding: utf-8 -*-
"""Backend registry."""
_BACKENDS = {}


def register_backend(name):
    def deco(cls):
        _BACKENDS[name] = cls
        return cls
    return deco


def get_backend(name, cfg=None):
    if name not in _BACKENDS:
        raise KeyError("unknown backend %r (available: %s)" % (name, list(_BACKENDS)))
    return _BACKENDS[name](cfg)


def list_backends():
    return sorted(_BACKENDS.keys())


class EmbodiedBackend:
    name = "base"

    def __init__(self, cfg=None):
        self.cfg = cfg

    def solve(self, task, skill=1.0):
        raise NotImplementedError

    def balance(self, com, feet, skill=1.0):
        raise NotImplementedError

    def train_step(self, skill, lr=0.2):
        return skill
