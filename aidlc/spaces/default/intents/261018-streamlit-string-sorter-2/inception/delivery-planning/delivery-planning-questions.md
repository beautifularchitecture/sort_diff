# Delivery Planning — Questions

## Context

Three Units in a linear chain: U1 sorting-core (library) → U2 playground-ui (ui) → U3 delivery-pipeline (packaging). No walking skeleton (team.md). Team practice: squash-merge to `main`, test-after, auto-deploy to production on merge.

Terms used below:
- **Bolt**: one build pass over one Unit (or a group of Units), ending in something that runs and can be checked.
- **Walking skeleton**: a thin end-to-end slice built first to prove the pieces connect. The team chose not to use one.
- **Confidence hypothesis**: what shipping a Bolt will prove that we do not yet know.

## Strategic Questions (each with a recommended default)

**Q1. What should we build first?**
- A. Riskiest parts first
- B. Most valuable parts first
- C. Thin end-to-end slice first
- **Recommended: B.** The app is small and its risks (non-ASCII input, step-count definition) sit inside U1, which is already first in the chain. Value (the three sorts with correct counts) is also in U1.

**Q2. Score the work with a formal model (WSJF)?**
- A. Yes, with weights
- B. No, use the linear chain as the order
- **Recommended: B.** The DAG is already linear, so scoring cannot change the order.

**Q3. How big is one Bolt?**
- A. One Unit per Bolt
- B. Several Units per Bolt
- **Recommended: A.** Three Units, three Bolts, each with a clear done check.

**Q4. Can Bolts be built at the same time?**
- A. Yes
- B. No, one after another
- **Recommended: B.** The DAG allows no parallelism.

**Q5. What outside this team could hold us up?**
- Recommended answer: one item. A Streamlit Community Cloud account and the app's deploy connection, needed by U3 before US5.2 can be verified. It blocks U3 only. If it slips, U1 and U2 proceed and U3 waits.

**Q6. What worries you most, so we tackle it early?**
- Recommended answer: the step-count definition. FR4.1 (loop iterations) and FR4.2 (element comparisons) are not reconciled, and the contract review flagged it. Resolving it in Functional Design for U1 comes before any counting code.

## Construction Settings

**Q7. Construction iteration.**
- A. Unit-major: each Unit's design and code finish before the next Unit starts
- B. Stage-major: each stage runs across all Units first
- **Recommended: A (unit-major, serial).** Matches the linear chain and keeps each Unit verifiable on its own.

**Q8. Construction staffing.**
- A. Run Construction from this session (AI builds each Unit)
- B. Each team owns a Unit
- **Recommended: A.** One team and one session; no team ownership is needed.

**Q9. Construction verification command.**
- The project has no runnable check yet (greenfield). The protocol allows deferring the selection until the first Unit exists, with the first checkpoint asking before any verification runs.
- **Recommended: defer.** When U1 is built, the proposed command is `pytest`, and you approve it at that checkpoint. No placeholder is recorded.

## Reply

Reply "accept all defaults" to take every recommendation above, or name the questions you want changed (for example, "Q7 stage-major").

[Answer]: Accept all defaults

## Consolidated Summary Confirmation

Here is the combined summary of this stage's decisions. Please confirm it.

**Bolts (3, in order)**: Bolt 1 sorting-core (U1: sorts, counts, accuracy; pytest, 80% coverage floor). Bolt 2 playground-ui (U2: the single page, FR6.1 warning, local run). Bolt 3 delivery-pipeline (U3: CI and deploy on merge to `main`).

**Sequencing**: value-first, constrained by the linear chain. No walking skeleton. No WSJF scoring.

**Staffing and settings**: run from this session by the AI developer agent; no team ownership; unit-major, serial; collaborators off.

**Verification command**: deferred. `pytest` will be proposed at Bolt 1's checkpoint for approval.

**Risks carried**: step-count definition (FR4.1 vs FR4.2), FR1.3 wording vs D10, Python version and pinning, Streamlit Cloud account.

**Phase check**: PASS across the three Inception traceability files.

[Answer]: Looks correct
