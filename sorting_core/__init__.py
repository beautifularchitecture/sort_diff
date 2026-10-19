"""sorting_core — pure in-process sorting domain for the string sorter.

Public API re-exports. No I/O, no markup, no network, no auth
(SD-1, SD-3, SD-4, SD-5).
"""

from .algorithms import bubble_sort, quick_sort, selection_sort
from .checker import AccuracyChecker
from .engine import SortingEngine
from .normalize import InputProcessor
from .runner import run_all
from .types import AccuracyCheck, AlgorithmResult, Counter, SortInput
from .words import WordListProvider

__all__ = [
    "AccuracyCheck",
    "AccuracyChecker",
    "AlgorithmResult",
    "Counter",
    "InputProcessor",
    "SortInput",
    "SortingEngine",
    "WordListProvider",
    "bubble_sort",
    "quick_sort",
    "run_all",
    "selection_sort",
]
