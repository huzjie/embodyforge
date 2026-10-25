# -*- coding: utf-8 -*-
"""Serving: a stdlib HTTP server exposing the model (no external deps)."""


def main():
    from .app import run
    run()


__all__ = ["main"]
