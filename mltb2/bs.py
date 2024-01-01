# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""Beautiful Soup specific tools.

Hint:
    Use pip to install the necessary dependencies for this module:
    ``pip install mltb2[bs]``
"""

import re
from typing import Optional

import mdformat
from markdownify import MarkdownConverter, markdownify


def extract_text(soup, join_str=None) -> str:
    """TODO: add docstring."""
    if join_str is None:
        join_str = " "
    texts = [text for text in soup.stripped_strings]
    result: str = join_str.join(texts)
    return result


def normalize_text(text) -> str:  #
    """TODO: add docstring."""
    text = text.replace("\xa0", " ")
    text = text.replace("\u200b", " ")
    text = re.sub("  +", " ", text)
    text = text.strip()
    return text


def extract_one(soup, name=None, attrs={}, **kwargs):
    """TODO: add docstring."""
    result = soup.find_all(name, attrs, **kwargs)
    assert len(result) == 1, len(result)
    result = result[0]
    return result


def extract_all(soup, name=None, attrs={}, **kwargs):
    """TODO: add docstring."""
    result = soup.find_all(name, attrs, **kwargs)
    return result


def remove_all(soup, name=None, attrs={}, **kwargs) -> None:
    """TODO: add docstring."""
    result = soup.find_all(name, attrs, **kwargs)
    for r in result:
        r.decompose()


def soup_to_md(soup, mdformat_options: Optional[dict] = None) -> str:
    """TODO: add docstring."""
    if mdformat_options is None:
        mdformat_options = {"number": True, "wrap": "no"}
    text = MarkdownConverter().convert_soup(soup)
    text = mdformat.text(text, options=mdformat_options)
    return text


def html_to_md(html, mdformat_options: Optional[dict] = None) -> str:
    """TODO: add docstring."""
    if mdformat_options is None:
        mdformat_options = {"number": True, "wrap": "no"}
    text = markdownify(html)
    text = mdformat.text(text, options=mdformat_options)
    return text
