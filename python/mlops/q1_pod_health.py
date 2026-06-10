import json
import os

"""
Task: Classify Kubernetes pods as healthy or unhealthy.

You are given pods.json, a list of simplified pod dicts. Each pod looks like:

    {
        "name": "web-1",
        "phase": "Running",            # Running | Pending | Succeeded | Failed
        "restart_count": 0,
        "container_state": "running",  # running | waiting | terminated
        "reason": null,                # e.g. CrashLoopBackOff, OOMKilled, Unschedulable
        "deletion_timestamp": null     # set (a timestamp string) while the pod is terminating
    }

Note: not every key is guaranteed to be present on every pod.

Treat a pod as UNHEALTHY if any of these hold:
  - container is waiting with reason "CrashLoopBackOff"
  - container was terminated with reason "OOMKilled"
  - restart_count exceeds RESTART_THRESHOLD
  - phase is "Pending" because it cannot be scheduled (reason "Unschedulable")
  - it is stuck Terminating (deletion_timestamp is set but the pod is still here)

Implement:
  classify_pod(pod: dict) -> str            # "healthy" or "unhealthy"
  find_unhealthy(pods: list) -> list[str]   # names of the unhealthy pods
"""

RESTART_THRESHOLD = 5


def classify_pod(pod: dict) -> str:
    # Write your solution here
    pass


def find_unhealthy(pods: list) -> list:
    # Write your solution here
    pass


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "pods.json")) as f:
        pods = json.load(f)
    print(find_unhealthy(pods))
