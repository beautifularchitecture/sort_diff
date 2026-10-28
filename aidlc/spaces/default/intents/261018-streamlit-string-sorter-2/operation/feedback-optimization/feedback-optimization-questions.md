# Feedback & Optimization Questions

## Q1: SLO compliance
No SLO is defined (Observability Setup Q2). How should compliance be reported?

A. Report the deploy and CI results only; no SLO burn rate (Recommended)
B. Define an SLO now (give the target and window)
X. Other (please specify)

[Answer]: A

## Q2: Cost
The app runs on Streamlit Community Cloud and GitHub Actions with no paid AWS resources. Should cost be reviewed?

A. No cost review; no paid resources in use (Recommended)
B. Review cost on the platform accounts (name them)
X. Other (please specify)

[Answer]: A

## Q3: Drift
The deployment has no infrastructure-as-code state to drift from. What should be checked?

A. Compare the deployed commit with `main` HEAD and the dependency pins in `requirements.txt` (Recommended)
B. Add another check (describe it)
X. Other (please specify)

[Answer]: A

## Q4: Next iteration
Should the feedback loop feed a new Ideation cycle?

A. No new cycle; record the findings and close the workflow (Recommended)
B. Start a new Ideation cycle (describe the next change)
X. Other (please specify)

[Answer]: A

## Consolidated Summary Confirmation

- Q1 SLO compliance: A — report deploy and CI results only; no SLO burn rate.
- Q2 Cost: A — no cost review; no paid resources in use.
- Q3 Drift: A — compare the deployed commit with `main` HEAD and the `requirements.txt` pins.
- Q4 Next iteration: A — no new cycle; record findings and close the workflow.

Does this all look correct before I generate the artifacts?
- Looks correct
- Request changes

[Answer]: Looks correct
