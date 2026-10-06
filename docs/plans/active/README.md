# Active Execution Plans

Work in progress, grouped by module:

```text
active/<module-slug>/phase-<NN>-<slug>.md   # Module Phase Dossier (docs/templates/phase-dossier-template.md)
active/<module-slug>/plan-<slug>.md         # Optional small bounded plan (docs/templates/exec-plan.md)
```

- Create a module folder only when that module starts its first phase. `<module-slug>` must be registered in the Module Registry of `docs/plans/system-roadmap.md`.
- Each module holds **at most one** phase dossier here at a time.
- Keep the `🎫 Resume Ticket`, progress, and validation current.
- Move the file to `../completed/<module-slug>/` only after the result is verified. Remove the module folder here if it becomes empty.
- The Active Work Pointer in `docs/plans/system-roadmap.md` must list exactly the dossiers present here.
