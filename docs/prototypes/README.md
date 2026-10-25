# UI Prototypes & Visual Contracts (`docs/prototypes/`)

When a project includes any user-facing interface (Web, Mobile, Desktop, Admin Portal), `docs/prototypes/` serves as the **Single Source of Visual Truth** generated and approved during **Gate 3 — Step 3.0 (Conditional UI Prototyping & Visual Sign-Off)**.

```text
docs/prototypes/
├── README.md                                     <-- This guide
├── registry.md                                   <-- UI Prototype & Design System Registry (SCR-<MOD>-<NN>)
└── <module-slug>/
    ├── scr-01-<screen-slug>.html                 <-- Self-contained interactive HTML/CSS prototype
    └── scr-02-<screen-slug>.html                 <-- Self-contained interactive HTML/CSS prototype
```

## Why UI Prototypes Are Locked in Gate 3.0

1. **Prevent Gate 4/5 WBS Thrashing:** Approving clickable, visual HTML prototypes before writing Detailed Module Specs (`Step 3.1`) and Phase Dossiers (`Gate 4`) prevents mid-implementation layout rewrites.
2. **Shape Accurate Backend Contracts (`CT-*`):** Seeing the exact tables, filters, forms, modals, and empty/error states in `scr-<nn>-*.html` ensures `docs/plans/contract-registry.md` and `docs/modules-spec/<slug>.md` include every required request/response field.
3. **1:1 Visual & DOM Lock for AI Agents in Gate 5:** AI agents in Gate 5 are **strictly forbidden** from inventing layouts or improvising styles. They must read the approved `docs/prototypes/<module-slug>/scr-<nn>-*.html` file referenced in the active Atomic Task and port its DOM structure, CSS/Tailwind classes, visual states, and `data-testid` attributes **1:1** into the production framework.

## Rules Enforced by `scripts/validate_plans.py`

- Every UI screen is registered in `docs/prototypes/registry.md` with ID `SCR-<MOD>-<NN>` where `<MOD>` is a registered module code in `docs/plans/system-roadmap.md`.
- When a screen's status is `APPROVED`, its `Prototype Path` (`docs/prototypes/<module-slug>/scr-<nn>-*.html`) **must exist on disk** and **must contain `data-testid="..."` attributes** on key layout and interactive elements.
- **Gate 4/5 Lock:** No Phase Dossier may be created or executed for `<MOD>` while any of `<MOD>`'s screens in `docs/prototypes/registry.md` remain in `DRAFT` status.
- For backend-only / headless systems (`UI Required: NO`), leave the table in `docs/prototypes/registry.md` at its default placeholder row.
