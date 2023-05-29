# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""SoMaJo and Transformers tools."""


from dataclasses import dataclass
from typing import List

from tqdm.auto import tqdm

from mltb2.somajo import SoMaJoSentenceSplitter
from mltb2.transformers import TransformersTokenCounter


@dataclass
class TextSplitter:
    """Split the text into sections with a specified maximum token length.

    Does not divide words, but always whole sentences.
    """

    max_token: int
    somajo_sentence_splitter: SoMaJoSentenceSplitter
    transformers_token_counter: TransformersTokenCounter
    show_progress_bar: bool = True

    def __call__(self, text: str) -> List[str]:
        """Split the text into sections."""
        sentences = self.somajo_sentence_splitter(text)
        counts = self.transformers_token_counter(sentences)

        assert len(sentences) == len(counts)  # type: ignore

        result_splits: List[str] = []
        current_sentences: List[str] = []
        current_count: int = 0
        for sentence, count in zip(
            tqdm(sentences, disable=not self.show_progress_bar), counts  # type: ignore
        ):
            if count > self.max_token:
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
