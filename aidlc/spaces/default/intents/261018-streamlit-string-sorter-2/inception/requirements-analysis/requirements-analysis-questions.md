## Sources

- [desc] Initial description: This is an application that takes a bunch of strings and runs them through various sorting algorithms (bubble sort, selection sort, and quick sort in the first version). It checks for accuracy of results and tracks how many steps it took to produce the output. Users can either enter strings manually or select from a bunch of words in the UI, click a button to sort in the backend, and see the results in the frontend. Keep it as a simple Streamlit application.
- [scope] Workflow-selected scope: `feature`.
- [memory:M1] `ideation/intent-capture/intent-statement.md` — Problem statement, target customer (students, educators, developers), success metrics (accurate results, clear step counts/comparisons, intuitive UI, correct algorithm implementation), initiative trigger (educational/demonstration), initial scope signal.
- [memory:M2] `ideation/scope-definition/scope-document.md` — In scope: string input (manual + word list), sort on request, bubble/selection/quick sort, accuracy checking against reference, step counts, side-by-side results. Out of scope: other algorithms, file I/O/persistence, complex styling, personal data/payments/accounts, external integrations, cost to users, hosting in v1.
- [memory:M3] `ideation/feasibility/constraint-register.md` — C1–C11 (C9 trunk-based squash-merge to main; C10 staging deploy on merge + manual prod approval when hosted; C7 free distribution).
- [memory:M4] `inception/practices-discovery/team-practices.md` — test-after, pytest, ~80% line coverage on sorting logic, Black/Ruff/snake_case, deploy to production automatically on merge (team decision departing from org default), no skeleton.

## Q1. What does "accuracy of result" mean precisely? The scope says verify each algorithm's result against a trusted reference sort. 

[Answer]: A

A. Exact string order match to Python's built-in sorted() (lexicographic)
B. Exact string order match to Python's built-in sorted() with locale? Or just lexicographic (ASCII/Unicode as-is)?
C. We should also allow case-insensitive matching? 
D. We should also normalize whitespace?
X. Other (please specify)

## Q2. What counts as a "step" for each algorithm? The app must track and display how many steps it took.

[Answer]: E

A. Number of comparisons
B. Number of swaps (exchanges)
C. Both comparisons and swaps separately shown
D. A canonical definition per algorithm (bubble/selection/quick) — specify in docs; comparisons+swaps combined into one count
E. Measure iterations of outer/inner loops as defined in standard textbook form
X. Other (please specify)

## Q3. What is the step counting unit for the comparison UI? Must we show the same definition for all three algorithms?

[Answer]: B

A. Show per-algorithm definitions and a single "steps" count with footnote
B. Use the same definition for all three (e.g. total element comparisons) so they are directly comparable
C. Use the canonical complexity-observable metric (comparisons) for all; swaps optional
D. Show comparisons and swaps separately for each
X. Other (please specify)

## Q4. What is the "bunch of words" for selection in the UI? Must it be bundled in the app (no external data source)?

[Answer]: B

A. A small fixed list (e.g. 20-50 common words) bundled with the app
B. The user can paste a list or choose from a fixed bundled list (both modes)
C. Allow user to upload a small text file? (but C2 forbids file I/O/persistence in v1 — manual paste is text entry; file upload is file I/O)
D. Just use manual entry only (no word list selector)
X. Other (please specify)

## Q5. What inputs should be accepted? Case? Numbers? Empty strings? Duplicates? Length limits?

[Answer]: X (all the small letter words, even if you encounter captial you make is small. we only allow small letters and numbers and special characters based on ascii value)

A. Simple case-sensitive string tokens, no empty strings, no duplicates handling specified (keep as-is)
B. Case-insensitive comparison for sorting, but preserve original strings in output?
C. Case-sensitive; trim whitespace; reject/ignore empty strings; allow duplicates
D. Define: case-sensitive lexicographic, preserve formatting, allow duplicates; no length limits (classroom-sized)
E. Treat all as strings, case-sensitive, preserve exact string forms, skip empty lines
X. Other (please specify)

## Q6. How should results be displayed side-by-side? What fields per algorithm?

[Answer]: B

A. For each: sorted list, number of steps, whether correct (pass/fail)
B. For each: sorted list, comparisons count, swaps count, accuracy (match reference), and maybe elapsed time
C. Minimal: sorted result and total steps count and accuracy (pass/fail)
D. Include input shown, algorithm name, sorted array, step count, correctness flag
X. Other (please specify)

## Q7. What is the reference sort for accuracy checking? Must it be deterministic?

[Answer]: A

A. Python's sorted() with default lexicographic order (deterministic)
B. Python's sorted() with case-insensitive key? (but need to decide case handling first)
C. Same ordering rule as algorithms implement (so correctness means same order as reference under same key)
D. Implement a simple correct sort (like Python sorted) as reference in backend
X. Other (please specify)

## Q8. UI details: single button to sort? Or select which algorithm(s) to run? Must run all three and show side-by-side?

[Answer]: A

A. One button "Sort" runs all three algorithms on the same input and shows all three results side-by-side
B. User selects which algorithm(s) to run (checkboxes/dropdown) then click Sort
C. Three separate buttons (one per algorithm)
D. Run all three automatically when input changes? (but requirement says "a button will sort it in the backend")
X. Other (please specify)

## Q9. Error handling / edge cases? (empty input, single string, all same strings)

[Answer]: A

A. Handle empty input: show message "Enter or select at least one string" and don't run
B. Single string: should return it, steps count as 0 (or minimal), correct
C. All same strings: should return same, correct
D. All of A,B,C are required behaviors
E. Just proceed; if empty, maybe show empty result (no special error needed)
X. Other (please specify)

## Q10. Deployment/hosting? Team decided auto-deploy to production on merge (departure from org default). Is there a specific host in v1?

[Answer]: B (local for testing; after merge GitHub Action deploys to Streamlit Community Cloud)

A. No hosting in v1 — runs locally only (Streamlit run locally). Auto-deploy is future if hosted; not needed now.
B. Deploy to Streamlit Cloud on merge to main (auto-deploy). Need Streamlit Cloud account/config.
C. Deploy to a container (Docker) on merge to a simple host. Need host details.
D. Keep as local app only; no deployment pipeline needed in v1.
E. Auto-deploy to production on merge — use the simplest free host; specify later.
X. Other (please specify)

## Q11. Any performance constraints? Inputs are classroom-sized (feasibility). Any step count display limits?

[Answer]: A

A. No performance constraints in v1; classroom-sized inputs (small, e.g. < 100 strings). No step count limits.
B. Step counts can be large but integer; just display them. No truncation.
C. Both A and B
D. Optimize for readability, not performance; inputs small.
X. Other (please specify)

## Consolidated Summary Confirmation

Does this all look correct before I generate the requirements artifact?

- Looks correct
- Request changes

[Answer]: Looks correct

## Assumption Confirmation

Two assumptions from prior stages:

1. [assumption] "Steps" definition needs to be consistent/comparable across algorithms; scope requires comparable counts.
2. [assumption] The provided word list is bundled with the app (no external data source, per C6).

A. Accept assumptions
B. Convert to follow-up questions

[Answer]: A
