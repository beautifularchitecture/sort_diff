# User Stories — Story Plan

## Persona Development Approach

Three personas drawn from the requirements intent analysis (students, educators, developers), ranked by priority:

1. **Sam the Student** (primary) — learner using the app to understand how bubble, selection, and quick sort behave on strings; cares about visible results, step counts, and pass/fail accuracy.
2. **Elena the Educator** — instructor demonstrating algorithms live; cares about quick preset input (bundled word list) and trustworthy accuracy feedback.
3. **Devon the Developer** — practitioner refreshing intuition or checking implementation behavior; cares about local run and clean metrics.

## Story Format

Standard format `As a [persona], I want [goal], so that [benefit]`, with 3–6 Given/When/Then acceptance criteria per story (IDs `AC{g}.{s}.{n}`), INVEST-compliant (Independent, Negotiable, Valuable, Estimable, Small, Testable). Sad paths included in every story group.

## Story Prioritization (MoSCoW)

The MVP boundary is formally decided at Delivery Planning; priorities here inform it.

- **Must Have**: US1.1, US1.2, US2.1, US3.1, US3.2, US4.1, US4.2, US5.2 — every story traces to a functional requirement in v1 scope.
- **Should Have**: US5.1 — local run is required by FR7.1 but is developer-facing; ranked below the deployed-app stories for MoSCoW signalling.
- **Could Have**: none at this scope.
- **Won't Have (this version)**: captured in requirements Out of Scope (extra algorithms, file upload, accounts, performance tuning).

## Breakdown Approach

**By feature area**, mapping 1:1 onto the FR groups in requirements.md:

| Group | Theme       | Stories  | Requirements covered |
|-------|-------------|----------|----------------------|
| US1   | Input       | US1.1–1.2 | FR1                 |
| US2   | Sorting     | US2.1     | FR2                 |
| US3   | Results     | US3.1–3.2 | FR3, FR4, FR5       |
| US4   | Edge cases  | US4.1–4.2 | FR6                 |
| US5   | Deployment  | US5.1–5.2 | FR7                 |

## Embedded Questions

None required. The requirements analysis answered every open product question (Q1–Q11 plus accepted assumptions), and the human instructed full autopilot for this workflow; ambiguity analysis of the plan surfaced no vague language, contradictions, or missing details. The plan proceeds directly to generation; the human reviews the combined plan + stories at the completion gate.

## Consolidated Summary Confirmation

Here is the combined summary of this stage's decisions. Please confirm it.

**Personas (3)**: Sam the Student (primary — learner comparing algorithms), Elena the Educator (demo via bundled word list), Devon the Developer (local run, honest metrics).

**Stories (9, feature-area breakdown mapping 1:1 to FR groups)**:
- US1.1 (Must) Manual string entry — type/paste, lowercase normalization (FR1.1, FR1.3, FR1.4)
- US1.2 (Must) Bundled word-list selection — fixed list shipped with the app (FR1.2, FR1.5)
- US2.1 (Must) Single Sort button runs bubble, selection, and quick sort on the same input, lexicographically (FR2)
- US3.1 (Must) Side-by-side results with input shown, clear educational presentation (FR5)
- US3.2 (Must) Per-algorithm comparisons count, swaps count, and pass/fail accuracy vs Python `sorted()` (FR3, FR4)
- US4.1 (Must) Empty-input message "Enter or select at least one string", sorting does not run (FR6.1)
- US4.2 (Must) Single-string, all-identical, and empty-string edge cases (FR6.2–FR6.4)
- US5.1 (Should) Local run via `streamlit run` (FR7.1)
- US5.2 (Must) Auto-deploy to Streamlit Community Cloud on merge to main via GitHub Actions (FR7.2, FR7.3)

**Traceability**: FR1–FR7 all OK against US1.1–US5.2. NFR1, NFR2 OK (US3.2, US3.1). NFR3 Deferred to nfr-requirements. NFR4 Deferred to build-and-test.

**Stage mode note**: lead-only run (collaborators off for this scope) — no mob round, no contribution files owed.

[Answer]:
