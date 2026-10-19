# Business Rules — U2 playground-ui

UI behavior rules for the single-page Streamlit sorting playground. Each rule is identified by `BR<group>.<seq>`. U2 owns presentation and orchestration only; normalization, sorting, counting, and verification live in sorting-core (U1).

## Sources

This unit's behavior derives from the consumed upstream artifacts: `unit-of-work.md` (U2 owns SortingPlaygroundApp and WordListProvider), `unit-of-work-story-map.md` (U2 carries US1.1, US1.2, US3.1, US3.2, US4.1, US5.1), `components.md` (SortingPlaygroundApp and WordListProvider catalogue), `requirements.md` (FR1–FR7, NFR1–NFR4), and `contract-summary.md` (Contract 1 sorting-core API, Contract 2 app packaging).

## YAML Source of Truth

```yaml
business_rules:
  - id: BR1.1
    rule_name: "Single Sort Trigger"
    category: behavior
    component: SortingPlaygroundApp
    description: "One Sort button runs bubble sort, selection sort, and quick sort on the same normalized input in a single action."
    formal_definition: |
      On Sort press, SortingPlaygroundApp builds the shared list from typed entries and picked words,
      calls InputProcessor.normalize once, then SortingEngine.run_all on the shared SortInput,
      then AccuracyChecker.check per AlgorithmResult. Exactly three algorithms run per trigger.
    source: [FR2.5, FR5.2, AC2.1.1, AC2.1.2, AC2.1.3]
    validation:
      - "run_all() returns exactly three AlgorithmResult objects"
      - "all three algorithms receive the same normalized_strings"

  - id: BR1.2
    rule_name: "Exact Empty-Input Warning"
    category: behavior
    component: SortingPlaygroundApp
    description: "When the shared list is empty, render the exact message 'Enter or select at least one string', run no algorithm, and produce no result panels."
    formal_definition: |
      Before calling normalize, if the combined shared list has zero entries, render FR6.1 text verbatim,
      skip sort and verify, and hide all three algorithm columns.
    source: [FR6.1, FR6.2, AC4.1.1, AC4.1.2]
    validation:
      - "warning text equals 'Enter or select at least one string'"
      - "zero AlgorithmResult objects produced when input is empty"

  - id: BR1.3
    rule_name: "Combined and De-duplicated Input"
    category: behavior
    component: SortingPlaygroundApp
    description: "Typed entries and picked bundled words are combined into one shared list and de-duplicated before normalization."
    formal_definition: |
      shared_list = dedup(typed_entries + picked_words), preserving first occurrence order.
      Picked words are treated as the input list for all three algorithms.
    source: [AC1.2.2]
    validation:
      - "a string entered both typed and picked sorts once"

  - id: BR2.1
    rule_name: "Per-Algorithm Metrics Rendering"
    category: presentation
    component: SortingPlaygroundApp
    description: "Each algorithm column renders its comparisons and swaps counts as full integers with no truncation."
    formal_definition: |
      Under each column heading: 'Comparisons: N' then 'Swaps: N', where N is the integer reported by U1.
    source: [FR4.2, FR4.3, AC3.2.1, AC3.2.2, AC3.2.5]
    validation:
      - "comparisons and swaps are separate lines"
      - "counts are untruncated integers"

  - id: BR2.2
    rule_name: "Per-Algorithm Accuracy Rendering"
    category: presentation
    component: SortingPlaygroundApp
    description: "Each algorithm column renders 'Accuracy: pass' or 'Accuracy: fail' from U1's independent per-algorithm check."
    formal_definition: |
      Render the AccuracyCheck.passed boolean as 'Accuracy: pass' or 'Accuracy: fail' beneath the column's metrics.
    source: [FR3.2, FR3.3, AC3.2.3, AC3.2.4]
    validation:
      - "one accuracy line per algorithm"
      - "failure of one algorithm does not hide another's result"

  - id: BR2.3
    rule_name: "Side-by-Side Result Layout"
    category: presentation
    component: SortingPlaygroundApp
    description: "Render the input echo and three algorithm result columns side by side, each showing algorithm name and sorted list, using basic Streamlit defaults only."
    formal_definition: |
      Columns render in order [bubble, selection, quick]; each column header shows the algorithm name; no custom CSS.
    source: [FR5.3, FR5.4, AC3.1.1, AC3.1.2, AC3.1.3, AC3.1.4]
    validation:
      - "three columns plus input echo"
      - "each column shows algorithm name and sorted list"
```

## Rules Summary Table

| BR1.1 | Single Sort Trigger | SortingPlaygroundApp | behavior | FR2.5, FR5.2 | One Sort button runs all three on same input |
| BR1.2 | Exact Empty-Input Warning | SortingPlaygroundApp | behavior | FR6.1 | Exact message; no sorting; no panels |
| BR1.3 | Combined Input | SortingPlaygroundApp | behavior | AC1.2.2 | Typed + picked merged and de-duplicated |
| BR2.1 | Per-Algorithm Metrics Rendering | SortingPlaygroundApp | presentation | FR4.2, FR4.3 | Comparisons and Swaps as untruncated integers |
| BR2.2 | Per-Algorithm Accuracy Rendering | SortingPlaygroundApp | presentation | FR3.2, FR3.3 | pass/fail per algorithm, independently |
| BR2.3 | Side-by-Side Result Layout | SortingPlaygroundApp | presentation | FR5.3, FR5.4 | Input echo + three columns, basic Streamlit |
