# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

import pandas as pd

from mltb2.data import _load_colon_data, _load_colon_label, load_colon, load_leukemia_big, load_prostate


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


def test_load_colon():
    result = load_colon()
    assert result is not None
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], pd.Series)
    assert isinstance(result[1], pd.DataFrame)
    assert result[0].shape == (62,)
    assert result[1].shape == (62, 2000)


def test_load_prostate():
    result = load_prostate()
    assert result is not None
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], pd.Series)
    assert isinstance(result[1], pd.DataFrame)
    assert result[0].shape == (102,)
    assert result[1].shape == (102, 6033)


def test_load_leukemia_big():
    result = load_leukemia_big()
    assert result is not None
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], pd.Series)
    assert isinstance(result[1], pd.DataFrame)
    assert result[0].shape == (72,)
    assert result[1].shape == (72, 7128)
