import time

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

"""
Task: Fill in the inference handler for a pre-built FastAPI service.

Everything below is provided EXCEPT the body of `predict`. Implement it so that it:
  - confirms the model is loaded (503 if not)
  - runs inference on the incoming features
  - returns the prediction plus the measured latency in milliseconds
  - returns HTTP 400 on malformed input

Do NOT reload the model inside the handler — use the instance created at startup.
"""


# --- Provided: a dummy model loaded once at startup -------------------------
class DummyModel:
    def __init__(self):
        self.loaded = True

    def predict(self, features: list) -> int:
        # Pretend this is a real forward pass.
        if not features:
            raise ValueError("empty feature vector")
        return 1 if sum(features) > 0 else 0


model = DummyModel()
app = FastAPI()


# --- Provided: request / response contracts ---------------------------------
class PredictRequest(BaseModel):
    features: list[float]


class PredictResponse(BaseModel):
    prediction: int
    latency_ms: float


# --- Implement this ---------------------------------------------------------
@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    # TODO: implement the handler
    pass
