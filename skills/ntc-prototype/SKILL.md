---
name: ntc-prototype
description: "Step 2 of NTC Micro-Harness (/ntc-prototype): Generate, iterate, and lock self-contained interactive HTML/CSS UI prototypes (docs/prototypes/<slug>/scr-<nn>-*.html) with 4 visual states and data-testid hooks based on PRD.md and ARCHITECTURE.md."
---

# `/ntc-prototype` — Step 2: Interactive UI Prototyping & Visual Sign-Off (`docs/prototypes/`)

Activate this skill whenever the user invokes **`/ntc-prototype`** (Step 2 of the NTC Micro-Harness workflow).

## Pre-Conditions
1. `PRD.md` and `ARCHITECTURE.md` must exist at the repository root (created in Step 1 via `/ntc-init`).
2. If `PRD.md` specifies `UI Required: NO`:
   - Set `> **UI Required:** NO` in `docs/prototypes/registry.md`.
   - Inform the user that UI prototyping is skipped for headless/backend-only systems and prompt them to run **`/ntc-spec`** (Step 3).

## Supported Flags & Arguments
- *(No flags)*: Generate all candidate screens from `PRD.md` and `ARCHITECTURE.md` into `docs/prototypes/registry.md` and `docs/prototypes/<module-slug>/scr-<nn>-<slug>.html`.
- `--screen <SCR-MOD-NN>`: Create or regenerate only a specific screen prototype (e.g., `/ntc-prototype --screen SCR-WEB-01`).
- `--revise "<feedback>"`: Modify existing HTML prototype(s) or Design System Tokens based on user feedback, and record a revision row in Section 3 (`Prototype Revision & Change Log`) of `docs/prototypes/registry.md`.
- `--approve`: Mark all active screens in `docs/prototypes/registry.md` as `APPROVED`, verify that every file exists on disk and contains `data-testid=` attributes, and unlock **Step 3 (`/ntc-spec`)**.

---

## Mandatory Execution Sequence

### 1. Lock Design System Tokens & Screen Inventory (`docs/prototypes/registry.md`)
Read `PRD.md` (Section 5: Candidate UI Screens) and `ARCHITECTURE.md`, then populate **`docs/prototypes/registry.md`** (using `docs/templates/ui-prototype-registry-template.md`):
- Set `> **UI Required:** YES`.
- Define exact **Design System Tokens** in Section 1:
  - Color palette (Primary, Secondary, Surface, Text, Semantic Status colors)
  - Typography (Font families, scale, weights)
  - Spacing, border radius, shadows, and responsive layout shell
- Register every screen in Section 2 (`## 2. UI Screen & Prototype Registry`) with:
  - `Screen ID`: `SCR-<MOD>-<NN>` (e.g., `SCR-WEB-01`)
  - `Module`: `<MOD>` (e.g., `WEB`)
  - `Prototype Path`: `docs/prototypes/<module-slug>/scr-<nn>-<screen-slug>.html`
  - `States Covered`: `default, loading, empty, error`
  - `Consumed Contracts`: Candidate `CT-<PROVIDER>-<NN>` IDs
  - `Status`: `DRAFT` (until explicitly approved by the user)

### 2. Generate Self-Contained Interactive HTML/CSS Prototypes (`docs/prototypes/<module-slug>/scr-<nn>-*.html`)
For each registered screen, create a rich, standalone HTML file that the user can open directly in any browser:
- **Zero Build Step:** Use inline CSS or Tailwind CDN + lightweight vanilla JS.
- **Interactive State Switcher Bar:** Include a floating/top switcher bar in the HTML prototype that lets the Human Architect click to preview all 4 mandatory states:
  1. `default` (populated with realistic domain data exposing all fields needed from backend contracts)
  2. `loading` (skeleton loaders / spinners)
  3. `empty` (zero-data illustration + primary call-to-action)
  4. `error` (error banner / retry state / form validation errors)
- **Mandatory `data-testid` Anchors:** Attach explicit `data-testid="scr-<nn>-<element>"` attributes to all key DOM containers, forms, inputs, tables, modals, and action buttons (e.g., `data-testid="scr-01-login-form"`, `data-testid="scr-01-submit-btn"`). These anchors are mechanically enforced by `scripts/validate_plans.py` and ported 1:1 in Step 6.

### 3. Iterate & Lock (`--revise` / `--approve`)
- After generating or revising prototypes, present clickable file links to `docs/prototypes/<module-slug>/scr-<nn>-*.html` and `docs/prototypes/registry.md`.
- **Hard Stop:** Do NOT generate `SPEC.md` or advance to Step 3 while screens are still `DRAFT`.
- When the user runs **`/ntc-prototype --approve`** (or confirms visual approval):
  1. Update every screen's `Status` in `docs/prototypes/registry.md` from `DRAFT` to **`APPROVED`**.
  2. Verify every approved `.html` file exists on disk and contains `data-testid=`.
  3. Announce that all UI prototypes are locked (`APPROVED`) and instruct the user to run **`/ntc-spec`** to start **Step 3 (Overall `SPEC.md` + Skill Mapping)**.
