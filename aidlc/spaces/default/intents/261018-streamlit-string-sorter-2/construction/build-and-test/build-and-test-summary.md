# Build and Test Summary

Intent: `261018-streamlit-string-sorter-2` — Streamlit String Sorting Visualizer
Date: 2026-10-22
Test strategy: Standard (integration instructions required; all produces generated)

## Overall result

**PASS with one surfaced documentation defect.** The repository builds, all
116 tests pass, both coverage floors are exceeded, and 31/31 in-scope
verification targets are Met. The cross-unit traceability check returns FAIL
for a requirement-ID gap inherited from Code Generation (details below); no
test or behaviour is unverified.

## Unit-by-unit build status

| Unit | Scope | Build | Tests | Coverage | Status |
|------|-------|-------|-------|----------|--------|
| `sorting-core` (U1) | Normalization, three algorithms, accuracy checker, engine | Compiles; imports cleanly | 97 passed | 100% of 166 statements | Ready |
| `playground-ui` (U2) | Streamlit script: input, guards, three-column results, word list | Compiles; imports; boots headless | 12 passed | `app.py` 100% (56 statements) | Ready |
| `delivery-pipeline` (U3) | GitHub Actions workflow (push to `main`, Black → Ruff → pytest) | YAML parses; structure asserted | 7 passed | via full suite (100%) | Ready |

Combined authoritative run: `pytest` → **116 passed**, 100.00% `sorting_core`
coverage, exit 0.

## Coverage achieved vs expected

| Measure | Target | Achieved | Verdict |
|---------|--------|----------|---------|
| `sorting_core` line coverage | ≥ 80% (NFR4.2) | 100.00% (166/166) | Met |
| `app.py` line coverage | ≥ 80% (U2 instructions) | 100% (56/56) | Met |
| CI gate configuration | Black, Ruff, bare `pytest` with floor, `if: always()` | Present and asserted by tests | Met |

## Test types executed

- Unit: algorithms, counting, checker, normalization (97 tests).
- Integration: UI → core wiring through `AppTest`; repository → CI commands (19 tests).
- Edge cases: empty input, single element, all-identical strings, duplicates, non-ASCII, 100/101-string boundary, hostile strings as inert text.
- Security: AST/API static scan, least-privilege workflow assertions.
- Performance: bounded-work checks at the 100-string cap (no numeric target exists).
- Build smoke: byte-compile, warning-free import, headless Streamlit boot.
- Not executed (deferred): live CI run and deployment observation — the next two stages own them.

Full evidence, per-target mapping, and failure explanations are in
`test-results.md`; the traceability verdict is in `cross-unit-traceability.md`.

## Known limitations

1. **Requirement-ID traceability gap (FAIL at Step 10).** `FR1.1`–`FR6.4`
   (27 IDs) plus `NFR1.2`, `NFR3.5`, `NFR4.3` are absent from all three
   `traceability.json` files at ID level. Their acceptance criteria are
   covered OK (29/29 ACs), so this is a documentation gap, not untested
   behaviour. Recommended fix: a mechanical refresh of the traceability files,
   no code change.
2. **U3 scoped pytest run exits 1 on coverage.** The project-wide
   `--cov=sorting_core --cov-fail-under=80` addopts cannot be satisfied by a
   workflow-only test run. The 7 tests pass; the full suite is the
   authoritative gate. The floor and configuration were left untouched.
3. **Local Python 3.14.8 vs CI 3.12.** All gates pass locally; the first live
   3.12 run is owned by CI Pipeline.
4. **No live deployment was exercised.** AC5.2.x deployment observation is
   owned by Deployment Pipeline / Deployment Execution.

## Readiness statement

The code is **build-ready and test-ready**: it compiles, boots, sorts
correctly for all three algorithms, reports accurate comparison/swap counts
and accuracy, enforces the input guards, and meets the coverage floor with
headroom. It is **ready for CI Pipeline and Deployment Pipeline** on the
strength of the verified workflow configuration. The traceability gap should
be corrected before the initiative is considered documentation-complete; it
does not block the build.

## Artifacts

| Artifact | Contents |
|----------|----------|
| `build-instructions.md` | Prerequisites, setup, compile/import/run commands, troubleshooting |
| `integration-test-instructions.md` | Tested boundaries, commands, coverage targets, addopts caveat |
| `performance-test-instructions.md` | Cap check, bounded-work rationale, optional benchmark |
| `security-test-instructions.md` | Security NFR checks, static scan, out-of-scope notes |
| `test-results.md` | Build/coverage/test results, failure details, 31-row verification matrix |
| `cross-unit-traceability.md` | Per-unit traceability, dependency resolution, uncovered IDs (FAIL) |
| `build-and-test-summary.md` | This document |
