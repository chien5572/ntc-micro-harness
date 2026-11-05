# Repository Workflow: NTC Micro-Harness Atomic Engineering Protocol (v2.1 Plugin Edition)

Repository discovery documents (`PRD.md`, `ARCHITECTURE.md`), visual prototypes (`docs/prototypes/`), overall specification (`SPEC.md`), skill playbooks (`ai-skill-maps.md`), detailed module specifications (`docs/modules-spec/`), plans, code, tests, and runtime signals are the single system of record.

Planning and specifications are layered across 6 progressive steps (`/ntc-*` slash commands) so each document stays small enough to protect the agent's context window:

```text
[Step 1: /ntc-init]       Git Remote Setup + Interactive Discovery Q&A
 ├─ PRD.md                                       Product Requirements, Personas, User Journeys & Screen Candidates
 └─ ARCHITECTURE.md                              System Topology, Tech Stack Matrix & Candidate Modules (with SYS)
     │
[Step 2: /ntc-prototype]  Interactive UI Prototyping (if UI Required: YES)
 ├─ docs/prototypes/registry.md                  Design System Tokens + UI Screen Registry (SCR-<MOD>-<NN> = APPROVED)
 └─ docs/prototypes/<module-slug>/scr-*.html     Self-contained clickable HTML/CSS prototypes with data-testid hooks
     │
[Step 3: /ntc-spec]       Overall SPEC + Roadmap + Contracts + AI Skill Mapping
 ├─ SPEC.md                                      Supreme System Specification (locked by Human Architect)
 ├─ docs/plans/system-roadmap.md                 Project Roadmap (Global Phases, Module Registry, Active Work Pointer, CR Log)
 ├─ docs/plans/contract-registry.md              Cross-module contracts (CT-<PROVIDER>-<NN>: REST/gRPC/Event/Schema)
 └─ ai-skill-maps.md                             AI Skill Playbook per Module/Service (.agents/skills/<skill>/SKILL.md)
     │
[Step 4: /ntc-modules]    Detailed Module Specifications (informed by SPEC.md + ai-skill-maps.md + Prototypes)
 ├─ docs/modules-spec/<module-slug>.md           Detailed Module SPEC + DDL + Contracts + SCR-* + Module Phase Sequence
 └─ STEP-by-STEP.md                              Human-Only Execution Playbook (Agents DO NOT read this file)
     │
[Step 5: /ntc-plan]       Pre-Generate 100% of Phase Dossiers & Level-4 WBS (Gate 4)
 └─ docs/plans/active/<module-slug>/
     ├─ phase-01-<slug>.md                       Pre-generated Phase Dossier (with real-time 🎫 Resume Ticket)
     └─ phase-02-<slug>.md                       Pre-generated Phase Dossier (PENDING until phase-01 completes)
         │
[Step 6: /ntc-run]        Atomic Implementation (Gate 5: 1 Turn = 1 Task + 1:1 UI Parity + Auto Git Commit)
 └─ docs/plans/completed/<module-slug>/phase-<NN>-<slug>.md   Verified, archived dossiers + Closing SYS E2E Gate
```

---

## 1. The 6-Step `/ntc-*` Operating Standard

Every software project, microservices platform, or modular monolith must strictly adhere to the following 6-step gated lifecycle.

### Step 1 (`/ntc-init`): Git Remote Setup, Interactive Q&A → `PRD.md` & `ARCHITECTURE.md`
1. **Git Remote Connection First (Before Any Work):**
   - When the Human Architect runs `/ntc-init` (or starts a new project), the Agent **first checks or asks for the Project Git Repository URL** (which the user may provide or leave blank for a local-only repository) alongside the basic project idea/requirements.
   - If `.git` does not exist, the Agent initializes `git init`. If the user provides a repository URL, the Agent configures `git remote add origin <repo-url>` (or `git remote set-url origin <repo-url>`) and verifies connectivity before proceeding.
   - If the workspace does not yet contain the Harness files (`AGENTS.md`, `docs/`, `scripts/validate_plans.py`), the Agent bootstraps them automatically.
2. **Interactive Requirements Clarification (Q&A):**
   - Based on the user's initial description, the Agent acts as a Solution Architect and asks **3–5 structured clarifying questions** (covering user roles/RBAC, core business flows, preferred tech stack/database, whether the system has a user interface `UI Required: YES | NO`, and key non-functional constraints).
3. **Author `PRD.md` & `ARCHITECTURE.md`:**
   - Once the Human Architect answers the clarifying questions, the Agent generates:
     - **`PRD.md`** (from `docs/templates/prd-template.md`): product vision, personas, in-scope/out-of-scope features, user journeys, and candidate UI screens (`SCR-<MOD>-<NN>`).
     - **`ARCHITECTURE.md`** (from `docs/templates/architecture-template.md`): high-level topology diagram, technology stack matrix, candidate module decomposition (`SYS` reserved for cross-cutting foundation & closing E2E), data ownership rules, and risk mitigations.
4. **Approval Gate (Step 1):** The Human Architect reviews and approves `PRD.md` and `ARCHITECTURE.md` before advancing to Step 2. **Writing production code is strictly forbidden.**

---

### Step 2 (`/ntc-prototype`): Interactive UI Prototyping & Visual Sign-Off (`docs/prototypes/`)
1. **Headless / Backend-Only Systems (`UI Required: NO`):**
   - If `PRD.md` specifies `UI Required: NO` (or `/ntc-init --no-ui` was used), the Agent sets `> **UI Required:** NO` in `docs/prototypes/registry.md`, leaves its screen table at the default placeholder row, and proceeds directly to **Step 3 (`/ntc-spec`)**.
2. **Systems with UI / Frontend Modules (`UI Required: YES`):**
   - Driven directly by `PRD.md` and `ARCHITECTURE.md` (before writing `SPEC.md`), the Agent:
     - Populates **`docs/prototypes/registry.md`** (from `docs/templates/ui-prototype-registry-template.md`) with locked **Design System Tokens** (color variables, typography, spacing, layout shell) and the **UI Screen & Prototype Registry (`SCR-<MOD>-<NN>`)**.
     - Generates self-contained, clickable HTML/CSS prototypes at **`docs/prototypes/<module-slug>/scr-<nn>-<slug>.html`** that the Human Architect can open directly in a browser.
     - Each HTML prototype **MUST** include:
       - All required visual states (`default`, `loading`, `empty`, `error`, plus key modals/drawers) with an interactive state switcher bar for easy review.
       - Explicit **`data-testid="scr-<nn>-<element>"`** attributes on the root container, forms, inputs, buttons, and data tables/lists.
       - Realistic sample data that exposes every field needed from backend contracts (`CT-*`).
3. **Iterative Refinement & Visual Sign-Off Gate (Hard Stop):**
   - The Human Architect previews the HTML files and uses `/ntc-prototype --revise "<feedback>"` (or `--screen SCR-<MOD>-<NN>`) to iterate until 100% satisfied.
   - When satisfied, the Human Architect runs `/ntc-prototype --approve` (or confirms approval), marking all active screens in `docs/prototypes/registry.md` as **`APPROVED`**. The Agent must NOT advance to Step 3 while any active screen is still `DRAFT`.

---

### Step 3 (`/ntc-spec`): Overall `SPEC.md`, Roadmap, Contracts & Skill Playbook (`ai-skill-maps.md`)
Step 3 executes in **two sequential sub-steps**:

#### Step 3.1: Synthesize Overall `SPEC.md`, `system-roadmap.md` & `contract-registry.md`
1. Combining the approved `PRD.md`, `ARCHITECTURE.md`, and the approved visual prototypes in `docs/prototypes/registry.md`, the Agent generates:
   - **`SPEC.md`** (from `docs/templates/spec-template.md`): the supreme Single Source of Truth locking functional scope, domain entities, core user flows, NFRs, and module boundaries.
   - **`docs/plans/system-roadmap.md`** (from `docs/templates/system-roadmap-template.md`): architecture blueprint, **Module Registry** (Code, Slug, Responsibility, Code Root, `docs/modules-spec/<slug>.md`, Depends On, Status), **Global Phases** (`GP-01` opening `SYS-P01` foundation through `GP-<FINAL>` closing `SYS-P<FINAL>` Full-Stack E2E), **Module Dependency Graph**, **Active Work Pointer**, and **Change Request (`CR-<NN>`) Log**.
   - **`docs/plans/contract-registry.md`** (from `docs/templates/contract-registry-template.md`): every known inter-module contract (`CT-<PROVIDER>-<NN>`), initially `DRAFT`.
2. The Human Architect reviews and locks the overall `SPEC.md`, Module Registry, and Contract Registry.

#### Step 3.2: Interactive Skill Discovery & `ai-skill-maps.md` Creation (Before Detailed Module Specs)
1. Immediately after `SPEC.md` and the Module Registry are locked, the Agent maps **which AI Skills are needed for each function (module/service)**.
2. The Agent asks the Human Architect for optional skill catalog URLs/repositories (e.g., `https://skillsmp.com/search`, `https://felo.ai/vi/skills`, GitHub repositories, or local skills) and proposes a **Candidate AI Skill Mapping Table** covering:
   - Custom project guardrails: `atomic-harness-gatekeeper`, `<project>-domain-invariants`, and `ui-prototype-fidelity` (when `UI Required: YES`).
   - Specialized technical/domain skills for each registered module (`SYS`, `AUTH`, `CORE`, `WEB`, etc.).
3. **User Approval Gate:** Once the Human Architect approves (`--approve`), the Agent installs/creates the skill files in `.agents/skills/<skill-name>/SKILL.md` and generates **`ai-skill-maps.md`** (from `docs/templates/ai-skill-maps-template.md`) as the official guide for how skills are applied to each module/service.

---

### Step 4 (`/ntc-modules`): Author ALL Detailed Module Specifications (`docs/modules-spec/<slug>.md`) & `STEP-by-STEP.md`
1. **Skill-Guided Module Spec Authoring:**
   - Before writing a module's detailed specification, the Agent **reads the mandatory skills assigned to that module in `ai-skill-maps.md`** (`.agents/skills/<skill>/SKILL.md`).
   - Guided by `SPEC.md`, the module's activated skills, `docs/plans/contract-registry.md`, and `docs/prototypes/registry.md` (`SCR-<MOD>-<NN>`), the Agent instantiates `docs/modules-spec/<module-slug>.md` (from `docs/templates/module-spec-template.md`) for **every registered module** (including `system.md`).
2. **Required Contents of `docs/modules-spec/<module-slug>.md`:**
   - Traceability to `SPEC.md` & Scope Boundaries (In-Scope / Out-of-Scope).
   - User Stories (*"As a [Role], I want [Action], so that [Benefit]"*).
   - Tech Stack, Applied AI Skills (from `ai-skill-maps.md`), Runtime & Build/Test Commands.
   - Exact Domain Data Models & Storage Schema (DDL tables, indexes, constraints, Redis keys).
   - Provided & Consumed Contracts (`CT-<MOD>-<NN>`), Events, payload validation rules, and **UI Screen & Prototype Mappings (`SCR-<MOD>-<NN>`)** for UI modules.
   - Core Business Flows (sequence diagrams), State Machine tables, and Edge Cases.
   - Stage-by-Stage Acceptance Criteria (**Given / When / Then**).
   - Non-Functional Requirements (NFRs) & Error Codes.
   - **Module Phase Sequence Table (`<MOD>-P<NN>`)** aligned to Global Phases.
3. **Human Approval & `STEP-by-STEP.md` Generation:**
   - The Human Architect reviews and approves all `docs/modules-spec/*.md` files (`/ntc-modules --approve`).
   - Immediately upon approval, the Agent generates **`STEP-by-STEP.md`** at the repository root (from `docs/templates/step-by-step-template.md`), packaging the module execution order, `/ntc-*` commands, and copy-paste prompts.
   - **Human-Only Rule:** `STEP-by-STEP.md` is strictly an operator guide for the Human Architect. **AI Agents MUST NOT read `STEP-by-STEP.md` during execution.**

---

### Step 5 (`/ntc-plan` — Gate 4): Pre-Generate ALL Phase Dossiers & WBS (Project-Wide)
1. When the Human Architect runs `/ntc-plan` (or prompts via `STEP-by-STEP.md`), the Agent reads `ai-skill-maps.md` (and `.agents/skills/*/SKILL.md`), `docs/prototypes/registry.md`, and `docs/modules-spec/<module-slug>.md`.
2. The Agent instantiates **ALL Phase Dossiers** (`docs/plans/active/<module-slug>/phase-<NN>-<slug>.md` from `docs/templates/phase-dossier-template.md`) for **every planned phase of every module in the entire project**.
3. Each Phase Dossier decomposes its work into **Major Tasks (`<MOD>-P<NN>.<M>`)** and **Level-4 Atomic Micro-Tasks (`<MOD>-P<NN>.<M>.<A>`)**:
   - Task `<M>.1`: Interface / Type / Schema / Contract Definition (Contract-First).
   - Task `<M>.2`: Core business logic or UI component implementation (with explicit `UI Prototype Reference: SCR-<MOD>-<NN>` pointing to `docs/prototypes/<module-slug>/scr-<nn>-*.html` for UI tasks).
   - Task `<M>.3`: Unit / Component tests & executable verification proof (asserting `data-testid` parity for UI tasks).
4. For each module, the first phase (`<MOD>-P01`) is initialized with `Lifecycle Status: READY_TO_EXECUTE` (or `IN_PROGRESS` when activated), while subsequent phases (`<MOD>-P02`, `<MOD>-P03`...) sit in `docs/plans/active/<module-slug>/` with `Lifecycle Status: PENDING`.
5. **Step 5 (Gate 4) Exit Lock:** Writing production code (Step 6 / Gate 5) is strictly forbidden until **all Phase Dossiers for all modules across the project** have been created in `docs/plans/active/`, all registered UI prototypes in `docs/prototypes/registry.md` are `APPROVED`, verified via `python scripts/validate_plans.py --fix` (`0 violations`), and approved by the Human Architect.

---

### Step 6 (`/ntc-run` / `"Tiếp tục"` — Gate 5): Atomic Implementation & State Machine
1. **Single Atomic Task Turn (`1 Turn = 1 Task`):** In any single turn (triggered via `/ntc-run` or `"tiếp tục"`), the Agent executes **EXACTLY ONE ATOMIC TASK**.
2. **Single-Module Scope:** The task modifies only its module's `Code Root` and its active dossier in `docs/plans/active/<module-slug>/`.
3. **1:1 UI Prototype Parity Invariant (For UI Tasks):** Whenever an Atomic Task specifies a `UI Prototype Reference` (`SCR-<MOD>-<NN>`), the Agent **MUST** read the approved HTML prototype file (`docs/prototypes/<module-slug>/scr-<nn>-*.html`) and `docs/prototypes/registry.md` in that turn. The Agent must port the exact DOM hierarchy, CSS/Tailwind classes, visual tokens, interactive states (`default`, `loading`, `empty`, `error`), and `data-testid` attributes **1:1** into the framework component. Inventing unapproved layouts or dropping `data-testid` hooks is a protocol violation.
4. **Executable Proof Invariant:** Every atomic task must be validated with real executable evidence (unit tests pass, component `data-testid` assertions pass, build succeeds, contract checks pass) before checking off `- [x]`.
5. **Atomic Git Commit Checkpointing (Clean Rollback Point per Task):** At the end of every Atomic Task turn in Step 6 — strictly AFTER the `Executable Proof Command` passes, `- [x]` is checked off, the `🎫 Resume Ticket` is updated, and `python scripts/validate_plans.py --fix` succeeds — the Agent **MUST** stage the module's changes and create an atomic git commit:
   ```bash
   git add <code-root> docs/plans/ docs/modules-spec/
   git commit -m "feat(<slug>): complete <MOD>-P<NN>.<M>.<A> - <short task summary>"
   ```
   The resulting commit hash is recorded in Section 4 (`Execution Evidence & Verification Log`) of the active Phase Dossier. Because every completed `[x]` task is committed to `HEAD`, any uncommitted diff in `git status` / `git diff HEAD` belongs exclusively to an interrupted in-flight task.
6. **Cross-Module Integration & Full-Stack E2E Gate (`SYS` Closing Phase — `/ntc-status --e2e`):**
   - The reserved `SYS` (`system`) module acts as a **two-sided bookend**:
     - **Opening Bookend (`SYS-P01` in `GP-01`):** Scaffolds shared infrastructure, local orchestration (`docker-compose.yml` / dev stack), and codifies shared contracts (`CT-*` → `AVAILABLE`).
     - **Closing Bookend (`SYS-P<FINAL>` in `GP-<FINAL>`):** Executes ONLY after all domain and UI module phases are archived in `docs/plans/completed/<slug>/`. It boots the live integrated stack (DB + Backend Services + API Gateway + Frontend), verifies live cross-module contract (`CT-*`) round-trips without mocks, and runs end-to-end (E2E) user journeys (using Playwright/Cypress or integration runners) that target the exact **`data-testid="scr-<nn>-..."` anchors** locked in `docs/prototypes/registry.md` from UI interaction → API call → DB state mutation → UI state update.
7. **The `/ntc-run` & `"Tiếp tục"` (Continue) State Machine:**
   - **Within an Active Phase (`IN_PROGRESS`):** When the user enters `/ntc-run` (or `"tiếp tục"`, `"continue"`, `/ntc-run --module <MOD>`, `"tiếp tục <MOD>"`), the Agent checks the `🎫 Resume Ticket`, performs the **3-Step Crash / Dirty-State Reconciliation** (Section 4.2), and executes the **next sequential unchecked `- [ ]` Atomic Task** in the current Phase Dossier.
   - **Completing the Final Atomic Task of a Phase:** In the turn where the last unchecked Atomic Task of `<MOD>-P<NN>` passes verification:
     1. The Agent marks `- [x]` on that final task.
     2. Updates the `🎫 Resume Ticket` to `Lifecycle Status: PHASE_COMPLETED` with `Immediate Next Atomic Action: Awaiting explicit user command "/ntc-run --phase <MOD>-P<NN+1>" or "tiếp tục phase <MOD>-P<NN+1>" to archive <MOD>-P<NN> and start <MOD>-P<NN+1>.`
     3. Announces clearly: *"Đã hoàn thành toàn bộ Atomic Tasks của Phase `<MOD>-P<NN>`. Vui lòng nhập `/ntc-run --phase <MOD>-P<NN+1>` (hoặc `tiếp tục phase <MOD>-P<NN+1>`) để lưu trữ phase hiện tại và chuyển sang phase kế tiếp."*
   - **Phase Boundary Hard Stop:** If a phase is at `PHASE_COMPLETED` (zero `- [ ]` tasks remaining) and the user types plain `/ntc-run` or `"tiếp tục"`, the Agent **MUST NOT** start the next phase. It must stop and remind the user: *"Phase `<MOD>-P<NN>` đã hết Atomic Task. Vui lòng nhập rõ lệnh `/ntc-run --phase <MOD>-P<NN+1>` hoặc `tiếp tục phase <MOD>-P<NN+1>` để chuyển phase."*
   - **Phase Transition Command (`/ntc-run --phase <MOD>-P<NN+1>` or `"tiếp tục phase <MOD>-P<NN+1>"`):** When the user explicitly enters `/ntc-run --phase <MOD>-P<NN+1>` or `"tiếp tục phase <MOD>-P<NN+1>"` (or `"tiếp tục phase <NN+1>"`), in that single turn the Agent automatically:
     1. Moves `docs/plans/active/<module-slug>/phase-<NN>-<slug>.md` to `docs/plans/completed/<module-slug>/phase-<NN>-<slug>.md`.
     2. Activates `docs/plans/active/<module-slug>/phase-<NN+1>-<slug>.md` (`Lifecycle Status: IN_PROGRESS`) and runs `python scripts/validate_plans.py --fix` to synchronize `docs/modules-spec/<module-slug>.md` and `docs/plans/system-roadmap.md`.
     3. Sanity-checks `<MOD>-P<NN+1>` against the completed code of `<MOD>-P<NN>` and **immediately executes the first Atomic Task (`<MOD>-P<NN+1>.1.1`)** of `<MOD>-P<NN+1>`, updating its `🎫 Resume Ticket` and committing at the end of the turn.

---

## 2. Plugin Slash Commands (`/ntc-*`) Quick Reference

| Step | Slash Command | Supported Flags / Arguments | When to Use |
| :--- | :--- | :--- | :--- |
| **Step 1** | **`/ntc-init`** | `--repo <git-url>`<br>`--idea "<summary>"`<br>`--no-ui` | At project start: asks for Git repo URL (optional), initializes git & remote `origin`, asks clarifying questions, and generates `PRD.md` + `ARCHITECTURE.md`. |
| **Step 2** | **`/ntc-prototype`** | `--screen <SCR-ID>`<br>`--revise "<feedback>"`<br>`--approve` | After `PRD.md` & `ARCHITECTURE.md` are ready (if `UI Required: YES`): generates/updates interactive HTML prototypes in `docs/prototypes/` until locked with `--approve`. |
| **Step 3** | **`/ntc-spec`** | `--skills-from "<url>"`<br>`--approve` | After UI prototypes are approved: generates overall `SPEC.md` + `system-roadmap.md` + `contract-registry.md`, then maps & installs module AI skills into `ai-skill-maps.md`. |
| **Step 4** | **`/ntc-modules`** | `--module <MOD>`<br>`--approve` | After `SPEC.md` & `ai-skill-maps.md` are locked: reads module skills + `SPEC.md` + prototypes to generate detailed `docs/modules-spec/<slug>.md` for every module & `STEP-by-STEP.md`. |
| **Step 5** | **`/ntc-plan`** | `--module <MOD>`<br>`--verify` | After `docs/modules-spec/*.md` are approved (Gate 4): pre-generates 100% of Phase Dossiers (`docs/plans/active/<slug>/phase-*.md`) with Level-4 Atomic WBS. |
| **Step 6** | **`/ntc-run`** | `--module <MOD>`<br>`--phase <MOD>-P<NN>` | During Gate 5 implementation (equivalent to `"tiếp tục"`): runs 3-Step Crash Recovery, executes 1 Atomic Task with 1:1 UI parity, tests, updates ticket, and creates an Atomic Git Commit. |
| **Delta CR** | **`/ntc-cr`** | `"<change description>"`<br>`--approve-delta` | Anytime during Step 5/6 when adding/modifying features, contracts (`CT-*`), or screens (`SCR-*`): runs the 4-Step Delta Reverse-Unlock Protocol (`CR-<NN>`). |
| **Verify & E2E** | **`/ntc-status`** | `--fix`<br>`--e2e` | Anytime to run `python scripts/validate_plans.py --fix` and view progress, or `--e2e` to trigger the closing `SYS-P<FINAL>` Full-Stack E2E phase. |

---

## 3. Identifier Convention

| Level | Format | Example | Authoritative File |
| :--- | :--- | :--- | :--- |
| Global Phase (project) | `GP-<NN>` | `GP-01` | `docs/plans/system-roadmap.md` |
| Module | `<MOD>` (2-5 uppercase) + `<slug>` | `AUTH` / `auth` | `docs/modules-spec/auth.md` |
| Module Phase | `<MOD>-P<NN>` ↔ `phase-<NN>-<slug>.md` | `AUTH-P01` | `docs/plans/active/auth/phase-01-*.md` |
| Major Task | `<MOD>-P<NN>.<M>` | `AUTH-P01.2` | `docs/plans/active/auth/phase-01-*.md` |
| Atomic Task | `<MOD>-P<NN>.<M>.<A>` | `AUTH-P01.2.3` | `docs/plans/active/auth/phase-01-*.md` |
| Dynamic Sub-Task (Hotfix) | `<MOD>-P<NN>.<M>.<A>[a-z]` | `AUTH-P01.2.3a` | `docs/plans/active/auth/phase-01-*.md` |
| Contract | `CT-<PROVIDER>-<NN>` | `CT-AUTH-01` | `docs/plans/contract-registry.md` |
| UI Screen Prototype | `SCR-<MOD>-<NN>` | `SCR-WEB-01` | `docs/prototypes/registry.md` |
| Mid-Flight Change Request | `CR-<NN>` | `CR-01` | `docs/plans/system-roadmap.md` (`## 6. Change Request (CR) Log`) |

Module codes and slugs are assigned once in the Module Registry and never reused. The pseudo-module `system` / `SYS` is reserved for cross-cutting work.

---

## 4. Cross-Module Contract & UI Prototype Protocol

### 4.1 API / Event / Schema Contracts (`CT-<PROVIDER>-<NN>`)
1. **Register (Step 3 — `/ntc-spec`):** Add the contract to `docs/plans/contract-registry.md` with ID (`CT-<PROVIDER>-<NN>`), type (`REST` | `gRPC` | `Event` | `Schema` | `Library`), provider, consumers, spec path, semantic version, and status `DRAFT`.
2. **Codify (Step 6 — `GP-01` / `SYS-P01`):** An atomic task writes the machine-readable spec at the declared path (OpenAPI, Protobuf, JSON Schema, AsyncAPI, typed DTO package). Once the file exists and validates, status becomes `AVAILABLE`.
3. **Consume:** Providers and consumers implement against the codified spec only. Consumers may use contract-derived test doubles to develop in parallel; they must never import another module's internals, query its storage, or read its source.
4. **Change Control:** Any change bumps the version and adds a Change Log entry listing impacted consumers. A breaking change requires explicit Human Architect approval and a decision record (`docs/templates/decision.md`) before implementation.
5. **Deprecate:** A contract becomes `DEPRECATED` only after all listed consumers have migrated.

### 4.2 UI Prototype Contracts & 1:1 Visual Parity (`SCR-<MOD>-<NN>`)
1. **Register & Build (Step 2 — `/ntc-prototype`):** For projects with user interfaces (`UI Required: YES`), every screen is derived from `PRD.md` & `ARCHITECTURE.md`, registered in `docs/prototypes/registry.md` (`SCR-<MOD>-<NN>`), and built as a self-contained HTML/CSS prototype at `docs/prototypes/<module-slug>/scr-<nn>-<slug>.html` with status `DRAFT`.
2. **Anchor with `data-testid` & States:** Every HTML prototype must define explicit `data-testid="scr-<nn>-<element>"` attributes on key containers, forms, inputs, buttons, and tables, and demonstrate `default`, `loading`, `empty`, and `error` states.
3. **Sign-Off Before Overall SPEC & Module Specs:** The Human Architect previews, iterates (`--revise`), and approves (`--approve`) each prototype in Step 2. Once approved, status in `docs/prototypes/registry.md` becomes `APPROVED`. `scripts/validate_plans.py` blocks Step 5/6 if any screen for a module with Phase Dossiers remains `DRAFT` or lacks `data-testid` hooks.
4. **1:1 Porting in Step 6 (`/ntc-run`):** During Step 6, any Atomic Task linked to `SCR-<MOD>-<NN>` must read the HTML file and port its DOM structure, design tokens, CSS/Tailwind classes, and `data-testid` attributes **1:1** into the production component, verified by component tests in Task `.3`.

---

## 5. Zero-Context Resume & Crash Recovery Protocol

### 5.1 Multi-Module & Multi-Agent Resume
When resuming work in a fresh session (or across parallel agent tabs / Git Worktrees), the Human Architect inputs `/ntc-run`, `"tiếp tục"`, `"Continue"`, or `"Đang làm đến đâu rồi"` — optionally followed by a module code (e.g. `/ntc-run --module AUTH` or `"tiếp tục AUTH"`):
1. Read **Active Work Pointer** in `docs/plans/system-roadmap.md`.
2. Select the target module's active phase dossier in `docs/plans/active/<module-slug>/` (choosing the dossier with `Lifecycle Status: IN_PROGRESS` or `PHASE_COMPLETED`, or the lowest-numbered `phase-<NN>-*.md` if starting).
3. Activate the mandatory skills for that module from `ai-skill-maps.md`.

### 5.2 Atomic Git Commit Checkpointing & 3-Step Crash Reconciliation
Because every verified `[x]` Atomic Task is immediately committed to Git (`HEAD`) at the end of its turn, `HEAD` is always a known-good, test-passing checkpoint. If the IDE, terminal, or power was lost **mid-turn** while an Atomic Task was being executed, any uncommitted modification in `git status` / `git diff HEAD` belongs **100% to that single interrupted Atomic Task**.

Before writing any code on `/ntc-run` or `"tiếp tục"`, the Agent MUST reconcile:

1. **Write-Ahead Ticket Update:** At the very start of every Atomic Task turn, before touching any source file, update the `🎫 Resume Ticket` to `Lifecycle Status: IN_PROGRESS` and set `Active Atomic Task` to the task being started.
2. **Working Tree & `HEAD` Inspection (`git status --short` & `git diff HEAD`):** When resuming via `/ntc-run` or `"tiếp tục"`, inspect the first unchecked `- [ ]` Atomic Task's `Target Files` and run `git status --short` / `git diff HEAD` scoped to the module's `Code Root`.
3. **Deterministic Recovery Action:**
   - **Clean State (No uncommitted edits in Target Files relative to `HEAD`):** The task has not started. Execute the task from scratch, then commit at the end of the turn.
   - **Completed-Before-Crash State (Target Files already implemented before crash):** Run the task's `Executable Proof Command`. If all tests and acceptance criteria **PASS**, mark `- [x]` on that task, create the missing atomic git commit (`git commit -m "feat(<slug>): complete <MOD>-P<NN>.<M>.<A> (recovered)"`), log the recovery in Section 4 of the dossier, and immediately execute the next sequential Atomic Task in the same turn.
   - **Partially-Written / Interrupted State (Target Files modified mid-edit or failing tests):** Report the exact state in 3 lines (*Module/Phase/Task, interrupted file & line/failure relative to `HEAD`, and recovery action*), then complete the remaining logic of that exact Atomic Task without duplicating valid work (or restore a corrupted file from `HEAD` via `git checkout HEAD -- <file>` if needed), verify tests pass, and create the atomic git commit.

---

## 6. Multi-Agent, Git Worktree & Cross-Module E2E Integration

### 6.1 Parallel Module Execution (Mode A & Mode B)
Once foundational contracts (`SYS` / `GP-01`) are `AVAILABLE`, multiple AI agents can execute different modules in parallel using two supported modes:

1. **Mode A — Parallel Tabs / Subagents in Shared Workspace:**
   - Each agent is assigned a distinct module code (`<MOD>`) and is strictly confined to `<MOD>`'s `Code Root` and `docs/plans/active/<module-slug>/`.
   - Because each module owns its own `docs/modules-spec/<module-slug>.md` and `docs/plans/active/<module-slug>/` directory, parallel agents never conflict on dossier files.
2. **Mode B — Isolated Git Worktrees (Recommended for Heavy Parallel Builds):**
   - Each agent creates an isolated worktree (`git worktree add ../<project>-<slug> -b feat/<slug> main`).
   - All Step 6 atomic turns, builds, unit tests, and per-task atomic git commits run inside the worktree.
   - Upon completing all phases of `<MOD>`, the agent runs the full module test suite and `python scripts/validate_plans.py --fix`, merges `feat/<slug>` back into `main`, and removes the worktree.

### 6.2 Closing `SYS` Cross-Module Integration & Full-Stack E2E Gate (`GP-<FINAL>` / `/ntc-status --e2e`)
While individual modules (`AUTH`, `ORD`, `WEB`, ...) test their logic in isolation during `GP-02` / `GP-03`, the system is NOT complete until the closing **`SYS` Integration & E2E Phase** (`SYS-P<FINAL>`) passes:
1. **Entry Pre-Condition:** All domain and frontend module phases listed in earlier Global Phases must be archived in `docs/plans/completed/<module-slug>/`.
2. **Live Topology Boot:** `SYS-P<FINAL>` boots the full multi-service / modular-monolith topology (real database instances + migrations, Redis/message brokers, backend services, API gateway, and compiled frontend app).
3. **Live Cross-Module Contract Verification:** Executes real HTTP/gRPC/Event contract integration tests across services (`CT-*`) with zero mocks.
4. **Full-Stack E2E Browser Verification (Frontend ↔ Backend ↔ DB):** When `UI Required: YES`, executes automated E2E tests (e.g., Playwright) driving the real UI via the locked **`data-testid="scr-<nn>-..."` attributes** from `docs/prototypes/registry.md`, asserting that user actions trigger real backend API calls (`CT-*`), persist in the database, and render the approved UI states (`default`, `loading`, `empty`, `error`).

---

## 7. Mid-Flight Change Request & Scope Evolution Protocol (`/ntc-cr` / `CR-<NN>`)

When the project is already in Step 5 (Gate 4) or Step 6 (Gate 5) and a new requirement, edge case, or UI change arises, the Agent classifies it into one of two tiers:

| Tier | Trigger Condition | Identifier | Protocol |
| :--- | :--- | :--- | :--- |
| **Tier 1: In-Phase Dynamic Sub-Task (Hotfix)** | Local bug, missing validation, or edge case strictly within the current module's scope; **no** change to `CT-*` contracts or `SCR-*` UI screens. | `<MOD>-P<NN>.<M>.<A>[a-z]` (e.g., `AUTH-P01.2.2a`) | Insert the sub-task directly into the current active dossier (`docs/plans/active/<slug>/phase-<NN>-*.md`), document the reason, execute it in 1 turn, verify, and commit. |
| **Tier 2: Mid-Flight Change Request (Scope Evolution)** | User requests a new feature, new/modified UI screen (`SCR-*`), new/updated cross-module contract (`CT-*`), or a change spanning multiple modules via `/ntc-cr "<mô tả>"` or `"yêu cầu thay đổi: <mô tả>"`. | `CR-<NN>` (e.g., `CR-01`) | Execute the **4-Step Delta Reverse-Unlock Protocol** below. **NEVER** uncheck completed `[x]` tasks or edit archived files in `docs/plans/completed/`. |

### The 4-Step Delta Reverse-Unlock Protocol (`CR-<NN>`)
When the Human Architect invokes `/ntc-cr "<nội dung>"` or enters `"yêu cầu thay đổi: <nội dung>"` (or `"change request: <description>"`):
1. **Step 1 — Freeze & Register `CR-<NN>` Impact Audit:**
   - Pause Step 6 code execution and register a new row `CR-<NN>` in `docs/plans/system-roadmap.md` (`## 6. Change Request (CR) Log`) with status `IN_REVIEW`.
   - Identify the exact **Delta Blast Radius**: which `PRD.md` / `SPEC.md` sections, `CT-*` contracts, `SCR-*` UI prototypes, `docs/modules-spec/<slug>.md` files, and modules are impacted.
2. **Step 2 — Delta Step 2 & Step 3 (UI Prototypes & Contracts First):**
   - **If UI changes (`SCR-*`):** Create or update ONLY the affected HTML prototype files in `docs/prototypes/<module-slug>/scr-<nn>-*.html` (preserving/adding `data-testid` hooks), log `CR-<NN>` in `docs/prototypes/registry.md`, and **STOP for Human Architect visual approval (`APPROVED`)**.
   - **If Cross-Module Contracts change (`CT-*`):** Register the new `CT-*` or bump the semantic version of the existing `CT-*` in `docs/plans/contract-registry.md` and log `CR-<NN>` in the Contract Change Log.
3. **Step 3 — Delta Step 4 & Step 5 (Append-Only Spec & Dossier Amendment):**
   - Update `SPEC.md` and the affected `docs/modules-spec/<slug>.md` files to reflect the approved delta (and update `ai-skill-maps.md` if a new technology skill is required).
   - Update Phase Dossiers **without touching completed history**:
     - *Case A (Module still has an `IN_PROGRESS` or `PENDING` dossier in `docs/plans/active/<slug>/`):* Append new Major/Atomic Tasks (`<MOD>-P<NN>.<M>.1..3` tagged with `[CR-<NN>]`) to the appropriate active dossier.
     - *Case B (All previous phases of the module are already in `docs/plans/completed/<slug>/`):* Append a new **Delta Phase (`<MOD>-P<NN+1>`)** to `docs/modules-spec/<slug>.md` (`## 9. Module Phase Sequence`) and generate a new dossier `docs/plans/active/<slug>/phase-<NN+1>-cr-<nn>-<slug>.md`.
4. **Step 4 — Validate, Commit Delta Plan & Resume Step 6:**
   - Mark `CR-<NN>` as `APPROVED` in `docs/plans/system-roadmap.md`, run `python scripts/validate_plans.py --fix`, commit the planning delta (`git commit -m "chore(plan): apply CR-<NN> delta specs and WBS"`), and resume Step 6 execution via `/ntc-run` or `"tiếp tục"`.

---

## 8. Structural Validation & Auto-Synchronization (`/ntc-status` / `scripts/validate_plans.py`)

Run the cross-platform Python validator after any planning change, phase transition, or archival step:

```bash
# Validate structure, IDs, contracts, UI prototypes, specs, and dossiers
python scripts/validate_plans.py

# Automatically synchronize Module Phase Sequence tables and Active Work Pointer from disk
python scripts/validate_plans.py --fix
```
