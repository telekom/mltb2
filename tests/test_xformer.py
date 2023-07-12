# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT


from mltb2.xformer import TransformersTokenCounter


def test_TransformersTokenCounter_call_string():
    transformers_token_counter = TransformersTokenCounter("deepset/gbert-base")
    token_count = transformers_token_counter("Das ist ein Text.")

    assert token_count == 5


def test_TransformersTokenCounter_call_list():
    transformers_token_counter = TransformersTokenCounter("deepset/gbert-base")
    token_count = transformers_token_counter(["Das ist ein Text.", "Das ist ein anderer Text."])

    assert isinstance(token_count, list)
    assert len(token_count) == 2
    assert token_count[0] == 5
    assert token_count[1] == 6
