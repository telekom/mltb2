# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""Beautiful Soup and HTML specific tools.

Hint:
    Use pip to install the necessary dependencies for this module:
    ``pip install mltb2[bs]``
"""

from typing import Any, Dict, Optional

import mdformat
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter, markdownify


def extract_text(soup: BeautifulSoup, join_str: Optional[str] = None) -> str:
    """TODO: add docstring."""
    if join_str is None:
        join_str = " "
    texts = list(soup.stripped_strings)
    result: str = join_str.join(texts)
    return result


# TODO: add return type
def extract_one(soup: BeautifulSoup, name=None, attrs: Optional[dict] = None, **kwargs: Dict[str, Any]):
    """TODO: add docstring."""
    if attrs is None:
        attrs = {}
    result = soup.find_all(name, attrs, **kwargs)
    if len(result) != 1:
        raise RuntimeError(f"Expected exactly one result, but got {len(result)}!")
    result = result[0]
    return result


# TODO: add return type
def extract_all(soup: BeautifulSoup, name=None, attrs: Optional[dict] = None, **kwargs: Dict[str, Any]):
    """TODO: add docstring."""
    if attrs is None:
        attrs = {}
    result = soup.find_all(name, attrs, **kwargs)
    return result


def remove_all(soup: BeautifulSoup, name=None, attrs: Optional[dict] = None, **kwargs: Dict[str, Any]) -> None:
    """TODO: add docstring."""
    if attrs is None:
        attrs = {}
    result = soup.find_all(name, attrs, **kwargs)
    for r in result:
        r.decompose()


def soup_to_md(soup: BeautifulSoup, mdformat_options: Optional[dict] = None) -> str:
    """TODO: add docstring."""
    if mdformat_options is None:
        mdformat_options = {"number": True, "wrap": "no"}
    text = MarkdownConverter().convert_soup(soup)
    text = mdformat.text(text, options=mdformat_options)
    return text


def html_to_md(html: str, mdformat_options: Optional[dict] = None) -> str:
    """TODO: add docstring."""
    if mdformat_options is None:
        mdformat_options = {"number": True, "wrap": "no"}
    text = markdownify(html)
    text = mdformat.text(text, options=mdformat_options)
    return text
