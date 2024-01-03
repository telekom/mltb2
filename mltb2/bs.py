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
    """Extract the text from a BeautifulSoup object.

    Warning:
        This implementation has known issues with whitespace handling.

    Args:
        soup: The BeautifulSoup object to extract the text from.
        join_str: String to join the text parts with. Per default a space is used.
    Returns:
        Text from the BeautifulSoup object.
    """
    if join_str is None:
        join_str = " "
    texts = list(soup.stripped_strings)
    result: str = join_str.join(texts)
    return result


def extract_one(soup: BeautifulSoup, name=None, attrs: Optional[dict] = None, **kwargs: Dict[str, Any]) -> Any:
    """Extract exactly one specified element from a BeautifulSoup object.

    This function expacts that exactly only one result is found.
    Otherwise a RuntimeError is raised.

    Args:
        soup: The BeautifulSoup object to extract the element from.
        name: Name of the tag to extract.
        attrs: Attributes of the tag to extract.
        kwargs: Additional keyword arguments.
    Returns:
        The extracted BeautifulSoup element.
    Raises:
        RuntimeError: If not exactly one result is found.
    """
    if attrs is None:
        attrs = {}
    result = soup.find_all(name, attrs, **kwargs)
    if len(result) != 1:
        raise RuntimeError(f"Expected exactly one result, but got {len(result)}!")
    result = result[0]
    return result


def extract_all(soup: BeautifulSoup, name=None, attrs: Optional[dict] = None, **kwargs: Dict[str, Any]) -> Any:
    """Extract all specified elements from a BeautifulSoup object.

    Args:
        soup: The BeautifulSoup object to extract the elements from.
        name: Name of the tag to extract.
        attrs: Attributes of the tag to extract.
        kwargs: Additional keyword arguments.
    Returns:
        The extracted BeautifulSoup elements.
    """
    if attrs is None:
        attrs = {}
    result = soup.find_all(name, attrs, **kwargs)
    return result


def remove_all(soup: BeautifulSoup, name=None, attrs: Optional[dict] = None, **kwargs: Dict[str, Any]) -> None:
    """Remove all specified elements from a BeautifulSoup object.

    The removal is done in place. Nothing is returned.

    Args:
        soup: The BeautifulSoup object to remove the elements from.
        name: Name of the tag(-s) to remove.
        attrs: Attributes of the tag(-s) to remove.
        kwargs: Additional keyword arguments.
    """
    if attrs is None:
        attrs = {}
    result = soup.find_all(name, attrs, **kwargs)
    for r in result:
        r.decompose()


def soup_to_md(soup: BeautifulSoup, mdformat_options: Optional[dict] = None) -> str:
    """Convert a BeautifulSoup object to Markdown.

    The default mdformat options are:

    - ``number=True``: apply consecutive numbering to ordered lists
    - ``wrap="no"``: paragraph word wrap mode
    - ``end-of-line="lf"``: use LF as line ending

    See Also:
        The `mdformat Options
        <https://mdformat.readthedocs.io/en/stable/users/installation_and_usage.html#options>`_.
    Args:
        soup: BeautifulSoup object.
        mdformat_options: Options for mdformat.
    Returns:
        The Markdown text.
    """
    if mdformat_options is None:
        mdformat_options = {"number": True, "wrap": "no"}
    text = MarkdownConverter().convert_soup(soup)
    text = mdformat.text(text, options=mdformat_options)
    return text


def html_to_md(html: str, mdformat_options: Optional[dict] = None) -> str:
    """Convert HTML to Markdown.

    The default mdformat options are:

    - ``number=True``: apply consecutive numbering to ordered lists
    - ``wrap="no"``: paragraph word wrap mode
    - ``end-of-line="lf"``: use LF as line ending

    See Also:
        The `mdformat Options
        <https://mdformat.readthedocs.io/en/stable/users/installation_and_usage.html#options>`_.
    Args:
        html: HTML text.
        mdformat_options: Options for mdformat.
    Returns:
        The Markdown text.
    """
    if mdformat_options is None:
        mdformat_options = {"number": True, "wrap": "no"}
    text = markdownify(html)
    text = mdformat.text(text, options=mdformat_options)
    return text
