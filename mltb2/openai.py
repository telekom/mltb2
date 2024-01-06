# Copyright (c) 2023-2024 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""OpenAI specific module.

Hint:
    Use pip to install the necessary dependencies for this module:
    ``pip install mltb2[openai]``
"""


from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Union

import tiktoken
import yaml
from openai import AzureOpenAI, OpenAI
from tiktoken.core import Encoding
from tqdm import tqdm


@dataclass
class OpenAiTokenCounter:
    """Count OpenAI tokens.

    Args:
        model_name:
            The OpenAI model name. Some examples:

            * ``gpt-4``
            * ``gpt-3.5-turbo``
            * ``text-davinci-003``
            * ``text-embedding-ada-002``

        show_progress_bar: Show a progressbar during processing.
    """

    model_name: str
    encoding: Encoding = field(init=False, repr=False)
    show_progress_bar: bool = False

    def __post_init__(self) -> None:
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


@dataclass
class OpenAiChatCompletion:
    """TODO: add docstring."""

    api_key: str
    model: str
    client: Union[OpenAI, AzureOpenAI] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Do post init."""
        self.client = OpenAI(api_key=self.api_key)

    @classmethod
    def from_yaml(cls, yaml_file):
        """Construct this class from a yaml file."""
        with open(yaml_file, "r") as file:
            completion_kwargs = yaml.safe_load(file)
        return cls(**completion_kwargs)

    def __call__(self, prompt: Union[str, List[Dict[str, str]]], completion_kwargs: Optional[Dict[str, Any]] = None):
        """TODO: add docstring."""
        # TODO: check key of messages
        completion_kwargs = {} if completion_kwargs is None else completion_kwargs
        messages = [{"role": "user", "content": prompt}] if isinstance(prompt, str) else prompt
        chat_completion = self.client.chat.completions.create(
            messages=messages,  # type: ignore[arg-type]
            model=self.model,
            **completion_kwargs,
        )
        return chat_completion


@dataclass
class OpenAiAzureChatCompletion(OpenAiChatCompletion):
    """TODO: add docstring."""

    api_version: str
    azure_endpoint: str

    def __post_init__(self) -> None:
        """Do post init."""
        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.azure_endpoint,
        )
