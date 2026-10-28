# Reverse Engineering Timestamp

## Run Record

- Date: 2026-10-29
- Commit: df37765

Notes on this run:
- The commit requested for this run was `745cec4`. That object does not exist in this repository (`git cat-file -t 745cec4` reports it missing). The recorded commit is HEAD, `df37765`.
- The working tree is not clean. Uncommitted changes at scan time: `README.md` (Setup, Run, and Checks sections added), `aidlc/spaces/default/intents/intents.json`, and an audit shard under the `261018-streamlit-string-sorter-2` intent. Only `README.md` is in the analyzed paths.
- The gate (Black, Ruff, pytest) was not executed in this run.

## Scope of Analysis

```yaml
scope_version: 1
kind: full
intent: uvx-migration
fingerprint: 745cec4aa0edae3419cf39855a422ba4aa6f117d
analyzed:
  paths:
    - ./
  components:
    - app
    - sorting_core
    - sorting_core.types
    - sorting_core.normalize
    - sorting_core.algorithms
    - sorting_core.engine
    - sorting_core.checker
    - sorting_core.runner
    - sorting_core.words
    - tests
    - ci-workflow
    - devcontainer
    - project-configuration
shallow:
  paths: []
```
