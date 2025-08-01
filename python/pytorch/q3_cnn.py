import torch
import torch.nn as nn
import torch.nn.functional as F

"""
Task: Build a small CNN for classifying 28x28 grayscale images into 10 classes.
Include forward pass only.

The model should have:
1. Two convolutional layers with ReLU activation and max pooling.
2. A fully connected layer that outputs the class scores.

Input: A batch of 28x28 grayscale images
Output: Class scores for each image in the batch.
"""


class SimpleCNN(nn.Module):
    def __init__(self):
        pass

    def forward(self, x):
        pass


# Example usage
if __name__ == "__main__":
    model = SimpleCNN()
    dummy_input = torch.randn(8, 1, 28, 28)  # batch of 8 grayscale images
    output = model(dummy_input)
    print("Output shape:", output.shape)     # Should be (8, 10)
