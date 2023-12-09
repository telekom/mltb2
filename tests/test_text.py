# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

import pytest

from mltb2.text import (
    INVISIBLE_CHARACTERS,
    SPECIAL_WHITESPACES,
    has_invisible_characters,
    has_special_whitespaces,
    remove_invisible_characters,
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
