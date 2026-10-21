# Infrastructure Design Questions — delivery-pipeline (U3)

Settled earlier and not repeated here: GitHub Actions as the CI platform, `ubuntu-latest` runner, Python 3.12 via `actions/setup-python`, `pip install -r requirements.txt` with no lockfile, push-to-`main`-only trigger, one serial job running checkout → install → Black → Ruff → pytest (all gate steps run, job fails at end), no deploy step (Streamlit Community Cloud rebuilds on push), no stored deploy credential, 80% coverage floor in the project pytest configuration, fail the run on test/coverage/lint, no deploy retry.

## Q1: Relationship to U2's CI workflow

U2's infrastructure-design defined a two-job workflow (`tests` + `ui`) triggered on both push to `main` and pull requests against `main`. U3's own confirmed NFR decisions are push-to-`main`-only (no PR trigger) and one serial job. U3 owns the workflow end to end (it consumes Contract 2). How should the two be reconciled?

A. U3 supersedes the workflow: replace U2's trigger and job split with the U3-confirmed model — push to `main` only, one serial job whose steps cover the whole repository (`black --check .`, `ruff check .`, `pytest` over `tests/` including `tests/ui/`). U2's two-job split was a U2 design choice that the later U3-confirmed answers override; record the change.
B. Keep U2's two-job split and PR trigger for the checks, and add U3's packaging concerns on top
X. Other (please specify)

[Answer]:

## Q2: Coverage measurement under a single job

Contract 2 fixes the consumer command as exactly `pytest`, and the coverage floor rides in the project pytest configuration that U1 owns. Under a single job covering the whole repo, how should the floor's coverage scope be declared?

A. The project pytest configuration (`pyproject.toml` addopts) carries `--cov=sorting_core --cov=app --cov-fail-under=80` so one `pytest` run measures both packages; U3 still invokes bare `pytest` per Contract 2.
B. The configuration measures `sorting_core` only, and `app.py` coverage is left to whatever the test suite reaches (no separate floor for the UI entry script).
X. Other (please specify)

[Answer]:

## Q3: Rollback for a broken `main`

With continuous deployment and no staging tier, a commit that imports cleanly but breaks behaviour at runtime still reaches production. What is the rollback posture?

A. Revert the offending commit on `main`; the platform rebuilds from the reverted tree and trunk-based squash history means one revert restores the prior state. No automated rollback step exists.
B. Add an automated rollback step to the workflow that redeploys the previous known-good build on failure
X. Other (please specify)

[Answer]:

## Q4: Monitoring of the pipeline itself

Beyond the GitHub Actions run status and the Streamlit platform build status, what monitoring should the delivery pipeline have?

A. None beyond the platform's own signals: the Actions run result is the correctness signal and the platform rebuild status is the deploy signal. No pipeline-emitted metrics, dashboards, or alerts.
B. Add a periodic (scheduled) health check that pings the deployed app's URL and opens an issue on failure
X. Other (please specify)

[Answer]:

## Q5: Retention of run logs and failures

How long should CI run logs and failure evidence be kept?

A. GitHub's default retention (90 days for Actions logs); no artifact upload or failure-archiving step. Failed runs live in the Actions history until GitHub expires them.
B. Upload test/coverage reports as workflow artifacts on every run so failures can be inspected later
X. Other (please specify)

[Answer]:

---

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifacts?

- Looks correct
- Request changes

[Answer]:
