#!/usr/bin/env bash
# ==============================================================================
# NTC Micro Harness - Automated Bash Installer (Linux / macOS)
# ==============================================================================
set -euo pipefail

TARGET_DIR="${1:-.}"
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================================="
echo " Installing NTC Micro Harness into: ${TARGET_DIR}"
echo "=========================================================="

mkdir -p "${TARGET_DIR}"
TARGET_DIR="$(cd "${TARGET_DIR}" && pwd)"

# 1. Install or update AGENTS.md
DST_AGENTS="${TARGET_DIR}/AGENTS.md"
if [ ! -f "${DST_AGENTS}" ]; then
    cp "${SOURCE_DIR}/AGENTS.md" "${DST_AGENTS}"
    echo "  [+] Created AGENTS.md"
else
    if grep -q "<!-- HARNESS:BEGIN -->" "${DST_AGENTS}"; then
        echo "  [.] AGENTS.md already contains Harness block (skipping)"
    else
        printf "\n\n" >> "${DST_AGENTS}"
        cat "${SOURCE_DIR}/AGENTS.md" >> "${DST_AGENTS}"
        echo "  [+] Appended Harness block to existing AGENTS.md"
    fi
fi

# 2. Copy docs structure
DOCS_ITEMS=(
    "WORKFLOW.md"
    "README.md"
    "patterns/encoding-invariants.md"
    "plans/README.md"
    "plans/contract-registry.md"
    "plans/system-roadmap.md"
    "plans/active/README.md"
    "plans/completed/README.md"
    "plans/modules/README.md"
    "templates/application-runbook.md"
    "templates/contract-registry-template.md"
    "templates/decision.md"
    "templates/exec-plan.md"
    "templates/module-roadmap-template.md"
    "templates/phase-dossier-template.md"
    "templates/spec-template.md"
    "templates/system-roadmap-template.md"
)

for item in "${DOCS_ITEMS[@]}"; do
    SRC_FILE="${SOURCE_DIR}/docs/${item}"
    DST_FILE="${TARGET_DIR}/docs/${item}"
    if [ -f "${SRC_FILE}" ]; then
        mkdir -p "$(dirname "${DST_FILE}")"
        if [ ! -f "${DST_FILE}" ]; then
            cp "${SRC_FILE}" "${DST_FILE}"
            echo "  [+] Created docs/${item}"
        else
            echo "  [.] docs/${item} already exists (skipping)"
        fi
    fi
done

# 3. Copy scripts/validate-plans.ps1
if [ -f "${SOURCE_DIR}/scripts/validate-plans.ps1" ]; then
    mkdir -p "${TARGET_DIR}/scripts"
    if [ ! -f "${TARGET_DIR}/scripts/validate-plans.ps1" ]; then
        cp "${SOURCE_DIR}/scripts/validate-plans.ps1" "${TARGET_DIR}/scripts/validate-plans.ps1"
        echo "  [+] Created scripts/validate-plans.ps1"
    fi
fi

# 4. Agent rule files
AGENT_FILES=(".cursorrules" "CLAUDE.md" ".windsurfrules")
for rule_file in "${AGENT_FILES[@]}"; do
    DST_RULE="${TARGET_DIR}/${rule_file}"
    if [ ! -f "${DST_RULE}" ]; then
        cat << 'EOF' > "${DST_RULE}"
<!-- HARNESS:BEGIN -->
Always adhere strictly to the Atomic Engineering Protocol defined in `AGENTS.md` and `docs/WORKFLOW.md`.
- Hierarchy of Truth: SPEC.md > AGENTS.md > docs/plans/system-roadmap.md > docs/plans/active/<module>/phase-*.md.
- Implement exactly ONE Atomic Task per turn. Never generate incomplete stubs.
- Update the `🎫 Resume Ticket` before concluding any turn.
<!-- HARNESS:END -->
EOF
        echo "  [+] Configured agent rule: ${rule_file}"
    fi
done

echo ""
echo "=========================================================="
echo " SUCCESS: NTC Micro Harness installed successfully!"
echo "=========================================================="
echo "Next Steps:"
echo "  1. Draft requirements at SPEC.md using docs/templates/spec-template.md."
echo "  2. Start your AI Agent (Antigravity, Claude Code, Cursor, Windsurf) and prompt:"
echo '     "Read SPEC.md and AGENTS.md to collaboratively build our System Roadmap."'
echo ""
