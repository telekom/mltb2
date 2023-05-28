# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

from mltb2.somajo import SoMaJoSentenceSplitter


def test_SoMaJoSentenceSplitter_call() -> None:
    """Test ``SoMaJoSentenceSplitter.call`` happy case."""
    splitter = SoMaJoSentenceSplitter("de_CMC")
    text = "Das ist der erste Satz. Das ist der 2. Satz."
    sentences = splitter(text)

    assert len(sentences) == 2
    assert sentences[0] == "Das ist der erste Satz."
    assert sentences[1] == "Das ist der 2. Satz."


def test_SoMaJoSentenceSplitter_call_space_and_linebreak() -> None:
    """Test ``SoMaJoSentenceSplitter.call`` with space an line break."""
    splitter = SoMaJoSentenceSplitter("de_CMC")
    text = "  Das   ist der erste Satz.   \n   Das ist der 2.  \n    Satz.  "
    sentences = splitter(text)

    assert len(sentences) == 2
    assert sentences[0] == "Das ist der erste Satz."
    assert sentences[1] == "Das ist der 2. Satz."
