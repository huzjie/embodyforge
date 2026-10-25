# -*- coding: utf-8 -*-
"""Integrations: a Gym-style env and a ROS-topic bridge stub.

These keep the project useful in real pipelines (sim training, ROS deployment)
while remaining zero-dependency: the env exposes the standard reset/step API and
the bridge is a pure-Python stand-in for a ROS node.
"""
from .gym_env import LocomotionEnv
from .ros_bridge import ROSBridge

__all__ = ["LocomotionEnv", "ROSBridge"]
