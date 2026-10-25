# NTC Micro Harness: Atomic Engineering Protocol (Microservices Edition v2.0)

<p align="center">
  <strong>🌐 Language / Ngôn ngữ:</strong>
  <strong>🇺🇸 English (Current)</strong> |
  <a href="README.vi.md">🇻🇳 Tiếng Việt</a>
</p>

[![CI Validation](https://github.com/chien5572/ntc-micro-harness/actions/workflows/validate.yml/badge.svg)](https://github.com/chien5572/ntc-micro-harness/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Protocol Version](https://img.shields.io/badge/Harness-v2.0.0-green.svg)](AGENTS.md)
[![Compatible with](https://img.shields.io/badge/AI%20Agents-Antigravity%20%7C%20Claude%20Code%20%7C%20Cursor%20%7C%20Windsurf-orange.svg)](AGENTS.md)

**NTC Micro Harness v2.0** is an enterprise-grade, zero-drift, token-efficient engineering harness and behavioral governance framework designed for pair-programming and multi-agent orchestration with autonomous AI coding assistants (**Google Antigravity**, **Anthropic Claude Code**, **Cursor**, **Windsurf**, and **Roo Code / Cline**).

Instead of allowing AI agents to jump prematurely into writing fragmented, unverified code or improvising unapproved user interfaces, **NTC Micro Harness v2.0** enforces a deterministic **5-Stage Gated Lifecycle**:
1. **UI Prototype & Visual Sign-Off First (if UI Required):** Locks interactive HTML/CSS prototypes (`docs/prototypes/<slug>/scr-<nn>-*.html`) with `data-testid` anchors and design tokens in **Gate 3.0** before writing detailed specs or code.
2. **Complete Module Specifications & AI Skill Mapping:** Authors detailed specifications for every module (`docs/modules-spec/`), discovers and installs project AI skills (`ai-skill-maps.md`), and generates a human operator playbook (`STEP-by-STEP.md`).
3. **Upfront Project-Wide WBS:** Pre-generates all Phase Dossiers across every module (`docs/plans/active/`) before touching production code.
4. **Atomic Execution & `"Tiếp tục"` Engine:** Executes strictly **one Atomic Task per turn** (`1 Turn = 1 Task`) with **1:1 UI Prototype Parity**, executable test proof, **3-Step Crash Recovery**, and a hard stop at phase boundaries (`"tiếp tục phase <MOD>-P<NN+1>"`).

---

## Table of Contents

1. [Introduction & Why NTC Micro Harness v2.0?](#1-introduction--why-ntc-micro-harness-v20)
2. [Core Architecture & Hierarchy of Truth](#2-core-architecture--hierarchy-of-truth)
3. [One-Liner Installation Guide (All Environments)](#3-one-liner-installation-guide-all-environments)
   - [3.1 Windows PowerShell / PowerShell Core](#31-windows-powershell--powershell-core)
   - [3.2 Windows Command Prompt (CMD)](#32-windows-command-prompt-cmd)
   - [3.3 Linux / macOS / WSL / Git Bash](#33-linux--macos--wsl--git-bash)
   - [3.4 Universal Python One-Liner (Any OS)](#34-universal-python-one-liner-any-os)
   - [3.5 Advanced Installer Flags & What Gets Installed](#35-advanced-installer-flags--what-gets-installed)
4. [Complete Execution Workflow (Step-by-Step Guide)](#4-complete-execution-workflow-step-by-step-guide)
   - [Step 0: Initialize `SPEC.md`](#step-0-initialize-specmd)
   - [Gate 1: Root Specification Ingestion & Architecture Audit](#gate-1-root-specification-ingestion--architecture-audit)
   - [Gate 2: System Roadmap & Cross-Module Contract Registry](#gate-2-system-roadmap--cross-module-contract-registry)
   - [Gate 3: UI Prototypes (`3.0`), Detailed Module SPECs (`3.1`), `ai-skill-maps.md` (`3.2`), and `STEP-by-STEP.md` (`3.3`)](#gate-3-ui-prototypes-30-detailed-module-specs-31-ai-skill-mapsmd-32-and-step-by-stepmd-33)
   - [Gate 4: Project-Wide Phase Dossiers & Atomic WBS Pre-Generation](#gate-4-project-wide-phase-dossiers--atomic-wbs-pre-generation)
   - [Gate 5: Atomic Implementation, 1:1 UI Parity & The `"Tiếp tục"` State Machine](#gate-5-atomic-implementation-11-ui-parity--the-tiếp-tục-state-machine)
5. [5-Layer UI Prototype Enforcement (How Agents Are Locked to Approved UI)](#5-5-layer-ui-prototype-enforcement-how-agents-are-locked-to-approved-ui)
6. [Crash Recovery & Multi-Agent Parallel Execution](#6-crash-recovery--multi-agent-parallel-execution)
   - [6.1 3-Step Mid-Turn Crash & Dirty-State Recovery](#61-3-step-mid-turn-crash--dirty-state-recovery)
   - [6.2 Multi-Agent Parallel Execution (Shared Tabs vs. Git Worktrees)](#62-multi-agent-parallel-execution-shared-tabs-vs-git-worktrees)
7. [Automated Validation & Auto-Synchronization (`validate_plans.py`)](#7-automated-validation--auto-synchronization-validate_planspy)
8. [Repository Structure & Identifier Convention Reference](#8-repository-structure--identifier-convention-reference)

---

## 1. Introduction & Why NTC Micro Harness v2.0?

When building complex microservices, modular monoliths, or full-stack applications, unharnessed AI coding agents consistently fail in six predictable ways. **NTC Micro Harness v2.0** eliminates each failure mode mechanically:

| Failure Mode | Symptom in Unharnessed AI | NTC Micro Harness v2.0 Remedy |
| :--- | :--- | :--- |
| **1. Premature Coding & Shallow Specs** | Agent rushes to write code before database schemas, state machines, edge cases, and cross-service contracts exist. | **Gate 1 → Gate 3 Lock:** Production code is strictly forbidden until `SPEC.md`, `system-roadmap.md`, `contract-registry.md`, and **all** `docs/modules-spec/<slug>.md` are completed. |
| **2. Hallucinated / Unapproved UI Layouts** | Agent invents arbitrary layouts, inconsistent colors, or missing UI states during frontend implementation, causing endless rework. | **Gate 3.0 UI Prototyping & 1:1 Parity Lock:** Interactive HTML/CSS prototypes (`docs/prototypes/<slug>/scr-<nn>-*.html`) with `data-testid` anchors must be previewed and `APPROVED` by the user before specs/code. Gate 5 forces 1:1 DOM & token porting. |
| **3. Ignored or Unmapped AI Skills** | Agent forgets to consult domain/framework skills (`.agents/skills/`) and invents inconsistent patterns across modules. | **Gate 3.2 (`ai-skill-maps.md`):** Agent stops to ask for skill repository URLs, proposes skills for human approval, installs them into `.agents/skills/`, and binds every module/phase to mandatory skills. |
| **4. Planning / Coding Context Thrashing** | Constantly switching back and forth between high-level planning and coding breaks developer flow and bloats context. | **Gate 4 Project-Wide WBS Pre-Generation:** **Every Phase Dossier across all modules** is decomposed into Level-4 Atomic Tasks upfront before Gate 5 unlocks. |
| **5. Multi-Task Sprawl & High Prompt Friction** | Agent edits 15 files in one turn leaving `// TODO` stubs, or forces the developer to copy-paste long task IDs every turn. | **`"Tiếp tục"` State Machine:** Enforces `1 Turn = 1 Atomic Task` with executable test proof. Simply type `"tiếp tục"` to run the next task; hard-stops at phase boundaries until `"tiếp tục phase <MOD>-P<NN+1>"` is entered. |
| **6. Mid-Turn Crash / Session Amnesia** | IDE crashes mid-turn or a new session starts days later, causing the agent to overwrite or duplicate half-written files. | **Write-Ahead `🎫 Resume Ticket` + 3-Step Crash Recovery:** Inspects `git status` and `git diff` against the active task's target files to seamlessly resume or complete interrupted work. |

---

## 2. Core Architecture & Hierarchy of Truth

All planning, UI prototyping, and specification artifacts are layered so that an AI agent only loads the slice of context required for its current turn:

```text
SPEC.md (Supreme System Specification)
 ├─ AGENTS.md                                     Mandatory AI Behavioral Contract & Operating Rules
 ├─ docs/plans/system-roadmap.md                  Project Roadmap (Global Phases, Module Registry, Active Work Pointer)
 ├─ docs/plans/contract-registry.md               Cross-Module APIs, Events, Schemas (CT-<PROVIDER>-<NN>)
 ├─ docs/prototypes/registry.md                   UI Prototype & Design System Registry (SCR-<MOD>-<NN>, if UI Required)
 │   └─ docs/prototypes/<module-slug>/scr-*.html  Approved Interactive HTML/CSS Prototypes (with data-testid anchors)
 ├─ docs/modules-spec/<module-slug>.md            Detailed Module SPEC + UI Screen Mapping + Module Phase Sequence (<MOD>-P<NN>)
 ├─ ai-skill-maps.md                              Project AI Skill Playbook (.agents/skills/<skill>/SKILL.md)
 ├─ STEP-by-STEP.md                               Human-Only Playbook (Copy-paste prompts; AI Agents DO NOT read this)
 └─ docs/plans/active/<module-slug>/
     ├─ phase-01-<slug>.md                        Active Phase Dossier (IN_PROGRESS + real-time 🎫 Resume Ticket)
     └─ phase-02-<slug>.md                        Pre-generated Next Phase Dossier (PENDING)
         └─ Major Task (<MOD>-P<NN>.<M>)
             └─ Atomic Task (<MOD>-P<NN>.<M>.<A>) ──► 1 Turn = 1 Task + 1:1 UI Prototype Parity + Executable Proof
                 ("tiếp tục phase ...")           ──► Archived to docs/plans/completed/<module-slug>/
```

### Hierarchy of Truth

A lower document must **never** contradict a higher one. If a discrepancy is detected, the AI agent must **STOP immediately and ask the Human Architect**:

1. **`SPEC.md`** — Supreme system specification, functional boundaries, UI requirements (`UI Required: YES | NO`), and architectural intent defined by the Human Architect.
2. **`AGENTS.md`** — Mandatory operating contract, behavioral boundaries, and execution invariants.
3. **`docs/plans/system-roadmap.md`** — Master Project Roadmap: Module Registry, Global Phases (`GP-<NN>`), inter-module dependency graph, and the real-time **Active Work Pointer**.
4. **`docs/plans/contract-registry.md`** — Cross-Module Contract Registry: every shared REST/gRPC endpoint, async event, and schema (`CT-<MOD>-<NN>`).
5. **`docs/prototypes/registry.md` & `docs/prototypes/<module-slug>/scr-<nn>-*.html`** — Visual & UI Prototype Contract Registry (when `UI Required: YES`): locks design tokens, interactive screen layouts, visual states (`default`, `loading`, `empty`, `error`), and `data-testid` anchors (`SCR-<MOD>-<NN>`) approved by the Human Architect.
6. **`docs/modules-spec/<module-slug>.md`** — Detailed Module Specification: scope, user stories, exact DB/storage schemas, contracts, UI screen mappings (`SCR-<MOD>-<NN>`), sequence diagrams/state machines, Given/When/Then acceptance criteria, error codes, and the **Module Phase Sequence** (`<MOD>-P<NN>`).
7. **`ai-skill-maps.md`** — Project AI Skill Playbook mapping each module and phase to mandatory local skills (`.agents/skills/<skill-name>/SKILL.md`).
8. **`docs/plans/active/<module-slug>/phase-<NN>-<slug>.md`** — Pre-generated Module Phase Dossiers containing Major Tasks, Level-4 Atomic WBS, UI Prototype References, and the real-time `🎫 Resume Ticket`.
9. **`docs/plans/completed/<module-slug>/phase-<NN>-<slug>.md`** — Verified, archived phase dossiers (immutable audit history).

> [!IMPORTANT]
> **Human-Only Boundary (`STEP-by-STEP.md`):** `STEP-by-STEP.md` is generated at the end of Gate 3 strictly for the **Human Architect** to read and copy prompts from. **AI Agents are strictly forbidden from reading `STEP-by-STEP.md` during execution.**

---

## 3. One-Liner Installation Guide (All Environments)

Open your terminal **directly inside your target project directory** (existing or newly created):

```bash
cd /path/to/your-project
```

Then copy and paste the **single one-liner command** for your operating system / shell below. The command will automatically fetch **NTC Micro Harness v2.0** from GitHub, install the harness into your current project folder (`.`), configure AI agent rules (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`), and clean up all temporary files.

---

### 3.1 Windows PowerShell / PowerShell Core

Open **PowerShell** inside your project directory and paste:

```powershell
irm https://raw.githubusercontent.com/chien5572/ntc-micro-harness/main/install.ps1 | iex
```

*(Alternative using `git clone` in PowerShell)*:
```powershell
git clone --depth 1 https://github.com/chien5572/ntc-micro-harness.git .ntc-tmp; & .\.ntc-tmp\install.ps1 -TargetPath .; Remove-Item -Recurse -Force .ntc-tmp
```

---

### 3.2 Windows Command Prompt (CMD)

Open **Command Prompt (`cmd.exe`)** inside your project directory and paste:

```cmd
powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://raw.githubusercontent.com/chien5572/ntc-micro-harness/main/install.ps1 | iex"
```

*(Alternative using `git` + `python` in CMD)*:
```cmd
git clone --depth 1 https://github.com/chien5572/ntc-micro-harness.git .ntc-tmp && python .ntc-tmp\install.py --target . --agent all && rmdir /s /q .ntc-tmp
```

---

### 3.3 Linux / macOS / WSL / Git Bash

Open **Bash** or **Zsh** inside your project directory and paste:

```bash
curl -fsSL https://raw.githubusercontent.com/chien5572/ntc-micro-harness/main/install.sh | bash
```

*(Alternative using `git clone` in Bash/Zsh)*:
```bash
git clone --depth 1 https://github.com/chien5572/ntc-micro-harness.git .ntc-tmp && bash .ntc-tmp/install.sh . && rm -rf .ntc-tmp
```

---

### 3.4 Universal Python One-Liner (Any OS)

If **Python 3.8+** is installed on any OS (Windows, macOS, Linux), open a terminal inside your project folder and paste:

```bash
python -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/chien5572/ntc-micro-harness/main/install.py').read())"
```
*(Use `python3` instead of `python` on macOS/Linux if `python` is not aliased).*

---

### 3.5 Advanced Installer Flags & What Gets Installed

When running `install.py` or `install.ps1` with custom options:

| Option (`install.py`) | Option (`install.ps1`) | Description |
| :--- | :--- | :--- |
| `--target .` | `-TargetPath "."` | Target project directory (defaults to current working directory `.`). |
| `--agent all` | `-AgentRules all` | Generate rule hooks for `all` (`CLAUDE.md`, `.cursorrules`, `.windsurfrules`), or specify `claude`, `cursor`, `windsurf`, `none`. |
| `--force` | `-Force` | Overwrite existing harness files if upgrading from an older version. |

**Safe Non-Destructive Behavior on Existing Projects:**
- If your project already has an `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, or `.windsurfrules`, the installer **safely appends** the `<!-- HARNESS:BEGIN -->` block without deleting your existing instructions.
- Copies `docs/WORKFLOW.md`, `docs/prototypes/registry.md`, `docs/modules-spec/README.md`, `docs/plans/system-roadmap.md`, `docs/plans/contract-registry.md`, all templates in `docs/templates/`, and `scripts/validate_plans.py`.

Verify your installation immediately by running:
```bash
python scripts/validate_plans.py
```

---

## 4. Complete Execution Workflow (Step-by-Step Guide)

```mermaid
flowchart LR
    S0["Step 0<br/>Draft SPEC.md"] --> G1["Gate 1<br/>Ingest SPEC &<br/>Audit Architecture"]
    G1 --> G2["Gate 2<br/>System Roadmap &<br/>Contract Registry"]
    G2 --> G3["Gate 3<br/>3.0 UI Prototypes (if UI)<br/>3.1 All Module SPECs<br/>3.2 ai-skill-maps.md<br/>3.3 STEP-by-STEP.md"]
    G3 --> G4["Gate 4<br/>Pre-Generate ALL<br/>Phase Dossiers (WBS)"]
    G4 --> G5["Gate 5<br/>Atomic Execution &<br/>1:1 UI Parity ('tiếp tục')"]
```

Follow the steps below in order to take any project from idea to production-verified code.

---

### Step 0: Initialize `SPEC.md`

Copy the starter specification template to the root of your project and fill in your business requirements, target stack, UI requirements (`UI Required: YES | NO`), and core workflows:

```bash
# Linux / macOS / Git Bash
cp docs/templates/spec-template.md SPEC.md

# Windows PowerShell
Copy-Item docs/templates/spec-template.md SPEC.md
```

---

### Gate 1: Root Specification Ingestion & Architecture Audit

Open your AI coding agent (Antigravity, Claude Code, Cursor, or Windsurf) and paste this prompt:

```text
Read SPEC.md and AGENTS.md.
Execute Gate 1 (Root Specification Ingestion):
1. Analyze the system architecture, domain boundaries, UI surface (`UI Required: YES | NO`), and technical risks.
2. Propose the list of modules/microservices (with 2-5 uppercase letter Module Codes, slugs, data ownership, and responsibilities — reserving SYS / system for cross-cutting foundation work).
3. List any clarifying architectural or UI/UX questions before we proceed to Gate 2.
STRICT RULE: Do NOT write any production code.
```

---

### Gate 2: System Roadmap & Cross-Module Contract Registry

Once you answer the agent's questions and approve the module breakdown, prompt:

```text
Approved. Proceed to Gate 2:
1. Populate `docs/plans/system-roadmap.md` (using `docs/templates/system-roadmap-template.md`) with the Architecture Blueprint, Module Registry (pointing to `docs/modules-spec/<slug>.md`), Global Phases (`GP-01`, `GP-02`, ...), Module Dependency Graph, and Active Work Pointer.
2. Populate `docs/plans/contract-registry.md` (using `docs/templates/contract-registry-template.md`) with all cross-module APIs, events, and shared schemas (`CT-<PROVIDER>-<NN>`), initialized as `DRAFT`.
3. Run `python scripts/validate_plans.py` and stop for my Gate 2 approval.
```

---

### Gate 3: UI Prototypes (`3.0`), Detailed Module SPECs (`3.1`), `ai-skill-maps.md` (`3.2`), and `STEP-by-STEP.md` (`3.3`)

Gate 3 executes in **four sequential sub-steps** (`Step 3.0` is conditional on whether your project has a UI):

#### Step 3.0 (Conditional — Mandatory if Project Has UI): Interactive UI Prototyping & Visual Sign-Off (`docs/prototypes/`)

- **If your project has NO user interface (`UI Required: NO`):** The agent sets `> **UI Required:** NO` in `docs/prototypes/registry.md` and proceeds directly to **Step 3.1**.
- **If your project includes any UI / Frontend module (`UI Required: YES`):** Before writing any `docs/modules-spec/*.md` file, lock the UI design and screen flows with this prompt:

```text
Gate 2 is approved. Execute Gate 3 - Step 3.0 (UI Prototyping & Design System Lock):
1. Populate `docs/prototypes/registry.md` (using `docs/templates/ui-prototype-registry-template.md`) with our locked Design System tokens (color variables, typography, spacing, layout shell) and the UI Screen Registry (`SCR-<MOD>-<NN>`).
2. Generate self-contained interactive HTML/CSS prototypes at `docs/prototypes/<module-slug>/scr-<nn>-<slug>.html` for every screen so I can open and test them directly in a browser.
3. Every HTML prototype MUST include all visual states (`default`, `loading`, `empty`, `error`) and explicit `data-testid="scr-<nn>-<element>"` attributes on key containers, forms, inputs, buttons, and tables.
4. STOP and wait for me to preview the HTML files, request any visual adjustments, and approve them (`Status: APPROVED` in `docs/prototypes/registry.md`) before proceeding to Step 3.1.
```

> [!NOTE]
> Once you review the `.html` prototypes in your browser and are happy with the layout, tell the agent: *"I approve all UI prototypes. Mark them `APPROVED` in `docs/prototypes/registry.md` and proceed to Step 3.1."*

#### Step 3.1: Generate Detailed Module Specifications (`docs/modules-spec/<slug>.md`) for ALL Modules

Prompt the agent:

```text
Proceed to Gate 3 - Step 3.1:
Using `docs/templates/module-spec-template.md`, generate the Detailed Module Specification `docs/modules-spec/<module-slug>.md` for EVERY registered module in `docs/plans/system-roadmap.md` (starting with `system.md`, then each domain/UI module).
Each module spec must be 100% complete (Scope, User Stories, Tech Stack, Exact DB/Storage DDL & Indexes, Contracts & Events, Section 5.4 UI Screen & Prototype Mappings `SCR-<MOD>-<NN>` for UI modules, Sequence Diagrams & State Machines, Given/When/Then Acceptance Criteria, NFRs/Error Codes, and Module Phase Sequence `<MOD>-P<NN>`).
If there are many modules, generate them thoroughly (1–2 modules per turn) until all modules have their `docs/modules-spec/<slug>.md` file.
When all `docs/modules-spec/*.md` files are complete, STOP and ask me for AI Skill catalog URLs to begin Step 3.2.
```

#### Step 3.2: Interactive AI Skill Discovery & `ai-skill-maps.md`

As soon as all `docs/modules-spec/*.md` files exist, the agent will **STOP and ask you** for website URLs or skill repositories to search for AI skills. Reply with your preferred skill catalogs:

```text
Search for relevant AI skills for our tech stack and domain modules from these sources:
- https://skillsmp.com/search
- https://felo.ai/vi/skills
- Local `.agents/skills/` or official framework skill repositories
Also propose custom project-specific skills (including `atomic-harness-gatekeeper`, `<project>-domain-invariants`, and `ui-prototype-fidelity` if our project has UI).
Present the candidate skill table mapped to our modules for my approval before installing them or creating `ai-skill-maps.md`.
```

After reviewing the agent's proposed skill table, approve it:

```text
I approve the skill list. Please:
1. Create/install the approved `.agents/skills/<skill-name>/SKILL.md` files.
2. Generate `ai-skill-maps.md` at the repository root (from `docs/templates/ai-skill-maps-template.md`).
3. Immediately proceed to Gate 3 - Step 3.3: generate `STEP-by-STEP.md` (from `docs/templates/step-by-step-template.md`) for the Human Architect, and run `python scripts/validate_plans.py --fix`.
```

#### Step 3.3: Human Execution Playbook (`STEP-by-STEP.md`)

- The agent generates `STEP-by-STEP.md` at the project root containing the exact module dependency order and ready-to-copy prompts customized for your project's actual module codes (`SYS`, `AUTH`, `WEB`, etc.).
- **Remember:** `STEP-by-STEP.md` is strictly for **you (the Human Architect)** to read and copy prompts from. AI agents never read `STEP-by-STEP.md`.

---

### Gate 4: Project-Wide Phase Dossiers & Atomic WBS Pre-Generation

Before writing a single line of production code, **all Phase Dossiers (`docs/plans/active/<module-slug>/phase-<NN>-<slug>.md`) for every module in the project** must be pre-generated and decomposed into Level-4 Atomic Tasks.

Copy the Gate 4 prompt from your `STEP-by-STEP.md` (or use the prompt below):

```text
Proceed to Gate 4 (Project-Wide Phase Dossiers & Atomic WBS Pre-Generation):
1. Read `AGENTS.md`, `ai-skill-maps.md` (and activate the mandatory `.agents/skills/*/SKILL.md` files), `docs/plans/system-roadmap.md`, `docs/plans/contract-registry.md`, `docs/prototypes/registry.md`, and all `docs/modules-spec/*.md` files. (Do NOT read `STEP-by-STEP.md`).
2. Using `docs/templates/phase-dossier-template.md`, generate ALL Phase Dossiers `docs/plans/active/<module-slug>/phase-<NN>-<slug>.md` for EVERY planned phase of EVERY module in the project.
3. Decompose every phase into Major Tasks (`<MOD>-P<NN>.<M>`) and Level-4 Atomic Micro-Tasks (`<MOD>-P<NN>.<M>.<A>`):
   - `.1`: Contract / Interface / Schema / Type definition (Contract-First)
   - `.2`: Core business logic or UI component implementation (for UI tasks, explicitly populate `UI Prototype Reference: SCR-<MOD>-<NN>` pointing to `docs/prototypes/<module-slug>/scr-<nn>-*.html`)
   - `.3`: Unit / Component verification tests with Executable Proof Command (asserting `data-testid` anchors for UI tasks)
4. Set `phase-01` of the starting module(s) to `READY_TO_EXECUTE` and subsequent phases (`phase-02`, `phase-03`...) to `PENDING`.
5. Run `python scripts/validate_plans.py --fix` and report the full list of generated Phase Dossiers for Gate 4 approval.
STRICT RULE: Do NOT write production code in Gate 4.
```

---

### Gate 5: Atomic Implementation, 1:1 UI Parity & The `"Tiếp tục"` State Machine

Once all Phase Dossiers are in `docs/plans/active/` and `python scripts/validate_plans.py` passes with 0 errors, you unlock **Gate 5**.

#### 1. Starting Phase 01 of a Module (e.g., `SYS-P01`)

```text
Gate 4 is approved. Enter Gate 5 and start Phase `SYS-P01`:
1. Read `ai-skill-maps.md` and activate the required skills for `SYS` (`system`).
2. Read `docs/modules-spec/system.md` and `docs/plans/active/system/phase-01-foundation.md`.
3. Execute ONLY the first Atomic Task `SYS-P01.1.1` (`1 Turn = 1 Atomic Task`).
4. Run the Executable Proof Command, check off `[x]`, update the `🎫 Resume Ticket`, and run `python scripts/validate_plans.py --fix`.
```

#### 2. Sequential Execution via `"tiếp tục"`

From this point forward, you do **not** need to type long prompts or task IDs. Simply type:

```text
tiếp tục
```
*(Or `"tiếp tục <MOD>"`, e.g., `"tiếp tục AUTH"` / `"tiếp tục WEB"`, or `"continue"`).*

On each `"tiếp tục"`, the agent automatically:
1. Checks the `🎫 Resume Ticket` and runs **3-Step Crash / Dirty-State Recovery**.
2. Marks the target Atomic Task `IN_PROGRESS` (Write-Ahead).
3. **If the task has a `UI Prototype Reference` (`SCR-<MOD>-<NN>`):** Reads the approved `docs/prototypes/<module-slug>/scr-<nn>-*.html` file and ports its DOM hierarchy, CSS/Tailwind tokens, states (`default`/`loading`/`empty`/`error`), and `data-testid` attributes **1:1** into the component.
4. Executes the unit/component test command (`Executable Proof`).
5. Marks `- [x]` on the task, updates the `🎫 Resume Ticket` with the next Atomic Task ID, and stops cleanly.

#### 3. Completing the Final Task of a Phase & The Hard Stop Guardrail

When the agent finishes the **last unchecked Atomic Task** of `<MOD>-P<NN>` (e.g., `AUTH-P01`):
- It marks `- [x]` on the final task and sets `Lifecycle Status: PHASE_COMPLETED` in the `🎫 Resume Ticket`.
- It outputs the mandatory completion announcement:
  > *"Đã hoàn thành toàn bộ Atomic Tasks của Phase `AUTH-P01`. Vui lòng nhập `tiếp tục phase AUTH-P02` để lưu trữ phase hiện tại và chuyển sang phase kế tiếp."*
- **Hard Stop Protection:** If you accidentally type plain `"tiếp tục"` when `AUTH-P01` is already `PHASE_COMPLETED`, the agent **will NOT start `AUTH-P02`**. It will stop and remind you to enter the explicit phase transition command.

#### 4. Transitioning to the Next Phase via `"tiếp tục phase <MOD>-P<NN+1>"`

To archive the completed phase and immediately begin the next phase, type:

```text
tiếp tục phase AUTH-P02
```
*(Or `"tiếp tục phase 02"`).*

In that **single turn**, the agent automatically:
1. Moves `docs/plans/active/auth/phase-01-*.md` → `docs/plans/completed/auth/phase-01-*.md`.
2. Activates `docs/plans/active/auth/phase-02-*.md` (`Lifecycle Status: IN_PROGRESS`).
3. Runs `python scripts/validate_plans.py --fix` to synchronize the Module Phase Sequence table in `docs/modules-spec/auth.md` and the `Active Work Pointer` in `docs/plans/system-roadmap.md`.
4. Immediately executes the **first Atomic Task (`AUTH-P02.1.1`)** of the new phase!

---

## 5. 5-Layer UI Prototype Enforcement (How Agents Are Locked to Approved UI)

To prevent AI agents from ignoring or drifting away from the UI prototype you approved in Gate 3.0, **NTC Micro Harness v2.0** enforces a **5-Layer Defense-in-Depth Lock**:

| Layer | Enforcement Surface | How It Prevents UI Drift |
| :--- | :--- | :--- |
| **Layer 1: Visual Contract Registry** | `docs/prototypes/registry.md` & `docs/prototypes/<slug>/scr-<nn>-*.html` | Locks Design System tokens (colors, fonts, layout shell) and assigns every screen a canonical ID (`SCR-<MOD>-<NN>`). Must be marked `APPROVED` before Gate 3.1. |
| **Layer 2: Dossier-Level Traceability** | `docs/modules-spec/<slug>.md` (§5.4) & `phase-<NN>-*.md` (§3) | Every UI Atomic Task carries `- **UI Prototype Reference:** SCR-<MOD>-<NN> (docs/prototypes/...)`. On `"tiếp tục"`, the agent sees the exact `.html` path right inside the active task. |
| **Layer 3: `data-testid` & DOM Parity** | HTML Prototypes → Production Components → Unit Tests (`.3`) | HTML prototypes must include `data-testid="scr-<nn>-<element>"` hooks. Gate 5 components must preserve those exact `data-testid` hooks, and Task `.3` unit tests assert them. |
| **Layer 4: Skill & Playbook Rules** | `AGENTS.md`, `ai-skill-maps.md` (`ui-prototype-fidelity`), `STEP-by-STEP.md` | Explicitly instructs the agent to `read_file` the HTML prototype in the same turn before writing component code and forbids improvising styles or layouts. |
| **Layer 5: Mechanical Validator** | `python scripts/validate_plans.py` | Automatically blocks Gate 4/5 if any `SCR-<MOD>-<NN>` is still `DRAFT` (`PROTOTYPE_NOT_APPROVED`), if the `.html` file is missing (`PROTOTYPE_FILE_MISSING`), or if the `.html` file lacks `data-testid=` attributes (`PROTOTYPE_TESTID_MISSING`). |

---

## 6. Crash Recovery & Multi-Agent Parallel Execution

### 6.1 3-Step Mid-Turn Crash & Dirty-State Recovery

What happens if your IDE crashes, your laptop loses power, or the network drops **in the middle of an Atomic Task**?

Simply reopen your editor and type:
```text
tiếp tục
```

Before writing a single line of code, the agent executes the **3-Step Crash Recovery Protocol**:
1. **Inspects the Active Dossier:** Locates the first unchecked `- [ ]` Atomic Task and its declared `Target Files` and `Executable Proof Command`.
2. **Inspects Git Working Tree:** Runs `git status --short` and `git diff` scoped to the module's `Code Root`.
3. **Deterministic Reconciliation:**
   - **Case A — Clean Working Tree:** The crash occurred before any file was written. The agent executes the Atomic Task cleanly from scratch.
   - **Case B — Code Completed Before Crash & Tests Pass:** The agent runs the `Executable Proof Command`. If all tests already pass, it checks off `- [x]`, logs the recovery in the dossier's Execution Log, and immediately executes the **next** unchecked Atomic Task in the same turn.
   - **Case C — Partially Written / Failing Tests:** The agent outputs a concise 3-line recovery report identifying the exact interrupted file/line and completes the remaining code of that exact Atomic Task without duplicating work.

---

### 6.2 Multi-Agent Parallel Execution (Shared Tabs vs. Git Worktrees)

Once foundational contracts in `GP-01` (`SYS-P01`) are codified and marked `AVAILABLE` in `docs/plans/contract-registry.md`, you can run **multiple AI agents in parallel** across independent modules (e.g., Agent 1 on `AUTH`, Agent 2 on `ORD`, Agent 3 on `WEB`):

#### Mode A: Parallel Agent Tabs in the Same Workspace
Open separate chat tabs in Antigravity / Claude Code / Cursor and scope each tab by module code:
- **Tab 1:** `"tiếp tục AUTH"`
- **Tab 2:** `"tiếp tục WEB"`

Because `AUTH` only touches `services/auth/` + `docs/plans/active/auth/` and `WEB` only touches `services/web/` + `docs/plans/active/web/`, they never overwrite each other's files.

#### Mode B: Isolated Git Worktrees (Recommended for Heavy Builds & Port Isolation)
From your project root, create an isolated Git Worktree per module:

```bash
git worktree add ../myproject-auth -b feat/auth main
git worktree add ../myproject-web -b feat/web main
```

Open an AI agent inside each worktree folder and run `"tiếp tục AUTH"` / `"tiếp tục WEB"`. When a module finishes all of its phases:

```bash
python scripts/validate_plans.py --fix
git add . && git commit -m "feat(auth): complete all AUTH module phases"
# From the main repository root:
git checkout main
git merge --no-ff feat/auth
git worktree remove ../myproject-auth
```

---

## 7. Automated Validation & Auto-Synchronization (`validate_plans.py`)

NTC Micro Harness v2.0 ships with a zero-dependency, cross-platform Python structural validator (`scripts/validate_plans.py`).

```bash
# 1. Validate all structural, contract, prototype, and dossier invariants across the repository
python scripts/validate_plans.py

# 2. Automatically synchronize Module Phase Sequence tables and the Active Work Pointer from disk
python scripts/validate_plans.py --fix
```

**What `scripts/validate_plans.py` verifies:**
- `AGENTS.md` contains the intact `<!-- HARNESS:BEGIN -->` ... `<!-- HARNESS:END -->` contract block.
- Every module registered in `docs/plans/system-roadmap.md` has a valid `docs/modules-spec/<slug>.md` and a valid Module Phase Sequence table.
- Every contract in `docs/plans/contract-registry.md` (`CT-<MOD>-<NN>`) references a registered provider module, valid consumer modules, and an existing spec file when status is `AVAILABLE`.
- Every UI screen in `docs/prototypes/registry.md` (`SCR-<MOD>-<NN>`) references a registered module, points to a valid `docs/prototypes/<slug>/scr-*.html` file containing `data-testid="..."` hooks when `APPROVED`, and is never left in `DRAFT` once Phase Dossiers exist for that module.
- When Phase Dossiers exist (Gate 4/5), `ai-skill-maps.md` and `STEP-by-STEP.md` exist at the repository root.
- Every Phase Dossier in `docs/plans/active/<slug>/` and `docs/plans/completed/<slug>/` has a valid `🎫 Resume Ticket`, `Lifecycle Status`, and properly formatted Atomic Task checkboxes.
- When `--fix` is passed, it automatically updates the `Module Phase Sequence` status column in `docs/modules-spec/<slug>.md` and the `Active Work Pointer` table in `docs/plans/system-roadmap.md` to match the live dossiers on disk.

---

## 8. Repository Structure & Identifier Convention Reference

### Repository Structure

```text
.
├── AGENTS.md                                      # Root AI operating contract & behavioral rules (v2.0)
├── README.md                                      # English documentation
├── README.vi.md                                   # Vietnamese documentation (Tiếng Việt)
├── docs/
│   ├── WORKFLOW.md                                # Complete 5-stage protocol, UI parity & crash recovery spec
│   ├── README.md                                  # Documentation directory map
│   ├── prototypes/                                # UI Prototype & Design System Registry (Gate 3.0)
│   │   ├── README.md
│   │   └── registry.md                            # Screen inventory (SCR-<MOD>-<NN>) & design tokens
│   ├── modules-spec/                              # Detailed Module Specifications (docs/modules-spec/<slug>.md)
│   │   └── README.md
│   ├── patterns/
│   │   └── encoding-invariants.md                 # Engineering invariants & mechanical validation patterns
│   ├── plans/
│   │   ├── system-roadmap.md                      # Master Project Roadmap, Module Registry & Active Work Pointer
│   │   ├── contract-registry.md                   # Cross-module API/Event/Schema contract registry
│   │   ├── active/                                # Pre-generated & active phase dossiers (<slug>/phase-<NN>-*.md)
│   │   └── completed/                             # Archived phase dossiers (immutable audit trail)
│   └── templates/
│       ├── spec-template.md                       # Root SPEC.md starter template
│       ├── system-roadmap-template.md             # Master roadmap template
│       ├── contract-registry-template.md          # Cross-module contract registry template
│       ├── ui-prototype-registry-template.md      # UI Prototype & Design System registry template
│       ├── module-spec-template.md                # Detailed Module Spec template (docs/modules-spec/<slug>.md)
│       ├── ai-skill-maps-template.md              # Project AI Skill Playbook template (ai-skill-maps.md)
│       ├── step-by-step-template.md               # Human-Only Operator Playbook template (STEP-by-STEP.md)
│       ├── phase-dossier-template.md              # Phase Dossier + Resume Ticket + WBS + UI Prototype Reference
│       ├── decision.md                            # Architecture Decision Record (ADR) template
│       ├── exec-plan.md                           # Single-session execution plan template
│       └── application-runbook.md                 # Service operations & incident runbook template
├── scripts/
│   └── validate_plans.py                          # Cross-platform Python validator & auto-synchronizer (--fix)
├── install.py                                     # Universal Python installer (local & remote one-liner)
├── install.ps1                                    # Windows PowerShell installer (local & remote one-liner)
├── install.sh                                     # Linux / macOS / WSL Bash installer (local & remote one-liner)
└── LICENSE                                        # MIT License
```

### Identifier Convention Cheat Sheet

| Level | Format | Example | Authoritative File |
| :--- | :--- | :--- | :--- |
| **Global Phase** | `GP-<NN>` | `GP-01` | `docs/plans/system-roadmap.md` |
| **Module Code / Slug** | `<MOD>` / `<slug>` | `AUTH` / `auth` | `docs/plans/system-roadmap.md` & `docs/modules-spec/auth.md` |
| **Module Phase** | `<MOD>-P<NN>` | `AUTH-P01` | `docs/plans/active/auth/phase-01-*.md` |
| **Major Task** | `<MOD>-P<NN>.<M>` | `AUTH-P01.2` | `docs/plans/active/auth/phase-01-*.md` |
| **Atomic Task** | `<MOD>-P<NN>.<M>.<A>` | `AUTH-P01.2.3` | `docs/plans/active/auth/phase-01-*.md` (**1 Turn = 1 Task**) |
| **Dynamic Hotfix Task** | `<MOD>-P<NN>.<M>.<A>[a-z]` | `AUTH-P01.2.3a` | `docs/plans/active/auth/phase-01-*.md` |
| **Cross-Module Contract** | `CT-<PROVIDER>-<NN>` | `CT-AUTH-01` | `docs/plans/contract-registry.md` |
| **UI Screen Prototype** | `SCR-<MOD>-<NN>` | `SCR-WEB-01` | `docs/prototypes/registry.md` (`docs/prototypes/<slug>/scr-<nn>-*.html`) |

---

## License

Licensed under the [MIT License](LICENSE). Copyright (c) 2026 [chien5572](https://github.com/chien5572).
