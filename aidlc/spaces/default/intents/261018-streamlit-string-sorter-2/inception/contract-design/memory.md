# Contract Design — Observation Diary

## Interpretations

- The external-API branch of the stage is determined by the requirements (NFR3.4 and out-of-scope list), so no external contract was produced and no question was asked about it.
- Contract 1 encodes decision D10 (non-ASCII passes through unchanged), so the FR1.3 wording and the design are reconciled at contract level, and the requirement text is flagged for its owner.

## Deviations

- The stage's Step 2 question flow was resolved from requirements rather than asked, consistent with the autopilot instruction; the single open point (Python version and pinning) is recorded as an open question, not asked.

## Tradeoffs

- Two contracts, not one: the packaging interface is a real boundary (U2 to U3) and the CI workflow would otherwise reach into U2 source.
- Operation-level contracts (normalize, run_all, check) rather than a schema-only contract, because the boundary is a Python call, not a serialized payload.

## Open questions

- Target Python version and dependency pinning, blocking U3 CI configuration.
- Review finding: `requirements.md` FR1.3 still reads as an ASCII-only restriction; owner to update the wording.
