# Agent Instructions

<!-- HARNESS:BEGIN -->
## Harness: Atomic Engineering Protocol (Microservices Edition v2.0)

Start with the requested outcome and use the repository as the single system of record.
Read `docs/WORKFLOW.md` and only the relevant system, module spec, skill map, phase dossier, code, and validation material.

### Core Operating Invariants

1. **Hierarchy of Truth & Documents** (a lower document must never contradict a higher one; on conflict, STOP and ask):
   - `SPEC.md`: The supreme system specification, functional boundaries, and architectural intent defined by the Human Architect.
   - `AGENTS.md`: The mandatory operating contract, behavioral boundaries, and execution rules.
   - `docs/plans/system-roadmap.md`: The Project Roadmap — architecture blueprint, Module Registry, Global Phases, inter-module dependency graph, and the **Active Work Pointer**.
   - `docs/plans/contract-registry.md`: The Cross-Module Contract Registry — every inter-module API, event, and shared schema with provider, consumers, spec path, version, and status.
   - `docs/modules-spec/<module-slug>.md`: The Detailed Module Specification — linked to `SPEC.md`, defining scope, user stories, exact DB/storage schemas, contracts, business flows/state machines, Given/When/Then acceptance criteria, error codes, and the **Module Phase Sequence** (`<MOD>-P<NN>`).
   - `ai-skill-maps.md`: The Project AI Skill Playbook — maps every module and phase to mandatory local skills (`.agents/skills/<skill-name>/SKILL.md`) that the agent MUST read before planning or writing code.
   - `docs/plans/active/<module-slug>/phase-<NN>-<slug>.md`: Pre-generated Module Phase Dossiers containing Major Tasks, Atomic Work Breakdown Structure (WBS), and the real-time `🎫 Resume Ticket`.
   - `docs/plans/completed/<module-slug>/phase-<NN>-<slug>.md`: Verified, archived dossiers (immutable audit record).
   - **Human-Only Boundary (`STEP-by-STEP.md`):** The root `STEP-by-STEP.md` file is generated at the end of Gate 3 strictly for the **Human Architect** to read and copy prompts from. **AI Agents MUST NOT read `STEP-by-STEP.md` during execution.**

2. **The 5-Stage Gated Lifecycle (NEVER skip gates):**
   - **Gate 1 - Root Specification Ingestion:** When instructed to read `SPEC.md` and `AGENTS.md`, analyze system architecture, propose candidate modules (services) with data ownership (`SYS` reserved for cross-cutting work), and audit technical risks. **NEVER start writing production code.**
   - **Gate 2 - Project Roadmap & Contract Registry Alignment:** Collaboratively build `docs/plans/system-roadmap.md` (Module Registry pointing to `docs/modules-spec/<slug>.md`, Global Phases, dependency graph, Active Work Pointer) and `docs/plans/contract-registry.md`. Await user approval before Gate 3.
   - **Gate 3 - All Detailed Module SPECs, `ai-skill-maps.md`, and `STEP-by-STEP.md`:**
     - **Step 3.1 (All Detailed Module SPECs):** Instantiate `docs/modules-spec/<module-slug>.md` from `docs/templates/module-spec-template.md` for **ALL registered modules** in the project, strictly aligned with `SPEC.md` and `docs/plans/contract-registry.md`.
     - **Step 3.2 (Interactive Skill Discovery & `ai-skill-maps.md`):** Once all `docs/modules-spec/*.md` files are complete, **STOP and ask the user** to input website URLs or skill repositories (e.g., `https://skillsmp.com/search`, `https://felo.ai/vi/skills`, GitHub) to search for relevant AI skills/plugins. Propose a candidate skill list (including custom project skills like `atomic-harness-gatekeeper` and `<project>-domain-invariants`) mapped to modules for user review. **Only after the user approves the skill list**, install the skills into `.agents/skills/` and instantiate `ai-skill-maps.md` from `docs/templates/ai-skill-maps-template.md`.
     - **Step 3.3 (Generate Human Playbook `STEP-by-STEP.md`):** Immediately after `ai-skill-maps.md` is created, instantiate `STEP-by-STEP.md` from `docs/templates/step-by-step-template.md` containing the dependency execution order and copy-paste prompts (enforcing `ai-skill-maps.md` and `docs/modules-spec/<slug>.md`). Await user approval before Gate 4.
   - **Gate 4 - Full Phase Dossiers & WBS Pre-Generation (Project-Wide):**
     - Consult `ai-skill-maps.md`, read the required `.agents/skills/<skill>/SKILL.md` files, and instantiate **ALL Phase Dossiers** (`docs/plans/active/<module-slug>/phase-<NN>-<slug>.md` from `docs/templates/phase-dossier-template.md`) for **ALL modules in the entire project**.
     - Decompose every phase into Major Tasks (`<MOD>-P<NN>.<M>`) and **Atomic Tasks (Level 4 - Micro-tasks: `<MOD>-P<NN>.<M>.<A>`)**.
     - **Gate 4 Exit Lock:** Code implementation (Gate 5) is strictly forbidden until **every planned phase of every module** has its Phase Dossier generated in `docs/plans/active/`, passes `python scripts/validate_plans.py`, and is approved by the user.
   - **Gate 5 - Atomic Implementation & `"Tiếp tục"` State Machine:**
     - Begin code implementation ONLY after Gate 4 is complete and the user instructs to start or continue a phase/task.

3. **Implementation Invariants (Strict Execution at Gate 5):**
   - **Single Atomic Task Turn (1 Turn = 1 Task):** In any single response, execute **ONLY ONE ATOMIC TASK** (`<MOD>-P<NN>.<M>.<A>`). Never implement multiple tasks, modules, or phases at once.
   - **Skill Activation Invariant:** Before implementing a module's phase, read the mandatory skills listed for that module/phase in `ai-skill-maps.md`.
   - **Single-Module Scope & Multi-Agent Isolation:** An atomic task modifies only its own module's `Code Root` and that module's dossier in `docs/plans/active/<module-slug>/`. Parallel agents (across tabs, subagents, or isolated Git Worktrees) may execute independent modules simultaneously once shared contracts (`CT-*`) are `AVAILABLE`.
   - **Contract-First (Module & Cross-Module):** Task `.1` of any Major Task MUST define Types, Interfaces, Schemas, DTOs, or Protobufs before business logic. Every cross-module contract in `docs/plans/contract-registry.md` must be codified at its spec path (status `AVAILABLE`) before consumer/provider integration logic is written.
   - **Contract Change Control:** Changing a registered contract bumps its semantic version and logs impacted consumers. Breaking changes require explicit user approval and a decision record (`docs/templates/decision.md`).
   - **Executable Proof & No-Stubbing Rule:** Every atomic task must be verified with executable proof (unit tests pass, typechecks succeed, or diagnostic logs). Never output incomplete stubs (`// TODO`, `// implement later`).
   - **In-Phase Dynamic Amendment:** If an unforeseen bug or edge case is discovered during Gate 5 within the current module's scope, insert a sub-task (`<MOD>-P<NN>.<M>.<A>a`) into the active dossier, document the reason, and execute it atomically.

4. **The `"Tiếp tục"` State Machine, Crash Recovery & Archival Engine:**
   - **Write-Ahead & End-of-Turn Checkpointing:** Mark the `🎫 Resume Ticket` as `IN_PROGRESS` with the target Atomic Task ID **before** editing code, and update it with verification results, line numbers, and the **Immediate Next Atomic Action** before yielding any turn. Run `python scripts/validate_plans.py --fix` whenever phase status or focus changes.
   - **3-Step Crash / Dirty-State Recovery (When App Closes Mid-Task):** Whenever resuming via `"tiếp tục"` (or `"continue"`), NEVER trust the `🎫 Resume Ticket` blindly. Inspect: (1) the first unchecked `- [ ]` Atomic Task in the active dossier, (2) `git status` / `git diff` inside the module's `Code Root`, and (3) the target files on disk:
     - *If target files were modified by an interrupted turn and tests already PASS:* check off `[x]`, update the `🎫 Resume Ticket`, report recovery, and execute the next unchecked Atomic Task.
     - *If target files are partially written or failing tests from a mid-turn crash:* report the exact interrupted file/line in 3 lines and finish that exact Atomic Task without duplicating code.
   - **Sequential `"Tiếp tục"` Execution:** When the active phase has remaining unchecked `- [ ]` Atomic Tasks and the user inputs `"tiếp tục"` (or `"continue"`, `"tiếp tục <MOD>"`), automatically execute the **next sequential unchecked Atomic Task** in that phase.
   - **Final Task of a Phase & Phase Boundary Hard Stop:**
     - On the turn that completes the **final** Atomic Task of a phase (`<MOD>-P<NN>`), check off `[x]`, set `Lifecycle Status` to `PHASE_COMPLETED`, and announce: *"Đã hoàn thành toàn bộ Atomic Tasks của Phase `<MOD>-P<NN>`. Vui lòng nhập `tiếp tục phase <MOD>-P<NN+1>` để lưu trữ phase hiện tại và chuyển sang phase kế tiếp."*
     - **Hard Stop Guardrail:** When a phase has 0 unchecked tasks left (`PHASE_COMPLETED`), if the user inputs plain `"tiếp tục"`, **DO NOT** advance to the next phase. Report that `<MOD>-P<NN>` is out of tasks and require the explicit command `"tiếp tục phase <MOD>-P<NN+1>"`.
   - **Automatic Phase Transition (`"tiếp tục phase <MOD>-P<NN+1>"`):** When the user explicitly inputs `"tiếp tục phase <MOD>-P<NN+1>"` (or `"tiếp tục phase <NN+1>"`), in that single turn the agent MUST:
     1. Move the completed dossier from `docs/plans/active/<module-slug>/phase-<NN>-*.md` to `docs/plans/completed/<module-slug>/phase-<NN>-*.md`.
     2. Activate `docs/plans/active/<module-slug>/phase-<NN+1>-*.md` (`Lifecycle Status: IN_PROGRESS`) and run `python scripts/validate_plans.py --fix` to synchronize `docs/modules-spec/<module-slug>.md` and the `Active Work Pointer` in `docs/plans/system-roadmap.md`.
     3. Immediately execute the **first Atomic Task (`<MOD>-P<NN+1>.1.1`)** of the newly activated phase.
<!-- HARNESS:END -->
