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
from openai.types.chat import ChatCompletion
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
class OpenAiChatResult:
    """TODO: add docstring.

    Args:
        content: the result of the OpenAI completion
        model: model name which has been used
        prompt_tokens: number of tokens of the prompt
        completion_tokens: number of tokens of the completion (``text``)
        total_tokens: number of total tokens (``prompt_tokens + completion_tokens``)
        finish_reason: The reason why the completion stopped.

            * ``stop``: Means the API returned the full completion without running into any token limit.
            * ``length``: Means the API stopped the completion because of running into a token limit.
            * ``function_call``: When the model called a function.
    """

    content: Optional[str] = None
    model: Optional[str] = None
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    finish_reason: Optional[str] = None
    completion_args: Optional[Dict[str, Any]] = None

    @classmethod
    def from_chat_completion(
        cls,
        chat_completion: ChatCompletion,
        completion_kwargs: Optional[Dict[str, Any]] = None,
    ):
        """TODO: add docstring."""
        result = {}
        result["completion_args"] = completion_kwargs
        chat_completion_dict = chat_completion.model_dump()
        result["model"] = chat_completion_dict.get("model")
        usage = chat_completion_dict.get("usage")
        if usage is not None:
            result["prompt_tokens"] = usage.get("prompt_tokens")
            result["completion_tokens"] = usage.get("completion_tokens")
            result["total_tokens"] = usage.get("total_tokens")
        choices = chat_completion_dict.get("choices")
        if choices is not None and len(choices) > 0:
            choice = choices[0]
            result["finish_reason"] = choice.get("finish_reason")
            message = choice.get("message")
            if message is not None:
                result["content"] = message.get("content")
        return cls(**result)  # type: ignore[arg-type]


@dataclass
class OpenAiChat:
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

    def __call__(
        self,
        prompt: Union[str, List[Dict[str, str]]],
        completion_kwargs: Optional[Dict[str, Any]] = None,
    ):
        """TODO: add docstring."""
        # TODO: check key of messages
        completion_kwargs = {} if completion_kwargs is None else completion_kwargs
        messages = [{"role": "user", "content": prompt}] if isinstance(prompt, str) else prompt
        chat_completion = self.client.chat.completions.create(
            messages=messages,  # type: ignore[arg-type]
            model=self.model,
            **completion_kwargs,
        )
        result = OpenAiChatResult.from_chat_completion(chat_completion, completion_kwargs=completion_kwargs)
        return result


@dataclass
class OpenAiAzureChat(OpenAiChat):
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
