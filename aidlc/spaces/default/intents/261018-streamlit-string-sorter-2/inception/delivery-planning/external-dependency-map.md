# External Dependency Map

Each external item, the Bolt that depends on it, and what happens if it slips.

| # | External item | Owner | Needed by | Blocks | Lead time | Slip plan |
|---|---|---|---|---|---|---|
| E1 | Streamlit Community Cloud account and app deploy connection | Human owner | Bolt 3 | US5.2 (auto-deploy on merge), Bolt 3 verification | Not measured; account creation is typically quick | Bolts 1 and 2 proceed; Bolt 3 waits. Local run (US5.1) is unaffected. |
| E2 | GitHub repository with Actions enabled and a `main` branch protected for squash-merge | Human owner | Bolt 3 | CI workflow and deploy trigger | Not measured; already in use by the team | Bolt 3 waits; Bolts 1 and 2 are unaffected. |

No other external system is used. The app has no network access at runtime (FR1.5, NFR2.3), and no external API is consumed (contract-summary.md, external boundaries: none).
