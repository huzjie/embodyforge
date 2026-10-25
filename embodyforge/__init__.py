# -*- coding: utf-8 -*-
"""embodyforge - embodied humanoid coordinated-motion control engine.

A pure-Python, zero-dependency reference implementation of the ideas behind the
Guinness World Record set on 2026-10-24 by 110 full-size humanoid robots
(Agibot / Zhiyuan "Expedition A3") dancing simultaneously -- and of the wider
"embodied foundation model" thesis that the industry is calling the coming
"GPT-3 moment" of robotics (2026-2028).

The composable pieces:

  * kinematics  - forward / inverse kinematics and Jacobians for a many-DoF
                  humanoid (legs and arms as revolute-joint chains).
  * dynamics    - center-of-mass, zero-moment point (ZMP) and the linear
                  inverted-pendulum model (LIPM) that underpin balance.
  * gait        - footstep planning, gait phase and a walk-cycle generator.
  * control     - PD joint torque control, ZMP preview control and fall detection.
  * choreo      - a keyframe motion library with slerp interpolation and
                  beat-synchronized dance routines.
  * orchestra   - multi-robot synchronization: logical clock sync, Kuramoto
                  phase-locking, formation control and collision avoidance.
  * embodied    - an embodied foundation model (perception -> action) and a
                  skill library learned with reinforcement signals.

Everything is deterministic (md5-seeded) and shares a single oracle. ``skill =
0.5`` is a random / untrained policy, ``skill = 1.0`` is the perfect one, so
every benchmark sweeps monotonically from a random baseline to the optimum.
"""

__version__ = "1.0.0"

from .config import Config, load_config
from .robot import HumanoidRobot
from .model import EmbodiedModel
from .orchestra.phaselock import KuramotoLock
from .embodied.foundation import EmbodiedFoundationModel

__all__ = [
    "Config", "load_config", "HumanoidRobot", "EmbodiedModel",
    "KuramotoLock", "EmbodiedFoundationModel", "__version__",
]
