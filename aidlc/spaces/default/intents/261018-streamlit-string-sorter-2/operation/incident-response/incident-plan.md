# Incident Response Plan — incident-response

## Scope
Single Streamlit app deployed on Streamlit Community Cloud from `main`. Failure modes covered: deploy build failure, CI failure on `main`, app fails to load (see `runbooks.md`).

## Roles
- **Owner (incident lead):** the repository owner. Handles triage, mitigation, and communication for every incident.
- No paging, on-call rotation, or escalation path.

## Severity
Single level. Any failure of the three covered modes is handled as a normal incident; response is best-effort during the owner's working hours.

## Process
1. Detect via the Streamlit dashboard or GitHub Actions.
2. Open a GitHub issue in the repository titled `Incident: <short description>`.
3. Run the matching runbook in `runbooks.md`.
4. Verify recovery, then close the issue with a one-line summary of cause and fix.

## Communication
All incident status is posted as comments on the GitHub issue.

## Recovery
No RTO or RPO targets. Recovery means redeploying the last good commit on `main`.

## Post-incident
No formal postmortem is required. The owner adds a one-line note to the closing issue describing the cause and the prevention step, if any.
