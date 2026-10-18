# Tech Stack Decisions — sorting-core (U1)

## Decisions

| Area | Decision | Rationale | Source |
|---|---|---|---|
| Language | Python 3.12 | Confirmed in NFR Q6 (C). Matches the CI target listed as an open question in contract-summary. | NFR Q6, contract-summary (open question) |
| Standard library only | Pure Python; no third-party runtime dependency in `sorting-core` | Pure domain logic (ADR-004); `sorted()` is the accuracy reference | NFR3.4, components.md (AccuracyChecker) |
| Test framework | pytest | Team testing posture | team.md, NFR4.2 |
| Formatter and linter | Black and Ruff | Team code style | team.md Code Style, NFR4.1 |
| Dependency pinning | Minimum-version ranges in `requirements.txt` | Confirmed in NFR Q6 (C) | NFR Q6 |
| Naming | snake_case modules, functions, and variables | Team code style | team.md, NFR4.1 |

## Notes

- Dependency pinning is a project-wide choice made in NFR Q6. It is recorded here and applies to the whole repository's `requirements.txt`. The `sorting-core` unit adds no runtime dependency.
- Python 3.12 is the value the CI workflow in U3 must use. Recording it here resolves the open question in contract-summary for the Python version. The dependency-pin strategy is also resolved.
