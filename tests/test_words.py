"""Tests for WordListProvider (BR-WLP-1, SD-4)."""

import pytest

from sorting_core import WordListProvider


@pytest.fixture
def provider() -> WordListProvider:
    return WordListProvider()


def test_words_non_empty(provider: WordListProvider):
    assert len(provider.get_words()) >= 1


def test_words_all_strings(provider: WordListProvider):
    assert all(isinstance(word, str) and word for word in provider.get_words())


def test_words_fixed_across_calls(provider: WordListProvider):
    # BR-WLP-1: the list does not change between accesses.
    assert provider.get_words() == provider.get_words()


def test_words_immutable_tuple(provider: WordListProvider):
    # No modification, insertion, or deletion at runtime.
    words = provider.get_words()
    assert isinstance(words, tuple)
    with pytest.raises(AttributeError):
        words.append("hack")  # type: ignore[attr-defined]


def test_version_non_empty(provider: WordListProvider):
    assert isinstance(provider.get_version(), str)
    assert provider.get_version()
