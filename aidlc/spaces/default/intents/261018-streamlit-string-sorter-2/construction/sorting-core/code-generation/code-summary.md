# Code Summary — sorting-core (U1)

## Implementation Status
Artifacts specify the complete package structure. Code implementation will follow the plan; this summary describes what will be built.

## Public API
- `SortInput`, `AlgorithmResult`, `AccuracyCheck`, `Counter` (dataclasses)
- `InputProcessor`, `SortingEngine`, `AccuracyChecker`, `WordListProvider`
- `run_all(raw_entries: list[str]) -> tuple[list[AlgorithmResult], list[AccuracyCheck]]` or combined results (final shape per entities.md)

## Key Rules Enforced
- Normalization matches BR-INP-1/2; run_id per BR-INP-3.
- All three algorithms use shared counter definition (BR-SE-1); swap counts per BR-SE-2.
- Recursive Lomuto quicksort; stable sort semantics achieved via index-keying to match `sorted()` (BR-SE-5).
- Exactly three algorithms (BR-SE-4).
- Exact-match accuracy (BR-AC-1), independent checks (BR-AC-2).
- Type boundary validation (SD-2), no I/O/HTML (SD-1, SD-3, SD-4).
- Immutable bundled words (BR-WLP-1).

## Traceability
Each component traces to business rules in rules.md and security design in security-design.md. The package is a pure library consumed by playground-ui (U2).

Implementation files: 8 modules as specified in the code generation plan. Tests to follow in tests/ (unit-test-instructions.md).