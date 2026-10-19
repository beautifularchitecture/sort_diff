"""Input normalization (BR-INP-1, BR-INP-2, BR-INP-3).

Boundary validation per SD-2: a non-list or a non-string item raises
``TypeError`` before any processing happens.
"""

from __future__ import annotations

import re
import uuid

from .types import SortInput

_SPLIT_PATTERN = re.compile(r"[,\n]")


def _lowercase_ascii(token: str) -> str:
    """Lowercase ASCII capitals A-Z only; every other char passes through.

    BR-INP-1 step 4: A-Z -> a-z; non-ASCII, digits, lowercase, and
    punctuation are unchanged. ``str.lower()`` is deliberately NOT used
    because it would also lowercase non-ASCII letters such as 'Ä'.
    """
    return "".join(chr(ord(ch) + 32) if "A" <= ch <= "Z" else ch for ch in token)


class InputProcessor:
    """Turns raw UI entries into a normalized :class:`SortInput`."""

    def normalize(self, raw_entries: list[str]) -> SortInput:
        """Normalize ``raw_entries`` into a ``SortInput`` (BR-INP-1).

        Steps per entry: split on newlines and commas, trim, drop empty
        tokens, lowercase ASCII capitals, preserve duplicates. A fresh
        ``run_id`` (UUID4) is generated per call (BR-INP-3).
        """
        if not isinstance(raw_entries, list) or not all(
            isinstance(entry, str) for entry in raw_entries
        ):
            raise TypeError(
                "raw_entries must be a list of strings, "
                f"got {type(raw_entries).__name__}"
            )

        normalized_strings: list[str] = []
        for entry in raw_entries:
            for token in _SPLIT_PATTERN.split(entry):
                trimmed = token.strip()
                if not trimmed:
                    continue  # BR-INP-2: drop empty-after-trim tokens
                normalized_strings.append(_lowercase_ascii(trimmed))

        return SortInput(
            run_id=str(uuid.uuid4()),
            raw_entries=list(raw_entries),
            normalized_strings=normalized_strings,
        )


__all__ = ["InputProcessor"]
