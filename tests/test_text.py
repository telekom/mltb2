# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

from mltb2.text import remove_invisible_characters, replace_special_whitespaces


def test_remove_invisible_characters():
    text = "Hello\u200bWorld\u00ad!"
    result = remove_invisible_characters(text)
    assert result == "HelloWorld!"


def test_remove_invisible_characters_empty():
    text = ""
    result = remove_invisible_characters(text)
    assert result == ""


def test_replace_special_whitespaces():
    text = "a\u00a0b\u2009c\u202fd\u2007e"
    result = replace_special_whitespaces(text)
    assert result == "a b c d e"

def test_replace_special_whitespaces_empty():
    text = ""
    result = replace_special_whitespaces(text)
    assert result == ""
