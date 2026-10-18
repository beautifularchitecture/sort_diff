# Requirements

## Intent Analysis

The goal is to create a simple Streamlit application that demonstrates and compares three sorting algorithms (bubble sort, selection sort, quick sort) on string data. Users need to understand how each algorithm behaves by seeing results side-by-side along with accuracy verification and step counts. The app serves educational/demonstration purposes for students, educators, and developers.

## Functional Requirements

### FR1. String Input
FR1.1. The system must accept string input via manual entry in the UI.
FR1.2. The system must accept string input via selection from a bundled word list (user can paste or choose from a fixed bundled list).
FR1.3. Input processing must normalize strings to lowercase when encountering capital letters; the system only allows lowercase letters, numbers, and special characters based on ASCII value (per user specification for Q5).
FR1.4. The system must preserve the original string forms as entered (after normalization rule applied consistently) in both input display and output.
FR1.5. The bundled word list must be included with the app (no external data source).

### FR2. Sorting Algorithms
FR2.1. The system must implement bubble sort for strings.
FR2.2. The system must implement selection sort for strings.
FR2.3. The system must implement quick sort for strings.
FR2.4. All three algorithms must sort strings lexicographically (ASCII/Unicode as-is, default lexicographic ordering).
FR2.5. All three algorithms must run on the same input when sorting is triggered.

### FR3. Accuracy Checking
FR3.1. For each algorithm, the system must verify accuracy by comparing its sorted result against Python's built-in `sorted()` (default lexicographic, deterministic).
FR3.2. Accuracy must be reported as pass/fail for each algorithm (exact order match to reference).
FR3.3. All three algorithms must be checked for accuracy independently.

### FR4. Step Counting
FR4.1. The system must track step counts for each algorithm using the textbook definition: measure iterations of outer/inner loops as defined in the standard textbook form for each algorithm (bubble, selection, quick).
FR4.2. The same definition of "total element comparisons" must be used as the primary comparable count for UI display across all three algorithms (to enable direct comparison).
FR4.3. The system must also track and display swap counts separately for each algorithm (complementary to comparisons).
FR4.4. Step/comparison counts are integers and must be displayed without truncation (no limits on classroom-sized inputs).
FR4.5. For edge cases (single element, all equal), counts must be recorded correctly (e.g., minimal counts).

### FR5. User Interface
FR5.1. The UI must be implemented as a simple Streamlit application.
FR5.2. A single "Sort" button must run all three algorithms on the same input and display all three results side-by-side.
FR5.3. For each algorithm, the UI must display: algorithm name, sorted list, comparisons count, swaps count, and accuracy (pass/fail).
FR5.4. The UI must show the input that was sorted.
FR5.5. The UI must provide clear, intuitive presentation suitable for educational use.

### FR6. Error Handling and Edge Cases
FR6.1. If the input is empty (no strings entered/selected), the system must display a message "Enter or select at least one string" and must not run sorting.
FR6.2. For a single string input, the system must return it correctly with appropriate step counts (minimal/zero as defined by algorithm implementation) and accuracy pass.
FR6.3. For inputs where all strings are identical, the system must return the same list correctly with accuracy pass.
FR6.4. The system must reject/ignore empty strings appropriately when processing input.

### FR7. Deployment
FR7.1. The app must run locally for testing (via `streamlit run`).
FR7.2. The system must be deployable to Streamlit Community Cloud.
FR7.3. Deployment to production (Streamlit Community Cloud) must occur automatically on merge to `main` via GitHub Actions (continuous deployment), consistent with team practice of auto-deploying to production on merge.

## Non-Functional Requirements

### NFR1. Correctness
NFR1.1. Sorting results must be exactly correct as verified against the reference sort.
NFR1.2. Step counting must be implemented consistently according to the chosen definitions.

### NFR2. Simplicity and Usability
NFR2.1. The UI must remain simple (no complex styling beyond basic Streamlit).
NFR2.2. The application must be easy to understand for educational purposes (clear display of comparisons, swaps, and accuracy).
NFR2.3. The app must be self-contained with no external integrations or data sources.

### NFR3. Scope and Constraints
NFR3.1. Only bubble sort, selection sort, and quick sort are implemented (no other algorithms).
NFR3.2. No file I/O or persistent storage.
NFR3.3. No personal data, payments, or user accounts.
NFR3.4. No external system integrations.
NFR3.5. Free distribution; no cost to users.
NFR3.6. Inputs are classroom-sized (small, typically < 100 strings); no specific performance constraints beyond being responsive for small inputs.

### NFR4. Code Quality
NFR4.1. Code must follow team style: Black formatter, Ruff linter, snake_case naming.
NFR4.2. Tests (pytest) must achieve at least ~80% line coverage on sorting logic, following test-after methodology.
NFR4.3. Implementation must be testable and maintainable.

## Constraints

- Technical: Must be a simple Streamlit app (Python)
- Process: Trunk-based development with short-lived branches, squash-merged to main; auto-deploy to production on merge
- Scope: v1 limited to three algorithms only
- Distribution: Free, runs locally; deployable to Streamlit Community Cloud

## Assumptions

- [assumption] "Steps" definition (textbook loop iterations) is consistent with total element comparisons as the primary UI metric for cross-algorithm comparison.
- [assumption] The bundled word list is packaged with the app (no external data access).
- [assumption] Input normalization: when encountering capital letters, make them lowercase; only allow lowercase letters, numbers, and special characters based on ASCII value. This is the normalization rule applied during input processing.
- [assumption] "Comparisons count" and "swaps count" are tracked separately as specified; the primary comparable metric across algorithms is total element comparisons.

## Out of Scope

- Additional sorting algorithms beyond bubble, selection, quick sort
- File upload functionality (beyond manual text entry/paste and bundled list selection)
- Persistent storage or file I/O
- Complex UI styling
- Authentication, accounts, payments, personal data collection
- External system integrations or external data sources
- Performance optimization for large datasets
- Hosting beyond Streamlit Community Cloud in v1

## Open Questions

- None identified; all questions from requirements analysis have been answered.
