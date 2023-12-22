# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

import pandas as pd
import pytest
from numpy.testing import assert_almost_equal

from mltb2.data import _load_colon_data, _load_colon_label, load_colon, load_leukemia_big, load_prostate

from .ori_data_loader import load_colon_data, load_leukemia_data, load_prostate_data


def test_load_colon_data():
    result = _load_colon_data()  # only load data not labels
    assert result is not None
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (62, 2000)


def test_load_colon_label():
    result = _load_colon_label()  # only load labels not data
    assert result is not None
    assert isinstance(result, pd.Series)
    assert len(result) == 62


def test_load_colon(tmpdir):
    result = load_colon(tmpdir)
    assert result is not None
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], pd.Series)
    assert isinstance(result[1], pd.DataFrame)
    assert result[0].shape == (62,)
    assert result[1].shape == (62, 2000)


def test_load_colon_compare_original(tmpdir):
    result = load_colon(tmpdir)
    ori_result = load_colon_data()
    assert result[0].shape == ori_result[0].shape
    assert result[1].shape == ori_result[1].shape
    assert_almost_equal(result[0].to_numpy(), ori_result[0].to_numpy())
    assert_almost_equal(result[1].to_numpy(), ori_result[1].to_numpy())


def test_load_prostate(tmpdir):
    result = load_prostate(tmpdir)
    assert result is not None
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], pd.Series)
    assert isinstance(result[1], pd.DataFrame)
    assert result[0].shape == (102,)
    assert result[1].shape == (102, 6033)


def test_load_prostate_compare_original(tmpdir):
    result = load_prostate(tmpdir)
    ori_result = load_prostate_data()
    assert result[0].shape == ori_result[0].shape
    assert result[1].shape == ori_result[1].shape
    assert_almost_equal(result[0].to_numpy(), ori_result[0].to_numpy())
    assert_almost_equal(result[1].to_numpy(), ori_result[1].to_numpy())


def test_load_leukemia_big(tmpdir):
    result = load_leukemia_big(tmpdir)
    assert result is not None
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], pd.Series)
    assert isinstance(result[1], pd.DataFrame)
    assert result[0].shape == (72,)
    assert result[1].shape == (72, 7128)


def test_load_leukemia_big_compare_original(tmpdir):
    result = load_leukemia_big(tmpdir)
    ori_result = load_leukemia_data()
    assert result[0].shape == ori_result[0].shape
    assert result[1].shape == ori_result[1].shape
    assert_almost_equal(result[0].to_numpy(), ori_result[0].to_numpy())
    assert_almost_equal(result[1].to_numpy(), ori_result[1].to_numpy())
