"""Module containing utility classes for the datamodule."""
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict
from collections.abc import Iterable

from torch import Tensor
from torch.utils.data import default_collate

from constants import JETS_COLUMNS
from src.torch_data.constants import CSTS_COLUMNS


class StreamData(TypedDict):
    """Dictionary containing data for a batch of jets."""
    jets: Tensor
    csts: Tensor
    split: Tensor


@dataclass
class StreamDataConfig:
    """Configuration for the stream dataset."""
    batch_size: int = 1000
    jet_features: list[str] | None = None
    csts_features: list[str] | None = None
    num_jets: int | None = None
    num_csts: int | None = None

    def __post_init__(self):
        if self.jet_features is None:
            self.jet_features = JETS_COLUMNS
        if self.csts_features is None:
            self.csts_features = CSTS_COLUMNS


@dataclass
class DataPaths:
    """Collection of paths to the datamodule."""
    train_path: Path | str
    val_path: Path | str
    test_path: Path | str | None = None
    predict_path: Path | str | None = None

    def __post_init__(self):
        if self.predict_path is None:
            self.predict_path = self.val_path


@dataclass
class DataLoaderConfig:
    """DataLoader configuration."""
    num_workers: int
    pin_memory: bool = True


def collate_and_transform(
    batch: Iterable[dict],
    do_default_collate: bool = True,
    transforms: list[callable] | None = None,
) -> dict:
    """Collate the batch and apply the transforms.

    Why this not lightning's on_before_batch_transfer?
    This still runs inside the pytorch multiprocessing pool for data loading.
    Thus it runs asynchonously for each batch being prepared.
    """
    if do_default_collate:
        batch = default_collate(batch)
    if transforms is not None:
        for transform in transforms:
            batch = transform(batch)
    return batch
