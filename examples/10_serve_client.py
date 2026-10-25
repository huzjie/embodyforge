# -*- coding: utf-8 -*-
"""A tiny client for the stdlib HTTP server (run `python -m embodyforge serve` first)."""
import json
import urllib.request

BASE = "http://127.0.0.1:8322"


def get(path):
    with urllib.request.urlopen(BASE + path, timeout=5) as r:
        return json.loads(r.read().decode("utf-8"))


def post(path, obj):
    data = json.dumps(obj).encode("utf-8")
    req = urllib.request.Request(BASE + path, data=data,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=5) as r:
        return json.loads(r.read().decode("utf-8"))


print("health:", get("/health"))
print("models:", get("/v1/models")["declared"])
print("solve:", post("/v1/solve", {"scene_id": "demo", "skill": 0.9}))
print("step:", post("/v1/step", {"t": 0.0, "skill": 0.9})["balance_margin"])
