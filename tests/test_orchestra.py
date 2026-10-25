# -*- coding: utf-8 -*-
import unittest

from embodyforge.orchestra.clock import LogicalClock, sync_clocks, make_robot_clocks
from embodyforge.orchestra.phaselock import KuramotoLock
from embodyforge.orchestra.formation import FormationController
from embodyforge.orchestra.collision import CollisionAvoidance
from embodyforge.core.linalg import vec3


class TestClock(unittest.TestCase):
    def test_sync_reduces_spread(self):
        clocks = make_robot_clocks(8, seed="t")
        before = max(c.offset for c in clocks) - min(c.offset for c in clocks)
        sync_clocks(clocks, rounds=10, coupling=0.8)
        after = max(c.offset for c in clocks) - min(c.offset for c in clocks)
        self.assertLess(after, before)


class TestPhaseLock(unittest.TestCase):
    def test_order_parameter_skill(self):
        lo = KuramotoLock(8, coupling=0.3)
        for _ in range(20):
            lo.step(dt=0.05, skill=0.5)
        hi = KuramotoLock(8, coupling=0.3)
        for _ in range(20):
            hi.step(dt=0.05, skill=1.0)
        self.assertGreater(hi.order_parameter(), lo.order_parameter())

    def test_order_parameter_bounds(self):
        lock = KuramotoLock(4)
        r = lock.order_parameter()
        self.assertGreaterEqual(r, 0.0)
        self.assertLessEqual(r, 1.0 + 1e-9)


class TestFormation(unittest.TestCase):
    def test_targets(self):
        f = FormationController("circle")
        t = f.targets(8)
        self.assertEqual(len(t), 8)


class TestCollision(unittest.TestCase):
    def test_collision_decreases_with_skill(self):
        ca = CollisionAvoidance(0.6, 0.5)
        positions = [vec3(0.1 * i, 0.1 * i, 0) for i in range(6)]
        lo = ca.count_collisions(positions, skill=0.5)
        hi = ca.count_collisions(positions, skill=1.0)
        self.assertLessEqual(hi, lo)


if __name__ == "__main__":
    unittest.main()
