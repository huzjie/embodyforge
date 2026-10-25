# -*- coding: utf-8 -*-
"""Kuramoto phase-locking.

The Kuramoto model is the canonical description of how weakly-coupled oscillators
synchronize. Each robot has a phase ``theta_i`` that advances at its natural
frequency and is pulled toward the mean phase of its neighbors::

    dtheta_i/dt = omega_i + K/N * sum_j sin(theta_j - theta_i)

The skill of the controller maps to the coupling strength: higher skill = faster
and tighter synchronization, so the sync-precision benchmark sweeps monotonically.
"""
import math
from ..utils.random import stable_float


class KuramotoLock:
    def __init__(self, n, coupling=0.3, natural_freq=1.0):
        self.n = n
        self.coupling = coupling
        # deterministic non-symmetric initial phases + slightly spread natural
        # frequencies; evenly-spaced phases are an unstable equilibrium where the
        # coupling term vanishes, so a tiny spread is required to actually lock
        self.phases = [stable_float("ph:%d" % i, 0.0, 2.0 * math.pi) for i in range(n)]
        self.omegas = [natural_freq + stable_float("om:%d" % i, -0.2, 0.2)
                       for i in range(n)]

    def step(self, dt=0.05, skill=1.0):
        boost = (skill - 0.5) * 2.0
        K = self.coupling * boost
        new = []
        for i in range(self.n):
            pull = sum(math.sin(self.phases[j] - self.phases[i])
                       for j in range(self.n)) / self.n
            new.append(self.phases[i] + dt * (self.omegas[i] + K * pull))
        self.phases = new
        return self.phases

    def order_parameter(self):
        """Kuramoto order parameter r in [0,1]: 1 = fully synchronized."""
        n = self.n
        sx = sum(math.cos(p) for p in self.phases)
        sy = sum(math.sin(p) for p in self.phases)
        return math.sqrt(sx * sx + sy * sy) / n

    def phase_error(self):
        """Mean pairwise phase difference (radians) in [0, pi]."""
        # circular variance
        r = self.order_parameter()
        return math.acos(max(-1.0, min(1.0, r)))
