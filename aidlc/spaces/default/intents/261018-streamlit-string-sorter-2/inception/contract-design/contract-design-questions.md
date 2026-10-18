# Contract Design — Questions & Decisions

## Sources

- `inception/units-generation/unit-of-work.md` and `unit-of-work-dependency.md` (U1 → U2 → U3)
- `inception/domain-design/components.md` (entity shapes)
- `inception/requirements-analysis/requirements.md` (NFR3.4, out-of-scope list)

## Applicability

Execute. There is an inter-unit boundary (U2 calls U1). No external API exists: the requirements exclude external integrations and public APIs.

## Decisions (made under full autopilot; human confirms at summary confirmation)

- **D1. External API surface.** None. Determined by NFR3.4 and the out-of-scope list.
- **D2. Mechanism for U1 → U2.** Synchronous in-process Python calls. The app is a single process, and one button press drives one request cycle.
- **D3. Contract ownership.** U1 owns the sorting-core API. U2 owns the packaging interface. Both changes ship in one squash-merged change.
- **D4. Versioning.** No semantic versioning policy, because there are no external consumers. A `version` field is recorded for traceability.
- **D5. Error, timeout, retry.** Errors are limited to caller defects (`TypeError`, `ValueError`). Timeouts and retries do not apply in-process.
- **D6. `run_id` ownership.** `InputProcessor.normalize` generates it, which closes the Domain Design review finding about the missing generator.
- **D7. Empty input at the contract.** `run_all` returns three empty results rather than raising. The FR6.1 warning is shown by U2 before the call, so the contract does not decide the user message.

## Ambiguity Analysis

One genuinely open point remains: the target Python version and dependency pin strategy. It blocks only U3's CI configuration and is recorded as an open question in `contract-summary.md`. Everything else is resolved.

## Consolidated Summary Confirmation

Here is the combined summary of this stage's decisions. Please confirm it.

**Contracts (2)**: C1 sorting-core API (U1 → U2, in-process, operations normalize / run_all / check). C2 app packaging interface (U2 → U3, entry script `app.py`, `requirements.txt`, the run, test, and lint commands).

**External boundaries**: none (requirements exclude them).

**Ownership**: U1 owns C1; U2 owns C2; changes to either ship together.

**Open**: target Python version and dependency pinning, which blocks the CI configuration in U3.

[Answer]: Looks correct
