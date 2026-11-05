---
name: ntc-init
description: "Step 1 of NTC Micro-Harness (/ntc-init): Connect project Git remote repository (optional), bootstrap Harness files, ask interactive clarifying questions on basic requirements, and generate PRD.md and ARCHITECTURE.md."
---

# `/ntc-init` — Step 1: Git Remote Setup & Interactive Discovery (`PRD.md` + `ARCHITECTURE.md`)

Activate this skill whenever the user invokes **`/ntc-init`** or asks to initialize a new project with **NTC Micro-Harness**.

## Supported Flags & Arguments
- `--repo <git-url>` *(optional)*: Remote Git repository URL (e.g., `https://github.com/org/project.git` or `git@github.com:org/project.git`). May be omitted or left blank for local-only repositories.
- `--idea "<description>"` *(optional)*: Initial project idea or basic requirements summary.
- `--no-ui` *(optional)*: Marks the project as headless/backend-only (`UI Required: NO`), skipping Step 2 (`/ntc-prototype`).
- `--approve` *(optional)*: Marks `PRD.md` and `ARCHITECTURE.md` as `APPROVED` and unlocks Step 2 (`/ntc-prototype`) or Step 3 (`/ntc-spec`).

---

## Mandatory Execution Sequence

### Phase 1.0: Git Repository Connection & Harness Bootstrap (BEFORE Anything Else)
1. **Ask for Git Repository URL & Basic Requirements (if not yet provided):**
   - **CRITICAL RULE:** Before doing any analysis or generating any specification, check if the user has provided:
     1. **Link Git Repo của dự án (`--repo`):** Để kết nối với dịch vụ Git (GitHub / GitLab / Bitbucket) ngay từ đầu *(ghi rõ người dùng có thể nhập URL hoặc để trống nếu chỉ làm local)*.
     2. **Ý tưởng / Yêu cầu cơ bản của dự án (`--idea`):** Mô tả ngắn gọn hệ thống muốn xây dựng.
   - If the user invoked `/ntc-init` without specifying whether they have a Git remote URL, **ask them for the Git Repo URL (can be left blank) + their basic requirements first**.
2. **Initialize Git & Connect Remote (`origin`):**
   - Check if `.git` exists in the workspace root (`git status`). If not, run `git init`.
   - If the user provided a non-empty Git repository URL:
     - Check `git remote -v`.
     - Run `git remote add origin <repo-url>` (or `git remote set-url origin <repo-url>` if `origin` already exists).
     - Report the connected remote URL clearly to the user.
   - If the user left the Git repository URL blank, initialize local `git init` and record `Repository Remote: Local-Only (no remote configured)` in `PRD.md` and `ARCHITECTURE.md`.
3. **Bootstrap Harness Directory Structure (if missing):**
   - Check if `AGENTS.md`, `docs/WORKFLOW.md`, and `scripts/validate_plans.py` exist in the workspace.
   - If missing, run the NTC Micro-Harness installer (`python install.py --target .`) or copy the template files into the workspace.

### Phase 1.1: Interactive Requirements Clarification (Q&A)
1. Analyze the user's basic requirements.
2. Formulate **3 to 5 concise, high-impact clarifying questions** (using `ask_question` tool if available, or structured bullet points) covering:
   - **Target Personas & Roles (RBAC):** Who uses the system and what permissions do they have?
   - **Core End-to-End Workflows:** What are the 2–3 most critical user journeys?
   - **UI Surface (`UI Required: YES | NO`):** Web app, Mobile app, Admin portal, or Backend/API/CLI only? What key screens are envisioned?
   - **Tech Stack & Data Persistence:** Preferred frontend framework, backend language/framework, database, and caching/queue tools.
   - **Scale, Security & Integrations:** Authentication method (JWT/OAuth2), third-party APIs, or deployment constraints.
3. **STOP and wait for the user's answers** before drafting `PRD.md` and `ARCHITECTURE.md`.

### Phase 1.2: Generate `PRD.md` & `ARCHITECTURE.md`
1. Once the user answers the clarifying questions, create:
   - **`PRD.md`** at the repository root (following `docs/templates/prd-template.md`):
     - Executive Vision & Problem Statement
     - Target Personas & Roles (`RBAC`)
     - In-Scope (`FEAT-<NN>`) & Out-of-Scope Capabilities
     - End-to-End User Journeys
     - Candidate UI Screens (`SCR-<MOD>-<NN>`) for Step 2 (if `UI Required: YES`)
     - Interactive Q&A Clarification Log
   - **`ARCHITECTURE.md`** at the repository root (following `docs/templates/architecture-template.md`):
     - High-Level System Topology (Mermaid diagram)
     - Technology Stack Matrix
     - Candidate Service / Module Decomposition (always including reserved `SYS` / `system` module for shared contracts, infra, and closing Full-Stack E2E)
     - Data Ownership, Security & Non-Functional Constraints
     - Technical Risks & Mitigations
2. If `UI Required: NO`, also set `> **UI Required:** NO` inside `docs/prototypes/registry.md`.

### Phase 1.3: Review & Approval Gate (Hard Stop)
- Present a concise summary of `PRD.md` and `ARCHITECTURE.md` to the user.
- **NEVER write production code in Step 1.**
- Instruct the user:
  - If they want adjustments, reply with their feedback.
  - Once satisfied:
    - If `UI Required: YES`, run **`/ntc-prototype`** to proceed to **Step 2 (Interactive UI Prototyping)**.
    - If `UI Required: NO`, run **`/ntc-spec`** to proceed directly to **Step 3 (Overall `SPEC.md` & Skill Mapping)**.
