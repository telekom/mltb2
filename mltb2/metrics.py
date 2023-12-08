from typing import List, Dict, Tuple
import numpy as np


def get_stability(selected_features_matrix):

    robustness_vector = selected_features_matrix.sum(axis=0)
    print(robustness_vector[robustness_vector.nonzero()])
    subset_vector = selected_features_matrix.sum(axis=1)

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


def test_stability():
    only_ones = np.ones((10, 20))
    stability = get_stability(only_ones)
    assert stability == 1, stability

    perfect_stability = np.concatenate((np.ones((10, 8)), np.zeros((10, 120))), axis=1)
    assert perfect_stability.shape == (10, 128)
    perfect_stability_metric = get_stability(perfect_stability)
    assert perfect_stability_metric == 1, perfect_stability_metric

    perfect_stability2 = np.concatenate((np.ones((10, 1)), np.zeros((10, 120))), axis=1)
    assert perfect_stability2.shape == (10, 121)
    perfect_stability_metric2 = get_stability(perfect_stability2)
    assert perfect_stability_metric2 == 1, perfect_stability_metric2

    # print(get_stability(perfect_stability))
    not_stable = get_stability(np.zeros((10, 20)))
    assert not_stable == 0, not_stable


def _subset_size_stability(subset_vector, number_of_features, k):
    """

    Args:
        subset_vector: Numpy array containing the number of selected features
            per fold. The length of the array equals the number of all folds.
        number_of_features: Number of all features in the input data.

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
