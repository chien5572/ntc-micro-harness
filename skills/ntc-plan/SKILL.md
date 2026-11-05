---
name: ntc-plan
description: "Step 5 / Gate 4 of NTC Micro-Harness (/ntc-plan): Pre-generate 100% of Phase Dossiers (docs/plans/active/<slug>/phase-<NN>-*.md) with Level-4 Atomic WBS across all modules and validate with scripts/validate_plans.py."
---

# `/ntc-plan` — Step 5 (Gate 4): Pre-Generate All Phase Dossiers & Level-4 Atomic WBS

Activate this skill whenever the user invokes **`/ntc-plan`** (Step 5 / Gate 4 of the NTC Micro-Harness workflow).

## Pre-Conditions
1. All registered modules in `docs/plans/system-roadmap.md` must have their detailed specifications in `docs/modules-spec/<module-slug>.md` (created and approved in Step 4 via `/ntc-modules`).
2. `ai-skill-maps.md` and `STEP-by-STEP.md` must exist at the repository root *(Remember: AI Agents must NOT read `STEP-by-STEP.md`; only verify its file existence)*.
3. If `UI Required: YES`, all registered UI screens in `docs/prototypes/registry.md` must have `Status: APPROVED`.

## Supported Flags & Arguments
- *(No flags)*: Generate all Phase Dossiers (`docs/plans/active/<module-slug>/phase-<NN>-<slug>.md`) for all modules in the project (or sequentially module by module to avoid truncation).
- `--module <MOD>`: Generate Phase Dossiers and Level-4 WBS for a specific module (e.g., `/ntc-plan --module AUTH`).
- `--verify`: Run `python scripts/validate_plans.py --fix` and verify that 100% of planned phases across all modules have valid dossiers in `docs/plans/active/` with `0 violations`.

---

## Mandatory Execution Sequence

### 1. Read Module Skills, Module Spec & Approved Prototypes
For each target module `<MOD>` (`<module-slug>`):
1. Read `ai-skill-maps.md` and the mandatory `.agents/skills/<skill>/SKILL.md` files mapped to `<MOD>`.
2. Read `docs/modules-spec/<module-slug>.md` (specifically `## 9. Module Phase Sequence` and `## 5.4 UI Screen & Prototype Mapping`).
3. Read `docs/plans/contract-registry.md` and (if UI module) `docs/prototypes/registry.md`.

### 2. Instantiate All Phase Dossiers (`docs/plans/active/<module-slug>/phase-<NN>-<slug>.md`)
For every planned phase `<MOD>-P<NN>` in `docs/modules-spec/<module-slug>.md`:
- Create `docs/plans/active/<module-slug>/phase-<NN>-<phase-slug>.md` from `docs/templates/phase-dossier-template.md`.
- **Resume Ticket Setup:**
  - For Phase `01` (`<MOD>-P01`): Set `- **Lifecycle Status:** READY_TO_EXECUTE` and `- **Module:** \`<MOD>\``.
  - For subsequent phases (`<MOD>-P02`, `<MOD>-P03`...): Set `- **Lifecycle Status:** PENDING` (so at most one dossier per module is active at a time).
- **Decompose into Major Tasks (`<MOD>-P<NN>.<M>`) and Level-4 Atomic Tasks (`<MOD>-P<NN>.<M>.<A>`):**
  - **Atomic Task `<MOD>-P<NN>.<M>.1` (Contract-First):** Types, Interfaces, DTOs, DDL Schemas, or OpenAPI/Protobuf definitions.
  - **Atomic Task `<MOD>-P<NN>.<M>.2` (Core Implementation):** Business logic, repository/controller, or UI component implementation.
    - **Mandatory for UI Tasks:** Explicitly include `UI Prototype Reference: SCR-<MOD>-<NN> (docs/prototypes/<module-slug>/scr-<nn>-<slug>.html)` and require 1:1 porting of DOM, CSS tokens, 4 visual states, and `data-testid` anchors.
  - **Atomic Task `<MOD>-P<NN>.<M>.3` (Executable Verification Proof):** Unit, integration, or UI component test suite (asserting `data-testid` anchors for UI tasks) with an exact `Executable Proof Command`.

### 3. Validate & Gate 4 Exit Lock
1. Update module status in `docs/plans/system-roadmap.md` to `READY`.
2. Run `python scripts/validate_plans.py --fix` and ensure `PASSED: 0 violations`.
3. **Hard Stop:** Present the WBS summary to the Human Architect for approval. **Do NOT write production code in Step 5.** Instruct the user to run **`/ntc-run`** (or type `"tiếp tục"`) once approved to start Step 6 (Gate 5).
