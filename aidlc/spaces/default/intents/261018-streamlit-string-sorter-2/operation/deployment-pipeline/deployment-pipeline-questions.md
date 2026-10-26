# Deployment Pipeline Questions

## Q1: Deployment strategy
What deployment strategy should we use for this application?
A. Blue/Green
B. Canary
C. Rolling
D. Recreate
X. Other (please specify)

[Answer]: D

## Q2: Environment promotion gates
What environment promotion approach should we take?
A. Direct to production (no staging) - matches current team practice
B. Dev → Staging → Production with gates
C. Dev → Production only with approval gate
X. Other (please specify)

[Answer]: A

## Q3: Approval workflow for production
What approval is needed before production deployment?
A. No approval required (fully automated) - matches team.md continuous deployment
B. Manual approval required
C. Approval from specific roles only
X. Other (please specify)

[Answer]: A

## Q4: Rollback procedure
How should rollbacks be handled?
A. Manual rollback via git revert
B. Automated rollback on health check failure
C. Both manual and automated
X. Other (please specify)

[Answer]: A

## Q5: Feature flag strategy
Do we need feature flags for this deployment?
A. No feature flags needed
B. Yes, use CloudWatch Evidently
C. Yes, use AWS AppConfig
D. Yes, custom solution
X. Other (please specify)

[Answer]: A

## Consolidated Summary Confirmation
- Q1 Deployment strategy: D — Recreate
- Q2 Environment promotion gates: A — Direct to production (no staging)
- Q3 Approval workflow for production: A — No approval required (fully automated)
- Q4 Rollback procedure: A — Manual rollback via git revert
- Q5 Feature flag strategy: A — No feature flags needed

Does this all look correct before I generate the artifact?
- Looks correct
- Request changes

[Answer]: Looks correct
