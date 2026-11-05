---
name: ntc-modules
description: "Step 4 of NTC Micro-Harness (/ntc-modules): Read SPEC.md, ai-skill-maps.md, and approved UI prototypes to generate detailed specifications (docs/modules-spec/<slug>.md) for each module/service, and generate STEP-by-STEP.md upon approval."
---

# `/ntc-modules` — Step 4: Detailed Module Specifications (`docs/modules-spec/<slug>.md`) & `STEP-by-STEP.md`

Activate this skill whenever the user invokes **`/ntc-modules`** (Step 4 of the NTC Micro-Harness workflow).

## Pre-Conditions
1. Overall `SPEC.md`, `docs/plans/system-roadmap.md`, `docs/plans/contract-registry.md`, and `ai-skill-maps.md` must exist and be locked from Step 3 (`/ntc-spec`).
2. If `UI Required: YES`, all UI prototypes in `docs/prototypes/registry.md` must be `APPROVED`.

## Supported Flags & Arguments
- *(No flags)*: Generate `docs/modules-spec/<module-slug>.md` for all registered modules in `docs/plans/system-roadmap.md` (or sequentially module by module if there are many modules to avoid output truncation).
- `--module <MOD>`: Generate or refine the detailed specification for a single module code (e.g., `/ntc-modules --module AUTH`).
- `--approve`: Mark all module specifications as reviewed/approved (`SPEC_REVIEW` / `READY` in `docs/plans/system-roadmap.md`), automatically generate the Human-Only Playbook **`STEP-by-STEP.md`**, run `python scripts/validate_plans.py --fix`, and unlock **Step 5 (`/ntc-plan`)**.

---

## Mandatory Execution Sequence

### 1. Activate Module Skills from `ai-skill-maps.md` First
Before authoring `docs/modules-spec/<module-slug>.md` for any module `<MOD>`:
1. Read `ai-skill-maps.md` to identify all mandatory skills mapped to `<MOD>`.
2. Read the corresponding `.agents/skills/<skill-name>/SKILL.md` files so that the module's database schemas, architecture layers, API contracts, and UI component rules follow those skills' best practices.

### 2. Author `docs/modules-spec/<module-slug>.md` for Every Registered Module
Instantiate `docs/modules-spec/<module-slug>.md` from `docs/templates/module-spec-template.md` for every module in `docs/plans/system-roadmap.md` (including `docs/modules-spec/system.md` for `SYS`):
- **Section 1 & 2:** Traceability to `SPEC.md`, In-Scope/Out-of-Scope boundaries, and User Stories.
- **Section 3:** Tech Stack, Runtime, Applied Skills (from `ai-skill-maps.md`), and exact Build/Test/Lint commands.
- **Section 4:** Exact Domain Data Models & Storage Schema (complete SQL DDL / Prisma / ORM schemas, indexes, constraints, Redis key patterns).
- **Section 5:** Cross-Module Contracts (`CT-<MOD>-<NN>` provided and consumed) AND **Section 5.4: UI Screen & Prototype Mapping (`SCR-<MOD>-<NN>`)** for UI modules (explicitly linking each screen to its approved `docs/prototypes/<slug>/scr-<nn>-*.html` file and `data-testid` anchors).
- **Section 6 & 7:** Sequence diagrams, State Machine transitions, edge cases, and **Given / When / Then** acceptance criteria.
- **Section 8:** NFRs and standardized Error Codes.
- **Section 9 (`## 9. Module Phase Sequence`):** Planned phases (`<MOD>-P01`, `<MOD>-P02`...) mapped to Global Phases (`GP-<NN>`), with `Status: PENDING`.
  - For `system.md` (`SYS`), include both the opening foundation phase (`SYS-P01` in `GP-01`) and the closing Cross-Module Integration & Full-Stack E2E phase (`SYS-P<FINAL>` in `GP-<FINAL>`).

### 3. Approval & Automatic `STEP-by-STEP.md` Generation (`--approve`)
- Present the generated `docs/modules-spec/*.md` files to the Human Architect for review.
- When the user approves (`/ntc-modules --approve` or confirms approval):
  1. Instantiate **`STEP-by-STEP.md`** at the repository root (from `docs/templates/step-by-step-template.md`), tailored with the project's actual module codes, dependency order, `/ntc-plan` / `/ntc-run` / `/ntc-cr` / `/ntc-status` commands, and copy-paste prompts.
  2. Update module statuses in `docs/plans/system-roadmap.md` from `PLANNED` to `SPEC_REVIEW` (or `READY`).
  3. Run `python scripts/validate_plans.py --fix` and confirm `PASSED: 0 violations`.
  4. Instruct the user to run **`/ntc-plan`** to begin **Step 5 (Gate 4: Pre-Generate All Phase Dossiers & Level-4 WBS)**.
