# -*- coding: utf-8 -*-
"""Mock backend: deterministic, trainable, skill-driven.

The mock backend reproduces the ground truth from the shared oracle, modulated
by ``skill``. It is what makes every benchmark sweep monotonically:

  * solve    -> action == required_primitive with probability driven by boost
  * balance  -> realized margin scaled by (0.5 + 0.5*skill)
  * sync     -> Kuramoto lock converges with coupling scaled by skill
  * train    -> geometric skill climb ``skill += lr * (1 - skill)``
"""
from .base import EmbodiedBackend, register_backend
from ..oracle import correct_primitive, target_position
from ..utils.random import stable_bool


@register_backend("mock")
class MockBackend(EmbodiedBackend):
    name = "mock"

    def solve(self, task, skill=1.0):
        boost = (skill - 0.5) * 2.0
        correct = correct_primitive(task.task_id)
        # skill=0.5 -> p=0.5 random; skill=1.0 -> p=1.0 always correct
        hit = stable_bool("hit:" + str(task.task_id), p=0.5 + 0.5 * boost)
        return (correct if hit else ("stand" if correct != "stand" else "walk")),                hit

    def balance(self, com, feet, skill=1.0):
        from ..control.balance import ZMPPreviewController
        from ..config import Config
        cfg = Config() if self.cfg is None else self.cfg
        ctl = ZMPPreviewController(cfg.control)
        return ctl.margin(com, [0.0, 0.0, 0.0], feet, skill=skill)

    def sync_order(self, n, skill=1.0):
        # deterministic order parameter at skill
        return 0.5 + 0.5 * skill

    def train_step(self, skill, lr=0.2):
        return skill + lr * (1.0 - skill)
