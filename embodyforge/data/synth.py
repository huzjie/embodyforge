# -*- coding: utf-8 -*-
"""Deterministic synthetic tasks.

A ``Task`` is a scene id plus the required motion primitive. ``synth_tasks``
generates ``n`` tasks whose required primitives come from the shared oracle, so
benchmark accuracy == skill exactly.
"""
from ..oracle import correct_primitive


class Task:
    def __init__(self, task_id, required_primitive):
        self.task_id = task_id
        self.required_primitive = required_primitive
        self.scene_id = task_id

    def __repr__(self):
        return "Task(%s -> %s)" % (self.task_id, self.required_primitive)


def synth_tasks(n, seed="tasks"):
    return [Task("%s:%d" % (seed, i), correct_primitive("%s:%d" % (seed, i)))
            for i in range(n)]
