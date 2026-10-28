# String Sorting Visualizer

An educational Streamlit app for exploring how different sorting algorithms order strings. It compares bubble sort, selection sort, and quick sort on the same input so learners can inspect each result and compare element comparisons, swaps, and sorting accuracy against Python's built-in `sorted()` function.

## Features

- Enter strings manually or choose from a bundled word list.
- Sort the same input with bubble sort, selection sort, and quick sort.
- View the sorted output, comparison count, swap count, and accuracy for each algorithm.
- See the input used for each comparison.

## Requirements

- Python 3.12 or newer

## Setup

This project uses [uv](https://docs.astral.sh/uv/). Install uv once; there is no manual virtual environment to create or activate. `uv run` and `uvx` provision Python and the dependencies in `requirements.txt` on demand.

## Run the app

```bash
uv run --with-requirements requirements.txt streamlit run app.py
```

Streamlit prints a local URL (by default http://localhost:8501). Open it in a browser.

## Run the checks

The CI gates run in this order. Run them locally before pushing:

```bash
uvx black --check .
uvx ruff check .
uvx --with-requirements requirements.txt pytest
```

To run a single test without the coverage gate:

```bash
uvx --with-requirements requirements.txt pytest tests/test_algorithms.py::test_name --no-cov
```

Partial runs need `--no-cov` because `pyproject.toml` enforces 80% coverage on `sorting_core`.

## Docker Hub credentials

GitHub Actions expects the Docker Hub credentials to be configured as GitHub repository secrets:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

Add them in the repository's **Settings → Secrets and variables → Actions**. Store the Docker Hub access token as a secret; do not put credential values in this README or commit them to the repository.
