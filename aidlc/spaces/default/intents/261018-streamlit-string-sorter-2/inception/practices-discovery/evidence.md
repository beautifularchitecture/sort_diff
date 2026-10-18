## Evidence inspected / inferred

- **Project type**: Greenfield. No application code exists yet in the workspace, so no code, git history, or CI/deployment configuration was scanned; all brownfield upstream artifacts (`code-structure`, `technology-stack`, `dependencies`, `code-quality-assessment`, `architecture`, `business-overview`) are conditional on brownfield and are absent by design.
- **Default-practice source**: `aidlc/spaces/default/memory/org.md` — the five matching sections were read as suggested defaults, not established team facts: `## Way of Working` (trunk-based, short-lived branches off `main`, squash-merge), `## Walking Skeleton` (scope-dependent skeleton ceremony), `## Testing Posture` (feature-scope default: test-after ordering, 80% line-coverage floor, CI before merge), `## Deployment` (deploy on merge to staging, production gated by a separate manual approval; continuous production deployment named as a team decision), `## Code Style` (defer to project formatter/linter config — Black/Prettier, Ruff/ESLint, idiomatic naming).
- **Re-run context**: `aidlc/spaces/default/memory/team.md` and `project.md` contain no affirmed content yet — every section is an empty template, so there was no prior team baseline to integrate.
- **Other inputs read**: `aidlc-state.md` (scope `feature`, depth Standard, test strategy Standard, collaborators off → lead-only run), the initial project description (Streamlit app: strings entered or picked from a list, sorted by bubble/selection/quick sort, accuracy and step counts checked, sort triggered by a button, results shown in the frontend), and the completed interview `practices-discovery-questions.md`.
- **Lead-only run**: `support_agents` was empty, so Step 3 ran no spoke reviews and no contribution files exist; this lead's draft stood as the practices and the interview resolved them. Only the lead edited the four declared artifacts.
- **Timestamp provenance**: `aidlc engine now` → `2026-10-18T06:54:55Z`; `git rev-parse HEAD` → `40c7e10148ce73df200ce0c02ad1371602c327c3`.
- **No memory promotion yet**: `memory/team.md` and `memory/project.md` were not edited — promotion happens later via `aidlc engine state practices-promote` at the affirmation gate.

## Interview decisions (interview closed)

| # | Area | Human's choice | Effect |
|---|------|----------------|--------|
| Q1 | Way of Working | **A** — short-lived branch off `main`, squash-merged into `main` within a day or two | Affirms the org default; recorded in `## Way of Working`. |
| Q2 | Walking skeleton | **B — No** — go straight at the three sorting algorithms and the UI | This intent builds no walking skeleton; recorded in `## Walking Skeleton`. |
| Q3 | Testing | **A** — tests after each piece is implemented, pytest, roughly 80% line coverage on the sorting logic | `Methodology: test-after`, ordering and coverage recorded in `## Testing Posture`. |
| Q4 | Deployment | **B — deploy to production automatically on every merge** | Continuous deployment to production on merge recorded in `## Deployment`. |
| Q5 | Code Style | **A** — Python defaults: Black formatter, Ruff linter, snake_case | Recorded in `## Code Style`. |
| — | Consolidated summary | **Looks correct** | Draft practices accepted as summarized. |
| — | Assumptions | **A — Accept assumptions** | Assumption 1: "org default" means the framework's shipped defaults in `memory/org.md` (no team practices existed yet). Assumption 2: no deployment target is named yet — Streamlit Cloud / container / internal hosting stays open for Requirements Analysis. |

### Departure from the org default (deliberate, human's own choice)

- **Q4 departs from `memory/org.md`.** The org default is *deploy on merge to staging, production gated by a separate manual approval*; `org.md` explicitly says continuous production deployment is a team decision, not a framework default. The human chose option B — automatic production deployment on every merge — in the open interview. This is recorded as the team's affirmed practice in `## Deployment`, with the departure stated there rather than silently replacing the default.

## Unresolved uncertainty

- **Deployment target (primary)**: still unnamed — Streamlit Cloud, container, or internal hosting. The affirmed practice fixes *when* production deploys (on every merge), not *where*; the target stays open for Requirements Analysis and will shape the deployment pipeline details.
- Deferred product details that surfaced during drafting but belong to Requirements Analysis, not to this stage: how step counts are defined (comparisons vs swaps vs operations), and the source of the selectable word list (static, file, or embedded).
