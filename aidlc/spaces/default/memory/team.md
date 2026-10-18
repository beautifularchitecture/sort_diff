# Team-Level Rules

> This team's affirmed practices and corrections. Loaded after `org.md` as
> strict-additive guidance; contradictions with broader policy are rejected.
> Populated by the practices-discovery affirmation gate. Edit at the gate,
> not directly.

## Way of Working

- We use trunk-based development: every change lands on a short-lived branch off `main` and is squash-merged back into `main` within a day or two, with the branch/Bolt name as the commit message.
- No long-lived branches and no release branches; if multiple environments are ever needed, we gate releases via tags or environment-specific deployment configs, never via long-lived release branches.
- Construction worktrees branch from `main` (`--base main`) and merge back to `main` with the squash strategy (`--target main --strategy squash`).

## Walking Skeleton

- This intent does **not** build a walking skeleton. The human chose to go straight at the three sorting algorithms and the Streamlit UI rather than proving a thin end-to-end slice first (interview Q2, answer B).
- No skeleton slice is built before the real features, and no skeleton bootstrap checkpoint applies to this intent; ordinary per-stage approvals follow the workflow's normal policy.

## Testing Posture

- **Methodology**: test-after
- **Methodology evidence**: The human chose "tests after each piece is implemented" in the interview (Q3, answer A — the org default for this scope), so tests are written after each piece of code rather than first.
- **Ordering**: Implement each testable piece — each sorting algorithm, then the UI wiring — and then write and run that piece's tests before moving on to the next piece.
- **Tooling**: pytest for unit tests; the test suite runs in CI before merge.
- **Coverage**: roughly 80% line coverage on the sorting logic (the three algorithms), held as a floor in Build and Test and never weakened to make a step pass.
- **Scope notes**: focus on correctness and step-count accuracy for bubble sort, selection sort, and quick sort; no BDD feature files unless a later stage introduces them.

## Guard Policy

<!-- Affirmed by the team. Mode: strict, relaxed, or off. Strict here holds for every intent, whatever one person asks in chat; relaxed or off here applies to every intent whose policy came from its scope, unless project.md or the person sets another; changing this line changes it. A section under the retired Change Control heading, written by an earlier release, is still read. -->

## Deployment

- We deploy to production automatically on every merge: continuous deployment, no staging tier and no manual production-approval gate between a green `main` commit and production.
- This deliberately departs from the org default (deploy on merge to *staging*, production gated by a separate manual approval). The human chose it explicitly in the interview (Q4, answer B); `memory/org.md` frames continuous production deployment as a team decision, and this is that decision.
- The deployment target itself (Streamlit Cloud, container, or internal hosting) is not yet chosen and stays open for Requirements Analysis; this practice says *when* we deploy, not *where*.

## Code Style

- Python defaults: Black as the formatter, Ruff as the linter, snake_case naming.
- We follow idiomatic Python style, with type hints where they help, and read the project's linter/formatter configuration first when making style judgments — this team's configuration is Black + Ruff.
- Lint and format checks run in CI before merge and a failure blocks the merge; no project-wide rename rules beyond snake_case.
## Forbidden

<!-- Team-specific forbidden patterns -->

## Mandated

<!-- Team-specific mandates -->

## Corrections

<!-- Self-learning loop appends here. -->
