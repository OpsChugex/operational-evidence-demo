# OCX-OPS-001: Operational Evidence Demo

[![Validate operational evidence demo](https://github.com/OpsChugex/operational-evidence-demo/actions/workflows/validate.yml/badge.svg)](https://github.com/OpsChugex/operational-evidence-demo/actions/workflows/validate.yml)

**Classification:** Controlled demonstration

**Scope:** Local simulation only

**Customer systems:** None

This repository demonstrates a reproducible evidence flow:

**change → telemetry → correlated evidence → diagnosis → human review → remediation → proof of fix**

It does not connect to customer infrastructure and does not claim production monitoring, customer outcomes, uptime, cost savings or incident-response performance.

## Scenarios

- Healthy baseline
- Memory regression after deployment
- Database latency
- Security exposure

## Reproduce the evidence

Requires Python 3.12+ and uses only the Python standard library.

```bash
python validate_demo.py
python validate_http_recovery.py
```

A successful run confirms that the documented scenario contract is intact and that the controlled HTTP service can move from a degraded memory-regression scenario back to the healthy state.

## Files

- `demo_service.py` contains the self-contained controlled service and scenario data.
- `validate_demo.py` validates the scenario contract.
- `validate_http_recovery.py` validates the degraded-to-healthy recovery path.
- `.github/workflows/validate.yml` repeats both checks in GitHub Actions.

## Evidence interpretation

A passing workflow is evidence that **this controlled demonstration** behaved as documented for the tested commit. It is not evidence that a customer environment was monitored or remediated.

## Security and cost boundaries

- No cloud resources are created.
- No credentials or secrets are required.
- No customer data is accessed.
- GitHub Actions permissions are read-only.
- Third-party actions are pinned to immutable commit SHAs.
