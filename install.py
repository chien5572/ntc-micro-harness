#!/usr/bin/env python3
"""NTC Micro-Harness v2.1 (Plugin Edition) - Automated Project & Antigravity Plugin Installer.

Installs the 6-Step Atomic Engineering Protocol & `/ntc-*` Plugin into:
  1. Global Antigravity Plugin directory (`~/.gemini/config/plugins/ntc-micro-harness/`)
     for Antigravity 2.0, Antigravity IDE, and Antigravity CLI (`agy`).
  2. Target project workspace (`AGENTS.md`, `docs/`, `scripts/validate_plans.py`,
     `.agents/skills/ntc-*/SKILL.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`).
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

HARNESS_VERSION = "2.1.0"
REPO_GIT_URL = "https://github.com/chien5572/ntc-micro-harness.git"
REPO_ZIP_URL = "https://github.com/chien5572/ntc-micro-harness/archive/refs/heads/main.zip"

NTC_SKILLS = [
    "ntc-init",
    "ntc-prototype",
    "ntc-spec",
    "ntc-modules",
    "ntc-plan",
    "ntc-run",
    "ntc-cr",
    "ntc-status",
]

AGENT_INTEGRATION_TEMPLATES = {
    "CLAUDE.md": """# Claude Code Instructions

<!-- HARNESS:BEGIN -->
Always adhere strictly to the 6-Step Atomic Engineering Protocol defined in `AGENTS.md` and `docs/WORKFLOW.md`.
- Hierarchy of Truth: `PRD.md` & `ARCHITECTURE.md` (Step 1 `/ntc-init`) > `docs/prototypes/registry.md` (Step 2 `/ntc-prototype`) > `SPEC.md` > `AGENTS.md` > `docs/plans/system-roadmap.md` > `docs/plans/contract-registry.md` > `ai-skill-maps.md` (Step 3 `/ntc-spec`) > `docs/modules-spec/<slug>.md` (Step 4 `/ntc-modules`) > `docs/plans/active/<slug>/phase-*.md` (Step 5 `/ntc-plan`).
- Note: `STEP-by-STEP.md` is strictly for the Human Architect; AI Agents must NOT read it.
- Step 1 (`/ntc-init`): Always ask for the Project Git Repository URL (optional — can be left blank) first to initialize `git init` and connect `git remote add origin <repo-url>` before asking clarifying Q&A and generating `PRD.md` + `ARCHITECTURE.md`.
- Step 2 (`/ntc-prototype`): Build interactive HTML/CSS prototypes (`docs/prototypes/<slug>/scr-*.html` with `data-testid` anchors) from `PRD.md` + `ARCHITECTURE.md` and wait for `--approve` (`APPROVED`).
- Step 3 (`/ntc-spec`): Lock overall `SPEC.md` + `system-roadmap.md` + `contract-registry.md`, then map and install AI skills per module into `.agents/skills/` and `ai-skill-maps.md`.
- Step 4 (`/ntc-modules`): Read `ai-skill-maps.md` + `SPEC.md` + approved prototypes to author `docs/modules-spec/<slug>.md` for all modules, then generate `STEP-by-STEP.md`.
- Step 5 (`/ntc-plan`): Pre-generate all Phase Dossiers across all modules before any production code is written.
- Step 6 (`/ntc-run` / `"tiếp tục"`): 1 Turn = 1 Atomic Task. Enforce 1:1 UI Prototype Parity (`SCR-<MOD>-<NN>`), update `🎫 Resume Ticket`, run `python scripts/validate_plans.py --fix`, and create an Atomic Git Commit checkpoint (`HEAD`). Handle mid-flight changes via `/ntc-cr` (`CR-<NN>`).
<!-- HARNESS:END -->
""",
    ".cursorrules": """# Cursor Agent Rules

<!-- HARNESS:BEGIN -->
Always adhere strictly to the 6-Step Atomic Engineering Protocol defined in `AGENTS.md` and `docs/WORKFLOW.md`.
- Slash Commands: `/ntc-init` (Step 1: Git remote + Q&A -> `PRD.md` & `ARCHITECTURE.md`) -> `/ntc-prototype` (Step 2: HTML UI Prototypes `SCR-<MOD>-<NN>`) -> `/ntc-spec` (Step 3: Overall `SPEC.md` + `ai-skill-maps.md`) -> `/ntc-modules` (Step 4: `docs/modules-spec/<slug>.md` + `STEP-by-STEP.md`) -> `/ntc-plan` (Step 5: All Phase Dossiers WBS) -> `/ntc-run` (Step 6: `1 Turn = 1 Atomic Task`).
- Never read `STEP-by-STEP.md` (Human-Only Playbook).
- Implement exactly ONE Atomic Task per turn (`1 Turn = 1 Task`). For UI tasks, port the approved `SCR-<MOD>-<NN>` HTML prototype 1:1 (including `data-testid` hooks). Never output incomplete stubs.
- Update the `🎫 Resume Ticket`, run `python scripts/validate_plans.py --fix`, and create an Atomic Git Commit checkpoint before concluding any turn.
- On `/ntc-cr` or `"yêu cầu thay đổi: ..."`, follow the `CR-<NN>` 4-Step Delta Reverse-Unlock Protocol.
<!-- HARNESS:END -->
""",
    ".windsurfrules": """# Windsurf Cascade Rules

<!-- HARNESS:BEGIN -->
Adhere strictly to the 6-Step Atomic Engineering Protocol defined in `AGENTS.md` and `docs/WORKFLOW.md`.
- Follow `/ntc-init` -> `/ntc-prototype` -> `/ntc-spec` -> `/ntc-modules` -> `/ntc-plan` -> `/ntc-run` (do not read `STEP-by-STEP.md`).
- Maintain single-module boundaries, contract-first invariants, 1:1 UI prototype parity (`SCR-<MOD>-<NN>`), `/ntc-cr` (`CR-<NN>`) delta change control, and the `/ntc-run` / `"tiếp tục"` state machine.
- Update the `🎫 Resume Ticket`, run `python scripts/validate_plans.py --fix`, and create an Atomic Git Commit checkpoint before yielding.
<!-- HARNESS:END -->
""",
}


def fetch_remote_harness(temp_dir: Path) -> Path:
    """Downloads the harness repository into temp_dir via git or HTTPS zip archive."""
    print(f"[*] Fetching NTC Micro-Harness v{HARNESS_VERSION} from {REPO_GIT_URL} ...")
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
            raise RuntimeError("Failed to download and extract NTC Micro-Harness archive.")
        return extracted_dirs[0]


def configure_git_repo(target_root: Path, repo_url: str | None) -> None:
    """Initializes git in target_root and optionally connects remote origin."""
    git_dir = target_root / ".git"
    if not git_dir.exists():
        subprocess.run(["git", "init"], cwd=str(target_root), check=False, stdout=subprocess.DEVNULL)
        print(f"  [+] Initialized empty Git repository in {target_root}")

    if repo_url and repo_url.strip():
        clean_url = repo_url.strip()
        res = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=str(target_root),
            capture_output=True,
            text=True,
        )
        if res.returncode == 0:
            subprocess.run(["git", "remote", "set-url", "origin", clean_url], cwd=str(target_root), check=False)
            print(f"  [+] Updated Git remote 'origin' -> {clean_url}")
        else:
            subprocess.run(["git", "remote", "add", "origin", clean_url], cwd=str(target_root), check=False)
            print(f"  [+] Connected Git remote 'origin' -> {clean_url}")


def install_global_plugin(source_root: Path, plugin_dir: Path | None = None) -> Path:
    """Installs NTC Micro-Harness as a global Antigravity plugin (~/.gemini/config/plugins/ntc-micro-harness)."""
    dst_plugin = plugin_dir or (Path.home() / ".gemini" / "config" / "plugins" / "ntc-micro-harness")
    dst_plugin.mkdir(parents=True, exist_ok=True)

    for item in ["plugin.json", ".claude-plugin/plugin.json", "assets/logo.svg", "rules/AGENTS.md", "README.md", "README.vi.md"]:
        s_file = source_root / item
        d_file = dst_plugin / item
        if s_file.exists():
            d_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(s_file, d_file)

    for skill_name in NTC_SKILLS:
        s_skill = source_root / "skills" / skill_name / "SKILL.md"
        d_skill = dst_plugin / "skills" / skill_name / "SKILL.md"
        if s_skill.exists():
            d_skill.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(s_skill, d_skill)

    print(f"  [+] Installed Global Antigravity Plugin (2.0 / IDE / CLI) at: {dst_plugin}")
    return dst_plugin


def install_harness(
    source_root: Path,
    target_root: Path,
    agent_rules: list[str] | None = None,
    force: bool = False,
    repo_url: str | None = None,
    install_plugin: bool = True,
    plugin_only: bool = False,
) -> None:
    """Installs the NTC Micro-Harness plugin and/or workspace files."""
    if plugin_only:
        print(f"[*] Installing NTC Micro-Harness v{HARNESS_VERSION} Global Plugin for Antigravity (2.0, IDE, CLI)...")
        install_global_plugin(source_root)
        print("\n" + "=" * 68)
        print(f"SUCCESS: NTC Micro-Harness v{HARNESS_VERSION} Global Plugin installed!")
        print("=" * 68)
        print("Restart Antigravity 2.0 / Antigravity IDE / `agy` CLI to activate `/ntc-*` commands.\n")
        return

    target_root = target_root.resolve()
    print(f"[*] Installing NTC Micro-Harness v{HARNESS_VERSION} into: {target_root}")

    if not target_root.exists():
        target_root.mkdir(parents=True, exist_ok=True)

    if repo_url is not None:
        configure_git_repo(target_root, repo_url)

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
        "prototypes/README.md",
        "prototypes/registry.md",
        "patterns/encoding-invariants.md",
        "plans/README.md",
        "plans/contract-registry.md",
        "plans/system-roadmap.md",
        "plans/active/README.md",
        "plans/completed/README.md",
        "templates/prd-template.md",
        "templates/architecture-template.md",
        "templates/application-runbook.md",
        "templates/contract-registry-template.md",
        "templates/ui-prototype-registry-template.md",
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

    # 4. Install /ntc-* slash command skills into workspace (.agents/skills/)
    for skill_name in NTC_SKILLS:
        s_skill = source_root / "skills" / skill_name / "SKILL.md"
        d_skill = target_root / ".agents" / "skills" / skill_name / "SKILL.md"
        if s_skill.exists():
            if not d_skill.exists() or force:
                d_skill.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(s_skill, d_skill)
                print(f"  [+] Installed slash skill /{skill_name} -> {d_skill.relative_to(target_root)}")

    # 5. Global Antigravity plugin installation (~/.gemini/config/plugins/ntc-micro-harness)
    if install_plugin:
        install_global_plugin(source_root)

    # 6. Configure agent integration rules
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

    print("\n" + "=" * 68)
    print(f"SUCCESS: NTC Micro-Harness v{HARNESS_VERSION} (Plugin Edition) installed!")
    print("=" * 68)
    print("6-Step /ntc-* Slash Command Workflow:")
    print("  1. /ntc-init       -> Connect Git remote repo (optional) + Q&A -> PRD.md & ARCHITECTURE.md")
    print("  2. /ntc-prototype  -> Build & refine interactive HTML UI Prototypes (SCR-<MOD>-<NN>)")
    print("  3. /ntc-spec       -> Lock overall SPEC.md + Roadmap + Contracts + ai-skill-maps.md")
    print("  4. /ntc-modules    -> Author detailed docs/modules-spec/<slug>.md + STEP-by-STEP.md")
    print("  5. /ntc-plan       -> Pre-generate all Phase Dossiers & Level-4 Atomic WBS")
    print("  6. /ntc-run        -> Execute 1 Atomic Task per turn + 1:1 UI Parity + Auto Git Commit")
    print("  *  /ntc-cr         -> 4-Step Delta Reverse-Unlock for mid-flight Change Requests (CR-<NN>)")
    print("  *  /ntc-status     -> Validate plans (--fix) or run Closing SYS Full-Stack E2E (--e2e)\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Install NTC Micro-Harness v2.1 (Plugin Edition) into Antigravity (2.0, IDE, CLI) and/or a project workspace.",
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
        "--repo",
        "-r",
        type=str,
        default=None,
        help="Optional Git remote repository URL to connect (origin) before starting work",
    )
    parser.add_argument(
        "--plugin",
        "-p",
        action="store_true",
        default=True,
        help="Install NTC Micro-Harness as a global Antigravity plugin (~/.gemini/config/plugins/ntc-micro-harness)",
    )
    parser.add_argument(
        "--no-plugin",
        action="store_true",
        help="Skip installing into the global Antigravity plugin directory",
    )
    parser.add_argument(
        "--plugin-only",
        action="store_true",
        help="Only install the global Antigravity plugin (~/.gemini/config/plugins/ntc-micro-harness) without modifying current workspace",
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
    do_plugin = False if args.no_plugin else args.plugin

    local_root = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
    if (local_root / "AGENTS.md").exists() and (local_root / "docs" / "WORKFLOW.md").exists():
        install_harness(
            source_root=local_root,
            target_root=args.target,
            agent_rules=agent_selection,
            force=args.force,
            repo_url=args.repo,
            install_plugin=do_plugin,
            plugin_only=args.plugin_only,
        )
    else:
        with tempfile.TemporaryDirectory(prefix="ntc-harness-") as tmp:
            remote_root = fetch_remote_harness(Path(tmp))
            install_harness(
                source_root=remote_root,
                target_root=args.target,
                agent_rules=agent_selection,
                force=args.force,
                repo_url=args.repo,
                install_plugin=do_plugin,
                plugin_only=args.plugin_only,
            )


if __name__ == "__main__":
    main()
