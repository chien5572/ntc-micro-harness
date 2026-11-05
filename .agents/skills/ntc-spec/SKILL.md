---
name: ntc-spec
description: "Step 3 of NTC Micro-Harness (/ntc-spec): Synthesize overall SPEC.md, system-roadmap.md, and contract-registry.md from PRD/ARCHITECTURE/Prototypes, then discover and map AI skills per module into ai-skill-maps.md."
---

# `/ntc-spec` — Step 3: Overall `SPEC.md`, Project Roadmap, Contracts & AI Skill Playbook (`ai-skill-maps.md`)

Activate this skill whenever the user invokes **`/ntc-spec`** (Step 3 of the NTC Micro-Harness workflow).

## Pre-Conditions
1. `PRD.md` and `ARCHITECTURE.md` must exist.
2. If `UI Required: YES`, all UI screens in `docs/prototypes/registry.md` MUST be marked **`APPROVED`** before running `/ntc-spec`. If any screen is still `DRAFT`, stop and ask the user to approve prototypes first via `/ntc-prototype --approve`.

## Supported Flags & Arguments
- *(No flags)*: Synthesize `SPEC.md`, `docs/plans/system-roadmap.md`, and `docs/plans/contract-registry.md` from `PRD.md` + `ARCHITECTURE.md` + `docs/prototypes/registry.md`, and propose the module-by-module AI Skill Mapping table.
- `--skills-from "<url-or-source>"`: Search specific skill repositories/websites (e.g., `https://skillsmp.com/search`, `https://felo.ai/vi/skills`, GitHub) when proposing skills for modules.
- `--approve`: Lock `SPEC.md`, install the approved skills into `.agents/skills/<skill-name>/SKILL.md`, generate `ai-skill-maps.md`, run `python scripts/validate_plans.py`, and unlock **Step 4 (`/ntc-modules`)**.

---

## Mandatory Execution Sequence

### Sub-Step 3.1: Synthesize Overall `SPEC.md`, `system-roadmap.md` & `contract-registry.md`
1. **Generate `SPEC.md`** at the repository root (from `docs/templates/spec-template.md`), reconciling:
   - Executive summary, scope boundaries, and user flows from `PRD.md`.
   - Architecture pattern, tech stack, data models, and service decomposition from `ARCHITECTURE.md`.
   - Exact screen inventory (`SCR-<MOD>-<NN>`) and UI data requirements from the approved `docs/prototypes/registry.md`.
2. **Populate `docs/plans/system-roadmap.md`** (from `docs/templates/system-roadmap-template.md`):
   - Register every module in `## 2. Module Registry` with its unique 2–5 uppercase `Code` (`SYS`, `AUTH`, `CORE`, `WEB`...), lowercase `Slug`, `Code Root`, `Module Spec` path (`docs/modules-spec/<slug>.md`), `Depends On`, and `Status: PLANNED`.
   - Ensure the reserved `SYS` (`system`) module acts as both the **Opening Bookend** (`SYS-P01` in `GP-01` for shared contracts & infra) and the **Closing Bookend** (`SYS-P<FINAL>` in `GP-<FINAL>` for Cross-Module Integration & Full-Stack E2E verification).
3. **Populate `docs/plans/contract-registry.md`** (from `docs/templates/contract-registry-template.md`):
   - Register every cross-module contract (`CT-<PROVIDER>-<NN>`) required by the backend services and UI screens (`SCR-*`), initially with `Status: DRAFT`.

### Sub-Step 3.2: Propose & Map AI Skills per Module (`ai-skill-maps.md`)
Why here? By mapping and installing AI Skills in **Step 3 (before writing `docs/modules-spec/*.md` in Step 4)**, the Agent will read those specialized framework/domain skills *before* designing detailed DB schemas, API contracts, and state machines for each module in Step 4!

1. Based on the modules/services in `SPEC.md` and `docs/plans/system-roadmap.md`, propose a **Candidate AI Skill Mapping Table** assigning specific skills to each module (`SYS`, `AUTH`, `WEB`, etc.), always including:
   - `atomic-harness-gatekeeper` (mandatory protocol & gate enforcement across all modules)
   - `<project>-domain-invariants` (core business rules and data isolation invariants from `SPEC.md`)
   - `ui-prototype-fidelity` (mandatory for all UI modules when `UI Required: YES` to enforce 1:1 HTML prototype porting and `data-testid` parity)
   - Technology-specific skills matching each module's stack (e.g., Next.js/React, FastAPI/NestJS/Go, PostgreSQL/Prisma, Playwright E2E, `using-git-worktrees`).
2. Ask the user to review and approve both the overall `SPEC.md` and the proposed AI Skill list (or provide additional skill URLs via `--skills-from`).
3. **Upon User Approval (`/ntc-spec --approve`):**
   - Create/install each approved skill's instruction file at `.agents/skills/<skill-name>/SKILL.md`.
   - Instantiate **`ai-skill-maps.md`** at the repository root (from `docs/templates/ai-skill-maps-template.md`), documenting how each skill is used for each module/service and phase.
   - Run `python scripts/validate_plans.py` to verify `system-roadmap.md`, `contract-registry.md`, and `prototypes/registry.md` have `0 violations`.
   - Instruct the user to run **`/ntc-modules`** to begin **Step 4 (Detailed Module Specifications)**.
