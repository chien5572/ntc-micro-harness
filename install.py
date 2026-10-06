#!/usr/bin/env python3
"""NTC Micro Harness - Automated Project Installer.

Installs the Atomic Engineering Protocol (Microservices Edition) into any target
software project. Sets up document hierarchies, templates, validation scripts,
and agent rule configurations for Antigravity, Claude Code, Cursor, and Windsurf.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

HARNESS_VERSION = "1.0.0"

AGENT_INTEGRATION_TEMPLATES = {
    "CLAUDE.md": """# Claude Code Instructions

<!-- HARNESS:BEGIN -->
Always adhere strictly to the Atomic Engineering Protocol defined in `AGENTS.md` and `docs/WORKFLOW.md`.
- Read `SPEC.md` and `AGENTS.md` first. Never start coding without an approved System Roadmap and Phase Dossier.
- Enforce the 5-Stage Gated Lifecycle and Single Atomic Task Turn (1 Turn = 1 Micro-task).
- Always verify work with executable proof before completing a task.
- Update the `🎫 Resume Ticket` before yielding your turn.
<!-- HARNESS:END -->
""",
    ".cursorrules": """# Cursor Agent Rules

<!-- HARNESS:BEGIN -->
Always adhere strictly to the Atomic Engineering Protocol defined in `AGENTS.md` and `docs/WORKFLOW.md`.
- Hierarchy of Truth: SPEC.md > AGENTS.md > docs/plans/system-roadmap.md > docs/plans/active/<module>/phase-*.md.
- Never write production code during Gate 1 (Specification Ingestion) or Gate 2 (Roadmap Alignment).
- Implement exactly ONE Atomic Task per turn. Never generate incomplete stubs (no TODOs).
- Update the `🎫 Resume Ticket` in the active dossier before concluding any turn.
<!-- HARNESS:END -->
""",
    ".windsurfrules": """# Windsurf Cascade Rules

<!-- HARNESS:BEGIN -->
Adhere strictly to the Atomic Engineering Protocol defined in `AGENTS.md` and `docs/WORKFLOW.md`.
- Read SPEC.md and AGENTS.md before taking any architectural actions.
- Maintain single-module boundaries and contract-first invariants.
- Update the `🎫 Resume Ticket` in the active phase dossier before yielding.
<!-- HARNESS:END -->
""",
}


def install_harness(
    source_root: Path,
    target_root: Path,
    agent_rules: list[str] | None = None,
    force: bool = False,
) -> None:
    """Installs the NTC Micro Harness files into the target project root."""
    target_root = target_root.resolve()
    print(f"[*] Installing NTC Micro Harness v{HARNESS_VERSION} into: {target_root}")

    if not target_root.exists():
        target_root.mkdir(parents=True, exist_ok=True)

    # 1. Install or merge AGENTS.md
    src_agents = source_root / "AGENTS.md"
    dst_agents = target_root / "AGENTS.md"

    if not dst_agents.exists() or force:
        shutil.copy2(src_agents, dst_agents)
        print(f"  [+] Created {dst_agents.relative_to(target_root)}")
    else:
        # Check if already has HARNESS block
        content = dst_agents.read_text(encoding="utf-8")
        if "<!-- HARNESS:BEGIN -->" in content:
            print(f"  [.] {dst_agents.name} already contains Harness block (skipping, use --force to overwrite)")
        else:
            harness_block = src_agents.read_text(encoding="utf-8")
            merged = content.rstrip() + "\n\n" + harness_block
            dst_agents.write_text(merged, encoding="utf-8")
            print(f"  [+] Appended Harness protocol block to existing {dst_agents.name}")

    # 2. Copy docs structure
    src_docs = source_root / "docs"
    dst_docs = target_root / "docs"

    docs_items = [
        "WORKFLOW.md",
        "README.md",
        "patterns/encoding-invariants.md",
        "plans/README.md",
        "plans/contract-registry.md",
        "plans/system-roadmap.md",
        "plans/active/README.md",
        "plans/completed/README.md",
        "plans/modules/README.md",
        "templates/application-runbook.md",
        "templates/contract-registry-template.md",
        "templates/decision.md",
        "templates/exec-plan.md",
        "templates/module-roadmap-template.md",
        "templates/phase-dossier-template.md",
        "templates/spec-template.md",
        "templates/system-roadmap-template.md",
    ]

    for rel_path in docs_items:
        s_file = src_docs / rel_path
        d_file = dst_docs / rel_path

        if not s_file.exists():
            continue

        if d_file.exists() and not force:
            print(f"  [.] {d_file.relative_to(target_root)} already exists (skipping)")
            continue

        d_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(s_file, d_file)
        print(f"  [+] Created {d_file.relative_to(target_root)}")

    # 3. Copy scripts/validate-plans.ps1
    src_scripts = source_root / "scripts" / "validate-plans.ps1"
    dst_scripts = target_root / "scripts" / "validate-plans.ps1"

    if src_scripts.exists():
        if not dst_scripts.exists() or force:
            dst_scripts.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_scripts, dst_scripts)
            print(f"  [+] Created {dst_scripts.relative_to(target_root)}")
        else:
            print(f"  [.] {dst_scripts.relative_to(target_root)} already exists (skipping)")

    # 4. Configure agent integration rules
    if agent_rules:
        for rule_file, rule_content in AGENT_INTEGRATION_TEMPLATES.items():
            if "all" in agent_rules or rule_file.lstrip(".").split("rules")[0].lower() in agent_rules or rule_file.lower().startswith(tuple(agent_rules)):
                dst_rule = target_root / rule_file
                if not dst_rule.exists() or force:
                    dst_rule.write_text(rule_content, encoding="utf-8")
                    print(f"  [+] Configured agent rule: {rule_file}")
                else:
                    existing = dst_rule.read_text(encoding="utf-8")
                    if "<!-- HARNESS:BEGIN -->" not in existing:
                        dst_rule.write_text(existing.rstrip() + "\n\n" + rule_content, encoding="utf-8")
                        print(f"  [+] Appended harness rule to: {rule_file}")

    print("\n" + "=" * 65)
    print("SUCCESS: NTC Micro Harness successfully installed!")
    print("=" * 65)
    print("Next Steps:")
    print("  1. Draft your project requirements at `SPEC.md` using `docs/templates/spec-template.md`.")
    print("  2. Start your AI Agent (Antigravity, Claude Code, Cursor, Windsurf) and prompt:")
    print('     "Read SPEC.md and AGENTS.md to collaboratively build our System Roadmap."')
    print("  3. Validate planning documents at any time using:")
    print("     powershell -ExecutionPolicy Bypass -File scripts/validate-plans.ps1\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Install NTC Micro Harness into any software repository.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--target",
        "-t",
        type=Path,
        default=Path("."),
        help="Target project directory path",
    )
    parser.add_argument(
        "--agent",
        "-a",
        nargs="+",
        choices=["all", "claude", "cursor", "windsurf", "none"],
        default=["all"],
        help="AI assistant rule files to configure (all, claude, cursor, windsurf, none)",
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Overwrite existing files even if they already exist",
    )

    args = parser.parse_args()
    source_root = Path(__file__).resolve().parent

    agent_selection = [] if "none" in args.agent else args.agent
    install_harness(
        source_root=source_root,
        target_root=args.target,
        agent_rules=agent_selection,
        force=args.force,
    )


if __name__ == "__main__":
    main()
