#!/usr/bin/env python3
"""NTC Micro Harness v2.0 - Automated Project Installer.

Installs the Atomic Engineering Protocol (Microservices Edition v2.0) into any target
software project. Supports both local execution and zero-clone remote one-liner
execution right inside your project terminal.
"""

from __future__ import annotations

import argparse
import io
import shutil
import subprocess
import tempfile
import urllib.request
import zipfile
from pathlib import Path

HARNESS_VERSION = "2.0.0"
REPO_GIT_URL = "https://github.com/chien5572/ntc-micro-harness.git"
REPO_ZIP_URL = "https://github.com/chien5572/ntc-micro-harness/archive/refs/heads/main.zip"

AGENT_INTEGRATION_TEMPLATES = {
    "CLAUDE.md": """# Claude Code Instructions

<!-- HARNESS:BEGIN -->
Always adhere strictly to the Atomic Engineering Protocol defined in `AGENTS.md` and `docs/WORKFLOW.md`.
- Hierarchy of Truth: `SPEC.md` > `AGENTS.md` > `docs/plans/system-roadmap.md` > `docs/plans/contract-registry.md` > `docs/modules-spec/<slug>.md` > `ai-skill-maps.md` > `docs/plans/active/<slug>/phase-*.md`.
- Note: `STEP-by-STEP.md` is strictly for the Human Architect; AI Agents must NOT read it.
- Enforce the 5-Stage Gated Lifecycle: all `docs/modules-spec/*.md`, `ai-skill-maps.md`, and `STEP-by-STEP.md` are created in Gate 3; all Phase Dossiers across all modules are pre-generated in Gate 4 before any Gate 5 code is written.
- In Gate 5: 1 Turn = 1 Atomic Task. Perform 3-Step Crash Recovery on `"tiếp tục"`. Stop at the end of a phase and require `"tiếp tục phase <MOD>-P<NN+1>"` to archive and transition.
- Update the `🎫 Resume Ticket` and run `python scripts/validate_plans.py --fix` before yielding.
<!-- HARNESS:END -->
""",
    ".cursorrules": """# Cursor Agent Rules

<!-- HARNESS:BEGIN -->
Always adhere strictly to the Atomic Engineering Protocol defined in `AGENTS.md` and `docs/WORKFLOW.md`.
- Hierarchy of Truth: `SPEC.md` > `AGENTS.md` > `docs/plans/system-roadmap.md` > `docs/plans/contract-registry.md` > `docs/modules-spec/<slug>.md` > `ai-skill-maps.md` > `docs/plans/active/<slug>/phase-*.md`.
- Never read `STEP-by-STEP.md` (Human-Only Playbook).
- Never write production code before Gate 5 (all `docs/modules-spec/*.md` and all `docs/plans/active/<slug>/phase-*.md` must exist first).
- Implement exactly ONE Atomic Task per turn (`1 Turn = 1 Task`). Never output incomplete stubs.
- Update the `🎫 Resume Ticket` in the active dossier before concluding any turn.
<!-- HARNESS:END -->
""",
    ".windsurfrules": """# Windsurf Cascade Rules

<!-- HARNESS:BEGIN -->
Adhere strictly to the Atomic Engineering Protocol defined in `AGENTS.md` and `docs/WORKFLOW.md`.
- Read `SPEC.md`, `AGENTS.md`, and `ai-skill-maps.md` (do not read `STEP-by-STEP.md`).
- Maintain single-module boundaries, contract-first invariants, and the `"tiếp tục"` / `"tiếp tục phase ..."` state machine.
- Update the `🎫 Resume Ticket` and run `python scripts/validate_plans.py --fix` before yielding.
<!-- HARNESS:END -->
""",
}


def fetch_remote_harness(temp_dir: Path) -> Path:
    """Downloads the harness repository into temp_dir via git or HTTPS zip archive."""
    print(f"[*] Fetching NTC Micro Harness v{HARNESS_VERSION} from {REPO_GIT_URL} ...")
    clone_target = temp_dir / "ntc-micro-harness"
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", "--quiet", REPO_GIT_URL, str(clone_target)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return clone_target
    except Exception:
        print("  [.] Git clone unavailable, downloading ZIP archive over HTTPS...")
        with urllib.request.urlopen(REPO_ZIP_URL, timeout=30) as response:
            zip_bytes = response.read()
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
            zf.extractall(temp_dir)
        extracted_dirs = [p for p in temp_dir.iterdir() if p.is_dir() and (p / "AGENTS.md").exists()]
        if not extracted_dirs:
            raise RuntimeError("Failed to download and extract NTC Micro Harness archive.")
        return extracted_dirs[0]


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
        "modules-spec/README.md",
        "patterns/encoding-invariants.md",
        "plans/README.md",
        "plans/contract-registry.md",
        "plans/system-roadmap.md",
        "plans/active/README.md",
        "plans/completed/README.md",
        "templates/application-runbook.md",
        "templates/contract-registry-template.md",
        "templates/decision.md",
        "templates/exec-plan.md",
        "templates/module-spec-template.md",
        "templates/ai-skill-maps-template.md",
        "templates/step-by-step-template.md",
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

    # 3. Copy scripts/validate_plans.py
    src_script = source_root / "scripts" / "validate_plans.py"
    dst_script = target_root / "scripts" / "validate_plans.py"

    if src_script.exists():
        if not dst_script.exists() or force:
            dst_script.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_script, dst_script)
            print(f"  [+] Created {dst_script.relative_to(target_root)}")
        else:
            print(f"  [.] {dst_script.relative_to(target_root)} already exists (skipping)")

    # 4. Configure agent integration rules
    if agent_rules:
        for rule_file, rule_content in AGENT_INTEGRATION_TEMPLATES.items():
            if (
                "all" in agent_rules
                or rule_file.lstrip(".").split("rules")[0].lower() in agent_rules
                or rule_file.lower().startswith(tuple(agent_rules))
            ):
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
    print(f"SUCCESS: NTC Micro Harness v{HARNESS_VERSION} successfully installed!")
    print("=" * 65)
    print("Next Steps:")
    print("  1. Draft your system requirements at `SPEC.md` using `docs/templates/spec-template.md`.")
    print("  2. Start your AI Agent (Antigravity, Claude Code, Cursor, Windsurf) and prompt:")
    print('     "Read SPEC.md and AGENTS.md to perform Gate 1 & Gate 2."')
    print("  3. Validate and auto-sync planning documents at any time using:")
    print("     python scripts/validate_plans.py --fix\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Install NTC Micro Harness v2.0 into any software repository.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--target",
        "-t",
        type=Path,
        default=Path("."),
        help="Target project directory path (defaults to current working directory)",
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
    agent_selection = [] if "none" in args.agent else args.agent

    local_root = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
    if (local_root / "AGENTS.md").exists() and (local_root / "docs" / "WORKFLOW.md").exists():
        install_harness(
            source_root=local_root,
            target_root=args.target,
            agent_rules=agent_selection,
            force=args.force,
        )
    else:
        with tempfile.TemporaryDirectory(prefix="ntc-harness-") as tmp:
            remote_root = fetch_remote_harness(Path(tmp))
            install_harness(
                source_root=remote_root,
                target_root=args.target,
                agent_rules=agent_selection,
                force=args.force,
            )


if __name__ == "__main__":
    main()
