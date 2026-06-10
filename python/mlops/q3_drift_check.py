import numpy as np

"""
Task: Detect feature drift between a reference dataset and an incoming batch.

Both arrays are 2D with shape (n_samples, n_features); columns are features.

Implement:
  detect_drift(reference, incoming, threshold) -> list

Return the indices of features whose distribution has shifted beyond `threshold`.
A normalized mean shift is acceptable here, e.g. for each feature:

    shift = |mean(incoming) - mean(reference)| / (std(reference) + eps)

and flag the feature when shift > threshold.

Requirements:
  - vectorize over numpy; do not loop feature-by-feature
  - do not crash on zero-variance features (guard the divide)

In production you'd use a proper distributional test instead of a mean shift,
e.g. PSI (Population Stability Index) or a two-sample KS test per feature.
"""


def detect_drift(reference: np.ndarray, incoming: np.ndarray, threshold: float) -> list:
    # Write your solution here
    pass
