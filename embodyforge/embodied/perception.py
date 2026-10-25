# -*- coding: utf-8 -*-
"""Perception encoder.

Turns a raw observation (a deterministic pseudo-vector keyed by scene id) into a
latent state. For the reference the encoder is a fixed deterministic projection
(md5-seeded), not a trained network -- it only needs to be injective so that
distinct scenes yield distinct latents, which is what the skill oracle relies on.
"""
from ..utils.random import stable_vector
from ..core.linalg import normed


class PerceptionEncoder:
    def __init__(self, obs_dim=32):
        self.obs_dim = obs_dim

    def encode(self, scene_id):
        v = stable_vector("obs:" + str(scene_id), self.obs_dim)
        return normed(v)
