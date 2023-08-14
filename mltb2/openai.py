# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""OpenAI specific functionality.

Use pip to install the necessary dependencies for this module:
``pip install mltb2[openai]``
"""


from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Union

import tiktoken
from dotenv import dotenv_values
from openai import ChatCompletion, Completion
from openai.openai_object import OpenAIObject
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


@dataclass
class OpenAiCompletionAnswer:
    """Answer of an OpenAI completion.

    Args:
        text: the result of the OpenAI completion
        model: model name which has been used
        prompt_tokens: number of tokens of the prompt
        completion_tokens: number of tokens of the completion (``text``)
        total_tokens: number of total tokens (``prompt_tokens + completion_tokens``)
        finish_reason: The reason why the completion stopped.

            * ``stop``: Means the API returned the full completion without running into any token limit.
            * ``length``: Means the API stopped the completion because of running into a token limit.
            * ``function_call``: When the model called a function.

    See Also:

        * `The chat completion object <https://platform.openai.com/docs/api-reference/chat/object>`_
        * `The completion object <https://platform.openai.com/docs/api-reference/completions/object>`_
    """

    text: Optional[str] = None
    model: Optional[str] = None
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    finish_reason: Optional[str] = None
    temperature: Optional[float] = None

    @classmethod
    def from_open_ai_object(cls, open_ai_object: OpenAIObject, temperature: Optional[float] = None):
        """Construct this class from ``OpenAIObject``."""
        result = {}
        result["model"] = open_ai_object.get("model")
        usage = open_ai_object.get("usage")
        if usage is not None:
            result["prompt_tokens"] = usage.get("prompt_tokens")
            result["completion_tokens"] = usage.get("completion_tokens")
            result["total_tokens"] = usage.get("total_tokens")
        choices = open_ai_object.get("choices")
        if choices is not None and len(choices) > 0:
            choice = choices[0]
            result["finish_reason"] = choice.get("finish_reason")
            if "text" in choice:  # non chat models
                result["text"] = choice.get("text")
            elif "message" in choice:  # chat models
                message = choice.get("message")
                if message is not None:
                    result["text"] = message.get("content")
        return cls(**result, temperature=temperature)


@dataclass
class OpenAiBaseCompletion(ABC):
    """Abstract base class for OpenAI completion.

    See Also:

        * `Create chat completion <https://platform.openai.com/docs/api-reference/chat/create>`_
        * `Create completion <https://platform.openai.com/docs/api-reference/completions/create>`_
    """

    api_type: str
    api_version: str
    api_base: str
    api_key: str
    engine: str
    base_temperature: float = 0.0
    max_tokens: Optional[int] = None

    @classmethod
    def from_env_file(cls, env_file):
        """Construct this class from an env. file.

        The following properties must be specified:

        * ``api_type``
        * ``api_version``
        * ``api_base``
        * ``api_key``
        * ``engine``

        The following properties are optional:

        * ``base_temperature`` with default value of ``0.0``
        * ``max_tokens``
        """
        open_ai_chat_completion_config = dotenv_values(env_file)
        if "base_temperature" in open_ai_chat_completion_config:
            try:
                open_ai_chat_completion_config["base_temperature"] = float(
                    open_ai_chat_completion_config["base_temperature"]
                )
            except ValueError as ve:
                raise ValueError("Can not convert 'base_temperature' to float.") from ve
        if "max_tokens" in open_ai_chat_completion_config:
            try:
                open_ai_chat_completion_config["max_tokens"] = int(open_ai_chat_completion_config["max_tokens"])
            except ValueError as ve:
                raise ValueError("Can not convert 'max_tokens' to int.") from ve
        return cls(**open_ai_chat_completion_config)

    @abstractmethod
    def _open_ai_completion(self, prompt: str, temperature: Optional[float] = None) -> OpenAIObject:
        """Abstract method to call the OpenAI completion."""
        pass

    def __call__(self, prompt: str, temperature: Optional[float] = None) -> OpenAiCompletionAnswer:
        """Call the OpenAI completion.

        Args:
            prompt: the prompt
            temperature: The temperature which can overwrite the ``base_temperature``.
        """
        if temperature is None:
            temperature = self.base_temperature
        open_ai_object: OpenAIObject = self._open_ai_completion(prompt, temperature)
        open_ai_completion_answer = OpenAiCompletionAnswer.from_open_ai_object(open_ai_object, temperature=temperature)
        return open_ai_completion_answer


@dataclass
class OpenAiChatCompletion(OpenAiBaseCompletion):
    """OpenAI chat completion.

    Can also be constructed with :meth:`OpenAiBaseCompletion.from_env_file`.

    See Also:
        `Create chat completion <https://platform.openai.com/docs/api-reference/chat/create>`_
    """

    def _open_ai_completion(self, prompt: str, temperature: Optional[float] = None) -> OpenAIObject:
        """Call to the OpenAI chat completion."""
        additional_completion_args = {}
        if self.max_tokens is not None:
            additional_completion_args["max_tokens"] = self.max_tokens
        open_ai_object: OpenAIObject = ChatCompletion.create(
            api_type=self.api_type,
            api_version=self.api_version,
            api_base=self.api_base,
            api_key=self.api_key,
            engine=self.engine,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            **additional_completion_args,
        )
        return open_ai_object


@dataclass
class OpenAiCompletion(OpenAiBaseCompletion):
    """OpenAI (non chat) completion.

    Can also be constructed with :meth:`OpenAiBaseCompletion.from_env_file`.

    See Also:
        `Create completion <https://platform.openai.com/docs/api-reference/completions/create>`_
    """

    def _open_ai_completion(self, prompt: str, temperature: Optional[float] = None) -> OpenAIObject:
        """Call to the OpenAI (not chat) completion."""
        additional_completion_args = {}
        if self.max_tokens is not None:
            additional_completion_args["max_tokens"] = self.max_tokens
        open_ai_object: OpenAIObject = Completion.create(
            api_type=self.api_type,
            api_version=self.api_version,
            api_base=self.api_base,
            api_key=self.api_key,
            engine=self.engine,
            prompt=prompt,
            temperature=temperature,
            **additional_completion_args,
        )
        return open_ai_object
