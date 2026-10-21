"""String Sorter Playground — Streamlit single-page app (playground-ui, U2).

Presentation and orchestration only (ADR-004): collects typed entries and
picked words, delegates normalization, sorting, counting, and verification
to sorting-core (U1), and renders the input echo plus three result columns.

Local run: ``streamlit run app.py`` (Contract 2). No custom CSS, no
``unsafe_allow_html``, no I/O, no network, no identity (SD-2, SD-4, SD-5).
"""

from __future__ import annotations

import re

import streamlit as st

from sorting_core import (
    AccuracyCheck,
    AccuracyChecker,
    AlgorithmResult,
    InputProcessor,
    SortingEngine,
    WordListProvider,
)

# Bundled word list (FR1.5, AC1.2.3): fixed, read-only (a tuple), no I/O.
WORD_LIST: tuple[str, ...] = WordListProvider().get_words()

# SD-3 / NFR3.6: refuse to sort above this many de-duplicated strings.
MAX_SORT_STRINGS = 100

# FR6.1: exact empty-input message.
EMPTY_INPUT_MESSAGE = "Enter or select at least one string"

# SD-3 snippet message: states the limit when it is exceeded.
LIMIT_MESSAGE = "Input exceeds the 100-string limit."

_EMPTY_STATE_HINT = (
    "Enter or pick strings above, then press Sort to compare "
    "bubble, selection, and quick sort."
)

_ALGORITHM_LABELS = {
    "bubble": "bubble sort",
    "selection": "selection sort",
    "quick": "quick sort",
}

# Same split rule as sorting_core's normalize (newline and comma); used
# only to tokenize the text area for de-duplication (PD-4). Authoritative
# tokenization stays in U1's normalize.
_SPLIT_PATTERN = re.compile(r"[,\n]")


def split_typed_entries(typed_text: str) -> list[str]:
    """Split raw text-area content the way ``normalize`` will split it.

    Split on newlines and commas, trim surrounding whitespace, and drop
    empty tokens. This is de-duplication tokenization only; the strings
    returned here are still passed to U1's ``normalize`` untouched.
    """
    return [
        token.strip() for token in _SPLIT_PATTERN.split(typed_text) if token.strip()
    ]


def build_shared_list(typed_text: str, picked_words: list[str]) -> list[str]:
    """Combine typed entries and picked words, de-duplicating (Q2 Option C).

    Typed entries come first, then picked words; a string seen twice is
    kept once, preserving first-seen order (FR1.4, AC1.1.1, AC1.2.2).
    Built once per rerun, before the cap check (PD-4).
    """
    seen: set[str] = set()
    shared: list[str] = []
    for token in split_typed_entries(typed_text) + list(picked_words):
        if token not in seen:
            seen.add(token)
            shared.append(token)
    return shared


def render_results(
    shared_list: list[str],
    results: list[AlgorithmResult],
    checks: list[AccuracyCheck],
) -> None:
    """Render the input echo and three result columns (AC3.1.1–AC3.1.3).

    One column per algorithm in [bubble, selection, quick] order (PD-3).
    All user strings reach the screen through Streamlit's default text
    and markdown APIs as plain strings — never ``unsafe_allow_html``
    (SD-2). Counts are rendered as full integers (AC3.2.5).
    """
    st.markdown("**Input**")
    st.text(", ".join(shared_list))

    columns = st.columns(3)
    for column, result, check in zip(columns, results, checks, strict=True):
        with column:
            st.markdown(f"**{_ALGORITHM_LABELS[result.algorithm]}**")
            st.text("\n".join(result.sorted_strings))
            st.markdown(f"Comparisons: {result.comparisons}")
            st.markdown(f"Swaps: {result.swaps}")
            st.markdown(f"Accuracy: {'pass' if check.passed else 'fail'}")


def main() -> None:
    """Render the playground screen and wire widgets to sorting-core."""
    st.title("String Sorter Playground")

    typed_text = st.text_area("Strings to sort", key="strings_text_area")
    picked_words = st.multiselect(
        "Pick from the bundled word list",
        WORD_LIST,
        key="word_picks",
    )
    sort_pressed = st.button("Sort", key="sort_button")

    # The empty-state hint shows only before the first Sort press (US4.1).
    # The flag records that a press happened; it is not result state
    # (PD-2 forbids storing results, not a pressed-once marker).
    if sort_pressed:
        st.session_state.sort_attempted = True

    if not st.session_state.get("sort_attempted", False):
        st.info(_EMPTY_STATE_HINT)
        return

    shared_list = build_shared_list(typed_text, picked_words)

    if not shared_list:
        st.warning(EMPTY_INPUT_MESSAGE)
        return

    if len(shared_list) > MAX_SORT_STRINGS:
        st.error(LIMIT_MESSAGE)
        return

    # SD-6 / NFR3.1: no try/except here — TypeError, ValueError, and
    # RecursionError from U1 propagate so Streamlit shows the traceback.
    # PD-1 / PD-2: no caching and no stored results; the pipeline runs
    # fresh from the current widget values on every rerun.
    sort_input = InputProcessor().normalize(shared_list)
    results = SortingEngine().run_all(sort_input)
    checker = AccuracyChecker()
    checks = [checker.check(result, sort_input) for result in results]
    render_results(shared_list, results, checks)


if __name__ == "__main__":
    main()
