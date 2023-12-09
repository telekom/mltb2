# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""Text specific functionality."""

from typing import Dict, Final, Tuple

INVISIBLE_CHARACTERS: Final[Tuple[str, ...]] = (
    "\u200b",  # Zero Width Space (ZWSP) https://www.compart.com/en/unicode/U+200b
    "\u00ad",  # Soft Hyphen (SHY) https://www.compart.com/en/unicode/U+00ad
)

INVISIBLE_CHARACTERS_TRANS: Final[Dict[int, None]] = str.maketrans({char: None for char in INVISIBLE_CHARACTERS})

SPECIAL_WHITESPACES: Final[Tuple[str, ...]] = (
    "\u00a0",  # No-Break Space (NBSP) https://www.compart.com/en/unicode/U+00a0
    "\u2009",  # Thin Space https://www.compart.com/en/unicode/U+2009
    "\u202f",  # Narrow No-Break Space (NNBSP) https://www.compart.com/en/unicode/U+202f
    "\u2007",  # Figure Space https://www.compart.com/en/unicode/U+2007
)

SPECIAL_WHITESPACES_TRANS: Final[Dict[int, None]] = str.maketrans({char: " " for char in SPECIAL_WHITESPACES})


def remove_invisible_characters(text: str) -> str:
    """Remove invisible characters from text.

    The invisible characters are defined in the constant `INVISIBLE_CHARACTERS`.

    Args:
        text: The text from which the invisible characters are to be removed.

    Returns:
        The cleaned text.
    """
    return text.translate(INVISIBLE_CHARACTERS_TRANS)

def replace_special_whitespaces(text: str) -> str:
    """Replace special whitespaces with normal whitespaces.

    The special whitespaces are defined in the constant `SPECIAL_WHITESPACES`.

    Args:
        text: The text from which the special whitespaces are to be replaced.

    Returns:
        The cleaned text.
    """
    return text.translate(SPECIAL_WHITESPACES_TRANS)
