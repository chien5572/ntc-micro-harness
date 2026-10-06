# Module Phase Dossier: <MOD>-P<NN> - <Phase Title>

> **Module:** `<MOD>` (`docs/plans/modules/<module-slug>.md#7-module-phase-sequence`)  
> **Global Phase:** `GP-<NN>` (`docs/plans/system-roadmap.md#3-global-phase-sequence`)  
> **Location:** `docs/plans/active/<module-slug>/phase-<NN>-<slug>.md` → moved to `docs/plans/completed/<module-slug>/` when verified  
> **Phase Owner:** AI Agent & Human Architect  
> **Last Updated:** YYYY-MM-DD HH:MM  

---

## 🎫 Resume Ticket (Instant State Checkpoint)
<!-- AGENT INVARIANT: MANDATORY to update this block before concluding ANY response turn -->
- **Module:** `<MOD>`
- **Lifecycle Status:** `READY_TO_PLAN` | `WBS_REVIEW` | `IN_PROGRESS` | `BLOCKED_BY_DEPENDENCY` | `INTERRUPTED` | `PHASE_COMPLETED`
- **Active Major Task:** Major Task <MOD>-P<NN>.1 - <Major Task Name>
- **Active Atomic Task:** Atomic Task <MOD>-P<NN>.1.1 - <Atomic Task Name>
- **In-flight File & Location:** `services/<module-slug>/src/service.ts:42`
- **Current Context / State:** Parsing logic completed; currently implementing repository calls; unit test `services/<module-slug>/tests/service.spec.ts` failing at case Y.
- **Immediate Next Atomic Action (When resuming):**
  Open `services/<module-slug>/src/service.ts` at line 42, finish repository invocation, then execute `npm test --prefix services/<module-slug>`.

---

## 1. Phase Architecture & Boundary Check
- **Phase Objective:**
- **Module Code Root (Single-Module Scope):** `services/<module-slug>/`
- **Boundary with other Phases of this Module (preventing regressions):**
- **Cross-Module Dependencies (Dependency Gate — all must be `AVAILABLE`):**

  | Contract ID | Provider | Registry Status | Used For |
  | :--- | :--- | :--- | :--- |
  | `CT-<OTHER>-01` | `<OTHER>` | `AVAILABLE` | ... |

- **Contracts Provided / Changed in this Phase:**

  | Contract ID | Change | Version | Breaking | Impacted Consumers |
  | :--- | :--- | :--- | :--- | :--- |
  | `CT-<MOD>-01` | Create | `1.0.0` | No | `SYS` |

- **Impacted Files:**
  - Create: `services/<module-slug>/src/...`
  - Modify: `services/<module-slug>/tests/...`

---

## 2. Work Breakdown Structure (WBS)

### Major Task <MOD>-P<NN>.1: <Feature / Component 1>
- [x] **Atomic Task <MOD>-P<NN>.1.1:** Define Interfaces / Types / DTOs / Schemas. *(Contract-First)*
- [ ] **Atomic Task <MOD>-P<NN>.1.2:** Implement core domain logic.
- [ ] **Atomic Task <MOD>-P<NN>.1.3:** Implement and verify unit tests for Major Task <MOD>-P<NN>.1.

### Major Task <MOD>-P<NN>.2: <Feature / Component 2>
*(Will be decomposed into Atomic Tasks upon completion of Major Task 1 or on demand)*
- [ ] **Atomic Task <MOD>-P<NN>.2.1:** ...

---

## 3. Atomic Task Specifications & Execution Protocol

> **Execution Rule:** 
> 1 Chat Turn = Execute EXACTLY 1 Atomic Task, inside this module's Code Root only. 
> After completing each Atomic Task: Run validation -> Check off [x] -> Update Resume Ticket -> STOP and report.

### Atomic Task <MOD>-P<NN>.1.1: [Task Name]
- **Objective:**
- **Target Files:** `services/<module-slug>/src/...`
- **Contracts Touched:** `CT-<MOD>-01` (or none)
- **Executable Proof Command:** `npm test` or `pytest tests/...`
- **Acceptance Criteria:**

---

## 4. Execution Evidence & Verification Log
*(Record diagnostic proof and test output after each atomic task)*
- **Atomic Task <MOD>-P<NN>.1.1:** PASS - [Log / Test result snippet]
- **Atomic Task <MOD>-P<NN>.1.2:** PASS - [Log / Test result snippet]
