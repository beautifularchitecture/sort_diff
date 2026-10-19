# Business Rules — U1 sorting-core

Formal specification of domain rules, constraints, and validation logic. Each rule is identified by `BR<group>.<seq>` (the `BRx.y` format the traceability sensor recognizes).

## Sources

This unit's scope, ownership boundaries, and story assignment derive from the consumed upstream artifacts: `unit-of-work.md` (U1 owns `SortInput`, `AlgorithmResult`, `AccuracyCheck`), `unit-of-work-story-map.md` (U1 carries US2.1, US3.2, US4.2), `components.md` (component catalogue), `requirements.md` (FR/NFR), and `contract-summary.md` (U1 → U2 contracts).

## YAML Source of Truth

```yaml
business_rules:
  - id: BR1.1
    rule_name: "Input Normalization"
    category: calculation
    description: "Raw entries are normalized by splitting, trimming, dropping empty tokens, and lowercasing ASCII capitals only."
    component: InputProcessor
    applies_to: [SortInput]
    formal_definition: |
      For each entry in raw_entries:
        1. Split on newline (\n) and comma (,) to produce tokens
        2. Trim leading and trailing whitespace from each token
        3. Drop tokens that are empty (length 0 after trim)
        4. For each remaining token:
           a. Lowercase ASCII capital letters: A-Z → a-z
           b. Pass all other characters through unchanged (non-ASCII, numbers, lowercase, punctuation)
        5. Collect all processed tokens into normalized_strings
        6. Preserve duplicates (do not deduplicate)
    source: [FR1.3, FR1.4, D10]
    validation:
      - "normalized_strings is derived deterministically from raw_entries"
      - "Every token in normalized_strings traces to exactly one entry in raw_entries"
      - "len(normalized_strings) <= sum over entries of (delimiter count in that entry + 1)"
      - "All strings in normalized_strings are non-empty"
      - "No duplicates are removed"
      - "ASCII capitals A-Z are always lowercased; non-ASCII characters are unchanged"
    examples:
      - raw_entries: ["Alice", "bob", "", "Alice", "cäfe"]
        normalized_strings: ["alice", "bob", "alice", "cäfe"]
        note: "Empty token removed; cäfe unchanged (non-ASCII ä passes through); Alice lowercased"
      - raw_entries: ["HELLO,world\nnew line"]
        normalized_strings: ["hello", "world", "new", "line"]
        note: "Split on comma and newline; one entry yields four tokens, so len(normalized_strings) exceeds len(raw_entries)"

  - id: BR1.2
    rule_name: "Empty String Handling"
    category: validation
    description: "Empty tokens are dropped during normalization. Empty normalized_strings is not sorted by U1; validation is handled by U2."
    component: InputProcessor
    applies_to: [SortInput]
    formal_definition: |
      1. Any token that is empty (zero length) after trimming whitespace is discarded.
      2. If all tokens are empty, normalized_strings is empty.
      3. U1 does not validate the non-empty constraint; U2 validates and renders the FR6.1 message.
    source: [FR6.4]
    validation:
      - "After normalization, no empty strings exist in normalized_strings"
      - "Empty input case is handled by U2, not U1"
    examples:
      - raw_entries: ["", "  ", "hello"]
        normalized_strings: ["hello"]
        note: "Empty and whitespace-only tokens dropped"

  - id: BR1.3
    rule_name: "Run Identifier Generation"
    category: calculation
    description: "Each SortInput is assigned a unique run_id at creation time."
    component: InputProcessor
    applies_to: [SortInput]
    formal_definition: |
      1. When normalize() is called, generate a run_id (UUID or timestamp-based).
      2. Assign this run_id to the SortInput.
      3. This run_id is immutable and unique within the application lifetime.
      4. This run_id is copied into all AlgorithmResult and AccuracyCheck objects derived from this SortInput.
    source: [Contract 1 (U1 → U2)]
    validation:
      - "run_id is non-empty, non-null"
      - "run_id is unique across all SortInput objects in a session"
      - "run_id does not change after SortInput creation"
    examples:
      - run_id: "uuid:550e8400-e29b-41d4-a716-446655440000"

  - id: BR2.1
    rule_name: "Comparison Counting — Single Definition for All Algorithms"
    category: calculation
    description: "All three algorithms count element comparisons identically: every time two elements are compared to decide their order, the count increments."
    component: SortingEngine
    applies_to: [AlgorithmResult]
    formal_definition: |
      For each algorithm:
        1. Increment the comparisons counter every time two elements are compared with an
           ordering operator (<, >, <=, >=) to decide their relative order.
        2. This includes all comparisons in outer loops, inner loops, recursion, and partitioning.
        3. The comparison is counted regardless of outcome (true or false).
        4. Do NOT count array accesses, assignments, or other operations.
        5. Do NOT count the equality tests used only to skip a no-op swap (BR2.2); those are
           identity checks on the swap operation, not ordering decisions.

      Worked examples (traced from the pseudocode in functional-spec.md):

      Bubble sort on [3, 1, 2] — 3 comparisons:
        - Pass 1 (i=0): compare 3>1 (count=1), swap → [1,3,2]; compare 3>2 (count=2), swap → [1,2,3]
        - Pass 2 (i=1): compare 1>3 (count=3), no swap
        - Pass 3 (i=2): inner loop empty, no comparisons
        - Total comparisons: 3  (n*(n-1)/2 = 3)

      Selection sort on [3, 1, 2] — 3 comparisons:
        - Pass i=0: compare 1<3 (count=1), compare 2<1 (count=2), swap → [1,3,2]
        - Pass i=1: compare 2<3 (count=3), swap → [1,2,3]
        - Total comparisons: 3  (exactly n*(n-1)/2)

      Quick sort on [3, 1, 2] with Lomuto partition — 2 comparisons:
        - Partition around pivot 2: compare 3<2 (count=1); compare 1<2 (count=2)
        - Subarrays [1] and [3] have no comparisons
        - Total comparisons: 2
    source: [FR4.1, FR4.2]
    validation:
      - "comparisons >= 0 for all inputs"
      - "comparisons = 0 for empty or single-element input"
      - "comparisons for bubble sort and selection sort equals n*(n-1)/2 exactly, regardless of input order"
      - "comparisons is the same across runs with identical input and algorithm (deterministic)"
      - "comparisons is directly comparable across all three algorithms (same definition)"
    rationale: |
      FR4.2 explicitly requires "total element comparisons must be used as the primary comparable count for UI display across all three algorithms (to enable direct comparison)."
      A single, consistent definition ensures that comparison counts are fair to compare between bubble sort, selection sort, and quick sort.

  - id: BR2.2
    rule_name: "Swap Counting — Algorithm-Specific, Secondary Metric"
    category: calculation
    description: "Swaps are counted per algorithm's natural definition. A swap is counted only when it exchanges two different positions holding different values; no-op exchanges are not counted. Swaps are a secondary metric not directly comparable across algorithms."
    component: SortingEngine
    applies_to: [AlgorithmResult]
    formal_definition: |
      Counted swap: an exchange of the contents of two positions that changes the array —
      the positions differ (i != j) AND the values differ (arr[i] != arr[j]).

      Not counted: a self-exchange (i == j) or an exchange of two equal values; neither
      changes the array. The equality test that guards a swap is an identity check on the
      swap operation and does NOT increment the comparisons counter (BR2.1).

      For bubble sort:
        1. Count every adjacent exchange where output[j] > output[j+1] (always a real exchange).
        2. Example on [3,1,2]: Pass 1 swaps 3↔1 then 3↔2 → 2 swaps; Pass 2 performs none. Total: 2.

      For selection sort:
        1. Count the exchange performed when the pass minimum is not already in place.
        2. Example on [3,1,2]: pass i=0 swaps 3↔1; pass i=1 swaps 3↔2. Total: 2.

      For quick sort (guarded Lomuto partition):
        1. Count each inner exchange and the final pivot placement only when it is a real
           exchange (positions and values both differ).
        2. Example on [3,1,2] pivot=2: inner exchange 3↔1, then pivot placement 3↔2. Total: 2.
        3. On already-sorted or all-identical input every candidate exchange is a no-op, so
           the count is 0.
    source: [FR4.3]
    validation:
      - "swaps >= 0 for all inputs"
      - "swaps = 0 for already-sorted input (no real exchange is needed, for all three algorithms)"
      - "swaps = 0 for all-identical input (every candidate exchange is a no-op)"
      - "swaps = 0 for single-element or empty input"
      - "swaps is algorithm-specific and NOT directly comparable across algorithms"
    rationale: |
      Swaps are an algorithm-specific metric. Each algorithm naturally produces a different
      swap count for the same input (bubble sort swaps frequently; selection sort less often;
      quick sort varies by partition choice). Excluding no-op exchanges keeps the count
      meaningful and keeps "swaps = 0 on already-sorted input" true for every algorithm —
      in particular for Lomuto quick sort, which would otherwise re-place an already-placed
      pivot. Swaps are educational detail; comparisons is the primary metric (BR2.1).

  - id: BR2.3
    rule_name: "Lexicographic Ordering"
    category: calculation
    description: "Strings are sorted in lexicographic order using the default Unicode comparison operator."
    component: SortingEngine
    applies_to: [AlgorithmResult]
    formal_definition: |
      1. Use Python's default string comparison (<, >, ==) which orders by Unicode code point.
      2. Comparison is case-sensitive: 'A' (0x41) < 'a' (0x61) is true.
      3. Non-ASCII characters are compared by Unicode value: 'ä' (0xE4) vs 'a' (0x61).
    source: [FR2.4]
    validation:
      - "Sorted order matches Python's sorted() on identical input"
    examples:
      - input: ['b', 'A', 'a']
        output: ['A', 'a', 'b']
        note: "Unicode: 'A' (65) < 'a' (97) < 'b' (98)"
      - input: ['café', 'cafe', 'bag']
        output: ['bag', 'cafe', 'café']
        note: "Non-ASCII: 'cafe' (all ASCII) < 'café' (contains ä=U+00E4)"

  - id: BR2.4
    rule_name: "Three Algorithms Only"
    category: constraint
    description: "The SortingEngine implements exactly three algorithms: bubble sort, selection sort, and quick sort. No other algorithms."
    component: SortingEngine
    applies_to: [AlgorithmResult]
    formal_definition: |
      1. SortingEngine.run_all() returns exactly three AlgorithmResult objects.
      2. Algorithms are: bubble (index 0), selection (index 1), quick (index 2).
      3. No additional algorithms are implemented or supported.
      4. Each algorithm is run on the same input (same normalized_strings).
    source: [FR2.1, FR2.2, FR2.3, NFR3.1]
    validation:
      - "run_all() always returns a list of exactly three results"
      - "algorithm field is one of: 'bubble', 'selection', 'quick'"
      - "All three results have the same run_id and normalized input"

  - id: BR2.5
    rule_name: "Sorted-Output Equality"
    category: constraint
    description: "Every algorithm's sorted_strings must equal sorted(normalized_strings) exactly, element for element and in order."
    component: SortingEngine
    applies_to: [AlgorithmResult]
    formal_definition: |
      1. sorted_strings is in ascending Unicode lexicographic order.
      2. sorted_strings == sorted(normalized_strings), compared element-by-element and in order.
      3. Because the elements are strings, equal elements are literally identical; the sorted
         multiset therefore has exactly one achievable order, so the output is uniquely
         determined and internal sort stability is not observable in the result.
    source: [FR3.1, FR2.4, Q4 decision]
    validation:
      - "For identical input, sorted_strings must equal sorted(normalized_strings)"
    rationale: |
      Python's sorted() is stable, and FR3.1 checks an exact order match against it. For a
      list of strings, any correct sort yields the same list, so every correct algorithm
      satisfies this rule regardless of whether its internal implementation is stable.

  - id: BR3.1
    rule_name: "Accuracy Check — Exact Match Against Reference"
    category: verification
    description: "An AlgorithmResult passes the accuracy check if and only if its sorted_strings list exactly matches sorted(SortInput.normalized_strings)."
    component: AccuracyChecker
    applies_to: [AccuracyCheck]
    formal_definition: |
      1. Reference order: computed via Python's built-in sorted(SortInput.normalized_strings).
      2. Check: compare AlgorithmResult.sorted_strings with reference_order element-by-element.
      3. passed = true only if:
         - Both lists have the same length
         - Each element at index i matches (string equality)
      4. Otherwise, passed = false.
    source: [FR3.1, FR3.2, FR3.3]
    validation:
      - "passed is always a boolean (true or false)"
      - "No partial credit: one mismatch → false"
    examples:
      - normalized_strings: ['b', 'a', 'a']
        reference: sorted(normalized_strings) = ['a', 'a', 'b']
        result.sorted_strings: ['a', 'a', 'b']
        passed: true
      - normalized_strings: ['b', 'a', 'a']
        result.sorted_strings: ['a', 'b', 'a']
        passed: false (order mismatch)

  - id: BR3.2
    rule_name: "Independent Algorithm Verification"
    category: verification
    description: "Each algorithm is verified independently; failure of one does not affect or cascade to others."
    component: AccuracyChecker
    applies_to: [AccuracyCheck]
    formal_definition: |
      1. AccuracyChecker.check() is called three times per sort run, once per algorithm.
      2. Each call produces one AccuracyCheck with its own passed boolean.
      3. If bubble sort fails but selection sort passes, all three results are still returned.
      4. No algorithm is skipped or re-run based on another's result.
    source: [FR3.3]
    validation:
      - "Three AccuracyCheck objects always exist for a run, one per algorithm"
      - "Each check is independent and has its own passed value"

  - id: BR4.1
    rule_name: "Data Flow — Run ID Consistency"
    category: constraint
    description: "The run_id flows from SortInput through AlgorithmResult to AccuracyCheck; mismatches indicate a caller defect."
    component: [InputProcessor, SortingEngine, AccuracyChecker]
    applies_to: [SortInput, AlgorithmResult, AccuracyCheck]
    formal_definition: |
      1. InputProcessor generates run_id when creating SortInput.
      2. SortingEngine copies run_id from SortInput into each AlgorithmResult.
      3. AccuracyChecker copies run_id from SortInput and AlgorithmResult into AccuracyCheck.
      4. All three objects with the same run_id belong to one sort execution.
      5. If run_ids do not match, it is a caller error (U2 defect).
    source: [Contract 1]
    validation:
      - "All AlgorithmResult objects from one run_all() call have the same run_id as the input SortInput"
      - "All AccuracyCheck objects for a run have the same run_id as the input SortInput"
    error_handling:
      - "Mismatch is a ValueError (caller defect, not runtime error)"

  - id: BR4.2
    rule_name: "All Algorithms Receive Identical Input"
    category: constraint
    description: "All three algorithms operate on the same normalized_strings; no per-algorithm preprocessing."
    component: SortingEngine
    applies_to: [AlgorithmResult]
    formal_definition: |
      1. SortingEngine.run_all(sort_input) runs bubble, selection, and quick sort on sort_input.normalized_strings.
      2. No per-algorithm filtering, transformation, or normalization.
      3. All three results correspond to the same input.
    source: [FR2.5]
    validation:
      - "Three AlgorithmResult objects all have the same run_id and input reference"
      - "Comparison and swap counts are specific to algorithm, but input is shared"

  - id: BR5.1
    rule_name: "Edge Case — Empty Input"
    category: validation
    description: "Empty input is handled gracefully: returns empty results with zero counts."
    component: [InputProcessor, SortingEngine, AccuracyChecker]
    applies_to: [SortInput, AlgorithmResult, AccuracyCheck]
    formal_definition: |
      1. If normalized_strings is empty (no tokens after normalization):
         - U1 returns three AlgorithmResult objects with empty sorted_strings and zero counts.
         - U2 never calls U1 with empty input; U2 validates and renders the FR6.1 message first.
      2. AccuracyChecker still runs (if called by U2 for testing) and returns passed = true ([] == sorted([])).
    source: [FR6.1, FR6.2]
    validation:
      - "If normalized_strings is empty, result.sorted_strings is empty"
      - "If normalized_strings is empty, result.comparisons = 0 and result.swaps = 0"
      - "If normalized_strings is empty, result.passed = true"

  - id: BR5.2
    rule_name: "Edge Case — Single Element"
    category: validation
    description: "Single-element input requires no comparisons or swaps; output is the input."
    component: [SortingEngine, AccuracyChecker]
    applies_to: [AlgorithmResult, AccuracyCheck]
    formal_definition: |
      1. If normalized_strings has length 1:
         - sorted_strings = normalized_strings (no sorting needed)
         - comparisons = 0 (no element is compared to anything)
         - swaps = 0 (no element is swapped)
      2. AccuracyChecker returns passed = true.
    source: [FR6.2]
    validation:
      - "Single-element input always produces zero comparisons and zero swaps"
      - "sorted_strings = normalized_strings"
    examples:
      - normalized_strings: ['hello']
        sorted_strings: ['hello']
        comparisons: 0
        swaps: 0

  - id: BR5.3
    rule_name: "Edge Case — All Identical Strings"
    category: validation
    description: "When all input strings are identical, no real exchange is performed; comparison counts follow each algorithm and swaps stay 0."
    component: [SortingEngine, AccuracyChecker]
    applies_to: [AlgorithmResult, AccuracyCheck]
    formal_definition: |
      1. If all strings in normalized_strings are identical (a == b for all pairs):
         - sorted_strings = normalized_strings (order is unobservable across identical values)
         - swaps = 0 for all three algorithms (every candidate exchange is a no-op)
         - comparisons follow each algorithm's definition (bubble and selection: n*(n-1)/2; quick: as traced)
      2. AccuracyChecker returns passed = true.
    source: [FR6.3]
    validation:
      - "Identical input produces zero swaps for all three algorithms"
      - "sorted_strings equals the input list"
    examples:
      - normalized_strings: ['apple', 'apple', 'apple']
        sorted_strings: ['apple', 'apple', 'apple']
        swaps: 0
        bubble_comparisons: 3
        selection_comparisons: 3
        quick_comparisons: 3
```

---

## Rules Summary Table

| Rule ID | Rule Name | Component | Category | Source | Validation |
|---|---|---|---|---|---|
| BR1.1 | Input Normalization | InputProcessor | calculation | FR1.3, FR1.4, D10 | Deterministic; duplicates preserved; ASCII only lowercased |
| BR1.2 | Empty String Handling | InputProcessor | validation | FR6.4 | Empty tokens dropped; U2 validates non-empty |
| BR1.3 | Run Identifier Generation | InputProcessor | calculation | Contract 1 | Unique; immutable; copied to results |
| BR2.1 | Comparison Counting | SortingEngine | calculation | FR4.1, FR4.2 | Same definition for all three algorithms; directly comparable |
| BR2.2 | Swap Counting | SortingEngine | calculation | FR4.3 | Algorithm-specific; no-op exchanges excluded; secondary metric |
| BR2.3 | Lexicographic Ordering | SortingEngine | calculation | FR2.4 | Unicode default ordering |
| BR2.4 | Three Algorithms Only | SortingEngine | constraint | NFR3.1 | Bubble, selection, quick only |
| BR2.5 | Sorted-Output Equality | SortingEngine | constraint | FR3.1, Q4 | sorted_strings equals sorted(normalized_strings) |
| BR3.1 | Accuracy Check — Exact Match | AccuracyChecker | verification | FR3.1, FR3.2 | No partial credit; must match sorted() exactly |
| BR3.2 | Independent Verification | AccuracyChecker | verification | FR3.3 | Each algorithm checked independently |
| BR4.1 | Run ID Consistency | Integration | constraint | Contract 1 | run_id flows from SortInput through results |
| BR4.2 | Identical Input to All Algorithms | SortingEngine | constraint | FR2.5 | All three receive same normalized_strings |
| BR5.1 | Empty Input | InputProcessor, SortingEngine | validation | FR6.1, FR6.2 | Empty results with zero counts; U2 validates |
| BR5.2 | Single Element | SortingEngine, AccuracyChecker | validation | FR6.2 | Zero comparisons; zero swaps; output = input |
| BR5.3 | All Identical Strings | SortingEngine, AccuracyChecker | validation | FR6.3 | Zero swaps; output equals input |

---

## Traceability — Rules to Requirements

| Requirement | Related Rules | Rationale |
|---|---|---|
| FR1.3 (Input normalization) | BR1.1, BR1.2 | Defines the exact normalization algorithm |
| FR1.4 (Preserve original forms) | BR1.1 | Duplicates preserved; characters unchanged except ASCII capitals |
| FR2.1–FR2.3 (Three algorithms) | BR2.4, BR2.1, BR2.2, BR2.5 | Algorithms defined; counting rules specified |
| FR2.4 (Lexicographic order) | BR2.3 | Unicode default comparison |
| FR2.5 (Same input for all) | BR4.2 | All algorithms operate on identical input |
| FR3.1 (Accuracy verification) | BR3.1, BR2.5 | Exact-match check against sorted() |
| FR3.2–FR3.3 (Pass/fail per algorithm) | BR3.1, BR3.2 | Independent checks; boolean result |
| FR4.1 (Textbook step counting) | BR2.1 | Comparisons defined consistently for all three |
| FR4.2 (Comparable primary count) | BR2.1 | Comparisons is the single comparable metric |
| FR4.3 (Swap counts separately) | BR2.2 | Swaps tracked independently; secondary metric |
| FR4.5 (Edge cases) | BR5.1, BR5.2, BR5.3 | Empty, single, identical cases handled correctly |
| FR6.1 (Empty input message) | BR1.2, BR5.1 | U2 validates; U1 returns empty results if called |
| FR6.2 (Single element) | BR5.2 | Zero comparisons and swaps; output = input |
| FR6.3 (All identical) | BR5.3 | Zero swaps; output equals input |
| FR6.4 (Empty token dropping) | BR1.2 | Implemented in normalization |
| NFR3.1 (Only bubble, selection, quick) | BR2.4 | Constraint enforced |
| NFR4.2 (80% coverage) | BR2.1, BR3.1, BR5.1, BR5.2, BR5.3 | Rules define testable behavior |
