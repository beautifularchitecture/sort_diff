# Incident Response Questions

## Q1: Most likely failure modes
This app is a single Streamlit process with no database, queue, or outbound calls. The likely failures are a failed deploy build, a CI failure on `main`, or the app failing to load. Which should the runbooks cover?

A. All three: deploy build failure, CI failure, and app fails to load (Recommended)
B. Deploy build failure only
C. Add others (describe them)
X. Other (please specify)

[Answer]: A

## Q2: Escalation path and on-call
No paging or on-call exists (Observability Setup Q6). Who handles an incident?

A. Repository owner handles everything, no escalation (Recommended)
B. Repository owner plus a named backup (give the name and channel)
X. Other (please specify)

[Answer]: A

## Q3: Automated remediation
What may be automated?

A. No automation; manual steps only, documented in runbooks (Recommended)
B. Automate a redeploy or rerun of the CI workflow (describe the trigger)
X. Other (please specify)

[Answer]: A

## Q4: Communication during an incident
Where should incident status be posted?

A. GitHub issue in the repository (Recommended)
B. Email to the owner
C. Other channel (name it)
X. Other (please specify)

[Answer]: A

## Q5: Recovery targets (RTO/RPO)
The app stores no data (no persistent storage). What recovery targets apply?

A. No RTO/RPO; recovery means redeploy the last good commit (Recommended)
B. Set an RTO target (give the time)
X. Other (please specify)

[Answer]: A

## Consolidated Summary Confirmation

- Q1 Failure modes: A — deploy build failure, CI failure, and app fails to load.
- Q2 Escalation: A — repository owner handles everything, no escalation.
- Q3 Automation: A — no automation; manual steps only, documented in runbooks.
- Q4 Communication: A — GitHub issue in the repository.
- Q5 Recovery targets: A — no RTO/RPO; recover by redeploying the last good commit.

Does this all look correct before I generate the artifacts?
- Looks correct
- Request changes

[Answer]: Looks correct
