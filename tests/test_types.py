"""Tests for the sorting_core data model (entities.md)."""

from dataclasses import FrozenInstanceError

import pytest

from sorting_core import AccuracyCheck, AlgorithmResult, Counter, SortInput


def test_sort_input_fields():
    si = SortInput(run_id="r1", raw_entries=["A"], normalized_strings=["a"])
    assert si.run_id == "r1"
    assert si.raw_entries == ["A"]
    assert si.normalized_strings == ["a"]


def test_sort_input_is_frozen():
    si = SortInput(run_id="r1", raw_entries=[], normalized_strings=[])
    with pytest.raises(FrozenInstanceError):
        si.run_id = "r2"  # type: ignore[misc]


def test_algorithm_result_fields_and_frozen():
    r = AlgorithmResult(
        run_id="r1",
        algorithm="bubble",
        sorted_strings=["a"],
        comparisons=0,
        swaps=0,
    )
    assert r.comparisons == 0
    assert r.swaps == 0
    with pytest.raises(FrozenInstanceError):
        r.comparisons = 1  # type: ignore[misc]


def test_accuracy_check_fields_and_frozen():
    c = AccuracyCheck(run_id="r1", algorithm="quick", passed=True)
    assert c.passed is True
    with pytest.raises(FrozenInstanceError):
        c.passed = False  # type: ignore[misc]


def test_counter_defaults_and_reset():
    counter = Counter()
    assert counter.comparisons == 0
    assert counter.swaps == 0
    counter.comparisons = 7
    counter.swaps = 3
    counter.reset()
    assert counter.comparisons == 0
    assert counter.swaps == 0
