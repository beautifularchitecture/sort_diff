# NFR Requirements Questions — playground-ui (U2)

Inception NFRs apply: NFR2 Simplicity and Usability, NFR3 Scope and Constraints (classroom-sized inputs, no external integrations), NFR4 Code Quality.

Already answered project-wide in `construction/sorting-core/nfr-requirements/nfr-requirements-questions.md` and carried into this unit: no numeric sort-time target (responsive for small inputs), best-effort reliability with no SLO, no per-run logging beyond the hosting platform's logs, Python 3.12 with minimum-version dependency ranges. Those are inherited, not re-asked. The questions below cover only what is genuinely new to the UI layer.

## Q1: Enforcing the classroom input cap in the UI

The sorting core documents the 100-string classroom limit as an expectation the caller (this UI) enforces. How should the UI handle input beyond it?

A. Hard cap: if more than 100 strings reach the shared list, refuse to sort and show a message stating the 100-string limit
B. Soft warning: sort anyway but display a note that inputs above 100 strings may feel slow
C. No enforcement: rely on responsiveness for small inputs (the project has no numeric performance target)
X. Other (please specify)

[Answer]: A

## Q2: Streamlit dependency pinning

This unit declares the runtime dependency (streamlit) in `requirements.txt`; U1 chose Python 3.12 with minimum-version ranges. How should streamlit be pinned?

A. Minimum version range (for example `streamlit>=1.40`), matching the project's range strategy
B. Exact pin to one version (for example `streamlit==1.40.0`) for reproducible demos
X. Other (please specify)

[Answer]: A

## Q3: Rendering safety for user input

User-typed strings are echoed back and shown in result columns. How should they be rendered?

A. Plain text only: render every user string through Streamlit's default text APIs (auto-escaped); never pass user input to unsafe HTML/markdown rendering
B. Markdown allowed: render user strings as markdown (tables).render -- open for formatting
X. Other (please specify)

[Answer]: A

## Q4: UI responsiveness target

The core has no numeric sort-time target (inherited). Should the UI layer define its own target for a classroom-sized run (widgets to rendered columns)?

A. No numeric target; responsive for up to 100 strings is sufficient (inherits the project answer)
B. A concrete target such as under 2 seconds end-to-end for 100 strings
X. Other (please specify)

[Answer]: A

---

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
