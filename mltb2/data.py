# Copyright (c) 2020 - 2023 Philip May
# Copyright (c) 2021 Sigrun May, Helmholtz-Zentrum für Infektionsforschung GmbH (HZI)
# Copyright (c) 2021 Sigrun May, Ostfalia Hochschule für angewandte Wissenschaften
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""Data loading functionality."""

import os
from hashlib import sha256
from typing import Tuple

import joblib
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

from mltb2.files import get_and_create_mltb2_data_dir


def _load_colon_data() -> pd.DataFrame:
    """Load colon data (not the labels).

    The data is loaded and parsed from the internet.
    Also see `colon tissues probed by oligonucleotide arrays
    <http://genomics-pubs.princeton.edu/oncology/affydata/index.html>`_.

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
    Also see `colon tissues probed by oligonucleotide arrays
    <http://genomics-pubs.princeton.edu/oncology/affydata/index.html>`_.

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
        except ValueError:
            pass  # we ignore this

    assert len(label) == 62
    label_series = pd.Series(label)
    return label_series


def load_colon() -> Tuple[pd.Series, pd.DataFrame]:
    """Load colon data.

    The data is loaded and parsed from the internet.
    Also see `colon tissues probed by oligonucleotide arrays
    <http://genomics-pubs.princeton.edu/oncology/affydata/index.html>`_.

    Returns:
        Tuple containing labels and data.
    """
    filename = "colon.pkl.gz"
    mltb2_data_home = get_and_create_mltb2_data_dir()
    full_path = os.path.join(mltb2_data_home, filename)
    if not os.path.exists(full_path):
        data_df = _load_colon_data()
        label_series = _load_colon_label()
        result = (label_series, data_df)
        joblib.dump(result, full_path, compress=("gzip", 3))
    else:
        result = joblib.load(full_path)

    return result
