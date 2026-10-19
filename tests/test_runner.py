"""Tests for the convenience run_all pipeline (integration of U1 parts)."""

import pytest

from sorting_core import AccuracyCheck, AlgorithmResult, SortInput, run_all


def test_run_all_returns_three_results_and_checks():
    sort_input, results, checks = run_all(["Bob", "alice", "bob"])
    assert isinstance(sort_input, SortInput)
    assert len(results) == 3
    assert [r.algorithm for r in results] == ["bubble", "selection", "quick"]
    assert all(isinstance(r, AlgorithmResult) for r in results)
    assert len(checks) == 3
    assert all(isinstance(c, AccuracyCheck) for c in checks)


def test_run_all_same_run_id_everywhere():
    sort_input, results, checks = run_all(["bob", "apple"])
    assert all(r.run_id == sort_input.run_id for r in results)
    assert all(c.run_id == sort_input.run_id for c in checks)


def test_run_all_all_checks_pass():
    _, results, checks = run_all(["delta", "alpha", "charlie", "alpha"])
    assert all(c.passed for c in checks)
    assert results[0].sorted_strings == ["alpha", "alpha", "charlie", "delta"]


def test_run_all_matches_sorted_reference():
    sort_input, results, _ = run_all(["zeta", "Émile", "alpha", "zeta"])
    expected = sorted(sort_input.normalized_strings)
    for result in results:
        assert result.sorted_strings == expected


def test_run_all_normalizes_first():
    sort_input, _, _ = run_all(["A,B", "c"])
    assert sort_input.normalized_strings == ["a", "b", "c"]


def test_run_all_propagates_type_error():
    with pytest.raises(TypeError):
        run_all("not-a-list")
