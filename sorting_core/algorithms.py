"""The three sorting algorithms (BR-SE-1 .. BR-SE-5).

Exactly three algorithms are implemented: bubble, selection, and quick
(BR-SE-4). All of them:

- take the shared :class:`~sorting_core.types.Counter` and increment
  ``comparisons`` for every pairwise comparison and ``swaps`` per their
  own definition (NFR design Q3, option A);
- work on ``(value, original_index)`` pairs so equal strings keep their
  input order and the output equals Python's ``sorted()`` (BR-SE-5);
- never mutate the caller's list (each builds its own pair list).

Comparison counting (BR-SE-1): one increment per pairwise ``<``/``>``
operator application, regardless of outcome. Tuple comparisons count once
at the algorithm level even when Python falls through to the index.

Swap counting (BR-SE-2): a swap counts when two distinct positions are
exchanged (self-swaps are skipped); selection sort's stable shift-based
variant counts each shifted write, as noted in the functional spec.
"""

from __future__ import annotations

from .types import Counter


def _to_pairs(strings: list[str]) -> list[tuple[str, int]]:
    return [(s, i) for i, s in enumerate(strings)]


def _to_strings(pairs: list[tuple[str, int]]) -> list[str]:
    return [value for value, _ in pairs]


def bubble_sort(strings: list[str], counter: Counter) -> list[str]:
    """Bubble sort (BR-SE-1, BR-SE-2, BR-SE-3).

    Adjacent pairs are compared and swapped when out of tuple order; a
    pass with no swaps terminates early. Comparisons: up to n(n-1)/2.
    Swaps: one per adjacent exchange (equals are never swapped).
    """
    items = _to_pairs(strings)
    n = len(items)
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            counter.comparisons += 1
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
                counter.swaps += 1
                swapped = True
        if not swapped:
            break
    return _to_strings(items)


def selection_sort(strings: list[str], counter: Counter) -> list[str]:
    """Selection sort (BR-SE-1, BR-SE-2, BR-SE-3).

    Finds the minimum ``(value, index)`` pair in each pass and shifts it
    into place. The shift-based placement is the stable variant from the
    functional spec: a plain swap of non-adjacent positions would reorder
    equal strings and break BR-SE-5/BR-AC-1. ``swaps`` therefore counts
    shifted writes (one per moved element). Comparisons: exactly
    n(n-1)/2.
    """
    items = _to_pairs(strings)
    n = len(items)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            counter.comparisons += 1
            if items[j] < items[min_idx]:
                min_idx = j
        if min_idx != i:
            min_item = items[min_idx]
            for k in range(min_idx, i, -1):
                items[k] = items[k - 1]
                counter.swaps += 1
            items[i] = min_item
    return _to_strings(items)


def quick_sort(strings: list[str], counter: Counter) -> list[str]:
    """Recursive quick sort with Lomuto partition (Q2, option A).

    The pivot is the last pair of the segment; elements strictly smaller
    (by ``(value, index)``) move left, which also keeps equal strings in
    input order (BR-SE-5). Self-swaps are not counted.
    """
    items = _to_pairs(strings)
    _quicksort(items, 0, len(items) - 1, counter)
    return _to_strings(items)


def _quicksort(
    items: list[tuple[str, int]], low: int, high: int, counter: Counter
) -> None:
    if low < high:
        pivot_idx = _partition(items, low, high, counter)
        _quicksort(items, low, pivot_idx - 1, counter)
        _quicksort(items, pivot_idx + 1, high, counter)


def _partition(
    items: list[tuple[str, int]], low: int, high: int, counter: Counter
) -> int:
    pivot = items[high]
    boundary = low - 1
    for j in range(low, high):
        counter.comparisons += 1
        if items[j] < pivot:
            boundary += 1
            if boundary != j:
                items[boundary], items[j] = items[j], items[boundary]
                counter.swaps += 1
    if boundary + 1 != high:
        items[boundary + 1], items[high] = items[high], items[boundary + 1]
        counter.swaps += 1
    return boundary + 1


__all__ = ["bubble_sort", "quick_sort", "selection_sort"]
