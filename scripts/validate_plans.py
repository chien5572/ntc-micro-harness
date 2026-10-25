#!/usr/bin/env python3
"""Validates and synchronizes the NTC Micro Harness v2.0 planning hierarchy.

Mechanically enforces the structural rules defined in AGENTS.md and docs/WORKFLOW.md:
  - Required harness documents, directories, and templates exist;
  - AGENTS.md keeps exactly one HARNESS:BEGIN / HARNESS:END block;
  - Module Registry rows are well-formed; the reserved SYS module exists;
    non-PLANNED modules have a Detailed Module Spec in docs/modules-spec/<slug>.md;
  - When Phase Dossiers exist (Gate 4/5), ai-skill-maps.md and STEP-by-STEP.md exist;
  - Contract Registry rows are well-formed; providers/consumers are registered
    modules; AVAILABLE contracts have an existing spec file on disk;
  - Global Phases reference registered modules;
  - docs/plans/active|completed contain only <module-slug>/ folders with
    phase-<NN>-<slug>.md or plan-<slug>.md files;
  - Multiple pre-generated Phase Dossiers are allowed in docs/plans/active/<slug>/,
    but at most ONE phase dossier per module may have Lifecycle Status IN_PROGRESS
    (or INTERRUPTED / PHASE_COMPLETED);
  - Active dossiers carry a valid Resume Ticket naming the right module;
    Major/Atomic Task IDs use the <MOD>-P<NN> prefix of their file;
    archived dossiers have no unchecked Atomic Tasks;
  - Detailed Module Spec phase tables (## 9. Module Phase Sequence) agree with
    the dossiers on disk;
  - The Active Work Pointer in docs/plans/system-roadmap.md lists all active
    phase dossiers on disk;
  - With --fix: automatically synchronizes Module Phase Sequence tables in
    docs/modules-spec/<slug>.md and the Active Work Pointer table in
    docs/plans/system-roadmap.md from the actual dossiers on disk.

Exit code 0 = valid (warnings allowed), 1 = violations found.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

EM_DASH = "\u2014"

MODULE_STATUSES = {"PLANNED", "SPEC_REVIEW", "BLUEPRINT_REVIEW", "READY", "IN_PROGRESS", "COMPLETED"}
GLOBAL_STATUSES = {"PENDING", "ACTIVE", "COMPLETED"}
PHASE_STATUSES = {"PENDING", "ACTIVE", "BLOCKED", "COMPLETED"}
CONTRACT_STATUSES = {"DRAFT", "AVAILABLE", "DEPRECATED"}
CONTRACT_TYPES = {"REST", "gRPC", "Event", "Schema", "Library"}
LIFECYCLE_STATUSES = {
    "PENDING",
    "READY_TO_PLAN",
    "WBS_REVIEW",
    "READY_TO_EXECUTE",
    "IN_PROGRESS",
    "BLOCKED_BY_DEPENDENCY",
    "INTERRUPTED",
    "PHASE_COMPLETED",
}
ACTIVE_EXECUTION_LIFECYCLES = {"IN_PROGRESS", "INTERRUPTED", "PHASE_COMPLETED"}

CODE_PATTERN = re.compile(r"^[A-Z]{2,5}$")
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PHASE_FILE_PATTERN = re.compile(r"^phase-(\d{2})-[a-z0-9]+(-[a-z0-9]+)*\.md$")
PLAN_FILE_PATTERN = re.compile(r"^plan-[a-z0-9]+(-[a-z0-9]+)*\.md$")


class Validator:
    def __init__(self, root: Path, fix: bool = False) -> None:
        self.root = root.resolve()
        self.fix = fix
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.fixes: List[str] = []

    def add_violation(self, rule: str, where: str, message: str, fix_hint: str) -> None:
        self.errors.append(f"[{rule}] {where}: {message}\n      -> {fix_hint}")

    def add_warning(self, rule: str, where: str, message: str, fix_hint: str) -> None:
        self.warnings.append(f"[{rule}] {where}: {message}\n      -> {fix_hint}")

    def add_fix(self, where: str, message: str) -> None:
        self.fixes.append(f"[FIXED] {where}: {message}")

    def repo_path(self, relative: str) -> Path:
        return self.root / Path(relative)

    def read_lines(self, relative: str) -> List[str]:
        return self.repo_path(relative).read_text(encoding="utf-8").splitlines()

    def write_lines(self, relative: str, lines: List[str]) -> None:
        self.repo_path(relative).write_text("\n".join(lines) + "\n", encoding="utf-8")

    @staticmethod
    def get_section_bounds(lines: List[str], heading_pattern: str) -> Optional[Tuple[int, int]]:
        """Returns (start_idx, end_idx) of lines under the first H1/H2 matching heading_pattern."""
        rx = re.compile(heading_pattern)
        start_idx: Optional[int] = None
        in_fence = False
        for idx, line in enumerate(lines):
            if re.match(r"^\s*```", line):
                in_fence = not in_fence
            if not in_fence and re.match(r"^#{1,2}\s", line):
                if start_idx is not None:
                    return (start_idx, idx)
                if rx.search(line):
                    start_idx = idx + 1
        if start_idx is not None:
            return (start_idx, len(lines))
        return None

    @classmethod
    def get_section(cls, lines: List[str], heading_pattern: str) -> Tuple[bool, List[str]]:
        bounds = cls.get_section_bounds(lines, heading_pattern)
        if bounds is None:
            return (False, [])
        return (True, lines[bounds[0] : bounds[1]])

    @staticmethod
    def split_row(line: str) -> List[str]:
        trimmed = line.strip()
        if trimmed.startswith("|"):
            trimmed = trimmed[1:]
        if trimmed.endswith("|"):
            trimmed = trimmed[:-1]
        return [cell.strip() for cell in trimmed.split("|")]

    @staticmethod
    def clear_cell(cell: str) -> str:
        return cell.replace("`", "").strip()

    @classmethod
    def is_placeholder(cls, cell: str) -> bool:
        c = cls.clear_cell(cell)
        return (
            c == ""
            or c == EM_DASH
            or c == "-"
            or c == "..."
            or bool(re.match(r"^\*.*\*$", c))
        )

    @classmethod
    def parse_table(cls, lines: List[str]) -> Tuple[bool, List[str], List[Dict[str, str]]]:
        headers: Optional[List[str]] = None
        rows: List[Dict[str, str]] = []
        state = "seek"
        for line in lines:
            is_row = line.strip().startswith("|")
            if state == "seek":
                if is_row:
                    headers = cls.split_row(line)
                    state = "separator"
                continue
            if state == "separator":
                state = "rows"
                continue
            if not is_row:
                break
            assert headers is not None
            cells = cls.split_row(line)
            row: Dict[str, str] = {}
            for i, h in enumerate(headers):
                row[h] = cells[i] if i < len(cells) else ""
            rows.append(row)
        return (headers is not None, headers or [], rows)

    def get_required_table(
        self,
        relative: str,
        heading_pattern: str,
        heading_label: str,
        required_headers: List[str],
    ) -> Optional[Tuple[List[str], List[Dict[str, str]], str]]:
        found_sec, sec_lines = self.get_section(self.read_lines(relative), heading_pattern)
        where = f"{relative} ({heading_label})"
        if not found_sec:
            self.add_violation(
                "SECTION_MISSING",
                relative,
                f"heading '{heading_label}' not found",
                "Restore the section heading from the matching template in docs/templates/.",
            )
            return None
        found_tbl, headers, rows = self.parse_table(sec_lines)
        if not found_tbl:
            self.add_violation(
                "TABLE_MISSING",
                where,
                "no markdown table found",
                "Restore the table from the matching template in docs/templates/.",
            )
            return None
        ok = True
        for h in required_headers:
            if h not in headers:
                self.add_violation(
                    "TABLE_HEADER",
                    where,
                    f"missing column '{h}'",
                    "Restore the table header names from the matching template in docs/templates/.",
                )
                ok = False
        if not ok:
            return None
        return (headers, rows, where)

    def get_dossier_files(self, area: str, slug: str) -> List[Path]:
        d = self.repo_path(f"docs/plans/{area}/{slug}")
        if not d.is_dir():
            return []
        return sorted(
            [f for f in d.iterdir() if f.is_file() and PHASE_FILE_PATTERN.match(f.name)],
            key=lambda p: p.name,
        )

    @classmethod
    def extract_lifecycle_status(cls, content: List[str]) -> str:
        for line in content:
            m = re.match(r"^\s*-\s*\*\*Lifecycle Status:\*\*\s*(.+)$", line)
            if m:
                raw = m.group(1).strip()
                if "|" in raw:
                    # Template default with multiple pipe-separated options
                    first = cls.clear_cell(raw.split("|")[0])
                    return first
                return cls.clear_cell(raw)
        return "UNKNOWN"

    def apply_auto_fix(self, code_to_slug: Dict[str, str]) -> None:
        """Synchronizes Module Phase Sequence tables and Active Work Pointer from disk."""
        # 1. Sync each docs/modules-spec/<slug>.md phase table with active/ and completed/ on disk
        for code, slug in sorted(code_to_slug.items()):
            spec_rel = f"docs/modules-spec/{slug}.md"
            spec_path = self.repo_path(spec_rel)
            if not spec_path.is_file():
                continue

            lines = self.read_lines(spec_rel)
            bounds = self.get_section_bounds(lines, r"^## 9\.\s*Module Phase Sequence")
            if bounds is None:
                continue

            active_map: Dict[str, Tuple[str, str]] = {}  # nn -> (rel_path, lifecycle_status)
            for f in self.get_dossier_files("active", slug):
                m = PHASE_FILE_PATTERN.match(f.name)
                if m:
                    rel = f"docs/plans/active/{slug}/{f.name}"
                    lc = self.extract_lifecycle_status(self.read_lines(rel))
                    active_map[m.group(1)] = (rel, lc)

            done_map: Dict[str, str] = {}  # nn -> rel_path
            for f in self.get_dossier_files("completed", slug):
                m = PHASE_FILE_PATTERN.match(f.name)
                if m:
                    done_map[m.group(1)] = f"docs/plans/completed/{slug}/{f.name}"

            sec_lines = lines[bounds[0] : bounds[1]]
            found_tbl, headers, _ = self.parse_table(sec_lines)
            if not found_tbl or "Phase" not in headers or "Status" not in headers:
                continue

            phase_idx = headers.index("Phase")
            status_idx = headers.index("Status")
            dossier_idx = headers.index("Dossier") if "Dossier" in headers else -1

            changed = False
            state = "seek"
            for i in range(bounds[0], bounds[1]):
                line = lines[i]
                is_row = line.strip().startswith("|")
                if state == "seek":
                    if is_row:
                        state = "separator"
                    continue
                if state == "separator":
                    state = "rows"
                    continue
                if not is_row:
                    break

                cells = self.split_row(line)
                if len(cells) < len(headers):
                    cells.extend([""] * (len(headers) - len(cells)))
                phase_cell = self.clear_cell(cells[phase_idx])
                m_phase = re.match(rf"^{re.escape(code)}-P(\d{{2}})$", phase_cell)
                if not m_phase:
                    continue
                nn = m_phase.group(1)
                new_status = cells[status_idx]
                new_dossier = cells[dossier_idx] if dossier_idx >= 0 else ""

                if nn in done_map:
                    new_status = "`COMPLETED`"
                    if dossier_idx >= 0:
                        new_dossier = f"`{done_map[nn]}`"
                elif nn in active_map:
                    rel_path, lc = active_map[nn]
                    if lc == "BLOCKED_BY_DEPENDENCY":
                        new_status = "`BLOCKED`"
                    elif lc in ACTIVE_EXECUTION_LIFECYCLES or lc == "READY_TO_EXECUTE":
                        new_status = "`ACTIVE`"
                    else:
                        new_status = "`PENDING`"
                    if dossier_idx >= 0:
                        new_dossier = f"`{rel_path}`"

                if cells[status_idx] != new_status or (dossier_idx >= 0 and cells[dossier_idx] != new_dossier):
                    cells[status_idx] = new_status
                    if dossier_idx >= 0:
                        cells[dossier_idx] = new_dossier
                    lines[i] = "| " + " | ".join(cells) + " |"
                    changed = True

            if changed:
                self.write_lines(spec_rel, lines)
                self.add_fix(spec_rel, "synchronized Module Phase Sequence table from disk")

        # 2. Sync Active Work Pointer in docs/plans/system-roadmap.md
        roadmap_rel = "docs/plans/system-roadmap.md"
        if not self.repo_path(roadmap_rel).is_file():
            return
        lines = self.read_lines(roadmap_rel)
        bounds = self.get_section_bounds(lines, r"^## 5\.\s*Active Work Pointer")
        if bounds is None:
            return

        # Gather all active dossiers across registered modules
        pointer_rows: List[str] = []
        for code, slug in sorted(code_to_slug.items()):
            for f in self.get_dossier_files("active", slug):
                rel = f"docs/plans/active/{slug}/{f.name}"
                lc = self.extract_lifecycle_status(self.read_lines(rel))
                pointer_rows.append(f"| `{code}` | `{rel}` | `{lc}` |")

        if not pointer_rows:
            pointer_rows = ["| *[None]* | | |"]

        # Replace table rows inside ## 5. Active Work Pointer
        sec_lines = lines[bounds[0] : bounds[1]]
        tbl_start: Optional[int] = None
        tbl_end: Optional[int] = None
        state = "seek"
        for offset, line in enumerate(sec_lines):
            is_row = line.strip().startswith("|")
            if state == "seek":
                if is_row:
                    state = "separator"
                continue
            if state == "separator":
                state = "rows"
                tbl_start = bounds[0] + offset + 1
                tbl_end = tbl_start
                continue
            if not is_row:
                tbl_end = bounds[0] + offset
                break
            tbl_end = bounds[0] + offset + 1

        if tbl_start is not None and tbl_end is not None:
            existing_rows = lines[tbl_start:tbl_end]
            if existing_rows != pointer_rows:
                new_lines = lines[:tbl_start] + pointer_rows + lines[tbl_end:]
                self.write_lines(roadmap_rel, new_lines)
                self.add_fix(roadmap_rel, "synchronized Active Work Pointer table from docs/plans/active/")

    def run(self) -> int:
        # 1. Required documents & templates
        required_files = [
            "AGENTS.md",
            "docs/WORKFLOW.md",
            "docs/README.md",
            "docs/modules-spec/README.md",
            "docs/plans/README.md",
            "docs/plans/system-roadmap.md",
            "docs/plans/contract-registry.md",
            "docs/plans/active/README.md",
            "docs/plans/completed/README.md",
            "docs/templates/spec-template.md",
            "docs/templates/system-roadmap-template.md",
            "docs/templates/contract-registry-template.md",
            "docs/templates/module-spec-template.md",
            "docs/templates/ai-skill-maps-template.md",
            "docs/templates/step-by-step-template.md",
            "docs/templates/phase-dossier-template.md",
            "docs/templates/decision.md",
            "docs/templates/exec-plan.md",
            "docs/templates/application-runbook.md",
        ]
        for rel in required_files:
            if not self.repo_path(rel).is_file():
                self.add_violation(
                    "REQUIRED_FILE",
                    rel,
                    "required harness document or template is missing",
                    "Restore it from the harness distribution or its template.",
                )

        # Ensure legacy docs/plans/modules/ directory is not present
        if self.repo_path("docs/plans/modules").exists():
            self.add_violation(
                "LEGACY_MODULES_DIR",
                "docs/plans/modules/",
                "legacy docs/plans/modules/ folder exists",
                "Use docs/modules-spec/<module-slug>.md instead and remove docs/plans/modules/.",
            )

        roadmap_rel = "docs/plans/system-roadmap.md"
        registry_rel = "docs/plans/contract-registry.md"
        has_roadmap = self.repo_path(roadmap_rel).is_file()
        has_registry = self.repo_path(registry_rel).is_file()

        # 2. AGENTS.md harness markers
        if self.repo_path("AGENTS.md").is_file():
            agents_lines = self.read_lines("AGENTS.md")
            begins = [i for i, l in enumerate(agents_lines, 1) if "<!-- HARNESS:BEGIN -->" in l]
            ends = [i for i, l in enumerate(agents_lines, 1) if "<!-- HARNESS:END -->" in l]
            if len(begins) != 1 or len(ends) != 1:
                self.add_violation(
                    "HARNESS_MARKERS",
                    "AGENTS.md",
                    f"expected exactly one BEGIN and one END marker, found {len(begins)} and {len(ends)}",
                    "Keep a single <!-- HARNESS:BEGIN --> ... <!-- HARNESS:END --> block.",
                )
            elif begins[0] > ends[0]:
                self.add_violation(
                    "HARNESS_MARKERS",
                    "AGENTS.md",
                    "HARNESS:END appears before HARNESS:BEGIN",
                    "Reorder the markers.",
                )

        # 3. Module Registry
        slug_to_code: Dict[str, str] = {}
        code_to_slug: Dict[str, str] = {}
        module_status: Dict[str, str] = {}

        if has_roadmap:
            reg = self.get_required_table(
                roadmap_rel,
                r"^## 2\.\s*Module Registry",
                "## 2. Module Registry",
                ["Code", "Slug", "Code Root", "Module Spec", "Status"],
            )
            if reg is not None:
                _, rows, label = reg
                for row in rows:
                    if self.is_placeholder(row["Code"]):
                        continue
                    code = self.clear_cell(row["Code"])
                    slug = self.clear_cell(row["Slug"])
                    status = self.clear_cell(row["Status"])
                    where = f"{label} row '{code}'"
                    if not CODE_PATTERN.match(code):
                        self.add_violation(
                            "MODULE_CODE",
                            where,
                            f"module code '{code}' is not 2-5 uppercase letters",
                            "Use a code such as AUTH or ORD (docs/WORKFLOW.md section 2).",
                        )
                        continue
                    if not SLUG_PATTERN.match(slug):
                        self.add_violation(
                            "MODULE_SLUG",
                            where,
                            f"slug '{slug}' is not lowercase kebab-case",
                            "Use a slug such as auth or order-history.",
                        )
                        continue
                    if code in code_to_slug:
                        self.add_violation(
                            "MODULE_DUPLICATE",
                            where,
                            f"module code '{code}' is registered twice",
                            "Module codes are assigned once and never reused.",
                        )
                        continue
                    if slug in slug_to_code:
                        self.add_violation(
                            "MODULE_DUPLICATE",
                            where,
                            f"slug '{slug}' is registered twice",
                            "Module slugs are assigned once and never reused.",
                        )
                        continue
                    code_to_slug[code] = slug
                    slug_to_code[slug] = code
                    module_status[code] = status

                    if status not in MODULE_STATUSES:
                        self.add_violation(
                            "MODULE_STATUS",
                            where,
                            f"status '{status}' is not one of {' | '.join(sorted(MODULE_STATUSES))}",
                            "Use a valid status from docs/templates/system-roadmap-template.md.",
                        )
                    expected_spec = f"docs/modules-spec/{slug}.md"
                    spec_col = self.clear_cell(row["Module Spec"])
                    if spec_col != expected_spec:
                        self.add_violation(
                            "MODULE_SPEC_PATH",
                            where,
                            f"Module Spec path '{spec_col}' should be '{expected_spec}'",
                            "Detailed Module Specs live at docs/modules-spec/<module-slug>.md.",
                        )
                    if status != "PLANNED" and not self.repo_path(expected_spec).is_file():
                        self.add_violation(
                            "MODULE_SPEC_MISSING",
                            where,
                            f"status is '{status}' but {expected_spec} does not exist",
                            "Create the Detailed Module Spec from docs/templates/module-spec-template.md (Gate 3) or set status to PLANNED.",
                        )

                if code_to_slug.get("SYS") != "system":
                    self.add_violation(
                        "SYS_RESERVED",
                        label,
                        "reserved pseudo-module 'SYS' / 'system' is not registered",
                        "Register SYS with slug system for cross-cutting work.",
                    )

        # If --fix was requested, synchronize tables before running cross-sync checks
        if self.fix and code_to_slug:
            self.apply_auto_fix(code_to_slug)

        # Detailed Module Spec files must belong to registered modules
        specs_dir = self.repo_path("docs/modules-spec")
        if specs_dir.is_dir():
            for f in sorted(specs_dir.iterdir(), key=lambda p: p.name):
                if f.is_dir():
                    self.add_violation(
                        "MODULE_SPEC_LAYOUT",
                        f"docs/modules-spec/{f.name}/",
                        "module specs are flat files, not folders",
                        "Use docs/modules-spec/<module-slug>.md; dossiers belong in docs/plans/active/<module-slug>/.",
                    )
                elif f.is_file() and f.suffix == ".md" and f.name != "README.md":
                    slug = f.stem
                    if slug not in slug_to_code:
                        self.add_violation(
                            "MODULE_SPEC_ORPHAN",
                            f"docs/modules-spec/{f.name}",
                            f"slug '{slug}' is not in the Module Registry",
                            "Register the module in docs/plans/system-roadmap.md or remove the file.",
                        )

        # 4. Contract Registry
        if has_registry:
            ct = self.get_required_table(
                registry_rel,
                r"^## 1\.\s*Contracts",
                "## 1. Contracts",
                ["Contract ID", "Type", "Provider", "Consumers", "Spec Path", "Version", "Status"],
            )
            if ct is not None:
                _, rows, label = ct
                seen_ct: Dict[str, bool] = {}
                for row in rows:
                    if self.is_placeholder(row["Contract ID"]):
                        continue
                    cid = self.clear_cell(row["Contract ID"])
                    where = f"{label} row '{cid}'"
                    m_ct = re.match(r"^CT-([A-Z]{2,5})-(\d{2})$", cid)
                    if not m_ct:
                        self.add_violation(
                            "CONTRACT_ID",
                            where,
                            f"contract ID '{cid}' does not match CT-<PROVIDER>-<NN>",
                            "Rename it, e.g. CT-AUTH-01.",
                        )
                        continue
                    id_provider = m_ct.group(1)
                    if cid in seen_ct:
                        self.add_violation(
                            "CONTRACT_DUPLICATE",
                            where,
                            f"contract ID '{cid}' is registered twice",
                            "Contract IDs are unique; bump the version instead of duplicating.",
                        )
                    seen_ct[cid] = True
                    provider = self.clear_cell(row["Provider"])
                    if provider != id_provider:
                        self.add_violation(
                            "CONTRACT_PROVIDER",
                            where,
                            f"provider '{provider}' does not match the ID prefix '{id_provider}'",
                            "The provider code is part of the contract ID.",
                        )
                    if slug_to_code and provider not in code_to_slug:
                        self.add_violation(
                            "CONTRACT_PROVIDER",
                            where,
                            f"provider '{provider}' is not a registered module",
                            "Register the module in the Module Registry first.",
                        )
                    consumers_cell = self.clear_cell(row["Consumers"])
                    if not self.is_placeholder(consumers_cell):
                        for c_raw in consumers_cell.split(","):
                            c = c_raw.strip()
                            if not c:
                                continue
                            if c == provider:
                                self.add_violation(
                                    "CONTRACT_CONSUMER",
                                    where,
                                    f"provider '{c}' is listed as its own consumer",
                                    "Remove it from Consumers.",
                                )
                            elif slug_to_code and c not in code_to_slug:
                                self.add_violation(
                                    "CONTRACT_CONSUMER",
                                    where,
                                    f"consumer '{c}' is not a registered module",
                                    "Register the module or fix the code.",
                                )
                    ctype = self.clear_cell(row["Type"])
                    if ctype not in CONTRACT_TYPES:
                        self.add_violation(
                            "CONTRACT_TYPE",
                            where,
                            f"type '{ctype}' is not one of {' | '.join(sorted(CONTRACT_TYPES))}",
                            "Use a valid type from the registry legend.",
                        )
                    version = self.clear_cell(row["Version"])
                    if not re.match(r"^\d+\.\d+\.\d+$", version):
                        self.add_warning(
                            "CONTRACT_VERSION",
                            where,
                            f"version '{version}' is not MAJOR.MINOR.PATCH",
                            "Use semantic versioning so change control can detect breaking changes.",
                        )
                    status = self.clear_cell(row["Status"])
                    if status not in CONTRACT_STATUSES:
                        self.add_violation(
                            "CONTRACT_STATUS",
                            where,
                            f"status '{status}' is not one of {' | '.join(sorted(CONTRACT_STATUSES))}",
                            "Use DRAFT, AVAILABLE, or DEPRECATED.",
                        )
                    spec = self.clear_cell(row["Spec Path"])
                    if status == "AVAILABLE":
                        if self.is_placeholder(spec) or not self.repo_path(spec).exists():
                            self.add_violation(
                                "CONTRACT_SPEC",
                                where,
                                f"status is AVAILABLE but spec '{spec}' does not exist",
                                "Codify the spec at the declared path (Contract-First) or set status back to DRAFT.",
                            )

        # 5. Global Phase Sequence
        if has_roadmap:
            gp = self.get_required_table(
                roadmap_rel,
                r"^## 3\.\s*Global Phase Sequence",
                "## 3. Global Phase Sequence",
                ["GP", "Participating Module Phases", "Status"],
            )
            if gp is not None:
                _, rows, label = gp
                seen_gp: Dict[str, bool] = {}
                for row in rows:
                    if self.is_placeholder(row["GP"]):
                        continue
                    gid = self.clear_cell(row["GP"])
                    where = f"{label} row '{gid}'"
                    if not re.match(r"^GP-\d{2}$", gid):
                        self.add_violation(
                            "GP_ID",
                            where,
                            f"global phase ID '{gid}' does not match GP-<NN>",
                            "Rename it, e.g. GP-01.",
                        )
                        continue
                    if gid in seen_gp:
                        self.add_violation(
                            "GP_DUPLICATE",
                            where,
                            f"global phase '{gid}' appears twice",
                            "Global phase IDs are unique.",
                        )
                    seen_gp[gid] = True
                    status = self.clear_cell(row["Status"])
                    if status not in GLOBAL_STATUSES:
                        self.add_violation(
                            "GP_STATUS",
                            where,
                            f"status '{status}' is not one of {' | '.join(sorted(GLOBAL_STATUSES))}",
                            "Use PENDING, ACTIVE, or COMPLETED.",
                        )
                    for m in re.finditer(r"\b([A-Z]{2,5})-P(\d{2})\b", row["Participating Module Phases"]):
                        m_code, m_nn = m.group(1), m.group(2)
                        if slug_to_code and m_code not in code_to_slug:
                            self.add_violation(
                                "GP_MODULE",
                                where,
                                f"phase '{m.group(0)}' references unregistered module '{m_code}'",
                                "Register the module or fix the phase ID.",
                            )
                        elif status == "COMPLETED" and m_code in code_to_slug:
                            done = [
                                f
                                for f in self.get_dossier_files("completed", code_to_slug[m_code])
                                if f.name.startswith(f"phase-{m_nn}-")
                            ]
                            if not done:
                                self.add_violation(
                                    "GP_COMPLETION",
                                    where,
                                    f"marked COMPLETED but '{m.group(0)}' has no dossier in docs/plans/completed/{code_to_slug[m_code]}/",
                                    "A global phase completes only when all its module phases are archived.",
                                )

        # 6. active/ and completed/ layout + dossier content
        active_dossiers: List[str] = []
        dossier_index: Dict[str, str] = {}  # "area|slug|nn" -> filename

        for area in ("active", "completed"):
            area_dir = self.repo_path(f"docs/plans/{area}")
            if not area_dir.is_dir():
                continue

            for f in sorted(area_dir.iterdir(), key=lambda p: p.name):
                if f.is_file():
                    if f.name == "README.md":
                        continue
                    self.add_violation(
                        "FLAT_DOSSIER",
                        f"docs/plans/{area}/{f.name}",
                        "files must live inside a module folder",
                        f"Move it to docs/plans/{area}/<module-slug>/.",
                    )
                elif f.is_dir():
                    slug = f.name
                    dir_rel = f"docs/plans/{area}/{slug}"
                    if slug not in slug_to_code:
                        self.add_violation(
                            "MODULE_FOLDER",
                            f"{dir_rel}/",
                            f"folder '{slug}' is not a registered module slug",
                            "Register the module in docs/plans/system-roadmap.md or rename the folder.",
                        )
                        continue
                    code = slug_to_code[slug]

                    in_progress_files: List[str] = []

                    for child in sorted(f.iterdir(), key=lambda p: p.name):
                        if child.is_dir():
                            self.add_violation(
                                "NESTED_FOLDER",
                                f"{dir_rel}/{child.name}/",
                                "module folders must not contain sub-folders",
                                "Keep dossiers directly in the module folder.",
                            )
                            continue

                        rel = f"{dir_rel}/{child.name}"
                        m_phase = PHASE_FILE_PATTERN.match(child.name)
                        if m_phase:
                            nn = m_phase.group(1)
                            key = f"{area}|{slug}|{nn}"
                            if key in dossier_index:
                                self.add_violation(
                                    "PHASE_DUPLICATE",
                                    rel,
                                    f"phase {nn} already has dossier '{dossier_index[key]}'",
                                    "Keep a single dossier per module phase.",
                                )
                            dossier_index[key] = child.name
                            if area == "active":
                                active_dossiers.append(rel)

                            content = self.read_lines(rel)
                            prefix = f"{code}-P{nn}"

                            if area == "active":
                                if not any(re.match(r"^## .*Resume Ticket", l) for l in content):
                                    self.add_violation(
                                        "RESUME_TICKET",
                                        rel,
                                        "no '## ... Resume Ticket' section",
                                        "Restore the Resume Ticket block from docs/templates/phase-dossier-template.md.",
                                    )
                                mod_lines = [l for l in content if re.match(r"^\s*-\s*\*\*Module:\*\*", l)]
                                if not mod_lines:
                                    self.add_violation(
                                        "RESUME_TICKET",
                                        rel,
                                        "Resume Ticket has no '- **Module:**' field",
                                        f"Add '- **Module:** `{code}`' to the Resume Ticket.",
                                    )
                                else:
                                    mod_val = self.clear_cell(re.sub(r"^\s*-\s*\*\*Module:\*\*", "", mod_lines[0]))
                                    if mod_val != code:
                                        self.add_violation(
                                            "RESUME_TICKET",
                                            rel,
                                            f"Resume Ticket module '{mod_val}' does not match folder module '{code}'",
                                            f"Set '- **Module:** `{code}`'.",
                                        )
                                lc_status = self.extract_lifecycle_status(content)
                                if lc_status not in LIFECYCLE_STATUSES:
                                    self.add_violation(
                                        "RESUME_TICKET_STATUS",
                                        rel,
                                        f"Lifecycle Status '{lc_status}' is not one of {' | '.join(sorted(LIFECYCLE_STATUSES))}",
                                        "Use a valid Lifecycle Status in the Resume Ticket.",
                                    )
                                if lc_status in ACTIVE_EXECUTION_LIFECYCLES:
                                    in_progress_files.append(child.name)

                                if not any("Immediate Next Atomic Action" in l for l in content):
                                    self.add_violation(
                                        "RESUME_TICKET",
                                        rel,
                                        "Resume Ticket has no 'Immediate Next Atomic Action'",
                                        "Restore the field from docs/templates/phase-dossier-template.md.",
                                    )

                            for line_no, line in enumerate(content, 1):
                                m_maj = re.match(r"^### Major Task (\S+?):", line)
                                if m_maj:
                                    if not re.match(rf"^{re.escape(prefix)}\.\d+$", m_maj.group(1)):
                                        self.add_violation(
                                            "TASK_ID",
                                            f"{rel}:{line_no}",
                                            f"Major Task ID '{m_maj.group(1)}' should be {prefix}.<M>",
                                            "Use the <MOD>-P<NN>.<M> format matching this dossier.",
                                        )
                                m_atom = re.match(r"^\s*-\s*\[([ xX])\]\s*\*\*Atomic Task (\S+?):\*\*", line)
                                if m_atom:
                                    checked = m_atom.group(1) != " "
                                    task_id = m_atom.group(2)
                                    if not re.match(rf"^{re.escape(prefix)}\.\d+\.\d+[a-z]?$", task_id):
                                        self.add_violation(
                                            "TASK_ID",
                                            f"{rel}:{line_no}",
                                            f"Atomic Task ID '{task_id}' should be {prefix}.<M>.<A>",
                                            "Use the <MOD>-P<NN>.<M>.<A> format matching this dossier.",
                                        )
                                    if area == "completed" and not checked:
                                        self.add_violation(
                                            "ARCHIVE_INCOMPLETE",
                                            f"{rel}:{line_no}",
                                            f"archived dossier has unchecked Atomic Task '{task_id}'",
                                            "Only verified phases may be archived; move it back to active/ or complete the task.",
                                        )
                        elif PLAN_FILE_PATTERN.match(child.name):
                            continue
                        else:
                            self.add_violation(
                                "DOSSIER_NAME",
                                rel,
                                "file name must be phase-<NN>-<slug>.md or plan-<slug>.md",
                                "Rename the file (docs/WORKFLOW.md section 2).",
                            )

                    if area == "active" and len(in_progress_files) > 1:
                        self.add_violation(
                            "ONE_IN_PROGRESS_PHASE",
                            f"{dir_rel}/",
                            f"{len(in_progress_files)} phase dossiers have active execution status (IN_PROGRESS/INTERRUPTED/PHASE_COMPLETED): {', '.join(in_progress_files)}",
                            "Pre-generated subsequent phase dossiers in active/ must have Lifecycle Status PENDING until the current phase transitions.",
                        )

        for key, fname in list(dossier_index.items()):
            parts = key.split("|")
            if parts[0] == "active" and f"completed|{parts[1]}|{parts[2]}" in dossier_index:
                self.add_violation(
                    "PHASE_BOTH_AREAS",
                    f"docs/plans/active/{parts[1]}/{fname}",
                    f"phase {parts[2]} exists in both active/ and completed/",
                    "A dossier is moved (not copied) to completed/.",
                )

        # Gate 3/4 check: if any dossiers exist on disk, ai-skill-maps.md and STEP-by-STEP.md must exist
        if dossier_index:
            if not self.repo_path("ai-skill-maps.md").is_file():
                self.add_violation(
                    "SKILL_MAP_MISSING",
                    "ai-skill-maps.md",
                    "Phase Dossiers exist (Gate 4/5) but ai-skill-maps.md is missing at repository root",
                    "Complete Gate 3.2 to generate ai-skill-maps.md from docs/templates/ai-skill-maps-template.md.",
                )
            if not self.repo_path("STEP-by-STEP.md").is_file():
                self.add_violation(
                    "STEP_PLAYBOOK_MISSING",
                    "STEP-by-STEP.md",
                    "Phase Dossiers exist (Gate 4/5) but STEP-by-STEP.md is missing at repository root",
                    "Complete Gate 3.3 to generate STEP-by-STEP.md from docs/templates/step-by-step-template.md.",
                )

        # 7. Detailed Module Specs (docs/modules-spec/<slug>.md) vs dossiers on disk
        for code, slug in sorted(code_to_slug.items()):
            spec_rel = f"docs/modules-spec/{slug}.md"
            has_spec = self.repo_path(spec_rel).is_file()
            disk_active = self.get_dossier_files("active", slug)
            disk_done = self.get_dossier_files("completed", slug)

            if not has_spec:
                if disk_active or disk_done:
                    self.add_violation(
                        "MODULE_SPEC_MISSING",
                        spec_rel,
                        f"module '{code}' has phase dossiers but no Detailed Module Spec",
                        "Create docs/modules-spec/<slug>.md (Gate 3) before generating Phase Dossiers (Gate 4).",
                    )
                continue

            sp = self.get_required_table(
                spec_rel,
                r"^## 9\.\s*Module Phase Sequence",
                "## 9. Module Phase Sequence",
                ["Phase", "Status"],
            )
            if sp is None:
                continue

            _, rows, label = sp
            planned: Dict[str, str] = {}
            for row in rows:
                if self.is_placeholder(row["Phase"]):
                    continue
                phase = self.clear_cell(row["Phase"])
                where = f"{label} row '{phase}'"
                m_p = re.match(rf"^{re.escape(code)}-P(\d{{2}})$", phase)
                if not m_p:
                    self.add_violation(
                        "PHASE_ID",
                        where,
                        f"phase ID '{phase}' should be {code}-P<NN>",
                        "Use this module's code as the phase prefix.",
                    )
                    continue
                nn = m_p.group(1)
                if nn in planned:
                    self.add_violation(
                        "PHASE_DUPLICATE",
                        where,
                        f"phase '{phase}' appears twice",
                        "Phase IDs are unique within a module.",
                    )
                status = self.clear_cell(row["Status"])
                planned[nn] = status
                if status not in PHASE_STATUSES:
                    self.add_violation(
                        "PHASE_STATUS",
                        where,
                        f"status '{status}' is not one of {' | '.join(sorted(PHASE_STATUSES))}",
                        "Use PENDING, ACTIVE, BLOCKED, or COMPLETED.",
                        )
                    continue
                in_active = f"active|{slug}|{nn}" in dossier_index
                in_done = f"completed|{slug}|{nn}" in dossier_index
                if status == "ACTIVE" and not in_active:
                    self.add_violation(
                        "PHASE_SYNC",
                        where,
                        f"status is ACTIVE but no docs/plans/active/{slug}/phase-{nn}-*.md exists",
                        "Instantiate the dossier (Gate 4) or run `python scripts/validate_plans.py --fix`.",
                    )
                if status == "COMPLETED" and not in_done:
                    self.add_violation(
                        "PHASE_SYNC",
                        where,
                        f"status is COMPLETED but no docs/plans/completed/{slug}/phase-{nn}-*.md exists",
                        "Archive the verified dossier or run `python scripts/validate_plans.py --fix`.",
                    )
                if status == "PENDING" and in_done:
                    self.add_violation(
                        "PHASE_SYNC",
                        where,
                        "status is PENDING but the dossier is already in completed/",
                        "Set the status to COMPLETED or run `python scripts/validate_plans.py --fix`.",
                    )

            for f in disk_active:
                m_f = PHASE_FILE_PATTERN.match(f.name)
                assert m_f is not None
                nn = m_f.group(1)
                if nn not in planned:
                    self.add_violation(
                        "PHASE_SYNC",
                        f"docs/plans/active/{slug}/{f.name}",
                        f"phase {code}-P{nn} is not in {spec_rel} section 9",
                        f"Add {code}-P{nn} to {spec_rel} section 9.",
                    )
                elif planned[nn] not in ("ACTIVE", "BLOCKED", "PENDING"):
                    self.add_violation(
                        "PHASE_SYNC",
                        f"docs/plans/active/{slug}/{f.name}",
                        f"spec status for {code}-P{nn} is '{planned[nn]}', expected ACTIVE, PENDING, or BLOCKED",
                        f"Update {spec_rel} section 9 or run `python scripts/validate_plans.py --fix`.",
                    )

            for f in disk_done:
                m_f = PHASE_FILE_PATTERN.match(f.name)
                assert m_f is not None
                nn = m_f.group(1)
                if nn not in planned:
                    self.add_violation(
                        "PHASE_SYNC",
                        f"docs/plans/completed/{slug}/{f.name}",
                        f"phase {code}-P{nn} is not in {spec_rel} section 9",
                        f"Add {code}-P{nn} to {spec_rel} section 9.",
                    )
                elif planned[nn] != "COMPLETED":
                    self.add_violation(
                        "PHASE_SYNC",
                        f"docs/plans/completed/{slug}/{f.name}",
                        f"spec status for {code}-P{nn} is '{planned[nn]}', expected COMPLETED",
                        f"Update {spec_rel} section 9 or run `python scripts/validate_plans.py --fix`.",
                    )

            if disk_active and module_status.get(code) not in ("IN_PROGRESS", "READY"):
                self.add_warning(
                    "MODULE_STATUS_SYNC",
                    roadmap_rel,
                    f"module '{code}' has dossiers in active/ but registry status is '{module_status.get(code)}'",
                    "Set the module status to READY (Gate 4) or IN_PROGRESS (Gate 5).",
                )

        # 8. Active Work Pointer
        if has_roadmap:
            found_ptr, ptr_lines = self.get_section(self.read_lines(roadmap_rel), r"^## 5\.\s*Active Work Pointer")
            if not found_ptr:
                self.add_violation(
                    "SECTION_MISSING",
                    roadmap_rel,
                    "heading '## 5. Active Work Pointer' not found",
                    "Restore the section from docs/templates/system-roadmap-template.md.",
                )
            else:
                text = "\n".join(ptr_lines)
                listed = set(re.findall(r"docs/plans/active/[a-z0-9-]+/phase-\d{2}-[a-z0-9-]+\.md", text))
                for rel in active_dossiers:
                    if rel not in listed:
                        self.add_violation(
                            "POINTER_SYNC",
                            f"{roadmap_rel} (## 5. Active Work Pointer)",
                            f"active dossier '{rel}' is not listed",
                            "Run `python scripts/validate_plans.py --fix` or add it to the Active Work Pointer table.",
                        )
                for rel in sorted(listed):
                    if rel not in active_dossiers:
                        self.add_violation(
                            "POINTER_SYNC",
                            f"{roadmap_rel} (## 5. Active Work Pointer)",
                            f"points to '{rel}', which is not in docs/plans/active/",
                            "Run `python scripts/validate_plans.py --fix` or remove the stale entry.",
                        )
                if not any(re.match(r"^\s*-\s*\*\*Current Stage:\*\*", l) for l in ptr_lines):
                    self.add_violation(
                        "POINTER_FIELD",
                        f"{roadmap_rel} (## 5. Active Work Pointer)",
                        "missing '- **Current Stage:**'",
                        "Restore the field from docs/templates/system-roadmap-template.md.",
                    )
                if not any(re.match(r"^\s*-\s*\*\*Current Focus:\*\*", l) for l in ptr_lines):
                    self.add_violation(
                        "POINTER_FIELD",
                        f"{roadmap_rel} (## 5. Active Work Pointer)",
                        "missing '- **Current Focus:**'",
                        "Restore the field from docs/templates/system-roadmap-template.md.",
                    )

        # Report
        print(f"Harness plan validation (v2.0): {self.root}")
        print(f"  modules registered: {len(code_to_slug)}; active phase dossiers: {len(active_dossiers)}")
        for fx in self.fixes:
            print(f"FIX   {fx}")
        for w in self.warnings:
            print(f"WARN  {w}")
        for e in self.errors:
            print(f"ERROR {e}")

        if self.errors:
            print(f"FAILED: {len(self.errors)} violation(s), {len(self.warnings)} warning(s).")
            return 1
        print(f"PASSED: 0 violations, {len(self.warnings)} warning(s).")
        return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate and synchronize the NTC Micro Harness planning hierarchy."
    )
    parser.add_argument(
        "--root",
        "-r",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Repository root directory",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Automatically synchronize Module Phase Sequence tables and Active Work Pointer from disk",
    )
    args = parser.parse_args()
    validator = Validator(root=args.root, fix=args.fix)
    sys.exit(validator.run())


if __name__ == "__main__":
    main()
