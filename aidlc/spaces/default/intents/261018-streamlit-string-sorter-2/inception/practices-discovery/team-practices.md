# Team Practices

## Way of Working

- **Proposal (to be confirmed by interview):** Follow trunk-based development aligned with org defaults. Short-lived feature branches off `main` (resolved within 1-2 days). Squash-merge into `main` with the Bolt/branch name as the commit message. Keep trunk clean and avoid long-lived release branches; gate production via tags or environment-specific deployment configs if multiple environments are needed.

## Walking Skeleton

- **Proposal (to be confirmed):** For this feature scope with a single-developer/fast-moving build, a walking skeleton is **not required**. The slice is small (three sorting algorithms + Streamlit UI + backend sort button). We can start from the minimal working app and iterate. If the human prefers to prove the end-to-end path early, we will build the thinnest possible skeleton (enter/select strings → backend sort with one algorithm → display result) first. The org's skeleton-on/off guidance (skeleton-on when scope declares skeleton: on; per-unit checkpoints) applies once chosen.

## Testing Posture

- **Methodology**: test-after
- **Methodology evidence**: The org default for feature scope is test-after (implement each testable layer, then write/run its tests). Given this is a simple deterministic app (sorting), test-after is pragmatic for a first pass while keeping tests present. TDD is possible but not mandated.
- **Ordering**: Implement backend sorting logic and core utilities first, then write unit tests for each algorithm (correctness, step counts) and edge cases; then implement UI wiring and add minimal integration checks as needed.
- **Coverage/tooling (proposed):** Target >= 80% line coverage for core logic (sorting algorithms) as per org guidance for feature scope. Use pytest for unit tests. Run tests in CI before merge (proposed). No BDD feature files unless specified.
- **Scope notes (proposed):** Bugfix/security-patch style regressions not applicable. Focus on correctness and step-count accuracy for bubble, selection, and quick sort.

## Deployment

- **Proposal (to be confirmed):** Deploy on merge to staging (per org default). Production requires separate manual approval (tech lead + product owner sign-off) via the CD platform/environment protection. No continuous production deploy by default. For a local/dev Streamlit app, deployment target may be a simple hosting environment (Streamlit Cloud, container, or internal); specific target to be confirmed. Keep one trunk; no long-lived release branches.

## Code Style

- **Proposal (to be confirmed):** Follow Python idioms (snake_case, type hints where helpful). Use a formatter (Black) and linter (Ruff) if configured; if not present, add minimal config. Prefer small, testable modules (separate `sorting/` module for algorithms, `app.py` for Streamlit UI). Avoid hardcoded secrets. Validate/sanitize inputs minimally (strings from UI). Read project linter config first if it exists (per org guidance).

**Note:** These are proposals based on org defaults and the greenfield project description. They will be refined via the human interview (Step 4) and integrated (Step 5). No team.md edits have been made yet (promotion happens later).