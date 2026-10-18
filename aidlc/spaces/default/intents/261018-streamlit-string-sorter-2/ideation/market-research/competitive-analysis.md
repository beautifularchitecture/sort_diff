# Competitive Analysis

## Sources

- `ideation/market-research/market-research-questions.md` — Q1: A, Q2: D, Q4: B, Q6: A (confirmed)
- `ideation/intent-capture/intent-statement.md` — target customer, success metrics, v1 scope

## Purpose

Who else helps people see how sorting algorithms behave, and where this app sits among them. The person building this is not competing for users — the app is a free teaching aid optimized for educators demonstrating algorithms in a lesson.

## Closest Alternatives

### Free algorithm-visualization sites (VisuAlgo, Python Tutor)

- **Strengths**: polished, well-known, broad algorithm coverage, animated stepping, multi-language support, no maintenance burden for the teacher.
- **Weaknesses**: generic — not tailored to one lesson or one class; general-purpose interfaces carry more ceremony than a five-minute demonstration needs; little or no side-by-side comparison of several algorithms on the same input with step counts.
- **Pricing model**: free tiers supported by institutional sponsorship or advertising; paid tiers for classroom/course features.

### Teaching demos on GitHub / Streamlit sharing

- **Strengths**: free, source-available, often small and readable, close in spirit to what is being built here.
- **Weaknesses**: quality and maintenance vary widely; many cover a single algorithm or omit accuracy checks and step counts; not maintained as courseware.
- **Pricing model**: free.

### Commercial edtech platforms teaching sorting

- **Strengths**: curriculum-aligned, polished narratives, assessment tooling, support.
- **Weaknesses**: heavyweight and paid for what is only needed as a short in-lesson demonstration; the app's audience is not shopping for a course platform.
- **Pricing model**: subscription or institutional licence.

## Positioning

- **Where this app sits**: a small, free, single-purpose demonstration tool in the same family as the alternatives above — closest in spirit to a teaching demo, with the specific combination of multiple string-based algorithms, accuracy checking, and per-algorithm step counts on one shared input.
- **Differentiation claimed**: none beyond that combination (answer Q2: nothing special — correct sorting and visible step counts are enough). The app does not claim an advantage over VisuAlgo-class tools; it exists as a simple, ownable classroom aid.
- **Primary audience for v1**: educators demonstrating algorithms in a lesson (answer Q4), with students and developers as secondary beneficiaries of the same interface.
- **Market size assumption**: a single classroom, class, or personal teaching context. No adoption targets, growth goals, or user counts are claimed (answer Q6: free, shared as source code or run locally).

## Strategic Read

Building is justified by simplicity and ownership, not by a market gap: the alternatives are either too generic, too heavy, or too inconsistent for a short in-lesson demonstration of string sorting with step counts. Because no differentiation is claimed, the competitive risk of building is low — the app's value is that it is small, controllable, and free.

## Assumptions & Open Questions

- [assumption] The alternatives above are representative of what this audience would otherwise use; no user research or usage data was collected for this stage.
- [assumption] "Educators demonstrating in a lesson" as the primary audience does not change the v1 feature set agreed in intent-capture (bubble, selection, and quick sort on strings, with step counts and accuracy checking).
