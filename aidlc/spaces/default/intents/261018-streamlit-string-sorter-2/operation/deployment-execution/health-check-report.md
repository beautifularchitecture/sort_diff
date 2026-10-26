# Health Check Report — Streamlit String Sorter

## Sources

- `operation/deployment-execution/deployment-log.md` — build timeline, release commit, platform evidence.
- `operation/deployment-execution/smoke-test-results.md` — authenticated functional smoke test.
- `operation/environment-provisioning/environment-inventory.md` — platform-managed hosting, no dedicated health route.
- `construction/delivery-pipeline/infrastructure-design/monitoring-design.md` — the two deploy signals: Actions result and platform build status.
- Streamlit build log supplied by the app owner.
- GitHub Actions run `40392449969` for commit `2952504`.

## Health Signals

| Signal | Source | Result | Status |
|---|---|---|---|
| Platform build | Streamlit Community Cloud | Uvicorn started on `:8501` at 09:37:33 UTC | Pass |
| Platform rebuild | Streamlit Community Cloud | `🔄 Updated app!` at 20:04:57 UTC | Pass |
| CI checks | GitHub Actions `CI / checks` | Success at 20:05:35 UTC | Pass |
| App server | Streamlit build log | Uvicorn server started | Pass |
| Authenticated app load | App owner | App opened and accepted input | Pass |
| Functional smoke test | App owner | All three sorts returned sorted, accuracy-checked results | Pass |
| Unauthenticated app access | HTTP check | `HTTP/2 303` to `share.streamlit.io/-/auth/app` | Not publicly reachable |
| Health endpoint | `/_stcore/health` | `303` to Streamlit login | Auth-gated |
| Dedicated application health route | Repository | None; single Streamlit process | Not applicable |
| Automated post-deploy smoke | CI workflow | None | Not configured |
| Dashboards, alerts, SLOs | Platform / repository | None | Not configured |

## Assessment

The deployed commit is healthy for the authenticated owner:

- The platform built `2952504` and started the app.
- A subsequent rebuild completed successfully.
- GitHub Actions passed for the same commit.
- The owner's post-deployment smoke test passed.

Public availability is **not** established. The unauthenticated request and the
`/_stcore/health` probe both return `303` to the Streamlit login flow, so no
public health signal or independent smoke test is possible until the app's
sharing setting is changed. This is a visibility configuration, not a failed
build or a crashed process.

There is no dedicated health endpoint, no pipeline-emitted metric, no dashboard,
no alert, and no SLO. The only deploy signals are the GitHub Actions run and the
Streamlit platform build status, as recorded in `monitoring-design.md`.

## Risks

| Risk | Current state | Mitigation |
|---|---|---|
| App is not publicly reachable | Unauthenticated requests redirect to login | Change the Streamlit sharing setting; re-run the public health check |
| No automated detection of a broken deploy | Manual smoke test only | Owner check after each rebuild; manual rollback runbook |
| Platform runtime differs from CI | Python 3.14.9 on the platform; CI pins 3.12 | CI still passed at 3.12; keep platform and CI versions in mind for future changes |
| Unpinned dependencies | `requirements.txt` uses minimum ranges; platform resolved latest compatible versions | Confirm the build after dependency changes; rollback covers a bad dependency |
| Manual rollback only | No automated health trigger | Use `rollback-runbook.md`; the platform keeps the last good build until a rebuild succeeds |

## Verdict

**Healthy for authenticated users; public health verification pending.** The
build, CI run, server start, and owner smoke test all passed. The app does not
yet expose a public health signal because it is private.
