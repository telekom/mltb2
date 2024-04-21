# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

import os

import pytest

from mltb2.files import fetch_remote_file, get_and_create_mltb2_data_dir


def test_fetch_remote_file(tmpdir):
    filename = "LICENSE.txt"
    remote_file = fetch_remote_file(
        dirname=tmpdir,
        filename=filename,
        url="https://raw.githubusercontent.com/telekom/mltb2/main/LICENSE",
        sha256_checksum="733fe19287807e392fc0899a1577fa36bad2ab543efdce372a2fc05399b91c2f",
    )
    assert remote_file == os.path.join(tmpdir, filename)
    assert os.path.exists(os.path.join(tmpdir, filename))


def test_fetch_remote_file_wrong_checksum(tmpdir):
    filename = "LICENSE.txt"
    with pytest.raises(IOError):
        _ = fetch_remote_file(
            dirname=tmpdir,
            filename=filename,
            url="https://raw.githubusercontent.com/telekom/mltb2/main/LICENSE",
            sha256_checksum="wrong",
        )
    assert not os.path.exists(os.path.join(tmpdir, filename))


def test_get_and_create_mltb2_data_dir(tmpdir):
    mltb2_data_dir = get_and_create_mltb2_data_dir(tmpdir)

    assert mltb2_data_dir == os.path.join(tmpdir, "mltb2")
