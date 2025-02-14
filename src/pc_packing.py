import h5py
import numpy as np
from torch.utils.data import Dataset


def pack(x: np.ndarray, mask: np.ndarray) -> tuple:
    """Undo all padding and compress the sequence."""
    seqlens = mask.sum(axis=-1)
    culens = seqlens.cumsum(axis=0)
    culens = np.pad(culens, (1, 0))
    return x[mask], culens


def unpack(x: np.ndarray, culens: np.ndarray, pad_length: int = 0) -> np.ndarray:
    """Restore the padding and unpack the sequence."""
    seqlens = np.diff(culens)
    pad_length = pad_length or seqlens.max()
    mask = np.arange(pad_length) < seqlens[:, None]
    out = np.zeros((*mask.shape, x.shape[-1]), dtype=x.dtype)
    out[mask] = x
    return out, mask

class Streamable(Dataset):
    def __init__(self, path: str, batch_size: int = 32):
        self.file = h5py.File(path, "r")
        self.batch_size = batch_size
        self.file_len = self.file["jets"].shape[0]

    def __len__(self):
        return len(self.file["jets"])

    def __getitem__(self, idx: int):
        jets = self.file["jets"][idx]
        csts_culens = self.file["csts_culens"][idx : idx + self.batch_size + 1]
        csts = self.file["csts"][csts_culens[0] : csts_culens[-1]]
        csts, mask = unpack(csts, csts_culens)
        return jets, csts, mask

if __name__ == "__main__":
    B, N, D = 1000, 100, 3
    jets = np.random.randn(B, N)
    csts = np.random.randn(B, N, D)
    mask = np.random.randn(B, N) > 0

    # Pack and save the data
    packed, culens = pack(csts, mask)
    with h5py.File("data.h5", "w") as f:
        f.create_dataset("csts", data=packed)
        f.create_dataset("csts_culens", data=culens)
        f.create_dataset("jets", data=jets)


    # Load and unpack the data
    with h5py.File("data.h5", "r") as f:
        csts2 = f["csts"][:]
        culens2 = f["csts_culens"][:]
    assert np.allclose(csts[mask], csts2)


    # Test loading a specific chunk
    start = 10
    end = 20
    with h5py.File("data.h5", "r") as f:
        culens3 = f["csts_culens"][start : end + 1]
        csts3 = f["csts"][culens3[0] : culens3[-1]]
    assert np.allclose(csts[start:end][mask[start:end]], csts3)


    dataset = Streamable("data.h5")
    print(len(dataset))
    print(dataset[0][1].shape)
    print(dataset[1][1].shape)
    print(dataset[999][1].shape)

    # Cleanup
    dataset.file.close()