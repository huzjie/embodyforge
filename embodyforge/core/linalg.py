# -*- coding: utf-8 -*-
"""Minimal 3-vector linear algebra over plain Python lists."""
import math


def vec3(x=0.0, y=0.0, z=0.0):
    return [x, y, z]


def add3(a, b):
    return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]


def sub3(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]


def mul3(a, s):
    return [a[0] * s, a[1] * s, a[2] * s]


def scale3(a, s):
    return mul3(a, s)


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    ]


def norm(a):
    return math.sqrt(dot(a, a))


def normed(a):
    n = norm(a)
    if n < 1e-12:
        return [0.0, 0.0, 0.0]
    return [a[0] / n, a[1] / n, a[2] / n]


def dist(a, b):
    return norm(sub3(a, b))
