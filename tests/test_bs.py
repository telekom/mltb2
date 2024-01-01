# Copyright (c) 2024 Philip May
# Copyright (c) 2004-2023 Leonard Richardson
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

import pytest
from bs4 import BeautifulSoup

from mltb2.bs import extract_text

# this code snippet is from the BeautifulSoup documentation
# MIT License
# Copyright (c) 2004-2023 Leonard Richardson
html_doc = """
<html><head><title>The Dormouse's story</title></head>

<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""


@pytest.fixture
def my_soup() -> BeautifulSoup:
    soup = BeautifulSoup(html_doc)
    return soup


@pytest.mark.xfail(reason="see https://github.com/telekom/mltb2/issues/127")
def test_extract_text(my_soup: BeautifulSoup):
    result = extract_text(my_soup)
    assert (
        result == "The Dormouse's story The Dormouse's story Once upon a time there were three little sisters; "
        "and their names were Elsie, Lacie and Tillie; and they lived at the bottom of a well. ..."
    )
