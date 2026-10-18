# User Flow

## Sources

- `ideation/rough-mockups/rough-mockups-questions.md` — confirmed Q1–Q7
- `ideation/scope-definition/intent-backlog.md` — value stream: input → button → three algorithms with step counting → accuracy check → side-by-side results

## Happy Path

```text
[start: open app]
      |
      v
[Enter strings] ----------------------+
  | one big text box (one per line)   |  either/or/both
  | or pick from word-list picker     |
  +-----------------------------------+
      |
      v
[Click Sort]
      |
      v
[Bubble sort runs] --> [Selection sort runs] --> [Quick sort runs]
      |                      |                      |
      v                      v                      v
[steps counted]        [steps counted]        [steps counted]
      |                      |                      |
      +---- each checked against reference sort ----+
      |                      |                      |
      v                      v                      v
[Results displayed side by side: sorted list, step count, accuracy, per algorithm]
      |
      v
[User compares step counts, verifies accuracy marks]
      |
      v
[end]
```

## Step Detail

1. **Open app** — the single page loads with an empty input area and a results hint (Q1: A).
2. **Provide input** — type/paste strings one per line (Q3: A), pick words from the bundled list (Q4: A), or both; both sources feed the same list.
3. **Click Sort** — one button triggers all three algorithms on that list (scope: side-by-side, one run).
4. **Algorithms run** — each reports its step count; each result is checked against the reference sort (accuracy, B5).
5. **Results appear** — three aligned columns: sorted list, step count, accuracy (Q2: A, Q5: A).
6. **Compare** — user reads step counts side by side; accuracy marks confirm correctness.

## Branches & Edge Cases

| Situation | Flow |
|-----------|------|
| Sort with no input | Results show the empty-state hint; no error |
| Only typed strings, no picked words | Same flow; picker simply contributes nothing |
| Only picked words, no typed strings | Same flow; text box contributes nothing |
| Duplicates in input | Allowed; appear as-is in every sorted output |
| Edit input after a sort, sort again | Results are replaced by the new run (no history — storage is out of scope, C2) |

## Non-Flows (out of scope)

- No account/login, no saving results, no file upload/download, no per-algorithm animation or step replay (v1 shows counts and final output only).
- No multi-page navigation: everything happens on the one screen (Q1: A).

## Assumptions & Open Questions

- [assumption] Algorithms run synchronously on button click; classroom-sized inputs (feasibility A1) mean no progress indicator is needed in v1.
- [assumption] Re-sorting is just "edit and click Sort again" — no separate reset control beyond clearing the input.
