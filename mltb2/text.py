# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""Text specific module."""

import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Dict, Final, Iterable, Optional, Pattern, Set, Tuple, Union

from scipy.spatial.distance import cityblock
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


def _normalize_counter_to_defaultdict(counter: Counter, max_dimensions: int) -> defaultdict:
    """Normalize a counter to to ``max_dimensions``.

    The number of dimensions is limited to ``max_dimensions``
    of the most commen characters.
    The counter values are normalized by deviding them by the total count.

    Args:
        counter: The counter to normalize.
        max_dimensions: The maximum number of dimensions to use for the normalization.
    Returns:
        The normalized counter with a maximum of ``max_dimensions`` dimensions.
    """
    total_count = sum(counter.values())
    normalized_counter = defaultdict(float)
    for char, count in counter.most_common(max_dimensions):
        normalized_counter[char] = count / total_count
    return normalized_counter


@dataclass
class TextDistance:
    """Calculate the distance between two texts.

    One text is fitted and then the Manhatten distance to another given text is calculated.

    Args:
        show_progress_bar: Show a progressbar during processing.
        max_dimensions: The maximum number of dimensions to use for the distance calculation.
    """

    show_progress_bar: bool = False
    max_dimensions: int = 100

    # counter for the text we fit
    _char_counter: Optional[Counter] = field(default_factory=Counter, init=False)

    # normalized counter for the text we fit - see _normalize_char_counter
    _normalized_char_counts: Optional[defaultdict] = field(default=None, init=False)

    # set of all counted characters - see _normalize_char_counter
    _counted_char_set: Optional[Set[str]] = field(default=None, init=False)

    def fit(self, text: Union[str, Iterable[str]]) -> None:
        """Fit the text.

        Args:
            text: The text to fit.
        """
        if self._char_counter is None:
            raise ValueError("Fit mut not be called after distance calculation!")

        if isinstance(text, str):
            self._char_counter.update(text)
        else:
            for t in tqdm(text, disable=not self.show_progress_bar):
                self._char_counter.update(t)

    def _normalize_char_counter(self):
        """Normalize the char counter to a defaultdict.

        This supports lazy postprocessing of the char counter.
        """
        if self._char_counter is not None:
            self._normalized_char_counts = _normalize_counter_to_defaultdict(self._char_counter, self.max_dimensions)
            self._char_counter = None
            self._counted_char_set = set(self._normalized_char_counts)

    def distance(self, text) -> float:
        """Calculate the distance between the fitted text and the given text.

        This implementation uses the Manhattan distance and only the
        first ``max_dimensions`` of the most commen characters.

        Args:
            text: The text to calculate the cosine distance to.
        """
        self._normalize_char_counter()
        all_vector = []
        text_vector = []
        text_count = Counter(text)
        text_count_defaultdict = _normalize_counter_to_defaultdict(text_count, self.max_dimensions)
        for c in self._counted_char_set.union(text_count_defaultdict):  # type: ignore
            all_vector.append(
                self._normalized_char_counts[c]  # type: ignore
            )  # if c is not in defaultdict, it will return 0
            text_vector.append(text_count_defaultdict[c])  # if c is not in defaultdict, it will return 0
        return cityblock(all_vector, text_vector)
