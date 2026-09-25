from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from json import dumps, loads

SCENARIOS = {
    "healthy": {
        "scenario": "healthy", "availability": 99.99, "error_rate": 0.1,
        "deployment_recent": False, "pod_restarts": 0,
        "database_latency": 35, "public_ssh": False,
    },
    "memory_regression": {
        "scenario": "memory_regression", "availability": 97.5, "error_rate": 14.0,
        "deployment_recent": True, "pod_restarts": 2,
        "database_latency": 45, "public_ssh": False,
    },
    "database_latency": {
        "scenario": "database_latency", "availability": 98.8, "error_rate": 4.5,
        "deployment_recent": False, "pod_restarts": 0,
        "database_latency": 1450, "public_ssh": False,
    },
    "security_exposure": {
        "scenario": "security_exposure", "availability": 99.9, "error_rate": 0.2,
        "deployment_recent": False, "pod_restarts": 0,
        "database_latency": 40, "public_ssh": True,
    },
}

_active_scenario = "healthy"


class Handler(BaseHTTPRequestHandler):
    def _write_json(self, payload, status=200):
        body = dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._write_json({"status": "ok", "classification": "controlled-demo"})
        elif self.path == "/state":
            self._write_json(SCENARIOS[_active_scenario])
        else:
            self._write_json({"error": "not_found"}, status=404)

    def do_POST(self):
        global _active_scenario
        if self.path != "/scenario":
            self._write_json({"error": "not_found"}, status=404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        try:
            payload = loads(self.rfile.read(length).decode("utf-8"))
        except Exception:
            self._write_json({"error": "invalid_json"}, status=400)
            return
        scenario = payload.get("scenario")
        if scenario not in SCENARIOS:
            self._write_json({"error": "unknown_scenario"}, status=400)
            return
        _active_scenario = scenario
        self._write_json({"status": "active", "scenario": scenario})

    def log_message(self, format, *args):
        return


def serve(host="127.0.0.1", port=8080):
    ThreadingHTTPServer((host, port), Handler).serve_forever()


if __name__ == "__main__":
    serve()
