# Unit of Work Dependencies

## Dependency Graph

```text
U1 sorting-core  ──►  U2 playground-ui  ──►  U3 delivery-pipeline
```

Each arrow reads "depends on": U2 depends on U1; U3 depends on U2. The graph is acyclic.

## Integration Points

| From | To | Integration | Contract |
|---|---|---|---|
| U2 | U1 | synchronous in-process calls | `InputProcessor.normalize(entries) -> SortInput`; `SortingEngine.run_all(sort_input) -> [AlgorithmResult]`; `AccuracyChecker.check(result, sort_input) -> AccuracyCheck` |
| U3 | U2 | build and deploy the app entry point | Streamlit entry script; test command `pytest` covers U1 and U2 logic |

No network, database, queue, or shared data between Units.

## Parallel Development

None. The chain is linear. U2 cannot be integrated until U1's interfaces exist, and U3 has nothing to deploy until U2 runs.

Within U1, the three algorithms and the normalizer can be developed in any order, because they share only the data types of `SortInput` and `AlgorithmResult`. This is intra-Unit work, not a Unit-level parallelism.

## Edge Block

```yaml
units:
  - name: sorting-core
    kind: library
    depends_on: []
  - name: playground-ui
    kind: ui
    depends_on: [sorting-core]
  - name: delivery-pipeline
    kind: packaging
    depends_on: [playground-ui]
```

Validity checks: names are unique and lowercase path segments; every `depends_on` entry is declared; no unit depends on itself; the graph is acyclic.

## Skeleton

Not applicable. The team chose no walking skeleton for this intent (team.md, Walking Skeleton). U1 is the first Unit in DAG order and is a complete, testable slice of the domain, which is sufficient for test-after development.
