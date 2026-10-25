# -*- coding: utf-8 -*-
import unittest

from embodyforge.control.pd import PDController
from embodyforge.control.balance import ZMPPreviewController, support_polygon, _point_in_polygon
from embodyforge.core.linalg import vec3


class TestPD(unittest.TestCase):
    def test_torque_tracks(self):
        pd = PDController(10.0, 1.0)
        tau = pd.torque([0.0], [0.0], [0.5])
        self.assertGreater(tau[0], 0.0)


class TestBalance(unittest.TestCase):
    def test_polygon_non_degenerate(self):
        poly = support_polygon([vec3(0.06, 0, 0), vec3(-0.06, 0, 0)])
        self.assertEqual(len(poly), 4)

    def test_point_in_polygon(self):
        poly = [(-0.1, -0.1), (0.1, -0.1), (0.1, 0.1), (-0.1, 0.1)]
        self.assertTrue(_point_in_polygon((0.0, 0.0), poly))
        self.assertFalse(_point_in_polygon((1.0, 1.0), poly))

    def test_margin_monotonic(self):
        ctl = ZMPPreviewController()
        feet = [vec3(0.06, 0, 0), vec3(-0.06, 0, 0)]
        com = [0.0, 0.0, 0.8]
        lo = ctl.margin(com, [0, 0, 0], feet, skill=0.5)
        hi = ctl.margin(com, [0, 0, 0], feet, skill=1.0)
        self.assertGreater(hi, lo)


if __name__ == "__main__":
    unittest.main()
