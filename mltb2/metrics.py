# Copyright (c) 2022 Sigrun May, Ostfalia Hochschule für angewandte Wissenschaften
# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""TODO: add docstring."""

import math

import numpy as np


def high_dim_feature_selection_stability_score(selected_features_binary_matrix: np.ndarray):
    """TODO: add docstring.

    See Also:
        - `https://github.com/Wahid-dr/gStab-Package/blob/main/ICTAPP-23-44-FinalVersion.pdf`_
    """
    if selected_features_binary_matrix.ndim != 2:
        raise ValueError("'selected_features_matrix' must be a two-dimensional array!")

    if not np.all((selected_features_binary_matrix == 0) | (selected_features_binary_matrix == 1)):
        raise ValueError("Input matrix is not binary")

    robustness_vector = selected_features_binary_matrix.sum(axis=0)
    subset_vector = selected_features_binary_matrix.sum(axis=1)

    number_of_features = len(robustness_vector)
    number_of_folds = len(subset_vector)

    stability = 0.0
    count_k = 0
    for k in range(1, number_of_folds + 1):
        count_k += 1

        # empirical density of the robustness_vector
        # number of features which were selected k-times
        robustness_density = list(robustness_vector).count(k)
        subset_size_stability = _subset_size_stability(subset_vector, number_of_features, k)

        assert subset_vector[k - 1] != 0
        assert subset_vector[k - 1] != 0.0
        assert not math.isnan(subset_vector[k - 1])

        stability += (k**2 * robustness_density * subset_size_stability) / subset_vector[k - 1]
        if np.isnan(stability):
            print("stability is nan")
            return 0

    if stability > number_of_folds**2:
        print(stability)
    stability = stability / (number_of_folds**2)

    assert count_k == number_of_folds
    if stability > 1:
        print(stability, " stability greater than 1")
    # assert stability <= 1.1, stability
    return stability


def _subset_size_stability(subset_vector, number_of_features, k):
    """TODO: add docstring.

    Args:
        subset_vector: Numpy array containing the number of selected features
            per fold. The length of the array equals the number of all folds.
        number_of_features: Number of all features in the input data.
        k: TODO: add docstring.

    Returns:
        Subset-size stability
    """
    k = k - 1  # Shift from one-based k to zero-based for correct indexing
    assert k >= 0
    if k == 0:
        subset_size_stability = subset_vector[k] / number_of_features

    elif subset_vector[k] > subset_vector[k - 1]:
        subset_size_stability = subset_vector[k - 1] / subset_vector[k]

    elif subset_vector[k] < subset_vector[k - 1]:
        subset_size_stability = subset_vector[k] / subset_vector[k - 1]

    elif subset_vector[k] == subset_vector[k - 1]:
        subset_size_stability = 1

    else:
        raise ValueError("Incorrect subset vector")

    return subset_size_stability
