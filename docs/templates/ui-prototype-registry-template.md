# UI Prototype & Design System Registry: <Project Name>

> **UI Required:** YES | NO  
> **Status:** APPROVED | IN_REVIEW | DRAFT | N/A  
> **Authority:** Created during **Gate 3 (Step 3.0)** from `SPEC.md` and `docs/plans/system-roadmap.md`; must be **APPROVED** by the Human Architect before authoring Detailed Module Specs (Step 3.1) or Phase Dossiers (Gate 4).  
> **Last Synchronized:** YYYY-MM-DD  

<!--
STRUCTURE INVARIANTS (checked by scripts/validate_plans.py):
- Keep the headings "## 1. Design System & Visual Tokens", "## 2. UI Screen & Prototype Registry", and "## 3. Prototype Sign-Off & Change Log".
- Keep table header names in Section 2 unchanged: Screen ID | Module | Screen Name | Prototype Path | States Covered | Consumed Contracts | Status
- Screen ID format: SCR-<MOD>-<NN>; <MOD> must equal the Module column and be a registered module code in docs/plans/system-roadmap.md.
- Prototype Path: must point to a self-contained HTML file under docs/prototypes/<module-slug>/scr-<nn>-<slug>.html.
- Status: DRAFT | APPROVED | DEPRECATED.
  - When Status is APPROVED, the HTML file at Prototype Path MUST exist on disk and MUST include `data-testid="..."` attributes on key interactive/layout elements.
  - Before any Phase Dossier (Gate 4/5) is created for <MOD>, all active screens for <MOD> must be APPROVED (never DRAFT).
-->

---

## 1. Design System & Visual Tokens

*(Locked visual foundation shared across all prototypes and production UI components. AI Agents in Gate 5 MUST copy these exact tokens/classes and NEVER improvise alternative palettes or typography.)*

- **Styling Engine / Strategy:** (e.g., Tailwind CSS v3/v4, CSS Variables, Shadcn UI tokens)
- **Color Palette (Exact Hex / CSS Variables):**
  - Primary / Brand: `--color-primary: #2563EB`
  - Secondary / Accent: `--color-accent: #0F172A`
  - Background / Surface: `--color-bg: #F8FAFC`, `--color-surface: #FFFFFF`
  - Semantic States: Success `#16A34A` | Warning `#D97706` | Danger `#DC2626`
- **Typography:**
  - Heading Font: `Inter`, `600/700`
  - Body Font: `Inter`, `400/500`
  - Monospace Font: `JetBrains Mono`
- **Layout Shell & Breakpoints:**
  - Navigation Pattern: (e.g., Left collapsible sidebar `260px` + sticky topbar `64px` + scrollable main container `max-w-7xl`)
  - Spacing & Border Radius: Base unit `4px`, card radius `rounded-xl` (`12px`), control radius `rounded-lg` (`8px`)
- **Mandatory `data-testid` & State Parity Rule:**
  1. Every HTML prototype in `docs/prototypes/<module-slug>/` MUST include `data-testid="scr-<nn>-<element>"` on its root container, forms, inputs, action buttons, data tables/lists, and state views (`default`, `loading`, `empty`, `error`).
  2. During Gate 5 implementation, AI Agents MUST preserve the exact DOM hierarchy, CSS/Tailwind classes, and `data-testid` attributes 1:1 when porting to production framework components.

---

## 2. UI Screen & Prototype Registry

| Screen ID | Module | Screen Name | Prototype Path | States Covered | Consumed Contracts | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `SCR-WEB-01` | `WEB` | Login & MFA Challenge | `docs/prototypes/web/scr-01-login.html` | `default, loading, error` | `CT-AUTH-01` | `APPROVED` |
| `SCR-WEB-02` | `WEB` | Order Management Dashboard | `docs/prototypes/web/scr-02-orders.html` | `default, loading, empty, error` | `CT-ORD-01` | `DRAFT` |

**Status values:** `DRAFT` | `APPROVED` | `DEPRECATED`

---

## 3. Prototype Sign-Off & Change Log

*(Append-only. Once a screen is `APPROVED`, any layout or flow modification requires updating the HTML prototype first and logging Human Architect approval below before changing production code.)*

| Date | Screen ID | Version | Approved By | Summary of Visual / Flow Lock |
| :--- | :--- | :--- | :--- | :--- |
| YYYY-MM-DD | `SCR-WEB-01` | `1.0.0` | Human Architect | Initial layout, validation states, and `data-testid` hooks locked |
