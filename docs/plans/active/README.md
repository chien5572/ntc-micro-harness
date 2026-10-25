# Active Execution Plans (`docs/plans/active/`)

Pre-generated and in-progress Phase Dossiers, grouped by module:

```text
active/<module-slug>/phase-01-<slug>.md   # Active Phase Dossier (Lifecycle Status: IN_PROGRESS | PHASE_COMPLETED)
active/<module-slug>/phase-02-<slug>.md   # Pre-generated Next Phase Dossier (Lifecycle Status: PENDING)
active/<module-slug>/plan-<slug>.md       # Optional small bounded plan (docs/templates/exec-plan.md)
```

## Rules

- `<module-slug>` must be registered in the Module Registry of `docs/plans/system-roadmap.md` and have a specification at `docs/modules-spec/<module-slug>.md`.
- During **Gate 4**, **all planned Phase Dossiers for all modules** are pre-generated here before code implementation (Gate 5) begins.
- Within any `<module-slug>/` folder, **at most one** Phase Dossier may have `Lifecycle Status: IN_PROGRESS` (or `INTERRUPTED` / `PHASE_COMPLETED` awaiting phase transition) at a time. Subsequent phases in the queue keep `Lifecycle Status: PENDING` (or `READY_TO_EXECUTE`).
- Keep the `🎫 Resume Ticket`, task checkboxes, and verification logs current on every turn.
- When all Atomic Tasks of `<MOD>-P<NN>` are verified and the user issues `"tiếp tục phase <MOD>-P<NN+1>"`, move `phase-<NN>-<slug>.md` to `../completed/<module-slug>/`, activate `phase-<NN+1>-<slug>.md`, and run `python scripts/validate_plans.py --fix`.
