"""Convenience pipeline: normalize -> run all algorithms -> verify.

Wires the three components together in the order U2 (playground-ui)
drives them on each Sort button press, so callers get one call instead
of three. Boundary errors (``TypeError``, ``ValueError``) propagate to
the caller unchanged — nothing is swallowed.
"""

from __future__ import annotations

from .checker import AccuracyChecker
from .engine import SortingEngine
from .normalize import InputProcessor
from .types import AccuracyCheck, AlgorithmResult, SortInput


def run_all(
    raw_entries: list[str],
) -> tuple[SortInput, list[AlgorithmResult], list[AccuracyCheck]]:
    """Run the full pipeline on ``raw_entries``.

    Returns the ``SortInput``, the three ``AlgorithmResult`` objects
    (bubble, selection, quick), and one independent ``AccuracyCheck``
    per algorithm.
    """
    sort_input = InputProcessor().normalize(raw_entries)
    results = SortingEngine().run_all(sort_input)
    checker = AccuracyChecker()
    checks = [checker.check(result, sort_input) for result in results]
    return sort_input, results, checks


__all__ = ["run_all"]
