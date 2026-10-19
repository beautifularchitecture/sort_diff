# Security Design — sorting-core (U1)

Implements the requirements in `nfr-requirements/security-requirements.md` (NFR2.1, NFR2.2, NFR3.2, NFR3.3).

## Design Decisions

| ID | Decision | Implements |
|---|---|---|
| SD-1 | Input is typed data only. Algorithms compare strings with `<` and `>`; nothing is evaluated, parsed as code, or deserialized. | NFR2.1 |
| SD-2 | The core validates input types at its boundary and fails fast with `TypeError` (NFR design Q1, option A). Invalid input never reaches a sort. | NFR2.1 |
| SD-3 | The core returns plain Python values (lists of strings, integers, booleans). It never builds HTML or markup, so no escaping logic lives in the core. Escaping is the caller's responsibility. | NFR2.2 |
| SD-4 | No imports of I/O, network, or process modules in the `sorting-core` package. | NFR3.2 |
| SD-5 | No user identity is accepted or stored. | NFR3.3 |

## Boundary Validation

- `normalize` (InputProcessor): accepts a list of strings. Any non-list, or any item that is not a string, raises `TypeError`.
- `run_all` (SortingEngine): accepts a `SortInput`. Any other type raises `TypeError`.
- `check` (AccuracyChecker): accepts an `AlgorithmResult` and a `SortInput`. Any other type raises `TypeError`. A `run_id` mismatch raises `ValueError`.

Snippet (interface level, illustrative):

```python
def normalize(raw_entries: list[str]) -> SortInput:
    if not isinstance(raw_entries, list) or not all(isinstance(e, str) for e in raw_entries):
        raise TypeError("raw_entries must be a list of strings")
    ...
```

## Caller Obligations (U2 playground-ui)

The core cannot enforce these itself, so the caller must:

- Escape every value before rendering it as HTML (NFR2.2, SD-3).
- Cap the input at 100 strings before calling `normalize` (the NFR Q2 maximum). The core accepts unbounded lists and does not enforce this cap; the DoS treatment below depends on it.

## Threats Considered

| Threat | Treatment |
|---|---|
| Code injection via input text | SD-1 and SD-2 |
| Markup injection in the UI | SD-3 (caller escapes output) |
| Unexpected I/O from the core | SD-4 |
| Denial of service through input size | Accepted at the 100-string maximum (NFR Q2). Quadratic algorithms are acceptable at that size. |
