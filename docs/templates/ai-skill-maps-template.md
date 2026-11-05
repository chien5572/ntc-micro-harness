# Project AI Skill Playbook (`ai-skill-maps.md`)

> **Purpose:** This document is the authoritative AI Skill Routing Map for both the **Human Architect** and **AI Coding Agents** in `<Project Name>`.
>
> **Origin (Step 3 — `/ntc-spec`):** Generated immediately after locking the overall `SPEC.md` and Module Registry in `docs/plans/system-roadmap.md` — **BEFORE** authoring detailed module specifications (`docs/modules-spec/<slug>.md` in Step 4 `/ntc-modules`).
>
> **Mandatory Rule for AI Agents:** Before authoring a Detailed Module Spec (Step 4 `/ntc-modules`), instantiating a Phase Dossier (Step 5 `/ntc-plan`), or executing an Atomic Task (Step 6 `/ntc-run`):
> 1. Identify the target **Module (`<MOD>`)** and **Phase (`<MOD>-P<NN>`)**.
> 2. Look up the **Module & Phase Skill Mapping Matrix** in Section 2 below.
> 3. Read the corresponding `.agents/skills/<skill-name>/SKILL.md` files before writing module specs, WBS plans, contracts, or production code.

---

## 1. Installed Project Skills Catalog (`.agents/skills/`)

All approved project skills are installed locally under `.agents/skills/`:

| # | Skill Name (`name`) | Local `SKILL.md` Path | Source | Primary Target Modules |
| :-: | :--- | :--- | :--- | :--- |
| 1 | **`atomic-harness-gatekeeper`** | [`.agents/skills/atomic-harness-gatekeeper/SKILL.md`](.agents/skills/atomic-harness-gatekeeper/SKILL.md) | Custom (Harness Core) | All Modules (`AGENTS.md`, `docs/plans/*`, `docs/modules-spec/*`) |
| 2 | **`<project>-domain-invariants`** | [`.agents/skills/<project>-domain-invariants/SKILL.md`](.agents/skills/<project>-domain-invariants/SKILL.md) | Custom (Project Domain) | Core domain rules from `SPEC.md` & `docs/modules-spec/*` |
| 3 | **`ui-prototype-fidelity`** | [`.agents/skills/ui-prototype-fidelity/SKILL.md`](.agents/skills/ui-prototype-fidelity/SKILL.md) | Custom (UI Parity Lock) | All UI Modules (`docs/prototypes/registry.md` & `scr-*.html`) |
| 4 | **`using-git-worktrees`** | [`.agents/skills/using-git-worktrees/SKILL.md`](.agents/skills/using-git-worktrees/SKILL.md) | Built-in / Superpowers | Parallel Multi-Agent Git Worktree isolation |
| 5 | **`<tech-skill-1>`** | [`.agents/skills/<tech-skill-1>/SKILL.md`](.agents/skills/<tech-skill-1>/SKILL.md) | SkillsMP / Felo / Custom | `services/<module-slug>` |
| 6 | **`<tech-skill-2>`** | [`.agents/skills/<tech-skill-2>/SKILL.md`](.agents/skills/<tech-skill-2>/SKILL.md) | SkillsMP / Felo / Custom | `services/<module-slug>` |

---

## 2. Module & Phase Skill Mapping Matrix

| Module / Global Scope | Code Root & Spec Path | Mandatory Skills to Activate (Step 4 Spec → Step 5 Plan → Step 6 Run) |
| :--- | :--- | :--- |
| **All Steps & All Phases** | `AGENTS.md`, `SPEC.md`, `docs/plans/*` | `atomic-harness-gatekeeper`, `<project>-domain-invariants` |
| **`SYS` (`system`)** | `./` (`docs/modules-spec/system.md`) | `atomic-harness-gatekeeper`, `<infra-or-e2e-skills>` |
| **`AUTH` (`auth`)** | `services/auth/` (`docs/modules-spec/auth.md`) | `atomic-harness-gatekeeper`, `<project>-domain-invariants`, `<tech-skill-1>` |
| **`WEB` (`web`)** | `apps/web/` (`docs/modules-spec/web.md`) | `atomic-harness-gatekeeper`, `ui-prototype-fidelity`, `<tech-skill-2>` |

---

## 3. Detailed Skill Playbook (When & How to Use)

### 3.1 Core Governance & Domain Invariant Skills

#### 1) `atomic-harness-gatekeeper`
- **File:** [`.agents/skills/atomic-harness-gatekeeper/SKILL.md`](.agents/skills/atomic-harness-gatekeeper/SKILL.md)
- **When to activate:**
  - At the start of every session or when receiving `/ntc-run`, `"tiếp tục"`, `"tiếp tục <MOD>"`, or `"tiếp tục phase <MOD>-P<NN>"`.
  - During Step 4 (`/ntc-modules`), Step 5 (`/ntc-plan`), and Step 6 (`/ntc-run`).
  - Before concluding any turn to update the `🎫 Resume Ticket`, run `python scripts/validate_plans.py --fix`, and create the Atomic Git Commit checkpoint.
- **Core Enforcement:** Locks `1 Turn = 1 Atomic Task`, `Contract-First`, `1:1 UI Prototype Parity (SCR-<MOD>-<NN> + data-testid)`, `No-Stubbing`, **End-of-Turn Atomic Git Commit Checkpointing**, 3-Step Crash Recovery against `HEAD`, the **4-Step Delta Reverse-Unlock Protocol (`/ntc-cr` / `CR-<NN>`)** for mid-flight change requests, and the Phase Boundary Hard Stop on `"tiếp tục"`.

#### 2) `<project>-domain-invariants`
- **File:** [`.agents/skills/<project>-domain-invariants/SKILL.md`](.agents/skills/<project>-domain-invariants/SKILL.md)
- **When to activate:** When authoring `docs/modules-spec/<slug>.md` (Step 4) or implementing domain logic, state transitions, and unit tests (Step 6).
- **Core Enforcement:** Prevents drift from non-negotiable domain formulas, state machine guards, and data ownership boundaries defined in `SPEC.md`.

#### 3) `ui-prototype-fidelity` *(Mandatory if Project Has UI Modules)*
- **File:** [`.agents/skills/ui-prototype-fidelity/SKILL.md`](.agents/skills/ui-prototype-fidelity/SKILL.md)
- **When to activate:** When executing Step 4 (`/ntc-modules`), Step 5 (`/ntc-plan`), or Step 6 (`/ntc-run`) for any UI / Frontend module referencing `SCR-<MOD>-<NN>` in `docs/prototypes/registry.md`.
- **Core Enforcement:** Requires reading `docs/prototypes/<module-slug>/scr-<nn>-*.html` before coding, porting DOM hierarchy, CSS/Tailwind tokens, and `default`/`loading`/`empty`/`error` states 1:1, and asserting `data-testid` anchors in Task `.3` unit/component tests.

---

### 3.2 Module-Specific Technical Skills

#### 4) `<tech-skill-1>`
- **File:** [`.agents/skills/<tech-skill-1>/SKILL.md`](.agents/skills/<tech-skill-1>/SKILL.md)
- **When to activate:** When authoring `docs/modules-spec/<slug>.md` (Step 4), generating Phase Dossiers (Step 5), or implementing Atomic Tasks (Step 6) for `<MOD>`.
- **Target Scope:** `services/<module-slug>/` (`docs/modules-spec/<module-slug>.md`).
- **Key Patterns to Enforce:**
  - Pattern A
  - Pattern B
