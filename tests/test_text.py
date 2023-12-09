# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

from mltb2.text import remove_invisible_chars


def test_remove_invisible_chars():
    text = "Hello\u200bWorld\u00ad!"
    result = remove_invisible_chars(text)
    assert result == "HelloWorld!"


def test_remove_invisible_chars_empty():
    text = ""
    result = remove_invisible_chars(text)
    assert result == ""
