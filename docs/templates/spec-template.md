# Product & System Specification: <Project Name>

> **Guidance:** This document serves as the supreme Single Source of Truth (SPEC) for the project.  
> You can copy this structure into web reasoning models (Claude Opus, ChatGPT o3, Gemini Pro) to thoroughly refine your system specification before committing it to the repository.

---

## 1. Executive Summary & Vision
- **Project / System Name:**
- **Core Problem Statement:** What problem does this system exist to solve?
- **Target Audience & Stakeholders:** Who will interact with or rely on this system?
- **Success Metrics & Key Results (KPIs):**

## 2. System Architecture & Tech Stack
- **Architecture Pattern:** (Modular Monolith / Microservices / Clean Architecture / Event-Driven / Hexagonal)
- **Language & Runtime:** (e.g., Node.js / TypeScript, Python 3.12+, Golang, Rust)
- **Primary Frameworks & Libraries:**
- **Databases & Persistence:** (e.g., PostgreSQL, Redis, S3-compatible Object Storage)
- **Communication Protocols & APIs:** (REST / gRPC / GraphQL / WebSockets / Message Queues)

## 3. Scope & System Boundaries
### In-Scope (Mandatory Deliverables):
- [ ] Core Capability A
- [ ] Core Capability B
- [ ] Core Capability C

### Out-of-Scope (Strictly Forbidden in this Cycle):
- [ ] Non-essential features (preventing scope creep)
- [ ] Premature third-party integrations

## 4. Domain Data Models & Entities
*(Define core domain entities, data relationships, and schema boundaries)*
- **Entity 1:** Attributes, constraints, foreign keys
- **Entity 2:** Attributes, constraints, relationships

## 5. Core User Flows & API Contracts
*(Step-by-step description from request ingress to state mutation and response)*
- **Flow 1: [Flow Name - e.g., User Registration & Verification]**
  1. Input Payload:
  2. Business Invariants & Processing:
  3. Resulting State & Output:
- **Flow 2: [Flow Name]**

## 6. Non-Functional Requirements
- **Performance & Throughput:** (Latency targets, p99 requirements, concurrency limits)
- **Security & Access Control:** (JWT, RBAC, OAuth2, Rate Limiting, Encryption at rest/transit)
- **Resilience & Fault Tolerance:** (Retry policies, circuit breakers, idempotency)
- **Observability:** (Structured logging, distributed tracing, metric counters)

## 7. Service / Module Decomposition
*(Candidate modules. The Agent refines these into the Module Registry during Gate 2. `system` / `SYS` is reserved for cross-cutting work.)*

| Proposed Code | Module | Responsibility | Owned Data | Provides | Consumes | Sync / Async |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `SYS` | system | Shared contracts, local infra, CI, gateway, E2E | — | Shared libraries | — | — |
| `AUTH` | auth | Identity & tokens | users, credentials | Token issuance / introspection | — | REST, gRPC |
| `...` | ... | ... | ... | ... | ... | ... |

- **Code Layout Hint:** (e.g. monorepo `services/<slug>/`, polyrepo, shared `contracts/` directory)
- **Contract Formats:** (OpenAPI, Protobuf, AsyncAPI / JSON Schema, typed DTO package)

## 8. Delivery Roadmap Hints
### Global Phases (project level)
- **GP-01 (Foundation & Contracts):** Repo scaffolding, local infra, shared contracts codified.
- **GP-02 (Core Domain Services):** Primary business logic of each service.
- **GP-03 (Integration & Async Flows):** Events, workers, cross-service flows, third-party webhooks.
- **GP-04 (Hardening & Release):** E2E tests, load testing, security review.

### Per-Module Hints
- **AUTH:** P01 contracts & schema → P02 token logic → P03 introspection API.
- **...:**
