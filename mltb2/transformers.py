# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""Transformers tools."""

import os
from dataclasses import dataclass, field
from typing import Iterable, List, Union

from transformers import AutoTokenizer
from transformers.tokenization_utils import PreTrainedTokenizerBase


@dataclass
class TransformersTokenCounter:
    """Count Transformers tokenizer tokens."""

    pretrained_model_name_or_path: Union[str, os.PathLike]
    tokenizer: PreTrainedTokenizerBase = field(init=False, repr=False)

    def __post_init__(self):
        """Do post init."""
        self.tokenizer = AutoTokenizer.from_pretrained(self.pretrained_model_name_or_path)

    def __call__(self, text: Union[str, Iterable]) -> Union[int, List[int]]:
        """Count tokens for text."""
        if isinstance(text, str):
            tokenized_text = self.tokenizer.tokenize(text)
            return len(tokenized_text)
        else:
            counts = []
            for t in text:
                tokenized_text = self.tokenizer.tokenize(t)
                counts.append(len(tokenized_text))
            return counts
