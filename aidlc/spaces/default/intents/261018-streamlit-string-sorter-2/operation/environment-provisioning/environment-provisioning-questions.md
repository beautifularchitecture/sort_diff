# Environment Provisioning Questions

## Q1: Current provisioning state
What is the current state of the Streamlit Community Cloud app described in the infrastructure design? The inventory and validation report need to distinguish an app that already exists from one that still has to be created.

A. Already created and connected to this repository, and live
B. Created but not yet connected to this repository
C. Not created yet
X. Other (please specify)

[Answer]:B

## Q2: Production URL
What production URL should the environment inventory and validation report record for the deployed app? If it is not available yet, I will record it as pending rather than guess.

A. I will paste the platform-assigned URL in my reply
B. Not available yet — record it as pending
C. There is no public URL; validate statically only
X. Other (please specify)

[Answer]: https://sortdiff-nnthjumkztx7gfdla6vmlz.streamlit.app/

## Q3: Validation depth
How should I validate the environment in this stage? I can inspect the repository and workflow files directly, but I cannot sign in to the Streamlit account; a live check needs the deployed URL.

A. Static validation only (repository, workflow, and recorded platform configuration)
B. Static validation plus a live HTTP smoke test of the deployed URL
C. Live smoke test only
X. Other (please specify)

[Answer]:A

## Q4: Absent infrastructure confirmation
The infrastructure design records no VPC, subnets, security groups, NACLs, secret store, or cross-account connectivity. Should the validation report record all of these as not applicable? I am asking so the report states a confirmed fact rather than an assumption.

A. Yes — record them as not applicable; none exist
B. No — one or more exist (describe them in your reply)
X. Other (please specify)

[Answer]: A

## Consolidated Summary Confirmation

- Q1 Current provisioning state: B — Created but not yet connected to this repository
- Q2 Production URL: https://sortdiff-nnthjumkztx7gfdla6vmlz.streamlit.app/ (provided; live status not verified because static-only validation was chosen)
- Q3 Validation depth: A — Static validation only
- Q4 Absent infrastructure: A — Record VPC, subnets, security groups, NACLs, secret store, and cross-account connectivity as not applicable

Does this all look correct before I generate the artifact?
- Looks correct
- Request changes

[Answer]: Looks correct
