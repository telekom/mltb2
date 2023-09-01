# Copyright (c) 2023 Philip May, Deutsche Telekom AG
# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""Markdown specific functionality."""

import re
from typing import Final, List

_HEADLINE_REGEX: Final = re.compile(r"^#+ .*", flags=re.MULTILINE)


def _chunk_md_by_headline(md_text: str) -> List[str]:
    """Chunk Markdown by headlines."""
    positions: List[int] = [m.start() for m in re.finditer(_HEADLINE_REGEX, md_text)]

    # extend positions
    if 0 not in positions:
        positions = [0] + positions
    positions.append(len(md_text))

    result = [md_text[x:y].strip() for x, y in zip(positions, positions[1:])]
    return result


def chunk_md(md_text: str) -> List[str]:
    """Chunk Markdown by headlines without isolated headlines."""
    md_chunks = _chunk_md_by_headline(md_text)

    merged_chunks = []
    temp_merged_chunk = []
    for chunk in md_chunks:
        temp_merged_chunk.append(chunk)
        if "\n" in chunk:  # content found
            new_content = "\n\n".join(temp_merged_chunk)
            merged_chunks.append(new_content)
            temp_merged_chunk = []

    # if len(temp_content) > 0 this is only headlines and we skip them
    return merged_chunks
