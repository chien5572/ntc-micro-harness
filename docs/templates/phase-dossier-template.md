# Module Phase Dossier: <MOD>-P<NN> - <Phase Title>

> **Module:** `<MOD>` (`docs/modules-spec/<module-slug>.md#9-module-phase-sequence`)  
> **Global Phase:** `GP-<NN>` (`docs/plans/system-roadmap.md#3-global-phase-sequence`)  
> **Skill Map Reference:** `ai-skill-maps.md`  
> **Mandatory Skills Activated:** `atomic-harness-gatekeeper`, `<project>-domain-invariants`, `<module-tech-skills>`  
> **Location:** `docs/plans/active/<module-slug>/phase-<NN>-<slug>.md` → moved to `docs/plans/completed/<module-slug>/` when verified & transitioned  
> **Phase Owner:** AI Agent & Human Architect  
> **Last Updated:** YYYY-MM-DD HH:MM  

---

## 🎫 Resume Ticket (Instant State Checkpoint)
<!-- AGENT INVARIANT: Update to IN_PROGRESS BEFORE editing code (write-ahead), and update before concluding ANY turn. -->
- **Module:** `<MOD>`
- **Lifecycle Status:** `PENDING` | `READY_TO_EXECUTE` | `IN_PROGRESS` | `BLOCKED_BY_DEPENDENCY` | `INTERRUPTED` | `PHASE_COMPLETED`
- **Active Major Task:** Major Task <MOD>-P<NN>.1 - <Major Task Name>
- **Active Atomic Task:** Atomic Task <MOD>-P<NN>.1.1 - <Atomic Task Name>
- **In-flight File & Location:** `services/<module-slug>/src/service.ts:42`
- **Current Context / State:** Parsing logic completed; currently implementing repository calls; unit test `services/<module-slug>/tests/service.spec.ts` passing/failing at case Y.
- **Immediate Next Atomic Action (When resuming):**
  Execute Atomic Task `<MOD>-P<NN>.1.2` in `services/<module-slug>/src/service.ts`, then run `npm test --prefix services/<module-slug>`.

---

## 1. Phase Architecture & Boundary Check
- **Phase Objective:**
- **Detailed Module Spec Section Reference:** `docs/modules-spec/<module-slug>.md` (§...)
- **Approved UI Prototypes Mapped to this Phase (if UI module):** `SCR-<MOD>-01` (`docs/prototypes/<module-slug>/scr-01-....html`) *(or `N/A — Non-UI Phase`)*
- **Mandatory Skills Read Before Execution:** `.agents/skills/atomic-harness-gatekeeper/SKILL.md`, `...`
- **Module Code Root (Single-Module Scope):** `services/<module-slug>/`
- **Boundary with other Phases of this Module (preventing regressions):**
- **Cross-Module Dependencies (Dependency Gate — all must be `AVAILABLE` before Gate 5 execution of this phase):**

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
- [ ] **Atomic Task <MOD>-P<NN>.2.1:** Define Interfaces / Types / Schemas for Component 2. *(Contract-First)*
- [ ] **Atomic Task <MOD>-P<NN>.2.2:** Implement domain logic for Component 2.
- [ ] **Atomic Task <MOD>-P<NN>.2.3:** Implement and verify unit tests for Major Task <MOD>-P<NN>.2.

---

## 3. Atomic Task Specifications & Execution Protocol

> **Execution & `"Tiếp tục"` State Machine Rule:**
> - **1 Chat Turn = Execute EXACTLY 1 Atomic Task**, inside this module's `Code Root` only.
> - **When user types `"tiếp tục"`:** Reconcile working tree (3-Step Crash Recovery), then execute the next sequential unchecked `- [ ]` Atomic Task.
> - **When completing the LAST Atomic Task of this phase:** Check off `[x]`, set `Lifecycle Status: PHASE_COMPLETED`, and announce that all tasks of `<MOD>-P<NN>` are done and the user must enter `"tiếp tục phase <MOD>-P<NN+1>"` to transition.
> - **Hard Stop:** Never advance to `<MOD>-P<NN+1>` on plain `"tiếp tục"`. Only on `"tiếp tục phase <MOD>-P<NN+1>"` do you archive this dossier to `docs/plans/completed/<module-slug>/`, run `python scripts/validate_plans.py --fix`, activate `<MOD>-P<NN+1>`, and execute `<MOD>-P<NN+1>.1.1`.

### Atomic Task <MOD>-P<NN>.1.1: [Task Name]
- **Objective:**
- **Target Files:** `services/<module-slug>/src/...`
- **Contracts Touched:** `CT-<MOD>-01` (or none)
- **UI Prototype Reference (Strict 1:1 Parity if UI task):** `SCR-<MOD>-01` (`docs/prototypes/<module-slug>/scr-01-....html`) — MUST read file & port 1:1 DOM, classes, states (`default`/`loading`/`empty`/`error`), and `data-testid` anchors (or `none`)
- **Executable Proof Command:** `npm test` or `pytest tests/...`
- **Acceptance Criteria (from `docs/modules-spec/<module-slug>.md`):**

---

## 4. Execution Evidence & Verification Log
*(Record diagnostic proof and test output after each atomic task)*
- **Atomic Task <MOD>-P<NN>.1.1:** PASS - [Log / Test result snippet]
