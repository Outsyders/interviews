# MLOps

Short, practical tasks focused on the "Ops" half of ML — health checks, serving,
data drift, reliability, and resilient batch jobs. Each file has a task docstring
and a stub to fill in; provided data and helpers are already written. Tests live in
`tests/test_mlops.py`.

| # | File | Task | ~min |
|---|------|------|------|
| 1 | `q1_pod_health.py` | Classify Kubernetes pods healthy/unhealthy by walking pod dicts (`pods.json`). | 12 |
| 2 | `q2_inference_handler.py` | Fill in a FastAPI inference handler: use the startup model, time latency, 400 on bad input. | 13 |
| 3 | `q3_drift_check.py` | Detect feature drift between a reference array and an incoming batch (vectorized). | 12 |
| 4 | `q4_retry_backoff.py` | Retry decorator with exponential backoff; don't retry non-retryable errors. | 12 |
| 5 | `q5_batch_inference.py` | Resilient batch inference over a CSV; one bad row must not kill the job. | 13 |

Run the tests:

```
make install   # needs fastapi + httpx for q2
make test
```
