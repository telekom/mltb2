# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""Text specific module."""

import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Dict, Final, Iterable, Pattern, Tuple, Union

from scipy.spatial.distance import cosine
from tqdm import tqdm

INVISIBLE_CHARACTERS: Final[Tuple[str, ...]] = (
    "\u200b",  # Zero Width Space (ZWSP) https://www.compart.com/en/unicode/U+200b
    "\u00ad",  # Soft Hyphen (SHY) https://www.compart.com/en/unicode/U+00ad
    # TODO: what about:
    # https://www.compart.com/en/unicode/U+2028
    # https://www.compart.com/en/unicode/U+2029
)

INVISIBLE_CHARACTERS_TRANS: Final[Dict[int, None]] = str.maketrans({char: None for char in INVISIBLE_CHARACTERS})

SPECIAL_WHITESPACES: Final[Tuple[str, ...]] = (
    # unicode block "General Punctuation": https://www.compart.com/en/unicode/block/U+2000
    "\u2000",  # En Quad
    "\u2001",  # Em Quad
    "\u2002",  # En Space
    "\u2003",  # Em Space
    "\u2004",  # Three-Per-Em Space
    "\u2005",  # Four-Per-Em Space
    "\u2006",  # Six-Per-Em Space
    "\u2007",  # Figure Space https://www.compart.com/en/unicode/U+2007
    "\u2008",  # Punctuation Space
    "\u2009",  # Thin Space https://www.compart.com/en/unicode/U+2009
    "\u200a",  # Hair Space https://www.compart.com/en/unicode/U+200A
    "\u202f",  # Narrow No-Break Space (NNBSP) https://www.compart.com/en/unicode/U+202f
    # other unicode blocks
    "\u00a0",  # No-Break Space (NBSP) https://www.compart.com/en/unicode/U+00a0
)

SPECIAL_WHITESPACES_TRANS: Final[Dict[int, str]] = str.maketrans({char: " " for char in SPECIAL_WHITESPACES})

INVISIBLE_CHARACTERS_AND_SPECIAL_WHITESPACES_TRANS = {**SPECIAL_WHITESPACES_TRANS, **INVISIBLE_CHARACTERS_TRANS}

MULTI_SPACE_PATTERN: Pattern = re.compile(r" {2,}")


def remove_invisible_characters(text: str) -> str:
    """Remove invisible characters from text.

    The invisible characters are defined in the constant ``INVISIBLE_CHARACTERS``.

    Args:
        text: The text from which the invisible characters are to be removed.

    Returns:
        The cleaned text.
    """
    return text.translate(INVISIBLE_CHARACTERS_TRANS)


def has_invisible_characters(text: str) -> bool:
    """Check if text contains invisible characters.

    The invisible characters are defined in the constant ``INVISIBLE_CHARACTERS``.

    Args:
        text: The text to check.

    Returns:
        ``True`` if the text contains invisible characters, ``False`` otherwise.
    """
    return any(char in text for char in INVISIBLE_CHARACTERS)


def replace_special_whitespaces(text: str) -> str:
    """Replace special whitespaces with normal whitespaces.

    The special whitespaces are defined in the constant ``SPECIAL_WHITESPACES``.

    Args:
        text: The text from which the special whitespaces are to be replaced.

    Returns:
        The cleaned text.
    """
    return text.translate(SPECIAL_WHITESPACES_TRANS)


def has_special_whitespaces(text: str) -> bool:
    """Check if text contains special whitespaces.

    The special whitespaces are defined in the constant ``SPECIAL_WHITESPACES``.

    Args:
        text: The text to check.

    Returns:
        ``True`` if the text contains special whitespaces, ``False`` otherwise.
    """
    return any(char in text for char in SPECIAL_WHITESPACES)


def replace_multiple_whitespaces(text: str) -> str:
    """Replace multiple whitespaces with single whitespace.

    Args:
        text: The text from which the multiple whitespaces are to be replaced.

    Returns:
        The cleaned text.
    """
    return MULTI_SPACE_PATTERN.sub(" ", text)


def clean_all_invisible_chars_and_whitespaces(text: str) -> str:
    """Clean text form invisible characters and whitespaces.

    - Remove invisible characters from text.
    - Replace special whitespaces with normal whitespaces.
    - Replace multiple whitespaces with single whitespace.
    - Remove leading and trailing whitespaces.

    The invisible characters are defined in the constant ``INVISIBLE_CHARACTERS``.
    The special whitespaces are defined in the constant ``SPECIAL_WHITESPACES``.

    Args:
        text: The text to clean.

    Rteturns:
        The cleaned text.
    """
    text = text.translate(INVISIBLE_CHARACTERS_AND_SPECIAL_WHITESPACES_TRANS)
    text = replace_multiple_whitespaces(text)
    text = text.strip()
    return text


@dataclass
class TextDistance:
    """Calculate the cosine distance between two texts.

    One text is fitted and then the cosine distance to another given text is calculated.

    Args:
        show_progress_bar: Show a progressbar during processing.
    """

    char_counter: Counter = field(init=False)
    show_progress_bar: bool = False

    def __post_init__(self):
        """Do post init."""
        self.char_counter = Counter()

    def fit(self, text: Union[str, Iterable[str]]) -> None:
        """Fit the text.

        Args:
            text: The text to fit.
        """
        if isinstance(text, str):
            self.char_counter.update(text)
        else:
            for t in tqdm(text, disable=not self.show_progress_bar):
                self.char_counter.update(t)

    def cosine_distance(self, text) -> float:
        """Calculate the cosine distance between the fitted text and the given text.

        Args:
            text: The text to calculate the cosine distance to.
        """
        all_vector = []
        text_vector = []
        text_count = Counter(text)
        for c in set(self.char_counter).union(text_count):
            all_vector.append(self.char_counter[c])  # if c is not in Counter, it will return 0
            text_vector.append(text_count[c])  # if c is not in Counter, it will return 0
        return cosine(all_vector, text_vector)
