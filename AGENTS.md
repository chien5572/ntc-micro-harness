# Agent Instructions

<!-- HARNESS:BEGIN -->
## Harness: Atomic Engineering Protocol (Microservices Edition)

Start with the requested outcome and use the repository as the system of record.
Read `docs/WORKFLOW.md` and only the relevant system, module, phase, code, and validation material.

### Core Operating Invariants

1. **Hierarchy of Truth & Documents** (a lower document must never contradict a higher one; on conflict, STOP and ask):
   - `SPEC.md`: The supreme specification, functional boundaries, and architectural intent defined by the Human Architect.
   - `AGENTS.md`: The mandatory operating contract, behavioral boundaries, and execution rules.
   - `docs/plans/system-roadmap.md`: The Project Roadmap — architecture blueprint, Module Registry, Global Phases, inter-module dependency graph, and the **Active Work Pointer**.
   - `docs/plans/contract-registry.md`: The Cross-Module Contract Registry — every inter-module API, event, and shared schema with provider, consumers, spec path, version, and status.
   - `docs/plans/modules/<module>.md`: The Module Blueprint — charter, diagrams, data ownership, flows, provided/consumed contracts, and the module's own phase sequence.
   - `docs/plans/active/<module>/phase-<NN>-<slug>.md`: The active Module Phase Dossier containing Major Tasks, Atomic Work Breakdown Structure (WBS), and the real-time Resume Ticket.
   - `docs/plans/completed/<module>/phase-<NN>-<slug>.md`: Verified, archived dossiers (immutable audit record).

2. **The 5-Stage Gated Lifecycle (NEVER skip gates):**
   - **Gate 1 - Specification Ingestion:** When instructed to read `SPEC.md` and `AGENTS.md`, analyze architecture, propose candidate modules (services), and audit risks. **NEVER start writing code.**
   - **Gate 2 - Project Roadmap Alignment:** Collaboratively build `docs/plans/system-roadmap.md` (Module Registry, Global Phases, dependency graph) and `docs/plans/contract-registry.md` with the user. Await user approval before any module work.
   - **Gate 3 - Module Blueprint:** Only when instructed to plan a specific module, instantiate `docs/plans/modules/<module>.md` from `docs/templates/module-roadmap-template.md`, strictly respecting the Project Roadmap and Contract Registry. One module per request. Await user approval.
   - **Gate 4 - Module Phase Dossier & Recursive Atomic Breakdown:** Only when instructed to start a phase of a module, instantiate `docs/plans/active/<module>/phase-<NN>-<slug>.md`. Elaborate Major Tasks, then break them into **Atomic Tasks (Level 4 - Micro-tasks)**. If the user feels it is not detailed enough, continue the recursive breakdown loop.
   - **Gate 5 - Atomic Implementation:** **ONLY begin code implementation when the user explicitly instructs to implement a specific Atomic Task ID** (`<MOD>-P<NN>.<M>.<A>`).

3. **Implementation Invariants (Strict Execution):**
   - **Single Atomic Task Turn (1 Turn = 1 Task):** In any single response, execute **ONLY ONE ATOMIC TASK**. Never implement multiple tasks, modules, or services at once.
   - **Single-Module Scope:** An atomic task modifies only its own module's Code Root (declared in the Module Registry) and that module's planning files. Edits to shared contracts are their own atomic task.
   - **Contract-First (Module):** Task 1 of any module phase MUST define Types, Interfaces, Schemas, DTOs, or Protobufs before implementing business logic.
   - **Contract-First (Cross-Module):** Every inter-module API, event, or shared schema MUST be registered in `docs/plans/contract-registry.md` and codified at its declared spec path (status `AVAILABLE`) before provider or consumer logic is written.
   - **Contract Change Control:** Changing a registered contract bumps its version and lists impacted consumers in the registry change log. Breaking changes require explicit user approval and a decision record (`docs/templates/decision.md`).
   - **Dependency Gate:** A module phase may start only when the contracts it consumes are `AVAILABLE`. Consume other modules only through registered contracts (contract-derived test doubles are allowed). Never reach into another module's internals, storage, or source.
   - **Executable Proof:** Every atomic task must be verified with executable proof (unit tests pass, typechecks succeed, or explicit diagnostic logs). Never claim completion without proof.
   - **No-Stubbing Rule:** Never output incomplete stubs (`// TODO`, `// implement later`). Code must be fully implemented or bounded strictly to that atomic task.

4. **Micro-State Checkpointing & Resume Engine:**
   - **Before yielding any turn**, the agent MUST update the `🎫 Resume Ticket` at the top of the active dossier (`docs/plans/active/<module>/phase-<NN>-<slug>.md`), and update the **Active Work Pointer** in `docs/plans/system-roadmap.md` whenever the current stage or focus changes.
   - The ticket must capture: module, phase, current file, line number, dirty state, test failures, and the **Immediate Next Atomic Action**.
   - **One Active Phase per Module:** each `docs/plans/active/<module>/` holds at most one dossier. Several modules may be active, but only one is the **Current Focus**.
   - **Zero-Context Resume:** When the user returns (whether next day or next month) and asks *"Continue"*, *"Where were we?"*, *"Tiếp tục"*, or *"Đang làm đến đâu rồi"* (optionally followed by a module code), read the Active Work Pointer → open the named or focused dossier in `docs/plans/active/<module>/` → inspect its `🎫 Resume Ticket`, report the exact state in 3 lines, and resume without re-inventing or breaking prior code. If several dossiers are active and none is named or focused, list them and ask.
   - **Archival:** When every Atomic Task of a phase is verified, move the dossier from `docs/plans/active/<module>/` to `docs/plans/completed/<module>/` and update statuses in the Module Blueprint and Project Roadmap.
<!-- HARNESS:END -->
