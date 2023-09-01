# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

from typing import Final

from mltb2.md import _chunk_md_by_headline, chunk_md

MD: Final[
    str
] = """\
# Headline 1

Content.

## Headline 2 / 1

Content.


### Headline 3 / 1


#### Headline 4 / 1

Content.

#### Headline 4 / 2"""


def test_chunk_md_by_headline():
    result = _chunk_md_by_headline(MD)
    assert isinstance(result, list)
    assert len(result) == 5
    assert result[0] == "# Headline 1\n\nContent."
    assert result[1] == "## Headline 2 / 1\n\nContent."
    assert result[2] == "### Headline 3 / 1"
    assert result[3] == "#### Headline 4 / 1\n\nContent."
    assert result[4] == "#### Headline 4 / 2"


def test_chunk_md():
    result = chunk_md(MD)
    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0] == "# Headline 1\n\nContent."
    assert result[1] == "## Headline 2 / 1\n\nContent."
    assert result[2] == "### Headline 3 / 1\n\n#### Headline 4 / 1\n\nContent."
