# Unit of Work

Three Units, derived from the five Domain Design components. Plan approved by the human (Approve Plan, non-ASCII pass-through per D10).

## Unit Table

| Unit ID | Name | Directory | Kind | Complexity |
|---|---|---|---|---|
| U1 | sorting-core | `u1-sorting-core` | library | M |
| U2 | playground-ui | `u2-playground-ui` | ui | M |
| U3 | delivery-pipeline | `u3-delivery-pipeline` | packaging | S |

## U1 — sorting-core

- **Kind**: library
- **Description**: Pure domain logic with no UI runtime. Normalizes input, runs bubble, selection, and quick sort with one shared comparison and swap count, and verifies each result against Python `sorted()`.
- **Components**: InputProcessor, SortingEngine, AccuracyChecker
- **Owns entities**: SortInput, AlgorithmResult, AccuracyCheck
- **Responsibilities**
  - Normalization: split on newlines and commas, trim, drop empty tokens, lowercase ASCII capitals, pass non-ASCII through unchanged (FR1.3, FR1.4, FR6.4, D10)
  - Three algorithms over lexicographic order (FR2.1–FR2.5)
  - Comparison and swap counting with one definition for all three (FR4.1–FR4.5)
  - Accuracy: exact order match against `sorted()` per algorithm (FR3.1–FR3.3)
- **Deployment model**: in-process module imported by U2; no standalone deployment
- **Implementation notes**
  - Pure functions; no I/O and no Streamlit imports
  - Test-after with pytest; ~80% line coverage floor on the sorting logic (team testing posture)
  - Empty input is handled by the caller (U2) for the FR6.1 message; U1 returns an empty result when given an empty list

## U2 — playground-ui

- **Kind**: ui
- **Description**: The single Streamlit page. Renders the input row, Sort button, input echo, three result columns, and the FR6.1 warning. Bundles the fixed word list.
- **Components**: SortingPlaygroundApp, WordListProvider
- **Owns entities**: BundledWordList
- **Responsibilities**
  - Render the screen per refined mockups (D1–D10): text area, multiselect, Sort, echo, three columns, empty-state hint
  - Orchestrate normalize, sort, verify, render on button press (ADR-004)
  - Render exact FR6.1 warning and skip sorting on an empty shared list
  - Provide the bundled word list as read-only picker options (FR1.5)
  - Local run entry point: `streamlit run` (US5.1)
- **Deployment model**: Streamlit application; deployed by U3
- **Implementation notes**
  - No algorithm, normalization, or verification logic in this Unit (ADR-004)
  - No custom CSS; Streamlit defaults only (design-system-mapping)
  - Bundled list is a shipped constant, no network fetch, non-empty (FR1.5, AC1.2.3)

## U3 — delivery-pipeline

- **Kind**: packaging
- **Description**: CI workflow and continuous deployment. On merge to `main`, runs the test suite and lint and deploys the app to Streamlit Community Cloud.
- **Components**: none (infrastructure artefacts only; not a domain component)
- **Owns entities**: none
- **Responsibilities**
  - GitHub Actions workflow: install, Black and Ruff checks, pytest, deploy on merge to `main` (US5.2, FR7.2, FR7.3)
  - Streamlit Community Cloud configuration pointing at the app entry point
  - Fail the pipeline on test, lint, or format failures (team Code Style: failure blocks merge)
- **Deployment model**: CI pipeline plus Streamlit Community Cloud hosting
- **Implementation notes**
  - Trunk-based: squash-merge to `main` triggers deploy (team Way of Working)
  - No deployment to staging; production deploy on merge is the team's affirmed practice (team.md)

## Rules Verified

- Each Unit has a stable ID (`U{n}`) and a construction directory (`u{n}-{description}`).
- Every Unit has a kind from the allowed set.
- No Unit is a bare design document: U1 and U2 produce runnable code, and U3 produces a runnable pipeline.
