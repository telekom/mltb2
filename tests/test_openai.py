# Copyright (c) 2023-2024 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

from typing import List

from hypothesis import given, settings
from hypothesis.strategies import lists, text

from mltb2.openai import OpenAiTokenCounter


@settings(max_examples=1000)
@given(text())
def test_OpenAiTokenCounter_str_hypothesis(text: str):  # noqa: N802
    token_counter = OpenAiTokenCounter("gpt-4")
    token_count = token_counter(text)

    assert token_count >= 0  # type: ignore[operator]


def test_OpenAiTokenCounter_call_string():  # noqa: N802
    token_counter = OpenAiTokenCounter("gpt-4")
    token_count = token_counter("Das ist ein Text.")

    assert token_count == 5


@settings(max_examples=1000, deadline=None)
@given(lists(text()))
def test_OpenAiTokenCounter_list_hypothesis(texts: List[str]):  # noqa: N802
    token_counter = OpenAiTokenCounter("gpt-4")
    token_count = token_counter(texts)

    assert len(token_count) == len(texts)  # type: ignore[arg-type]
    assert all(count >= 0 for count in token_count)  # type: ignore[union-attr]


def test_OpenAiTokenCounter_call_list():  # noqa: N802
    token_counter = OpenAiTokenCounter("gpt-4")
    token_count = token_counter(["Das ist ein Text.", "Das ist ein anderer Text."])

    assert isinstance(token_count, list)
    assert len(token_count) == 2
    assert token_count[0] == 5
    assert token_count[1] == 7
