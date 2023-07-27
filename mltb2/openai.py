# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""OpenAI specific functionality.

Use pip to install the necessary dependencies for this module:
``pip install mltb2[openai]``
"""


from dataclasses import dataclass, field
from typing import Iterable, List, Union

import tiktoken
from tiktoken.core import Encoding
from tqdm import tqdm


@dataclass
class OpenAiTokenCounter:
    """Count OpenAI tokens.

    Args:
        model_name: The OpenAI model name.
        show_progress_bar: Show a progressbar during processing.
    """

    model_name: str
    encoding: Encoding = field(init=False, repr=False)
    show_progress_bar: bool = False

    def __post_init__(self):
        """Do post init."""
        self.encoding = tiktoken.encoding_for_model(self.model_name)

    def __call__(self, text: Union[str, Iterable]) -> Union[int, List[int]]:
        """Count tokens for text.

        Args:
            text: The text for which the tokens are to be counted.
        Returns:
            The number of tokens if text was just a ``str``.
            If text is an ``Iterable`` then a ``list`` of number of tokens.
        """
        if isinstance(text, str):
            tokenized_text = self.encoding.encode(text)
            return len(tokenized_text)
        else:
            counts = []
            for t in tqdm(text, disable=not self.show_progress_bar):
                tokenized_text = self.encoding.encode(t)
                counts.append(len(tokenized_text))
            return counts
