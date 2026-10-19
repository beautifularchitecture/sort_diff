"""Tests for AccuracyChecker.check (BR-AC-1, BR-AC-2, BR-INT-1, SD-2)."""

import pytest

from sorting_core import (
    AccuracyChecker,
    AlgorithmResult,
    InputProcessor,
    SortingEngine,
    SortInput,
)


@pytest.fixture
def checker() -> AccuracyChecker:
    return AccuracyChecker()


@pytest.fixture
def sort_input() -> SortInput:
    return InputProcessor().normalize(["charlie", "apple", "bob"])


def make_result(
    sort_input: SortInput,
    sorted_strings: list[str],
    algorithm: str = "bubble",
) -> AlgorithmResult:
    return AlgorithmResult(
        run_id=sort_input.run_id,
        algorithm=algorithm,
        sorted_strings=sorted_strings,
        comparisons=0,
        swaps=0,
    )


def test_exact_match_passes(checker: AccuracyChecker, sort_input: SortInput):
    result = make_result(sort_input, ["apple", "bob", "charlie"])
    check = checker.check(result, sort_input)
    assert check.passed is True
    assert check.run_id == sort_input.run_id
    assert check.algorithm == "bubble"


def test_order_mismatch_fails(checker: AccuracyChecker, sort_input: SortInput):
    # BR-AC-1: no partial credit — one mismatch means passed is false.
    result = make_result(sort_input, ["apple", "charlie", "bob"])
    assert checker.check(result, sort_input).passed is False


def test_duplicate_order_mismatch_fails(checker: AccuracyChecker):
    # Stability matters: ['a','a','b'] vs ['a','b','a'] is a failure.
    sort_input = InputProcessor().normalize(["b", "a", "a"])
    result = make_result(sort_input, ["a", "b", "a"])
    assert checker.check(result, sort_input).passed is False
    stable = make_result(sort_input, ["a", "a", "b"])
    assert checker.check(stable, sort_input).passed is True


def test_length_mismatch_fails(checker: AccuracyChecker, sort_input: SortInput):
    result = make_result(sort_input, ["apple", "bob"])
    assert checker.check(result, sort_input).passed is False


def test_empty_input_passes_when_empty_result(checker: AccuracyChecker):
    # BR-EDGE-1: [] == sorted([]) -> passed true.
    sort_input = InputProcessor().normalize([])
    result = make_result(sort_input, [])
    assert checker.check(result, sort_input).passed is True


def test_run_id_mismatch_raises_value_error(
    checker: AccuracyChecker, sort_input: SortInput
):
    # BR-INT-1: mismatch is a caller defect -> ValueError.
    other = InputProcessor().normalize(["charlie", "apple", "bob"])
    result = make_result(other, ["apple", "bob", "charlie"])
    with pytest.raises(ValueError):
        checker.check(result, sort_input)


def test_checks_are_independent(checker: AccuracyChecker):
    # BR-AC-2: one failing algorithm does not cascade to the others.
    sort_input = InputProcessor().normalize(["charlie", "apple", "bob"])
    results = SortingEngine().run_all(sort_input)
    good = [checker.check(r, sort_input) for r in results]
    assert [c.passed for c in good] == [True, True, True]

    bad_bubble = AlgorithmResult(
        run_id=sort_input.run_id,
        algorithm="bubble",
        sorted_strings=["charlie", "apple", "bob"],
        comparisons=0,
        swaps=0,
    )
    bad_check = checker.check(bad_bubble, sort_input)
    assert bad_check.passed is False
    # re-checking the good results still passes
    assert [checker.check(r, sort_input).passed for r in results] == [
        True,
        True,
        True,
    ]


def test_engine_results_all_pass_accuracy(
    checker: AccuracyChecker, sort_input: SortInput
):
    results = SortingEngine().run_all(sort_input)
    checks = [checker.check(r, sort_input) for r in results]
    assert all(c.passed for c in checks)


@pytest.mark.parametrize("bad_result", ["x", None, 1])
def test_non_algorithm_result_raises_type_error(
    checker: AccuracyChecker, sort_input: SortInput, bad_result
):
    with pytest.raises(TypeError):
        checker.check(bad_result, sort_input)


@pytest.mark.parametrize("bad_input", ["x", None, 1])
def test_non_sort_input_raises_type_error(
    checker: AccuracyChecker, sort_input: SortInput, bad_input
):
    result = make_result(sort_input, ["apple", "bob", "charlie"])
    with pytest.raises(TypeError):
        checker.check(result, bad_input)
