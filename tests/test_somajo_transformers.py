# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT


import pytest

from mltb2.somajo import SoMaJoSentenceSplitter
from mltb2.somajo_transformers import TextSplitter
from mltb2.transformers import TransformersTokenCounter


def test_TextSplitter_call():
    somajo_sentence_splitter = SoMaJoSentenceSplitter("de_CMC")
    transformers_token_counter = TransformersTokenCounter("deepset/gbert-base")
    text_splitter = TextSplitter(
        max_token=12,
        somajo_sentence_splitter=somajo_sentence_splitter,
        transformers_token_counter=transformers_token_counter,
    )
    text = " ".join([f"Satz {i} ist das." for i in range(5)])
    split_text = text_splitter(text)

    assert isinstance(split_text, list)
    assert len(split_text) == 3
    assert split_text[0] == "Satz 0 ist das. Satz 1 ist das."
    assert split_text[1] == "Satz 2 ist das. Satz 3 ist das."
    assert split_text[2] == "Satz 4 ist das."


def test_TextSplitter_call_sentence_too_long():
    somajo_sentence_splitter = SoMaJoSentenceSplitter("de_CMC")
    transformers_token_counter = TransformersTokenCounter("deepset/gbert-base")
    text_splitter = TextSplitter(
        max_token=3,
        somajo_sentence_splitter=somajo_sentence_splitter,
        transformers_token_counter=transformers_token_counter,
    )
    text = " ".join([f"Satz {i} ist das." for i in range(5)])

    with pytest.raises(ValueError):
        text_splitter(text)
