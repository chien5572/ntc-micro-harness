# Execution Plans & Dossiers

In the **Harness Atomic Engineering** protocol (Microservices Edition), planning is layered and execution documents are decoupled into distributed dossiers to protect LLM context windows and guarantee token budget efficiency.

## Storage Structure

```text
docs/plans/
├── system-roadmap.md                     <-- PROJECT ROADMAP (Global Phases, Module Registry, dependency graph, Active Work Pointer)
├── contract-registry.md                  <-- CROSS-MODULE CONTRACTS (provider, consumers, spec path, version, status)
├── modules/
│   ├── system.md                         <-- Blueprint of the reserved cross-cutting pseudo-module (SYS)
│   └── <module-slug>.md                  <-- MODULE BLUEPRINT (phases, diagrams, flows, contracts of ONE module)
├── active/
│   └── <module-slug>/
│       └── phase-<NN>-<slug>.md          <-- IN PROGRESS: Module Phase Dossier (with real-time Resume Ticket)
└── completed/
    └── <module-slug>/
        └── phase-<NN>-<slug>.md          <-- DONE: archived, verified dossiers (immutable audit record)
```

- `active/` answers *"what is being worked on?"*; `completed/` answers *"what is finished?"*.
- Each `active/<module-slug>/` holds **at most one** phase dossier. Small bounded plans (`docs/templates/exec-plan.md`) may also live there as `plan-<slug>.md`.

## Operating Lifecycle

1. **Gate 2:** At project inception, `system-roadmap.md` and `contract-registry.md` are derived from `SPEC.md`.
2. **Gate 3:** When a module is to be planned, instantiate `modules/<module-slug>.md` from `docs/templates/module-roadmap-template.md`.
3. **Gate 4:** When starting phase N of a module, instantiate `active/<module-slug>/phase-<NN>-<slug>.md` from `docs/templates/phase-dossier-template.md`.
4. **Gate 5:** Throughout execution, the `🎫 Resume Ticket` at the top of the active dossier is updated before ending any turn, and the Active Work Pointer in `system-roadmap.md` is updated whenever stage or focus changes.
5. **Archival:** When all Atomic Tasks pass verification, move the dossier to `completed/<module-slug>/`, then update the phase status in the Module Blueprint and the pointer / Global Phase status in `system-roadmap.md`.
6. **Validation:** run `scripts/validate-plans.ps1` after any planning change or archival step.
