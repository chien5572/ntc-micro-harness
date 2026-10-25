# Execution Plan: Title

Date: YYYY-MM-DD
Status: Active | Blocked | Completed

> **Architecture Guidance:**
> - For small, single-session, bounded work: Use this concise flat plan, stored at
>   `docs/plans/active/<module-slug>/plan-<slug>.md` (use `system` for cross-module work) and moved to
>   `docs/plans/completed/<module-slug>/` when verified.
> - For complex systems, multi-service backends, or multi-phase projects: Use the layered standard:
>   1. `docs/templates/system-roadmap-template.md` -> located at `docs/plans/system-roadmap.md`
>   2. `docs/templates/contract-registry-template.md` -> located at `docs/plans/contract-registry.md`
>   3. `docs/templates/module-spec-template.md` -> located at `docs/modules-spec/<module-slug>.md`
>   4. `docs/templates/ai-skill-maps-template.md` -> located at `ai-skill-maps.md`
>   5. `docs/templates/step-by-step-template.md` -> located at `STEP-by-STEP.md` (Human-Only Playbook)
>   6. `docs/templates/phase-dossier-template.md` -> located at `docs/plans/active/<module-slug>/phase-<NN>-<slug>.md`

## Outcome
Describe the observable result this work must produce.

## Context
Link the relevant product, module spec (`docs/modules-spec/<module-slug>.md`), skill map (`ai-skill-maps.md`), decision, code, and validation truth.

## Approach & Atomic Tasks
- [ ] Task 1
- [ ] Task 2

## Validation
- Focused proof:
- Repository checks (`python scripts/validate_plans.py`):

## Result
Complete after implementation. Record verified outcome and evidence.
