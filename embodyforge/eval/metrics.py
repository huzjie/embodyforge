# -*- coding: utf-8 -*-
"""Evaluation metrics used by benchmarks."""


def cosine(a, b):
    na = sum(x * x for x in a) ** 0.5
    nb = sum(x * x for x in b) ** 0.5
    if na < 1e-9 or nb < 1e-9:
        return 0.0
    return sum(x * y for x, y in zip(a, b)) / (na * nb)


def accuracy(preds, targets):
    if not preds:
        return 0.0
    return sum(1 for p, t in zip(preds, targets) if p == t) / len(preds)


def mean_absolute_error(preds, targets):
    if not preds:
        return 0.0
    return sum(abs(p - t) for p, t in zip(preds, targets)) / len(preds)
