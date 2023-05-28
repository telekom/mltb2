# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""Tokenizer tools."""


from dataclasses import dataclass, field
from typing import List

from somajo import SoMaJo


@dataclass
class SoMaJoSentenceSplitter:
    """Use SoMaJo to split text into sentences.

    Args:
        language: The language. ``de_CMC`` for German or ``en_PTB`` for English.
    """

    language: str
    somajo: SoMaJo = field(init=False, repr=False)

    def __post_init__(self):
        """Do post init."""
        self.somajo = SoMaJo(self.language)

    # see https://github.com/tsproisl/SoMaJo/issues/17
    @staticmethod
    def detokenize(tokens) -> str:
        """Convert SoMaJo tokens to sentence (string)."""
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
        """Split the test into a list of sentences."""
        sentences = self.somajo.tokenize_text([text])

        result = []

        for sentence in sentences:
            sentence_string = self.detokenize(sentence)
            result.append(sentence_string)

        return result
