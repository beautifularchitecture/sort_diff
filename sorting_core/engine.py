"""SortingEngine: runs the three algorithms on one SortInput.

Exactly three results, in order bubble, selection, quick (BR-SE-4), all
built from the same ``normalized_strings`` with no per-algorithm
preprocessing (BR-INT-2). One shared :class:`Counter` is created per
``run_all`` call and passed into each algorithm, reset between algorithms
so every result carries only its own counts (NFR design Q3, option A).
"""

from __future__ import annotations

from .algorithms import bubble_sort, quick_sort, selection_sort
from .types import AlgorithmResult, Counter, SortInput

_ALGORITHMS = (
    ("bubble", bubble_sort),
    ("selection", selection_sort),
    ("quick", quick_sort),
)


class SortingEngine:
    """Runs bubble, selection, and quick sort on one ``SortInput``."""

    def run_all(self, sort_input: SortInput) -> list[AlgorithmResult]:
        """Return three ``AlgorithmResult`` objects (BR-SE-4).

        Raises ``TypeError`` if ``sort_input`` is not a ``SortInput``
        (SD-2). The input's ``normalized_strings`` is never mutated.
        """
        if not isinstance(sort_input, SortInput):
            raise TypeError(
                "sort_input must be a SortInput instance, "
                f"got {type(sort_input).__name__}"
            )

        counter = Counter()
        results: list[AlgorithmResult] = []
        for name, algorithm in _ALGORITHMS:
            counter.reset()
            sorted_strings = algorithm(sort_input.normalized_strings, counter)
            results.append(
                AlgorithmResult(
                    run_id=sort_input.run_id,
                    algorithm=name,
                    sorted_strings=sorted_strings,
                    comparisons=counter.comparisons,
                    swaps=counter.swaps,
                )
            )
        return results


__all__ = ["SortingEngine"]
