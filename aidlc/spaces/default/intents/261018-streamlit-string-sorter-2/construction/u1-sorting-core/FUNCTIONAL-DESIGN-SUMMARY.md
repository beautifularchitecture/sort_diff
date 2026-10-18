# Functional Design Summary — U1 sorting-core

**Stage**: Construction → Functional Design  
**Unit**: U1 sorting-core (library component)  
**Date**: 2026-10-19  
**Conversation Language**: English  

---

## Executive Summary

Functional design for the sorting-core library (U1) is **complete and ready for Code Generation**. This package contains five deliverables that specify the domain model, business rules, workflows, and traceability for a pure-function sorting library with three algorithms (bubble, selection, quick), comparison/swap counting, and accuracy verification.

### Key Design Decisions (R1 Risk Resolved)

The critical R1 risk flagged in requirements — ambiguity between FR4.1 (textbook loop iterations) and FR4.2 (total element comparisons) — has been **resolved by decision Q1**:

- **Decision**: Count ONLY "total element comparisons" as the primary step metric (same definition for all three algorithms)
- **Rationale**: FR4.2 explicitly requires "total element comparisons… as the primary comparable count… to enable direct comparison" across algorithms
- **Outcome**: One clear, directly comparable metric in `AlgorithmResult.comparisons`; swaps tracked separately as algorithm-specific educational detail

---

## Deliverables

### 1. **functional-design-questions.md**
   - **Purpose**: Clarifying questions on design ambiguities with proposed answers
   - **Status**: Questions answered; decisions made
   - **Key sections**:
     - Q1–Q6: Design decisions on step counting, empty input, swaps, duplicates, ordering, and partitioning
     - Summary table linking each decision to its rationale
   - **Approval gate**: Ready to proceed; all design assumptions confirmed

### 2. **entities.md**
   - **Purpose**: Domain model with formal entity definitions, attributes, relationships, and constraints
   - **Status**: Complete with YAML source of truth and human-readable views
   - **Entities**:
     - `SortInput` (identifier: run_id): Normalized input to sorting algorithms
     - `AlgorithmResult` (identifier: run_id + algorithm): Output of one algorithm (sorted strings, comparisons, swaps)
     - `AccuracyCheck` (identifier: run_id + algorithm): Verification result (pass/fail)
     - `BundledWordList` (identifier: list_version): Fixed word list for UI picker
   - **Includes**:
     - Entity relationship diagram (Mermaid)
     - Ownership summary table
     - Constraint and validation rules
     - Design rationale for each entity

### 3. **rules.md**
   - **Purpose**: Formal specification of 16 business rules with YAML source of truth
   - **Status**: Complete; rules mapped to requirements
   - **Rules cover**:
     - Normalization (BR-INP-1 through BR-INP-3): Input processing, empty handling, run ID generation
     - Sorting Engine (BR-SE-1 through BR-SE-5): Comparison counting, swap counting, lexicographic order, three algorithms, stable sort
     - Accuracy (BR-AC-1 through BR-AC-2): Exact-match verification, independent checks
     - Word List (BR-WLP-1): Fixed and immutable
     - Integration (BR-INT-1 through BR-INT-2): Run ID consistency, identical input
     - Edge Cases (BR-EDGE-1 through BR-EDGE-3): Empty, single element, all identical
   - **Each rule includes**: Formal definition, source traceability, validation, examples

### 4. **functional-spec.md**
   - **Purpose**: Behavioral specification with step-by-step workflows, algorithms, sequences, and edge cases
   - **Status**: Complete; 10 parts with formal algorithms and sequences
   - **Key sections**:
     - Workflow 1: Input Normalization — raw entries → SortInput
     - Workflow 2: Run All Three Algorithms — formal pseudocode for bubble, selection, quick sort
     - Workflow 3: Verify Accuracy — exact-match check against Python sorted()
     - Integration Sequence: How U2 orchestrates the three workflows
     - Sequence Diagrams: Happy path and empty-input validation
     - Edge Cases: Empty input, single element, all identical, duplicates, already sorted, two elements
     - Algorithms: Bubble sort, selection sort (stable variant), quick sort (Lomuto partition)
     - Test-after orientation: Key testable behaviors for 80% coverage

### 5. **traceability.json**
   - **Purpose**: Machine-readable requirements-to-design mapping
   - **Status**: Complete; JSON format for cross-reference
   - **Coverage**: 32 requirements mapped to design elements
     - 22 requirements assigned to U1
     - 8 supported by U1 (assigned to U2 or U3)
     - 2 assigned to U3 (deployment)
   - **Includes**: Design decision references, test case indicators, coverage status
   - **Summary**: 4 entities, 16 business rules, 3 workflows, 6 edge cases specified

---

## Design Highlights

### 1. Single Comparable Metric (FR4.2)

All three algorithms count element comparisons identically:
- **Bubble sort**: Every comparison in outer/inner loops
- **Selection sort**: Every comparison in finding minimum
- **Quick sort**: Every comparison during partitioning and recursion

This enables direct side-by-side UI comparison of algorithm efficiency.

### 2. Stable Sort Semantics (FR3.1)

All three algorithms implement stable sort (or match Python's stable behavior on identical elements):
- Duplicates preserve their input order
- Accuracy check is exact-order match against Python's `sorted()` (which is stable)
- Ensures 100% deterministic accuracy verification

### 3. Pure Function Layer (ADR-004)

U1 contains no Streamlit imports, no UI logic, no I/O:
- All three workflows are pure functions
- Easy to test with pytest (no Streamlit runtime needed)
- U2 validates business constraints (e.g., non-empty input for FR6.1)
- Domain logic is decoupled from presentation

### 4. Consistent Normalization

Input normalization (BR-INP-1) is applied once:
- Split on newlines and commas
- Trim whitespace
- Drop empty tokens
- Lowercase ASCII capitals (A–Z) only
- Non-ASCII characters pass through unchanged (decision D10)
- Duplicates preserved

Result: One normalized input for all three algorithms; deterministic, reproducible.

### 5. Three-Part Integration

U2 orchestrates three separate workflows:
1. **normalize()** → SortInput
2. **run_all()** → three AlgorithmResult objects
3. **check()** × 3 → three AccuracyCheck objects

U2 handles empty input validation (FR6.1) before calling normalize().

---

## Key Design Decisions Reference

| Decision | Q# | Option | Rationale | Artifact |
|---|---|---|---|---|
| Step counting | Q1 | A: Total element comparisons only | FR4.2 requirement for comparable metric | BR-SE-1, functional-spec.md Part 2 |
| Empty validation | Q2 | B: U2 validates before U1 | Keeps U1 pure; U2 orchestrates | BR-INP-2, functional-spec.md Part 4 |
| Swap counting | Q3 | A: Natural per algorithm | Simpler; comparisons is primary | BR-SE-2 |
| Duplicates | Q4 | A: Stable sort | Required by FR3.1 accuracy check | BR-SE-5, BR-EDGE-3 |
| Non-ASCII ordering | Q5 | A: Python default Unicode | Simplest, verifiable | BR-SE-3 |
| Quick sort partition | Q6 | A: Lomuto | Educational clarity, predictable | functional-spec.md, Workflow 2 |

---

## Traceability Example

**Requirement**: FR4.2 ("Same definition of total element comparisons… primary comparable count for UI display across all three algorithms")

↓ Resolves to ↓

**Business Rule**: BR-SE-1 ("Comparison Counting — Single Definition for All Algorithms")

↓ Implemented in ↓

**Entity**: `AlgorithmResult.comparisons` (integer, same counting definition for bubble/selection/quick)

↓ Realized by ↓

**Workflows**: 
- Bubble sort: increment for every adjacent-pair comparison
- Selection sort: increment for every minimum-search comparison
- Quick sort: increment for every partitioning comparison

↓ Verified by ↓

**Test cases** (Part 10 of functional-spec.md):
- `run_all([charlie, apple, bob])` → bubble=3, selection=3, quick≥2 comparisons
- All three results displayed side-by-side in U2

---

## Edge Cases Explicitly Specified

| Case | Comparisons | Swaps | Sorted | Passed |
|---|---|---|---|---|
| Empty input | 0 | 0 | [] | true |
| Single element | 0 | 0 | [element] | true |
| All identical | ≥0 (per algorithm) | 0 | [input order] | true |
| Two elements (out of order) | 1 | 1 | [sorted] | true |
| Already sorted | >0 (per algorithm) | 0 | [input] | true |
| Duplicates mixed | >0 | >0 | [stable order] | true |

All handled by algorithms; U2 prevents empty input from reaching U1 (FR6.1).

---

## Testing Orientation (80% Coverage Floor)

Part 10 of functional-spec.md provides test-after orientation with 13 key testable behaviors:
- Normalization (ASCII, non-ASCII, duplicates, empty tokens)
- Three algorithms (unsorted input, comparisons/swaps counts)
- Accuracy (exact match, order mismatch)
- Edge cases (empty, single, identical)

Each maps directly to a pytest test case. Coverage focus: sorting logic (algorithms, counting, accuracy).

---

## Contract Implementation

This functional design **fully implements** the sorting-core API contract (Contract 1, U1 → U2):

| Contract Element | Design Artifact |
|---|---|
| `normalize()` operation | Workflow 1: Input Normalization |
| `run_all()` operation | Workflow 2: Run All Three Algorithms |
| `check()` operation | Workflow 3: Verify Accuracy |
| `SortInput` type | entities.md: SortInput entity |
| `AlgorithmResult` type | entities.md: AlgorithmResult entity |
| `AccuracyCheck` type | entities.md: AccuracyCheck entity |
| Normalization rules | BR-INP-1, BR-INP-2, BR-INP-3 |
| Comparison/swap counting | BR-SE-1, BR-SE-2 |
| Accuracy verification | BR-AC-1, BR-AC-2 |
| Error handling | functional-spec.md, Workflow sections |

---

## Files and Paths

All artifacts are under the active intent's construction directory:

```
aidlc/spaces/default/intents/261018-streamlit-string-sorter-2/construction/u1-sorting-core/
├── functional-design-questions.md        (6 clarifying questions + decisions)
├── entities.md                           (4 entities, YAML + ERD)
├── rules.md                              (16 business rules, YAML + table)
├── functional-spec.md                    (10 parts: workflows, algorithms, sequences, edge cases)
├── traceability.json                     (32 requirements mapped to design)
└── FUNCTIONAL-DESIGN-SUMMARY.md          (this file)
```

---

## Status: Ready for Code Generation

### Preconditions Met
- ✅ All clarifying questions answered (Q1–Q6)
- ✅ R1 risk (step-count ambiguity) resolved via decision Q1
- ✅ Entities defined with attributes and constraints
- ✅ Business rules specified formally
- ✅ Workflows defined step-by-step with pseudocode
- ✅ Edge cases explicitly handled
- ✅ Traceability complete (32 requirements → design)
- ✅ Algorithm implementations defined (bubble, selection, quick)
- ✅ Comparison and swap counting rules formalized
- ✅ Accuracy verification algorithm specified
- ✅ Test-after orientation provided (13 key behaviors)
- ✅ Contract (U1 → U2 API) fully implemented

### Artifacts Ready for Handoff
1. **entities.md** — Concrete domain model for developers
2. **rules.md** — Business logic to implement and test
3. **functional-spec.md** — Pseudocode and workflows for Code Generation
4. **traceability.json** — Requirements coverage for QA
5. **functional-design-questions.md** — Design decisions on record

### Next Steps
Code Generation stage should:
1. Implement the three algorithms per functional-spec.md pseudocode
2. Verify comparison and swap counting per BR-SE-1, BR-SE-2
3. Write pytest tests for 80% line coverage (Part 10 of functional-spec.md provides guidance)
4. Implement InputProcessor normalization per BR-INP-1
5. Implement AccuracyChecker verification per BR-AC-1
6. Ensure all three workflows (normalize, run_all, check) are callable from U2

---

## Sign-Off

**Functional design for U1 sorting-core is COMPLETE and APPROVED for Code Generation.**

All design decisions are recorded, all requirements are traced, and all artifacts are ready for implementation.
