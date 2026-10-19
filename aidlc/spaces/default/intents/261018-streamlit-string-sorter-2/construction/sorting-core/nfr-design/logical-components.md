# Logical Components — sorting-core (U1)

The sorting-core unit is an in-process Python package with no runtime services, queues, or external stores. Its logical components map one-to-one to the domain components in `components.md`.

## Components

| Logical component | Responsibility | Pattern | Notes |
|---|---|---|---|
| InputProcessor | Normalize raw entries into a `SortInput` | Pure function with boundary type checks (SD-2) | Generates `run_id` |
| SortingEngine | Run bubble, selection, and quick sort on one `SortInput` | Shared counter object (NFR design Q3, option A) | Recursive quick sort (NFR design Q2, option A) |
| AccuracyChecker | Compare each `AlgorithmResult` to `sorted()` | Pure function | Independent per algorithm |

## Shared Counter

- Each `Counter` holds two integers: `comparisons` and `swaps`.
- `run_all` creates three fresh `Counter` objects per call, one for each algorithm (bubble, selection, quick). Each algorithm receives only its own counter and increments only that counter. Counts are never shared or accumulated across algorithms.
- The counting definitions match BR2.1 (comparisons) and BR2.2 (swaps) in `functional-design/rules.md`. Worked example for `[3, 1, 2]`: bubble 3 comparisons, selection 3, quick 2; each value is reported from its own counter.
- No counter state survives a call, so no state leaks between runs.

## Failure Domains

- No failure domain spans components. A failure in one sort does not affect the other two, because each algorithm runs on its own copy of the list.
- Errors raised at the boundary (`TypeError`, `ValueError`) propagate to the caller unchanged. The core does not catch or swallow them.

## Deployment View

- Packaged as a module imported by playground-ui (U2).
- No separate process, container, or service.
