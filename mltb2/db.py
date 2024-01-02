# Copyright (c) 2023-2024 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""Database utils module."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Sequence


class AbstractBatchDataManager(ABC):
    """Abstract base class for batch processing of database data.

    This class (respectively an implementation of it) is intended to be
    used in conjunction with the :class:`BatchDataProcessor`.
    """

    @abstractmethod
    def load_batch(self) -> Sequence:
        """Load a batch of data from the database."""

    @abstractmethod
    def save_batch(self, batch: Sequence) -> None:
        """Save a batch of data to the database."""


@dataclass
class BatchDataProcessor:
    """Process batches of data from a database.

    Args:
        data_manager: The data manager to load and save batches of data.
        process_batch_callback: A callback function that processes one batch of data.
    """

    data_manager: AbstractBatchDataManager
    process_batch_callback: Callable[[Sequence], Sequence]

    def run(self) -> None:
        """Run the batch data processing.

        This is done until the data manager returns an empty batch.
        For each batch the ``process_batch_callback`` is called.
        Data is loaded by using an implementation of the :class:`AbstractBatchDataManager`.
        """
        while True:
            batch = self.data_manager.load_batch()
            if len(batch) == 0:
                break
            new_batch = self.process_batch_callback(batch)
            if len(new_batch) > 0:
                self.data_manager.save_batch(new_batch)
