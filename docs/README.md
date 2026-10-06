# Documentation Map

Start with the smallest authoritative surface.

## Current Product

- `WORKFLOW.md`: the 5-stage gated lifecycle (SPEC → Project Roadmap → Module
  Blueprint → Module Phase Dossier → Atomic Implementation), identifier
  convention, cross-module contract protocol, resume, and archival.
- `ARCHITECTURE.md`: current product, code, state, update, and ownership
  boundaries.
- `HARNESS.md`: product principles and installed-core model.
- `product/`: current product behavior and installation contract.
- `decisions/`: lasting choices future work must inherit.
- `plans/`: layered working memory —
  - `plans/system-roadmap.md`: Project Roadmap (Global Phases, Module
    Registry, dependency graph, Active Work Pointer);
  - `plans/contract-registry.md`: cross-module contracts;
  - `plans/modules/<module>.md`: one Module Blueprint per service;
  - `plans/active/<module>/`: phase dossiers in progress;
  - `plans/completed/<module>/`: verified, archived phase dossiers.
- [`patterns/encoding-invariants.md`](patterns/encoding-invariants.md): turn
  accepted architecture, reliability, security, and quality rules into native
  mechanical validation.
- `templates/`: spec, project roadmap, contract registry, module blueprint,
  phase dossier, exec plan, decision, and runbook structures (runbooks may be
  instantiated per module).
- `../scripts/validate-plans.ps1`: structural validation of the planning
  hierarchy.

## Consumer-Owned Truth

The consumer's README, product documents, architecture, code, tests, CI,
runtime signals, and application behavior remain authoritative. Harness does
not overwrite those with upstream product assumptions.

## Source Repository

- Root `README.md`: product overview, installation, maintenance, EOL, and
  development.
- `crates/harness/`: safe core installer/updater.
- `scripts/`: platform bootstrap, release, and validation entrypoints.
- `tests/`: behavior ownership and repository contract.

## History

The former SQLite control plane, protocol v1, story packets, migration evidence,
and compatibility documentation are preserved by Git history and immutable
`harness-cli-v*` tags. They are intentionally absent from the current tree so
search and agent retrieval return current product authority.
