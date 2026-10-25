# Project AI Skill Playbook (`ai-skill-maps.md`)

> **Purpose:** This document is the authoritative AI Skill Routing Map for both the **Human Architect** and **AI Coding Agents** in `<Project Name>`.
>
> **Origin (Gate 3 - Step 3.2):** Generated ONLY after:
> 1. All `docs/modules-spec/<module-slug>.md` files have been completed.
> 2. The Agent has asked the Human Architect for skill search URLs (e.g., `https://skillsmp.com/search`, `https://felo.ai/vi/skills`, GitHub), proposed relevant skills per module, received **explicit user approval**, and installed them into `.agents/skills/`.
>
> **Mandatory Rule for AI Agents:** Before instantiating any Phase Dossier (Gate 4) or executing any Atomic Task (Gate 5):
> 1. Identify the target **Module (`<MOD>`)** and **Phase (`<MOD>-P<NN>`)**.
> 2. Look up the **Module & Phase Skill Mapping Matrix** in Section 2 below.
> 3. Read the corresponding `.agents/skills/<skill-name>/SKILL.md` files before writing plans, contracts, or production code.

---

## 1. Installed Project Skills Catalog (`.agents/skills/`)

All approved project skills are installed locally under `.agents/skills/`:

| # | Skill Name (`name`) | Local `SKILL.md` Path | Source | Primary Target Modules |
| :-: | :--- | :--- | :--- | :--- |
| 1 | **`atomic-harness-gatekeeper`** | [`.agents/skills/atomic-harness-gatekeeper/SKILL.md`](.agents/skills/atomic-harness-gatekeeper/SKILL.md) | Custom (Harness Core) | All Modules (`AGENTS.md`, `docs/plans/*`, `docs/modules-spec/*`) |
| 2 | **`<project>-domain-invariants`** | [`.agents/skills/<project>-domain-invariants/SKILL.md`](.agents/skills/<project>-domain-invariants/SKILL.md) | Custom (Project Domain) | Core domain rules from `SPEC.md` & `docs/modules-spec/*` |
| 3 | **`using-git-worktrees`** | [`.agents/skills/using-git-worktrees/SKILL.md`](.agents/skills/using-git-worktrees/SKILL.md) | Built-in / Superpowers | Parallel Multi-Agent Git Worktree isolation |
| 4 | **`<tech-skill-1>`** | [`.agents/skills/<tech-skill-1>/SKILL.md`](.agents/skills/<tech-skill-1>/SKILL.md) | SkillsMP / Felo / Custom | `services/<module-slug>` |
| 5 | **`<tech-skill-2>`** | [`.agents/skills/<tech-skill-2>/SKILL.md`](.agents/skills/<tech-skill-2>/SKILL.md) | SkillsMP / Felo / Custom | `services/<module-slug>` |

---

## 2. Module & Phase Skill Mapping Matrix

| Module / Global Scope | Code Root & Spec Path | Mandatory Skills to Activate |
| :--- | :--- | :--- |
| **All Gates & All Phases** | `AGENTS.md`, `SPEC.md`, `docs/plans/*` | `atomic-harness-gatekeeper`, `<project>-domain-invariants` |
| **`SYS` (`system`)** | `./` (`docs/modules-spec/system.md`) | `atomic-harness-gatekeeper`, `<infra-or-contract-skills>` |
| **`AUTH` (`auth`)** | `services/auth/` (`docs/modules-spec/auth.md`) | `atomic-harness-gatekeeper`, `<project>-domain-invariants`, `<tech-skill-1>` |
| **`ORD` (`order`)** | `services/order/` (`docs/modules-spec/order.md`) | `atomic-harness-gatekeeper`, `<project>-domain-invariants`, `<tech-skill-2>` |

---

## 3. Detailed Skill Playbook (When & How to Use)

### 3.1 Core Governance & Domain Invariant Skills

#### 1) `atomic-harness-gatekeeper`
- **File:** [`.agents/skills/atomic-harness-gatekeeper/SKILL.md`](.agents/skills/atomic-harness-gatekeeper/SKILL.md)
- **When to activate:**
  - At the start of every session or when receiving `"tiếp tục"`, `"tiếp tục <MOD>"`, or `"tiếp tục phase <MOD>-P<NN>"`.
  - During Gate 4 (Phase Dossier WBS generation) and Gate 5 (Atomic Task implementation).
  - Before concluding any turn to update the `🎫 Resume Ticket` and run `python scripts/validate_plans.py --fix`.
- **Core Enforcement:** Locks `1 Turn = 1 Atomic Task`, `Contract-First`, `1:1 UI Prototype Parity (SCR-<MOD>-<NN> + data-testid)`, `No-Stubbing`, 3-Step Crash Recovery, and the Phase Boundary Hard Stop on `"tiếp tục"`.

#### 2) `<project>-domain-invariants`
- **File:** [`.agents/skills/<project>-domain-invariants/SKILL.md`](.agents/skills/<project>-domain-invariants/SKILL.md)
- **When to activate:** When designing domain logic, state transitions, or unit tests for core business flows.
- **Core Enforcement:** Prevents drift from non-negotiable domain formulas, state machine guards, and data ownership boundaries defined in `SPEC.md`.

#### 3) `ui-prototype-fidelity` *(Mandatory if Project Has UI Modules)*
- **File:** [`.agents/skills/ui-prototype-fidelity/SKILL.md`](.agents/skills/ui-prototype-fidelity/SKILL.md)
- **When to activate:** When executing Gate 4 WBS or Gate 5 Atomic Tasks for any UI / Frontend module referencing `SCR-<MOD>-<NN>` in `docs/prototypes/registry.md`.
- **Core Enforcement:** Requires reading `docs/prototypes/<module-slug>/scr-<nn>-*.html` before coding, porting DOM hierarchy, CSS/Tailwind tokens, and `default`/`loading`/`empty`/`error` states 1:1, and asserting `data-testid` anchors in Task `.3` unit/component tests.

---

### 3.2 Module-Specific Technical Skills

#### 3) `<tech-skill-1>`
- **File:** [`.agents/skills/<tech-skill-1>/SKILL.md`](.agents/skills/<tech-skill-1>/SKILL.md)
- **When to activate:** When generating Phase Dossiers (Gate 4) or implementing Atomic Tasks (Gate 5) for `<MOD>`.
- **Target Scope:** `services/<module-slug>/` (`docs/modules-spec/<module-slug>.md`).
- **Key Patterns to Enforce:**
  - Pattern A
  - Pattern B
