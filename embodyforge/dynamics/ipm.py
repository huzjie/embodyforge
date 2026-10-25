# -*- coding: utf-8 -*-
"""Linear inverted pendulum model (LIPM).

The LIPM is the canonical reduced-order model for biped balance: the whole robot
is a point mass on a massless rod of fixed height ``h``. Its CoM dynamics along
an axis ``x`` are::

    x_ddot = (g / h) * (x - zmp_x)

which is a simple, analytically solvable linear system -- exactly why ZMP preview
control (see ``control/balance.py``) can precompute CoM trajectories.
"""
import math


class LIPM:
    def __init__(self, height, gravity=9.81):
        self.h = height
        self.g = gravity
        self.omega = math.sqrt(gravity / height)  # natural frequency

    def com_ddot(self, com, zmp):
        return [(self.g / self.h) * (com[i] - zmp[i]) for i in range(3)]

    def step(self, com, vel, zmp, dt):
        dd = self.com_ddot(com, zmp)
        vel2 = [vel[i] + dd[i] * dt for i in range(3)]
        com2 = [com[i] + vel2[i] * dt for i in range(3)]
        return com2, vel2


def lipm_com_trajectory(com0, vel0, zmp, height, dt, n_steps, gravity=9.81):
    """Integrate the LIPM forward for ``n_steps``; returns list of CoM."""
    m = LIPM(height, gravity)
    com, vel = list(com0), list(vel0)
    out = [list(com)]
    for _ in range(n_steps):
        com, vel = m.step(com, vel, zmp, dt)
        out.append(list(com))
    return out


def lipm_zmp_control(com, vel, zmp_ref, kp, kd, height, gravity=9.81):
    """A simple PD tracking controller that returns the commanded CoM
    acceleration to follow a reference ZMP (used by preview control)."""
    m = LIPM(height, gravity)
    dd_open = m.com_ddot(com, zmp_ref)
    # add damping on velocity error toward zero (stabilize upright)
    return [dd_open[i] - kp * com[i] - kd * vel[i] for i in range(3)]
