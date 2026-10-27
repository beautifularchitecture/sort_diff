# Runbooks — incident-response

Scope: a single Streamlit app with no database, queue, or outbound calls. Automation: none; every step is manual.

## RB-1: Deploy build failure (Streamlit Community Cloud)
- **Detect:** Streamlit app dashboard shows a failed rebuild after a push to `main`.
- **Triage:** Open the build log in the Streamlit app management view. Identify the failing step (dependency install, import error, Python version).
- **Mitigate:** Revert the offending commit on `main` (`git revert <sha>`, push). Streamlit rebuilds from the new HEAD.
- **Verify:** Rebuild succeeds; the app loads and sorts a sample list.

## RB-2: CI failure on `main`
- **Detect:** GitHub Actions run for `main` fails (`checks` job: Black, Ruff, pytest).
- **Triage:** Read the failing gate's log in the Actions run summary.
- **Mitigate:** Fix forward with a small commit, or revert the offending commit. Re-run the workflow.
- **Verify:** `checks` job is green on `main`.

## RB-3: App fails to load
- **Detect:** The owner's app-load check fails, or the Streamlit dashboard shows the app as errored.
- **Triage:** Check the Streamlit platform logs (stdout/stderr) for the running process.
- **Mitigate:** Redeploy the last good commit: `git revert` the bad change on `main` (or reset the deployment target to the last good commit, if the platform supports it). Streamlit redeploys on push.
- **Verify:** App loads; a sample sort returns the expected sorted list and step counts.

## Notes
- No paging or on-call. The repository owner runs every runbook.
- No automated remediation. No RTO/RPO target; recovery means redeploying the last good commit.
