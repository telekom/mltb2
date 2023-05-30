# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

from math import isclose

from mltb2.somajo import JaccardSimilarity, SoMaJoSentenceSplitter


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


def test_JaccardSimilarity_call():
    text1 = "Das ist ein deutscher Text."
    text2 = "Das ist ein anderer Text."
    jaccard_similarity = JaccardSimilarity("de_CMC")
    result1 = jaccard_similarity(text1, text2)
    result2 = jaccard_similarity(text2, text1)

    assert isclose(result1, result2)
    assert isclose(result1, 5 / 7)
    assert result1 < 1.0
    assert result2 > 0.0


def test_JaccardSimilarity_call_same():
    text = "Das ist ein deutscher Text."
    jaccard_similarity = JaccardSimilarity("de_CMC")
    result = jaccard_similarity(text, text)

    assert isclose(result, 1.0)


def test_JaccardSimilarity_call_no_overlap():
    text1 = "Das ist ein deutscher Text."
    text2 = "Vollkommen anders!"
    jaccard_similarity = JaccardSimilarity("de_CMC")
    result = jaccard_similarity(text1, text2)

    assert isclose(result, 0.0)
