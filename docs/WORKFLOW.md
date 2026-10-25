# Repository Workflow: Atomic Engineering Protocol (Microservices Edition v2.0)

Repository product behavior, architecture, detailed module specifications, skill maps, plans, code, tests, and runtime signals are the single system of record.

Planning and specifications are layered so each document stays small enough to protect the agent's context window:

```text
SPEC.md (Supreme System Specification)
 ├─ docs/plans/system-roadmap.md                  Project Roadmap (Global Phases, Module Registry, Active Work Pointer)
 ├─ docs/plans/contract-registry.md               Cross-module contracts (REST / gRPC / Event / Schema / Library)
 ├─ docs/modules-spec/<module-slug>.md            Detailed Module SPEC + Module Phase Sequence (<MOD>-P<NN>)
 ├─ ai-skill-maps.md                              AI Skill Mapping Playbook (.agents/skills/<skill>/SKILL.md)
 ├─ STEP-by-STEP.md                               Human-Only Execution Playbook (Agents DO NOT read this file)
 └─ docs/plans/active/<module-slug>/
     ├─ phase-01-<slug>.md                        Pre-generated Phase Dossier (with real-time 🎫 Resume Ticket)
     ├─ phase-02-<slug>.md                        Pre-generated Phase Dossier (PENDING until phase-01 completes)
     └─ ...
         └─ Major Task  →  Atomic Task (1 Turn = 1 Task)
             (verified & phase transition)  →  docs/plans/completed/<module-slug>/phase-<NN>-<slug>.md
```

---

## 1. The 5-Stage Operating Standard

Every complex project, multi-service system, or enterprise feature must strictly adhere to the following 5-stage gated lifecycle.

### Gate 1: Root Specification Ingestion (`SPEC.md`)
1. The Human Architect drafts `SPEC.md` (using `docs/templates/spec-template.md`) at the repository root.
2. The Human Architect instructs the Agent: *"Read `SPEC.md` and `AGENTS.md`"*.
3. The Agent analyzes system architecture, proposes **candidate modules (services)** with clear responsibilities and data ownership (`SYS` / `system` reserved for cross-cutting work), identifies technical risks, and asks clarifying questions.
4. **Non-Negotiable Boundary:** **WRITING PRODUCTION CODE AT THIS STAGE IS STRICTLY FORBIDDEN.**

### Gate 2: Project Roadmap & Contract Registry Alignment
1. The Agent and Human Architect collaboratively construct:
   - `docs/plans/system-roadmap.md` (from `docs/templates/system-roadmap-template.md`): architecture blueprint, **Module Registry** (Code, Slug, Responsibility, Code Root, `docs/modules-spec/<slug>.md`, Depends On, Status), **Global Phases** (`GP-<NN>`), **Module Dependency Graph**, and **Active Work Pointer**.
   - `docs/plans/contract-registry.md` (from `docs/templates/contract-registry-template.md`): every known inter-module contract, initially `DRAFT`.
2. Cross-cutting work (shared contract packages, local orchestration, CI, gateway if not its own service, end-to-end tests) is owned by the reserved pseudo-module **`system` (code `SYS`)**.
3. **Approval Gate (Gate 2):** The Human Architect reviews and approves before advancing to Gate 3.

### Gate 3: Detailed Module SPECs, `ai-skill-maps.md`, and `STEP-by-STEP.md`
Gate 3 executes in **three mandatory sub-steps**:

#### Step 3.1: Author ALL Detailed Module Specifications (`docs/modules-spec/<module-slug>.md`)
1. From `SPEC.md` and `docs/plans/system-roadmap.md`, the Agent instantiates `docs/modules-spec/<module-slug>.md` (using `docs/templates/module-spec-template.md`) for **every registered module** in the project (including `system.md`).
2. Each `docs/modules-spec/<module-slug>.md` replaces legacy module blueprints and must contain:
   - Traceability to `SPEC.md` & Scope Boundaries (In-Scope / Out-of-Scope).
   - User Stories (*"As a [Role], I want [Action], so that [Benefit]"*).
   - Tech Stack, Runtime & Build/Test Commands.
   - Exact Domain Data Models & Storage Schema (DDL tables, indexes, partitioning, Redis keys).
   - Provided & Consumed Contracts (`CT-<MOD>-<NN>`), Events, and payload validation rules.
   - Core Business Flows (sequence diagrams), State Machine tables, and Edge Cases.
   - Stage-by-Stage Acceptance Criteria (**Given / When / Then**).
   - Non-Functional Requirements (NFRs) & Error Codes.
   - **Module Phase Sequence Table (`<MOD>-P<NN>`)** aligned to Global Phases.
3. To prevent output truncation, the Agent may generate one `docs/modules-spec/<module-slug>.md` per turn, continuing until **100% of registered modules** have complete specifications.

#### Step 3.2: Interactive Skill Discovery & `ai-skill-maps.md` Creation
1. Immediately after all `docs/modules-spec/*.md` files are complete, the Agent **MUST STOP and ask the Human Architect** to provide website URLs or skill catalogs to search for AI skills/plugins (for example: `https://skillsmp.com/search`, `https://felo.ai/vi/skills`, GitHub repositories, or local skill packs).
2. The Agent searches those sources against the tech stack and domain rules in `SPEC.md` and `docs/modules-spec/*.md`, then presents a **Proposed AI Skill Table** (combining discovered skills with custom project skills such as `atomic-harness-gatekeeper` and `<project>-domain-invariants`) for the Human Architect to review.
3. **User Approval Gate:** Only after the Human Architect reviews and confirms the final skill list does the Agent install the skills into `.agents/skills/<skill-name>/SKILL.md` and create **`ai-skill-maps.md`** (from `docs/templates/ai-skill-maps-template.md`).

#### Step 3.3: Generate the Human Execution Playbook (`STEP-by-STEP.md`)
1. Once `docs/modules-spec/*.md` and `ai-skill-maps.md` are finalized, the Agent generates **`STEP-by-STEP.md`** at the repository root (from `docs/templates/step-by-step-template.md`).
2. `STEP-by-STEP.md` packages the module dependency order and ready-to-copy prompt blocks (for both standard single-workspace tabs and isolated **Git Worktree** multi-agent workflows) that explicitly reference `ai-skill-maps.md` and `docs/modules-spec/<slug>.md`.
3. **Human-Only Rule:** `STEP-by-STEP.md` is strictly an operator guide for the Human Architect to follow the harness workflow. **AI Agents MUST NOT read `STEP-by-STEP.md` during subsequent execution.**

### Gate 4: Pre-Generate ALL Phase Dossiers & WBS (Project-Wide)
1. Guided by the user's prompts (copied from `STEP-by-STEP.md`), the Agent reads `ai-skill-maps.md` (and the corresponding `.agents/skills/*/SKILL.md` files) plus `docs/modules-spec/<module-slug>.md`.
2. The Agent instantiates **ALL Phase Dossiers** (`docs/plans/active/<module-slug>/phase-<NN>-<slug>.md` from `docs/templates/phase-dossier-template.md`) for **every planned phase of every module in the entire project**.
3. Each Phase Dossier decomposes its work into **Major Tasks (`<MOD>-P<NN>.<M>`)** and **Level-4 Atomic Micro-Tasks (`<MOD>-P<NN>.<M>.<A>`)**:
   - Task `<M>.1`: Interface / Type / Schema / Contract Definition (Contract-First).
   - Task `<M>.2`: Core business logic implementation.
   - Task `<M>.3`: Unit tests & executable verification proof.
4. For each module, the first phase (`<MOD>-P01`) is initialized with `Lifecycle Status: READY_TO_EXECUTE` (or `IN_PROGRESS` when activated), while subsequent phases (`<MOD>-P02`, `<MOD>-P03`...) sit in `docs/plans/active/<module-slug>/` with `Lifecycle Status: PENDING`.
5. **Gate 4 Exit Lock:** Writing production code (Gate 5) is strictly forbidden until **all Phase Dossiers for all modules across the project** have been created in `docs/plans/active/`, verified via `python scripts/validate_plans.py --fix`, and approved by the Human Architect.

### Gate 5: Atomic Implementation & The `"Tiếp tục"` State Machine
1. **Single Atomic Task Turn (`1 Turn = 1 Task`):** In any single turn, the Agent executes **EXACTLY ONE ATOMIC TASK**.
2. **Single-Module Scope:** The task modifies only its module's `Code Root` and its active dossier in `docs/plans/active/<module-slug>/`.
3. **Executable Proof Invariant:** Every atomic task must be validated with real executable evidence (unit tests pass, build succeeds, contract checks pass) before checking off `- [x]`.
4. **The `"Tiếp tục"` (Continue) State Machine:**
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

Module codes and slugs are assigned once in the Module Registry and never reused. The pseudo-module `system` / `SYS` is reserved for cross-cutting work.

---

## 3. Cross-Module Contract Protocol

1. **Register:** Add the contract to `docs/plans/contract-registry.md` with ID (`CT-<PROVIDER>-<NN>`), type (`REST` | `gRPC` | `Event` | `Schema` | `Library`), provider, consumers, spec path, semantic version, and status `DRAFT`.
2. **Codify:** An atomic task (typically in `GP-01` / `<MOD>-P01`) writes the machine-readable spec at the declared path (OpenAPI, Protobuf, JSON Schema, AsyncAPI, typed DTO package). Once the file exists and validates, status becomes `AVAILABLE`.
3. **Consume:** Providers and consumers implement against the codified spec only. Consumers may use contract-derived test doubles to develop in parallel; they must never import another module's internals, query its storage, or read its source.
4. **Change Control:** Any change bumps the version and adds a Change Log entry listing impacted consumers. A breaking change requires explicit Human Architect approval and a decision record (`docs/templates/decision.md`) before implementation.
5. **Deprecate:** A contract becomes `DEPRECATED` only after all listed consumers have migrated.

---

## 4. Zero-Context Resume & Crash Recovery Protocol

### 4.1 Multi-Module & Multi-Agent Resume
When resuming work in a fresh session (or across parallel agent tabs / Git Worktrees), the Human Architect inputs `"tiếp tục"`, `"Continue"`, `"Where were we?"`, or `"Đang làm đến đâu rồi"` — optionally followed by a module code (e.g. `"tiếp tục AUTH"`):
1. Read **Active Work Pointer** in `docs/plans/system-roadmap.md`.
2. Select the target module's active phase dossier in `docs/plans/active/<module-slug>/` (choosing the dossier with `Lifecycle Status: IN_PROGRESS` or `PHASE_COMPLETED`, or the lowest-numbered `phase-<NN>-*.md` if starting).
3. Activate the mandatory skills for that module from `ai-skill-maps.md`.

### 4.2 3-Step Crash / Interrupted Task Reconciliation
If the IDE, terminal, or power was lost **mid-turn** while an Atomic Task was being executed, the `🎫 Resume Ticket` or checkbox `- [ ]` on disk may lag behind actual file modifications. Before writing any code on `"tiếp tục"`, the Agent MUST reconcile:

1. **Write-Ahead Ticket Update:** At the very start of every Atomic Task turn, before touching any source file, update the `🎫 Resume Ticket` to `Lifecycle Status: IN_PROGRESS` and set `Active Atomic Task` to the task being started.
2. **Working Tree Inspection (`git status` & `git diff`):** When resuming via `"tiếp tục"`, inspect the first unchecked `- [ ]` Atomic Task's `Target Files` and run `git status --short` / `git diff` scoped to the module's `Code Root`.
3. **Deterministic Recovery Action:**
   - **Clean State (No uncommitted edits in Target Files):** The task has not started. Execute the task from scratch.
   - **Completed-Before-Crash State (Target Files already implemented):** Run the task's `Executable Proof Command`. If all tests and acceptance criteria **PASS**, mark `- [x]` on that task, log the recovery in Section 4 of the dossier, and immediately execute the next sequential Atomic Task in the same turn.
   - **Partially-Written / Interrupted State (Target Files modified mid-edit or failing tests):** Report the exact state in 3 lines (*Module/Phase/Task, interrupted file & line/failure, and recovery action*), then complete the remaining logic of that exact Atomic Task without duplicating or overwriting valid work.

---

## 5. Multi-Agent & Git Worktree Execution

Once foundational contracts (`SYS` / `GP-01`) are `AVAILABLE`, multiple AI agents can execute different modules in parallel using two supported modes:

1. **Mode A — Parallel Tabs / Subagents in Shared Workspace:**
   - Each agent is assigned a distinct module code (`<MOD>`) and is strictly confined to `<MOD>`'s `Code Root` and `docs/plans/active/<module-slug>/`.
   - Because each module owns its own `docs/modules-spec/<module-slug>.md` and `docs/plans/active/<module-slug>/` directory, parallel agents never conflict on dossier files.
2. **Mode B — Isolated Git Worktrees (Recommended for Heavy Parallel Builds):**
   - Each agent creates an isolated worktree (`git worktree add ../<project>-<slug> -b feat/<slug> main`).
   - All Gate 5 atomic turns, builds, and unit tests run inside the worktree.
   - Upon completing all phases of `<MOD>`, the agent runs the full module test suite and `python scripts/validate_plans.py --fix`, commits cleanly, merges `feat/<slug>` back into `main`, and removes the worktree.

---

## 6. Structural Validation & Auto-Synchronization (`scripts/validate_plans.py`)

Run the cross-platform Python validator after any planning change, phase transition, or archival step:

```bash
# Validate structure, IDs, contracts, specs, and dossiers
python scripts/validate_plans.py

# Automatically synchronize Module Phase Sequence tables and Active Work Pointer from disk
python scripts/validate_plans.py --fix
```
