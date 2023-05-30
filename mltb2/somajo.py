# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""SoMaJo tools."""


from dataclasses import dataclass, field
from typing import List

from somajo import SoMaJo
from tqdm.auto import tqdm


@dataclass
class SoMaJoSentenceSplitter:
    """Use SoMaJo to split text into sentences.

    Args:
        language: The language. ``de_CMC`` for German or ``en_PTB`` for English.
        show_progress_bar: Show a progressbar during processing.
    """

    language: str
    somajo: SoMaJo = field(init=False, repr=False)
    show_progress_bar: bool = True

    def __post_init__(self):
        """Do post init."""
        self.somajo = SoMaJo(self.language)

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