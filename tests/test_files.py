# Copyright (c) 2023-2024 Philip May
# Copyright (c) 2023-2024 Philip May, Deutsche Telekom AG
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

import os
import shutil
from uuid import uuid4

import pytest

from mltb2.files import FileBasedRestartableBatchDataProcessor, fetch_remote_file, get_and_create_mltb2_data_dir


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


def test_FileBasedRestartableBatchDataProcessor_batch_size(tmp_path):
    result_dir = tmp_path.absolute()
    with pytest.raises(ValueError):
        _ = FileBasedRestartableBatchDataProcessor(data=[], batch_size=0, uuid_name="uuid", result_dir=result_dir)


def test_FileBasedRestartableBatchDataProcessor_empty_data(tmp_path):
    result_dir = tmp_path.absolute()
    with pytest.raises(ValueError):
        _ = FileBasedRestartableBatchDataProcessor(data=[], batch_size=10, uuid_name="uuid", result_dir=result_dir)


def test_FileBasedRestartableBatchDataProcessor_uuid_in_data(tmp_path):
    result_dir = tmp_path.absolute()
    with pytest.raises(ValueError):
        _ = FileBasedRestartableBatchDataProcessor(
            data=[{"x": 10}], batch_size=10, uuid_name="uuid", result_dir=result_dir
        )


def test_FileBasedRestartableBatchDataProcessor_uuid_type(tmp_path):
    result_dir = tmp_path.absolute()
    with pytest.raises(TypeError):
        _ = FileBasedRestartableBatchDataProcessor(
            data=[{"uuid": 6, "x": 10}], batch_size=10, uuid_name="uuid", result_dir=result_dir
        )


def test_FileBasedRestartableBatchDataProcessor_uuid_empty(tmp_path):
    result_dir = tmp_path.absolute()
    with pytest.raises(ValueError):
        _ = FileBasedRestartableBatchDataProcessor(
            data=[{"uuid": "", "x": 10}], batch_size=10, uuid_name="uuid", result_dir=result_dir
        )


def test_FileBasedRestartableBatchDataProcessor_uuid_unique(tmp_path):
    result_dir = tmp_path.absolute()
    data = [{"uuid": "a", "x": 10}, {"uuid": "a", "x": 10}, {"uuid": "c", "x": 10}]
    with pytest.raises(ValueError):
        _ = FileBasedRestartableBatchDataProcessor(data=data, batch_size=10, uuid_name="uuid", result_dir=result_dir)


def test_FileBasedRestartableBatchDataProcessor_write_lock_files(tmp_path):
    result_dir = tmp_path.absolute()
    batch_size = 10
    data = [{"uuid": str(uuid4()), "x": i} for i in range(100)]
    data_processor = FileBasedRestartableBatchDataProcessor(
        data=data, batch_size=batch_size, uuid_name="uuid", result_dir=result_dir
    )
    data = data_processor.read_batch()

    assert len(data) == batch_size

    # check lock files
    lock_files = list(tmp_path.glob("*.lock"))
    assert len(lock_files) == batch_size


def test_FileBasedRestartableBatchDataProcessor_save_batch_data(tmp_path):
    result_dir = tmp_path.absolute()
    batch_size = 10
    data = [{"uuid": str(uuid4()), "x": i} for i in range(100)]
    data_processor = FileBasedRestartableBatchDataProcessor(
        data=data, batch_size=batch_size, uuid_name="uuid", result_dir=result_dir
    )
    data = data_processor.read_batch()
    data_processor.save_batch(data)

    # check lock files
    lock_files = list(tmp_path.glob("*.pkl.gz"))
    assert len(lock_files) == batch_size


def test_FileBasedRestartableBatchDataProcessor_remove_lock_files(tmp_path):
    result_dir = tmp_path.absolute()
    batch_size = 10
    data = [{"uuid": str(uuid4()), "x": i} for i in range(100)]
    data_processor = FileBasedRestartableBatchDataProcessor(
        data=data, batch_size=batch_size, uuid_name="uuid", result_dir=result_dir
    )
    data = data_processor.read_batch()
    data_processor.save_batch(data)

    # check lock files
    lock_files = list(tmp_path.glob("*.lock"))
    assert len(lock_files) == 0


def test_FileBasedRestartableBatchDataProcessor_save_unlocked(tmp_path):
    result_dir = tmp_path.absolute()
    batch_size = 10
    data = [{"uuid": str(uuid4()), "x": i} for i in range(100)]
    data_processor = FileBasedRestartableBatchDataProcessor(
        data=data, batch_size=batch_size, uuid_name="uuid", result_dir=result_dir
    )
    data = data_processor.read_batch()
    data[0]["uuid"] = "something_else"
    with pytest.raises(ValueError):
        data_processor.save_batch(data)


def test_FileBasedRestartableBatchDataProcessor_load_data(tmp_path):
    result_dir = tmp_path.absolute()
    batch_size = 10
    data = [{"uuid": str(uuid4()), "x": i} for i in range(100)]
    data_processor = FileBasedRestartableBatchDataProcessor(
        data=data, batch_size=batch_size, uuid_name="uuid", result_dir=result_dir
    )

    # process all data
    while True:
        _data = data_processor.read_batch()
        if len(_data) == 0:
            break
        data_processor.save_batch(_data)

    del data_processor
    processed_data = FileBasedRestartableBatchDataProcessor.load_data(result_dir)

    assert len(processed_data) == len(data)
    for d in processed_data:
        assert "uuid" in d
        assert "x" in d
        assert isinstance(d["uuid"], str)
        assert isinstance(d["x"], int)
        assert d["x"] < 100


def test_FileBasedRestartableBatchDataProcessor_load_data_no_duplicate(tmp_path):
    result_dir = tmp_path.absolute()
    batch_size = 10
    data = [{"uuid": str(uuid4()), "x": i} for i in range(100)]
    data_processor = FileBasedRestartableBatchDataProcessor(
        data=data, batch_size=batch_size, uuid_name="uuid", result_dir=result_dir
    )

    # process all data
    while True:
        _data = data_processor.read_batch()
        if len(_data) == 0:
            break
        data_processor.save_batch(_data)

    del data_processor

    result_file = list(tmp_path.glob("*.pkl.gz"))[0].as_posix()
    # copy result file to create a duplicate
    duplicate_result_file = result_file.replace(".pkl.gz", "#duplicate.pkl.gz")
    shutil.copyfile(result_file, duplicate_result_file)

    processed_data = FileBasedRestartableBatchDataProcessor.load_data(result_dir)

    assert len(processed_data) == len(data)
    for d in processed_data:
        assert "uuid" in d
        assert "x" in d
        assert isinstance(d["uuid"], str)
        assert isinstance(d["x"], int)
        assert d["x"] < 100


def test_FileBasedRestartableBatchDataProcessor_unknown_file(tmp_path):
    result_dir = tmp_path.absolute()
    batch_size = 10
    data = [{"uuid": str(uuid4()), "x": i} for i in range(100)]
    data_processor = FileBasedRestartableBatchDataProcessor(
        data=data, batch_size=batch_size, uuid_name="uuid", result_dir=result_dir
    )

    # place unknown file
    (tmp_path / "some_unknown_file.txt").touch()

    data = data_processor.read_batch()
