from demo_service import SCENARIOS

required = {"healthy", "memory_regression", "database_latency", "security_exposure"}
assert required == set(SCENARIOS), "Scenario set has changed unexpectedly"

for name, state in SCENARIOS.items():
    assert state["scenario"] == name
    assert isinstance(state["availability"], (int, float))
    assert isinstance(state["error_rate"], (int, float))
    assert 0 <= state["availability"] <= 100
    assert state["error_rate"] >= 0

assert SCENARIOS["memory_regression"]["deployment_recent"] is True
assert SCENARIOS["memory_regression"]["pod_restarts"] > 0
assert SCENARIOS["database_latency"]["database_latency"] > 1000
assert SCENARIOS["security_exposure"]["public_ssh"] is True

print("OPERATIONAL_EVIDENCE_DEMO=PASS")
print("CLASSIFICATION=CONTROLLED_DEMONSTRATION")
print("SCENARIOS=4")
