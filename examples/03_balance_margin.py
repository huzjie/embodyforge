# -*- coding: utf-8 -*-
"""ZMP balance margin at skill 0.5 vs 1.0."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from embodyforge.control.balance import ZMPPreviewController
from embodyforge.core.linalg import vec3

ctl = ZMPPreviewController()
feet = [vec3(0.06, 0.0, 0.0), vec3(-0.06, 0.0, 0.0)]
com = [0.0, 0.0, 0.8]
print("balance margin @ skill 0.5: %.4f" % ctl.margin(com, [0, 0, 0], feet, skill=0.5))
print("balance margin @ skill 1.0: %.4f" % ctl.margin(com, [0, 0, 0], feet, skill=1.0))
