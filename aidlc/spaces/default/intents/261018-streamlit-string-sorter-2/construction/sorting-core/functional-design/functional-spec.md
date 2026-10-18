# Functional Design Specification — U1 sorting-core

Complete behavioral specification including workflows, state transitions, sequence diagrams, and functional flows.

---

## Part 1: Workflow Overview

The sorting-core unit provides a pure domain API consumed by the playground-ui (U2). The workflow has three main paths:

1. **Normalization Path**: Raw entries → normalized SortInput
2. **Sorting Path**: SortInput → three AlgorithmResult objects
3. **Verification Path**: AlgorithmResult + SortInput → AccuracyCheck

All three paths are called in sequence by U2 on each Sort button press.

---

## Part 2: Core Workflows

### Workflow 1: Input Normalization

**Trigger**: U2 calls `InputProcessor.normalize(raw_entries)`

**Input**:
- `raw_entries`: list of strings (may contain empty strings, duplicates, mixed case, non-ASCII characters)

**Output**:
- `SortInput` object with `run_id`, `raw_entries`, and `normalized_strings`

**Steps**:
```
normalize(raw_entries):
  1. Generate a unique run_id (UUID or timestamp)
  2. Initialize normalized_strings as empty list
  3. For each entry in raw_entries:
    3.1. Split entry on '\n' and ',' to produce tokens
    3.2. For each token:
      3.2.1. Trim leading and trailing whitespace
      3.2.2. If token is empty after trim, skip it (drop it)
      3.2.3. If token is non-empty:
        - For each character in token:
          - If character is ASCII capital (A-Z), lowercase it
          - Otherwise, keep the character unchanged
        - Add the processed token to normalized_strings
  4. Return SortInput(run_id, raw_entries, normalized_strings)
```

**Postconditions**:
- `SortInput.run_id` is unique and immutable
- `SortInput.normalized_strings` has length <= `len(raw_entries)`
- All strings in `normalized_strings` are non-empty
- ASCII capitals are lowercased; non-ASCII pass through unchanged
- Duplicates are preserved

**Errors**:
- TypeError if `raw_entries` is not a list of strings (caller defect)

**Example**:
```
Input:  ["Hello,WORLD", "test", "", "café"]
Output: SortInput(
  run_id="550e8400-...",
  raw_entries=["Hello,WORLD", "test", "", "café"],
  normalized_strings=["hello", "world", "test", "café"]
)
```

---

### Workflow 2: Run All Three Algorithms

**Trigger**: U2 calls `SortingEngine.run_all(sort_input)`

**Input**:
- `sort_input`: SortInput object

**Output**:
- List of three AlgorithmResult objects (bubble, selection, quick)

**Steps**:
```
run_all(sort_input):
  1. Extract normalized_strings from sort_input
  2. Initialize results as empty list
  3. For each algorithm in [bubble, selection, quick]:
    3.1. Call algorithm(normalized_strings) to get sorted_list, comparisons, swaps
    3.2. Create AlgorithmResult(
          run_id=sort_input.run_id,
          algorithm=algorithm_name,
          sorted_strings=sorted_list,
          comparisons=comparisons,
          swaps=swaps
        )
    3.3. Append result to results list
  4. Return results
```

**Per-Algorithm Workflows**:

#### Bubble Sort
```
bubble_sort(strings):
  comparisons = 0
  swaps = 0
  output = copy(strings)
  n = len(output)
  
  for i in range(n):
    for j in range(n - 1 - i):
      comparisons += 1  # Compare elements at j and j+1
      if output[j] > output[j+1]:
        swap(output[j], output[j+1])
        swaps += 1
  
  return output, comparisons, swaps
```

**Characteristics**:
- Time: O(n²) comparisons regardless of input order
- Comparisons for n elements: n*(n-1)/2 on average
- Swaps: 0 (sorted), up to n*(n-1)/2 (reverse sorted)
- Stable: Yes (only swaps when strictly greater)

#### Selection Sort
```
selection_sort(strings):
  comparisons = 0
  swaps = 0
  output = copy(strings)
  n = len(output)
  
  for i in range(n - 1):
    min_idx = i
    for j in range(i + 1, n):
      comparisons += 1  # Compare output[j] with output[min_idx]
      if output[j] < output[min_idx]:
        min_idx = j
    if min_idx != i:
      swap(output[i], output[min_idx])
      swaps += 1
  
  return output, comparisons, swaps
```

**Characteristics**:
- Time: O(n²) comparisons regardless of input order
- Comparisons for n elements: exactly n*(n-1)/2
- Swaps: 0 (sorted), up to n-1 (reverse sorted)
- Stable: No (in-place swaps of non-adjacent elements). **CORRECTION**: Use stable variant or track original indices.
- **Implementation note**: For this educational tool, comparisons count is the standard n*(n-1)/2 regardless of duplicates.

**Stable Implementation Variant**:
```
selection_sort_stable(strings):
  # Use temporary list to maintain stability
  comparisons = 0
  swaps = 0  # Note: "swaps" here counts write operations, not element exchanges
  output = list(strings)
  n = len(output)
  
  for i in range(n - 1):
    min_idx = i
    for j in range(i + 1, n):
      comparisons += 1
      if output[j] < output[min_idx]:
        min_idx = j
    # Shift elements, not swap
    if min_idx != i:
      min_val = output[min_idx]
      for k in range(min_idx, i, -1):
        output[k] = output[k-1]
        swaps += 1
      output[i] = min_val
  
  return output, comparisons, swaps
```

#### Quick Sort (Lomuto Partition)
```
quick_sort(strings):
  comparisons = [0]  # Use list to allow modification in nested function
  swaps = [0]
  output = copy(strings)
  
  def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
      comparisons[0] += 1  # Compare arr[j] with pivot
      if arr[j] < pivot:
        i += 1
        swap(arr[i], arr[j])
        swaps[0] += 1
    swap(arr[i+1], arr[high])
    swaps[0] += 1
    return i + 1
  
  def quicksort_helper(arr, low, high):
    if low < high:
      pi = partition(arr, low, high)
      quicksort_helper(arr, low, pi - 1)
      quicksort_helper(arr, pi + 1, high)
  
  if len(output) > 0:
    quicksort_helper(output, 0, len(output) - 1)
  
  return output, comparisons[0], swaps[0]
```

**Characteristics**:
- Time: O(n log n) average, O(n²) worst case
- Comparisons: varies based on pivot choice; average O(n log n)
- Swaps: typically fewer than bubble sort
- Stable: No (partitioning moves elements)
- **Implementation note**: Lomuto partition is chosen for predictability.

**Postconditions for all algorithms**:
- `sorted_strings` is in lexicographic (Unicode) order
- `sorted_strings` uses stable sort semantics (duplicates preserve input order)
- `len(sorted_strings)` == `len(normalized_strings)`
- `comparisons >= 0`, `swaps >= 0`
- `comparisons = 0` and `swaps = 0` for empty or single-element input
- All elements from `normalized_strings` appear in `sorted_strings` (no loss or duplication)

**Errors**:
- TypeError if `sort_input` is not a SortInput object (caller defect)

**Example**:
```
Input:  SortInput(run_id="550e8400-...", normalized_strings=["charlie", "apple", "bob"])
Output: [
  AlgorithmResult(run_id="550e8400-...", algorithm="bubble", 
                  sorted_strings=["apple", "bob", "charlie"], 
                  comparisons=3, swaps=2),
  AlgorithmResult(run_id="550e8400-...", algorithm="selection", 
                  sorted_strings=["apple", "bob", "charlie"], 
                  comparisons=3, swaps=2),
  AlgorithmResult(run_id="550e8400-...", algorithm="quick", 
                  sorted_strings=["apple", "bob", "charlie"], 
                  comparisons=2, swaps=2)
]
```

---

### Workflow 3: Verify Accuracy

**Trigger**: U2 calls `AccuracyChecker.check(algorithm_result, sort_input)` (three times per run)

**Input**:
- `algorithm_result`: AlgorithmResult object
- `sort_input`: SortInput object (contains the reference normalized_strings)

**Output**:
- AccuracyCheck object with `run_id`, `algorithm`, and `passed` boolean

**Steps**:
```
check(algorithm_result, sort_input):
  1. Compute reference: reference_order = sorted(sort_input.normalized_strings)
  2. Get result: result_order = algorithm_result.sorted_strings
  3. Compare:
    3.1. If len(result_order) != len(reference_order):
      return AccuracyCheck(run_id, algorithm, passed=False)
    3.2. For each index i in range(len(reference_order)):
      if result_order[i] != reference_order[i]:
        return AccuracyCheck(run_id, algorithm, passed=False)
    3.3. If all elements match:
      return AccuracyCheck(run_id, algorithm, passed=True)
```

**Postconditions**:
- `AccuracyCheck.passed` is True only if `sorted_strings == sorted(normalized_strings)` exactly
- Comparison includes order (stable sort required)
- Each algorithm is verified independently

**Errors**:
- ValueError if `algorithm_result.run_id != sort_input.run_id` (data consistency error)
- TypeError if inputs are not the expected types (caller defect)

**Example**:
```
Input:  AlgorithmResult(run_id="550e8400-...", algorithm="bubble", 
                        sorted_strings=["apple", "bob", "charlie"]),
        SortInput(run_id="550e8400-...", normalized_strings=["charlie", "apple", "bob"])

Output: AccuracyCheck(run_id="550e8400-...", algorithm="bubble", passed=True)
```

---

## Part 3: Integration Sequence

### Complete Sort Run Sequence

**Trigger**: U2 calls the pipeline on Sort button press

**Sequence**:
```
SortingPlaygroundApp.on_sort_pressed():
  1. Collect typed entries and picked words from UI widgets
  2. Combine into raw_entries list
  3. Call InputProcessor.normalize(raw_entries)
  4. If SortInput.normalized_strings is empty:
    4.1. [U2 handles — not shown here]
  5. Call SortingEngine.run_all(sort_input)
    5.1. Returns list of three AlgorithmResult objects
  6. For each result in results:
    6.1. Call AccuracyChecker.check(result, sort_input)
    6.2. Append AccuracyCheck to checks list
  7. [U2 renders: input echo, three columns with results and checks]
```

---

## Part 4: Sequence Diagrams

### Diagram 1: Happy Path (Non-Empty Input)

```
U2 (Caller)         InputProcessor      SortingEngine       AccuracyChecker
  |                      |                    |                    |
  +--normalize()--------->|                    |                    |
  |                       |                    |                    |
  |<---SortInput(ok)------+                    |                    |
  |                                            |                    |
  +--run_all(sort_input)----------------------->|                   |
  |                                            |                    |
  |<---[bubble, selection, quick results]-----+                    |
  |                                                                 |
  +--check(result[0], sort_input)-------------------------------->|
  |                                                                 |
  |<---AccuracyCheck(passed=bool)------------------------+         |
  |                                                       |         |
  +--check(result[1], sort_input)-------------------------------->|
  |                                                                 |
  |<---AccuracyCheck(passed=bool)------------------------+         |
  |                                                       |         |
  +--check(result[2], sort_input)-------------------------------->|
  |                                                                 |
  |<---AccuracyCheck(passed=bool)------------------------+         |
  |                                                       |         |
  +---Render results------->|
```

Text fallback: U2 calls normalize(), receives a SortInput. Calls run_all() on SortingEngine, receives three AlgorithmResult objects. Calls check() on AccuracyChecker three times (once per algorithm), receives three AccuracyCheck objects. Renders all results.

### Diagram 2: Empty Input (U2 Validation)

```
U2 (Caller)         InputProcessor
  |                      |
  | [Check if raw_entries is empty]
  |
  | [Yes → Render FR6.1 message and stop]
  | [No → Proceed]
  |
  +--normalize()--------->|
  |                       |
  |<---SortInput(ok)------+
  |
  [Continue to run_all() and check()]
```

Text fallback: U2 validates empty input before calling InputProcessor. If empty, renders the FR6.1 message. If not, proceeds to normalize().

---

## Part 5: State Transitions and Conditions

### Comparison Counting State Machine

```
State: Start
  → Call compare(a, b)
  → comparisons++
  → State: Compare (outcome true or false doesn't matter)

State: Compare
  → Continue to next comparison in algorithm
  → State: Start (next iteration)

State: End (no more comparisons)
  → Algorithm complete
  → Return comparisons count
```

### Swap Counting State Machine (Bubble Sort Example)

```
State: Start iteration
  → For each adjacent pair (j, j+1)
  → Call compare(output[j], output[j+1])
  → comparisons++
  
  → If output[j] > output[j+1]:
    → swap(output[j], output[j+1])
    → swaps++
    → State: Swapped
  
  → Else:
    → State: No swap
  
  → Next pair or end
```

---

## Part 6: Edge Case Behaviors

### Edge Case 1: Empty Input

**Behavior**:
```
normalize([]) → SortInput(run_id, [], [])
run_all(SortInput([], [])) → [
  AlgorithmResult(run_id, bubble, [], 0, 0),
  AlgorithmResult(run_id, selection, [], 0, 0),
  AlgorithmResult(run_id, quick, [], 0, 0)
]
check(AlgorithmResult([], 0, 0), SortInput([])) → AccuracyCheck(run_id, algorithm, passed=True)
```

**Rationale**: Empty input is valid; U2 prevents empty results via FR6.1 message (no call to U1).

### Edge Case 2: Single Element

**Behavior**:
```
normalize(['hello']) → SortInput(run_id, ['hello'], ['hello'])
run_all(SortInput(['hello'])) → [
  AlgorithmResult(run_id, bubble, ['hello'], 0, 0),
  AlgorithmResult(run_id, selection, ['hello'], 0, 0),
  AlgorithmResult(run_id, quick, ['hello'], 0, 0)
]
check(AlgorithmResult(['hello'], 0, 0), SortInput(['hello'])) → AccuracyCheck(run_id, algorithm, passed=True)
```

**Rationale**: Single element is already sorted; no comparisons or swaps.

### Edge Case 3: All Identical Strings

**Behavior**:
```
normalize(['apple', 'apple', 'apple']) 
  → SortInput(run_id, ['apple', 'apple', 'apple'], ['apple', 'apple', 'apple'])

run_all(SortInput(['apple', 'apple', 'apple'])) → [
  AlgorithmResult(run_id, bubble, ['apple', 'apple', 'apple'], 3, 0),
    # 3 comparisons: (0,1), (1,2), then (0,1) again; no swaps
  AlgorithmResult(run_id, selection, ['apple', 'apple', 'apple'], 3, 0),
    # 3 comparisons: (1 vs 0), (2 vs 0), (2 vs 1); no swaps (already min)
  AlgorithmResult(run_id, quick, ['apple', 'apple', 'apple'], >=1, 0+)
    # Partitioning still occurs; swaps may occur (implementation-dependent on pivot)
]

check(AlgorithmResult(['apple', 'apple', 'apple'], 3, 0), SortInput(['apple', 'apple', 'apple'])) 
  → AccuracyCheck(run_id, algorithm, passed=True)
```

**Rationale**: Identical strings do not need to be reordered, so swaps should be 0. Comparisons still occur (algorithms still execute).

### Edge Case 4: Two Elements (Minimal Sort)

**Behavior**:
```
normalize(['bob', 'apple']) 
  → SortInput(run_id, ['bob', 'apple'], ['bob', 'apple'])

run_all(SortInput(['bob', 'apple'])) → [
  AlgorithmResult(run_id, bubble, ['apple', 'bob'], 1, 1),
  AlgorithmResult(run_id, selection, ['apple', 'bob'], 1, 1),
  AlgorithmResult(run_id, quick, ['apple', 'bob'], 1, 1)
]
```

**Rationale**: Two elements require exactly one comparison; if out of order, one swap.

### Edge Case 5: Already Sorted Input

**Behavior**:
```
normalize(['apple', 'banana', 'cherry']) 
  → SortInput(run_id, [...], ['apple', 'banana', 'cherry'])

run_all(SortInput(['apple', 'banana', 'cherry'])) → [
  AlgorithmResult(run_id, bubble, ['apple', 'banana', 'cherry'], 3, 0),
    # Bubble: 3 comparisons; 0 swaps (all in order)
  AlgorithmResult(run_id, selection, ['apple', 'banana', 'cherry'], 3, 0),
    # Selection: 3 comparisons; 0 swaps (already selected)
  AlgorithmResult(run_id, quick, ['apple', 'banana', 'cherry'], 2, 0)
    # Quick: 2 comparisons; 0 swaps (pivot choice dependent)
]
```

**Rationale**: Comparisons occur but no swaps needed.

### Edge Case 6: Duplicates with Mixed Order

**Behavior**:
```
normalize(['bob', 'alice', 'bob', 'alice']) 
  → SortInput(run_id, [...], ['bob', 'alice', 'bob', 'alice'])

run_all(SortInput(['bob', 'alice', 'bob', 'alice'])) → [
  AlgorithmResult(run_id, bubble, ['alice', 'alice', 'bob', 'bob'], comparisons, swaps),
    # Duplicates maintain input order: first 'bob' stays before first 'alice' initially... 
    # WAIT: bubble sort will move all 'alice's to front
    # Input: [bob, alice, bob, alice]
    # After sort: [alice, alice, bob, bob]
    # The two alice's appear as: position 0 = alice (from index 1), position 1 = alice (from index 3)
    # This is stable: the first alice (index 1) comes before the second alice (index 3)
  AlgorithmResult(...),
  AlgorithmResult(...)
]
```

**Rationale**: Stable sort preserves relative order of duplicates.

---

## Part 7: Derived Business Rules Summary

| Rule | Derivation |
|---|---|
| Each algorithm outputs sorted_strings in lexicographic order | Follows Python's default string comparison |
| Comparisons are the primary metric (FR4.2) | Single, consistent definition enables direct comparison |
| Swaps are algorithm-specific | Each algorithm has different natural swap counts |
| Accuracy check is deterministic | Exact match against sorted() is reproducible |
| Empty input returns empty results | Edge case; caller (U2) prevents empty input from reaching the UI |
| Stable sort is required | Python's sorted() is stable; accuracy check requires exact-order match |

---

## Part 8: Data Flow Diagram

```
U2 Input       InputProcessor        SortingEngine         AccuracyChecker
  (raw)             |                      |                    |
    |               |                      |                    |
    +--normalize()--→ SortInput            |                    |
    |               |                      |                    |
    ←---SortInput---+                      |                    |
    |                                      |                    |
    +----------run_all()------------------→ AlgorithmResult     |
    |                                      |  × 3              |
    ←---AlgorithmResult × 3-----------------+                   |
    |                                                            |
    +--check()-----------------------------→ AccuracyCheck      |
    | (×3)                                   |                  |
    ←---AccuracyCheck × 3-------------------+                   |
    |                                                            |
    [Render]
```

Text fallback: U2 sends raw input to InputProcessor, receives a SortInput. Sends SortInput to SortingEngine, receives three AlgorithmResult objects. Sends each result (with SortInput for reference) to AccuracyChecker, receives three AccuracyCheck objects. Renders all results.

---

## Part 9: API Contract Reference

This functional specification implements the contract defined in `contract-summary.md`:

| Contract Element | Implementation |
|---|---|
| normalize(entries) | Workflow 1: Input Normalization |
| run_all(sort_input) | Workflow 2: Run All Three Algorithms |
| check(result, sort_input) | Workflow 3: Verify Accuracy |
| Types: SortInput, AlgorithmResult, AccuracyCheck | Part 1: Entities (entities.md) |
| Rules: normalization, counting, accuracy | Part 2: Business Rules (rules.md) |

---

## Part 10: Test-After Orientation

Key testable behaviors (for pytest, ~80% coverage floor):

| Behavior | Test Case |
|---|---|
| normalize: ASCII capitals lowercased | normalize(['HELLO']) → ['hello'] |
| normalize: non-ASCII pass-through | normalize(['cäfe']) → ['cäfe'] |
| normalize: duplicates preserved | normalize(['a', 'a']) → ['a', 'a'] |
| normalize: empty tokens dropped | normalize(['', 'hello', '  ']) → ['hello'] |
| bubble_sort: 3 elements, unsorted | run_all(...) → [bubble_result with comparisons=3, swaps=2] |
| selection_sort: 3 elements, unsorted | run_all(...) → [selection_result with comparisons=3, swaps=2] |
| quick_sort: 3 elements, unsorted | run_all(...) → [quick_result with comparisons>=2, swaps>=1] |
| accuracy: exact match | check(result, sort_input) → passed=True when sorted_strings == sorted(normalized_strings) |
| accuracy: order mismatch | check(result_with_swapped_duplicates, sort_input) → passed=False |
| edge: empty input | run_all(...) → [AlgorithmResult(..., sorted_strings=[], comparisons=0, swaps=0)] |
| edge: single element | run_all(...) → [AlgorithmResult(..., sorted_strings=input, comparisons=0, swaps=0)] |
| edge: all identical | run_all(...) → [AlgorithmResult(..., sorted_strings=input, swaps=0)] |

---

## Summary

This functional specification defines:
1. **Three workflows** (normalize, run_all, check) with step-by-step algorithms
2. **Comparison and swap counting** with formal definitions per algorithm
3. **Accuracy verification** as an exact-order match against Python's sorted()
4. **Edge cases** (empty, single, identical, duplicates) with explicit behaviors
5. **Integration sequence** showing how U2 orchestrates the three workflows
6. **State transitions** for counting operations
7. **Test orientation** with key testable behaviors

All specifications align with requirements (FR1–FR7, NFR1–NFR4) and functional design questions (Q1–Q6).
