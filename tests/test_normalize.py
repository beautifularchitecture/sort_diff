"""Tests for InputProcessor.normalize (BR-INP-1, BR-INP-2, BR-INP-3, SD-2)."""

import re

import pytest

from sorting_core import InputProcessor, SortInput


@pytest.fixture
def processor() -> InputProcessor:
    return InputProcessor()


def test_full_normalization_example(processor: InputProcessor):
    # BR-INP-1 example. Note: the 'cäfe' entry is expected UNCHANGED apart
    # from ASCII lowercasing (the rules.md table renders it as 'café',
    # which contradicts its own note and entities.md; see code summary).
    result = processor.normalize(["Alice", "bob", "", "Alice", "cäfe"])
    assert result.normalized_strings == ["alice", "bob", "alice", "cäfe"]


def test_split_on_comma_and_newline(processor: InputProcessor):
    # BR-INP-1 formal definition splits on '\n' and ',' only — NOT on
    # spaces. (The rules.md example table renders "new line" as two tokens,
    # contradicting both its own note and the formal definition; see code
    # summary. Spaces inside an entry are preserved.)
    result = processor.normalize(["HELLO,world\nnew line"])
    assert result.normalized_strings == ["hello", "world", "new line"]


def test_split_on_newline_and_comma_separately(processor: InputProcessor):
    result = processor.normalize(["a\nb,c"])
    assert result.normalized_strings == ["a", "b", "c"]


def test_empty_and_whitespace_tokens_dropped(processor: InputProcessor):
    result = processor.normalize(["", "  ", "hello"])
    assert result.normalized_strings == ["hello"]


def test_duplicates_preserved(processor: InputProcessor):
    result = processor.normalize(["a", "a"])
    assert result.normalized_strings == ["a", "a"]


def test_ascii_capitals_only_lowercased(processor: InputProcessor):
    result = processor.normalize(["ÉCOLE", "ABC-XYZ"])
    assert result.normalized_strings == ["École", "abc-xyz"]


def test_trim_leading_and_trailing_whitespace(processor: InputProcessor):
    result = processor.normalize(["  padded\t"])
    assert result.normalized_strings == ["padded"]


def test_empty_input_yields_empty_normalized(processor: InputProcessor):
    result = processor.normalize([])
    assert result.normalized_strings == []
    assert result.raw_entries == []


def test_run_id_generated_unique_and_nonempty(processor: InputProcessor):
    first = processor.normalize(["a"])
    second = processor.normalize(["a"])
    assert isinstance(first.run_id, str)
    assert first.run_id
    assert first.run_id != second.run_id
    assert re.fullmatch(r"[0-9a-f-]{36}", first.run_id)


def test_raw_entries_preserved_as_given(processor: InputProcessor):
    raw = ["Bob,", " X ", ""]
    result = processor.normalize(raw)
    assert result.raw_entries == raw
    # mutating the caller's list afterwards must not affect the SortInput
    raw.append("later")
    assert result.raw_entries == ["Bob,", " X ", ""]


def test_returns_sort_input(processor: InputProcessor):
    assert isinstance(processor.normalize(["x"]), SortInput)


@pytest.mark.parametrize("bad", ["not-a-list", ("a", "b"), 42, None, {"a": 1}])
def test_non_list_raises_type_error(processor: InputProcessor, bad):
    with pytest.raises(TypeError):
        processor.normalize(bad)


@pytest.mark.parametrize("bad", [[1], [None], ["ok", 2], [b"bytes"]])
def test_non_string_item_raises_type_error(processor: InputProcessor, bad):
    with pytest.raises(TypeError):
        processor.normalize(bad)
