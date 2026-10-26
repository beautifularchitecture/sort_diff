# Deployment Execution Questions

## Q1: Release candidate
Which commit should this deployment represent? The current `main` HEAD is `7e95813`; the only uncommitted changes in the working tree are AI-DLC workflow records, not application code.

A. Deploy `main` HEAD `7e95813` as-is; leave the AI-DLC record changes uncommitted (Recommended)
B. Commit and push the AI-DLC record changes too, then deploy the new commit
C. Do not deploy yet — record the deployment as pending
X. Other (please specify)

[Answer]: A

## Q2: Platform connection
The environment inventory records the Streamlit Community Cloud app as created but not connected to this repository. Connecting it is a manual console action I cannot perform. What is its current state?

A. I will connect it now and confirm when the first platform build succeeds (Recommended)
B. It is already connected — correct the inventory
C. Leave it unconnected; record this deployment as blocked pending connection
X. Other (please specify)

[Answer]: A

## Q3: Execution responsibility
I cannot sign in to the Streamlit console or trigger the platform rebuild; deployment is platform-owned. How should execution and evidence be recorded?

A. You perform the platform steps and paste the build result; I record it and verify statically (Recommended)
B. Record the deployment as not executed, with the manual steps and pending evidence
C. I run a local pre-deployment smoke test only, and record the production deployment as pending
X. Other (please specify)

[Answer]: A

## Q4: Pre-deployment checks, migrations, and dependent services
Build and Test recorded 116 tests passing, 100% `sorting_core` coverage, and clean Black and Ruff checks. This project has no database migrations. The only external dependencies are GitHub, PyPI, and Streamlit Community Cloud.

A. All confirmed — checks pass, no migrations, no dependent services to wait on (Recommended)
B. Something differs (describe it in your reply)
X. Other (please specify)

[Answer]: A

## Q5: Deployment window
When should the deployment happen?

A. Now (Recommended)
B. Schedule it for a later window (give the date and time in your reply)
X. Other (please specify)

[Answer]: A

## Deployment Evidence Recorded During Execution

- The app owner supplied the Streamlit build log. It shows a successful build (`Uvicorn server started on :::8501`) and a later successful rebuild (`🔄 Updated app!` at 20:04:57).
- The remote `main` HEAD at that rebuild was `2952504` ("Added Dev Container Folder", 2026-10-26T20:04:52Z), not `7e95813`. The local workspace was one commit behind.
- `git diff 7e95813..2952504` shows only `.devcontainer/devcontainer.json` added (33 lines). Application code is unchanged, so the deployed release candidate is `2952504` and Q1's intent — deploy `main` HEAD as-is — is satisfied by the actual remote HEAD.
- Unauthenticated requests to the app URL redirect to `share.streamlit.io/-/auth/app`; the app is private. This is a visibility setting, not a build failure.

## Q6: Post-deployment smoke test
The app owner ran the smoke test while signed in.

A. Pass — app loads and all three sorts work
B. Fail — describe what happens in your reply
C. Not tested yet
X. Other (please specify)

[Answer]: A

## Q7: App visibility
Should the app stay private, or be made publicly reachable? The current unauthenticated check still redirects to Streamlit login.

A. Keep private
B. Make public — then I can verify the URL and health endpoint directly
X. Other (please specify)

[Answer]: B

## Consolidated Summary Confirmation

- Q1 Release candidate: A — deploy `main` HEAD as-is. Evidence correction: remote `main` was `2952504` (devcontainer-only change), so `2952504` is the deployed commit.
- Q2 Platform connection: A — app owner connected it; the Streamlit build succeeded at 09:37:33 and rebuilt at 20:04:57.
- Q3 Execution responsibility: A — app owner performed the platform steps and supplied the build log; I verified statically and over HTTP.
- Q4 Pre-deployment checks: A — 116 tests pass, 100% `sorting_core` coverage, Black/Ruff clean; no migrations; dependencies available.
- Q5 Deployment window: A — deployed now.
- Q6 Smoke test: A — pass; owner confirmed the app loads and all three sorts show sorted output, accuracy, comparisons, and swaps.
- Q7 Visibility: B — make public. Current verification still redirects unauthenticated requests to Streamlit login, so public access is not yet effective.
- Deployment result: build succeeded and the app is running for the authenticated owner. Public access remains pending. No automated post-deploy smoke or dedicated health endpoint exists.

Does this all look correct before I generate the artifacts?
- Looks correct
- Request changes

[Answer]: Looks correct
