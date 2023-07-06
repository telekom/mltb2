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
from typing import Container, Iterable, List, Optional, Set

from somajo import SoMaJo
from tqdm import tqdm


@dataclass
class SoMaJoBaseClass(ABC):
    """Base Class for SoMaJo tools.

    Args:
        language: The language. ``de_CMC`` for German or ``en_PTB`` for English.

    Note:
        This class is an abstract base class. It should not be used directly.
    """

    language: str
    somajo: SoMaJo = field(init=False, repr=False)

    def __post_init__(self):
        """Do post init."""
        self.somajo = SoMaJo(self.language)


def detokenize(tokens) -> str:
    """Convert SoMaJo tokens to sentence (string).

    Args:
        tokens: The tokens to be de-tokenized.
    Returns:
        The de-tokenized sentence.

    See Also:
        `How do I split sentences but not words? <https://github.com/tsproisl/SoMaJo/issues/17>`_
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


def extract_token_class_set(sentences: Iterable, keep_token_classes: Optional[Container[str]] = None) -> Set[str]:
    """Extract token from sentences by token class.

    Args:
        sentences: The sentences from which to extract.
        keep_token_classes: The token classes to keep. If ``None`` all will be kept.
    Returns:
        The set of extracted token texts.
    """
    result = set()
    for sentence in sentences:
        for token in sentence:
            if keep_token_classes is None:
                result.add(token.text)
            elif token.token_class in keep_token_classes:
                result.add(token.text)
            # else ignore
    return result


@dataclass
class SoMaJoSentenceSplitter(SoMaJoBaseClass):
    """Use SoMaJo to split text into sentences.

    Args:
        language: The language. ``de_CMC`` for German or ``en_PTB`` for English.
        show_progress_bar: Show a progressbar during processing.
    """

    show_progress_bar: bool = False

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
            sentence_string = detokenize(sentence)
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
        token_set = extract_token_class_set(sentences)  # TODO: filter tokens
        token_set = {t.lower() for t in token_set}

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
        """Extract URLs from text.

        Args:
            text: the text
        Returns:
            Set of extracted links.
        """
        sentences = self.somajo.tokenize_text([text])
        result = extract_token_class_set(sentences, keep_token_classes="URL")
        return result
