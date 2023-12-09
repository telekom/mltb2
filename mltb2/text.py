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


def remove_invisible_chars(text: str) -> str:
    """Remove invisible characters from text.

    The invisible characters are defined in the constant `INVISIBLE_CHARACTERS`.

    Args:
        text: The text from which the invisible characters are to be removed.

    Returns:
        The cleaned text.
    """
    return text.translate(INVISIBLE_CHARACTERS_TRANS)
