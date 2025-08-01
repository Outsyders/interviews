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
        super(SimpleCNN, self).__init__()
        
        # Convolutional layer 1
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # Convolutional layer 2
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1)
        
        # Fully connected layer
        self.fc1 = nn.Linear(32 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        # Input shape: (batch_size, 1, 28, 28)
        x = self.pool(F.relu(self.conv1(x)))  # -> (batch_size, 16, 14, 14)
        x = self.pool(F.relu(self.conv2(x)))  # -> (batch_size, 32, 7, 7)
        x = x.view(x.size(0), -1)             # Flatten -> (batch_size, 32*7*7)
        x = F.relu(self.fc1(x))               # -> (batch_size, 128)
        x = self.fc2(x)                       # -> (batch_size, num_classes)
        return x


# Example usage
if __name__ == "__main__":
    model = SimpleCNN()
    dummy_input = torch.randn(8, 1, 28, 28)  # batch of 8 grayscale images
    output = model(dummy_input)
    print("Output shape:", output.shape)     # Should be (8, 10)
