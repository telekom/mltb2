# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

from math import isclose

import pytest
from somajo import SoMaJo

from mltb2.somajo import (
    JaccardSimilarity,
    SoMaJoSentenceSplitter,
    TokenExtractor,
    UrlSwapper,
    detokenize,
    extract_token_class_set,
)


def test_SoMaJoSentenceSplitter_call() -> None:
    """Test ``SoMaJoSentenceSplitter.call`` happy case."""
    splitter = SoMaJoSentenceSplitter("de_CMC")
    text = "Das ist der erste Satz. Das ist der 2. Satz."
    sentences = splitter(text)

    assert len(sentences) == 2
    assert sentences[0] == "Das ist der erste Satz."
    assert sentences[1] == "Das ist der 2. Satz."


def test_SoMaJoSentenceSplitter_call_space_and_linebreak() -> None:
    """Test ``SoMaJoSentenceSplitter.call`` with space an line break."""
    splitter = SoMaJoSentenceSplitter("de_CMC")
    text = "  Das   ist der erste Satz.   \n   Das ist der 2.  \n    Satz.  "
    sentences = splitter(text)

    assert len(sentences) == 2
    assert sentences[0] == "Das ist der erste Satz."
    assert sentences[1] == "Das ist der 2. Satz."


def test_JaccardSimilarity_call():
    text1 = "Das ist ein deutscher Text."
    text2 = "Das ist ein anderer Text."
    jaccard_similarity = JaccardSimilarity("de_CMC")
    result1 = jaccard_similarity(text1, text2)
    result2 = jaccard_similarity(text2, text1)

    assert isclose(result1, result2)
    assert isclose(result1, 5 / 7)
    assert result1 < 1.0
    assert result2 > 0.0


def test_JaccardSimilarity_call_same():
    text = "Das ist ein deutscher Text."
    jaccard_similarity = JaccardSimilarity("de_CMC")
    result = jaccard_similarity(text, text)

    assert isclose(result, 1.0)


def test_JaccardSimilarity_call_no_overlap():
    text1 = "Das ist ein deutscher Text."
    text2 = "Vollkommen anders!"
    jaccard_similarity = JaccardSimilarity("de_CMC")
    result = jaccard_similarity(text1, text2)

    assert isclose(result, 0.0)


def test_TokenExtractor_extract_url_set_with_str():
    url1 = "http://may.la"
    url2 = "github.com"
    text_with_url = f"{url1} Das ist ein Text. {url2} Er enthält eine URL."
    token_extractor = TokenExtractor("de_CMC")
    result = token_extractor.extract_url_set(text_with_url)
    assert len(result) == 2
    assert url1 in result
    assert url2 in result


def test_TokenExtractor_extract_url_set_with_list():
    url1 = "http://may.la"
    url2 = "github.com"
    text_with_url = [f"{url1} Das ist ein Text.", f"{url2} Er enthält eine URL."]
    token_extractor = TokenExtractor("de_CMC")
    result = token_extractor.extract_url_set(text_with_url)
    assert len(result) == 2
    assert url1 in result
    assert url2 in result


def test_TokenExtractor_extract_url_set_no_url():
    text_with_url = "Das ist ein Text. Er enthält keine URLs."
    token_extractor = TokenExtractor("de_CMC")
    result = token_extractor.extract_url_set(text_with_url)
    assert len(result) == 0


def test_extract_token_class_set_symbol():
    somajo = SoMaJo("de_CMC")
    sentences = somajo.tokenize_text(["Das ist ein Satz. Das ist ein anderer Satz."])
    result = extract_token_class_set(sentences, keep_token_classes="symbol")

    assert isinstance(result, set)
    assert len(result) == 1
    assert "." in result


def test_extract_token_class_set_url():
    somajo = SoMaJo("de_CMC")
    sentences = somajo.tokenize_text(["Das ist ein Satz. Das ist ein Link: http://github.com"])
    result = extract_token_class_set(sentences, keep_token_classes="URL")

    assert isinstance(result, set)
    assert len(result) == 1
    assert "http://github.com" in result


def test_extract_token_class_set_url__url_with_dot_at_end():
    somajo = SoMaJo("de_CMC")
    sentences = somajo.tokenize_text(["Das ist ein Satz mit einem Link: http://github.com."])
    result = extract_token_class_set(sentences, keep_token_classes="URL")

    assert isinstance(result, set)
    assert len(result) == 1
    assert "http://github.com" in result


def test_detokenize():
    somajo = SoMaJo("de_CMC")
    sentences = somajo.tokenize_text(["Das ist ein Satz. Das ist ein anderer Satz."])
    result = detokenize(list(sentences)[0])

    assert isinstance(result, str)
    assert result == "Das ist ein Satz."


def test_UrlSwapper_swap_urls():
    token_extractor = TokenExtractor("de_CMC")
    url_swapper = UrlSwapper(token_extractor)
    text_with_url = "This is a text with URL: http://may.la."
    text_with_swapped_url = url_swapper.swap_urls(text_with_url)
    assert text_with_swapped_url == "This is a text with URL: https://link-1.com."


@pytest.mark.parametrize(
    "text_with_url",
    [
        "This is a text with URL: http://may.la.",
        "This is a text with Markdown URL: [Philip May](http://may.la).",
        "2 MD URL s: [Philip May](http://may.la). [other link](https://github.com/telekom/mltb2#installation)",
    ],
)
def test_UrlSwapper__is_reversible(text_with_url: str):
    token_extractor = TokenExtractor("de_CMC")
    url_swapper = UrlSwapper(token_extractor)
    text_with_reverse_swapped_url, no_reverse_swap_urls = url_swapper.reverse_swap_urls(
        url_swapper.swap_urls(text_with_url)
    )
    assert text_with_reverse_swapped_url == text_with_url
    assert len(no_reverse_swap_urls) == 0


def test_UrlSwapper__no_reverse_swap_urls():
    token_extractor = TokenExtractor("de_CMC")
    url_swapper = UrlSwapper(token_extractor)
    text_with_url = "This is a text with URL: http://may.la."
    swapped_url_text = url_swapper.swap_urls(text_with_url)
    additional_url = "http://other-url.org"
    swapped_url_text = f"{swapped_url_text} {additional_url}"
    text_with_reverse_swapped_url, no_reverse_swap_urls = url_swapper.reverse_swap_urls(swapped_url_text)
    assert len(no_reverse_swap_urls) == 1
    assert additional_url in no_reverse_swap_urls


# see https://github.com/telekom/mltb2/issues/94
def test_UrlSwapper__markdown_bug():
    token_extractor = TokenExtractor("de_CMC")
    url_swapper = UrlSwapper(token_extractor)
    text_with_url = "This is a MD link: [https://something-1.com](https://something-2.com)."
    swapped_url_text = url_swapper.swap_urls(text_with_url)
    assert "https://link-1.com" in swapped_url_text
    assert "https://link-2.com" in swapped_url_text
    assert len(url_swapper._url_map) == 2
