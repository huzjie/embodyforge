# -*- coding: utf-8 -*-
import unittest

from embodyforge.train import Trainer
from embodyforge.backends import get_backend, list_backends
from embodyforge.bench.run import run_all
from embodyforge.config import Config


class TestTrain(unittest.TestCase):
    def test_skill_climbs_monotonically(self):
        t = Trainer(Config())
        backend = get_backend("mock", t.cfg)
        hist = t.train(backend)
        for i in range(1, len(hist)):
            self.assertGreaterEqual(hist[i][1], hist[i - 1][1])
        self.assertGreater(hist[-1][1], 0.99)


class TestBench(unittest.TestCase):
    def test_all_benchmarks_monotonic(self):
        cfg = Config()
        results = run_all(cfg)
        for name, r in results.items():
            self.assertTrue(r.get("monotonic"), "benchmark %s not monotonic" % name)


class TestBackends(unittest.TestCase):
    def test_five_backends(self):
        names = list_backends()
        self.assertGreaterEqual(len(names), 5)
        for n in ("mock", "cpu", "openai", "vllm", "transformers"):
            self.assertIn(n, names)


if __name__ == "__main__":
    unittest.main()
