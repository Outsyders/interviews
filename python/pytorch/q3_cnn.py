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
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc = nn.Linear(32 * 7 * 7, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))  # 28x28 -> 14x14
        x = self.pool(F.relu(self.conv2(x)))  # 14x14 -> 7x7
        x = x.view(x.size(0), -1)
        return self.fc(x)


# Example usage
if __name__ == "__main__":
    model = SimpleCNN()
    dummy_input = torch.randn(8, 1, 28, 28)  # batch of 8 grayscale images
    output = model(dummy_input)
    print("Output shape:", output.shape)     # Should be (8, 10)
