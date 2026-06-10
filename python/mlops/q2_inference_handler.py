import time

"""
Task: Implement an inference handler.

A model is loaded once when this module is imported. Implement handle(payload)
so that it:
  - validates the payload: it must contain "features", a non-empty list —
    raise ValueError on anything malformed
  - runs the already-loaded model (do NOT create a new model per call)
  - returns {"prediction": <int>, "latency_ms": <float>}, where latency_ms is
    how long the inference call took, in milliseconds
"""


# --- Provided: a model loaded once, reused on every call --------------------
class DummyModel:
    def predict(self, features: list) -> int:
        # Pretend this is a real forward pass.
        return 1 if sum(features) > 0 else 0


model = DummyModel()


def handle(payload: dict) -> dict:
    # Write your solution here
    pass
