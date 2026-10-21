"""UI wiring tests for the Streamlit playground (playground-ui, U2).

Driven through ``streamlit.testing.v1.AppTest`` so widget calls execute
and ``--cov=app`` measures real lines (NFR4.2). Expected orders and
counts come from U1's ``sorting_core``; the UI only displays them.
"""

import ast
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

import sorting_core
from sorting_core import run_all

REPO_ROOT = Path(__file__).resolve().parents[2]
APP_PATH = REPO_ROOT / "app.py"

EMPTY_INPUT_MESSAGE = "Enter or select at least one string"
LIMIT_MESSAGE = "Input exceeds the 100-string limit."


def _app_test() -> AppTest:
    """Build a fresh, already-run AppTest instance for the entry script."""
    at = AppTest.from_file(str(APP_PATH), default_timeout=30)
    at.run()
    return at


def _markdown_values(at: AppTest) -> list[str]:
    return [element.value for element in at.markdown]


def _text_values(at: AppTest) -> list[str]:
    return [element.value for element in at.text]


def test_happy_path_renders_three_columns_with_pass_accuracy() -> None:
    """Typing three strings and pressing Sort renders all three results."""
    at = _app_test()
    at.text_area[0].set_value("banana, apple, cherry")
    at.button[0].click()
    at.run()

    assert not at.exception
    markdown = _markdown_values(at)
    for label in ("bubble sort", "selection sort", "quick sort"):
        assert f"**{label}**" in markdown
    assert markdown.count("Accuracy: pass") == 3
    assert "Accuracy: fail" not in markdown
    # The sorted order comes from U1: all three columns show it (the
    # echo is single-line; the per-column sorted lists are multi-line).
    expected_order = "\n".join(sorted(["banana", "apple", "cherry"]))
    sorted_lists = [
        value for value in _text_values(at) if "apple" in value and "\n" in value
    ]
    assert len(sorted_lists) == 3
    assert all(value == expected_order for value in sorted_lists)


def test_counts_match_sorting_core_and_render_as_full_integers() -> None:
    """Comparisons/Swaps lines show U1's exact integers, untruncated."""
    entries = [f"item{i:02d}" for i in range(20)][::-1]  # 20 reversed
    _, expected_results, _ = run_all(entries)

    at = _app_test()
    at.text_area[0].set_value(", ".join(entries))
    at.button[0].click()
    at.run()

    assert not at.exception
    markdown = _markdown_values(at)
    for result in expected_results:
        assert f"Comparisons: {result.comparisons}" in markdown
        assert f"Swaps: {result.swaps}" in markdown
    # 20 reversed strings yield comparisons well past three digits, so a
    # rendered match proves there is no truncation (AC3.2.5).
    assert expected_results[0].comparisons >= 100


def test_deduplication_sorts_typed_and_picked_string_once() -> None:
    """A string typed and also picked from the word list sorts once."""
    at = _app_test()
    at.text_area[0].set_value("apple, apple")
    at.multiselect[0].set_value(["apple"])
    at.button[0].click()
    at.run()

    assert not at.exception
    echo = _text_values(at)[0]
    assert echo.count("apple") == 1
    assert _markdown_values(at).count("Accuracy: pass") == 3


def test_empty_input_shows_exact_message_and_no_result_columns() -> None:
    """Sort with nothing entered: exact FR6.1 message, no results."""
    at = _app_test()
    at.run()
    # The empty-state hint is present before the first Sort press.
    assert at.info
    assert not at.warning

    at.button[0].click()
    at.run()

    assert not at.exception
    assert [alert.value for alert in at.warning] == [EMPTY_INPUT_MESSAGE]
    # The hint is replaced by the warning after the first Sort press.
    assert not at.info
    # No result columns: no algorithm headings, metrics, or accuracy.
    markdown = _markdown_values(at)
    assert not any("Comparisons:" in value for value in markdown)
    assert not any("Accuracy:" in value for value in markdown)


def test_over_cap_input_shows_limit_message_and_runs_no_sorting(
    monkeypatch,
) -> None:
    """More than 100 de-duplicated strings: refuse to sort (SD-3)."""

    def forbidden_normalize(self, raw_entries: list[str]):
        raise AssertionError("normalize must not run above the cap")

    monkeypatch.setattr(sorting_core.InputProcessor, "normalize", forbidden_normalize)

    at = _app_test()
    entries = ", ".join(f"item{i}" for i in range(101))
    at.text_area[0].set_value(entries)
    at.button[0].click()
    at.run()

    assert not at.exception
    assert [alert.value for alert in at.error] == [LIMIT_MESSAGE]
    markdown = _markdown_values(at)
    assert not any("Comparisons:" in value for value in markdown)


def test_word_list_is_non_empty_and_read_only() -> None:
    """The bundled word list is non-empty and cannot be mutated."""
    import app

    assert len(app.WORD_LIST) > 0
    assert all(isinstance(word, str) and word for word in app.WORD_LIST)
    with pytest.raises(AttributeError):
        app.WORD_LIST.append("not-allowed")  # type: ignore[attr-defined]


def test_multiselect_offers_the_bundled_word_list() -> None:
    """The picker's options are exactly the bundled list, read-only."""
    import app

    at = _app_test()
    at.run()

    assert list(at.multiselect[0].options) == list(app.WORD_LIST)


def test_source_uses_no_unsafe_html_and_no_eval_or_exec() -> None:
    """User strings stay inert data: no HTML injection, no eval/exec.

    Scans the parsed AST of ``app.py`` so documentation mentions of the
    forbidden constructs do not trip the check — only real usage does.
    Attribute-style ``compile`` is allowed (``re.compile`` of a static
    pattern is legitimate); only builtin-style calls are flagged.
    """
    tree = ast.parse(APP_PATH.read_text(encoding="utf-8"))
    forbidden_names = {"eval", "exec", "compile"}
    html_flags: list[str] = []
    forbidden_calls: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.keyword) and node.arg == "unsafe_allow_html":
            html_flags.append(node.arg)
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id in forbidden_names:
                forbidden_calls.append(func.id)
            elif isinstance(func, ast.Attribute) and func.attr in {"eval", "exec"}:
                forbidden_calls.append(func.attr)
    assert html_flags == []
    assert forbidden_calls == []


def test_single_string_renders_pass_with_zero_counts() -> None:
    """Edge case: one string sorts to itself with accuracy pass."""
    at = _app_test()
    at.text_area[0].set_value("pear")
    at.button[0].click()
    at.run()

    assert not at.exception
    markdown = _markdown_values(at)
    assert markdown.count("Accuracy: pass") == 3
    assert "Comparisons: 0" in markdown
    assert "Swaps: 0" in markdown
    assert "pear" in _text_values(at)


def test_all_identical_strings_collapse_to_one_and_pass() -> None:
    """Edge case: duplicates de-duplicate; the single string passes."""
    at = _app_test()
    at.text_area[0].set_value("zebra, zebra, zebra")
    at.button[0].click()
    at.run()

    assert not at.exception
    assert _markdown_values(at).count("Accuracy: pass") == 3
    echo = _text_values(at)[0]
    assert echo == "zebra"


def test_u1_exceptions_propagate_to_streamlit(monkeypatch) -> None:
    """SD-6: a sorting-core error is surfaced, never swallowed."""

    def boom(self, raw_entries: list[str]):
        raise ValueError("run_id mismatch")

    monkeypatch.setattr(sorting_core.InputProcessor, "normalize", boom)

    at = _app_test()
    at.text_area[0].set_value("banana")
    at.button[0].click()
    at.run()

    assert at.exception
    assert "run_id mismatch" in str(at.exception[0].value)


def test_results_recompute_after_widget_change_without_new_click() -> None:
    """PD-2: displayed output is a pure function of current widgets."""
    at = _app_test()
    at.text_area[0].set_value("banana, apple, cherry")
    at.button[0].click()
    at.run()
    assert any(value.endswith("cherry") and "\n" in value for value in _text_values(at))

    # Change the text area without clicking Sort again; the rerun shows
    # results for the new values, recomputed fresh (no stored results).
    at.text_area[0].set_value("delta, alpha")
    at.run()

    assert not at.exception
    expected = "\n".join(sorted(["delta", "alpha"]))
    sorted_lists = [
        value for value in _text_values(at) if "alpha" in value and "\n" in value
    ]
    assert len(sorted_lists) == 3
    assert all(value == expected for value in sorted_lists)
