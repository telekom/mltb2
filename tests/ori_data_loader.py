# Copyright (c) 2021 Sigrun May, Helmholtz-Zentrum für Infektionsforschung GmbH (HZI)
# Copyright (c) 2021 Sigrun May, Ostfalia Hochschule für angewandte Wissenschaften
# Copyright (c) 2020 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

# this is the original implementation from
# https://github.com/sigrun-may/cv-pruner/blob/ac35eba88a824e6bb6a6435cda67224a4db69e65/examples/data_loader.py

"""Data loader module."""

from typing import Tuple

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup


def load_colon_data() -> Tuple[pd.Series, pd.DataFrame]:
    """Load colon data.

    The data is loaded and parsed from the internet.
    Also see <http://genomics-pubs.princeton.edu/oncology/affydata/index.html>

    Returns:
        Tuple containing labels and data.
    """
    html_data = "http://genomics-pubs.princeton.edu/oncology/affydata/I2000.html"

    page = requests.get(html_data, timeout=10)

    soup = BeautifulSoup(page.content, "html.parser")
    colon_text_data = soup.get_text()

    colon_text_data_lines = colon_text_data.splitlines()
    colon_text_data_lines = [[float(s) for s in line.split()] for line in colon_text_data_lines if len(line) > 20]
    assert len(colon_text_data_lines) == 2000
    assert len(colon_text_data_lines[0]) == 62

    data = np.array(colon_text_data_lines).T

    html_label = "http://genomics-pubs.princeton.edu/oncology/affydata/tissues.html"
    page = requests.get(html_label, timeout=10)
    soup = BeautifulSoup(page.content, "html.parser")
    colon_text_label = soup.get_text()
    colon_text_label = colon_text_label.splitlines()

    label = []

    for line in colon_text_label:
        try:
            i = int(line)
            label.append(0 if i > 0 else 1)
        except:  # noqa: S110, E722
            pass

    assert len(label) == 62

    data_df = pd.DataFrame(data)

    # generate feature names
    column_names = []
    for column_name in data_df.columns:
        column_names.append("gene_" + str(column_name))

    data_df.columns = column_names

    return pd.Series(label), data_df


# TODO append random features and shuffle


def load_prostate_data() -> Tuple[pd.Series, pd.DataFrame]:
    """Load prostate data.

    The data is loaded and parsed from <https://web.stanford.edu/~hastie/CASI_files/DATA/prostate.html>

    Returns:
        Tuple containing labels and data.
    """
    df = pd.read_csv("https://web.stanford.edu/~hastie/CASI_files/DATA/prostmat.csv")
    data = df.T

    # labels
    labels = []
    for label in df.columns:  # pylint:disable=no-member
        if "control" in label:
            labels.append(0)
        elif "cancer" in label:
            labels.append(1)
        else:
            assert False, "This must not happen!"

    assert len(labels) == 102
    assert data.shape == (102, 6033)

    return pd.Series(labels), data


def load_leukemia_data() -> Tuple[pd.Series, pd.DataFrame]:
    """Load leukemia data.

    The data is loaded and parsed from the internet.
    Also see <https://web.stanford.edu/~hastie/CASI_files/DATA/leukemia.html>

    Returns:
        Tuple containing labels and data.
    """
    df = pd.read_csv("https://web.stanford.edu/~hastie/CASI_files/DATA/leukemia_big.csv")
    data = df.T

    # labels
    labels = []
    for label in df.columns:  # pylint:disable=no-member
        if "ALL" in label:
            labels.append(0)
        elif "AML" in label:
            labels.append(1)
        else:
            assert False, "This must not happen!"

    assert len(labels) == 72
    assert data.shape == (72, 7128)

    return pd.Series(labels), data
