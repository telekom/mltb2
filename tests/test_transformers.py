# Copyright (c) 2023-2024 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT


import pytest
from hypothesis import given, settings
from hypothesis.strategies import text

from mltb2.transformers import TransformersTokenCounter


@pytest.fixture(scope="module")
def deepset_gbert_base_token_counter() -> TransformersTokenCounter:
    return TransformersTokenCounter("deepset/gbert-base")


@settings(max_examples=1000, deadline=None)
@given(text=text())
def test_TransformersTokenCounter_hypothesis(  # noqa: N802
    text: str, deepset_gbert_base_token_counter: TransformersTokenCounter
):
    token_count = deepset_gbert_base_token_counter(text)

    assert isinstance(token_count, int)
    assert token_count >= 0


def test_TransformersTokenCounter_call_string():  # noqa: N802
    transformers_token_counter = TransformersTokenCounter("deepset/gbert-base")
    token_count = transformers_token_counter("Das ist ein Text.")

    assert token_count == 5


def test_TransformersTokenCounter_call_list():  # noqa: N802
    transformers_token_counter = TransformersTokenCounter("deepset/gbert-base")
    token_count = transformers_token_counter(["Das ist ein Text.", "Das ist ein anderer Text."])

    assert isinstance(token_count, list)
    assert len(token_count) == 2
    assert token_count[0] == 5
    assert token_count[1] == 6
