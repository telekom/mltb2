# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""OpenAI specific functionality.

Use pip to install the necessary dependencies for this module:
``pip install mltb2[openai]``
"""


from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional, Union

import tiktoken
import yaml
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

    @classmethod
    def from_open_ai_object(cls, open_ai_object: OpenAIObject):
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
        return cls(**result)


@dataclass
class OpenAiBaseCompletion(ABC):
    """Abstract base class for OpenAI completion.

    Args:
        completion_kwargs: kwargs for the OpenAI completion function

    See Also:
        * `Create chat completion <https://platform.openai.com/docs/api-reference/chat/create>`_
        * `Create completion <https://platform.openai.com/docs/api-reference/completions/create>`_
    """

    completion_kwargs: Dict[str, Any]

    @classmethod
    def from_yaml(cls, yaml_file):
        """Construct this class from a yaml file."""
        with open(yaml_file, "r") as file:
            completion_kwargs = yaml.safe_load(file)
        return cls(completion_kwargs)

    @abstractmethod
    def _completion(
        self, prompt: Union[str, List[Dict[str, str]]], completion_kwargs_for_this_call: Mapping[str, Any]
    ) -> OpenAIObject:
        """Abstract method to call the OpenAI completion."""
        pass

    def __call__(
        self, prompt: Union[str, List[Dict[str, str]]], completion_kwargs: Optional[Mapping[str, Any]] = None
    ) -> OpenAiCompletionAnswer:
        """Call the OpenAI prompt completion.

        Args:
            prompt: The prompt to be completed by the LLM.
                In case of chat models this can be a string or a list.
                In case of "non chat" models only a string is allowed.
            completion_kwargs: Overwrite the ``completion_kwargs`` for this call.
                This allows you, for example, to change the temperature for this call only.
        """
        completion_kwargs_for_this_call = self.completion_kwargs.copy()
        if completion_kwargs is not None:
            completion_kwargs_for_this_call.update(completion_kwargs)
        open_ai_object: OpenAIObject = self._completion(prompt, completion_kwargs_for_this_call)
        open_ai_completion_answer = OpenAiCompletionAnswer.from_open_ai_object(open_ai_object)
        return open_ai_completion_answer


@dataclass
class OpenAiChatCompletion(OpenAiBaseCompletion):
    """OpenAI chat completion.

    This also be constructed with :meth:`OpenAiBaseCompletion.from_yaml`.

    Args:
        completion_kwargs: The kwargs for the OpenAI completion function.

    See Also:
        `Create chat completion <https://platform.openai.com/docs/api-reference/chat/create>`_
    """

    def _completion(
        self, prompt: Union[str, List[Dict[str, str]]], completion_kwargs_for_this_call: Mapping[str, Any]
    ) -> OpenAIObject:
        """Call to the OpenAI chat completion."""
        if isinstance(prompt, str):
            messages = [{"role": "user", "content": prompt}]
        else:
            messages = prompt
        open_ai_object: OpenAIObject = ChatCompletion.create(
            messages=messages,
            **completion_kwargs_for_this_call,
        )
        return open_ai_object


def _check_mandatory_azure_completion_kwargs(completion_kwargs: Mapping[str, Any]) -> None:
    """Check mandatory Azure ``completion_kwargs``."""
    for mandatory_azure_completion_kwarg in ("api_base", "engine", "api_type", "api_version"):
        if mandatory_azure_completion_kwarg not in completion_kwargs:
            raise ValueError(f"You must set '{mandatory_azure_completion_kwarg}' for Azure completion!")
    if completion_kwargs["api_type"] != "azure":
        raise ValueError("You must set 'api_type' to 'azure' for Azure completion!")


@dataclass
class OpenAiAzureChatCompletion(OpenAiChatCompletion):
    """OpenAI Azure chat completion.

    This also be constructed with :meth:`OpenAiBaseCompletion.from_yaml`.

    Args:
        completion_kwargs: The kwargs for the OpenAI completion function.
            The following Azure specific properties must be specified:

                * ``api_type``
                * ``api_version``
                * ``api_base``
                * ``engine``

    See Also:
        * `Create chat completion <https://platform.openai.com/docs/api-reference/chat/create>`_
        * `Quickstart: Get started using GPT-35-Turbo and GPT-4 with Azure OpenAI Service <https://learn.microsoft.com/en-us/azure/ai-services/openai/chatgpt-quickstart?tabs=command-line&pivots=programming-language-python>`_
    """

    def __post_init__(self) -> None:
        """Do post init."""
        _check_mandatory_azure_completion_kwargs(self.completion_kwargs)


@dataclass
class OpenAiCompletion(OpenAiBaseCompletion):
    """OpenAI (non chat) completion.

    This also be constructed with :meth:`OpenAiBaseCompletion.from_yaml`.

    Args:
        completion_kwargs: The kwargs for the OpenAI completion function.

    See Also:
        `Create completion <https://platform.openai.com/docs/api-reference/completions/create>`_
    """

    def _completion(
        self, prompt: Union[str, List[Dict[str, str]]], completion_kwargs_for_this_call: Mapping[str, Any]
    ) -> OpenAIObject:
        """Call to the OpenAI (not chat) completion."""
        open_ai_object: OpenAIObject = Completion.create(
            prompt=prompt,
            **completion_kwargs_for_this_call,
        )
        return open_ai_object


@dataclass
class OpenAiAzureCompletion(OpenAiCompletion):
    """OpenAI Azure (non chat) completion.

    This also be constructed with :meth:`OpenAiBaseCompletion.from_yaml`.

    Args:
        completion_kwargs: The kwargs for the OpenAI completion function.
            The following Azure specific properties must be specified:

                * ``api_type``
                * ``api_version``
                * ``api_base``
                * ``engine``

    See Also:
        * `Create completion <https://platform.openai.com/docs/api-reference/completions/create>`_
        * `Quickstart: Get started generating text using Azure OpenAI Service <https://learn.microsoft.com/en-us/azure/ai-services/openai/quickstart?tabs=command-line&pivots=programming-language-python>`_
    """

    def __post_init__(self) -> None:
        """Do post init."""
        _check_mandatory_azure_completion_kwargs(self.completion_kwargs)
