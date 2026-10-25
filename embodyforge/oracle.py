# -*- coding: utf-8 -*-
"""Shared oracle -- the single source of truth for mock and benchmark.

The oracle deterministically derives, for a given task id, the ground truth
(correct motion primitive, target position, fall outcome, ...). Both the mock
backend and every benchmark call it with the same key, so skill=1.0 always
reproduces the ground truth and every metric is exactly monotonic in skill.
"""
from .utils.random import stable_float, stable_int, stable_vector


def motion_primitives():
    return ["stand", "walk", "turn", "step", "wave", "squat", "reach", "grasp"]


def correct_primitive(task_id):
    prims = motion_primitives()
    idx = stable_int("corr:" + str(task_id), 0, len(prims))
    return prims[idx]


def target_position(task_id):
    return stable_vector("tgt:" + str(task_id), 3, -1.0, 1.0)


def fall_label(task_id, skill):
    """Deterministic fall outcome: unskilled controllers fall more often."""
    p = stable_float("fall:" + str(task_id), 0.0, 1.0)
    return p > skill


def scene_observation(task_id, obs_dim=32):
    return stable_vector("obs:" + str(task_id), obs_dim)
