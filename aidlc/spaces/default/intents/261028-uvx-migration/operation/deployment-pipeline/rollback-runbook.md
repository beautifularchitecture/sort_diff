# Rollback Runbook — uvx-migration

Rollback choice (Q2 X): fix forward or revert. Push a new commit on top of `main`. Never rewrite or force-push `main`.

## When to use
The app fails to load or sort correctly after a push to `main`, and the cause is in the change.

## Steps
1. Find the bad commit: `git log --oneline -5 origin/main`.
2. Choose one:
   - **Revert:** `git revert <bad-sha>`, then `git push origin main`.
   - **Fix forward:** commit the corrective change on a branch, merge it into `main` through the normal CI path, then push.
3. Wait for the CI `checks` job to pass on the new commit.
4. Streamlit Community Cloud rebuilds from the new HEAD. Confirm the app loads and a sample sort returns the expected output.

## Notes
- A push to `main` deploys automatically, so a rollback takes effect only after CI and the platform rebuild finish.
- Do not use `git reset` or force-push on `main`. Project rules forbid it.
