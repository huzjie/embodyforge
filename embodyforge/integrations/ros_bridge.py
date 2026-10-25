# -*- coding: utf-8 -*-
"""A pure-Python stand-in for a ROS topic bridge.

Real deployments publish joint states / twist / odometry on ROS topics. This
bridge reproduces the publish/subscribe interface with in-memory queues so the
rest of the project can be wired into a ROS graph without the ROS dependency.
"""
from collections import defaultdict, deque


class ROSBridge:
    def __init__(self):
        self._subs = defaultdict(list)
        self._bufs = defaultdict(deque)

    def advertise(self, topic):
        self._bufs[topic] = deque(maxlen=100)

    def publish(self, topic, msg):
        self._bufs[topic].append(msg)
        for cb in self._subs.get(topic, []):
            cb(msg)

    def subscribe(self, topic, callback):
        self._subs[topic].append(callback)

    def latest(self, topic):
        buf = self._bufs.get(topic)
        return buf[-1] if buf else None

    def publish_joint_state(self, robot):
        self.publish("/joint_states", robot.joint_angles)

    def publish_odometry(self, com):
        self.publish("/odom", {"com": com})
