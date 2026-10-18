# Units Generation — Observation Diary

## Interpretations

- The stage asks for Units as topology, not an economic order. The DAG is linear (U1 to U2 to U3). I did not recommend a build order or critical path, which Delivery Planning owns.
- "Unit kind" was assigned from what each Unit IS: `library` for the pure domain, `ui` for the Streamlit page, `packaging` for the CI and deploy artefacts.
- U3 has no domain component. It is included because US5.2 (auto-deploy on merge) needs an owner and the team's practice is continuous deployment.

## Deviations

- The stage definition requires a plan approval question before generation. I presented the plan and waited for the human, then generated the artifacts.
- Traceability uses a primary Unit per story. Cross-cutting concerns are recorded in the story map rows that span units, not as multiple OK targets, to keep the traceability target unambiguous.

## Tradeoffs

- Three Units over one: one Unit would be simpler to sequence, but it mixes the testable domain with the CI and deploy concern, which change at different rates.
- Three Units over five (one per component): the component boundaries are a design choice, but five Units for a single-screen app would add integration overhead with no independent deployment need.
- Chose library kind for U1 rather than service: it has no standalone runtime and is imported in-process by U2.

## Open questions

- The non-ASCII question was resolved at the plan gate: pass-through is kept (D10).
- Test-after ordering and the ~80% floor are carried into Construction through the team's testing posture; no Unit-level change needed.
