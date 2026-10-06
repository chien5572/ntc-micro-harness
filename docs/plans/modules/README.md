# Module Blueprints

One file per module (service), instantiated during **Gate 3** from
`docs/templates/module-roadmap-template.md`:

```text
modules/<module-slug>.md
```

Each blueprint is the module's own roadmap: charter, tech stack, internal
architecture diagram, data ownership, provided/consumed contracts, core flows,
and the **Module Phase Sequence** (`<MOD>-P<NN>`, each aligned to a Global Phase).

## Rules

- `<module-slug>` (lowercase) and `<MOD>` (2-5 uppercase letters) are assigned once
  in the Module Registry of `docs/plans/system-roadmap.md` and never reused.
- `system.md` / `SYS` is reserved for cross-cutting work: shared contract
  packages, local orchestration, CI, gateway (unless it is its own service),
  and end-to-end tests.
- A blueprint must not contradict the Project Roadmap or
  `docs/plans/contract-registry.md`; new or changed contracts are proposed
  explicitly in the registry.
- Blueprint one module per request and wait for approval before starting any
  phase of it.
- Phase dossiers never live here: they live in `docs/plans/active/<module-slug>/`
  and move to `docs/plans/completed/<module-slug>/` when verified.
