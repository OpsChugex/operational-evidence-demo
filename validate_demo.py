from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

root = Path(__file__).resolve().parents[2]
source = root / "apps" / "diagnosis-demo" / "main.py"
spec = spec_from_file_location("opschugex_diagnosis_demo", source)
if spec is None or spec.loader is None:
    raise RuntimeError("Unable to load controlled diagnosis demo")

module = module_from_spec(spec)
spec.loader.exec_module(module)

scenarios = module.SCENARIOS
required = {"healthy", "memory_regression", "database_latency", "security_exposure"}
assert required == set(scenarios), "Scenario set has changed unexpectedly"

for name, state in scenarios.items():
    assert state["scenario"] == name
    assert isinstance(state["availability"], (int, float))
    assert isinstance(state["error_rate"], (int, float))

assert scenarios["memory_regression"]["deployment_recent"] is True
assert scenarios["memory_regression"]["pod_restarts"] > 0
assert scenarios["database_latency"]["database_latency"] > 1000
assert scenarios["security_exposure"]["public_ssh"] is True

print("OPERATIONAL_EVIDENCE_DEMO=PASS")
print("CLASSIFICATION=DEMONSTRATION")