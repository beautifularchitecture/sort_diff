# Accessibility Checklist — WCAG 2.1 Level AA

Target: WCAG 2.1 AA (D5). Checklist items are verified against Streamlit's default rendering; items outside Streamlit's control are noted. Rough mockups chose "basic accessibility"; AA is the working target for the items below.

## Perceivable

| # | Requirement | Status in this design | How |
|---|---|---|---|
| P1 | Text contrast ≥ 4.5:1 | Relies on Streamlit default theme | Default theme text meets AA; no custom low-contrast styles introduced (D4) |
| P2 | UI component contrast ≥ 3:1 | Relies on Streamlit default theme | Buttons, inputs use default theme borders/fills |
| P3 | Not color-alone meaning | **Met by design** | Accuracy is `✓ Pass` / `✗ Fail` text + icon (D5); warning uses ⚠ + text via `st.warning` |
| P4 | Text alternatives for non-text content | **Met by design** | No image assets; Unicode icons carry adjacent text |
| P5 | Content readable at 200% zoom | Relies on Streamlit responsive reflow | Three-column row stacks on narrow widths; no fixed pixel widths in custom code |

## Operable

| # | Requirement | Status in this design | How |
|---|---|---|---|
| O1 | All functionality via keyboard | **Met by design** | text_area, multiselect, and button are fully keyboard-operable Streamlit widgets |
| O2 | Visible focus indicator | Relies on Streamlit default | Streamlit renders default focus outlines; we never remove them (no custom CSS, D4) |
| O3 | Logical tab order | **Met by design** | Order: text area → multiselect → Sort → (no focusable results); matches visual order |
| O4 | No keyboard traps | **Met by design** | No modals, no custom widgets; Tab always exits every control |
| O5 | No time limits | **Met by design** | No timers, no auto-redirects, no expiring sessions |
| O6 | Touch targets ≥ 44×44 | Relies on Streamlit defaults | Desktop-only app (D6); touch targets not in scope |

## Understandable

| # | Requirement | Status in this design | How |
|---|---|---|---|
| U1 | Page language declared | Relies on Streamlit | Streamlit emits `<html lang="en">` by default |
| U2 | Visible labels before inputs | **Met by design** | `label=` on text_area and multiselect; Sort has visible text (D4, interaction-spec) |
| U3 | Error identification in text | **Met by design** | Empty-input message is exact FR6.1 text in `st.warning` — specific, actionable, not a red border alone |
| U4 | Consistent identification | **Met by design** | Single screen; labels fixed across runs |
| U5 | No unexpected context change on focus/input | **Met by design** | Nothing auto-submits; Sort is the only trigger |

## Robust

| # | Requirement | Status in this design | How |
|---|---|---|---|
| R1 | Valid, structured markup | Relies on Streamlit | Streamlit generates the DOM; we add no raw HTML (D4) |
| R2 | Heading hierarchy in order | **Met by design** | h1 (title) → h3 (algorithm names); no skipped levels (mockups.md) |
| R3 | Live regions for dynamic updates | **Partially met by Streamlit** | `st.warning`/`st.info` render alert semantics; results container update is announced by Streamlit's rerun model — exact announcement behaviour verified in Build and Test with a screen reader pass |
| R4 | Unique IDs | Relies on Streamlit | Widget `key=` values are unique in the single-page app |

## Landmarks

| Landmark | Element | Notes |
|---|---|---|
| banner/header | Streamlit header (title) | Default |
| main | Streamlit main block | Input row, Sort, echo, results all inside main |

## Testing Plan (Build and Test stage)

1. **Keyboard-only pass**: complete the full journey (type, pick, Sort, read results) without a mouse.
2. **Screen reader spot-check** (NVDA or VoiceOver): verify labels announced, warning announced on empty Sort, algorithm headings reachable, accuracy line read as text.
3. **Contrast spot-check**: verify accuracy ✓/✗ and warning text against their backgrounds with a contrast checker (expected: pass under default theme).
4. **200% zoom**: verify three columns reflow and nothing clips.

## Known limitations (accepted, documented)

- Exact screen-reader announcement wording for the results-region update depends on Streamlit's internals; verified empirically in Build and Test, not spec-guaranteed at design time (R3).
- Touch-target sizing and mobile zoom are out of scope (desktop-only app, D6).
