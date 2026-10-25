# -*- coding: utf-8 -*-
"""Command-line interface.

    python -m embodyforge doctor            # self-test all components + backends
    python -m embodyforge bench             # run 5 benchmarks
    python -m embodyforge train             # demonstrate skill 0.5 -> 1.0
    python -m embodyforge serve             # start the HTTP server
    python -m embodyforge demo              # one dance step + IK solve
"""
import argparse
import json
import sys


def _cmd_doctor(cfg):
    from .backends import list_backends, get_backend
    from .model import EmbodiedModel
    from .embodied.foundation import EmbodiedFoundationModel
    from .kinematics.chain import build_humanoid_chains
    from .kinematics.fk import fk_chain
    from .kinematics.ik import ik_chain
    from .data.synth import synth_tasks

    chains = build_humanoid_chains()
    print("chains: %d (%s)" % (len(chains), ", ".join(chains.keys())))
    # FK smoke
    _, ee = fk_chain(chains["left_leg"], [0.0] * chains["left_leg"].n_dof)
    print("left_leg FK end-effector:", [round(x, 4) for x in ee])
    # IK smoke: reach a forward-and-up target (away from straight-leg singularity)
    target = [0.35, 0.0, -0.9]
    q = ik_chain(chains["left_leg"], target)
    _, ee2 = fk_chain(chains["left_leg"], q or [0.0] * chains["left_leg"].n_dof)
    print("IK solve:", "ok" if q is not None else "failed",
          "-> end-effector", [round(x, 4) for x in ee2])
    # model forward
    m = EmbodiedModel(cfg)
    st = m.step(0.0, skill=1.0)
    print("model step: balance_margin=%.4f fallen=%s n_dof=%d" % (
        st["balance_margin"], st["fallen"], st["n_dof"]))
    # foundation
    f = EmbodiedFoundationModel(cfg.embodied)
    tasks = synth_tasks(20)
    hits = sum(1 for t in tasks if f.solve(t, skill=1.0)[1])
    print("foundation skill=1.0 recall: %d/%d" % (hits, len(tasks)))
    # backends
    print("backends:", ", ".join(list_backends()))
    for name in list_backends():
        b = get_backend(name, cfg)
        print("  %-14s train_step(0.5) -> %.4f" % (name, b.train_step(0.5, 0.2)))
    print("doctor: OK")


def _cmd_bench(cfg):
    from .bench.run import run_all, summarize
    results = run_all(cfg)
    print(summarize(results))


def _cmd_train(cfg):
    from .train import Trainer
    from .backends import get_backend
    backend = get_backend("mock", cfg)
    t = Trainer(cfg)
    hist = t.train(backend)
    print("skill: %.4f -> %.4f over %d steps (monotonic)" % (
        hist[0][1], hist[-1][1], len(hist) - 1))


def _cmd_demo(cfg):
    from .choreo.dance import build_dance_routine
    from .gait.generator import WalkCycle
    d = build_dance_routine(120.0)
    w = WalkCycle(cfg.gait)
    print("dance duration %.2fs (%.1f beats)" % (d.duration(), d.total_beats()))
    print("walk angles @t=0.5:", w.angles_at(0.5))


def _cmd_serve(cfg):
    from .serving.app import run
    run(cfg=cfg)


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(prog="embodyforge")
    parser.add_argument("--config", default=None)
    sub = parser.add_subparsers(dest="cmd")
    for name in ("doctor", "bench", "train", "serve", "demo"):
        sub.add_parser(name)
    args = parser.parse_args(argv)

    from .config import load_config
    cfg = load_config(args.config)

    if args.cmd == "doctor":
        _cmd_doctor(cfg)
    elif args.cmd == "bench":
        _cmd_bench(cfg)
    elif args.cmd == "train":
        _cmd_train(cfg)
    elif args.cmd == "serve":
        _cmd_serve(cfg)
    elif args.cmd == "demo":
        _cmd_demo(cfg)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
