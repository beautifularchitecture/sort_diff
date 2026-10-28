# Requirements

## Business Requirements

- BR-1: Investigate and fix the reported "swaps are always 0" display issue while ensuring counters are accurate.
- BR-2: Add a moving timer to the sorting visualization/UI.
- BR-3: Expand the "pick from list" with ~3000 random words.
- BR-4: Update comparisons/swaps/timer dynamically if sorting takes long.

## Functional Requirements

- FR-1: Comparisons and swaps must be computed and reported correctly by sorting algorithms (already true per tests).
- FR-2: The UI must display comparisons, swaps, and accuracy correctly after sorting.
- FR-3: Add a moving timer that updates during sorting (or shows elapsed time appropriately).
- FR-4: "Pick from list" must include ~3000 random words (de-duplicated as per constraints).
- FR-5: When sorting is in progress or takes time, update comparisons/swaps/timer dynamically (UI updates).

## Non-Functional Requirements

- NFR-1: Follow existing constraints - no unsafe_allow_html, no eval/exec/compile, exceptions from sorting_core must propagate.
- NFR-2: Max 100 de-duplicated strings in input.
- NFR-3: Keep changes compatible with existing tests.
