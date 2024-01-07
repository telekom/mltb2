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
    """Result of an OpenAI chat completion.

    If you want to convert this to a ``dict`` use ``asdict(open_ai_chat_result)``
    from the ``dataclasses`` module.

    See Also:
        OpenAI API reference: `The chat completion object <https://platform.openai.com/docs/api-reference/chat/object>`_

    Args:
        content: the result of the OpenAI completion
        model: model name which has been used
        prompt_tokens: number of tokens of the prompt
        completion_tokens: number of tokens of the completion (``content``)
        total_tokens: number of total tokens (``prompt_tokens + content_tokens``)
        finish_reason: The reason why the completion stopped.

            * ``stop``: Means the API returned the full completion without running into any token limit.
            * ``length``: Means the API stopped the completion because of running into a token limit.
            * ``content_filter``: When content was omitted due to a flag from the OpenAI content filters.
            * ``tool_calls``: When the model called a tool.
            * ``function_call`` (deprecated): When the model called a function.

        completion_args: The arguments which have been used for the completion. Examples:

            * ``model``: always set
            * ``max_tokens``: only set if ``completion_kwargs`` contained ``max_tokens``
            * ``temperature``: only set if ``completion_kwargs`` contained ``temperature``
            * ``top_p``: only set if ``completion_kwargs`` contained ``top_p``
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
        """Construct this class from an OpenAI ``ChatCompletion`` object.

        Args:
            chat_completion: The OpenAI ``ChatCompletion`` object.
            completion_kwargs: The arguments which have been used for the completion.
        Returns:
            The constructed class.
        """
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
    """Tool to interact with OpenAI chat models.

    This also be constructed with :meth:`~OpenAiChat.from_yaml`.

    See Also:
        OpenAI API reference: `Create chat completion <https://platform.openai.com/docs/api-reference/chat/create>`_

    Args:
        api_key: The OpenAI API key.
        model: The OpenAI model name.
    """

    api_key: str
    model: str
    client: Union[OpenAI, AzureOpenAI] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Do post init."""
        self.client = OpenAI(api_key=self.api_key)

    @classmethod
    def from_yaml(cls, yaml_file):
        """Construct this class from a yaml file.

        Args:
            yaml_file: The yaml file.
        Returns:
            The constructed class.
        """
        with open(yaml_file, "r") as file:
            completion_kwargs = yaml.safe_load(file)
        return cls(**completion_kwargs)

    def __call__(
        self,
        prompt: Union[str, List[Dict[str, str]]],
        completion_kwargs: Optional[Dict[str, Any]] = None,
    ) -> OpenAiChatResult:
        """Create a model response for the given prompt (chat conversation).

        Args:
            prompt: The prompt for the model.
            completion_kwargs: Keyword arguments for the OpenAI completion.

                - ``model`` can not be set via ``completion_kwargs``! Please set the ``model`` in the initializer.
                - ``messages`` can not be set via ``completion_kwargs``! Please set the ``prompt`` argument.

                Also see:

                    - ``openai.resources.chat.completions.Completions.create()``
                    - OpenAI API reference: `Create chat completion <https://platform.openai.com/docs/api-reference/chat/create>`_

        Returns:
            The result of the OpenAI completion.
        """
        if isinstance(prompt, list):
            for message in prompt:
                if "role" not in message or "content" not in message:
                    raise ValueError(
                        "If prompt is a list of messages, each message must have a 'role' and 'content' key!"
                    )
                if message["role"] not in ["system", "user", "assistant", "tool"]:
                    raise ValueError(
                        "If prompt is a list of messages, each message must have a 'role' key with one of the values "
                        "'system', 'user', 'assistant' or 'tool'!"
                    )

        if completion_kwargs is not None:
            # check keys of completion_kwargs
            if "model" in completion_kwargs:
                raise ValueError(
                    "'model' can not be set via 'completion_kwargs'! Please set the 'model' in the initializer."
                )
            if "messages" in completion_kwargs:
                raise ValueError(
                    "'messages' can not be set via 'completion_kwargs'! Please set the 'prompt' argument."
                )
        else:
            completion_kwargs = {}  # set default value
        completion_kwargs["model"] = self.model
        messages = [{"role": "user", "content": prompt}] if isinstance(prompt, str) else prompt
        chat_completion = self.client.chat.completions.create(
            messages=messages,  # type: ignore[arg-type]
            **completion_kwargs,
        )
        result = OpenAiChatResult.from_chat_completion(chat_completion, completion_kwargs=completion_kwargs)
        return result


@dataclass
class OpenAiAzureChat(OpenAiChat):
    """Tool to interact with Azure OpenAI chat models.

    This can also be constructed with :meth:`~OpenAiChat.from_yaml`.

    See Also:
        * OpenAI API reference: `Create chat completion <https://platform.openai.com/docs/api-reference/chat/create>`_
        * `Quickstart: Get started generating text using Azure OpenAI Service <https://learn.microsoft.com/en-us/azure/ai-services/openai/quickstart?tabs=command-line&pivots=programming-language-python>`_

    Args:
        api_key: The OpenAI API key.
        model: The OpenAI model name.
        api_version: The OpenAI API version.
            A common value for this is ``2023-05-15``.
        azure_endpoint: The Azure endpoint.
    """

    api_version: str
    azure_endpoint: str

    def __post_init__(self) -> None:
        """Do post init."""
        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.azure_endpoint,
        )
