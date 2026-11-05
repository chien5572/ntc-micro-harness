# Product Requirements Document (PRD): <Project Name>

> **Generated via `/ntc-init` (Step 1 — Interactive Discovery & Requirements Refinement)**  
> This document captures the product vision, user roles, core user journeys, functional requirements, and screen candidates refined through interactive Q&A between the Human Architect and the AI Agent.  
> Once approved, this PRD (together with `ARCHITECTURE.md`) drives **Step 2 (`/ntc-prototype`)** and **Step 3 (`/ntc-spec`)**.

- **Project Name:** `<Project Name>`
- **Repository URL (Git Remote):** `<https://github.com/org/repo.git | Local-Only>`
- **UI Required:** `YES | NO`
- **Document Status:** `DRAFT | APPROVED`

---

## 1. Executive Vision & Problem Statement
- **Problem Statement:** What core problem does this product solve, and why do existing solutions fall short?
- **Product Vision:** One-paragraph summary of the target outcome.
- **Success Metrics (KPIs):**
  - *Metric 1:* (e.g., Core workflow completion time < 30s)
  - *Metric 2:* (e.g., 99.9% transaction reliability)

## 2. Target Personas & Roles (RBAC)
| Role Code | Persona / Role Name | Description & Core Permissions | Primary Interface |
| :--- | :--- | :--- | :--- |
| `GUEST` | Unauthenticated Visitor | Sign up, sign in, view public landing/docs | Web / Public API |
| `USER` | Standard Authenticated User | Access core product workflows and personal workspace | Web / Mobile App |
| `ADMIN` | System Administrator | Manage users, configurations, audit logs, and billing | Admin Portal |

## 3. Core User Stories & Functional Scope

### 3.1 In-Scope Functional Capabilities (MVP / Current Cycle)
| Feature ID | Feature / Capability | User Story (*As a ... I want ... So that ...*) | Priority | Candidate Module |
| :--- | :--- | :--- | :--- | :--- |
| `FEAT-01` | Identity & Access | As a `USER`, I want to sign in securely so that my workspace is protected. | `P0` | `AUTH` (`auth`) |
| `FEAT-02` | Core Domain Workflow | As a `USER`, I want to create and track items so that I can fulfill the primary business goal. | `P0` | `CORE` (`core`) |
| `FEAT-03` | Interactive UI Portal | As a `USER`, I want a responsive web dashboard to manage my workflows visually. | `P0` | `WEB` (`web`) |

### 3.2 Out-of-Scope (Explicitly Deferred)
- [ ] Out-of-scope capability 1 (preventing scope creep)
- [ ] Out-of-scope capability 2

## 4. End-to-End User Journeys
### Journey 1: [Primary User Flow Name]
1. **Trigger & Entry Point:** User navigates to `<screen/endpoint>`.
2. **Main Steps:**
   - Step A: ...
   - Step B: ...
3. **Expected Outcome & State Change:** ...
4. **Failure / Edge Cases:** Invalid input, network timeout, permission denied.

## 5. Candidate UI Screens & Visual Flows (For Step 2: `/ntc-prototype`)
*(Populate when `UI Required: YES`. These screens will be built as interactive HTML/CSS prototypes in `docs/prototypes/<module-slug>/scr-<nn>-*.html` during Step 2).*

| Candidate Screen ID | UI Module | Screen Name | Target Roles | Key UI Components, States & Actions |
| :--- | :--- | :--- | :--- | :--- |
| `SCR-WEB-01` | `WEB` | Sign In / Onboarding | `GUEST` | Email/password form, validation errors, OAuth buttons, loading spinner |
| `SCR-WEB-02` | `WEB` | Main Dashboard | `USER`, `ADMIN` | KPI summary cards, filterable data table, empty state CTA, create modal |

## 6. Interactive Q&A Clarification Log
*(Recorded from `/ntc-init` discovery session)*
- **Q1:** ... → **Decision:** ...
- **Q2:** ... → **Decision:** ...
- **Q3:** ... → **Decision:** ...
