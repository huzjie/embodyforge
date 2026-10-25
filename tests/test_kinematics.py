# -*- coding: utf-8 -*-
import unittest

from embodyforge.kinematics.chain import build_humanoid_chains
from embodyforge.kinematics.fk import fk_chain, fk_all
from embodyforge.kinematics.ik import ik_chain
from embodyforge.core.linalg import norm, sub3


class TestKinematics(unittest.TestCase):
    def setUp(self):
        self.chains = build_humanoid_chains()

    def test_humanoid_chains(self):
        self.assertIn("left_leg", self.chains)
        self.assertIn("right_arm", self.chains)
        self.assertEqual(self.chains["left_leg"].n_dof, 6)
        self.assertEqual(self.chains["left_arm"].n_dof, 7)

    def test_fk_neutral_leg(self):
        leg = self.chains["left_leg"]
        _, ee = fk_chain(leg, [0.0] * leg.n_dof)
        # root [0.08, 0, -0.5] minus thigh 0.4 minus shin 0.4
        for a, b in zip(ee, [0.08, 0.0, -1.3]):
            self.assertAlmostEqual(a, b, places=5)

    def test_fk_all(self):
        angles = {n: [0.0] * c.n_dof for n, c in self.chains.items()}
        out = fk_all(self.chains, angles)
        self.assertEqual(set(out.keys()), set(self.chains.keys()))

    def test_ik_reaches_target(self):
        leg = self.chains["left_leg"]
        # forward-and-up target (away from the straight-leg singularity)
        target = [0.35, 0.0, -0.9]
        q = ik_chain(leg, target)
        self.assertIsNotNone(q)
        _, ee = fk_chain(leg, q)
        self.assertLess(norm(sub3(ee, target)), 0.05)


if __name__ == "__main__":
    unittest.main()
