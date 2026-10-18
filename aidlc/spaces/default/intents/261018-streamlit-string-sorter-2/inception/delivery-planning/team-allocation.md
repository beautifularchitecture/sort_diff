# Team Allocation

## Summary

- **Team count:** one (the human owner)
- **Construction staffing:** run from this session. The AI developer agent (`aidlc-developer-agent`) builds each Bolt. No team ownership is recorded, so no per-team approvals apply.
- **Program Board:** not needed, because there is one team and one owner.
- **Collaborators:** off for this scope. Each stage runs with its lead agent only.

## Bolt-to-Owner Assignment

| Bolt | Unit | Owner | Mode |
|---|---|---|---|
| Bolt 1 | U1 sorting-core | aidlc-developer-agent (AI), reviewed by the human at each checkpoint | Unit-major, serial |
| Bolt 2 | U2 playground-ui | aidlc-developer-agent (AI), reviewed by the human at each checkpoint | Unit-major, serial |
| Bolt 3 | U3 delivery-pipeline | aidlc-developer-agent (AI), reviewed by the human at each checkpoint | Unit-major, serial |

## Human Responsibilities

- Approve each Bolt's stage gates and summary confirmations.
- Provide the Streamlit Community Cloud account and deploy connection before Bolt 3 (see `external-dependency-map.md`).
- Approve the verification command when the first Unit exists (deferred, per Q9).

## Terms

- **Mob:** a group of people and agents working on one piece of work at once. Not used here, because collaborators are off.
- **Checkpoint:** a human review point at the end of a Bolt, before the next Bolt starts.
