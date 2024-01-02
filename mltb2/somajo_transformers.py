# Copyright (c) 2023 Philip May
# Copyright (c) 2023 Philip May, Deutsche Telekom AG
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""This module offers Hugging Face Transformers and SoMaJo specific tools.

This module is based on
`Hugging Face Transformers <https://huggingface.co/docs/transformers/index>`_ and
`SoMaJo <https://github.com/tsproisl/SoMaJo>`_.

Hint:
    Use pip to install the necessary dependencies for this module:
    ``pip install mltb2[somajo_transformers]``
"""


from dataclasses import dataclass
from typing import List

from tqdm import tqdm

from mltb2.somajo import SoMaJoSentenceSplitter
from mltb2.transformers import TransformersTokenCounter


@dataclass
class TextSplitter:
    """Split the text into sections with a specified maximum token number.

    Does not divide words, but always whole sentences.

    Args:
        max_token: Maximum number of tokens per text section.
        somajo_sentence_splitter: The sentence splitter to be used.
        transformers_token_counter: The token counter to be used.
        show_progress_bar: Show a progressbar during processing.
        ignore_overly_long_sentences: If this is ``False`` an ``ValueError`` exception is
            raised if a sentence is longer than ``max_token``.
            If it is ``True``, then the sentence is simply ignored.
    """

    max_token: int
    somajo_sentence_splitter: SoMaJoSentenceSplitter
    transformers_token_counter: TransformersTokenCounter
    show_progress_bar: bool = False
    ignore_overly_long_sentences: bool = False

    def __call__(self, text: str) -> List[str]:
        """Split the text into sections.

        Args:
            text: The text to be split.
        Returns:
            The list of section splits.
        """
        sentences = self.somajo_sentence_splitter(text)
        counts = self.transformers_token_counter(sentences)

        assert len(sentences) == len(counts)  # type: ignore[arg-type]

        result_splits: List[str] = []
        current_sentences: List[str] = []
        current_count: int = 0
        for sentence, count in zip(tqdm(sentences, disable=not self.show_progress_bar), counts):  # type: ignore[arg-type]
            if count > self.max_token:
                if self.ignore_overly_long_sentences:
                    continue
                else:
                    raise ValueError("No sentence may be longer than 'max_token'.")
            if current_count + count <= self.max_token:
                current_count += count
                current_sentences.append(sentence)
            else:
                result_split = " ".join(current_sentences)
                result_splits.append(result_split)
                current_sentences = []
                current_count = 0
                current_count += count
                current_sentences.append(sentence)

        # add the rest
        if len(current_sentences) > 0:
            result_split = " ".join(current_sentences)
            result_splits.append(result_split)

        return result_splits
