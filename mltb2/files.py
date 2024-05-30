# Copyright (c) 2023-2024 Philip May
# Copyright (c) 2023-2024 Philip May, Deutsche Telekom AG
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""File utils module.

This module provides utility functions for other modules.

Hint:
    Use pip to install the necessary dependencies for this module:
    ``pip install mltb2[files]``
"""


import contextlib
import os
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set
from uuid import uuid4

import joblib
from platformdirs import user_data_dir
from sklearn.datasets._base import RemoteFileMetadata, _fetch_remote


def get_and_create_mltb2_data_dir(mltb2_base_data_dir: Optional[str] = None) -> str:
    """Return and create a data dir for mltb2.

    The exact directory is given by the ``mltb2_base_data_dir`` as the base folder
    and then the folder ``mltb2`` is appended.

    Args:
        mltb2_base_data_dir: The base data directory. If ``None`` the default
            user data directory is used. The default user data directory is
            determined by :func:`platformdirs.user_data_dir`.

    Returns:
        The directory path.
    """
    if mltb2_base_data_dir is None:
        mltb2_data_dir = user_data_dir(appname="mltb2")
    else:
        mltb2_data_dir = os.path.join(mltb2_base_data_dir, "mltb2")
    if not os.path.exists(mltb2_data_dir):
        os.makedirs(mltb2_data_dir)
    return mltb2_data_dir


def fetch_remote_file(dirname, filename, url: str, sha256_checksum: str) -> str:
    """Fetch a file from a remote URL.

    Args:
        dirname: the directory where the file will be saved
        filename: the filename under which the file will be saved
        url: the url of the file
        sha256_checksum: the sha256 checksum of the file
    Returns:
        Full path of the created file.
    Raises:
        IOError: if the sha256 checksum is wrong
    """
    remote = RemoteFileMetadata(filename=filename, url=url, checksum=sha256_checksum)
    try:
        fetch_remote_file_path = _fetch_remote(remote, dirname=dirname)
    except Exception:
        with contextlib.suppress(FileNotFoundError):
            os.remove(os.path.join(dirname, filename))
        raise
    return fetch_remote_file_path


@dataclass
class FileBasedRestartableBatchDataProcessor:
    """Batch data processor which supports restartability and is backed by files.

    Args:
        data: The data to process.
        batch_size: The batch size.
        uuid_name: The name of the uuid field in the data.
        result_dir: The directory where the results are stored.
    """

    data: List[Dict[str, Any]]
    batch_size: int
    uuid_name: str
    result_dir: str
    _result_dir_path: Path = field(init=False, repr=False)
    _own_lock_uuids: Set[str] = field(init=False, repr=False, default_factory=set)

    def __post_init__(self) -> None:
        """Do post init."""
        # check that batch size is > 0
        if self.batch_size <= 0:
            raise ValueError("batch_size must be > 0!")

        if not len(self.data) > 0:
            raise ValueError("data must not be empty!")

        uuids: Set[str] = set()

        # check uuid_name
        for idx, d in enumerate(self.data):
            if self.uuid_name not in d:
                raise ValueError(f"uuid_name '{self.uuid_name}' not available in data at index {idx}!")
            uuid = d[self.uuid_name]
            if not isinstance(uuid, str):
                raise TypeError(f"uuid '{uuid}' at index {idx} is not a string!")
            if len(uuid) == 0:
                raise ValueError(f"uuid '{uuid}' at index {idx} is empty!")
            uuids.add(uuid)

        if len(uuids) != len(self.data):
            raise ValueError("uuids are not unique!")

        # create and check _result_dir_path
        self._result_dir_path = Path(self.result_dir)
        self._result_dir_path.mkdir(parents=True, exist_ok=True)  # create directory if not available
        if not self._result_dir_path.is_dir():
            raise ValueError(f"Faild to create or find result_dir '{self.result_dir}'!")

    def __len__(self) -> int:
        """Return the number of data records."""
        return len(self.data)

    @staticmethod
    def _get_uuid_from_filename(filename: str) -> Optional[str]:
        uuid = None
        if filename.endswith(".lock"):
            uuid = filename[: filename.rindex(".lock")]
        elif filename.endswith(".pkl.gz") and "_" in filename:
            uuid = filename[: filename.rindex("_")]
        return uuid

    def _get_locked_or_done_uuids(self) -> Set[str]:
        locked_or_done_uuids: Set[str] = set()
        for child_path in self._result_dir_path.iterdir():
            if child_path.is_file():
                filename = child_path.name
                uuid = FileBasedRestartableBatchDataProcessor._get_uuid_from_filename(filename)
                if uuid is not None:
                    locked_or_done_uuids.add(uuid)
        return locked_or_done_uuids

    def _write_lock_files(self, batch: Sequence[Dict[str, Any]]) -> None:
        for d in batch:
            uuid = d[self.uuid_name]
            (self._result_dir_path / f"{uuid}.lock").touch()
            self._own_lock_uuids.add(uuid)

    def _get_remaining_data(self) -> List[Dict[str, Any]]:
        locked_or_done_uuids: Set[str] = self._get_locked_or_done_uuids()
        remaining_data = [d for d in self.data if d[self.uuid_name] not in locked_or_done_uuids]
        return remaining_data

    def read_batch(self) -> Sequence[Dict[str, Any]]:
        """Read the next batch of data."""
        remaining_data: List[Dict[str, Any]] = self._get_remaining_data()

        # if we think we are done, delete all lock files and check again
        # this is because lock files might be orphaned
        if len(remaining_data) == 0:
            for lock_file_path in self._result_dir_path.glob("*.lock"):
                lock_file_path.unlink(missing_ok=True)
            remaining_data = self._get_remaining_data()

        random.shuffle(remaining_data)
        next_batch_size = min(self.batch_size, len(remaining_data))
        next_batch = remaining_data[:next_batch_size]
        self._write_lock_files(next_batch)
        return next_batch

    def _save_batch_data(self, batch: Sequence[Dict[str, Any]]) -> None:
        for d in batch:
            uuid = d[self.uuid_name]
            if uuid not in self._own_lock_uuids:
                raise ValueError(f"uuid '{uuid}' not locked by me!")
            filename = self._result_dir_path / f"{uuid}_{str(uuid4())}.pkl.gz"  # noqa: RUF010
            joblib.dump(d, filename, compress=("gzip", 3))

    def _remove_lock_files(self, batch: Sequence[Dict[str, Any]]) -> None:
        for d in batch:
            uuid = d[self.uuid_name]
            (self._result_dir_path / f"{uuid}.lock").unlink(missing_ok=True)
            self._own_lock_uuids.discard(uuid)

    def save_batch(self, batch: Sequence[Dict[str, Any]]) -> None:
        """Save the batch of data."""
        self._save_batch_data(batch)
        self._remove_lock_files(batch)

    @staticmethod
    def load_data(result_dir: str, ignore_load_error: bool = False) -> List[Dict[str, Any]]:
        """Load all data.

        After all data is processed, this method can be used to load all data.
        As the FileBasedRestartableBatchDataProcessor may be executed several times in parallel,
        data records may exist in duplicate. These duplicates are removed here.

        Args:
            result_dir: The directory where the results are stored.
            ignore_load_error: Ignore errors when loading the result files. Just print them.
        """
        _result_dir_path = Path(result_dir)
        if not _result_dir_path.is_dir():
            raise ValueError(f"Did not find result_dir '{result_dir}'!")

        data = []
        uuids = set()
        for child_path in _result_dir_path.iterdir():
            if child_path.is_file() and child_path.name.endswith(".pkl.gz"):
                uuid = FileBasedRestartableBatchDataProcessor._get_uuid_from_filename(child_path.name)
                if uuid not in uuids:

                    d = None
                    try:
                        d = joblib.load(child_path)
                    except Exception as e:
                        if ignore_load_error:
                            print(f"Error loading file '{child_path}': {e}")
                        else:
                            raise e  # NOQA: TRY201

                    if d is not None:
                        uuids.add(uuid)
                        data.append(d)
        return data
