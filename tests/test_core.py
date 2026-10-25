# -*- coding: utf-8 -*-
import math
import unittest

from embodyforge.core.linalg import vec3, add3, sub3, dot, cross, norm, normed
from embodyforge.core.quat import (quat_identity, quat_from_axis_angle,
                                   quat_mul, quat_rotate, quat_slerp)


class TestLinalg(unittest.TestCase):
    def test_dot_cross(self):
        a, b = vec3(1, 0, 0), vec3(0, 1, 0)
        self.assertAlmostEqual(dot(a, b), 0.0)
        self.assertEqual(cross(a, b), [0, 0, 1])

    def test_norm(self):
        self.assertAlmostEqual(norm(vec3(3, 4, 0)), 5.0)
        self.assertAlmostEqual(norm(normed(vec3(1, 2, 2))), 1.0)


class TestQuat(unittest.TestCase):
    def test_identity_rotate(self):
        v = vec3(1, 2, 3)
        r = quat_rotate(quat_identity(), v)
        for a, b in zip(r, v):
            self.assertAlmostEqual(a, b, places=6)

    def test_axis_angle_rotate_z(self):
        q = quat_from_axis_angle(vec3(0, 0, 1), math.pi / 2)
        r = quat_rotate(q, vec3(1, 0, 0))
        for a, b in zip(r, vec3(0, 1, 0)):
            self.assertAlmostEqual(a, b, places=5)

    def test_mul_identity(self):
        q = quat_from_axis_angle(vec3(1, 0, 0), 0.7)
        r = quat_mul(q, quat_identity())
        for a, b in zip(r, q):
            self.assertAlmostEqual(a, b, places=6)

    def test_slerp_endpoints(self):
        a = quat_identity()
        b = quat_from_axis_angle(vec3(0, 1, 0), 1.2)
        r0 = quat_slerp(a, b, 0.0)
        r1 = quat_slerp(a, b, 1.0)
        for x, y in zip(r0, a):
            self.assertAlmostEqual(x, y, places=5)
        for x, y in zip(r1, b):
            self.assertAlmostEqual(x, y, places=5)


if __name__ == "__main__":
    unittest.main()
