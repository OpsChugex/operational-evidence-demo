from importlib.util import module_from_spec, spec_from_file_location
from json import dumps, loads
from pathlib import Path
from threading import Thread
from urllib.request import Request, urlopen

root = Path(__file__).resolve().parents[2]
source = root / "apps" / "diagnosis-demo" / "main.py"
spec = spec_from_file_location("opschugex_diagnosis_http_demo", source)
if spec is None or spec.loader is None:
    raise RuntimeError("Unable to load controlled diagnosis demo")

module = module_from_spec(spec)
spec.loader.exec_module(module)
server = module.ThreadingHTTPServer(("127.0.0.1", 0), module.Handler)
port = server.server_address[1]
thread = Thread(target=server.serve_forever, daemon=True)
thread.start()

def read(path, method="GET", payload=None):
    request = Request(
        f"http://127.0.0.1:{port}{path}",
        data=(dumps(payload).encode("utf-8") if payload else None),
        headers={"Content-Type": "application/json"} if payload else {},
        method=method,
    )
    with urlopen(request, timeout=5) as response:
        assert response.status == 200
        return loads(response.read().decode("utf-8"))

try:
    assert read("/health")["status"] == "ok"
    assert read("/state")["scenario"] == "healthy"

    activated = read("/scenario", "POST", {"scenario": "memory_regression"})
    assert activated == {"status": "active", "scenario": "memory_regression"}
    degraded = read("/state")
    assert degraded["error_rate"] == 14.0
    assert degraded["pod_restarts"] == 2

    recovered = read("/scenario", "POST", {"scenario": "healthy"})
    assert recovered == {"status": "active", "scenario": "healthy"}
    assert read("/state")["scenario"] == "healthy"
    print("CONTROLLED_RECOVERY_FLOW=PASS")
finally:
    server.shutdown()
    server.server_close()