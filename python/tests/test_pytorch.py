import pytest
import os
import tempfile


@pytest.mark.parametrize("input_shape", [(1, 28, 28), (3, 32, 32), (1, 64, 64)])
def test_tensor_conversion(input_shape):
    from python.pytorch.q1_tensor_conversion import array_to_tensor
    import numpy as np
    import torch

    # Create a NumPy array with the parameterized input_shape
    array = np.random.rand(*input_shape).astype(np.float32)
    
    # Convert NumPy array to PyTorch tensor
    tensor = array_to_tensor(array)
    
    assert isinstance(tensor, torch.Tensor), f"Output should be a PyTorch tensor, got {type(tensor)}"
    assert tensor.shape == input_shape, f"Expected shape {input_shape}, got {tensor.shape}"
    assert tensor.cpu().numpy().tolist() == array.tolist(), "Converted NumPy array should match the original"


def create_temp_csv(num_rows=10, num_features=3):
    import pandas as pd

    data = {
        f"feature_{i+1}": [i + j for j in range(num_rows)]
        for i in range(num_features)
    }
    data["label"] = [j % 2 for j in range(num_rows)]
    df = pd.DataFrame(data)

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w')
    df.to_csv(tmp_file.name, index=False)
    return tmp_file.name


def test_csv_dataloader_shapes():
    from python.pytorch.q2_dataloader import CSVDataset
    from torch.utils.data import DataLoader
    import torch

    csv_path = create_temp_csv(num_rows=20, num_features=3)
    
    dataset = CSVDataset(csv_path)
    dataloader = DataLoader(dataset, batch_size=5, shuffle=False)

    for batch_features, batch_labels in dataloader:
        assert batch_features.shape == (5, 3), \
            f"Expected features shape (5, 3), got {batch_features.shape}"
        assert batch_labels.shape == (5,), \
            f"Expected labels shape (5,), got {batch_labels.shape}"
        assert isinstance(batch_features, torch.Tensor)
        assert isinstance(batch_labels, torch.Tensor)
        break  # Only check one batch

    os.remove(csv_path)  # Cleanup


def test_csv_dataset_len():
    from python.pytorch.q2_dataloader import CSVDataset
    csv_path = create_temp_csv(num_rows=12, num_features=2)
    dataset = CSVDataset(csv_path)
    assert len(dataset) == 12
    os.remove(csv_path)


def test_missing_file_raises_error():
    from python.pytorch.q2_dataloader import CSVDataset
    with pytest.raises(FileNotFoundError):
        _ = CSVDataset("non_existent_file.csv")


@pytest.mark.parametrize("batch_size", [1, 4, 8])
def test_cnn_output_shape(batch_size):
    from python.pytorch.q3_cnn import SimpleCNN
    import torch

    model = SimpleCNN()
    dummy_input = torch.randn(batch_size, 1, 28, 28)
    output = model(dummy_input)

    assert output.shape == (batch_size, 10), \
        f"Expected output shape {(batch_size, 10)}, but got {output.shape}"