import time
import functools

"""
Task: Write a retry decorator with exponential backoff.

  retry(max_attempts=3, base_delay=0.1, retryable=(ConnectionError, TimeoutError))

Behavior:
  - call the wrapped function; on success, return its result
  - if it raises a RETRYABLE exception, wait base_delay * (2 ** (attempt - 1))
    seconds, then try again, up to max_attempts total attempts
  - if it raises a NON-retryable exception (e.g. ValueError), do not retry —
    re-raise immediately
  - after exhausting all attempts, re-raise the last exception (do not swallow it)

A flaky function is provided below to exercise the decorator.
"""


def retry(max_attempts: int = 3, base_delay: float = 0.1, retryable: tuple = (ConnectionError, TimeoutError)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Write your solution here
            pass
        return wrapper
    return decorator


# --- Provided: a function that fails the first `fail_times` calls ------------
def make_flaky(fail_times: int, exc: Exception = ConnectionError("transient")):
    state = {"calls": 0}

    def flaky():
        state["calls"] += 1
        if state["calls"] <= fail_times:
            raise exc
        return "ok"

    return flaky, state
