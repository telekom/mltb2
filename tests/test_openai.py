# Copyright (c) 2023-2024 Philip May
# Copyright (c) 2024 Philip May, Deutsche Telekom AG
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

import os
from pathlib import Path
from typing import List

import pytest
import yaml
from hypothesis import given, settings
from hypothesis.strategies import lists, text

from mltb2.openai import OpenAiChat, OpenAiTokenCounter


@pytest.fixture(scope="module")
def gpt_4_open_ai_token_counter() -> OpenAiTokenCounter:
    return OpenAiTokenCounter("gpt-4")


@settings(max_examples=1000)
@given(text=text())
def test_OpenAiTokenCounter_str_hypothesis(text: str, gpt_4_open_ai_token_counter: OpenAiTokenCounter):
    token_count = gpt_4_open_ai_token_counter(text)
    assert token_count >= 0  # type: ignore[operator]


def test_OpenAiTokenCounter_call_string():
    token_counter = OpenAiTokenCounter("gpt-4")
    token_count = token_counter("Das ist ein Text.")

    assert token_count == 5


@settings(max_examples=1000)
@given(texts=lists(text()))
def test_OpenAiTokenCounter_list_hypothesis(texts: List[str], gpt_4_open_ai_token_counter: OpenAiTokenCounter):
    token_count = gpt_4_open_ai_token_counter(texts)
    assert len(token_count) == len(texts)  # type: ignore[arg-type]
    assert all(count >= 0 for count in token_count)  # type: ignore[union-attr]


def test_OpenAiTokenCounter_call_list():
    token_counter = OpenAiTokenCounter("gpt-4")
    token_count = token_counter(["Das ist ein Text.", "Das ist ein anderer Text."])

    assert isinstance(token_count, list)
    assert len(token_count) == 2
    assert token_count[0] == 5
    assert token_count[1] == 7


def test_OpenAiChat__missing_role_message_key():
    open_ai_chat = OpenAiChat(api_key="secret", model="apt-4")
    invalid_prompt_as_list = [{"x": "user", "content": "prompt"}]
    with pytest.raises(ValueError):
        open_ai_chat(invalid_prompt_as_list)


def test_OpenAiChat__missing_content_message_key():
    open_ai_chat = OpenAiChat(api_key="secret", model="apt-4")
    invalid_prompt_as_list = [{"role": "user", "x": "prompt"}]
    with pytest.raises(ValueError):
        open_ai_chat(invalid_prompt_as_list)


def test_OpenAiChat__invalid_role_in_message_key():
    open_ai_chat = OpenAiChat(api_key="secret", model="apt-4")
    invalid_prompt_as_list = [{"role": "x", "content": "prompt"}]
    with pytest.raises(ValueError):
        open_ai_chat(invalid_prompt_as_list)


def test_OpenAiChat__model_in_completion_kwargs():
    open_ai_chat = OpenAiChat(api_key="secret", model="apt-4")
    with pytest.raises(ValueError):
        open_ai_chat("Hello!", completion_kwargs={"model": "gpt-4"})


def test_OpenAiChat__messages_in_completion_kwargs():
    open_ai_chat = OpenAiChat(api_key="secret", model="apt-4")
    with pytest.raises(ValueError):
        open_ai_chat("Hello!", completion_kwargs={"messages": "World!"})


def test_OpenAiChat__from_yaml_key_from_env(tmp_path: Path):
    # create yaml file
    yaml_file = tmp_path / "openai_config.yaml"
    yaml_file_dict = {
        # "api_key": "some_api_key",
        "model": "some_model",
    }
    with open(yaml_file, "w") as file:
        yaml.dump(yaml_file_dict, file)

    os.environ["OPENAI_API_KEY"] = "some_other_api_key"

    open_ai_chat = OpenAiChat.from_yaml(yaml_file)

    assert open_ai_chat.api_key == "some_other_api_key"
    assert open_ai_chat.model == "some_model"
