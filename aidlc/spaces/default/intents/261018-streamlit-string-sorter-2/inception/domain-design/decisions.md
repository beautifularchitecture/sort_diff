# Architecture Decision Records — Domain Design

## ADR-001: Five-component decomposition (UI orchestrator plus four domain components)

**Status:** Accepted (2026-10-18, pending summary confirmation at the gate)

### Context

The requirements define three distinct concerns: input normalization and empty-token rules (FR1, FR6), sorting with shared step counting (FR2, FR4), and verification against a reference (FR3). FR1.5 also requires a fixed bundled word list. The team testing posture requires pytest coverage of the sorting logic (~80%, NFR4.2), so the domain must be testable without a UI runtime. The app is small, so over-decomposition is a real risk.

### Decision

Use five components: `SortingPlaygroundApp` (Streamlit UI and orchestration) plus four domain components `InputProcessor`, `SortingEngine`, `AccuracyChecker`, and `WordListProvider`. Each functional family has exactly one owner.

### Consequences

**Positive**
- Each concern has a single owner and an independent test surface.
- The UI can change without touching domain rules.
- The bundled list (FR1.5) has an explicit contract that can be tested separately.

**Negative**
- Five components is the upper bound of right-sizing for this application; more ceremony than a single module.
- Cross-component wiring lives in the UI, so the orchestrator must be kept in step with the four domain interfaces.

**Neutral**
- All components are in-process modules, not services. Splitting them into services later would be a new decision.

### Alternatives Rejected

- **Option B: four components, word list as a constant inside `SortingPlaygroundApp`.** Less ceremony, but FR1.5 has no owning component and no independent test surface. Rejected because the bundled list is a stated requirement, not incidental UI data.
- **Option C: a single `SortDomain` module owning parsing, all algorithms, and verification.** Minimal ceremony, but it mixes three concerns with different change rates and makes the accuracy contract harder to bound and test. Rejected.

---

## ADR-002: One SortingEngine owns all three algorithms behind a shared result contract

**Status:** Accepted (2026-10-18, pending summary confirmation at the gate)

### Context

FR2.5 requires that all three algorithms run on the same input in one run. FR4.2 requires one comparable step definition across all three. The three algorithms share a counting contract and a result shape.

### Decision

Place bubble sort, selection sort, and quick sort in one `SortingEngine` component. Each algorithm returns an `AlgorithmResult` with the same fields (sorted_strings, comparisons, swaps). Counting follows one definition shared by all three.

### Consequences

**Positive**
- A single counting definition is enforced in one place, which protects the comparability that is the app's educational point.
- Adding a fourth algorithm is out of scope (NFR3.1), so the single component stays small.

**Negative**
- Changing one algorithm's internals touches a component that also contains the other two; mitigated by per-algorithm unit tests.

**Neutral**
- Quick sort's recursive structure and the iterative bubble and selection loops share one result shape but not one implementation style.

### Alternatives Rejected

- **Three algorithm components, one per sort.** Rejected: three components for three functions that share one contract is ceremony, and the shared counting rule would have to be duplicated or extracted into a fourth component.
- **A strategy registry with pluggable algorithms.** Rejected: plugin extension is not required in v1 and violates the scope boundary.

---

## ADR-003: AccuracyChecker is a separate component using Python's sorted() as the reference

**Status:** Accepted (2026-10-18, pending summary confirmation at the gate)

### Context

FR3 requires that each algorithm's output be checked against a reference for exact order. Verification is a different concern from sorting, and the reference rule is independent of how any algorithm works.

### Decision

Create `AccuracyChecker` as its own component. It compares each AlgorithmResult's sorted_strings with `sorted()` applied to the same SortInput. Each algorithm is checked independently.

### Consequences

**Positive**
- A bug in an algorithm cannot also corrupt its own verification, because the checker never calls the engine.
- The reference rule lives in one place and is tested independently.

**Negative**
- An extra component to wire through the UI.

**Neutral**
- If a stronger reference is ever needed, only AccuracyChecker changes.

### Alternatives Rejected

- **Fold verification into SortingEngine.** Rejected: an algorithm that verifies its own output is weaker evidence, and the two change rates differ.
- **Verify inline in the UI.** Rejected: verification logic would sit outside the testable domain and violate ADR-004.

---

## ADR-004: SortingPlaygroundApp is a thin orchestrator with no business logic

**Status:** Accepted (2026-10-18, pending summary confirmation at the gate)

### Context

The team's testing posture is pytest-based, with about 80% line coverage on the sorting logic and no requirement to run a Streamlit runtime in tests. The UI must render the FR6.1 warning and the result columns without owning any algorithm, normalization, or verification rule.

### Decision

`SortingPlaygroundApp` only renders widgets and orchestrates the button-press pipeline: normalize, sort all three, verify each, render. All rules live in the four domain components, which the UI calls synchronously.

### Consequences

**Positive**
- Domain logic runs and is tested under pytest without Streamlit.
- The UI is small enough to review by inspection.

**Negative**
- Orchestration rules (for example, the order of operations on Sort press) are not unit-tested in isolation; covered by a small number of UI-level checks in Build and Test.

**Neutral**
- Pipeline order is fixed by the single Sort button (FR5.2).

### Alternatives Rejected

- **Put orchestration inside a domain facade component.** Rejected for v1: one more component for a single call chain adds ceremony without a second caller.
- **Let the UI own normalization or sorting as a shortcut.** Rejected: it would move rules out of the testable domain and violate the team's pytest posture.
