# -*- coding: utf-8 -*-
"""HTTP serving via the standard library (no Flask/FastAPI).

Endpoints:
  GET  /health          -> {"status": "ok"}
  GET  /v1/models       -> declared scale + backends
  POST /v1/solve        -> {"scene_id": "...", "skill": 0.9} -> chosen primitive
  POST /v1/step         -> {"t": 0.0, "skill": 0.9} -> one control step
"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from ..config import Config, load_config
from ..embodied.foundation import EmbodiedFoundationModel
from ..model import EmbodiedModel
from ..backends import list_backends
from ..data.synth import Task
from ..oracle import correct_primitive


def _json(handler, code, obj):
    body = json.dumps(obj).encode("utf-8")
    handler.send_response(code)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def make_handler(model, foundation):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/health":
                return _json(self, 200, {"status": "ok"})
            if self.path == "/v1/models":
                return _json(self, 200, {
                    "declared": model.cfg.declared.to_dict(),
                    "backends": list_backends(),
                })
            return _json(self, 404, {"error": "not found"})

        def do_POST(self):
            n = int(self.headers.get("Content-Length", 0))
            try:
                payload = json.loads(self.rfile.read(n).decode("utf-8")) if n else {}
            except Exception:
                return _json(self, 400, {"error": "bad json"})
            if self.path == "/v1/solve":
                scene = payload.get("scene_id", "demo")
                skill = float(payload.get("skill", 0.9))
                task = Task(scene, correct_primitive(scene))
                chosen, ok = foundation.solve(task, skill=skill)
                return _json(self, 200, {"scene_id": scene, "chosen": chosen,
                                         "success": ok, "skill": skill})
            if self.path == "/v1/step":
                t = float(payload.get("t", 0.0))
                skill = float(payload.get("skill", 0.9))
                state = model.step(t, skill=skill)
                return _json(self, 200, state)
            return _json(self, 404, {"error": "not found"})

        def log_message(self, *a):
            pass

    return Handler


def run(host=None, port=None, cfg=None):
    cfg = cfg or Config()
    host = host or cfg.serving.host
    port = port or cfg.serving.port
    model = EmbodiedModel(cfg)
    foundation = EmbodiedFoundationModel(cfg.embodied)
    srv = HTTPServer((host, port), make_handler(model, foundation))
    print("embodyforge serving on http://%s:%d" % (host, port), flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()


if __name__ == "__main__":
    run()
