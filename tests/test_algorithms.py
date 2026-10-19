"""Tests for the three sorting algorithms (BR-SE-1 .. BR-SE-5, BR-EDGE-*).

Counting expectations follow the worked examples in rules.md
(BR-SE-1/BR-SE-2) and the functional spec. Two documented deviations:

- BR-SE-1's bubble example claims 5 comparisons for a 3-element input.
  No standard bubble variant can produce that for n=3 (the spec's
  pseudocode always performs n(n-1)/2 = 3 comparisons). The (5
  comparisons, 3 swaps) totals are reproduced with a 4-element input
  carrying the three distinct values a<b<c plus a duplicate, which also
  matches BR-SE-2's "3 swaps" figure.
- BR-SE-2's quick example claims 1 swap for input [3,1,2]. Standard
  Lomuto on that arrangement performs 2 genuine swaps; input [1,3,2]
  yields exactly 1 swap, so that arrangement is used for the swap
  assertion.
"""

import random

import pytest

from sorting_core import Counter
from sorting_core.algorithms import bubble_sort, quick_sort, selection_sort

ALGORITHMS = {
    "bubble": bubble_sort,
    "selection": selection_sort,
    "quick": quick_sort,
}


def run(algorithm: str, strings: list[str]) -> tuple[list[str], Counter]:
    counter = Counter()
    output = ALGORITHMS[algorithm](strings, counter)
    return output, counter


# --- Counting worked examples (BR-SE-1, BR-SE-2) ---------------------------


def test_bubble_counting_worked_example():
    # Totals from BR-SE-1 (5 comparisons) and BR-SE-2 (3 swaps).
    output, counter = run("bubble", ["c", "a", "b", "b"])
    assert counter.comparisons == 5
    assert counter.swaps == 3
    assert output == ["a", "b", "b", "c"]


def test_bubble_three_element_example():
    # Functional spec Workflow 2: ['charlie', 'apple', 'bob'] -> 3, 2.
    output, counter = run("bubble", ["charlie", "apple", "bob"])
    assert counter.comparisons == 3
    assert counter.swaps == 2
    assert output == ["apple", "bob", "charlie"]


def test_selection_counting_worked_example():
    # BR-SE-1 selection example (3 comparisons) and BR-SE-2 (2 swaps).
    output, counter = run("selection", ["c", "a", "b"])
    assert counter.comparisons == 3
    assert counter.swaps == 2
    assert output == ["a", "b", "c"]


def test_quick_counting_worked_example():
    # BR-SE-1 quick example (2 comparisons with pivot = last element)
    # and BR-SE-2 (1 swap) on the [1,3,2] arrangement.
    output, counter = run("quick", ["a", "c", "b"])
    assert counter.comparisons == 2
    assert counter.swaps == 1
    assert output == ["a", "b", "c"]


def test_quick_three_element_swap_heavier_example():
    # Functional spec Workflow 2: Lomuto on ['charlie', 'apple', 'bob']
    # (pivot 'bob') performs 2 comparisons and 2 swaps.
    output, counter = run("quick", ["charlie", "apple", "bob"])
    assert counter.comparisons == 2
    assert counter.swaps == 2
    assert output == ["apple", "bob", "charlie"]


# --- Edge cases (BR-EDGE-1, BR-EDGE-2, BR-EDGE-3, FR4.5) ------------------


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_empty_input_zero_counts(algorithm: str):
    output, counter = run(algorithm, [])
    assert output == []
    assert counter.comparisons == 0
    assert counter.swaps == 0


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_single_element_zero_counts(algorithm: str):
    output, counter = run(algorithm, ["hello"])
    assert output == ["hello"]
    assert counter.comparisons == 0
    assert counter.swaps == 0


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_all_identical_zero_swaps_and_order_preserved(algorithm: str):
    # BR-EDGE-3: comparisons >= 0, swaps == 0, input order preserved.
    # (Bubble performs 2 comparisons here because it exits after the
    # first clean pass; selection performs 3, matching rules.md's
    # selection example; quick performs 3.)
    output, counter = run(algorithm, ["apple", "apple", "apple"])
    assert output == ["apple", "apple", "apple"]
    assert counter.swaps == 0
    assert counter.comparisons >= 0


def test_all_identical_comparison_counts():
    _, bubble = run("bubble", ["apple"] * 3)
    _, selection = run("selection", ["apple"] * 3)
    _, quick = run("quick", ["apple"] * 3)
    assert bubble.comparisons == 2
    assert selection.comparisons == 3  # matches rules.md example
    assert quick.comparisons == 3


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_two_element_minimal_sort(algorithm: str):
    # Functional spec Edge Case 4: one comparison, one swap.
    output, counter = run(algorithm, ["bob", "apple"])
    assert output == ["apple", "bob"]
    assert counter.comparisons == 1
    assert counter.swaps == 1


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_already_sorted_zero_swaps(algorithm: str):
    # BR-SE-2: swaps == 0 for already-sorted input.
    output, counter = run(algorithm, ["a", "b", "c"])
    assert output == ["a", "b", "c"]
    assert counter.swaps == 0
    assert counter.comparisons > 0


# --- Lexicographic order and stability (BR-SE-3, BR-SE-5) -----------------


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_unicode_lexicographic_order(algorithm: str):
    # BR-SE-3 examples: 'A' (65) < 'a' (97) < 'b' (98);
    # 'cafe' < 'café' ('ä' = U+00E4).
    output, _ = run(algorithm, ["b", "A", "a"])
    assert output == ["A", "a", "b"]
    output, _ = run(algorithm, ["café", "cafe", "bag"])
    assert output == ["bag", "cafe", "café"]


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_duplicates_preserve_input_order(algorithm: str):
    # BR-SE-5: output must equal sorted() exactly, duplicates included.
    strings = ["bob", "alice", "bob", "alice"]
    output, _ = run(algorithm, strings)
    assert output == ["alice", "alice", "bob", "bob"]
    assert output == sorted(strings)


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_matches_python_sorted_on_larger_input(algorithm: str):
    rng = random.Random(42)
    pool = ["alpha", "beta", "gamma", "delta", "épsi", "zeta", "alpha"]
    strings = [rng.choice(pool) for _ in range(40)]
    output, _ = run(algorithm, strings)
    assert output == sorted(strings)


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_input_list_not_mutated(algorithm: str):
    strings = ["c", "a", "b"]
    run(algorithm, strings)
    assert strings == ["c", "a", "b"]


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_counts_land_in_shared_counter(algorithm: str):
    # Q3: the counter object is passed in and mutated by the algorithm.
    counter = Counter()
    output = ALGORITHMS[algorithm](["c", "a", "b"], counter)
    assert output == ["a", "b", "c"]
    assert counter.comparisons > 0
    assert counter.swaps > 0
