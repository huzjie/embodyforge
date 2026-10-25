# -*- coding: utf-8 -*-
import unittest

from embodyforge.config import Config, load_config
from embodyforge.serving.app import make_handler
from embodyforge.model import EmbodiedModel
from embodyforge.embodied.foundation import EmbodiedFoundationModel


class TestConfig(unittest.TestCase):
    def test_load_default(self):
        cfg = load_config()
        self.assertEqual(cfg.declared.n_robots, 110)
        self.assertEqual(cfg.declared.dof_per_robot, 40)

    def test_from_dict(self):
        cfg = Config.from_dict({"declared": {"n_robots": 55}})
        self.assertEqual(cfg.declared.n_robots, 55)


class TestServing(unittest.TestCase):
    def test_make_handler(self):
        cfg = Config()
        model = EmbodiedModel(cfg)
        foundation = EmbodiedFoundationModel(cfg.embodied)
        H = make_handler(model, foundation)
        self.assertTrue(hasattr(H, "do_GET"))


if __name__ == "__main__":
    unittest.main()
