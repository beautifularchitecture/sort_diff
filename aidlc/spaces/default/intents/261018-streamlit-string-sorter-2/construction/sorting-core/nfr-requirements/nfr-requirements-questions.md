# NFR Requirements Questions — sorting-core (U1)

Inception NFRs apply: NFR1 Correctness, NFR2 Simplicity and Usability, NFR3 Scope and Constraints (classroom-sized inputs, typically under 100 strings), NFR4 Code Quality.

## Q1: Performance target for one sort run

How quickly must all three algorithms and the accuracy check finish for a classroom-sized input?

A. Under 100 ms for up to 100 strings
B. Under 1 second for up to 100 strings
C. No numeric target; responsive for small inputs only (NFR3.6 wording)
X. Other (please specify)

[Answer]: C

## Q2: Maximum input size

What is the largest input the sorting core must accept?

A. 100 strings
B. 1,000 strings
C. No fixed limit beyond available memory
X. Other (please specify)

[Answer]: A

## Q3: Input handling and security

The only input is user-typed text and bundled words. How should the core treat it?

A. Treat all input as plain text: never evaluate it, never render it as HTML, no authentication needed
B. A. plus a maximum length per string (for example 256 characters)
C. A. plus no length limit
X. Other (please specify)

[Answer]: A

## Q4: Reliability target

The app is a free, single-page demo. What availability target applies?

A. Best effort (no SLO; Streamlit Community Cloud availability)
B. 99% monthly availability, measured by an external uptime check
X. Other (please specify)

[Answer]: A

## Q5: Observability

What should the running app record about each sort run?

A. Nothing beyond the hosting platform's logs
B. Log one line per run to stdout: input size, duration, per-algorithm comparison and swap counts
C. B. plus a visible timing panel in the UI
X. Other (please specify)

[Answer]: A

## Q6: Python version and dependency pinning

Which Python version does CI and deployment target, and how are dependencies pinned?

A. Python 3.11, exact pins in requirements.txt
B. Python 3.12, exact pins in requirements.txt
C. Python 3.12, minimum-version ranges in requirements.txt
X. Other (please specify)

[Answer]: C

---

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
