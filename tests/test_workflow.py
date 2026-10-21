"""Structure tests for the committed CI workflow (U3 delivery-pipeline).

The GitHub Actions run itself is the end-to-end test for the workflow;
these tests assert that the committed `.github/workflows/ci.yml` matches
the fixed facts the design fixes (SD-1..SD-7, Contract 2).
"""

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "ci.yml"


def load_workflow() -> tuple[str, dict]:
    """Return the raw workflow text and its parsed YAML mapping."""
    text = WORKFLOW_PATH.read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    return text, data


def on_block(data: dict) -> dict:
    """Return the workflow trigger mapping.

    PyYAML follows YAML 1.1, where the bare ``on`` key resolves to the
    boolean ``True``; GitHub Actions reads it as the string ``on``.
    """
    return data["on"] if "on" in data else data[True]


def steps(data: dict) -> list[dict]:
    """Return the steps of the single ``checks`` job, in order."""
    return data["jobs"]["checks"]["steps"]


def step_keys(data: dict) -> list[str]:
    """One identifier per step: its ``uses`` ref or its ``run`` command."""
    return [step.get("uses") or step.get("run") for step in steps(data)]


def first_index(keys: list[str], prefix: str) -> int:
    """Index of the first step identifier starting with ``prefix``."""
    for index, key in enumerate(keys):
        if key.startswith(prefix):
            return index
    raise AssertionError(f"no step identifier starts with {prefix!r}")


def test_workflow_is_valid_yaml_mapping() -> None:
    """Case 1: the workflow file parses as a top-level YAML mapping."""
    _, data = load_workflow()
    assert isinstance(data, dict)


def test_triggers_on_push_to_main_only() -> None:
    """Case 2: push-to-main trigger only, no pull_request (SD-1, FR7.3)."""
    _, data = load_workflow()
    trigger = on_block(data)
    assert set(trigger) == {"push"}
    assert trigger["push"]["branches"] == ["main"]


def test_single_serial_checks_job_on_ubuntu() -> None:
    """Case 3: exactly one job, ``checks``, on ubuntu-latest (SD-2)."""
    _, data = load_workflow()
    assert list(data["jobs"]) == ["checks"]
    assert data["jobs"]["checks"]["runs-on"] == "ubuntu-latest"


def test_setup_python_then_install_in_order() -> None:
    """Case 4: setup-python 3.12 then pip install, in order (SD-2, SD-7)."""
    _, data = load_workflow()
    keys = step_keys(data)
    setup_index = first_index(keys, "actions/setup-python")
    install_index = keys.index("pip install -r requirements.txt")
    assert setup_index < install_index
    setup_step = steps(data)[setup_index]
    assert setup_step.get("with", {}).get("python-version") == "3.12"


def test_gate_steps_in_order_with_always() -> None:
    """Case 5: install, black, ruff, pytest in order, gates if: always()."""
    _, data = load_workflow()
    keys = step_keys(data)
    commands = ("black --check .", "ruff check .", "pytest")
    gate_indexes = [keys.index(command) for command in commands]
    ordered = [keys.index("pip install -r requirements.txt"), *gate_indexes]
    assert ordered == sorted(ordered)
    for index in gate_indexes:
        assert steps(data)[index].get("if") == "always()"


def test_least_privilege_and_no_secrets_or_deploy() -> None:
    """Case 6: permissions {contents: read}; no secrets., no deploy (SD-5/6)."""
    text, data = load_workflow()
    assert data.get("permissions") == {"contents": "read"}
    assert "secrets." not in text
    assert "deploy" not in text.lower()


def test_bare_pytest_command() -> None:
    """Case 7: the pytest step runs exactly ``pytest`` (SD-4, Contract 2)."""
    _, data = load_workflow()
    pytest_steps = [step for step in steps(data) if step.get("run") == "pytest"]
    assert len(pytest_steps) == 1
    assert pytest_steps[0]["run"].split() == ["pytest"]
