# Rollback Runbook — Streamlit String Sorter

## Sources

- `deployment-pipeline-questions.md` — Q1 D (recreate), Q3 A (no approval), Q4 A (manual rollback via `git revert`), Q5 A (no feature flags).
- `construction/delivery-pipeline/infrastructure-design/infrastructure-specification.md` — rollback is a commit revert; the platform rebuilds from the reverted tree.
- `construction/delivery-pipeline/infrastructure-design/cicd-pipeline.md` — trunk-based squash merges and the push-to-`main` deploy path.
- `construction/ci-pipeline/quality-gates.md` — the checks that should pass again after the revert.

## Scope

Rollback for the production Streamlit app deployed from `main`. It covers a bad application change, a bad dependency change, and a bad workflow change. Database migrations do not exist in this project, so there is no schema rollback step.

## Rollback Triggers

Roll back when any of these is true:

- The deployed app fails to load, crashes on interaction, or returns wrong or unchecked sort results.
- The Streamlit Community Cloud build for a new commit fails and the change needs to be withdrawn rather than fixed forward.
- A dependency change in `requirements.txt` breaks installation or runtime behaviour in production.
- A workflow change causes CI to fail in a way that must be withdrawn immediately.

A failed CI run alone does not require a rollback — the checks do not block deployment and a visibly failed run may be fixed forward.

## Authority

The repository owner decides and executes the rollback. No production approval gate exists (Q3 A), so no additional sign-off is required. Record the decision and the commit reverted in the repository or incident notes.

## Procedure

1. **Identify the offending commit.** On `main`, find the squash commit that introduced the problem:
   ```bash
   git log --oneline -10
   ```
   Confirm it is the change you intend to withdraw, not an unrelated later commit.
2. **Revert on `main`.** Create the revert commit:
   ```bash
   git revert --no-edit <commit-sha>
   ```
   `git revert` is the required mechanism (Q4 A). Do not use `git reset` or force-push on `main`; the trunk history must stay intact.
3. **Push the revert.**
   ```bash
   git push origin main
   ```
4. **Let the platform rebuild.** Streamlit Community Cloud rebuilds from the reverted `main` tree. The previous build keeps serving until the rebuild succeeds.
5. **Verify the revert build.** Complete the checks in "Post-Rollback Verification" below.

### If the revert conflicts

- Resolve the conflict in the revert commit, keeping the intent "restore the pre-change behaviour".
- If several commits combine into the regression, revert the earliest offending squash commit first, then the dependent ones in reverse order.
- If a clean `git revert` is impossible, create a new commit that restores the known-good versions of the affected files, land it through the normal `main` path, and note why a straight revert was not used.
- Never force-push `main` to rewrite history.

## Post-Rollback Verification

1. `git log --oneline -3` shows the revert commit on top of `main`.
2. The GitHub Actions `checks` run for the revert push completes (Black, Ruff, pytest with the coverage floor).
3. Streamlit Community Cloud reports a successful rebuild for the revert commit.
4. The app URL loads; enter or select several strings, run each of the three sorts, and confirm the displayed result matches the sorted order with accuracy and step counts shown.
5. No secrets or credentials appear in logs (none exist, so any appearance is a new problem).

## Communication and Evidence

- Note what broke, the reverted commit SHA, the revert commit SHA, and the verification timestamps in the repository issue or incident notes.
- Link the failed Actions run and the failed platform build (if any) as evidence.
- State plainly that the previous build is serving again once verification passes.

## After the Rollback

- Fix forward on a new short-lived branch and squash-merge it to `main` through the normal path.
- If the failure revealed a missing or weak check, propose it as a follow-up; do not weaken an existing quality gate to make the next merge pass.

## Limits

- There is no automated rollback and no health-check automation. Detection and execution are human-driven, so time-to-recovery depends on someone noticing the failure.
- Rollback restores the previous code and dependencies only. It cannot undo data changes because the app stores no data; if that ever changes, this runbook must add a data-restoration procedure.
- A platform-wide outage is outside this runbook; the Streamlit Community Cloud status is the signal in that case.
