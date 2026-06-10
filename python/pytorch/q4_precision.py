import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from torchvision.models import resnet18


"""
Task: Update the training loop to use mixed precision.
"""


# Dummy RGB image dataset (resnet18 expects 3-channel 224x224 inputs)
def get_dummy_loader(batch_size=32):
    x = torch.randn(512, 3, 224, 224)  # (B, C, H, W)
    y = torch.randint(0, 10, (512,))   # 10 classes
    dataset = TensorDataset(x, y)
    return DataLoader(dataset, batch_size=batch_size, shuffle=True)


# Training loop
def train(model, dataloader, device):
    model.to(device)
    model.train()

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-3)

    # GradScaler prevents fp16 gradients from underflowing to zero.
    use_amp = device.type == "cuda"
    scaler = torch.cuda.amp.GradScaler(enabled=use_amp)

    for epoch in range(2):
        for i, (inputs, labels) in enumerate(dataloader):
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()

            # Run the forward pass in mixed precision.
            with torch.autocast(device_type=device.type, enabled=use_amp):
                outputs = model(inputs)
                loss = criterion(outputs, labels)

            # Scale the loss, backprop, then unscale + step.
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

            if i % 10 == 0:
                print(f"[Epoch {epoch} | Step {i}] Loss: {loss.item():.4f}")


# Main entry
if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load pretrained resnet18 and adapt for 10-class classification
    model = resnet18(pretrained=False)
    model.fc = nn.Linear(model.fc.in_features, 10)

    dataloader = get_dummy_loader()
    train(model, dataloader, device)
