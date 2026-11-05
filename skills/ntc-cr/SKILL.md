---
name: ntc-cr
description: "Mid-Flight Change Request protocol of NTC Micro-Harness (/ntc-cr or 'yêu cầu thay đổi: ...'): Execute the 4-Step Delta Reverse-Unlock Protocol (CR-<NN>) to add/modify features, UI screens, or contracts during Step 5/6 without rewriting completed history."
---

# `/ntc-cr` — Mid-Flight Change Request (`CR-<NN>` 4-Step Delta Reverse-Unlock Protocol)

Activate this skill whenever the user invokes **`/ntc-cr "<description>"`** or types **`"yêu cầu thay đổi: <description>"`** / **`"change request: <description>"`** while the project is in Step 5 (Gate 4) or Step 6 (Gate 5).

## Core Rule: Immutable Completed History
- **NEVER** uncheck completed `- [x]` tasks or modify archived dossiers in `docs/plans/completed/<module-slug>/`.
- If the issue is just a local bug/edge-case within the current module with **no** contract (`CT-*`) or UI screen (`SCR-*`) changes, use **Tier 1 (In-Phase Dynamic Sub-Task `<MOD>-P<NN>.<M>.<A>a`)** instead.
- For any new feature, new/modified UI screen (`SCR-*`), or cross-module contract change (`CT-*`), execute the **4-Step Delta Reverse-Unlock Protocol** below.

## Supported Flags & Arguments
- `"/ntc-cr <description>"`: Start Step 1 & Step 2 of a new Change Request `CR-<NN>` (audit blast radius, update delta UI prototypes / contracts, and present for approval).
- `--approve-delta`: Approve the delta UI prototypes (`SCR-*` → `APPROVED`) and delta contracts (`CT-*`), apply Step 3 & Step 4 (update `SPEC.md`, `docs/modules-spec/<slug>.md`, append delta tasks/phase dossier, run `validate_plans.py --fix`, and commit the delta plan).

---

## The 4-Step Delta Reverse-Unlock Protocol (`CR-<NN>`)

### Step 1: Freeze & Register `CR-<NN>` Impact Audit
1. Pause Step 6 code execution.
2. Assign the next sequential ID `CR-<NN>` (e.g., `CR-01`) and add a row to `docs/plans/system-roadmap.md` (`## 6. Change Request (CR) Log`) with `Status: IN_REVIEW`.
3. Audit and report the **Delta Blast Radius**:
   - Impacted sections of `PRD.md` / `SPEC.md`
   - Impacted or new Cross-Module Contracts (`CT-<PROVIDER>-<NN>`)
   - Impacted or new UI Prototype Screens (`SCR-<MOD>-<NN>`)
   - Impacted Modules & Phases (`<MOD>-P<NN>`)

### Step 2: Delta UI Prototypes (`SCR-*`) & Contracts (`CT-*`) First
1. **If UI Screens are added or modified:**
   - Create or update ONLY the affected HTML prototype files at `docs/prototypes/<module-slug>/scr-<nn>-*.html` (ensuring all 4 states and `data-testid="scr-<nn>-..."` hooks are present).
   - Register/update the screen in `docs/prototypes/registry.md` and log `CR-<NN>` in Section 3 (`Prototype Revision & Change Log`).
   - **STOP and ask the Human Architect to preview and approve (`--approve-delta`)** so the screen status becomes `APPROVED`.
2. **If Cross-Module Contracts are added or modified:**
   - Register the new `CT-*` or bump the semantic version of the existing `CT-*` in `docs/plans/contract-registry.md`, and log `CR-<NN>` in Section 2 (`Contract Change Log`).

### Step 3: Append-Only Spec & Dossier Amendment
Once the user approves the delta prototypes/contracts (`--approve-delta`):
1. Update `SPEC.md` and the impacted `docs/modules-spec/<module-slug>.md` files with the delta requirements (and `ai-skill-maps.md` if new skills are needed).
2. Amend Phase Dossiers **without rewriting completed tasks**:
   - **Case A (Module still has an `IN_PROGRESS` or `PENDING` dossier in `docs/plans/active/<slug>/`):** Append new Major/Atomic Tasks (`<MOD>-P<NN>.<M>.1..3` tagged `[CR-<NN>]`) to the active/pending dossier.
   - **Case B (All previous phases of `<MOD>` are already archived in `docs/plans/completed/<slug>/`):** Append a new **Delta Phase (`<MOD>-P<NN+1>`)** to `docs/modules-spec/<slug>.md` (`## 9. Module Phase Sequence`) and generate a new dossier `docs/plans/active/<slug>/phase-<NN+1>-cr-<nn>-<slug>.md`.

### Step 4: Validate, Commit Delta Plan & Resume `/ntc-run`
1. Update `CR-<NN>` status in `docs/plans/system-roadmap.md` to `APPROVED` (and `COMPLETED` once implemented).
2. Run `python scripts/validate_plans.py --fix` and verify `PASSED: 0 violations`.
3. Stage and commit the planning delta:
   ```bash
   git add SPEC.md docs/
   git commit -m "chore(plan): apply CR-<NN> delta specs, prototypes, and WBS"
   ```
4. Announce that `CR-<NN>` is integrated and ready to execute via **`/ntc-run`** (or `"tiếp tục"`).
