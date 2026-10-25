# -*- coding: utf-8 -*-
"""Skill trainer.

The "skill" is the single scalar that captures policy quality. Training is a
geometric climb ``skill += lr * (1 - skill)`` -- always positive, never a random
walk. This is what every benchmark's learning curve is built on: skill starts at
0.5 (random) and monotonically approaches 1.0 (perfect).
"""
from .config import Config, load_config


class Trainer:
    def __init__(self, cfg=None):
        self.cfg = cfg if cfg is not None else Config()
        self.skill = 0.5

    def step(self, backend=None, lr=None):
        lr = lr if lr is not None else self.cfg.train.learning_rate
        if backend is not None:
            self.skill = backend.train_step(self.skill, lr=lr)
        else:
            self.skill += lr * (1.0 - self.skill)
        return self.skill

    def train(self, backend=None, steps=None):
        steps = steps if steps is not None else self.cfg.train.max_steps
        history = [(0, self.skill)]
        for i in range(1, steps + 1):
            s = self.step(backend)
            history.append((i, s))
        return history


def main():
    import sys
    cfg = load_config(sys.argv[1] if len(sys.argv) > 1 else None)
    t = Trainer(cfg)
    hist = t.train()
    print("skill: %.4f -> %.4f over %d steps" % (hist[0][1], hist[-1][1], len(hist) - 1))


if __name__ == "__main__":
    main()
