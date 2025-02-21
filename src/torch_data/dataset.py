from dataclasses import asdict
import logging

import numpy as np
import torch
from typing import Callable
from constants import CSTS_COLUMNS_LOOKUP, JETS_COLUMNS_LOOKUP

import h5py
from lightning import LightningDataModule
from torch.utils.data import DataLoader, Dataset

from utils import StreamData, StreamDataConfig, DataPaths, DataLoaderConfig


logger = logging.getLogger(__name__)


def batch_idxes(
        batch_size: int,
        num_jets: int,
        drop_last: bool = False,
        start: int = 0,
) -> list:
    """Construct a generator of batch indexes."""
    drop_last &= num_jets % batch_size != 0
    return list(range(start, num_jets - drop_last * batch_size, batch_size))


class StreamDataset(Dataset):
    """Streams in jets from a single large HDF file.

    Due to the speed of reading from disk which is a bottleneck, we read in a single
    slice, i.e. a batch of jets, at a time.
    """

    def __init__(
            self,
            file_path: str,
            jet_features: list[str],
            csts_features: list[str],
            num_jets: int | None = None,
            num_csts: int | None = None,
            batch_size: int = 1000,
    ) -> None:
        """Creates a new StreamDataset.

        Args:
            file_path:
            jet_features:
            csts_features:
            num_jets:
            num_csts:
            batch_size:
        """
        self.jet_features = jet_features
        self.csts_features = csts_features
        self.batch_size = batch_size

        # Open the file and calculate the length.
        self.file = h5py.File(file_path, mode="r")
        self.length_indices = np.array(self.file["csts_culens"])

        # Trim the features to those present in the file so we don't do it every time.
        self.jet_indices = [
            JETS_COLUMNS_LOOKUP[feature_name] for feature_name in jet_features
        ]
        self.csts_indices = [
            CSTS_COLUMNS_LOOKUP[feature_name] for feature_name in csts_features
        ]

        self.num_jets = self._get_num_jets(num_jets)
        self.num_csts = self._get_num_csts(num_csts)

    def _verify_features(self, jet_features: list[str], csts_features: list[str]) -> None:
        """Verify the features are present in the file."""
        jet_features = set(jet_features)
        csts_features = set(csts_features)

        for feature in jet_features:
            if feature not in JETS_COLUMNS_LOOKUP:
                logger.warning(f"Feature {feature} not a recognized JETS column.")

        for feature in csts_features:
            if feature not in CSTS_COLUMNS_LOOKUP:
                logger.warning(f"Feature {feature} not a recognized CSTS column.")

    def _get_num_jets(self, num_jets: int | None) -> int:
        file_len = len(self.length_indices) - 1  # Last index is the end of the file.
        if num_jets is None:
            return file_len
        return min(file_len, num_jets)

    def _get_num_csts(self, num_csts: int | None) -> int:
        file_len = len(self.length_indices) - 1  # Last index is the end of the file.
        if num_csts is None:
            return file_len
        return min(file_len, num_csts)

    def __len__(self) -> int:
        return self.num_jets

    def __getitem__(self, idx: int) -> StreamData:
        """Get a batch of jets."""
        idx_f = idx + self.batch_size

        start_jet_idx = self.length_indices[idx]
        end_jet_idx = self.length_indices[idx_f]

        jets = np.array(self.file["jets"][start_jet_idx: end_jet_idx])
        jets = jets[:, self.jet_indices]
        csts = np.array(self.file["csts"][idx: idx_f])
        csts = csts[:, self.csts_indices]
        split = self.length_indices[idx: idx_f] - start_jet_idx
        return {
            "jets": torch.from_numpy(jets),
            "csts": torch.from_numpy(csts),
            "split": torch.from_numpy(split),
        }


class StreamModule(LightningDataModule):
    def __init__(
            self,
            *,
            n_classes: int,
            data_paths: DataPaths,
            loader_config: DataLoaderConfig,
            data_config: StreamDataConfig | None = None,
            transforms: list[Callable[[StreamData], StreamData]] | None = None,
    ) -> None:
        super().__init__()

        data_config = data_config if data_config is not None else StreamDataConfig()

        self._data_paths = data_paths
        self._data_config: StreamDataConfig = data_config
        self._loader_config = loader_config

        self.n_classes = n_classes
        self.transforms = transforms
        self.batch_idx = 0

        # Initialise the validation set now to get a sample.
        self.valid_set = StreamDataset(self.val_path, **asdict(self._data_config))  # type: ignore

    @property
    def train_path(self) -> str:
        return self._data_paths.train_path

    @property
    def val_path(self) -> str:
        return self._data_paths.val_path

    @property
    def test_path(self) -> str:
        return self._data_paths.test_path

    @property
    def predict_path(self) -> str:
        return self._data_paths.test_path

    @property
    def batch_size(self) -> int:
        return self._data_config.batch_size

    def setup(self, stage: str) -> None:
        """Sets up the relevant datasets."""
        if stage in {"fit", "train"}:
            self.train_set = StreamDataset(self.train_path, **asdict(self._data_config))  # type: ignore
        if stage == "test":
            self.test_set = StreamDataset(self.test_path, **asdict(self._data_config))  # type: ignore
        if stage == "predict":
            self.predict_set = StreamDataset(self.test_path, **asdict(self._data_config))  # type: ignore

    def get_dataloader(self, dataset: StreamDataset, flag: str) -> DataLoader:
        return DataLoader(
            dataset=dataset,
            sampler=batch_idxes(
                self.batch_size,
                len(dataset),
                drop_last=flag == "train",
                start=self.batch_idx,
            ),
            batch_size=None,  # dataset returns a batches already!
            collate_fn=None,
            **asdict(self._loader_config),  # type: ignore
        )

    def train_dataloader(self) -> DataLoader:
        return self.get_dataloader(self.train_set, "train")

    def val_dataloader(self) -> DataLoader:
        return self.get_dataloader(self.valid_set, "val")

    def test_dataloader(self) -> DataLoader:
        return self.get_dataloader(self.test_set, "test")

    def predict_dataloader(self) -> DataLoader:
        return self.test_dataloader()

    def on_before_batch_transfer(self, batch: StreamData, dataloader_idx: int) -> StreamData:
        """Update the last batch index during validation."""
        if self.trainer.validating:
            self.batch_idx = self.trainer.global_step // self.trainer.current_epoch
        if self.transforms is not None:
            for transform in self.transforms:
                batch = transform(batch)
        return batch

    def get_data_sample(self) -> StreamData:
        """Get a data sample to help initialise the network."""
        return next(iter(self.valid_set))

    def load_state_dict(self, state_dict: dict) -> None:
        self.batch_idx = state_dict["batch_idx"]

    def state_dict(self) -> dict:
        return {"batch_idx": self.batch_idx}

    def get_n_classes(self) -> int:
        """Get the number of classes in the dataset."""
        return self.n_classes


if __name__ == "__main__":
    dm = StreamModule(
        n_classes=10,
        data_paths=DataPaths(
            train_path=(path := "/srv/beegfs/scratch/groups/rodem/ATLASOpenData/ttbar.h5"),
            val_path=path,
            test_path=path,
        ),
        loader_config=DataLoaderConfig(num_workers=4, pin_memory=True),
    )
    dm.setup("fit")
    tl = dm.train_dataloader()
    print(b := next(iter(tl)))
    print(b["csts"].shape)
    print(len(tl))
