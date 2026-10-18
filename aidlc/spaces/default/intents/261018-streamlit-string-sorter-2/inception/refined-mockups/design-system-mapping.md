# Design System Mapping

## Design System

**Streamlit built-in components and default theme only.** No external component library, no custom CSS, no theming beyond Streamlit defaults (NFR2.1 simplicity, NFR2.3 self-contained, D4).

## Component → Streamlit Widget Map

| UI element | Streamlit widget | Notes |
|---|---|---|
| Page title | `st.title("Sorting Algorithm Playground")` | Renders h1; page header landmark |
| Manual string input | `st.text_area(label="Type or paste strings, one per line")` | Visible label, not placeholder-only |
| Bundled word picker | `st.multiselect(label="Pick words", options=BUNDLED_WORDS)` | Options from a shipped Python constant (FR1.5) |
| Input row layout | `st.columns(2)` | Text area left, multiselect right |
| Sort button | `st.button("Sort", type="primary")` | Never disabled; empty input shows warning path |
| Input echo | `st.caption("Input to sort: …")` | After successful sort only |
| Empty-input warning | `st.warning("Enter or select at least one string")` | Exact FR6.1 string; alert live region |
| Results hint (before first sort) | `st.info("Press Sort to compare the three algorithms")` | Empty state, not an error |
| Results layout | `st.columns(3)` | Equal columns; stack on narrow viewports (Streamlit default) |
| Algorithm name | `st.subheader("Bubble Sort" / "Selection Sort" / "Quick Sort")` | h3 under page h1 |
| Sorted list | `st.text("\n".join(sorted_list))` | Monospace block, one string per line |
| Comparisons count | `st.write(f"Comparisons: {n}")` | The step metric (D7) |
| Swap count | `st.write(f"Swaps: {n}")` | Separate from comparisons (FR4.3) |
| Accuracy | `st.write("✓ Accuracy: Pass")` / `st.write("✗ Accuracy: Fail")` | Icon + text; never color alone (D5) |

## Data Constants

| Constant | Source | Notes |
|---|---|---|
| `BUNDLED_WORDS` | Python list shipped in the app package | ~20–30 common words; fixed, no external fetch (FR1.5/AC1.2.3). Exact list is an implementation detail of Code Generation. |

## Theme / Styling

- Streamlit default light theme; no `config.toml` theme overrides in v1.
- No custom CSS, no `st.markdown(unsafe_allow_html=True)` for layout.
- Icons for accuracy are Unicode characters (✓ / ✗) in text — not image assets, not color-only.

## What is deliberately NOT mapped

| Concern | Why not |
|---|---|
| Custom fonts / colors | NFR2.1 simplicity; default theme meets AA contrast |
| Progress bars / spinners | Synchronous classroom-sized runs (D3) |
| Download / save buttons | Out of scope (NFR3.2, no file I/O) |
| Navigation / sidebar | Single screen (rough-mockups Q1) |
| Mobile-specific components | Desktop only (D6) |
