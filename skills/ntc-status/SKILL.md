---
name: ntc-status
description: "Status, Validation & Closing E2E Gate of NTC Micro-Harness (/ntc-status): Run scripts/validate_plans.py [--fix], display project progress across modules/phases, or trigger the closing SYS-P<FINAL> Cross-Module Integration & Full-Stack E2E phase (--e2e)."
---

# `/ntc-status` — Structural Validation, Progress Dashboard & Closing `SYS` E2E Gate

Activate this skill whenever the user invokes **`/ntc-status`**.

## Supported Flags & Arguments
- *(No flags)*: Run `python scripts/validate_plans.py` and display a clean summary table of all registered modules, their phase statuses (`COMPLETED`, `IN_PROGRESS`, `PENDING`), active `🎫 Resume Ticket` pointers, and any open Change Requests (`CR-<NN>`).
- `--fix`: Run `python scripts/validate_plans.py --fix` to automatically synchronize `## 9. Module Phase Sequence` in all `docs/modules-spec/<slug>.md` files and `## 5. Active Work Pointer` in `docs/plans/system-roadmap.md` from disk.
- `--e2e`: Trigger or execute the closing **`SYS` Cross-Module Integration & Full-Stack E2E Gate (`SYS-P<FINAL>`)** in the final Global Phase (`GP-<FINAL>`).

---

## Mandatory Execution Sequence

### Mode A: Status & Structural Validation (Default / `--fix`)
1. Run `python scripts/validate_plans.py --fix` (if `--fix` is passed) or `python scripts/validate_plans.py`.
2. Read `docs/plans/system-roadmap.md`, `docs/prototypes/registry.md`, and any `IN_PROGRESS` dossiers in `docs/plans/active/`.
3. Present a concise **Project Health & Progress Report**:
   - **Current Lifecycle Step:** (Step 1 `PRD/ARCH` → Step 2 `Prototype` → Step 3 `SPEC/Skills` → Step 4 `Module Specs` → Step 5 `WBS Plan` → Step 6 `Atomic Run`).
   - **Validation Result:** `PASSED (0 violations)` or exact list of violations with fix hints.
   - **Module & Phase Matrix:** Module Code, Status, Completed Phases, Active Phase & Next Atomic Task (`<MOD>-P<NN>.<M>.<A>`).
   - **Recommended Next Command:** Exact `/ntc-*` command for the user to run next.

### Mode B: Closing `SYS` Cross-Module Integration & Full-Stack E2E Gate (`--e2e`)
When invoked with **`/ntc-status --e2e`**:
1. **Verify Entry Pre-Condition:** Check that all domain and UI module phases from earlier Global Phases (`GP-01..GP-<N-1>`) are archived in `docs/plans/completed/<module-slug>/`. If any domain/UI module still has uncompleted phases in `docs/plans/active/`, report which module phases must finish first.
2. **Activate `SYS-P<FINAL>` (`docs/plans/active/system/phase-<FINAL>-*.md`):**
   - Set `- **Lifecycle Status:** IN_PROGRESS` on the closing `SYS` dossier and run `python scripts/validate_plans.py --fix`.
   - Execute the next unchecked Atomic Task in `SYS-P<FINAL>` (`1 Turn = 1 Task`):
     - Boot the live integrated stack (Database + Migrations + Backend Services + API Gateway + Compiled Frontend).
     - Run live cross-module contract (`CT-*`) round-trip tests with **zero mocks**.
     - When `UI Required: YES`, run automated Full-Stack E2E browser tests (e.g., Playwright/Cypress) targeting the exact **`data-testid="scr-<nn>-..."` anchors** from `docs/prototypes/registry.md` across the full loop: UI interaction → API request → DB persistence → UI state render (`default`, `loading`, `empty`, `error`).
   - Check off `- [x]`, update the `🎫 Resume Ticket`, run `python scripts/validate_plans.py --fix`, and create an Atomic Git Commit checkpoint.
