# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT


from mltb2.fasttext import FastTextLanguageIdentification


def test_fasttext_language_identification_get_model_path_and_download():
    model_path = FastTextLanguageIdentification.get_model_path_and_download()
    assert model_path is not None


def test_fasttext_language_identification_call():
    language_identification = FastTextLanguageIdentification()
    languages = language_identification("This is an English sentence.")
    assert languages is not None
    assert len(languages) == 10


def test_fasttext_language_identification_call_with_always_detect_lang():
    language_identification = FastTextLanguageIdentification()
    languages = language_identification("This is an English sentence.", always_detect_lang=["fake_language"])
    assert languages is not None
    assert len(languages) == 11
    assert "fake_language" in languages
