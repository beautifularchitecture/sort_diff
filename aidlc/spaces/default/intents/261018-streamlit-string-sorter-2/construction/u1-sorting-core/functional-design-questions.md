# Functional Design Questions — U1 sorting-core

## Critical Decisions Requiring Clarification

### Q1: Step Count Definition (Resolves R1 Risk) ⚠️

**Context**: FR4.1 and FR4.2 appear to describe the same metric from different angles:
- FR4.1: "track step counts for each algorithm using the textbook definition: measure iterations of outer/inner loops as defined in the standard textbook form"
- FR4.2: "total element comparisons must be used as the primary comparable count for UI display across all three algorithms"

The requirements assume these are aligned, but "textbook loop iterations" and "total element comparisons" have different meanings depending on implementation.

**Specific Question**: For each of the three algorithms, which counts are we tracking?

**Option A**: Track ONLY "total element comparisons" (the primary UI metric in FR4.2):
- Bubble sort: count every pair comparison (including redundant passes)
- Selection sort: count every comparison in the selection loop
- Quick sort: count every comparison during partitioning and recursion
- Swaps tracked separately (FR4.3)
- Rationale: Single, directly comparable metric across all three; enables side-by-side accuracy comparison in the UI

**Option B**: Track BOTH "loop iterations" and "comparisons," display comparisons as primary:
- Bubble sort: outer loop iterations + comparisons (nested counting)
- Selection sort: outer loop iterations + comparisons
- Quick sort: recursion depth + comparisons
- More pedagogical detail, but adds complexity to tracking and UI display
- Rationale: Teaches both concepts, but requires two separate count fields per algorithm

**Option C**: Textbook "operations" per algorithm (varies by definition):
- Bubble sort: number of swaps (classical textbook measure)
- Selection sort: number of comparisons (classical textbook measure)
- Quick sort: number of comparisons (classical textbook measure)
- Not directly comparable across algorithms
- Rationale: Follows classical CS textbooks, but violates FR4.2's "enable direct comparison"

**Recommendation**: **Option A** is required by the contract (FR4.2 says "same definition… as the primary comparable count… to enable direct comparison"). This is the only choice that satisfies FR4.2's explicit requirement for a single comparable metric across all three algorithms.

**Proposed Decision**: Count ONLY "total element comparisons" as the primary step metric (stored in `AlgorithmResult.comparisons`), with "swaps" tracked separately as a secondary metric. The definition is: every comparison of two elements, including all passes through outer/inner loops and all partitioning steps in recursion. This is the same definition applied consistently to all three algorithms.

[Answer]: A — Track only total element comparisons (primary UI metric, same definition for all three); swaps tracked separately. This satisfies FR4.2's requirement for direct cross-algorithm comparison.

---

### Q2: Empty Input Handling

**Context**: FR6.1 says the UI must display "Enter or select at least one string" when input is empty and "must not run sorting." The domain design notes that U1 returns an empty result when given an empty list, and U2 handles the FR6.1 message and validation.

**Question**: Is the validation (empty check) performed in U1 or U2?

**Option A**: U1 validates — InputProcessor.normalize() raises ValueError if the input list is empty or contains only empty tokens after normalization.
- Rationale: Centralizes validation in the domain layer; U2 catches and displays the error message
- Trade-off: U1 must know about FR6.1 business rule

**Option B**: U2 validates — SortingPlaygroundApp checks if the list is empty BEFORE calling InputProcessor, and renders the message without invoking U1.
- Rationale: Keeps validation at the boundary; U1 remains a pure computation layer
- Trade-off: Requires U2 to know about the "empty input" rule

**Recommendation**: **Option B** aligns with the architecture principle (ADR-004) that "the domain layer contains no UI orchestration logic." U1 is pure functions; U2 orchestrates and validates.

[Answer]: B — U2 validates empty input and renders the FR6.1 message without invoking U1. U1 returns an empty result list (three AlgorithmResult objects with empty sorted_strings and zero counts) only when called with an empty SortInput, which U2 never does.

---

### Q3: Swap Counting Definition

**Context**: FR4.3 says "track and display swap counts separately for each algorithm." The textbook definitions of swaps differ:
- Bubble sort: swap when two adjacent elements are out of order
- Selection sort: swap once per iteration (after finding minimum)
- Quick sort: swap during partitioning (varies by implementation)

**Question**: Do we use the algorithm's natural swap count, or do we unify the definition across all three?

**Option A**: Natural swap count for each algorithm (no normalization):
- Bubble sort: count each adjacent-element swap
- Selection sort: count each swap after selection (usually 1 per pass, less on unsorted data with multiple comparisons)
- Quick sort: count swaps during partitioning (Hoare vs Lomuto partition matters here)
- Rationale: Authentic to each algorithm's implementation

**Option B**: Unified definition (e.g., "count every time two elements exchange positions in the array"):
- Apply to all three consistently
- Rationale: Enables direct comparison in the UI (like comparisons)
- Trade-off: May not match classical textbook counts

**Recommendation**: **Option A** is simpler and does not require normalization. Swaps are already tracked per algorithm's implementation. The *comparisons* metric (Q1) is the unified primary metric for cross-algorithm comparison; *swaps* is a secondary, algorithm-specific metric for education.

[Answer]: A — Track the natural swap count for each algorithm as implemented (bubble sort counts adjacent swaps, selection sort counts post-selection swaps, quick sort counts partitioning swaps). Swaps are an algorithm-specific educational detail; comparisons is the primary cross-algorithm metric.

---

### Q4: Duplicate String Handling

**Context**: The requirements (FR1.4 assumption) state "duplicates are kept." The contract specifies no deduplication. However, the exact rule for sorting duplicates is not stated.

**Question**: When sorting strings where some are identical (e.g., `["apple", "apple", "banana"]`), what is the expected order?

**Option A**: Stable sort — identical strings remain in input order (the order in which they appeared in the input).
- Rationale: Standard behavior for Python's `sorted()` (stable sort); matches the reference check in FR3.1
- Implementation: All three algorithms must be stable (or at minimum, must match Python's behavior on identical elements)

**Option B**: Unstable sort — any order among identical strings is acceptable as long as the sorted order is correct.
- Rationale: Simpler implementation (especially quick sort)
- Trade-off: May not match Python's `sorted()` on identical elements; could fail FR3.1 accuracy check

**Recommendation**: **Option A** is required by FR3.1, which checks "exact order match" against Python's `sorted()`. Python's `sorted()` is stable, so all three algorithms must produce the same order for identical strings.

[Answer]: A — Use stable sort semantics. All three algorithms must preserve the relative order of duplicate (identical) strings as they appear in the input. This ensures exact-match accuracy checks (FR3.1) against Python's sorted() (which is stable).

---

### Q5: Lexicographic Ordering and Non-ASCII Characters

**Context**: FR2.4 specifies "lexicographic (ASCII/Unicode as-is, default lexicographic ordering)." Decision D10 states "non-ASCII characters pass through unchanged" during normalization. Python's default string comparison is lexicographic.

**Question**: Confirm the exact sort order for mixed ASCII and non-ASCII strings.

**Option A**: Default Python lexicographic order (no special handling):
- Python sorts by Unicode code point
- Non-ASCII characters sort according to their Unicode values
- Example: `["ä", "a", "b"]` sorts as `["a", "ä", "b"]` (Unicode ordering)
- Rationale: Simplest implementation, matches Python's default, verifiable against `sorted()`

**Option B**: ASCII-only sort with non-ASCII characters deferred to the end:
- Rationale: Simpler visual comparison in educational context
- Trade-off: More complex to implement; does not match Python's default sorting

**Recommendation**: **Option A** — use Python's default Unicode lexicographic order for all strings. This is the simplest, and the accuracy check (FR3.1) verifies against Python's `sorted()`, which uses Unicode ordering.

[Answer]: A — Use Python's default Unicode lexicographic order for all strings (no special handling for non-ASCII). The comparison `a < b` in Python works for mixed-case and non-ASCII strings, and this order is verifiable against Python's sorted().

---

### Q6: Quick Sort Partitioning Strategy

**Context**: Quick sort has multiple well-known partitioning schemes (Hoare, Lomuto, three-way). Each has different swap and comparison counts.

**Question**: Which quick sort implementation should we use?

**Option A**: Lomuto partition (simpler, more predictable):
- Choose last element as pivot
- Single pass; one section < pivot, one section >= pivot
- Deterministic swap count
- Rationale: Easier to teach and understand; count is predictable

**Option B**: Hoare partition (classical, more efficient on random data):
- Two pointers converging; often fewer swaps
- Rationale: More efficient; matches classical algorithms textbooks
- Trade-off: Less predictable count for educational comparison

**Option C**: Three-way partition (handles duplicates well):
- Three sections: < pivot, == pivot, > pivot
- Rationale: Better performance on data with many duplicates
- Trade-off: More complex to implement and explain

**Recommendation**: **Option A** is better for an educational tool. Consistent counts and simpler logic make it easier to trace and verify.

[Answer]: A — Use Lomuto partition (last element as pivot, deterministic counts). Simpler to implement and explain in an educational context; counts are predictable and reproducible across runs.

---

## Summary of Design Decisions

| # | Decision | Choice | Rationale |
|---|---|---|---|
| Q1 | Step counting | Total element comparisons only, same definition for all three | Satisfies FR4.2: enables direct cross-algorithm comparison |
| Q2 | Empty input validation | U2 validates before calling U1 | Keeps U1 as pure computation layer (ADR-004) |
| Q3 | Swap counting | Natural swap count per algorithm | Simpler; comparisons is the primary metric |
| Q4 | Duplicate handling | Stable sort (preserve input order) | Required by FR3.1 (exact match vs Python sorted()) |
| Q5 | Non-ASCII ordering | Python default Unicode lexicographic | Simplest, verifiable vs Python sorted() |
| Q6 | Quick sort strategy | Lomuto partition | Simpler, more predictable for education |

---

## Approval Gate

**Ready to proceed with functional design artifacts** once the above decisions are confirmed. These decisions enable concrete entity definitions, business rules, and functional workflows in the following artifacts:
- `entities.md` (SortInput, AlgorithmResult, AccuracyCheck with concrete counting semantics)
- `rules.md` (business rules for counting, validation, accuracy)
- `functional-spec.md` (workflows with step counting, accuracy checking, edge cases)
- `traceability.json` (requirements to rules mapping)
