# -*- coding: utf-8 -*-
"""PD (proportional-derivative) joint torque controller.

``tau = kp * (q_des - q) + kd * (dq_des - dq)``. This is the per-joint servo that
tracks the reference angles produced by the gait generator or the choreography.
"""


def _pd_torque(q, dq, q_des, dq_des, kp, kd):
    return [kp * (qd - q[i]) + kd * (ddd - dq[i])
            for i, (qd, ddd) in enumerate(zip(q_des, dq_des))]


class PDController:
    def __init__(self, kp=120.0, kd=8.0):
        self.kp = kp
        self.kd = kd

    def torque(self, q, dq, q_des, dq_des=None):
        n = len(q)
        dq_des = dq_des if dq_des is not None else [0.0] * n
        return _pd_torque(q, dq, q_des, dq_des, self.kp, self.kd)

    def step(self, q, dq, q_des, dt):
        """Integrate one control step (simple semi-implicit Euler)."""
        tau = self.torque(q, dq, q_des)
        dq2 = [dq[i] + tau[i] * dt for i in range(len(q))]
        q2 = [q[i] + dq2[i] * dt for i in range(len(q))]
        return q2, dq2
