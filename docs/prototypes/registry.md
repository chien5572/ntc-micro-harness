# UI Prototype & Design System Registry: <Project Name>

> **UI Required:** NO  
> **Status:** N/A  
> **Authority:** Created during **Step 2 (`/ntc-prototype`)** from `PRD.md` and `ARCHITECTURE.md`; must be **APPROVED** by the Human Architect (`/ntc-prototype --approve`) before locking the overall `SPEC.md` (Step 3 `/ntc-spec`), Detailed Module Specs (Step 4 `/ntc-modules`), or Phase Dossiers (Step 5 `/ntc-plan`).  
> **Last Synchronized:** 2026-04-12  

<!--
STRUCTURE INVARIANTS (checked by scripts/validate_plans.py):
- Keep the headings "## 1. Design System & Visual Tokens", "## 2. UI Screen & Prototype Registry", and "## 3. Prototype Sign-Off & Change Log".
- Keep table header names in Section 2 unchanged: Screen ID | Module | Screen Name | Prototype Path | States Covered | Consumed Contracts | Status
- Screen ID format: SCR-<MOD>-<NN>; <MOD> must equal the Module column and be a registered module code in docs/plans/system-roadmap.md.
- Prototype Path: must point to a self-contained HTML file under docs/prototypes/<module-slug>/scr-<nn>-<slug>.html.
- Status: DRAFT | APPROVED | DEPRECATED.
  - When Status is APPROVED, the HTML file at Prototype Path MUST exist on disk and MUST include `data-testid="..."` attributes on key interactive/layout elements.
  - Before any Phase Dossier (Step 5 / Step 6) is created for <MOD>, all active screens for <MOD> must be APPROVED (never DRAFT).
-->

---

## 1. Design System & Visual Tokens

*(If `UI Required: YES`, define the locked visual foundation here during Step 2 `/ntc-prototype`. AI Agents in Step 6 `/ntc-run` MUST copy these exact tokens/classes and NEVER improvise alternative palettes or typography.)*

- **Styling Engine / Strategy:** —
- **Color Palette (Exact Hex / CSS Variables):** —
- **Typography:** —
- **Layout Shell & Breakpoints:** —
- **Mandatory `data-testid` & State Parity Rule:**
  1. Every HTML prototype in `docs/prototypes/<module-slug>/` MUST include `data-testid="scr-<nn>-<element>"` on its root container, forms, inputs, action buttons, data tables/lists, and state views (`default`, `loading`, `empty`, `error`).
  2. During Step 6 (`/ntc-run`) implementation, AI Agents MUST preserve the exact DOM hierarchy, CSS/Tailwind classes, and `data-testid` attributes 1:1 when porting to production framework components.

---

## 2. UI Screen & Prototype Registry

| Screen ID | Module | Screen Name | Prototype Path | States Covered | Consumed Contracts | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| *[None yet]* | | | | | | |

**Status values:** `DRAFT` | `APPROVED` | `DEPRECATED`

---

## 3. Prototype Sign-Off & Change Log

*(Append-only. Once a screen is `APPROVED`, any layout or flow modification requires updating the HTML prototype first and logging Human Architect approval below before changing production code.)*

| Date | Screen ID | Version | Approved By | Summary of Visual / Flow Lock |
| :--- | :--- | :--- | :--- | :--- |
| — | — | — | — | — |
