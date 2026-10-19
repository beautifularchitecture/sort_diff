# NFR Design Questions — sorting-core (U1)

Settled earlier and not repeated here: no numeric performance target, 100-string maximum, plain-text input with no evaluation, best-effort reliability, no observability beyond platform logs, Python 3.12, minimum-version dependency ranges.

## Q1: Error handling for invalid input at the core boundary

What should the core do when it receives a non-list or a non-string item?

A. Fail fast: raise TypeError with a clear message (recommended; matches the construction guardrail that errors are never silent)
B. Return an error result object for the caller to inspect
X. Other (please specify)

[Answer]: A

## Q2: Quick sort recursion

Lomuto quick sort recurses on each partition. Given the 100-string maximum, which style should the core use?

A. Recursive, relying on Python's default recursion limit (recommended; depth is at most about 100 for the stated maximum)
B. Iterative with an explicit stack
X. Other (please specify)

[Answer]: A

## Q3: How the three algorithms share comparison and swap counting

A. One counter object created per run and passed into each algorithm (recommended; testable and identical definition across algorithms)
B. Closure-based counters inside each algorithm function
X. Other (please specify)

[Answer]: A

---

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
