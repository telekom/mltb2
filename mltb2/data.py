# Copyright (c) 2020-2024 Philip May
# Copyright (c) 2021 Sigrun May, Helmholtz-Zentrum für Infektionsforschung GmbH (HZI)
# Copyright (c) 2021 Sigrun May, Ostfalia Hochschule für angewandte Wissenschaften
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""This module offers tools for loading data.

The following tabular data sets from the biological and medical domain are supported:

- colon: `<http://genomics-pubs.princeton.edu/oncology/affydata/index.html>`_
- prostate: `<https://web.stanford.edu/~hastie/CASI_files/DATA/prostate.html>`_
- leukemia_big: `<https://web.stanford.edu/~hastie/CASI_files/DATA/leukemia.html>`_

After loading the data from the internet it is parsed, converted and
cached in the mltb2 data directory.
This data directory is determined by :func:`mltb2.files.get_and_create_mltb2_data_dir`.

Hint:
    Use pip to install the necessary dependencies for this module:
    ``pip install mltb2[data]``
"""

import os
from hashlib import sha256
from io import StringIO
from typing import Optional, Tuple

import joblib
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

from mltb2.files import get_and_create_mltb2_data_dir


def _load_colon_data() -> pd.DataFrame:
    """Load colon data (not the labels).

    The data is loaded and parsed from the internet.
    Also see `<http://genomics-pubs.princeton.edu/oncology/affydata/index.html>`_.

    Returns:
        data as pandas DataFrame
    """
    # download data file
    url = "http://genomics-pubs.princeton.edu/oncology/affydata/I2000.html"
    page = requests.get(url, timeout=10)

    # check checksum of data file
    page_hash = sha256(page.content).hexdigest()
    assert page_hash == "74cc7b47d40a0fbca8dde05f42bcb799b7babad29ea634139a221bb4386b1c3d", page_hash

    soup = BeautifulSoup(page.content, "html.parser")
    page_text = soup.get_text()

    page_text_lines = page_text.splitlines()
    assert len(page_text_lines) >= 2000
    page_text_lines = [[float(s) for s in line.split()] for line in page_text_lines if len(line) > 20]
    assert len(page_text_lines) == 2000
    assert len(page_text_lines[0]) == 62

    data = np.array(page_text_lines).T
    data_df = pd.DataFrame(data)
    return data_df


def _load_colon_label() -> pd.Series:
    """Load colon label (not the data).

    The data is loaded and parsed from the internet.
    Also see `<http://genomics-pubs.princeton.edu/oncology/affydata/index.html>`_.

    Returns:
        labels as pandas Series
    """
    # download data file
    url = "http://genomics-pubs.princeton.edu/oncology/affydata/tissues.html"
    page = requests.get(url, timeout=10)

    # check checksum of data file
    page_hash = sha256(page.content).hexdigest()
    assert page_hash == "0c5b377c5dd5544d015bff479a4260d5ccf0bcf98657f600a1d37e34193e0f52", page_hash

    soup = BeautifulSoup(page.content, "html.parser")
    page_text = soup.get_text()
    page_text_lines = page_text.splitlines()

    label = []

    for line in page_text_lines:
        try:
            i = int(line)
            label.append(0 if i > 0 else 1)
        except ValueError:  # noqa: PERF203
            pass  # we ignore this

    assert len(label) == 62
    label_series = pd.Series(label)
    return label_series


def load_colon(mltb2_base_data_dir: Optional[str] = None) -> Tuple[pd.Series, pd.DataFrame]:
    """Load colon data.

    The data is loaded and parsed from the internet.
    Also see `<http://genomics-pubs.princeton.edu/oncology/affydata/index.html>`_.

    Args:
        mltb2_base_data_dir: The base data directory. If ``None`` the default
            user data directory is used. The default user data directory is
            determined by :func:`platformdirs.user_data_dir`.
    Returns:
        Tuple containing labels and data.
    """
    filename = "colon.pkl.gz"
    mltb2_data_home = get_and_create_mltb2_data_dir(mltb2_base_data_dir)
    full_path = os.path.join(mltb2_data_home, filename)
    if not os.path.exists(full_path):
        data_df = _load_colon_data()
        label_series = _load_colon_label()
        result = (label_series, data_df)
        joblib.dump(result, full_path, compress=("gzip", 3))
    else:
        result = joblib.load(full_path)

    return result


def load_prostate(mltb2_base_data_dir: Optional[str] = None) -> Tuple[pd.Series, pd.DataFrame]:
    """Load prostate data.

    The data is loaded and parsed from `<https://web.stanford.edu/~hastie/CASI_files/DATA/prostate.html>`_.

    Args:
        mltb2_base_data_dir: The base data directory. If ``None`` the default
            user data directory is used. The default user data directory is
            determined by :func:`platformdirs.user_data_dir`.
    Returns:
        Tuple containing labels and data.
    """
    filename = "prostate.pkl.gz"
    mltb2_data_home = get_and_create_mltb2_data_dir(mltb2_base_data_dir)
    full_path = os.path.join(mltb2_data_home, filename)
    if not os.path.exists(full_path):
        # download data file
        url = "https://web.stanford.edu/~hastie/CASI_files/DATA/prostmat.csv"
        page = requests.get(url, timeout=10)
        page_str = page.text

        # check checksum of data file
        page_hash = sha256(page_str.encode("utf-8")).hexdigest()
        assert page_hash == "f1ccfd3c9a837c002ec5d6489ab139c231739c3611189be14d15ca5541b92036", page_hash

        data_df = pd.read_csv(StringIO(page_str))
        data_df = data_df.T

        labels = []
        for label in data_df.index:
            if "control" in label:
                labels.append(0)
            elif "cancer" in label:
                labels.append(1)
            else:
                assert False, f"This must not happen! label: {label}"
        label_series = pd.Series(labels)
        assert len(label_series) == 102

        data_df = data_df.reset_index(drop=True)  # reset the index to default integer index
        assert data_df.shape == (102, 6033)

        result = (label_series, data_df)
        joblib.dump(result, full_path, compress=("gzip", 3))
    else:
        result = joblib.load(full_path)
    return result


def load_leukemia_big(mltb2_base_data_dir: Optional[str] = None) -> Tuple[pd.Series, pd.DataFrame]:
    """Load leukemia (big) data.

    The data is loaded and parsed from the internet.
    Also see `<https://web.stanford.edu/~hastie/CASI_files/DATA/leukemia.html>`_.

    Args:
        mltb2_base_data_dir: The base data directory. If ``None`` the default
            user data directory is used. The default user data directory is
            determined by :func:`platformdirs.user_data_dir`.
    Returns:
        Tuple containing labels and data.
    """
    filename = "leukemia_big.pkl.gz"
    mltb2_data_home = get_and_create_mltb2_data_dir(mltb2_base_data_dir)
    full_path = os.path.join(mltb2_data_home, filename)
    if not os.path.exists(full_path):
        # download data file
        url = "https://web.stanford.edu/~hastie/CASI_files/DATA/leukemia_big.csv"
        page = requests.get(url, timeout=10)
        page_str = page.text

        # check checksum of data file
        page_hash = sha256(page_str.encode("utf-8")).hexdigest()
        assert page_hash == "35e84928da625da0787efb31a451dedbdf390e821a94ef74b7b7ab6cab9466d4", page_hash

        data_df = pd.read_csv(StringIO(page_str))
        data_df = data_df.T

        labels = []
        for label in data_df.index:
            if "ALL" in label:
                labels.append(0)
            elif "AML" in label:
                labels.append(1)
            else:
                assert False, f"This must not happen! label: {label}"
        label_series = pd.Series(labels)
        assert len(label_series) == 72

        data_df = data_df.reset_index(drop=True)  # reset the index to default integer index
        assert data_df.shape == (72, 7128)

        result = (label_series, data_df)
        joblib.dump(result, full_path, compress=("gzip", 3))
    else:
        result = joblib.load(full_path)
    return result
