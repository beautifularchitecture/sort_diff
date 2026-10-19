# Frontend Components — playground-ui (U2)

## Components

| Component | Type | Responsibility | Depends On | State |
|---|---|---|---|---|
| SortingPlaygroundApp | Streamlit page | Single-screen UI; input row, Sort button, input echo, three result columns, empty-state hint; orchestrates normalize → run-all → verify → render on Sort press | InputProcessor, WordListProvider, SortingEngine, AccuracyChecker | shared list, picked words |
| WordListProvider | Streamlit multiselect options | Fixed bundled word list shipped with the app; read-only picker options; no network or file I/O at runtime | none | bundled list (constant) |

## Widgets

- Text area: manual entry of strings separated by line breaks or commas (US1.1).
- Multiselect: bundled word options (US1.2).
- Sort button: runs all three algorithms on the same shared list (US2.1, FR5.2).
- Input echo: shows the normalized input list that was sorted (FR5.4, AC3.1.1).
- Three result columns: one per algorithm, name + sorted list + metrics + accuracy (FR5.3).
- Warning: exact FR6.1 message when the shared list is empty; columns hidden (Q1).

## Styling

Basic Streamlit defaults only; no custom CSS; no complex styling beyond basic Streamlit (NFR2.1, NFR3.6).
