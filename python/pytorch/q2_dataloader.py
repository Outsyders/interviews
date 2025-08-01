import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd

"""
Task: Build a custom Dataset class and use DataLoader to batch the data.
Input: A CSV file path with columns features_1, features_2, ..., label
Output: A PyTorch Dataset that reads the CSV file and returns features and labels.
"""


class CSVDataset(Dataset):
    def __init__(self, csv_path: str):
        pass


# Example usage
if __name__ == "__main__":
    import os
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    dataset = CSVDataset(f"{current_dir}/sample.csv")
    dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

    for batch_features, batch_labels in dataloader:
        print("Batch features:", batch_features)
        print("Batch labels:", batch_labels)
        break  # Just print one batch