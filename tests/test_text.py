# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

from collections import Counter, defaultdict
from math import isclose

import pytest

from mltb2.text import (
    INVISIBLE_CHARACTERS,
    SPECIAL_WHITESPACES,
    TextDistance,
    _normalize_counter_to_defaultdict,
    clean_all_invisible_chars_and_whitespaces,
    has_invisible_characters,
    has_special_whitespaces,
    remove_invisible_characters,
    replace_multiple_whitespaces,
    replace_special_whitespaces,
)


def test_remove_invisible_characters():
    text = "Hello\u200bWorld\u00ad!"
    result = remove_invisible_characters(text)
    assert result == "HelloWorld!"


def test_remove_invisible_characters_empty():
    text = ""
    result = remove_invisible_characters(text)
    assert result == ""


@pytest.mark.parametrize("char", INVISIBLE_CHARACTERS)
def test_remove_invisible_characters_single_char(char: str):
    text = f">{char}<"
    result = remove_invisible_characters(text)
    assert result == "><"


def test_replace_special_whitespaces():
    text = "a\u00a0b\u2009c\u202fd\u2007e\u200af"
    result = replace_special_whitespaces(text)
    assert result == "a b c d e f"


def test_replace_special_whitespaces_empty():
    text = ""
    result = replace_special_whitespaces(text)
    assert result == ""


@pytest.mark.parametrize("char", SPECIAL_WHITESPACES)
def test_replace_special_whitespaces_single_char(char: str):
    text = f">{char}<"
    result = replace_special_whitespaces(text)
    assert result == "> <"


def test_has_invisible_characters_true():
    text = "Hello\u200bWorld\u00ad!"
    result = has_invisible_characters(text)
    assert result


def test_has_invisible_characters_false():
    text = "Hello!"
    result = has_invisible_characters(text)
    assert not result


def test_has_special_whitespaces_true():
    text = "a\u00a0b\u2009c\u202fd\u2007e\u200af"
    result = has_special_whitespaces(text)
    assert result


def test_has_special_whitespaces_false():
    text = "Hello you!"
    result = has_special_whitespaces(text)
    assert not result


def test_replace_multiple_whitespaces():
    text = "Hello  World  !"
    result = replace_multiple_whitespaces(text)
    assert result == "Hello World !"


def test_replace_multiple_whitespaces_empty():
    text = ""
    result = replace_multiple_whitespaces(text)
    assert result == ""


def test_replace_multiple_whitespaces_empty_result():
    text = "  "
    result = replace_multiple_whitespaces(text)
    assert result == " "


def test_replace_multiple_whitespaces_one_space():
    text = " "
    result = replace_multiple_whitespaces(text)
    assert result == " "


def test_clean_all_invisible_chars_and_whitespaces():
    text = " Hello\u200bWorld\u00ad! How\u2007  are you? "
    result = clean_all_invisible_chars_and_whitespaces(text)
    assert result == "HelloWorld! How are you?"


def test_clean_all_invisible_chars_and_whitespaces_empty_result():
    text = " \u200b\u00ad\u2007   "
    result = clean_all_invisible_chars_and_whitespaces(text)
    assert result == ""


def test_text_distance_distance_same():
    text = "Hello World!"
    td = TextDistance()
    td.fit(text)
    assert len(td._char_counter) == 9
    assert td._normalized_char_counts is None
    assert td._counted_char_set is None
    distance = td.distance(text)
    assert td._char_counter is None  # none after fit
    assert td._normalized_char_counts is not None
    assert td._counted_char_set is not None

    assert isclose(distance, 0.0), distance


def test_text_distance_orthogonal():
    text = "ab"
    td = TextDistance()
    td.fit(text)
    distance = td.distance("xy")
    assert distance > 0.0, distance
    assert isclose(distance, 2.0), distance


def test_text_distance_extended():
    text = "aabbbb"  # a:1/3, b:2/3
    td = TextDistance()
    td.fit(text)
    distance = td.distance("bbcccc")  # b:1/3, c:2/3
    assert distance > 0.0, distance
    assert isclose(distance, 1 / 3 + 1 / 3 + 2 / 3), distance


def test_text_distance_fit_not_allowed_after_distance():
    text = "Hello World!"
    td = TextDistance()
    td.fit(text)
    _ = td.distance(text)
    with pytest.raises(ValueError):
        td.fit("Hello World")


def test_text_distance_max_dimensions_must_be_greater_zero():
    with pytest.raises(ValueError):
        _ = TextDistance(max_dimensions=0)


def test_normalize_counter_to_defaultdict():
    counter = Counter("aaaabbbcc")
    max_dimensions = 2
    normalized_counter = _normalize_counter_to_defaultdict(counter, max_dimensions)

    assert isinstance(normalized_counter, defaultdict)
    assert len(normalized_counter) == max_dimensions
    assert isclose(normalized_counter["a"], 4 / 9)
    assert isclose(normalized_counter["b"], 3 / 9)
    assert "c" not in normalized_counter
    assert len(normalized_counter) == max_dimensions


def test_normalize_counter_to_defaultdict_empty_counter():
    counter = Counter()
    max_dimensions = 2
    normalized_counter = _normalize_counter_to_defaultdict(counter, max_dimensions)

    assert isinstance(normalized_counter, defaultdict)
    assert len(normalized_counter) == 0
