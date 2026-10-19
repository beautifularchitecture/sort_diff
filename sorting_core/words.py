"""Bundled word list (BR-WLP-1).

The list is fixed in code, non-empty, and immutable: it is exposed as a
tuple, so there is no way to modify, insert, or delete entries at
runtime. No file I/O, no network access, no dynamic updates (SD-4).
"""

from __future__ import annotations

_WORDS: tuple[str, ...] = (
    "apple",
    "banana",
    "cherry",
    "date",
    "elephant",
    "fig",
    "grape",
    "house",
)

_LIST_VERSION = "v1.0"


class WordListProvider:
    """Supplies the fixed, bundled word list for the UI picker."""

    def get_words(self) -> tuple[str, ...]:
        """Return the immutable word list (BR-WLP-1)."""
        return _WORDS

    def get_version(self) -> str:
        """Return the list version identifier."""
        return _LIST_VERSION


__all__ = ["WordListProvider"]
