---
name: ntc-run
description: "Step 6 / Gate 5 of NTC Micro-Harness (/ntc-run or 'tiếp tục'): Execute strictly 1 Atomic Task per turn with 3-Step Crash Recovery, 1:1 UI Prototype Parity, Executable Proof, Resume Ticket update, and Atomic Git Commit checkpointing."
---

# `/ntc-run` (or `"tiếp tục"`) — Step 6 (Gate 5): Atomic Implementation & State Machine

Activate this skill whenever the user invokes **`/ntc-run`**, **`"tiếp tục"`**, **`"continue"`**, or **`"tiếp tục phase <MOD>-P<NN>"`**.

## Pre-Conditions (Gate 4 Exit Lock Check)
Before writing any production code:
- All registered modules must have their Phase Dossiers pre-generated in `docs/plans/active/<module-slug>/`.
- `ai-skill-maps.md` and `STEP-by-STEP.md` must exist at the repository root *(Remember: AI Agents must NEVER read `STEP-by-STEP.md`)*.
- If `UI Required: YES`, all referenced UI prototypes (`SCR-<MOD>-<NN>`) in `docs/prototypes/registry.md` must be `APPROVED`.

## Supported Flags & Arguments
- *(No flags)* or `"tiếp tục"`: Execute the next sequential unchecked `- [ ]` Atomic Task in the currently active module/phase (`docs/plans/system-roadmap.md` → `## 5. Active Work Pointer`).
- `--module <MOD>` (or `"tiếp tục <MOD>"`): Target a specific module's active phase dossier (e.g., `/ntc-run --module AUTH`).
- `--phase <MOD>-P<NN>` (or `"tiếp tục phase <MOD>-P<NN>"`): Archive the completed previous phase (`<MOD>-P<NN-1>`) into `docs/plans/completed/<module-slug>/`, activate `<MOD>-P<NN>`, synchronize via `validate_plans.py --fix`, and immediately execute its first Atomic Task (`<MOD>-P<NN>.1.1`).

---

## Mandatory Single-Turn Execution Protocol (`1 Turn = 1 Atomic Task`)

### Step 1: Resolve Target Dossier & Phase Boundary Guardrail
1. Inspect `docs/plans/system-roadmap.md` (`## 5. Active Work Pointer`) and `docs/plans/active/<module-slug>/`.
2. **If the user passed `--phase <MOD>-P<NN+1>` (or `"tiếp tục phase <MOD>-P<NN+1>"`):**
   - Verify that `<MOD>-P<NN>` has 0 unchecked `- [ ]` Atomic Tasks (`PHASE_COMPLETED`).
   - Move `docs/plans/active/<module-slug>/phase-<NN>-*.md` to `docs/plans/completed/<module-slug>/phase-<NN>-*.md`.
   - Set `- **Lifecycle Status:** IN_PROGRESS` in `docs/plans/active/<module-slug>/phase-<NN+1>-*.md`.
   - Run `python scripts/validate_plans.py --fix`.
   - Proceed immediately to execute the first unchecked Atomic Task (`<MOD>-P<NN+1>.1.1`) of the newly activated phase!
3. **If the user invoked plain `/ntc-run` or `"tiếp tục"` and the current phase has 0 unchecked `- [ ]` tasks left (`PHASE_COMPLETED`):**
   - **HARD STOP GUARDRAIL:** Do NOT advance to the next phase automatically.
   - Report clearly: *"Phase `<MOD>-P<NN>` đã hoàn thành toàn bộ Atomic Tasks. Vui lòng nhập `/ntc-run --phase <MOD>-P<NN+1>` (hoặc `tiếp tục phase <MOD>-P<NN+1>`) để lưu trữ phase hiện tại và chuyển sang phase kế tiếp."*

### Step 2: 3-Step Crash / Dirty-State Recovery (Against `HEAD`)
Because every completed `[x]` Atomic Task is committed to `HEAD`, any uncommitted modification in `git status --short` / `git diff HEAD` belongs exclusively to an interrupted in-flight Atomic Task:
1. Identify the first unchecked `- [ ]` Atomic Task (`<MOD>-P<NN>.<M>.<A>`) and its `Target Files`.
2. Run `git status --short` and `git diff HEAD` scoped to `<MOD>`'s `Code Root`:
   - **Clean State:** Update the `🎫 Resume Ticket` to `Lifecycle Status: IN_PROGRESS` and `Active Atomic Task: <MOD>-P<NN>.<M>.<A>` (Write-Ahead), then proceed to Step 3.
   - **Completed-Before-Crash (Target files already modified and tests already PASS):** Mark `- [x]`, create the missing atomic git commit (`git commit -m "feat(<slug>): complete <MOD>-P<NN>.<M>.<A> (recovered)"`), log recovery in Section 4 of the dossier, and immediately execute the next unchecked Atomic Task in this same turn.
   - **Interrupted / Failing Mid-Turn Crash:** Report the interrupted file/line in 3 lines and finish that exact Atomic Task without duplicating code.

### Step 3: Activate Skills & Enforce 1:1 UI Prototype Parity
1. Read `ai-skill-maps.md` and read the `.agents/skills/<skill>/SKILL.md` files required for `<MOD>`.
2. **If the Atomic Task references a UI Prototype (`SCR-<MOD>-<NN>`):**
   - **MANDATORY:** Call `read_file` on `docs/prototypes/<module-slug>/scr-<nn>-*.html` and `docs/prototypes/registry.md` in this turn before writing code.
   - Port the exact DOM hierarchy, design tokens, CSS/Tailwind classes, 4 visual states (`default`, `loading`, `empty`, `error`), and **`data-testid="scr-<nn>-..."` attributes 1:1** into the production component. Never improvise layouts or drop `data-testid` hooks.
3. Implement **ONLY THIS SINGLE ATOMIC TASK** within `<MOD>`'s `Code Root` (no `// TODO` stubs).

### Step 4: Executable Proof, Dossier Update & Atomic Git Commit Checkpoint
1. Run the task's **`Executable Proof Command`** (unit tests, component `data-testid` assertions, typecheck, build) and verify it passes.
2. Check off `- [x]` on `<MOD>-P<NN>.<M>.<A>` in `docs/plans/active/<module-slug>/phase-<NN>-*.md`.
3. Update the **`🎫 Resume Ticket`**:
   - If more `- [ ]` tasks remain in this phase: set `Lifecycle Status: IN_PROGRESS` and `Immediate Next Atomic Action` to the next task ID.
   - If this was the **final** Atomic Task of `<MOD>-P<NN>`: set `Lifecycle Status: PHASE_COMPLETED` and announce: *"Đã hoàn thành toàn bộ Atomic Tasks của Phase `<MOD>-P<NN>`. Vui lòng nhập `/ntc-run --phase <MOD>-P<NN+1>` (hoặc `tiếp tục phase <MOD>-P<NN+1>`) để lưu trữ phase hiện tại và chuyển sang phase kế tiếp."*
4. Run `python scripts/validate_plans.py --fix` and ensure `0 violations`.
5. **Create Atomic Git Commit Checkpoint:**
   ```bash
   git add <code-root> docs/plans/ docs/modules-spec/
   git commit -m "feat(<slug>): complete <MOD>-P<NN>.<M>.<A> - <short summary>"
   ```
   Record the resulting commit hash in Section 4 (`Execution Evidence & Verification Log`) of the dossier.
