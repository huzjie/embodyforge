# -*- coding: utf-8 -*-
"""Run all benchmarks and print a summary table."""
from .balance import run_balance
from .sync import run_sync
from .gait import run_gait
from .skill_recall import run_skill_recall
from .speedup import run_speedup


def run_all(cfg, backend_name="mock"):
    results = {
        "balance": run_balance(cfg, backend_name),
        "sync": run_sync(cfg),
        "gait": run_gait(cfg),
        "skill_recall": run_skill_recall(cfg),
        "speedup": run_speedup(cfg),
    }
    return results


def summarize(results):
    lines = []
    for name, r in results.items():
        keys = [k for k in r if k.endswith("_lo") or k.endswith("_hi")]
        lo = r.get(name + "_lo", None) or next((r[k] for k in keys if k.endswith("_lo")), 0.0)
        hi = r.get(name + "_hi", None) or next((r[k] for k in keys if k.endswith("_hi")), 0.0)
        lines.append("%-14s 0.5:%.3f  1.0:%.3f  %s" % (
            name, lo, hi, "mono" if r.get("monotonic") else "??"))
    return "\n".join(lines)


def main():
    from ..config import load_config
    cfg = load_config()
    results = run_all(cfg)
    print(summarize(results))


if __name__ == "__main__":
    main()
