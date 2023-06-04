# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""File utils."""


import os
from typing import Optional

from platformdirs import user_data_dir
from sklearn.datasets._base import RemoteFileMetadata, _fetch_remote


def get_and_create_mltb2_data_dir(mltb2_base_data_dir: Optional[str] = None) -> str:
    """Return and create mltb data dir."""
    if mltb2_base_data_dir is None:
        mltb2_data_dir = user_data_dir(appname="mltb2")
    else:
        mltb2_data_dir = os.path.join(mltb2_base_data_dir, "mltb2")
    if not os.path.exists(mltb2_data_dir):
        os.makedirs(mltb2_data_dir)
    return mltb2_data_dir


def fetch_remote_file(dirname, filename, url, sha256_checksum) -> str:
    remote = RemoteFileMetadata(filename=filename, url=url, checksum=sha256_checksum)
    fetch_remote_file_path = _fetch_remote(remote, dirname=dirname)
    return fetch_remote_file_path
