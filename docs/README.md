# Documentation Map

Start with the smallest authoritative surface.

## Harness Core Hierarchy

- `../SPEC.md`: Supreme system specification, functional boundaries, and architectural intent (defined by the Human Architect).
- `../AGENTS.md`: Mandatory agent operating contract, 5-stage gated lifecycle, `"tiếp tục"` state machine, and crash recovery rules.
- `WORKFLOW.md`: Detailed 5-stage gated protocol (`SPEC.md` → Project Roadmap → UI Prototypes (`Step 3.0`, if UI) + All Detailed Module SPECs + `ai-skill-maps.md` + `STEP-by-STEP.md` → All Phase Dossiers → Atomic Implementation), identifier convention, contract & UI prototype parity protocol, multi-agent worktree isolation, and archival.
- `prototypes/`: UI Prototype & Design System Registry (`docs/prototypes/registry.md`) and self-contained interactive HTML/CSS prototypes (`docs/prototypes/<module-slug>/scr-<nn>-*.html`) with `data-testid` anchors, created and approved in **Gate 3 (Step 3.0)** whenever the project has a user interface.
- `modules-spec/`: Detailed specifications for every module (`docs/modules-spec/<module-slug>.md`), linking to `SPEC.md`, `docs/prototypes/registry.md`, and holding each module's **Module Phase Sequence** (`<MOD>-P<NN>`).
- `../ai-skill-maps.md`: Created during Gate 3.2 after interactive skill discovery and user approval; maps every module and phase to mandatory local skills in `.agents/skills/<skill-name>/SKILL.md`.
- `../STEP-by-STEP.md`: Created during Gate 3.3 as a **Human-Only Playbook** containing dependency flows and copy-paste prompts. **Agents do not read this file.**
- `plans/`: Layered execution memory —
  - `plans/system-roadmap.md`: Project Roadmap (Global Phases, Module Registry, dependency graph, Active Work Pointer);
  - `plans/contract-registry.md`: Cross-module contracts (`CT-<PROVIDER>-<NN>`);
  - `plans/active/<module-slug>/`: Pre-generated Phase Dossiers (`phase-<NN>-<slug>.md`) with real-time `🎫 Resume Ticket`;
  - `plans/completed/<module-slug>/`: Verified, archived Phase Dossiers (immutable audit trail).
- [`patterns/encoding-invariants.md`](patterns/encoding-invariants.md): Turn accepted architecture, reliability, security, and quality rules into native mechanical validation.
- `templates/`: Starter structures for root spec, system roadmap, contract registry, UI prototype registry (`ui-prototype-registry-template.md`), detailed module spec (`module-spec-template.md`), AI skill maps (`ai-skill-maps-template.md`), human step-by-step playbook (`step-by-step-template.md`), phase dossier, exec plan, decision (ADR), and application runbook.
- `../scripts/validate_plans.py`: Cross-platform Python structural validator and auto-synchronizer (`--fix`).
