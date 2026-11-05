# Repository Workflow: Atomic Engineering Protocol (Microservices Edition v2.0)

Repository product behavior, architecture, detailed module specifications, skill maps, plans, code, tests, and runtime signals are the single system of record.

Planning and specifications are layered so each document stays small enough to protect the agent's context window:

```text
SPEC.md (Supreme System Specification)
 ├─ docs/plans/system-roadmap.md                  Project Roadmap (Global Phases, Module Registry, Active Work Pointer)
 ├─ docs/plans/contract-registry.md               Cross-module contracts (REST / gRPC / Event / Schema / Library)
 ├─ docs/prototypes/registry.md                   UI Prototype & Design System Registry (SCR-<MOD>-<NN>, if UI Required)
 │   └─ docs/prototypes/<module-slug>/scr-*.html  Self-contained interactive HTML/CSS prototypes with data-testid hooks
 ├─ docs/modules-spec/<module-slug>.md            Detailed Module SPEC + UI Screen Mapping + Module Phase Sequence (<MOD>-P<NN>)
 ├─ ai-skill-maps.md                              AI Skill Mapping Playbook (.agents/skills/<skill>/SKILL.md)
 ├─ STEP-by-STEP.md                               Human-Only Execution Playbook (Agents DO NOT read this file)
 └─ docs/plans/active/<module-slug>/
     ├─ phase-01-<slug>.md                        Pre-generated Phase Dossier (with real-time 🎫 Resume Ticket)
     ├─ phase-02-<slug>.md                        Pre-generated Phase Dossier (PENDING until phase-01 completes)
     └─ ...
         └─ Major Task  →  Atomic Task (1 Turn = 1 Task + 1:1 UI Prototype Parity)
             (verified & phase transition)  →  docs/plans/completed/<module-slug>/phase-<NN>-<slug>.md
```

---

## 1. The 5-Stage Operating Standard

Every complex project, multi-service system, or enterprise feature must strictly adhere to the following 5-stage gated lifecycle.

### Gate 1: Root Specification Ingestion (`SPEC.md`)
1. The Human Architect drafts `SPEC.md` (using `docs/templates/spec-template.md`) at the repository root.
2. The Human Architect instructs the Agent: *"Read `SPEC.md` and `AGENTS.md`"*.
3. The Agent analyzes system architecture, proposes **candidate modules (services)** with clear responsibilities and data ownership (`SYS` / `system` reserved for cross-cutting work), confirms whether the system includes user-facing UI modules (`UI Required: YES | NO`), identifies technical risks, and asks clarifying questions.
4. **Non-Negotiable Boundary:** **WRITING PRODUCTION CODE AT THIS STAGE IS STRICTLY FORBIDDEN.**

### Gate 2: Project Roadmap & Contract Registry Alignment
1. The Agent and Human Architect collaboratively construct:
   - `docs/plans/system-roadmap.md` (from `docs/templates/system-roadmap-template.md`): architecture blueprint, **Module Registry** (Code, Slug, Responsibility, Code Root, `docs/modules-spec/<slug>.md`, Depends On, Status), **Global Phases** (`GP-<NN>`), **Module Dependency Graph**, and **Active Work Pointer**.
   - `docs/plans/contract-registry.md` (from `docs/templates/contract-registry-template.md`): every known inter-module contract, initially `DRAFT`.
2. Cross-cutting work (shared contract packages, local orchestration, CI, gateway if not its own service, end-to-end tests) is owned by the reserved pseudo-module **`system` (code `SYS`)**.
3. **Approval Gate (Gate 2):** The Human Architect reviews and approves before advancing to Gate 3.

### Gate 3: UI Prototypes (if UI), Detailed Module SPECs, `ai-skill-maps.md`, and `STEP-by-STEP.md`
Gate 3 executes in **four sequential sub-steps** (`Step 3.0` is conditional on whether the project has a UI):

#### Step 3.0 (Conditional): Interactive UI Prototyping & Visual Sign-Off (`docs/prototypes/`)
1. **Headless / Backend-Only Systems (`UI Required: NO`):** The Agent sets `> **UI Required:** NO` in `docs/prototypes/registry.md`, leaves its screen table at the default placeholder row, and proceeds immediately to **Step 3.1**.
2. **Systems with UI / Frontend Modules (`UI Required: YES`):** Before authoring any `docs/modules-spec/*.md` file, the Agent:
   - Populates **`docs/prototypes/registry.md`** (from `docs/templates/ui-prototype-registry-template.md`) with locked **Design System Tokens** (exact color variables, typography, spacing, layout shell) and the **UI Screen & Prototype Registry (`SCR-<MOD>-<NN>`)**.
   - Generates self-contained, clickable HTML/CSS prototypes at **`docs/prototypes/<module-slug>/scr-<nn>-<slug>.html`** that the Human Architect can open directly in a browser.
   - Each HTML prototype **MUST** include:
     - All required visual states (`default`, `loading`, `empty`, `error`, plus key modals/drawers).
     - Explicit **`data-testid="scr-<nn>-<element>"`** attributes on the root container, forms, inputs, buttons, and data tables/lists.
     - Realistic sample data that exposes every field needed from backend contracts (`CT-*`).
3. **Human Visual Sign-Off Gate (Hard Stop):** The Agent **MUST STOP** and ask the Human Architect to preview the HTML files in `docs/prototypes/<module-slug>/`, iterate on layout/UX as requested, and mark every screen in `docs/prototypes/registry.md` as **`APPROVED`**. The Agent must NOT advance to Step 3.1 while any active screen is still `DRAFT`. *(Self-contained HTML prototypes inside `docs/prototypes/` are the only code permitted prior to Gate 5).*

#### Step 3.1: Author ALL Detailed Module Specifications (`docs/modules-spec/<module-slug>.md`)
1. From `SPEC.md`, `docs/plans/system-roadmap.md`, and the approved `docs/prototypes/registry.md`, the Agent instantiates `docs/modules-spec/<module-slug>.md` (using `docs/templates/module-spec-template.md`) for **every registered module** in the project (including `system.md`).
2. Each `docs/modules-spec/<module-slug>.md` replaces legacy module blueprints and must contain:
   - Traceability to `SPEC.md` & Scope Boundaries (In-Scope / Out-of-Scope).
   - User Stories (*"As a [Role], I want [Action], so that [Benefit]"*).
   - Tech Stack, Runtime & Build/Test Commands.
   - Exact Domain Data Models & Storage Schema (DDL tables, indexes, partitioning, Redis keys).
   - Provided & Consumed Contracts (`CT-<MOD>-<NN>`), Events, payload validation rules, and **UI Screen & Prototype Mappings (`SCR-<MOD>-<NN>`)** for UI modules.
   - Core Business Flows (sequence diagrams), State Machine tables, and Edge Cases.
   - Stage-by-Stage Acceptance Criteria (**Given / When / Then**).
   - Non-Functional Requirements (NFRs) & Error Codes.
   - **Module Phase Sequence Table (`<MOD>-P<NN>`)** aligned to Global Phases.
3. To prevent output truncation, the Agent may generate one `docs/modules-spec/<module-slug>.md` per turn, continuing until **100% of registered modules** have complete specifications.

#### Step 3.2: Interactive Skill Discovery & `ai-skill-maps.md` Creation
1. Immediately after all `docs/modules-spec/*.md` files are complete, the Agent **MUST STOP and ask the Human Architect** to provide website URLs or skill catalogs to search for AI skills/plugins (for example: `https://skillsmp.com/search`, `https://felo.ai/vi/skills`, GitHub repositories, or local skill packs).
2. The Agent searches those sources against the tech stack and domain rules in `SPEC.md` and `docs/modules-spec/*.md`, then presents a **Proposed AI Skill Table** (combining discovered skills with custom project skills such as `atomic-harness-gatekeeper`, `<project>-domain-invariants`, and `ui-prototype-fidelity` for UI modules) for the Human Architect to review.
3. **User Approval Gate:** Only after the Human Architect reviews and confirms the final skill list does the Agent install the skills into `.agents/skills/<skill-name>/SKILL.md` and create **`ai-skill-maps.md`** (from `docs/templates/ai-skill-maps-template.md`).

#### Step 3.3: Generate the Human Execution Playbook (`STEP-by-STEP.md`)
1. Once `docs/modules-spec/*.md` and `ai-skill-maps.md` are finalized, the Agent generates **`STEP-by-STEP.md`** at the repository root (from `docs/templates/step-by-step-template.md`).
2. `STEP-by-STEP.md` packages the module dependency order and ready-to-copy prompt blocks (for both standard single-workspace tabs and isolated **Git Worktree** multi-agent workflows) that explicitly reference `ai-skill-maps.md`, `docs/prototypes/registry.md`, and `docs/modules-spec/<slug>.md`.
3. **Human-Only Rule:** `STEP-by-STEP.md` is strictly an operator guide for the Human Architect to follow the harness workflow. **AI Agents MUST NOT read `STEP-by-STEP.md` during subsequent execution.**

### Gate 4: Pre-Generate ALL Phase Dossiers & WBS (Project-Wide)
1. Guided by the user's prompts (copied from `STEP-by-STEP.md`), the Agent reads `ai-skill-maps.md` (and the corresponding `.agents/skills/*/SKILL.md` files), `docs/prototypes/registry.md`, and `docs/modules-spec/<module-slug>.md`.
2. The Agent instantiates **ALL Phase Dossiers** (`docs/plans/active/<module-slug>/phase-<NN>-<slug>.md` from `docs/templates/phase-dossier-template.md`) for **every planned phase of every module in the entire project**.
3. Each Phase Dossier decomposes its work into **Major Tasks (`<MOD>-P<NN>.<M>`)** and **Level-4 Atomic Micro-Tasks (`<MOD>-P<NN>.<M>.<A>`)**:
   - Task `<M>.1`: Interface / Type / Schema / Contract Definition (Contract-First).
   - Task `<M>.2`: Core business logic or UI component implementation (with explicit `UI Prototype Reference: SCR-<MOD>-<NN>` pointing to `docs/prototypes/<module-slug>/scr-<nn>-*.html` for UI tasks).
   - Task `<M>.3`: Unit / Component tests & executable verification proof (asserting `data-testid` parity for UI tasks).
4. For each module, the first phase (`<MOD>-P01`) is initialized with `Lifecycle Status: READY_TO_EXECUTE` (or `IN_PROGRESS` when activated), while subsequent phases (`<MOD>-P02`, `<MOD>-P03`...) sit in `docs/plans/active/<module-slug>/` with `Lifecycle Status: PENDING`.
5. **Gate 4 Exit Lock:** Writing production code (Gate 5) is strictly forbidden until **all Phase Dossiers for all modules across the project** have been created in `docs/plans/active/`, all registered UI prototypes in `docs/prototypes/registry.md` are `APPROVED`, verified via `python scripts/validate_plans.py --fix`, and approved by the Human Architect.

### Gate 5: Atomic Implementation & The `"Tiếp tục"` State Machine
1. **Single Atomic Task Turn (`1 Turn = 1 Task`):** In any single turn, the Agent executes **EXACTLY ONE ATOMIC TASK**.
2. **Single-Module Scope:** The task modifies only its module's `Code Root` and its active dossier in `docs/plans/active/<module-slug>/`.
3. **1:1 UI Prototype Parity Invariant (For UI Tasks):** Whenever an Atomic Task specifies a `UI Prototype Reference` (`SCR-<MOD>-<NN>`), the Agent **MUST** read the approved HTML prototype file (`docs/prototypes/<module-slug>/scr-<nn>-*.html`) and `docs/prototypes/registry.md` in that turn. The Agent must port the exact DOM hierarchy, CSS/Tailwind classes, visual tokens, interactive states (`default`, `loading`, `empty`, `error`), and `data-testid` attributes **1:1** into the framework component. Inventing unapproved layouts or dropping `data-testid` hooks is a protocol violation.
4. **Executable Proof Invariant:** Every atomic task must be validated with real executable evidence (unit tests pass, component `data-testid` assertions pass, build succeeds, contract checks pass) before checking off `- [x]`.
5. **Atomic Git Commit Checkpointing (Clean Rollback Point per Task):** At the end of every Atomic Task turn in Gate 5 — strictly AFTER the `Executable Proof Command` passes, `- [x]` is checked off, the `🎫 Resume Ticket` is updated, and `python scripts/validate_plans.py --fix` succeeds — the Agent **MUST** stage the module's changes and create an atomic git commit:
   ```bash
   git add <code-root> docs/plans/ docs/modules-spec/
   git commit -m "feat(<slug>): complete <MOD>-P<NN>.<M>.<A> - <short task summary>"
   ```
   The resulting commit hash is recorded in Section 4 (`Execution Evidence & Verification Log`) of the active Phase Dossier. Because every completed `[x]` task is committed to `HEAD`, any uncommitted diff in `git status` / `git diff HEAD` belongs exclusively to an interrupted in-flight task.
6. **Cross-Module Integration & Full-Stack E2E Gate (`SYS` Closing Phase):**
   - The reserved `SYS` (`system`) module acts as a **two-sided bookend**:
     - **Opening Bookend (`SYS-P01` in `GP-01`):** Scaffolds shared infrastructure, local orchestration (`docker-compose.yml` / dev stack), and codifies shared contracts (`CT-*` → `AVAILABLE`).
     - **Closing Bookend (`SYS-P<FINAL>` in `GP-<FINAL>`):** Executes ONLY after all domain and UI module phases are archived in `docs/plans/completed/<slug>/`. It boots the live integrated stack (DB + Backend Services + API Gateway + Frontend), verifies live cross-module contract (`CT-*`) round-trips without mocks, and runs end-to-end (E2E) user journeys (using Playwright/Cypress or integration runners) that target the exact **`data-testid="scr-<nn>-..."` anchors** locked in `docs/prototypes/registry.md` from UI interaction → API call → DB state mutation → UI state update.
7. **The `"Tiếp tục"` (Continue) State Machine:**
   - **Within an Active Phase (`IN_PROGRESS`):** When the user enters `"tiếp tục"` (or `"continue"`, `"tiếp tục <MOD>"`), the Agent checks the `🎫 Resume Ticket`, performs the **3-Step Crash / Dirty-State Reconciliation** (Section 4.2), and executes the **next sequential unchecked `- [ ]` Atomic Task** in the current Phase Dossier.
   - **Completing the Final Atomic Task of a Phase:** In the turn where the last unchecked Atomic Task of `<MOD>-P<NN>` passes verification:
     1. The Agent marks `- [x]` on that final task.
     2. Updates the `🎫 Resume Ticket` to `Lifecycle Status: PHASE_COMPLETED` with `Immediate Next Atomic Action: Awaiting explicit user command "tiếp tục phase <MOD>-P<NN+1>" to archive <MOD>-P<NN> and start <MOD>-P<NN+1>.`
     3. Announces clearly: *"Đã hoàn thành toàn bộ Atomic Tasks của Phase `<MOD>-P<NN>`. Vui lòng nhập `tiếp tục phase <MOD>-P<NN+1>` để lưu trữ phase hiện tại và chuyển sang phase kế tiếp."*
   - **Phase Boundary Hard Stop:** If a phase is at `PHASE_COMPLETED` (zero `- [ ]` tasks remaining) and the user types plain `"tiếp tục"`, the Agent **MUST NOT** start the next phase. It must stop and remind the user: *"Phase `<MOD>-P<NN>` đã hết Atomic Task. Vui lòng nhập rõ lệnh `tiếp tục phase <MOD>-P<NN+1>` để chuyển phase."*
   - **Phase Transition Command (`"tiếp tục phase <MOD>-P<NN+1>"`):** When the user explicitly enters `"tiếp tục phase <MOD>-P<NN+1>"` (or `"tiếp tục phase <NN+1>"`), in that single turn the Agent automatically:
     1. Moves `docs/plans/active/<module-slug>/phase-<NN>-<slug>.md` to `docs/plans/completed/<module-slug>/phase-<NN>-<slug>.md`.
     2. Activates `docs/plans/active/<module-slug>/phase-<NN+1>-<slug>.md` (`Lifecycle Status: IN_PROGRESS`) and runs `python scripts/validate_plans.py --fix` to synchronize `docs/modules-spec/<module-slug>.md` and `docs/plans/system-roadmap.md`.
     3. Sanity-checks `<MOD>-P<NN+1>` against the completed code of `<MOD>-P<NN>` and **immediately executes the first Atomic Task (`<MOD>-P<NN+1>.1.1`)** of `<MOD>-P<NN+1>`, updating its `🎫 Resume Ticket` at the end of the turn.

---

## 2. Identifier Convention

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

## 3. Cross-Module Contract & UI Prototype Protocol

### 3.1 API / Event / Schema Contracts (`CT-<PROVIDER>-<NN>`)
1. **Register:** Add the contract to `docs/plans/contract-registry.md` with ID (`CT-<PROVIDER>-<NN>`), type (`REST` | `gRPC` | `Event` | `Schema` | `Library`), provider, consumers, spec path, semantic version, and status `DRAFT`.
2. **Codify:** An atomic task (typically in `GP-01` / `<MOD>-P01`) writes the machine-readable spec at the declared path (OpenAPI, Protobuf, JSON Schema, AsyncAPI, typed DTO package). Once the file exists and validates, status becomes `AVAILABLE`.
3. **Consume:** Providers and consumers implement against the codified spec only. Consumers may use contract-derived test doubles to develop in parallel; they must never import another module's internals, query its storage, or read its source.
4. **Change Control:** Any change bumps the version and adds a Change Log entry listing impacted consumers. A breaking change requires explicit Human Architect approval and a decision record (`docs/templates/decision.md`) before implementation.
5. **Deprecate:** A contract becomes `DEPRECATED` only after all listed consumers have migrated.

### 3.2 UI Prototype Contracts & 1:1 Visual Parity (`SCR-<MOD>-<NN>`)
1. **Register & Build (Gate 3 - Step 3.0):** For projects with user interfaces (`UI Required: YES`), every screen is registered in `docs/prototypes/registry.md` (`SCR-<MOD>-<NN>`) and built as a self-contained HTML/CSS prototype at `docs/prototypes/<module-slug>/scr-<nn>-<slug>.html` with status `DRAFT`.
2. **Anchor with `data-testid` & States:** Every HTML prototype must define explicit `data-testid="scr-<nn>-<element>"` attributes on key containers, forms, inputs, buttons, and tables, and demonstrate `default`, `loading`, `empty`, and `error` states.
3. **Sign-Off Before Spec & WBS:** The Human Architect previews and approves each prototype. Once approved, status in `docs/prototypes/registry.md` becomes `APPROVED`. `scripts/validate_plans.py` blocks Gate 4/5 if any screen for a module with Phase Dossiers remains `DRAFT` or lacks `data-testid` hooks.
4. **1:1 Porting in Gate 5:** During Gate 5, any Atomic Task linked to `SCR-<MOD>-<NN>` must read the HTML file and port its DOM structure, design tokens, CSS/Tailwind classes, and `data-testid` attributes **1:1** into the production component, verified by component tests in Task `.3`.

---

## 4. Zero-Context Resume & Crash Recovery Protocol

### 4.1 Multi-Module & Multi-Agent Resume
When resuming work in a fresh session (or across parallel agent tabs / Git Worktrees), the Human Architect inputs `"tiếp tục"`, `"Continue"`, `"Where were we?"`, or `"Đang làm đến đâu rồi"` — optionally followed by a module code (e.g. `"tiếp tục AUTH"`):
1. Read **Active Work Pointer** in `docs/plans/system-roadmap.md`.
2. Select the target module's active phase dossier in `docs/plans/active/<module-slug>/` (choosing the dossier with `Lifecycle Status: IN_PROGRESS` or `PHASE_COMPLETED`, or the lowest-numbered `phase-<NN>-*.md` if starting).
3. Activate the mandatory skills for that module from `ai-skill-maps.md`.

### 4.2 Atomic Git Commit Checkpointing & 3-Step Crash Reconciliation
Because every verified `[x]` Atomic Task is immediately committed to Git (`HEAD`) at the end of its turn, `HEAD` is always a known-good, test-passing checkpoint. If the IDE, terminal, or power was lost **mid-turn** while an Atomic Task was being executed, any uncommitted modification in `git status` / `git diff HEAD` belongs **100% to that single interrupted Atomic Task**.

Before writing any code on `"tiếp tục"`, the Agent MUST reconcile:

1. **Write-Ahead Ticket Update:** At the very start of every Atomic Task turn, before touching any source file, update the `🎫 Resume Ticket` to `Lifecycle Status: IN_PROGRESS` and set `Active Atomic Task` to the task being started.
2. **Working Tree & `HEAD` Inspection (`git status --short` & `git diff HEAD`):** When resuming via `"tiếp tục"`, inspect the first unchecked `- [ ]` Atomic Task's `Target Files` and run `git status --short` / `git diff HEAD` scoped to the module's `Code Root`.
3. **Deterministic Recovery Action:**
   - **Clean State (No uncommitted edits in Target Files relative to `HEAD`):** The task has not started. Execute the task from scratch, then commit at the end of the turn.
   - **Completed-Before-Crash State (Target Files already implemented before crash):** Run the task's `Executable Proof Command`. If all tests and acceptance criteria **PASS**, mark `- [x]` on that task, create the missing atomic git commit (`git commit -m "feat(<slug>): complete <MOD>-P<NN>.<M>.<A> (recovered)"`), log the recovery in Section 4 of the dossier, and immediately execute the next sequential Atomic Task in the same turn.
   - **Partially-Written / Interrupted State (Target Files modified mid-edit or failing tests):** Report the exact state in 3 lines (*Module/Phase/Task, interrupted file & line/failure relative to `HEAD`, and recovery action*), then complete the remaining logic of that exact Atomic Task without duplicating valid work (or restore a corrupted file from `HEAD` via `git checkout HEAD -- <file>` if needed), verify tests pass, and create the atomic git commit.

---

## 5. Multi-Agent, Git Worktree & Cross-Module E2E Integration

### 5.1 Parallel Module Execution (Mode A & Mode B)
Once foundational contracts (`SYS` / `GP-01`) are `AVAILABLE`, multiple AI agents can execute different modules in parallel using two supported modes:

1. **Mode A — Parallel Tabs / Subagents in Shared Workspace:**
   - Each agent is assigned a distinct module code (`<MOD>`) and is strictly confined to `<MOD>`'s `Code Root` and `docs/plans/active/<module-slug>/`.
   - Because each module owns its own `docs/modules-spec/<module-slug>.md` and `docs/plans/active/<module-slug>/` directory, parallel agents never conflict on dossier files.
2. **Mode B — Isolated Git Worktrees (Recommended for Heavy Parallel Builds):**
   - Each agent creates an isolated worktree (`git worktree add ../<project>-<slug> -b feat/<slug> main`).
   - All Gate 5 atomic turns, builds, unit tests, and per-task atomic git commits run inside the worktree.
   - Upon completing all phases of `<MOD>`, the agent runs the full module test suite and `python scripts/validate_plans.py --fix`, merges `feat/<slug>` back into `main`, and removes the worktree.

### 5.2 Closing `SYS` Cross-Module Integration & Full-Stack E2E Gate (`GP-<FINAL>`)
While individual modules (`AUTH`, `ORD`, `WEB`, ...) test their logic in isolation during `GP-02` / `GP-03`, the system is NOT complete until the closing **`SYS` Integration & E2E Phase** (`SYS-P<FINAL>`) passes:
1. **Entry Pre-Condition:** All domain and frontend module phases listed in earlier Global Phases must be archived in `docs/plans/completed/<module-slug>/`.
2. **Live Topology Boot:** `SYS-P<FINAL>` boots the full multi-service / modular-monolith topology (real database instances + migrations, Redis/message brokers, backend services, API gateway, and compiled frontend app).
3. **Live Cross-Module Contract Verification:** Executes real HTTP/gRPC/Event contract integration tests across services (`CT-*`) with zero mocks.
4. **Full-Stack E2E Browser Verification (Frontend ↔ Backend ↔ DB):** When `UI Required: YES`, executes automated E2E tests (e.g., Playwright) driving the real UI via the locked **`data-testid="scr-<nn>-..."` attributes** from `docs/prototypes/registry.md`, asserting that user actions trigger real backend API calls (`CT-*`), persist in the database, and render the approved UI states (`default`, `loading`, `empty`, `error`).

---

## 6. Mid-Flight Change Request & Scope Evolution Protocol (`CR-<NN>`)

When the project is already in Gate 4 or Gate 5 and a new requirement, edge case, or UI change arises, the Agent classifies it into one of two tiers:

| Tier | Trigger Condition | Identifier | Protocol |
| :--- | :--- | :--- | :--- |
| **Tier 1: In-Phase Dynamic Sub-Task (Hotfix)** | Local bug, missing validation, or edge case strictly within the current module's scope; **no** change to `CT-*` contracts or `SCR-*` UI screens. | `<MOD>-P<NN>.<M>.<A>[a-z]` (e.g., `AUTH-P01.2.2a`) | Insert the sub-task directly into the current active dossier (`docs/plans/active/<slug>/phase-<NN>-*.md`), document the reason, execute it in 1 turn, verify, and commit. |
| **Tier 2: Mid-Flight Change Request (Scope Evolution)** | User requests a new feature, new/modified UI screen (`SCR-*`), new/updated cross-module contract (`CT-*`), or a change spanning multiple modules via `"yêu cầu thay đổi: <mô tả>"` (`"change request: <description>"`). | `CR-<NN>` (e.g., `CR-01`) | Execute the **4-Step Delta Reverse-Unlock Protocol** below. **NEVER** uncheck completed `[x]` tasks or edit archived files in `docs/plans/completed/`. |

### The 4-Step Delta Reverse-Unlock Protocol (`CR-<NN>`)
When the Human Architect enters `"yêu cầu thay đổi: <nội dung>"` (or `"change request: <description>"`):
1. **Step 1 — Freeze & Register `CR-<NN>` Impact Audit:**
   - Pause Gate 5 code execution and register a new row `CR-<NN>` in `docs/plans/system-roadmap.md` (`## 6. Change Request (CR) Log`) with status `IN_REVIEW`.
   - Identify the exact **Delta Blast Radius**: which `SPEC.md` sections, `CT-*` contracts, `SCR-*` UI prototypes, `docs/modules-spec/<slug>.md` files, and modules are impacted.
2. **Step 2 — Delta Gate 2 & Gate 3.0 (Contracts & UI Prototypes First):**
   - **If UI changes (`SCR-*`):** Create or update ONLY the affected HTML prototype files in `docs/prototypes/<module-slug>/scr-<nn>-*.html` (preserving/adding `data-testid` hooks), log `CR-<NN>` in `docs/prototypes/registry.md`, and **STOP for Human Architect visual approval (`APPROVED`)**.
   - **If Cross-Module Contracts change (`CT-*`):** Register the new `CT-*` or bump the semantic version of the existing `CT-*` in `docs/plans/contract-registry.md` and log `CR-<NN>` in the Contract Change Log.
3. **Step 3 — Delta Gate 3.1 & Gate 4 (Append-Only Spec & Dossier Amendment):**
   - Update `SPEC.md` and the affected `docs/modules-spec/<slug>.md` files to reflect the approved delta.
   - Update Phase Dossiers **without touching completed history**:
     - *Case A (Module still has an `IN_PROGRESS` or `PENDING` dossier in `docs/plans/active/<slug>/`):* Append new Major/Atomic Tasks (`<MOD>-P<NN>.<M>.1..3` tagged with `[CR-<NN>]`) to the appropriate active dossier.
     - *Case B (All previous phases of the module are already in `docs/plans/completed/<slug>/`):* Append a new **Delta Phase (`<MOD>-P<NN+1>`)** to `docs/modules-spec/<slug>.md` (`## 9. Module Phase Sequence`) and generate a new dossier `docs/plans/active/<slug>/phase-<NN+1>-cr-<nn>-<slug>.md`.
4. **Step 4 — Validate, Commit Delta Plan & Resume Gate 5:**
   - Mark `CR-<NN>` as `APPROVED` in `docs/plans/system-roadmap.md`, run `python scripts/validate_plans.py --fix`, commit the planning delta (`git commit -m "chore(plan): apply CR-<NN> delta specs and WBS"`), and resume Gate 5 execution via `"tiếp tục"`.

---

## 7. Structural Validation & Auto-Synchronization (`scripts/validate_plans.py`)

Run the cross-platform Python validator after any planning change, phase transition, or archival step:

```bash
# Validate structure, IDs, contracts, specs, and dossiers
python scripts/validate_plans.py

# Automatically synchronize Module Phase Sequence tables and Active Work Pointer from disk
python scripts/validate_plans.py --fix
```
