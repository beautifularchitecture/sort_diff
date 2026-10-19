# NFR Design Questions — playground-ui (U2)

Settled earlier and not repeated here: no numeric performance target, hard 100-string cap, plain-text rendering (no unsafe HTML), streamlit minimum-version range, Python 3.12, best-effort reliability, no observability beyond platform logs.

## Q1: Handling an error raised by sorting-core

The core fails fast with `TypeError` (bad input type) or `ValueError` (run_id mismatch), and its quick sort can raise `RecursionError` on pathological input. How should the UI react?

A. Catch these at the boundary and render a Streamlit error message; never let the app crash
B. Let the exception propagate and let Streamlit show the traceback
X. Other (please specify)

[Answer]: B

## Q2: Caching the sort run

Should the UI cache the result of `run_all` across Streamlit reruns?

A. No caching: recompute on every Sort press (simple; input is tiny)
B. Cache with `st.cache_data` keyed on the normalized input
X. Other (please specify)

[Answer]: A

## Q3: Where results live between reruns

Streamlit reruns the script on every interaction. Where should the displayed results live?

A. In `st.session_state`, set on Sort press, so results survive unrelated widget interactions
B. Recompute from the current widgets on every rerun (results vanish if input changes)
X. Other (please specify)

[Answer]: B

---

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
