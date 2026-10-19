# Infrastructure Design Questions — sorting-core (U1)

Settled earlier and not repeated here: GitHub Actions for CI (FR7.3), Python 3.12, pytest, Black and Ruff (team.md), minimum-version dependency ranges, no runtime services for this unit.

## Q1: What the CI workflow checks for sorting-core

A. Install, Black check, Ruff check, pytest with 80% line coverage floor on the sorting logic; any failure blocks merge (recommended; matches team.md and NFR4.2)
B. Install, Black check, Ruff check, pytest without a coverage gate; coverage reported only
X. Other (please specify)

[Answer]:

## Q2: Where sorting-core's tests run relative to the app

A. Run this unit's tests as a separate CI job before the app's UI tests (recommended; fails fast on core logic errors)
B. Run all tests in one job together with the app
X. Other (please specify)

[Answer]:
