# Copyright (c) 2022 Sigrun May, Ostfalia Hochschule für angewandte Wissenschaften
# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

import numpy as np
import pytest

from mltb2.metrics import high_dim_feature_selection_stability_score


def test_high_dim_feature_selection_stability_score():
    """TODO: add docstring."""
    only_ones = np.ones((10, 20))
    stability = high_dim_feature_selection_stability_score(only_ones)
    assert stability == 1, stability

    perfect_stability = np.concatenate((np.ones((10, 8)), np.zeros((10, 120))), axis=1)
    assert perfect_stability.shape == (10, 128)
    perfect_stability_metric = high_dim_feature_selection_stability_score(perfect_stability)
    assert perfect_stability_metric == 1, perfect_stability_metric

    perfect_stability2 = np.concatenate((np.ones((10, 1)), np.zeros((10, 120))), axis=1)
    assert perfect_stability2.shape == (10, 121)
    perfect_stability_metric2 = high_dim_feature_selection_stability_score(perfect_stability2)
    assert perfect_stability_metric2 == 1, perfect_stability_metric2


def test_high_dim_feature_selection_stability_score__wrong_input_dimensions():
    selected_features_matrix = np.ones((5, 5, 5))
    with pytest.raises(ValueError):
        high_dim_feature_selection_stability_score(selected_features_matrix)


def test_high_dim_feature_selection_stability_score__wrong_input_dimensions():
    selected_features_matrix = np.concatenate((np.ones((10, 1)), np.zeros((10, 120))), axis=1)
    selected_features_matrix[3, 6] = 0.5

    with pytest.raises(ValueError):
        high_dim_feature_selection_stability_score(selected_features_matrix)
