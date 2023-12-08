# Copyright (c) 2022 Sigrun May, Ostfalia Hochschule für angewandte Wissenschaften
# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

import numpy as np

from mltb2.metrics import get_stability


def test_stability():
    """TODO: add docstring."""
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
