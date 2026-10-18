## Evidence inspected/inferred

- **Project state** (from `aidlc/spaces/default/intents/261018-streamlit-string-sorter-2/aidlc-state.md`): Greenfield; scope feature; depth Standard; test strategy Standard; collaborators off (lead-only). Languages/Frameworks/Build System listed as Unknown. Ideation complete; currently in inception, executing practices-discovery. Reverse-engineering skipped.
- **Project description**: Streamlit app that takes strings (entered or selected from a list), runs through sorting algorithms, checks accuracy and number of steps, first step only bubble/selection/quick sort, button triggers backend sort, results shown in frontend. Simple.
- **Default-practice source (org.md)**: Sections read — Way of Working (trunk-based, short-lived feature branches off main, squash-merge), Walking Skeleton (scope-dependent, skeleton-on when scope declares skeleton: on), Testing Posture (feature scope defaults: test-after, 80% line coverage for core logic, CI before merge), Deployment (deploy on merge to staging, prod gated by manual approval), Code Style (defer to project config: Black/Prettier, Ruff/ESLint, idiomatic naming).

## Reasoning for proposed practices

- **Way of Working**: Align to org trunk-based defaults. Feature scope + greenfield simple app; short-lived branches fit.
- **Walking Skeleton**: Skeleton ceremony is scope-dependent in org guidance; feature scope doesn't force it. Given "simple Streamlit application" with 3 algorithms, proposing not required initially; leave open to human confirmation.
- **Testing Posture**: Org feature default is test-after + 80% coverage on core logic. Methodology explicitly specified in output; ordering chosen to test algorithms (core logic) after implementation with clear focus on accuracy/step counts. Pytest is natural for Python/Streamlit logic.
- **Deployment**: Org default (staging on merge, prod manual approval). Streamlit target TBD but practice is clear.
- **Code Style**: Python idioms; Black/Ruff proposed as common for Python; org states read project linter config first.

## Unresolved uncertainties

- **Deployment target**: Streamlit Cloud, Docker container, internal hosting? May affect deployment pipeline details later.
- **Algorithm details**: How step counts are defined (comparisons/swaps/operations count)? Needs clarification for accurate testing.
- **Word list source**: Static list in UI, file, or embedded? Simple approach preferred.
- **Branching/CI**: Repo may or may not have existing CI; will follow org defaults if absent.
- **Walking skeleton preference**: Human may prefer skeleton-on even if not required.

These will be resolved in the interview (Step 4). No team.md or project.md edits performed.