# Business Rules — U1 sorting-core

Formal specification of domain rules, constraints, and validation logic. Each rule is identified by `BR<component>.<n>` for traceability.

## YAML Source of Truth

```yaml
business_rules:
  - rule_id: BR-INP-1
    rule_name: "Input Normalization"
    category: data_transformation
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
      - "len(normalized_strings) <= len(raw_entries)"
      - "All strings in normalized_strings are non-empty"
      - "No duplicates are removed"
      - "ASCII capitals A-Z are always lowercased; non-ASCII characters are unchanged"
    examples:
      - raw_entries: ["Alice", "bob", "", "Alice", "cäfe"]
        normalized_strings: ["alice", "bob", "alice", "café"]
        note: "Empty token removed; cäfe unchanged (non-ASCII ä passes through); Alice lowercased"
      - raw_entries: ["HELLO,world\nnew line"]
        normalized_strings: ["hello", "world", "new", "line"]
        note: "Split on comma and newline"

  - rule_id: BR-INP-2
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

  - rule_id: BR-INP-3
    rule_name: "Run Identifier Generation"
    category: identification
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

  - rule_id: BR-SE-1
    rule_name: "Comparison Counting — Single Definition for All Algorithms"
    category: metric
    description: "All three algorithms count element comparisons identically: every time two elements are compared (tested for order), the count increments."
    component: SortingEngine
    applies_to: [AlgorithmResult]
    formal_definition: |
      For each algorithm:
        1. Increment comparisons counter every time two elements are compared with <, >, <=, >=, or == operators.
        2. This includes all comparisons in outer loops, inner loops, recursion, and partitioning.
        3. The comparison is counted regardless of outcome (true or false).
        4. Do NOT count array accesses, assignments, or other operations — only element-to-element comparisons.
      
      Example for bubble sort on [3, 1, 2]:
        - Pass 1: compare 3>1 (count=1), swap; compare 1>2 (count=2), no swap
        - Pass 2: compare 3>1 (count=3), swap; compare 1>2 (count=4), no swap
        - Pass 3: compare 3>1 (count=5), swap
        - Total comparisons: 5
      
      Example for selection sort on [3, 1, 2]:
        - Find min in [3,1,2]: compare 3>1 (count=1), compare 1>2 (count=2), swap with 3 → [1,3,2]
        - Find min in [3,2]: compare 3>2 (count=3), swap with 3 → [1,2,3]
        - Find min in [3]: no comparisons
        - Total comparisons: 3
      
      Example for quick sort on [3, 1, 2] with Lomuto partition:
        - Partition around pivot 2: compare 3>2 (count=1), compare 1<2 (count=2), swap; no more comparisons
        - Partition left [1]: no comparisons
        - Partition right [3]: no comparisons
        - Total comparisons: 2
    source: [FR4.1, FR4.2]
    validation:
      - "comparisons >= 0 for all inputs"
      - "comparisons = 0 for empty or single-element input"
      - "comparisons is the same across runs with identical input and algorithm (deterministic)"
      - "comparisons is directly comparable across all three algorithms (same definition)"
    rationale: |
      FR4.2 explicitly requires "total element comparisons must be used as the primary comparable count for UI display across all three algorithms (to enable direct comparison)."
      A single, consistent definition ensures that comparison counts are fair to compare between bubble sort, selection sort, and quick sort.

  - rule_id: BR-SE-2
    rule_name: "Swap Counting — Algorithm-Specific, Secondary Metric"
    category: metric
    description: "Swaps are counted per algorithm's natural definition; swaps are a secondary metric not directly comparable across algorithms."
    component: SortingEngine
    applies_to: [AlgorithmResult]
    formal_definition: |
      For bubble sort:
        1. Count every swap of adjacent elements when they are out of order.
        2. Adjacent means indices i and i+1.
        3. Example on [3,1,2]: Pass 1 has 1 swap (3↔1); Pass 2 has 1 swap (3↔2); Pass 3 has 1 swap (3↔2) = 3 swaps total.
      
      For selection sort:
        1. Count every swap after finding the minimum in a pass.
        2. Typically one swap per pass (unless the minimum is already in place, then 0).
        3. Example on [3,1,2]: Find min=1, swap with 3 (count=1); Find min=2, swap with 3 (count=1); Find min=3, already in place (count=0) = 2 swaps total.
      
      For quick sort (Lomuto partition):
        1. Count every swap during partitioning.
        2. Example on [3,1,2] pivot=2: Swap 3↔2 (count=1), then partitions [1] and [3] have no swaps = 1 swap total.
    source: [FR4.3]
    validation:
      - "swaps >= 0 for all inputs"
      - "swaps = 0 for already-sorted input (no swaps needed)"
      - "swaps = 0 for single-element or empty input"
      - "swaps is algorithm-specific and NOT directly comparable across algorithms"
    rationale: |
      Swaps are an algorithm-specific metric. Each algorithm naturally produces a different swap count
      for the same input (bubble sort swaps frequently; selection sort less often; quick sort varies by partition choice).
      Swaps are educational detail, not the primary comparison metric (comparisons is primary per BR-SE-1).

  - rule_id: BR-SE-3
    rule_name: "Lexicographic Ordering"
    category: algorithm
    description: "Strings are sorted in lexicographic order using the default Unicode comparison operator."
    component: SortingEngine
    applies_to: [AlgorithmResult]
    formal_definition: |
      1. Use Python's default string comparison (<, >, ==) which orders by Unicode code point.
      2. Comparison is case-sensitive: 'a' (0x61) < 'A' (0x41) is false; 'A' (0x41) < 'a' (0x61) is true.
      3. Non-ASCII characters are compared by Unicode value: 'ä' (0xE4) vs 'a' (0x61).
      4. Sorting is stable: when two strings are equal, they maintain their input order.
    source: [FR2.4]
    validation:
      - "Sorted order matches Python's sorted() on identical input"
      - "Stable sort semantics: duplicates preserve input order"
    examples:
      - input: ['b', 'A', 'a']
        output: ['A', 'a', 'b']
        note: "Unicode: 'A' (65) < 'a' (97) < 'b' (98)"
      - input: ['café', 'cafe', 'bag']
        output: ['bag', 'cafe', 'café']
        note: "Non-ASCII: 'cafe' (all ASCII) < 'café' (contains non-ASCII ä=U+00E4)"

  - rule_id: BR-SE-4
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

  - rule_id: BR-SE-5
    rule_name: "Stable Sort Semantics"
    category: algorithm
    description: "All three algorithms must produce stable output: identical elements appear in their input order."
    component: SortingEngine
    applies_to: [AlgorithmResult]
    formal_definition: |
      1. When two strings compare equal (a == b in Unicode), they remain in input order.
      2. This means the sorted_strings list preserves the relative position of duplicates from normalized_strings.
      3. Example: if normalized_strings = ['apple', 'apple', 'banana'], 
                 sorted_strings = ['apple', 'apple', 'banana']
                 (the two 'apple' instances maintain their original order).
    source: [FR3.1 (requires exact match vs sorted()), Q4 decision]
    validation:
      - "For identical input, sorted_strings must equal sorted(normalized_strings)"
      - "Duplicates must appear in the same relative order as the input"
    rationale: |
      Python's sorted() is stable. To pass FR3.1 accuracy checks (exact order match),
      all three algorithms must be stable or at minimum must match Python's order on identical elements.

  - rule_id: BR-AC-1
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
         - Order is preserved (including duplicates)
      4. Otherwise, passed = false.
    source: [FR3.1, FR3.2, FR3.3]
    validation:
      - "passed is always a boolean (true or false)"
      - "No partial credit: one mismatch → false"
      - "Stable sort order must match (duplicates in original order)"
    examples:
      - normalized_strings: ['b', 'a', 'a']
        reference: sorted(normalized_strings) = ['a', 'a', 'b']
        result.sorted_strings: ['a', 'a', 'b']
        passed: true
      - normalized_strings: ['b', 'a', 'a']
        result.sorted_strings: ['a', 'b', 'a']
        passed: false (order mismatch on duplicates)

  - rule_id: BR-AC-2
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

  - rule_id: BR-WLP-1
    rule_name: "Bundled Word List — Fixed and Immutable"
    category: data_ownership
    description: "The word list is fixed at application startup and does not change during runtime."
    component: WordListProvider
    applies_to: [BundledWordList]
    formal_definition: |
      1. BundledWordList.words is defined and packaged with the application code (not loaded from external source).
      2. The list is non-empty (at least one word).
      3. The list is immutable: no modification, insertion, or deletion at runtime.
      4. All words are strings; may include duplicates.
    source: [FR1.5, NFR2.3]
    validation:
      - "words list is defined in code (constants.py or similar)"
      - "words is non-empty on every access"
      - "No file I/O, no network access, no dynamic updates"
    examples:
      - words: ['apple', 'banana', 'cherry', 'date', 'elephant', 'fig', 'grape', 'house']
        list_version: 'v1.0'

  - rule_id: BR-INT-1
    rule_name: "Data Flow — Run ID Consistency"
    category: integration
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

  - rule_id: BR-INT-2
    rule_name: "All Algorithms Receive Identical Input"
    category: integration
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

  - rule_id: BR-EDGE-1
    rule_name: "Edge Case — Empty Input"
    category: edge_case
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

  - rule_id: BR-EDGE-2
    rule_name: "Edge Case — Single Element"
    category: edge_case
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

  - rule_id: BR-EDGE-3
    rule_name: "Edge Case — All Identical Strings"
    category: edge_case
    description: "When all input strings are identical, no swaps are needed; comparisons depend on algorithm."
    component: [SortingEngine, AccuracyChecker]
    applies_to: [AlgorithmResult, AccuracyCheck]
    formal_definition: |
      1. If all strings in normalized_strings are identical (a == b for all pairs):
         - sorted_strings = normalized_strings (preserved in input order)
         - swaps = 0 (no swaps needed; already in order)
         - comparisons >= 0 (algorithm still performs comparisons; see examples)
      2. AccuracyChecker returns passed = true.
    source: [FR6.3]
    validation:
      - "Identical input produces zero swaps"
      - "sorted_strings preserves input order"
    examples:
      - normalized_strings: ['apple', 'apple', 'apple']
        sorted_strings: ['apple', 'apple', 'apple']
        swaps: 0
        bubble_comparisons: 6 (still compares all pairs even if equal)
        selection_comparisons: 3 (finds min in each pass)
```

---

## Rules Summary Table

| Rule ID | Rule Name | Component | Category | Source | Validation |
|---|---|---|---|---|---|
| BR-INP-1 | Input Normalization | InputProcessor | data_transformation | FR1.3, FR1.4, D10 | Deterministic; duplicates preserved; ASCII only lowercased |
| BR-INP-2 | Empty String Handling | InputProcessor | validation | FR6.4 | Empty tokens dropped; U2 validates non-empty |
| BR-INP-3 | Run Identifier Generation | InputProcessor | identification | Contract 1 | Unique; immutable; copied to results |
| BR-SE-1 | Comparison Counting | SortingEngine | metric | FR4.1, FR4.2 | Same definition for all three algorithms; directly comparable |
| BR-SE-2 | Swap Counting | SortingEngine | metric | FR4.3 | Algorithm-specific; secondary metric |
| BR-SE-3 | Lexicographic Ordering | SortingEngine | algorithm | FR2.4 | Unicode default; stable sort |
| BR-SE-4 | Three Algorithms Only | SortingEngine | constraint | NFR3.1 | Bubble, selection, quick only |
| BR-SE-5 | Stable Sort Semantics | SortingEngine | algorithm | FR3.1, Q4 | Duplicates preserve input order |
| BR-AC-1 | Accuracy Check — Exact Match | AccuracyChecker | verification | FR3.1, FR3.2 | No partial credit; must match sorted() exactly |
| BR-AC-2 | Independent Verification | AccuracyChecker | verification | FR3.3 | Each algorithm checked independently |
| BR-WLP-1 | Bundled Word List — Immutable | WordListProvider | data_ownership | FR1.5, NFR2.3 | Non-empty; no external source; no runtime modification |
| BR-INT-1 | Run ID Consistency | Integration | integration | Contract 1 | run_id flows from SortInput through results |
| BR-INT-2 | Identical Input to All Algorithms | SortingEngine | integration | FR2.5 | All three receive same normalized_strings |
| BR-EDGE-1 | Empty Input | InputProcessor, SortingEngine | edge_case | FR6.1, FR6.2 | Empty results with zero counts; U2 validates |
| BR-EDGE-2 | Single Element | SortingEngine, AccuracyChecker | edge_case | FR6.2 | Zero comparisons; zero swaps; output = input |
| BR-EDGE-3 | All Identical Strings | SortingEngine, AccuracyChecker | edge_case | FR6.3 | Zero swaps; input order preserved |

---

## Traceability — Rules to Requirements

| Requirement | Related Rules | Rationale |
|---|---|---|
| FR1.3 (Input normalization) | BR-INP-1, BR-INP-2 | Defines the exact normalization algorithm |
| FR1.4 (Preserve original forms) | BR-INP-1 | Duplicates preserved; characters unchanged except ASCII capitals |
| FR2.1–FR2.3 (Three algorithms) | BR-SE-4, BR-SE-1, BR-SE-2, BR-SE-5 | Algorithms defined; counting rules specified |
| FR2.4 (Lexicographic order) | BR-SE-3 | Unicode default comparison |
| FR2.5 (Same input for all) | BR-INT-2 | All algorithms operate on identical input |
| FR3.1 (Accuracy verification) | BR-AC-1, BR-SE-5 | Exact-match check against sorted() with stable sort |
| FR3.2–FR3.3 (Pass/fail per algorithm) | BR-AC-1, BR-AC-2 | Independent checks; boolean result |
| FR4.1 (Textbook step counting) | BR-SE-1 | Comparisons defined consistently for all three |
| FR4.2 (Comparable primary count) | BR-SE-1 | Comparisons is the single comparable metric |
| FR4.3 (Swap counts separately) | BR-SE-2 | Swaps tracked independently; secondary metric |
| FR4.5 (Edge cases) | BR-EDGE-1, BR-EDGE-2, BR-EDGE-3 | Empty, single, identical cases handled correctly |
| FR6.1 (Empty input message) | BR-INP-2, BR-EDGE-1 | U2 validates; U1 returns empty results if called |
| FR6.2 (Single element) | BR-EDGE-2 | Zero comparisons and swaps; output = input |
| FR6.3 (All identical) | BR-EDGE-3 | Zero swaps; input order preserved |
| FR6.4 (Empty token dropping) | BR-INP-2 | Implemented in normalization |
| NFR3.1 (Only bubble, selection, quick) | BR-SE-4 | Constraint enforced |
| NFR4.2 (80% coverage) | BR-SE-1, BR-AC-1, BR-EDGE-* | Rules define testable behavior |
