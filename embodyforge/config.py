# -*- coding: utf-8 -*-
"""Configuration for embodyforge.

A plain dataclass plus a minimal YAML loader (falling back to a tiny hand-rolled
parser ``utils/yamlish.py`` because the managed Python runtime has no pyyaml).
Declared scale numbers (110 robots / 40 DoF / A3 form factor) are informational
only; the reference implementation instantiates tiny structures so a full
forward pass runs in milliseconds of pure Python.
"""
import os
from dataclasses import dataclass, field, asdict
from pathlib import Path

try:  # pragma: no cover - optional
    import yaml as _pyyaml  # type: ignore
except Exception:  # pragma: no cover
    _pyyaml = None


@dataclass
class KinematicsConfig:
    leg_dof: int = 6           # declared 6 per leg (hip 3 + knee 1 + ankle 2)
    arm_dof: int = 7           # declared 7 per arm
    n_legs: int = 2
    n_arms: int = 2
    thigh_len: float = 0.4
    shin_len: float = 0.4
    torso_len: float = 0.5
    ik_max_iter: int = 60
    ik_damping: float = 0.05
    ik_tol: float = 1e-3


@dataclass
class DynamicsConfig:
    mass_kg: float = 50.0       # declared A3 ~50 kg
    com_height: float = 0.8
    gravity: float = 9.81
    support_radius: float = 0.12


@dataclass
class GaitConfig:
    step_len: float = 0.2
    step_height: float = 0.06
    cadence: float = 1.2        # steps per second
    stance_ratio: float = 0.6
    n_phases: int = 8


@dataclass
class ControlConfig:
    kp: float = 120.0
    kd: float = 8.0
    preview_horizon: int = 10
    fall_margin: float = 0.05


@dataclass
class OrchestraConfig:
    n_robots: int = 8           # declared 110
    coupling: float = 0.3       # Kuramoto coupling strength
    clock_interval: float = 0.05
    collision_radius: float = 0.6
    repulsion: float = 0.5


@dataclass
class EmbodiedConfig:
    n_skills: int = 16
    n_primitives: int = 8
    obs_dim: int = 32
    temperature: float = 0.8
    learning_rate: float = 0.2
    max_steps: int = 40


@dataclass
class ServingConfig:
    host: str = "127.0.0.1"
    port: int = 8322


@dataclass
class TrainConfig:
    learning_rate: float = 0.2
    max_steps: int = 40
    seed: int = 20261025


@dataclass
class BenchConfig:
    n_tasks: int = 200
    n_steps: int = 64
    seed: int = 20261025


@dataclass
class DeclaredConfig:
    n_robots: int = 110
    dof_per_robot: int = 40
    height_m: float = 1.2
    mass_kg: float = 50.0
    guinness: str = "most humanoid robots dancing simultaneously"
    record_date: str = "2026-10-24"
    gait_speed_ms: float = 1.0

    def to_dict(self):
        return asdict(self)


@dataclass
class Config:
    kinematics: KinematicsConfig = field(default_factory=KinematicsConfig)
    dynamics: DynamicsConfig = field(default_factory=DynamicsConfig)
    gait: GaitConfig = field(default_factory=GaitConfig)
    control: ControlConfig = field(default_factory=ControlConfig)
    orchestra: OrchestraConfig = field(default_factory=OrchestraConfig)
    embodied: EmbodiedConfig = field(default_factory=EmbodiedConfig)
    serving: ServingConfig = field(default_factory=ServingConfig)
    train: TrainConfig = field(default_factory=TrainConfig)
    bench: BenchConfig = field(default_factory=BenchConfig)
    declared: DeclaredConfig = field(default_factory=DeclaredConfig)

    @classmethod
    def from_dict(cls, d):
        d = d or {}
        factories = {
            "kinematics": KinematicsConfig, "dynamics": DynamicsConfig,
            "gait": GaitConfig, "control": ControlConfig,
            "orchestra": OrchestraConfig, "embodied": EmbodiedConfig,
            "serving": ServingConfig, "train": TrainConfig,
            "bench": BenchConfig, "declared": DeclaredConfig,
        }
        kw = {}
        for key, factory in factories.items():
            kw[key] = factory(**{k: v for k, v in (d.get(key) or {}).items()})
        return cls(**kw)

    def to_dict(self):
        return asdict(self)


def load_config(path=None):
    if path is None:
        here = Path(__file__).parent
        path = here / "configs" / "default.yaml"
        if not path.exists():
            path = here.parent / "configs" / "default.yaml"
    p = Path(path)
    if not p.exists():
        return Config()
    text = p.read_text(encoding="utf-8")
    data = None
    if _pyyaml is not None:
        try:
            data = _pyyaml.safe_load(text)
        except Exception:
            data = None
    if data is None:
        from .utils.yamlish import parse
        data = parse(text)
    return Config.from_dict(data)
