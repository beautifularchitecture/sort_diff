# Personas

## Persona Relationships and Priority

Ranked by priority for this product:

1. **Sam the Student** — primary user; every Must-Have story serves this persona directly.
2. **Elena the Educator** — secondary; shares Sam's journey but enters through the bundled word list and classroom pacing.
3. **Devon the Developer** — tertiary; adjacent user who values local execution and clean metrics but is not the design center.

Elena and Devon are real users of the same single-screen app, not separate workflows; stories occasionally speak to them where their goal differs from Sam's (US5.1, US5.2).

---

## Sam the Student

- **Role**: Computer science student learning about sorting algorithms.
- **Goals**: See how bubble sort, selection sort, and quick sort actually process string data; compare their step counts side-by-side; verify each result is correct so trust in the demonstration is immediate.
- **Pain points**: Textbook descriptions of sorting are abstract; hard to see how many comparisons an algorithm really makes; existing visualizers are often complex or cover too many algorithms at once.
- **Context**: Working through course material on a laptop, either alone or following along in a lab session; classroom-sized inputs (a handful to a few dozen strings).
- **Success looks like**: Paste or pick strings, press one button, and immediately read three sorted lists with comparison counts, swap counts, and a clear pass/fail next to each.

## Elena the Educator

- **Role**: Instructor teaching introductory algorithms.
- **Goals**: Demonstrate the three algorithms live without fiddling with setup; show students that each implementation is accurate against a trusted reference; pull up the same demo quickly at the start of each lecture.
- **Pain points**: Setting up live demos mid-class is fragile; students ask "is it actually right?" and she wants a built-in verification answer; juggling many visualization tools is distracting.
- **Context**: Projector in a lecture hall or shared screen in a small classroom; wants a predictable bundled word list ready to go.
- **Success looks like**: Open the deployed app, select from the bundled list, press Sort, and walk the room through three algorithms' results with confidence in their correctness.

## Devon the Developer

- **Role**: Developer refreshing their understanding of classic sorting algorithms or double-checking an implementation's behavior.
- **Goals**: Run the app locally in one command; read precise comparison and swap counts to sanity-check algorithm behavior; confirm edge cases behave as expected.
- **Pain points**: Heavyweight tools for a simple check; unclear counting definitions make side-by-side comparisons meaningless.
- **Context**: Terminal on a dev machine; comfortable with `streamlit run`; inputs small.
- **Success looks like**: Clone, run locally, paste an edge-case list, and see honest counts plus an accuracy pass for all three algorithms.
