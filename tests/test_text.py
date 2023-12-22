# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

from math import isclose

import pytest

from mltb2.text import (
    INVISIBLE_CHARACTERS,
    SPECIAL_WHITESPACES,
    TextDistance,
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
    distance = td.distance(text)
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


def test_text_distance_exception():
    text = "Hello World!"
    td = TextDistance()
    td.fit(text)
    _ = td.distance(text)
    with pytest.raises(ValueError):
        td.fit("Hello World")
