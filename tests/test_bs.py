# Copyright (c) 2024 Philip May
# Copyright (c) 2004-2023 Leonard Richardson
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

import pytest
from bs4 import BeautifulSoup

from mltb2.bs import extract_all, extract_one, extract_text, html_to_md, remove_all, soup_to_md

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

<p class="story">...</p>"""


@pytest.fixture
def my_soup() -> BeautifulSoup:
    soup = BeautifulSoup(html_doc, features="html.parser")
    return soup


@pytest.mark.xfail(reason="see https://github.com/telekom/mltb2/issues/127")
def test_extract_text(my_soup: BeautifulSoup):
    result = extract_text(my_soup)
    assert (
        result == "The Dormouse's story The Dormouse's story Once upon a time there were three little sisters; "
        "and their names were Elsie, Lacie and Tillie; and they lived at the bottom of a well. ..."
    )


def test_extract_one__happy_case(my_soup: BeautifulSoup):
    result = extract_one(my_soup, name="head")
    assert result is not None
    assert result.name == "head"
    assert result.text == "The Dormouse's story"


def test_extract_one__multiple_results(my_soup: BeautifulSoup):
    with pytest.raises(RuntimeError):
        _ = extract_one(my_soup, name="a")


def test_extract_all__happy_case(my_soup: BeautifulSoup):
    result = extract_all(my_soup, name="a")
    assert result is not None
    assert len(result) == 3
    assert result[0].name == "a"
    assert result[0].text == "Elsie"


def test_remove_all(my_soup: BeautifulSoup):
    remove_all(my_soup, name="a")
    result = extract_all(my_soup, name="a")
    assert result is not None
    assert len(result) == 0


def test_soup_to_md(my_soup: BeautifulSoup):
    result = soup_to_md(my_soup)
    assert result is not None
    assert (
        result == "The Dormouse's story **The Dormouse's story**\n\n"
        "Once upon a time there were three little sisters; "
        "and their names were [Elsie](http://example.com/elsie), "
        "[Lacie](http://example.com/lacie) and [Tillie](http://example.com/tillie); "
        "and they lived at the bottom of a well.\n\n...\n"
    )


def test_html_to_md():
    result = html_to_md(html_doc)
    assert result is not None
    assert (
        result == "The Dormouse's story **The Dormouse's story**\n\n"
        "Once upon a time there were three little sisters; "
        "and their names were [Elsie](http://example.com/elsie), "
        "[Lacie](http://example.com/lacie) and [Tillie](http://example.com/tillie); "
        "and they lived at the bottom of a well.\n\n...\n"
    )
