# Copyright (c) 2023 Philip May, Deutsche Telekom AG
# Copyright (c) 2023-2024 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""Markdown specific module.

Hint:
    Use pip to install the necessary dependencies for this module:
    ``pip install mltb2[md]``
"""

import re
from dataclasses import dataclass
from typing import Final, List

from tqdm import tqdm

from mltb2.transformers import TransformersTokenCounter

_HEADLINE_REGEX: Final = re.compile(r"^#+ .*", flags=re.MULTILINE)


def _chunk_md_by_headline(md_text: str) -> List[str]:
    """Chunk Markdown by headlines.

    Args:
        md_text: The Markdown text to be chunked.

    Returns:
        The list of Markdown chunks.
    """
    positions: List[int] = [m.start() for m in re.finditer(_HEADLINE_REGEX, md_text)]

    # extend positions
    if 0 not in positions:
        positions = [0] + positions  # noqa: RUF005
    positions.append(len(md_text))

    result = [md_text[x:y].strip() for x, y in zip(positions, positions[1:])]
    return result


def chunk_md(md_text: str) -> List[str]:
    """Chunk Markdown by headlines and merge isolated headlines.

    Merges isolated headlines with their corresponding subsequent paragraphs.
    Headings isolated at the end of ``md_text`` (headings without content) are removed in this process.

    Args:
        md_text: The Markdown text to be chunked.

    Returns:
        The list of Markdown chunks.
    """
    md_chunks = _chunk_md_by_headline(md_text)

    merged_chunks = []
    temp_merged_chunk = []
    for chunk in md_chunks:
        temp_merged_chunk.append(chunk)
        if "\n" in chunk:  # content chunk found
            joined_content = "\n\n".join(temp_merged_chunk)
            merged_chunks.append(joined_content)
            temp_merged_chunk = []

    # if len(temp_content) > 0 this is only headlines and we skip them
    return merged_chunks


@dataclass
class MdTextSplitter:
    """Split Markdown text into sections with a specified maximum token number.

    Does not divide headings with their corresponding paragraphs.

    Args:
        max_token: Maximum number of tokens per text section.
            Can only be exceeded if a single Markdown chunk is already larger.
        transformers_token_counter: The token counter to be used.
        show_progress_bar: Show a progressbar during processing.
    """

    max_token: int
    transformers_token_counter: TransformersTokenCounter
    show_progress_bar: bool = False

    def __call__(self, md_text: str) -> List[str]:
        """Split the Markdown text into sections.

        Args:
            md_text: The Markdown text to be split.
        Returns:
            The list of Markdown section splits.
        """
        md_chunks = chunk_md(md_text)
        counts = self.transformers_token_counter(md_chunks)

        assert len(md_chunks) == len(counts)  # type: ignore[arg-type]

        result_merges: List[str] = []
        temp_merges: List[str] = []
        current_count: int = 0

        for md_chunk, count in zip(
            tqdm(md_chunks, disable=not self.show_progress_bar), counts  # type: ignore[arg-type]
        ):
            if current_count + count > self.max_token and len(temp_merges) > 0:
                joined_content = "\n\n".join(temp_merges)
                result_merges.append(joined_content)
                temp_merges = []
                current_count = 0

            current_count += count
            temp_merges.append(md_chunk)

        # add the rest
        if len(temp_merges) > 0:
            joined_content = "\n\n".join(temp_merges)
            result_merges.append(joined_content)

        return result_merges
