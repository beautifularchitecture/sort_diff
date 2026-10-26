# Project-Level Rules

> Project-specific specialisation and corrections. Loaded after `org.md` and
> `team.md` as strict-additive guidance; contradictions with broader policy
> are rejected. Populated by practices-discovery and the self-learning loop.
>
> Use sparingly: most teams don't need a project layer. Reach for it
> only when this specific project needs stable, durable guidance beyond the
> team practice (for example, package-specific release checks or an additional
> regression suite for a legacy component).

## Way of Working

<!-- Project-specific specialisation. Example: -->
<!-- This monorepo requires package-scoped branch names and a package owner -->
<!-- review in addition to the team's normal merge policy. -->

## Walking Skeleton

<!-- Project-specific specialisation. Example: -->
<!-- The walking skeleton must exercise the legacy service adapter as well -->
<!-- as the new service boundary. -->

## Testing Posture

<!-- Project-specific specialisation. -->

## Guard Policy

<!-- Project-specific. Mode: strict, relaxed, or off. Strict here holds for every intent, whatever one person asks in chat; relaxed or off here applies to every intent whose policy came from its scope, unless the person sets another; changing this line changes it. A section under the retired Change Control heading, written by an earlier release, is still read. -->

## Deployment

<!-- Project-specific specialisation. -->

## Code Style

<!-- Project-specific specialisation. -->

## Tech Stack

<!-- Technology choices locked for this project. -->

## Decided

<!-- Decisions made in earlier stages that should not be re-asked. -->
<!-- Format: DECIDED: [decision] (Stage [slug], [date]) -->

## Scope Overrides

<!-- Custom scope rules for this project. -->

## Forbidden

<!-- Populated by practices-discovery affirmation gate. -->
<!-- Format: NEVER [behavior] (affirmed [date]) -->
<!-- Example: NEVER throw exceptions across service layer boundaries (affirmed 2026-05-17) -->

- NEVER use a sorting algorithm other than bubble sort, selection sort, or quick sort in this first step. (affirmed 2026-10-18)

## Mandated

<!-- Populated by practices-discovery affirmation gate. -->
<!-- Format: ALWAYS [behavior] (affirmed [date]) -->
<!-- Example: ALWAYS use Result<T,E> for fallible operations in service layer (affirmed 2026-05-17) -->

- ALWAYS check every sort result for accuracy against the expected result and report the number of steps taken (accuracy and step counts are stated requirements of this app). (affirmed 2026-10-18)

- ALWAYS run the sort in the backend when the UI button is pressed and return the result to the frontend. (affirmed 2026-10-18)

- ALWAYS deploy to production automatically whenever a change merges to `main` (the human's affirmed choice, departing from the org default). (affirmed 2026-10-18)

## Corrections

<!-- Project-specific corrections from human feedback. -->
<!-- Format: NEVER/ALWAYS [behavior] (learned [date]) -->
- When local `main` is behind remote, treat the actual remote HEAD as the release candidate if the only difference is non-application configuration; do not force-push shared `main` to match a stale local commit. (learned 2026-10-26) <!-- cid:261018-streamlit-string-sorter-2:deployment-execution:a3a82909b139fcfc1508ccb7356ed10ce5edddf2bf0daf2a4d6b1b888c0cba26 -->
- Accept the app owner's authenticated manual smoke test as post-deploy evidence when the app is private and the orchestrator cannot sign in or drive a browser. (learned 2026-10-26) <!-- cid:261018-streamlit-string-sorter-2:deployment-execution:3237cea350cdd9ac3beec00547d21b8d2fb4baa56112b096f0e1c412a2c6bdcd -->
- When the platform owns deployment and no credential is available, have the app owner perform the console steps and supply the build log. (learned 2026-10-26) <!-- cid:261018-streamlit-string-sorter-2:deployment-execution:d1e37784196c9b2e4f7b5bfadb800cf8c157df77c528811d3be2d18e7793f203 -->
- When an app is private, use build logs, CI results, and owner smoke tests instead of unauthenticated HTTP content checks. (learned 2026-10-26) <!-- cid:261018-streamlit-string-sorter-2:deployment-execution:cc7d96272f959f85085581ad0601c5485fce6634d1e409ac0492c178ad552a39 -->
- Never force-push shared `main` to rewind a non-application commit; accept the newer HEAD when the application diff is empty. (learned 2026-10-26) <!-- cid:261018-streamlit-string-sorter-2:deployment-execution:75928cdcdf86a2893ade0d6dacff80aef02ca852226fc3a3c8c165508a0def17 -->
- Do not block a deployment on app visibility; record public access as pending when the app is functional for the authenticated owner. (learned 2026-10-26) <!-- cid:261018-streamlit-string-sorter-2:deployment-execution:915f262f402a965501837a593886952f16a9c81cd2769375e5c1cda1d9f29182 -->
