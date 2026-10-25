# -*- coding: utf-8 -*-
import unittest

from embodyforge.dynamics.com import point_mass_com
from embodyforge.dynamics.zmp import zmp_from_com
from embodyforge.dynamics.ipm import LIPM
from embodyforge.gait.phase import GaitPhase
from embodyforge.gait.footstep import FootstepPlanner
from embodyforge.gait.generator import WalkCycle


class TestDynamics(unittest.TestCase):
    def test_com(self):
        com = point_mass_com([1.0, 1.0], [[0.0, 0, 0], [2.0, 0, 0]])
        self.assertAlmostEqual(com[0], 1.0)

    def test_zmp_still(self):
        # no acceleration -> zmp projects to com (x, y)
        z = zmp_from_com([1.0, 2.0, 0.8], [0.0, 0.0, 0.0], 0.8)
        self.assertAlmostEqual(z[0], 1.0)
        self.assertAlmostEqual(z[1], 2.0)
        self.assertAlmostEqual(z[2], 0.0)

    def test_lipm_step(self):
        m = LIPM(0.8)
        com2, vel2 = m.step([0.1, 0, 0.8], [0, 0, 0], [0.0, 0, 0], dt=0.01)
        # com accelerates away from zmp -> x increases
        self.assertGreater(com2[0], 0.1)


class TestGait(unittest.TestCase):
    def test_phase_range(self):
        p = GaitPhase()
        for t in (0.0, 0.5, 1.5):
            self.assertGreaterEqual(p.phase(t, 1.2), 0.0)
            self.assertLess(p.phase(t, 1.2), 1.0)

    def test_footstep(self):
        steps = FootstepPlanner(0.2).plan(6)
        self.assertEqual(len(steps), 6)
        self.assertAlmostEqual(steps[0][2], 0.0)

    def test_walk_cycle_angles(self):
        w = WalkCycle()
        a = w.angles_at(0.0)
        self.assertIn("left_leg", a)
        self.assertEqual(len(a["left_leg"]), 6)


if __name__ == "__main__":
    unittest.main()
