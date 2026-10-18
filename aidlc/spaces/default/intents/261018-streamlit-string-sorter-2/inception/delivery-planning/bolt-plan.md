# Bolt Plan

A **Bolt** is one build pass over one Unit of Work, ending in something that runs and can be checked. Bolts run in the order below, because the Unit dependency chain is linear (U1 → U2 → U3). This is not a walking skeleton: the team chose not to build one (team.md).

## Bolt 1 — sorting-core (U1)

- **Units included:** U1 `sorting-core` (library)
- **Walking skeleton:** no
- **Depends on:** none
- **Contents:** InputProcessor (normalize), SortingEngine (bubble, selection, quick sort with shared counting), AccuracyChecker (pass/fail against `sorted()`)
- **Definition of Done**
  - All three sorts pass the accuracy check on the sample inputs, including single, identical, and empty-token cases (US4.2)
  - Comparison and swap counts follow one definition for all three algorithms (FR4.2, FR4.3), once the step-count definition is settled in Functional Design
  - pytest passes; line coverage on the sorting logic is at least 80% (team testing posture)
  - Black and Ruff pass
- **Confidence hypothesis:** the three sorts produce results identical to Python's `sorted()`, with counts that can be compared across algorithms.
- **Expected demo:** pytest output showing each algorithm's result, comparison count, swap count, and accuracy for a sample list. This is a check, not a UI demo.

## Bolt 2 — playground-ui (U2)

- **Units included:** U2 `playground-ui` (ui)
- **Walking skeleton:** no
- **Depends on:** Bolt 1
- **Contents:** SortingPlaygroundApp (single page, orchestration), WordListProvider (bundled list), local run entry point
- **Definition of Done**
  - The page matches the refined mockups: input row, Sort button, input echo, three result columns (US3.1, US3.2)
  - Empty input shows the exact FR6.1 message and runs no sort (US4.1)
  - The word picker is populated from the bundled list with no network access (US1.2)
  - `streamlit run app.py` runs locally (US5.1)
  - Ruff and Black pass; UI wiring has at least a smoke test
- **Confidence hypothesis:** a learner can go from typed or picked input to a side-by-side comparison on one screen without help.
- **Expected demo:** local `streamlit run app.py`, entering a list and reading three result columns.

## Bolt 3 — delivery-pipeline (U3)

- **Units included:** U3 `delivery-pipeline` (packaging)
- **Walking skeleton:** no
- **Depends on:** Bolt 2
- **Contents:** GitHub Actions workflow (install, Ruff, Black, pytest, deploy on merge to `main`), Streamlit Community Cloud configuration
- **Definition of Done**
  - A pull request runs lint, format check, and tests, and a failure blocks the merge (team Code Style)
  - A squash-merge to `main` deploys the app to Streamlit Community Cloud automatically (US5.2, FR7.3)
  - The Python version and dependency pinning from the contract open question are decided
- **Confidence hypothesis:** a change merged to `main` reaches the public app without a manual step.
- **Expected demo:** a merge to `main` followed by a live app showing the change.
- **Blocked by:** the external items in `external-dependency-map.md`

## Order

Bolt 1, then Bolt 2, then Bolt 3. Each Bolt starts after the previous one passes its Definition of Done.
