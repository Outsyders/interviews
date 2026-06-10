import os
import json

import pytest


HERE = os.path.dirname(os.path.abspath(__file__))
MLOPS_DIR = os.path.join(os.path.dirname(HERE), "mlops")


# --- Task 1: pod health -----------------------------------------------------
def load_pods():
    with open(os.path.join(MLOPS_DIR, "pods.json")) as f:
        return json.load(f)


def test_classify_individual_pods():
    from mlops.q1_pod_health import classify_pod

    by_name = {p["name"]: p for p in load_pods()}
    assert classify_pod(by_name["web-1"]) == "healthy"
    assert classify_pod(by_name["api-1"]) == "healthy"
    assert classify_pod(by_name["web-2"]) == "unhealthy"        # CrashLoopBackOff
    assert classify_pod(by_name["cache-1"]) == "unhealthy"      # OOMKilled
    assert classify_pod(by_name["worker-1"]) == "unhealthy"     # restarts over threshold
    assert classify_pod(by_name["scheduler-1"]) == "unhealthy"  # Pending
    assert classify_pod(by_name["db-1"]) == "unhealthy"         # Terminating


def test_find_unhealthy_names():
    from mlops.q1_pod_health import find_unhealthy

    result = find_unhealthy(load_pods())
    assert set(result) == {"web-2", "cache-1", "worker-1", "scheduler-1", "db-1"}


def test_missing_restart_count_treated_as_zero():
    from mlops.q1_pod_health import classify_pod

    # api-1 has no restart_count key at all.
    assert classify_pod({"name": "x", "status": "Running"}) == "healthy"


# --- Task 2: inference handler ----------------------------------------------
def test_inference_handler():
    from mlops.q2_inference_handler import handle

    out = handle({"features": [1.0, 2.0, 3.0]})
    assert out["prediction"] == 1
    assert out["latency_ms"] >= 0


@pytest.mark.parametrize("bad", [{}, {"features": "not-a-list"}, {"features": []}])
def test_inference_handler_rejects_bad_input(bad):
    from mlops.q2_inference_handler import handle

    with pytest.raises(ValueError):
        handle(bad)


# --- Task 3: drift check ----------------------------------------------------
def test_detect_drift():
    import numpy as np
    from mlops.q3_drift_check import detect_drift

    rng = np.random.default_rng(0)
    reference = rng.normal(0, 1, size=(500, 3))
    incoming = reference.copy()
    incoming[:, 1] += 5.0  # shift only feature 1

    drifted = detect_drift(reference, incoming, threshold=1.0)
    assert 1 in drifted
    assert 0 not in drifted and 2 not in drifted


def test_detect_drift_handles_zero_variance():
    import numpy as np
    from mlops.q3_drift_check import detect_drift

    reference = np.zeros((100, 2))  # zero variance everywhere
    incoming = np.zeros((100, 2))
    # Must not raise (no divide-by-zero blowup) and report no drift.
    assert detect_drift(reference, incoming, threshold=1.0) == []


# --- Task 4: retry with backoff ---------------------------------------------
def test_retry_succeeds_after_transient_failures():
    from mlops.q4_retry_backoff import retry, make_flaky

    flaky, state = make_flaky(fail_times=2)
    wrapped = retry(max_attempts=3, base_delay=0.0)(flaky)
    assert wrapped() == "ok"
    assert state["calls"] == 3


def test_retry_reraises_after_exhausting():
    from mlops.q4_retry_backoff import retry, make_flaky

    flaky, state = make_flaky(fail_times=10)
    wrapped = retry(max_attempts=3, base_delay=0.0)(flaky)
    with pytest.raises(ConnectionError):
        wrapped()
    assert state["calls"] == 3


# --- Task 5: resilient batch inference --------------------------------------
def test_run_batch(tmp_path):
    import csv
    from mlops.q5_batch_inference import run_batch

    in_path = os.path.join(MLOPS_DIR, "inputs.csv")
    out_path = tmp_path / "out.csv"

    failures = run_batch(in_path, str(out_path))
    assert failures == 1  # the "BAD" row

    with open(out_path) as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 5  # 6 inputs minus the 1 bad row
    assert "prediction" in rows[0]
