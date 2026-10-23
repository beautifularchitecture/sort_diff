# Cross-Unit Traceability

Step 10 of Build and Test: collect each unit's `traceability.json` and
`code-summary.md`, resolve cross-unit dependencies, verify that each
three-segment acceptance criterion is covered by the unit that owns it, and
confirm that every target file the entries name exists.

Date: 2026-10-22. Intent: `261018-streamlit-string-sorter-2`.

## Verdict: FAIL (identifier-level documentation gap; no acceptance-criterion gap)

- **Acceptance criteria: PASS.** All 29 distinct `AC<n>.<n>.<n>` IDs from
  `stories.md` are covered `OK` by at least one unit, and every AC that U1
  marks `N/A` is covered `OK` by U2. No dependency dangles.
- **Measurable requirement IDs: FAIL.** 27 functional requirements
  (`FR1.1`–`FR6.4`) and 3 non-functional requirements (`NFR1.2`, `NFR3.5`,
  `NFR4.3`) appear in no unit's `coverage[]` at ID level, so the
  requirement → unit mapping cannot be confirmed from the artifacts.
- **Target files: PASS.** Every path named in the three `traceability.json`
  files exists in the repository; no test or source reference is stale.

The FR-level gap is inherited from Code Generation (the artifacts trace
acceptance criteria and business rules, not FR IDs). It does not indicate
untested behaviour — each FR's acceptance criteria are covered — but Step 10
cannot pass a check it cannot resolve, so this stage records FAIL and surfaces
the gap rather than inferring coverage.

## Per-unit artifacts

| Unit | Traceability entries | OK | N/A | Tests | Coverage |
|------|---------------------|----|-----|-------|----------|
| `sorting-core` (U1) | 39 | 34 | 5 (AC1.1.3, AC3.1.1–AC3.1.4 — display concerns owned by U2) | 97 | 100% |
| `playground-ui` (U2) | 38 | 38 | 0 | 12 | `app.py` 100% |
| `delivery-pipeline` (U3) | 17 | 17 | 0 | 7 | verified via full suite (see note) |
| **Total** | **94** | **89** | **5** | **116** | floor 80% met |

Note: the U3 workflow tests import no application code, so a unit-scoped
pytest run reports 0% coverage under the project-wide `--cov=sorting_core`
addopts. The full-suite run is the authoritative measurement and reports
100%.

## Cross-unit dependency resolution

| Criterion | Owning unit | Counterpart | Resolution |
|-----------|-------------|-------------|------------|
| AC1.1.3 (normalized input is displayed) | U2 | U1 supplies `SortInput.normalized_strings` | OK — U2 entry covers it |
| AC3.1.1–AC3.1.4 (algorithm columns, names, lists) | U2 | U1 supplies `AlgorithmResult` (name + sorted list + counts) | OK — U2 entries cover them |
| AC5.2.1–AC5.2.3 (deploy/CI behaviour) | U3 | U1/U2 commands (`black`, `ruff`, `pytest`) | OK — `tests/test_workflow.py` asserts the commands |
| AC3.2.x (counts and accuracy) | U1 and U2 | U1 computes; U2 displays | OK — both units have OK entries |

No circular or unresolved dependency was found.

## Uncovered requirement IDs

Functional requirements absent from all `coverage[]` arrays:

`FR1.1, FR1.2, FR1.3, FR1.4, FR1.5, FR2.1, FR2.2, FR2.3, FR2.4, FR2.5,
FR3.1, FR3.2, FR3.3, FR4.1, FR4.2, FR4.3, FR4.4, FR4.5, FR5.1, FR5.2,
FR5.3, FR5.4, FR5.5, FR6.1, FR6.2, FR6.3, FR6.4`

(`FR7.1`–`FR7.3` are present and OK in U3.)

Non-functional requirements absent from all `coverage[]` arrays:

`NFR1.2, NFR3.5, NFR4.3`

All other NFR IDs (`NFR1.1`, `NFR2.1`, `NFR2.2`, `NFR2.3`, `NFR2.3.1`,
`NFR3.1`–`NFR3.4.2`, `NFR3.6`, `NFR4.1`, `NFR4.1.1`, `NFR4.2`,
`NFR4.2.1`) are present in at least one unit with status OK.

## Impact and recommended action

- **Impact on this stage:** none on test execution or coverage; the suite and
  the verification matrix stand on their own evidence. The gap is a
  documentation/traceability defect in the Code Generation outputs.
- **Recommended action:** refresh the three `traceability.json` files with
  FR-level and missing NFR-level rows, pointing each at the acceptance
  criteria and tests that already cover it. This is mechanical and can be done
  in a follow-up Code Generation revision without changing code.
- **For the gate:** the human is told that the stage's tests are green but the
  cross-unit traceability check returns FAIL for this identifier-level gap.
