# Cross-Module Contract Registry: <Project Name>

> **Status:** APPROVED | IN_REVIEW | DRAFT  
> **Authority:** Derived from `docs/plans/system-roadmap.md`; changes follow the Contract Protocol in `docs/WORKFLOW.md` §3.  
> **Last Synchronized:** YYYY-MM-DD  

<!--
STRUCTURE INVARIANTS (checked by scripts/validate-plans.ps1):
- Keep the headings "## 1. Contracts" and "## 2. Contract Change Log" and the table header names.
- Contract ID format: CT-<PROVIDER>-<NN>; <PROVIDER> must equal the Provider column and be a registered module code.
- Consumers: comma-separated registered module codes (or —).
- Status: DRAFT | AVAILABLE | DEPRECATED. An AVAILABLE contract's Spec Path must exist in the repository.
-->

---

## 1. Contracts

| Contract ID | Type | Provider | Consumers | Spec Path | Version | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `CT-AUTH-01` | REST | `AUTH` | `SYS` | `contracts/openapi/auth-public.yaml` | `1.0.0` | `AVAILABLE` |
| `CT-AUTH-02` | gRPC | `AUTH` | `ORD` | `contracts/proto/auth/token_introspection.proto` | `1.0.0` | `DRAFT` |
| `CT-ORD-02` | Event | `ORD` | — | `contracts/events/order-created.schema.json` | `0.1.0` | `DRAFT` |

**Type values:** REST | gRPC | Event | Schema | Library

---

## 2. Contract Change Log
*(Append-only. Breaking changes require explicit Human Architect approval and a decision record before implementation.)*

| Date | Contract ID | Version | Breaking | Impacted Consumers | Decision / Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| YYYY-MM-DD | `CT-AUTH-01` | `—` → `1.0.0` | No | `SYS` | Initial codification (`AUTH-P01.1.1`) |
