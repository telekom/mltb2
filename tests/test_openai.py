# Copyright (c) 2023-2024 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

from typing import List

import pytest
from hypothesis import given, settings
from hypothesis.strategies import lists, text

from mltb2.openai import OpenAiTokenCounter


@pytest.fixture(scope="module")
def gpt_4_open_ai_token_counter() -> OpenAiTokenCounter:
    return OpenAiTokenCounter("gpt-4")


@settings(max_examples=1000)
@given(text=text())
def test_OpenAiTokenCounter_str_hypothesis(text: str, gpt_4_open_ai_token_counter: OpenAiTokenCounter):  # noqa: N802
    token_count = gpt_4_open_ai_token_counter(text)
    assert token_count >= 0  # type: ignore[operator]


def test_OpenAiTokenCounter_call_string():  # noqa: N802
    token_counter = OpenAiTokenCounter("gpt-4")
    token_count = token_counter("Das ist ein Text.")

    assert token_count == 5


@settings(max_examples=1000)
@given(texts=lists(text()))
def test_OpenAiTokenCounter_list_hypothesis(  # noqa: N802
    texts: List[str], gpt_4_open_ai_token_counter: OpenAiTokenCounter
):
    token_count = gpt_4_open_ai_token_counter(texts)
    assert len(token_count) == len(texts)  # type: ignore[arg-type]
    assert all(count >= 0 for count in token_count)  # type: ignore[union-attr]


def test_OpenAiTokenCounter_call_list():  # noqa: N802
    token_counter = OpenAiTokenCounter("gpt-4")
    token_count = token_counter(["Das ist ein Text.", "Das ist ein anderer Text."])

    assert isinstance(token_count, list)
    assert len(token_count) == 2
    assert token_count[0] == 5
    assert token_count[1] == 7
