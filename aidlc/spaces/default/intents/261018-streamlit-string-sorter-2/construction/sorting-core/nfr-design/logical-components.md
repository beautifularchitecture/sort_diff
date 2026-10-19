# Logical Components — sorting-core (U1)

The sorting-core unit is an in-process Python package with no runtime services, queues, or external stores. Its logical components map one-to-one to the domain components in `components.md`.

## Components

| Logical component | Responsibility | Pattern | Notes |
|---|---|---|---|
| InputProcessor | Normalize raw entries into a `SortInput` | Pure function with boundary type checks (SD-2) | Generates `run_id` |
| SortingEngine | Run bubble, selection, and quick sort on one `SortInput` | Shared counter object (NFR design Q3, option A) | Recursive quick sort (NFR design Q2, option A) |
| AccuracyChecker | Compare each `AlgorithmResult` to `sorted()` | Pure function | Independent per algorithm |

## Shared Counter

- One `Counter` object is created per `run_all` call.
- It holds two integers: `comparisons` and `swaps`.
- Each algorithm receives the counter as an argument and increments it. The definitions match BR-SE-1 and BR-SE-2 in `functional-design/rules.md`.
- The counter is created fresh for each run, so no state leaks between runs.

## Failure Domains

- No failure domain spans components. A failure in one sort does not affect the other two, because each algorithm runs on its own copy of the list.
- Errors raised at the boundary (`TypeError`, `ValueError`) propagate to the caller unchanged. The core does not catch or swallow them.

## Deployment View

- Packaged as a module imported by playground-ui (U2).
- No separate process, container, or service.
