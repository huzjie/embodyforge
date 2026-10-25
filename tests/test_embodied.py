# -*- coding: utf-8 -*-
import unittest

from embodyforge.embodied.foundation import EmbodiedFoundationModel
from embodyforge.embodied.action import motion_primitives
from embodyforge.embodied.skill import SkillLibrary
from embodyforge.data.synth import synth_tasks
from embodyforge.config import Config


class TestEmbodied(unittest.TestCase):
    def test_primitives(self):
        self.assertGreaterEqual(len(motion_primitives()), 8)

    def test_recall_monotonic(self):
        cfg = Config()
        model = EmbodiedFoundationModel(cfg.embodied)
        tasks = synth_tasks(100)
        lo = sum(1 for t in tasks if model.solve(t, skill=0.5)[1]) / 100
        hi = sum(1 for t in tasks if model.solve(t, skill=1.0)[1]) / 100
        self.assertGreater(hi, lo)
        self.assertAlmostEqual(hi, 1.0, places=6)

    def test_skill_library(self):
        lib = SkillLibrary(16)
        self.assertEqual(len(lib.names()), 16)


if __name__ == "__main__":
    unittest.main()
