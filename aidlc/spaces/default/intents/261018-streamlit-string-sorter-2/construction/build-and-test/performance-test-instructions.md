# Performance Test Instructions

Test strategy: **Standard**. No numeric performance target exists. NFR3.6 constrains the app to classroom-sized inputs with no specific performance target beyond handling inputs of up to 100 strings responsively; U2's performance design records no latency budget.

## Applicable checks

1. **100-string cap (NFR3.6, SD-3).** `tests/ui/test_app.py::test_over_cap_input_shows_limit_message_and_runs_no_sorting` proves that 101 de-duplicated strings are refused with the exact limit message and that no sorting runs. The happy-path and edge tests prove that inputs at or below the cap sort normally.
2. **Bounded worst-case work.** Three sorts over at most 100 strings plus three accuracy checks, all in-process, with no I/O, caching layer, background worker, or network call (PD-1/PD-2 in the per-unit performance design).

## How to run

```bash
pytest tests/ui/ -q
```

Expected: `12 passed`; the cap test is included.

## Optional informational benchmark (not a gate)

There is no threshold to assert against; record the number only if a human asks for it.

```bash
python - <<'PY'
import time
from sorting_core import InputProcessor, SortingEngine

words = [f"item{i:03d}" for i in range(100)]
start = time.perf_counter()
sort_input = InputProcessor().normalize(words)
SortingEngine().run_all(sort_input)
print(f"{time.perf_counter() - start:.4f}s for 100 strings x 3 sorts")
PY
```

## Owning stage

No target is deferred: there is no numeric performance target to validate, so none remains unverified. If a numeric target is introduced later, **Performance Validation** (Operation) owns steady-state and load validation, and **Deployment Pipeline / Deployment Execution** own the AC5.2.x deployment-time observation.
