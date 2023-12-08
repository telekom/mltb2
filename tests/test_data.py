# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

import pandas as pd

from mltb2.data import _load_colon_data, _load_colon_label


def test_load_colon_data():
    result = _load_colon_data()
    assert result is not None
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (62, 2000)


def test_load_colon_label():
    result = _load_colon_label()
    assert result is not None
    assert isinstance(result, pd.Series)
    assert len(result) == 62
