# Completed Execution Plans

Move a plan here only after its requested outcome and validation are recorded.
Completed plans are historical evidence, not default task instructions.

Keep a completed plan when it explains a consequential migration, recovery
procedure, architectural transition, or decision history that future work may
need. Ordinary bounded changes should rely on Git and pull-request history.

## Layout

```text
completed/<module-slug>/phase-<NN>-<slug>.md   # moved unchanged from ../active/<module-slug>/
completed/<module-slug>/plan-<slug>.md         # optional small bounded plans
```

- Files are moved, not copied: the same file name and contents as in `active/`.
- Archived files are immutable. Corrections belong in a new phase or a decision record.
- After moving, mark the phase `COMPLETED` in `docs/plans/modules/<module-slug>.md`.
