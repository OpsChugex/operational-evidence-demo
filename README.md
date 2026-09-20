# OCX-OPS-001: Operational Evidence Demo

**Classification:** Demonstration  
**Status:** Verified for controlled scenario validation

This is a local, controlled simulation used to demonstrate the OpsChugex evidence flow:

Change, telemetry, correlated evidence, diagnosis, human review, remediation and proof of fix.

It does not connect to customer systems and does not claim real production monitoring.

## Scenarios

- Healthy baseline
- Memory regression after deployment
- Database latency
- Security exposure

Run `python validate_demo.py` from the repository root to validate the scenario contract. Run `python validate_http_recovery.py` to start the controlled service locally, introduce a memory regression, and verify recovery to a healthy state.