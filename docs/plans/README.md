# Execution Plans & Dossiers

In the **NTC Micro-Harness Atomic Engineering** protocol (v2.1 Plugin Edition), planning and specifications are layered into distributed files across 6 `/ntc-*` steps to protect LLM context windows and guarantee token budget efficiency.

## Storage Structure

```text
docs/
├── prototypes/
│   ├── registry.md                           <-- UI PROTOTYPE & DESIGN SYSTEM REGISTRY (SCR-<MOD>-<NN>, Step 2 /ntc-prototype)
│   └── <module-slug>/
│       └── scr-01-<slug>.html                <-- APPROVED INTERACTIVE HTML PROTOTYPE (with data-testid anchors)
├── modules-spec/
│   ├── system.md                             <-- Detailed Spec + Phase Sequence of reserved SYS module (Step 4 /ntc-modules)
│   └── <module-slug>.md                      <-- DETAILED MODULE SPEC + UI Screen Mapping + Module Phase Sequence (<MOD>-P<NN>)
└── plans/
    ├── system-roadmap.md                     <-- PROJECT ROADMAP (Global Phases, Module Registry, Active Work Pointer, CR Log)
    ├── contract-registry.md                  <-- CROSS-MODULE CONTRACTS (provider, consumers, spec path, version, status)
    ├── active/
    │   └── <module-slug>/
    │       ├── phase-01-<slug>.md            <-- ACTIVE PHASE DOSSIER (IN_PROGRESS, with real-time 🎫 Resume Ticket)
    │       └── phase-02-<slug>.md            <-- PRE-GENERATED PHASE DOSSIER (PENDING until phase-01 is archived)
    └── completed/
        └── <module-slug>/
            └── phase-<NN>-<slug>.md          <-- DONE: archived, verified dossiers (immutable audit record)
```

## 6-Step `/ntc-*` Operating Lifecycle

1. **Step 1 (`/ntc-init`):** Connect Git remote `origin` (optional), answer clarifying questions, and generate `PRD.md` + `ARCHITECTURE.md`.
2. **Step 2 (`/ntc-prototype`):** If `UI Required: YES`, populate `docs/prototypes/registry.md` and create interactive HTML prototypes (`docs/prototypes/<module-slug>/scr-<nn>-*.html`) with `data-testid` anchors from `PRD.md` & `ARCHITECTURE.md` until approved (`--approve` → `APPROVED`).
3. **Step 3 (`/ntc-spec`):** Synthesize `SPEC.md`, `docs/plans/system-roadmap.md`, and `docs/plans/contract-registry.md`, then map and install module AI skills into `.agents/skills/` and `ai-skill-maps.md`.
4. **Step 4 (`/ntc-modules`):** Read each module's skills in `ai-skill-maps.md` + `SPEC.md` + approved prototypes to instantiate `docs/modules-spec/<module-slug>.md` for all modules, and generate `STEP-by-STEP.md` upon approval (`--approve`).
5. **Step 5 (`/ntc-plan`):** Pre-generate **all Phase Dossiers** (`docs/plans/active/<module-slug>/phase-<NN>-<slug>.md`) with full Major & Level-4 Atomic Task WBS across **all modules** before writing any production code.
6. **Step 6 (`/ntc-run` / `"tiếp tục"`):** Execute one Atomic Task per turn (`1 Turn = 1 Task`) with 1:1 UI Prototype parity and End-of-Turn Atomic Git Commit checkpointing. Handle mid-flight changes via `/ntc-cr` (`CR-<NN>`), and finish with the Closing `SYS` Full-Stack E2E Gate (`/ntc-status --e2e`).
