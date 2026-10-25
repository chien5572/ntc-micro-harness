# Execution Plans & Dossiers

In the **Harness Atomic Engineering** protocol (Microservices Edition v2.0), planning and specifications are layered into distributed files to protect LLM context windows and guarantee token budget efficiency.

## Storage Structure

```text
docs/
├── prototypes/
│   ├── registry.md                           <-- UI PROTOTYPE & DESIGN SYSTEM REGISTRY (SCR-<MOD>-<NN>, if UI)
│   └── <module-slug>/
│       └── scr-01-<slug>.html                <-- APPROVED INTERACTIVE HTML PROTOTYPE (with data-testid anchors)
├── modules-spec/
│   ├── system.md                             <-- Detailed Spec + Phase Sequence of reserved SYS module
│   └── <module-slug>.md                      <-- DETAILED MODULE SPEC + UI Screen Mapping + Module Phase Sequence (<MOD>-P<NN>)
└── plans/
    ├── system-roadmap.md                     <-- PROJECT ROADMAP (Global Phases, Module Registry, Dependency Graph, Active Work Pointer)
    ├── contract-registry.md                  <-- CROSS-MODULE CONTRACTS (provider, consumers, spec path, version, status)
    ├── active/
    │   └── <module-slug>/
    │       ├── phase-01-<slug>.md            <-- ACTIVE PHASE DOSSIER (IN_PROGRESS, with real-time 🎫 Resume Ticket)
    │       └── phase-02-<slug>.md            <-- PRE-GENERATED PHASE DOSSIER (PENDING until phase-01 is archived)
    └── completed/
        └── <module-slug>/
            └── phase-<NN>-<slug>.md          <-- DONE: archived, verified dossiers (immutable audit record)
```

- `docs/modules-spec/<module-slug>.md` defines **what** each module must do in detail and lists its phases.
- `docs/plans/active/<module-slug>/` holds all uncompleted Phase Dossiers pre-generated during **Gate 4**. Within a module, at most **one** dossier has `Lifecycle Status: IN_PROGRESS` (or `PHASE_COMPLETED` awaiting transition), while subsequent phases remain `PENDING`.
- `docs/plans/completed/<module-slug>/` holds verified, archived Phase Dossiers.

## Operating Lifecycle

1. **Gate 2:** Derive `system-roadmap.md` and `contract-registry.md` from `SPEC.md`.
2. **Gate 3:**
   - **Step 3.0 (If Project Has UI):** Populate `docs/prototypes/registry.md` and create interactive HTML prototypes (`docs/prototypes/<module-slug>/scr-<nn>-*.html`) with `data-testid` anchors for Human Architect visual approval (`APPROVED`).
   - **Step 3.1:** Instantiate `docs/modules-spec/<module-slug>.md` from `docs/templates/module-spec-template.md` for **all modules**.
   - **Step 3.2:** Ask the user for skill search websites, propose skills for user approval, install them into `.agents/skills/`, and generate `ai-skill-maps.md` (from `docs/templates/ai-skill-maps-template.md`).
   - **Step 3.3:** Generate `STEP-by-STEP.md` (from `docs/templates/step-by-step-template.md`) for the Human Architect (agents do not read `STEP-by-STEP.md`).
3. **Gate 4:** Pre-generate **all Phase Dossiers** (`docs/plans/active/<module-slug>/phase-<NN>-<slug>.md` from `docs/templates/phase-dossier-template.md`) with full Major & Atomic Task WBS across **all modules** before writing any production code.
4. **Gate 5:** Execute one Atomic Task per turn (`1 Turn = 1 Task`) driven by `"tiếp tục"`. When all Atomic Tasks of a phase complete, require `"tiếp tục phase <MOD>-P<NN+1>"` to archive the finished dossier to `completed/<module-slug>/`, activate the next dossier, and execute its first task.
5. **Validation & Auto-Sync:** Run `python scripts/validate_plans.py --fix` after any planning change or phase transition.
