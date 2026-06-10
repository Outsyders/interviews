import numpy as np
import torch

"""
Task: Convert this array to a PyTorch tensor and move it to GPU (if available).
Input: A NumPy array np_array = np.random.rand(3, 3)
Output: A PyTorch tensor with the same shape and data type as the NumPy array.
"""


def array_to_tensor(data: np.ndarray) -> torch.Tensor:
    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
    return torch.from_numpy(data)