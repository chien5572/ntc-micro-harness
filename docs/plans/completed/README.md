# Completed Execution Plans (`docs/plans/completed/`)

Move a Phase Dossier here when all of its Atomic Tasks are verified (`- [x]`) and the user triggers the phase transition (`"tiếp tục phase <MOD>-P<NN+1>"`) or final archival. Completed dossiers are immutable historical evidence.

## Layout

```text
completed/<module-slug>/phase-<NN>-<slug>.md   # moved from ../active/<module-slug>/
completed/<module-slug>/plan-<slug>.md         # optional small bounded plans
```

## Rules

- Files are **moved** (not copied) from `docs/plans/active/<module-slug>/`.
- Every Atomic Task checkbox in an archived dossier must be checked (`- [x]`).
- Archived files are immutable. Post-archival fixes belong in the currently active phase dossier or a new phase dossier.
- After moving a dossier here, run `python scripts/validate_plans.py --fix` to automatically mark the phase `COMPLETED` in `docs/modules-spec/<module-slug>.md` and update the `Active Work Pointer` in `docs/plans/system-roadmap.md`.
