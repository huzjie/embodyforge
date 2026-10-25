# -*- coding: utf-8 -*-
"""Action head and the motion-primitive vocabulary.

The action head scores each motion primitive for a given latent and returns the
argmax (or a sample at a temperature). Motion primitives are the robot's "verbs":
stand, walk, turn, step, wave, squat, reach, grasp.
"""
import math
from ..utils.random import stable_float
from ..oracle import correct_primitive, motion_primitives


class ActionHead:
    def __init__(self, n_primitives=8, temperature=0.8):
        self.primitives = motion_primitives()[:n_primitives]
        self.temperature = temperature

    def scores(self, latent, scene_id):
        """Deterministic per-primitive score for a scene (skill-agnostic prior)."""
        return [stable_float("act:%s:%s" % (scene_id, p), 0.0, 1.0)
                for p in self.primitives]

    def act(self, latent, scene_id, skill=1.0, sample=False):
        from ..utils.random import _rng
        boost = (skill - 0.5) * 2.0
        correct = self.correct_action(scene_id)
        scores = self.scores(latent, scene_id)
        # add boost to the correct primitive (strong margin so skill=1.0 wins)
        for i, p in enumerate(self.primitives):
            if p == correct:
                scores[i] += boost * 8.0
        if sample:
            # softmax sampling
            m = max(scores)
            exps = [math.exp((s - m) / self.temperature) for s in scores]
            z = sum(exps)
            r = _rng("sample:" + str(scene_id)).random() * z
            acc = 0.0
            for i, e in enumerate(exps):
                acc += e
                if r <= acc:
                    return self.primitives[i]
            return self.primitives[-1]
        return self.primitives[scores.index(max(scores))]

    def correct_action(self, scene_id):
        return correct_primitive(scene_id)
