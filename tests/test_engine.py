"""Tests for SortingEngine.run_all (BR-SE-4, BR-INT-1, BR-INT-2, BR-EDGE-*)."""

import pytest

from sorting_core import AlgorithmResult, InputProcessor, SortingEngine, SortInput


@pytest.fixture
def engine() -> SortingEngine:
    return SortingEngine()


@pytest.fixture
def sort_input() -> SortInput:
    return InputProcessor().normalize(["Charlie", "apple", "bob"])


def test_returns_exactly_three_results_in_order(
    engine: SortingEngine, sort_input: SortInput
):
    # BR-SE-4: bubble (0), selection (1), quick (2); no other algorithms.
    results = engine.run_all(sort_input)
    assert len(results) == 3
    assert [r.algorithm for r in results] == ["bubble", "selection", "quick"]
    assert all(isinstance(r, AlgorithmResult) for r in results)


def test_all_results_share_run_id_and_input(
    engine: SortingEngine, sort_input: SortInput
):
    # BR-INT-1 / BR-INT-2: same run_id and same normalized input.
    results = engine.run_all(sort_input)
    assert all(r.run_id == sort_input.run_id for r in results)
    expected = sorted(sort_input.normalized_strings)
    for result in results:
        assert result.sorted_strings == expected


def test_counts_are_per_algorithm_not_accumulated(
    engine: SortingEngine, sort_input: SortInput
):
    # One Counter is shared per run but reset between algorithms, so the
    # bubble result must not include selection/quick counts (Q3).
    results = engine.run_all(sort_input)
    bubble, selection, quick = results
    assert bubble.comparisons == 3
    assert selection.comparisons == 3
    assert quick.comparisons == 2


def test_input_normalized_strings_not_mutated(
    engine: SortingEngine, sort_input: SortInput
):
    before = list(sort_input.normalized_strings)
    engine.run_all(sort_input)
    assert sort_input.normalized_strings == before


def test_empty_input_edge_case(engine: SortingEngine):
    sort_input = InputProcessor().normalize([])
    results = engine.run_all(sort_input)
    assert len(results) == 3
    for result in results:
        assert result.sorted_strings == []
        assert result.comparisons == 0
        assert result.swaps == 0


def test_single_element_edge_case(engine: SortingEngine):
    sort_input = InputProcessor().normalize(["hello"])
    results = engine.run_all(sort_input)
    for result in results:
        assert result.sorted_strings == ["hello"]
        assert result.comparisons == 0
        assert result.swaps == 0


def test_all_identical_edge_case(engine: SortingEngine):
    sort_input = InputProcessor().normalize(["apple", "apple", "apple"])
    results = engine.run_all(sort_input)
    for result in results:
        assert result.sorted_strings == ["apple", "apple", "apple"]
        assert result.swaps == 0


@pytest.mark.parametrize("bad", ["not-a-sort-input", None, 42, ["a"]])
def test_non_sort_input_raises_type_error(engine: SortingEngine, bad):
    # SD-2: boundary validation fails fast with TypeError.
    with pytest.raises(TypeError):
        engine.run_all(bad)
