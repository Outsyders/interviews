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
        df = pd.read_csv(csv_path)  # raises FileNotFoundError for a bad path
        self.features = df.drop(columns=["label"]).values.astype("float32")
        self.labels = df["label"].values.astype("int64")

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, idx: int):
        x = torch.tensor(self.features[idx], dtype=torch.float32)
        y = torch.tensor(self.labels[idx], dtype=torch.long)
        return x, y


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