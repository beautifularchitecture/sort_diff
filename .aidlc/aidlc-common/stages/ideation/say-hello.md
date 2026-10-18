---
slug: say-hello
name: Say Hello
phase: ideation
execution: ALWAYS
condition: Runs in Ideation to check in on the person's state of mind before the rest of the workflow proceeds.
lead_agent: psychological-safety-agent
support_agents: []
mode: inline
summary_confirmation: required
produces:
  - user-state-of-mind
  - say-hello-questions
consumes: []
requires_stage:
  - intent-capture
sensors:
  - required-sections
scopes:
  - enterprise
  - feature
  - mvp
  - poc
inputs: The person's own account of how they are feeling about this work
outputs: user-state-of-mind.md, say-hello-questions.md (under this stage's record dir, engine-resolved)
---

# Say Hello

Check in with the person about how they are feeling about this work, and record
what they tell you so later stages can pace and frame their own work around it.
This is a check-in, not an analysis: capture the person's own account faithfully
and move on.

## Steps

### Step 1: Load Prior Context

- Check for existing `<record>/` artifacts from prior sessions.
- Load guardrails from `aidlc/spaces/<active-space>/memory/{org,team,project}.md`
  only to respect any team norms about how a check-in is run (for example a team
  that prefers an async written check-in over a live one). Never use memory to
  override or reinterpret what the person reports.

### Step 2: Create the Check-In Questions File

Create `<record>/ideation/say-hello/say-hello-questions.md`.

Start the file with a `## Sources` register. Every source is a top-level
Markdown list item using exactly one of these forms:

```markdown
- [desc] Initial description: "<JSON-escaped authoritative user directions>"
- [scope] Workflow-selected scope: `<scope>`.
```

Then create consecutively numbered `## Q<n>.` questions covering:

- **Q1** — How are you feeling about this work right now? (for example: excited,
  optimistic but cautious, neutral, anxious or uncertain, overwhelmed)
- **Q2** — What is your biggest worry or concern going into this work?
- **Q3** — What would help you feel more confident about how this goes?

Every question MUST include an explicit `Not sure`, `None`, or `Not applicable`
option as appropriate, so a person with nothing to report is never forced to
select invented detail. Use the [Answer]: tag format from stage-protocol.md.
Include A-E options with X (Other) as the final option. Leave all [Answer]: tags
blank. Follow-up questions continue the same `Q<n>` numbering so their source ids
remain stable.

Then follow the unified question flow from stage-protocol.md section 3: offer
Guide Me / Edit File / Chat modes.

### Step 3: Collect and Analyze Answers

After all answers are collected:
1. Confirm ALL [Answer]: tags are filled in.
2. Run ambiguity detection and contradiction analysis.
3. Create follow-up questions if needed.

### Step 4: Generate the Artifact

Create `<record>/ideation/say-hello/user-state-of-mind.md` containing:

- **Mood / Emotional State** — what the person reported about how they feel.
- **Concerns and Worries** — what they named as their biggest worry or concern.
- **What Would Help** — what they said would make them more confident.
- **Confidence in the Work** — how confident they described themselves as being.
- **Assumptions & Open Questions** — write `None.` when there are none.

Ground every section through a confirmed `[Q<n>]` answer and cite it inline.
Record the person's own words wherever possible; never paraphrase a feeling into
something more or less intense than what they said. If a person declines to
answer a question, record `Not reported (open question) [assumption]` rather
than inventing an answer. Never turn an unselected option into a claim about the
person.

### Step 5: Resolve Assumptions

If the `## Assumptions & Open Questions` section contains `None.`, continue.
Otherwise:

1. Create `## Assumption Confirmation` in `say-hello-questions.md` if it is
   absent. Otherwise, reuse that single section, replacing its assumption list
   and options and resetting `[Answer]:` to blank. List every assumption and
   these options: `A. Accept assumptions` and `B. Convert to follow-up questions`.
2. Present those two options as a structured question, log it through the
   standard question decision/answer pair, END YOUR TURN, and wait.
3. On `Accept assumptions`, fill the confirmation answer exactly as
   `[Answer]: A. Accept assumptions` and retain the `[assumption]` labels.
   Acceptance does not turn an assumption into fact.
4. On `Convert to follow-up questions`, fill that answer, append consecutively
   numbered `Q<n>` follow-ups, collect and confirm their answers, and revise the
   artifact.

Do not proceed to completion while an assumption confirmation `[Answer]:` is
blank.

### Step 6: Completion Handoff

Hand completion to `stage-protocol.md` via
`aidlc engine orchestrate report --stage say-hello --result <outcome>`. That
`report` call owns every lifecycle transition and advancement; never perform one
in prose, and never narrate this bookkeeping to the person.

### Step 7: Present Completion & Request Approval

Use the stage-protocol.md completion template with completion emoji: :wave:
- Summary of the recorded state of mind.
- Review path: `<record>/ideation/say-hello/`
- Standard approval gate (Approve / Request Changes)

## Sensors

This stage's outputs are markdown artefacts under `<record>/ideation/say-hello/`.

Imports: `required-sections`.

Upstream targets: none.

`required-sections` checks that the artifact carries its declared headings. This
stage makes no external claims, so `claim-sources` is intentionally not imported;
the person's self-report is the only source and it is cited inline in Step 4.

## Learn

When `directive.protocol_modules` lists `learnings`, follow
`stage-protocol-learnings.md`: keep the diary at `directive.memory_path` while
working and run the ritual before the approval gate, applying its bootstrap,
`single: true`, per-unit, and gate-revision exemptions. When the module is absent,
skip both the diary and the ritual.
