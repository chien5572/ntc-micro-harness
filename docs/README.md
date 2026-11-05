# Documentation Map

Start with the smallest authoritative surface.

## NTC Micro-Harness v2.1 Plugin Hierarchy (6-Step `/ntc-*` Workflow)

- `../PRD.md` & `../ARCHITECTURE.md`: Generated in **Step 1 (`/ntc-init`)** after Git remote connection (`origin`) and interactive requirements Q&A.
- `prototypes/`: UI Prototype & Design System Registry (`docs/prototypes/registry.md`) and self-contained interactive HTML/CSS prototypes (`docs/prototypes/<module-slug>/scr-<nn>-*.html`) with `data-testid` anchors, created and approved (`APPROVED`) in **Step 2 (`/ntc-prototype`)** from `PRD.md` & `ARCHITECTURE.md` whenever `UI Required: YES`.
- `../SPEC.md`: Supreme overall system specification synthesized and locked in **Step 3 (`/ntc-spec`)** from `PRD.md`, `ARCHITECTURE.md`, and the approved UI prototypes.
- `../ai-skill-maps.md`: Created in **Step 3 (`/ntc-spec`)** right after locking `SPEC.md`; maps every module/service and phase to mandatory local skills in `.agents/skills/<skill-name>/SKILL.md` so the Agent reads those skills before authoring detailed module specs, WBS plans, or code.
- `modules-spec/`: Detailed specifications for every module (`docs/modules-spec/<module-slug>.md`), created in **Step 4 (`/ntc-modules`)** using `SPEC.md`, `ai-skill-maps.md`, `docs/plans/contract-registry.md`, and `docs/prototypes/registry.md`, holding each module's **Module Phase Sequence** (`<MOD>-P<NN>`).
- `../STEP-by-STEP.md`: Created at the end of **Step 4 (`/ntc-modules --approve`)** as a **Human-Only Playbook** containing dependency flows, `/ntc-*` commands, and copy-paste prompts. **Agents do not read this file.**
- `../AGENTS.md` & `WORKFLOW.md`: Mandatory agent operating contract, 6-step `/ntc-*` gated lifecycle, `/ntc-run` / `"tiếp tục"` state machine, 1:1 UI parity, Atomic Git Commit checkpointing, `/ntc-cr` Change Request protocol, and crash recovery rules.
- `plans/`: Layered execution memory —
  - `plans/system-roadmap.md`: Project Roadmap (Global Phases with `SYS` opening/closing E2E bookends, Module Registry, dependency graph, Active Work Pointer, `CR-<NN>` Change Request Log);
  - `plans/contract-registry.md`: Cross-module contracts (`CT-<PROVIDER>-<NN>`);
  - `plans/active/<module-slug>/`: Pre-generated Phase Dossiers (`phase-<NN>-<slug>.md`, **Step 5 `/ntc-plan`**) with real-time `🎫 Resume Ticket`;
  - `plans/completed/<module-slug>/`: Verified, archived Phase Dossiers (**Step 6 `/ntc-run`**, immutable audit trail).
- [`patterns/encoding-invariants.md`](patterns/encoding-invariants.md): Turn accepted architecture, reliability, security, and quality rules into native mechanical validation.
- `templates/`: Starter structures for `PRD.md` (`prd-template.md`), `ARCHITECTURE.md` (`architecture-template.md`), root `SPEC.md` (`spec-template.md`), system roadmap, contract registry, UI prototype registry (`ui-prototype-registry-template.md`), AI skill maps (`ai-skill-maps-template.md`), detailed module spec (`module-spec-template.md`), human step-by-step playbook (`step-by-step-template.md`), phase dossier, exec plan, decision (ADR), and application runbook.
- `../scripts/validate_plans.py`: Cross-platform Python structural validator and auto-synchronizer (`--fix`, invoked via `/ntc-status`).
