"""AccuracyChecker: verifies one AlgorithmResult against Python's sorted().

BR-AC-1: ``passed`` is true only when ``sorted_strings`` equals
``sorted(normalized_strings)`` element by element (exact order match,
duplicates included). BR-AC-2: each algorithm is checked independently.
BR-INT-1: a ``run_id`` mismatch between result and input is a caller
defect and raises ``ValueError``.
"""

from __future__ import annotations

from .types import AccuracyCheck, AlgorithmResult, SortInput


class AccuracyChecker:
    """Compares one ``AlgorithmResult`` to the sorted() reference."""

    def check(
        self, algorithm_result: AlgorithmResult, sort_input: SortInput
    ) -> AccuracyCheck:
        """Return an ``AccuracyCheck`` for one algorithm (BR-AC-1).

        Raises ``TypeError`` for wrong argument types (SD-2) and
        ``ValueError`` when the result and input ``run_id`` values differ
        (BR-INT-1).
        """
        if not isinstance(algorithm_result, AlgorithmResult):
            raise TypeError(
                "algorithm_result must be an AlgorithmResult instance, "
                f"got {type(algorithm_result).__name__}"
            )
        if not isinstance(sort_input, SortInput):
            raise TypeError(
                "sort_input must be a SortInput instance, "
                f"got {type(sort_input).__name__}"
            )
        if algorithm_result.run_id != sort_input.run_id:
            raise ValueError(
                "run_id mismatch: AlgorithmResult.run_id "
                f"({algorithm_result.run_id!r}) does not match "
                f"SortInput.run_id ({sort_input.run_id!r})"
            )

        reference = sorted(sort_input.normalized_strings)
        passed = algorithm_result.sorted_strings == reference
        return AccuracyCheck(
            run_id=sort_input.run_id,
            algorithm=algorithm_result.algorithm,
            passed=passed,
        )


__all__ = ["AccuracyChecker"]
