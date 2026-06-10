import json
import os

"""
Task: Classify Kubernetes pods as healthy or unhealthy.

You are given pods.json, a list of simplified pod dicts. Each pod looks like:

    {"name": "web-1", "status": "Running", "restart_count": 0}

A pod is HEALTHY only when:
  - its status is "Running", and
  - its restart_count is at most RESTART_THRESHOLD

Any other status (e.g. "CrashLoopBackOff", "OOMKilled", "Pending",
"Terminating") is unhealthy. Note: restart_count may be missing — treat a
missing count as 0.

Implement:
  classify_pod(pod: dict) -> str            # "healthy" or "unhealthy"
  find_unhealthy(pods: list) -> list[str]   # names of the unhealthy pods
"""

RESTART_THRESHOLD = 5


def classify_pod(pod: dict) -> str:
    if pod.get("status") != "Running":
        return "unhealthy"
    if pod.get("restart_count", 0) > RESTART_THRESHOLD:
        return "unhealthy"
    return "healthy"


def find_unhealthy(pods: list) -> list:
    return [pod["name"] for pod in pods if classify_pod(pod) == "unhealthy"]


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "pods.json")) as f:
        pods = json.load(f)
    print(find_unhealthy(pods))
