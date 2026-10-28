# Code Structure — sort_diff

## Directory Layout (hand-written project content)
```
.
├── app.py                         Configuration/UI entry (Streamlit)
├── sorting_core/                  Domain package (pure stdlib)
│   ├── __init__.py                Public re-exports
│   ├── types.py                   Model: SortInput, AlgorithmResult, AccuracyCheck, Counter
│   ├── normalize.py               Service: InputProcessor (boundary validation + normalization)
│   ├── algorithms.py              Utility: bubble_sort, selection_sort, quick_sort
│   ├── engine.py                  Service: SortingEngine.run_all
│   ├── checker.py                 Service: AccuracyChecker
│   ├── runner.py                  Service: run_all convenience pipeline
│   └── words.py                   Static data: WordListProvider
├── tests/                         Test (pytest)
│   ├── test_algorithms.py, test_checker.py, test_engine.py,
│   │   test_normalize.py, test_runner.py, test_types.py, test_words.py
│   ├── test_workflow.py           Test: parses .github/workflows/ci.yml
│   └── ui/test_app.py             Test: streamlit AppTest against app.py
├── .github/workflows/ci.yml       Configuration (CI)
├── .devcontainer/devcontainer.json Configuration (dev container)
├── requirements.txt               Configuration (dependencies)
├── pyproject.toml                 Configuration (project metadata, black, ruff, pytest)
├── README.md, AGENTS.md           Documentation
└── .gitignore (project part)      Configuration
```
Excluded from this map: `.aidlc/`, `.opencode/`, `aidlc/` (AI-DLC), `.venv/`, caches, `.git/`.

## File Classification
| File | Category |
|------|----------|
| `app.py` | Controller/Handler (UI routing and rendering) |
| `sorting_core/types.py` | Model/Entity |
| `sorting_core/normalize.py` | Utility/Helper (boundary validation) |
| `sorting_core/algorithms.py` | Service/UseCase (algorithms) |
| `sorting_core/engine.py`, `checker.py`, `runner.py` | Service/UseCase |
| `sorting_core/words.py` | Static/Asset (data) |
| `sorting_core/__init__.py` | Configuration (re-exports) |
| `tests/*` | Test |
| `.github/workflows/ci.yml`, `.devcontainer/devcontainer.json`, `pyproject.toml`, `requirements.txt` | Configuration |

## Dependency Graph (intra-project imports)
- `app.py` → `sorting_core` (`InputProcessor`, `SortingEngine`, `AccuracyChecker`, `WordListProvider`, and types)
- `sorting_core/__init__.py` → `algorithms`, `checker`, `engine`, `normalize`, `runner`, `types`, `words`
- `sorting_core/engine.py` → `algorithms`, `types`
- `sorting_core/checker.py` → `types`
- `sorting_core/normalize.py` → `types`
- `sorting_core/runner.py` → `checker`, `engine`, `normalize`, `types`
- `sorting_core/algorithms.py` → `types`
- `sorting_core/types.py`, `sorting_core/words.py` → (none)
- Circular references: none found.

External imports: `streamlit` (`app.py`, tests), `pytest`, `yaml` (tests).

## Code Patterns
- Frozen dataclasses for value objects (`types.py`); one mutable `Counter` shared per engine run, reset between algorithms (`engine.py`).
- Boundary `TypeError`/`ValueError` checks in every public entry point (`normalize.py`, `engine.py`, `checker.py`).
- Each algorithm sorts `(value, index)` pairs to keep equal strings in input order (`algorithms.py`).
- `app.py` is a single `main()` function with module-level constants for exact UI strings.

## Error Handling Pattern
Errors are raised, not caught: the core raises `TypeError`/`ValueError` and `app.py` has no `try`/`except`, so Streamlit shows the traceback (`app.py` SD-6 comment).
