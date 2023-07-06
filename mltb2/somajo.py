# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""SoMaJo specific functionality.

This module is based on `SoMaJo <https://github.com/tsproisl/SoMaJo>`_.
Use pip to install the necessary dependencies for this module:
``pip install mltb2[somajo]``
"""


from abc import ABC
from dataclasses import dataclass, field
from typing import List, Set

from somajo import SoMaJo
from tqdm import tqdm


@dataclass
class SoMaJoBaseClass(ABC):
    """Base Class for SoMaJo tools."""

    language: str
    somajo: SoMaJo = field(init=False, repr=False)

    def __post_init__(self):
        """Do post init."""
        self.somajo = SoMaJo(self.language)


@dataclass
class SoMaJoSentenceSplitter(SoMaJoBaseClass):
    """Use SoMaJo to split text into sentences.

    Args:
        language: The language. ``de_CMC`` for German or ``en_PTB`` for English.
        show_progress_bar: Show a progressbar during processing.
    """

    show_progress_bar: bool = False

    # see https://github.com/tsproisl/SoMaJo/issues/17
    @staticmethod
    def detokenize(tokens) -> str:
        """Convert SoMaJo tokens to sentence (string).

        Args:
            tokens: The tokens to be de-tokenized.
        Returns:
            The de-tokenized sentence.
        """
        result_list = []
        for token in tokens:
            if token.original_spelling is not None:
                result_list.append(token.original_spelling)
            else:
                result_list.append(token.text)

            if token.space_after:
                result_list.append(" ")
        result = "".join(result_list)
        result = result.strip()
        return result

    def __call__(self, text: str) -> List[str]:
        """Split the text into a list of sentences.

        Args:
            text: The text to be split.
        Returns:
            The list of sentence splits.
        """
        sentences = self.somajo.tokenize_text([text])

        result = []

        for sentence in tqdm(sentences, disable=not self.show_progress_bar):
            sentence_string = self.detokenize(sentence)
            result.append(sentence_string)

        return result


@dataclass
class JaccardSimilarity(SoMaJoBaseClass):
    """Calculate the `jaccard similarity <https://en.wikipedia.org/wiki/Jaccard_index>`_.

    Args:
        language: The language. ``de_CMC`` for German or ``en_PTB`` for English.
    """

    def get_token_set(self, text: str) -> Set[str]:
        """Get token set for text.

        Args:
            text: The text to be tokenized into a set.
        Returns:
            The set of tokens (words).
        """
        sentences = self.somajo.tokenize_text([text])
        tokens = [t.text.lower() for sentence in sentences for t in sentence]
        # TODO: add option to filter tokens
        token_set = set(tokens)
        return token_set

    def __call__(self, text1: str, text2: str) -> float:
        """Calculate the jaccard similarity for two texts.

        Args:
            text1: Text one.
            text2: Text two.
        Returns:
            The jaccard similarity.
        """
        token_set1 = self.get_token_set(text1)
        token_set2 = self.get_token_set(text2)
        intersection = token_set1.intersection(token_set2)
        union = token_set1.union(token_set2)
        jaccard_similarity = float(len(intersection)) / len(union)
        return jaccard_similarity


@dataclass
class TokenExtractor(SoMaJoBaseClass):
    """Extract tokens from text.

    Args:
        language: The language. ``de_CMC`` for German or ``en_PTB`` for English.
    """

    def extract_url_set(self, text: str) -> Set[str]:
        """Extract tokens from text.

        Args:
            text: the text
        Returns:
            Set of extracted links.
        """
        sentences = self.somajo.tokenize_text([text])
        result = {token.text for sentence in sentences for token in sentence if token.token_class == "URL"}
        return result
