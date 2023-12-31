# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""Database utils module.

This module provides utility functions for other modules.
It is not meant to be used directly.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Sequence


class BatchDataManager(ABC):
    """TODO: add docstring."""

    @abstractmethod
    def load_batch(self) -> Sequence:
        """TODO: add docstring."""
        pass

    @abstractmethod
    def save_batch(self, batch: Sequence) -> None:
        """TODO: add docstring."""
        pass


@dataclass
class BatchDataProcessor:
    """TODO: add docstring."""

    data_manager: BatchDataManager
    process_batch_callback: Callable[[Sequence], Sequence]

    def run(self) -> None:
        """TODO: add docstring."""
        while True:
            batch = self.data_manager.load_batch()
            if len(batch) == 0:
                break
            new_batch = self.process_batch_callback(batch)
            if len(new_batch) > 0:
                self.data_manager.save_batch(new_batch)
