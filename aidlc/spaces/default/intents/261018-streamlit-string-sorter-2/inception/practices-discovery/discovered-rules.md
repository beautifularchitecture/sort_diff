## Mandated

- ALWAYS validate sorting algorithm correctness against expected results (accuracy is a stated requirement).
- ALWAYS report the number of steps taken to produce the output (bubble/selection/quick sort step counts must be measurable).
- ALWAYS treat inputs as user-provided strings (from manual entry or selection from a provided word list) and handle them safely.
- ALWAYS keep the UI and backend distinct (Streamlit UI triggers backend sort; results returned to frontend).

## Forbidden

- NEVER hardcode secrets or credentials (org default).
- NEVER introduce new sorting algorithms beyond bubble sort, selection sort, and quick sort in this first step (scope constraint from project description).
- NEVER leave unhandled exceptions at integration points (backend/UI boundary) that could crash the Streamlit app without a user-facing message.

**Note:** Minimal set for greenfield; may be expanded during interview if the human states additional hard constraints. Empty sections would be acceptable if no hard constraints are stated, but these reflect clear requirements from the project description and org security guidance.