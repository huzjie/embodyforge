# -*- coding: utf-8 -*-
"""ROS bridge: publish joint states and odometry (in-memory stand-in)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from embodyforge.integrations.ros_bridge import ROSBridge
from embodyforge.robot import HumanoidRobot

bridge = ROSBridge()
bridge.advertise("/joint_states")
bridge.advertise("/odom")
bridge.subscribe("/joint_states", lambda m: print("joint_states callback:", list(m.keys())))
robot = HumanoidRobot()
bridge.publish_joint_state(robot)
bridge.publish_odometry([0.0, 0.0, 0.8])
print("latest odom:", bridge.latest("/odom"))
