# Security Requirements — sorting-core (U1)

Derived from inception NFR2 (Simplicity and Usability), NFR3 (Scope and Constraints), and the confirmed answer to NFR Q3.

## Requirements

| ID | Requirement | Source | Verification |
|---|---|---|---|
| NFR2.1 | Input strings are treated as inert plain text. The core never evaluates, executes, or deserializes them. | NFR Q3 (A) | Unit test: strings such as `__import__('os')` and `<script>` are sorted as literal text. |
| NFR2.2 | The core does not produce HTML or markup. Rendering is the caller's responsibility, and the UI must escape output. | NFR Q3 (A) | Code review of `sorting-core` (no HTML/markup output); U2 test confirms escaped rendering. |
| NFR3.2 | The core performs no file I/O, network access, or persistent storage. | NFR3.2, NFR3.4 | Static check: no `open`, `socket`, `requests`, or `urllib` imports in `sorting-core`. |
| NFR3.3 | The core collects no personal data and has no authentication or authorization. | NFR3.3, NFR Q3 (A) | Design review; no user identity inputs exist in the interface. |

## Out of Scope for This Unit

- Authentication, sessions, and access control (NFR3.3): not applicable to a single-page demo with no accounts.
- Maximum string length (NFR Q3 option B and C were not chosen): no per-string length limit is enforced in this unit.
- Input count limit: the classroom cap of 100 strings (NFR Q2 A) is an input-size expectation, enforced by the caller (U2) rather than by the core.

## Threat Considerations

- **Code injection through input**: mitigated by NFR2.1. The core never evaluates input.
- **Resource exhaustion through large input**: low risk at the stated 100-string limit. Quadratic algorithms (bubble and selection) are acceptable at that size. No mitigation beyond the caller's expectation.
- **Information disclosure**: none. The core returns only the sorted strings and counters that the caller supplied.
