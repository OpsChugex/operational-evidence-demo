from json import dumps, loads
from threading import Thread
from urllib.request import Request, urlopen

from demo_service import Handler, ThreadingHTTPServer

server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
port = server.server_address[1]
Thread(target=server.serve_forever, daemon=True).start()


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
    assert read("/scenario", "POST", {"scenario": "memory_regression"}) == {
        "status": "active", "scenario": "memory_regression"
    }
    degraded = read("/state")
    assert degraded["error_rate"] == 14.0 and degraded["pod_restarts"] == 2
    assert read("/scenario", "POST", {"scenario": "healthy"}) == {
        "status": "active", "scenario": "healthy"
    }
    assert read("/state")["scenario"] == "healthy"
    print("CONTROLLED_RECOVERY_FLOW=PASS")
    print("DEGRADED_SCENARIO=memory_regression")
    print("RECOVERY_TARGET=healthy")
finally:
    server.shutdown()
    server.server_close()
