# User Stories

All stories follow the standard format `As a [persona], I want [goal], so that [benefit]` and satisfy INVEST criteria. Acceptance criteria use Given/When/Then with stable `AC{group}.{story}.{n}` IDs. Priorities are MoSCoW; the MVP boundary is formally decided at Delivery Planning.

## Story Map

| Priority | Story  | One-line goal |
|----------|--------|---------------|
| Must     | US1.1  | Enter strings manually (paste or type) |
| Must     | US1.2  | Select strings from the bundled word list |
| Must     | US2.1  | Run all three algorithms with one Sort button |
| Must     | US3.1  | See all three results side-by-side with the input |
| Must     | US3.2  | See comparisons, swaps, and accuracy per algorithm |
| Must     | US4.1  | Get a clear message on empty input |
| Must     | US4.2  | Get correct results for single/all-identical/empty-string edge cases |
| Should   | US5.1  | Run the app locally with one command |
| Must     | US5.2  | Get the app deployed automatically on merge to main |

---

## US1 — String Input

### US1.1 — Manual string entry

**As a** student, **I want** to type or paste a list of strings into the app, **so that** I can sort my own data without any setup.

- **Priority**: Must Have
- **Depends on**: none
- **Related**: US1.2 (alternate input path), US4.1 (empty-input guard)
- **INVEST notes**: Independent (input UI alone is deliverable and testable); Small; Testable via UI-level checks and parser unit tests.

**Acceptance criteria:**

- **AC1.1.1** — Given the app is open, When I type or paste strings (separated by line breaks or commas) into the input area and press Sort, Then all three algorithms run on that input and results are displayed.
- **AC1.1.2** — Given I enter a string containing uppercase letters, When input processing runs, Then those letters are normalized to lowercase before sorting, per the input-normalization rule (lowercase letters, numbers, and special characters by ASCII value).
- **AC1.1.3** — Given I enter a mix of letter case (e.g. `Banana`, `apple`, `CHERRY`), When results are displayed, Then the displayed input and outputs reflect the consistently normalized forms.
- **AC1.1.4** — Given I paste a multi-line list, When input is parsed, Then each line (or comma-separated token) becomes one string in the list to sort.

### US1.2 — Bundled word-list selection

**As an** educator, **I want** to select strings from a word list bundled with the app, **so that** I can run a demo quickly without typing.

- **Priority**: Must Have
- **Depends on**: none
- **Related**: US1.1 (manual path)
- **INVEST notes**: Independent (selector works without manual entry); Small; Testable against the fixed bundled list.

**Acceptance criteria:**

- **AC1.2.1** — Given the app is open, When I open the bundled word-list selector, Then a fixed set of words shipped with the app is available for selection (no external data source).
- **AC1.2.2** — Given I select one or more words from the bundled list, When I press Sort, Then the selected words are treated as the input list for all three algorithms.
- **AC1.2.3** — Given the app is deployed, When the word list is loaded, Then it comes from the bundled list packaged with the app (no network fetch at runtime).

---

## US2 — Sorting

### US2.1 — Single Sort button runs all three algorithms

**As a** student, **I want** one Sort button that runs bubble sort, selection sort, and quick sort on the same input, **so that** I can compare the three algorithms directly.

- **Priority**: Must Have
- **Depends on**: US1.1 or US1.2 at runtime for input (buildable and testable independently with synthetic input)
- **Related**: US3.1, US3.2 (presentation of results)
- **INVEST notes**: Valuable core of the product; Small (delegates to the three algorithm implementations); Testable via unit tests on each algorithm plus one UI-level check.

**Acceptance criteria:**

- **AC2.1.1** — Given I have provided input (manual or bundled-list), When I press the single Sort button, Then bubble sort, selection sort, and quick sort all execute on the same normalized input in that one action.
- **AC2.1.2** — Given sorting has been triggered, When the algorithms run, Then each sorts strings lexicographically (default ASCII/Unicode ordering).
- **AC2.1.3** — Given the app is running, When sorting executes, Then only bubble sort, selection sort, and quick sort run — no other algorithms.

---

## US3 — Results and Metrics

### US3.1 — Side-by-side result display

**As a** student, **I want** to see all three sorted results side-by-side along with the input I sorted, **so that** I can compare the algorithms' outputs at a glance.

- **Priority**: Must Have
- **Depends on**: US2.1 at runtime (needs a completed sort to display; independently buildable as a results panel)
- **Related**: US3.2 (metrics shown in the same panel)
- **INVEST notes**: Independent presentation concern; Small; Testable by asserting rendered content for a known input.

**Acceptance criteria:**

- **AC3.1.1** — Given sorting has completed, When I view the results area, Then the input list that was sorted is shown.
- **AC3.1.2** — Given sorting has completed, When I view the results area, Then all three algorithms' results appear together, side-by-side.
- **AC3.1.3** — Given a result block for one algorithm, When I read it, Then it shows the algorithm name and its sorted list.
- **AC3.1.4** — Given the results are rendered, When I view them, Then the presentation is clear and simple, suitable for educational use (no complex styling beyond basic Streamlit).

### US3.2 — Comparisons, swaps, and accuracy per algorithm

**As a** student, **I want** to see the comparison count, swap count, and a pass/fail accuracy check for each algorithm, **so that** I can understand how each algorithm worked and trust the result.

- **Priority**: Must Have
- **Depends on**: US2.1 at runtime; independently testable at the algorithm-function level
- **Related**: US3.1 (same result panel)
- **INVEST notes**: Testable against hand-computed counts and Python's `sorted()` reference; Small.

**Acceptance criteria:**

- **AC3.2.1** — Given an algorithm has sorted the input, When its metrics are displayed, Then the total element-comparison count is shown, using the same comparison definition across all three algorithms so the numbers are directly comparable.
- **AC3.2.2** — Given an algorithm has sorted the input, When its metrics are displayed, Then the swap count is shown separately from the comparison count.
- **AC3.2.3** — Given an algorithm has produced a sorted list, When accuracy is checked, Then the result is compared for exact order match against Python's built-in `sorted()` on the same input, and shown as pass/fail.
- **AC3.2.4** — Given sorting has completed, When accuracy is evaluated, Then each of the three algorithms is checked independently (one algorithm's failure does not hide another's result).
- **AC3.2.5** — Given a non-trivial input, When counts are displayed, Then comparison and swap counts appear as full integers with no truncation.

---

## US4 — Error Handling and Edge Cases

### US4.1 — Empty input message

**As a** student, **I want** a clear message when I press Sort with nothing entered or selected, **so that** I know what to do instead of seeing a broken or empty result.

- **Priority**: Must Have
- **Depends on**: none (guard around the sort trigger)
- **Related**: US1.1, US1.2
- **INVEST notes**: Small; directly testable.

**Acceptance criteria:**

- **AC4.1.1** — Given no strings have been entered or selected, When I press Sort, Then the message `Enter or select at least one string` is displayed.
- **AC4.1.2** — Given empty input, When I press Sort, Then no sorting algorithms run and no result panels are produced.

### US4.2 — Single, all-identical, and empty-string edge cases

**As a** developer, **I want** single-string, all-identical-strings, and embedded-empty-string inputs handled correctly, **so that** edge cases produce honest results and counts rather than surprises.

- **Priority**: Must Have
- **Depends on**: US2.1 at runtime; algorithm-level behavior independently testable
- **Related**: US3.2 (counts and accuracy displayed for these cases)
- **INVEST notes**: Testable with direct unit tests; Small.

**Acceptance criteria:**

- **AC4.2.1** — Given a single string in the input, When I press Sort, Then that string is returned as the sorted result with appropriate minimal/zero step counts for each algorithm and accuracy passes.
- **AC4.2.2** — Given an input where all strings are identical, When I press Sort, Then the same list is returned correctly, counts are recorded correctly, and accuracy passes for all three algorithms.
- **AC4.2.3** — Given the parsed input contains empty strings, When input is processed for sorting, Then empty strings are rejected or ignored appropriately and do not corrupt the sorted output.

---

## US5 — Deployment

### US5.1 — Local run

**As a** developer, **I want** to run the app locally with one command, **so that** I can test changes and use the app offline.

- **Priority**: Should Have (FR7.1 requirement; developer-facing, ranked below the deployed-app stories for MoSCoW clarity)
- **Depends on**: none
- **Related**: US5.2
- **INVEST notes**: Small; testable by following the documented run command.

**Acceptance criteria:**

- **AC5.1.1** — Given the project is set up locally, When I run the documented Streamlit command, Then the app starts and is usable in a browser.
- **AC5.1.2** — Given the app runs locally, When I use it, Then behavior matches the deployed version for the features in scope (same sorting, same metrics, same messages).

### US5.2 — Automatic deployment on merge to main

**As a** maintainer, **I want** the app deployed to Streamlit Community Cloud automatically whenever a change merges to main, **so that** the public app is always current without a manual release step.

- **Priority**: Must Have (team practice: continuous deployment to production on merge)
- **Depends on**: US5.1 (a runnable app to deploy)
- **Related**: US5.1
- **INVEST notes**: Small; testable by observing the CI workflow on a merge.

**Acceptance criteria:**

- **AC5.2.1** — Given a change has been squash-merged to `main`, When the GitHub Actions workflow runs, Then the app is deployed to Streamlit Community Cloud automatically.
- **AC5.2.2** — Given a deployment has completed, When a user opens the deployed app URL, Then the latest merged version of the app is served.
- **AC5.2.3** — Given a merge to a branch other than `main`, When CI runs, Then no production deployment is triggered.
