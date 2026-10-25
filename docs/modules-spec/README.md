# Detailed Module Specifications (`docs/modules-spec/`)

One detailed specification file per module (service/application), instantiated during **Gate 3 (Step 3.1)** from `docs/templates/module-spec-template.md`:

```text
docs/modules-spec/<module-slug>.md
```

Each file in `docs/modules-spec/` serves two unified roles:
1. **Detailed Module Specification:** Linked directly to root `SPEC.md`, `docs/plans/contract-registry.md`, and `docs/prototypes/registry.md` (for UI modules). Defines scope boundaries, user stories, tech stack, exact database/storage DDL schemas, provided/consumed contracts (`CT-<MOD>-<NN>`), UI screen & prototype mappings (`SCR-<MOD>-<NN>`), core business flows & state machines, stage-by-stage **Given/When/Then** acceptance criteria, and error codes.
2. **Module Phase Sequence (`## 9. Module Phase Sequence`):** Defines all planned phases (`<MOD>-P<NN>`) for the module, aligned to Global Phases (`GP-<NN>`), tracking their status (`PENDING` | `ACTIVE` | `BLOCKED` | `COMPLETED`) and linking to their Phase Dossiers in `docs/plans/active/<module-slug>/` or `docs/plans/completed/<module-slug>/`.

## Rules

- `<module-slug>` (lowercase kebab-case) and `<MOD>` (2–5 uppercase letters) are assigned once in the Module Registry of `docs/plans/system-roadmap.md` and never reused.
- `system.md` (`SYS`) is reserved for cross-cutting work: shared contract packages, local orchestration, CI, gateway (unless it is its own service), and end-to-end tests.
- **All registered modules** must have their `docs/modules-spec/<module-slug>.md` authored and aligned during Gate 3 before `ai-skill-maps.md`, `STEP-by-STEP.md`, or any Phase Dossier (Gate 4) is created.
- Phase dossiers never live here: they live in `docs/plans/active/<module-slug>/` and move to `docs/plans/completed/<module-slug>/` upon phase completion.
