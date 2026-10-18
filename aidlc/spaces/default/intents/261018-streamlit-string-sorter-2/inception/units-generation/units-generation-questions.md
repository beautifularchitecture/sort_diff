# Units Generation — Decomposition Plan & Questions

## Sources

- `inception/domain-design/components.md` (five components, four entities)
- `inception/domain-design/decisions.md` (ADR-001 to ADR-004)
- `inception/requirements-analysis/requirements.md` (FR1–FR7, NFR1–NFR4)
- `inception/user-stories/stories.md` (US1.1–US5.2)
- Team practice (`team.md`): trunk-based, squash-merge, test-after, auto-deploy to production on merge. No walking skeleton for this intent.

## Proposed Decomposition

Three Units, linear dependency chain. Each Unit maps to one deployable or verifiable slice.

| Unit ID | Name | Directory | Kind | Components | Depends on |
|---|---|---|---|---|---|
| U1 | sorting-core | `u1-sorting-core` | library | InputProcessor, SortingEngine, AccuracyChecker | none |
| U2 | playground-ui | `u2-playground-ui` | ui | SortingPlaygroundApp, WordListProvider | U1 |
| U3 | delivery-pipeline | `u3-delivery-pipeline` | packaging | CI workflow and Streamlit Community Cloud deploy configuration | U2 |

**Why this split**
- U1 is pure logic with no UI runtime, so it can be built and tested with pytest first (test-after, ~80% coverage on sorting logic).
- U2 is the thin Streamlit layer and bundles the word list; it cannot run without U1.
- U3 owns the merge-to-production pipeline (US5.2). It has nothing to deploy until U2 exists.

**Why not one Unit:** the team's pytest posture is easier to satisfy when the domain is its own Unit, and the CI/deploy concern changes at a different rate from the logic.

**Why not per-component Units:** five Units for five small components would add integration overhead to a single-screen app with no independent deployment need.

## Dependency DAG

```text
U1 sorting-core  ──►  U2 playground-ui  ──►  U3 delivery-pipeline
```

Parallel development: none. The chain is strictly linear, so Delivery Planning will have a single valid order.

## Story Assignment (primary target per story)

| Story | Primary Unit | Notes |
|---|---|---|
| US1.1 manual entry | U2 | Normalization rule implemented in U1 (InputProcessor) |
| US1.2 word-list selection | U2 | Word list owned by U2 (WordListProvider) |
| US2.1 single Sort button runs three algorithms | U1 | Engine behaviour; button wiring in U2 |
| US3.1 side-by-side display | U2 | Renders U1's results |
| US3.2 comparisons, swaps, accuracy | U1 | Counting and accuracy computed in U1; displayed in U2 |
| US4.1 empty-input message | U2 | Exact FR6.1 warning |
| US4.2 edge cases | U1 | Single, identical, and empty-token handling in U1 |
| US5.1 local run | U2 | Entry point is the Streamlit app |
| US5.2 auto-deploy on merge | U3 | GitHub Actions to Streamlit Community Cloud |

## Unit Kinds

- U1 `library`: reusable domain code with no standalone runtime.
- U2 `ui`: the frontend surface.
- U3 `packaging`: CI and distribution artefacts.

## Open Question (carried from Domain Design review)

**Non-ASCII input.** FR1.3 says the system "only allows" lowercase letters, numbers, and ASCII special characters. Domain Design passes non-ASCII through unchanged, sorted by code point (decision D10). This plan keeps D10 unless you say otherwise. The alternative is to reject non-ASCII input with a message, which would add a U2 validation rule and a new acceptance criterion.

## Plan Approval

Options:
- **Approve Plan** (keeps U1, U2, U3 and passes non-ASCII through, D10)
- **Revise Plan** (tell me what to change, including whether non-ASCII should be rejected)

[Answer]: Approve Plan (keep non-ASCII pass-through)

## Consolidated Summary Confirmation

Here is the combined summary of this stage's decisions. Please confirm it.

**Units (3, linear)**: U1 sorting-core (library: InputProcessor, SortingEngine, AccuracyChecker), U2 playground-ui (ui: SortingPlaygroundApp, WordListProvider), U3 delivery-pipeline (packaging: CI and deploy on merge).

**Dependencies**: U2 depends on U1; U3 depends on U2. Acyclic, no parallel work. Topology only; sequencing belongs to Delivery Planning.

**Stories**: US1.1, US1.2, US3.1, US4.1, US5.1 to U2; US2.1, US3.2, US4.2 to U1; US5.2 to U3. All nine stories assigned, one primary Unit each.

**Decisions**: non-ASCII input passes through unchanged (D10, carried from Domain Design; you approved keeping it). No walking skeleton (team.md).

[Answer]: Looks correct
