# Repository Workflow: Atomic Engineering Protocol (Microservices Edition)

Repository product behavior, architecture, decisions, plans, code, tests, and runtime signals are the single system of record.

Planning is layered so each document stays small enough to protect the agent's context window:

```text
SPEC.md
 └─ docs/plans/system-roadmap.md            Project Roadmap (Global Phases, Module Registry, dependencies)
     ├─ docs/plans/contract-registry.md     Cross-module contracts
     └─ docs/plans/modules/<module>.md      Module Blueprint (phases, diagrams, flows of ONE module)
         └─ docs/plans/active/<module>/phase-<NN>-<slug>.md     Module Phase Dossier (Resume Ticket)
             └─ Major Task  →  Atomic Task
                 (verified)  →  docs/plans/completed/<module>/phase-<NN>-<slug>.md
```

---

## 1. The 5-Stage Operating Standard

Every complex project, multi-service system, or enterprise feature must strictly adhere to the following 5-stage gated lifecycle.

### Stage 1: Specification Ingestion (SPEC Ingestion)
1. The Human Architect drafts `SPEC.md` (using `docs/templates/spec-template.md` and deep reasoning models on the web to challenge assumptions and define technical boundaries).
2. The `SPEC.md` file is placed in the repository root.
3. The Human Architect instructs the Agent: *"Read `SPEC.md` and `AGENTS.md`"*.
4. The Agent analyzes architecture, proposes **candidate modules (services)** with responsibilities and data ownership, identifies risks, and asks clarifying questions.
5. **Non-Negotiable Boundary:** **WRITING PRODUCTION CODE AT THIS STAGE IS STRICTLY FORBIDDEN.**

### Stage 2: Project Roadmap Alignment
1. The Agent and Human Architect collaboratively construct:
   - `docs/plans/system-roadmap.md` (from `docs/templates/system-roadmap-template.md`): architecture blueprint, **Module Registry** (code, slug, responsibility, Code Root, status), **Global Phases** (`GP-<NN>`, described at a high level with participating modules and exit criteria), the **Module Dependency Graph**, and the **Active Work Pointer**.
   - `docs/plans/contract-registry.md` (from `docs/templates/contract-registry-template.md`): every known inter-module contract, initially `DRAFT`.
2. Cross-cutting work (shared contract packages, local orchestration, CI, gateway if not its own service, end-to-end tests) is owned by the reserved pseudo-module **`system` (code `SYS`)**.
3. **Approval Gate (Gate 2):** The Human Architect reviews and approves. Only after approval may work advance to Stage 3.

### Stage 3: Module Blueprint
1. Triggered only when the Human Architect asks to plan a specific module (e.g. *"Plan module ORD"*).
2. The Agent instantiates `docs/plans/modules/<module-slug>.md` from `docs/templates/module-roadmap-template.md`: charter, tech stack, internal architecture diagram, data ownership, provided/consumed contracts (by contract ID), core flows (sequence diagrams), and the **Module Phase Sequence** (`<MOD>-P<NN>`, each aligned to a Global Phase).
3. The blueprint must not contradict the Project Roadmap or Contract Registry. If the module needs a new or changed contract, the Agent proposes the registry change explicitly.
4. One module per request. **Approval Gate (Gate 3):** the Human Architect approves the blueprint before any phase starts.

### Stage 4: Module Phase Dossier & Recursive Breakdown
1. Triggered only when the Human Architect asks to start a phase (e.g. *"Start phase 1 of module ORD"*).
2. **Dependency Gate:** every contract the phase consumes must be `AVAILABLE` in the Contract Registry. Otherwise, mark the phase `BLOCKED_BY_DEPENDENCY` and report what is missing.
3. The Agent instantiates `docs/plans/active/<module-slug>/phase-<NN>-<slug>.md` (from `docs/templates/phase-dossier-template.md`). Each module holds **at most one** active dossier.
4. The Agent expands the phase into **Major Tasks** (`<MOD>-P<NN>.<M>`).
5. **Recursive Breakdown Loop:**
   - The Agent decomposes Major Tasks into **Atomic Tasks (Level 4 - Micro-tasks)** (`<MOD>-P<NN>.<M>.<A>`):
     - Task X.1: Interface / Type / Schema Definition (Contract-First).
     - Task X.2: Business logic implementation.
     - Task X.3: Unit test & verification.
   - The Human Architect reviews the breakdown. If not sufficiently granular, the Agent continues recursive decomposition.
   - The breakdown loop completes only when the Human Architect explicitly instructs: *"Sufficiently detailed. Implement Atomic Task `<MOD>-P<NN>.<M>.<A>`."*

### Stage 5: Atomic Implementation & Resume Protocol
1. **Single Atomic Task Turn (1 Turn = 1 Task):** In any single turn or response, the Agent is restricted to implementing **EXACTLY ONE ATOMIC TASK**.
2. **Single-Module Scope:** The task modifies only its module's Code Root and planning files. A shared-contract edit is its own atomic task (usually owned by the provider module or `SYS`).
3. **Contract-First Invariant:** All interfaces, schemas, and types must be codified before business logic is written — within the module, and across modules via the Contract Registry.
4. **Executable Proof Invariant:** Every atomic task must be validated with executable evidence (unit tests pass, build succeeds, contract tests pass) before claiming completion.
5. **Resume Ticket Checkpoint:** Before yielding any turn, the Agent MUST update the `🎫 Resume Ticket` at the top of `docs/plans/active/<module>/phase-<NN>-<slug>.md`, and the Active Work Pointer in `docs/plans/system-roadmap.md` whenever stage or focus changes.
6. **Zero-Context Hiatus Resumption:** see Section 4.

---

## 2. Identifier Convention

| Level | Format | Example |
| :--- | :--- | :--- |
| Global Phase (project) | `GP-<NN>` | `GP-02` |
| Module | `<MOD>` (2-5 uppercase letters) + lowercase slug | `AUTH` / `auth` |
| Module Phase | `<MOD>-P<NN>` ↔ file `phase-<NN>-<slug>.md` | `AUTH-P01` |
| Major Task | `<MOD>-P<NN>.<M>` | `AUTH-P01.2` |
| Atomic Task | `<MOD>-P<NN>.<M>.<A>` | `AUTH-P01.2.3` |
| Contract | `CT-<PROVIDER>-<NN>` | `CT-AUTH-01` |

Module codes and slugs are assigned once in the Module Registry and never reused. The pseudo-module `system` / `SYS` is reserved for cross-cutting work.

---

## 3. Cross-Module Contract Protocol

1. **Register:** add the contract to `docs/plans/contract-registry.md` with ID, type (REST / gRPC / Event / Schema), provider, consumers, spec path, version, status `DRAFT`.
2. **Codify:** an atomic task writes the machine-readable spec at the declared path (OpenAPI, Protobuf, JSON Schema, AsyncAPI, typed DTO package...). Once the spec exists and validates, status becomes `AVAILABLE`.
3. **Consume:** providers and consumers implement against the codified spec only. Consumers may use contract-derived test doubles; they must never import another module's internals, query its storage, or read its source.
4. **Change Control:** any change bumps the version and adds a Change Log entry listing impacted consumers. A breaking change requires explicit Human Architect approval and a decision record (`docs/templates/decision.md`) before implementation.
5. **Deprecate:** a contract becomes `DEPRECATED` only after all listed consumers have migrated.

---

## 4. Resume Protocol (Multi-Module)

When resuming work in a fresh session (days or months later), the Human Architect simply inputs *"Continue"*, *"Where were we?"*, *"Tiếp tục"*, or *"Đang làm đến đâu rồi"* — optionally followed by a module code (e.g. *"Continue ORD"*).

1. Read **Active Work Pointer** in `docs/plans/system-roadmap.md` (Current Stage, Current Focus, active dossier table).
2. Select the dossier:
   - module named → `docs/plans/active/<module>/`;
   - otherwise → Current Focus;
   - several active and no focus → list them and ask.
3. If the stage is Gate 2 or Gate 3 (no dossier yet), resume the planning document named in the pointer.
4. Inspect the `🎫 Resume Ticket`, report the exact state in 3 lines (module/phase/task, in-flight file and failures, next atomic action), and resume without rewriting or breaking existing code.

The pointer's active dossier table must always match the actual contents of `docs/plans/active/`.

---

## 5. Completion and Archival

### 5.1 Module Phase Completion
When all Atomic Tasks in `docs/plans/active/<module>/phase-<NN>-<slug>.md` are verified:
1. Run the module's full test suite and its contract tests.
2. Move the file from `docs/plans/active/<module>/phase-<NN>-<slug>.md` to `docs/plans/completed/<module>/phase-<NN>-<slug>.md`. Remove `docs/plans/active/<module>/` if it is now empty.
3. Update the phase status to `COMPLETED` (and its dossier link) in `docs/plans/modules/<module>.md`.
4. Update the Active Work Pointer in `docs/plans/system-roadmap.md`.
5. Proceed to the next phase as scheduled in the Module Blueprint, only when instructed.

### 5.2 Global Phase Completion
A Global Phase `GP-<NN>` is `COMPLETED` when every module phase aligned to it is in `docs/plans/completed/` **and** the integration / end-to-end checks owned by `SYS` pass.

### 5.3 Module Completion
A module is `COMPLETED` in the Module Registry when every phase in its blueprint is `COMPLETED`.

### 5.4 Structural Validation
Run `scripts/validate-plans.ps1` after any planning change or archival step. It checks the document hierarchy, identifiers, Resume Tickets, the one-active-dossier rule, and Active Work Pointer consistency.
