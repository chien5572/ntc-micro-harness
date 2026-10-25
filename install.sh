#!/usr/bin/env bash
# ==============================================================================
# NTC Micro Harness v2.0 - Automated Bash Installer (Linux / macOS / WSL / Git Bash)
# Supports both local execution and remote 1-liner execution (`curl -fsSL ... | bash`)
# ==============================================================================
set -euo pipefail

TARGET_DIR="${1:-.}"
REPO_GIT_URL="https://github.com/chien5572/ntc-micro-harness.git"
REPO_TAR_URL="https://github.com/chien5572/ntc-micro-harness/archive/refs/heads/main.tar.gz"

TMP_DIR=""
cleanup() {
    if [ -n "${TMP_DIR}" ] && [ -d "${TMP_DIR}" ]; then
        rm -rf "${TMP_DIR}"
    fi
}
trap cleanup EXIT

SCRIPT_DIR=""
if [ -n "${BASH_SOURCE[0]:-}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

if [ -n "${SCRIPT_DIR}" ] && [ -f "${SCRIPT_DIR}/AGENTS.md" ] && [ -f "${SCRIPT_DIR}/docs/WORKFLOW.md" ]; then
    SOURCE_DIR="${SCRIPT_DIR}"
else
    TMP_DIR="$(mktemp -d 2>/dev/null || mktemp -d -t 'ntc-harness')"
    echo "[*] Fetching NTC Micro Harness v2.0 from ${REPO_GIT_URL} ..."
    if command -v git >/dev/null 2>&1; then
        git clone --depth 1 --quiet "${REPO_GIT_URL}" "${TMP_DIR}/repo"
        SOURCE_DIR="${TMP_DIR}/repo"
    else
        curl -fsSL "${REPO_TAR_URL}" | tar -xz -C "${TMP_DIR}"
        SOURCE_DIR="$(find "${TMP_DIR}" -maxdepth 2 -name "AGENTS.md" -exec dirname {} \; | head -n 1)"
    fi
fi

mkdir -p "${TARGET_DIR}"
TARGET_DIR="$(cd "${TARGET_DIR}" && pwd)"

echo "=========================================================="
echo " Installing NTC Micro Harness v2.0 into: ${TARGET_DIR}"
echo "=========================================================="

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
    "modules-spec/README.md"
    "patterns/encoding-invariants.md"
    "plans/README.md"
    "plans/contract-registry.md"
    "plans/system-roadmap.md"
    "plans/active/README.md"
    "plans/completed/README.md"
    "templates/application-runbook.md"
    "templates/contract-registry-template.md"
    "templates/decision.md"
    "templates/exec-plan.md"
    "templates/module-spec-template.md"
    "templates/ai-skill-maps-template.md"
    "templates/step-by-step-template.md"
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

# 3. Copy scripts/validate_plans.py
if [ -f "${SOURCE_DIR}/scripts/validate_plans.py" ]; then
    mkdir -p "${TARGET_DIR}/scripts"
    if [ ! -f "${TARGET_DIR}/scripts/validate_plans.py" ]; then
        cp "${SOURCE_DIR}/scripts/validate_plans.py" "${TARGET_DIR}/scripts/validate_plans.py"
        echo "  [+] Created scripts/validate_plans.py"
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
- Hierarchy of Truth: `SPEC.md` > `AGENTS.md` > `docs/plans/system-roadmap.md` > `docs/plans/contract-registry.md` > `docs/modules-spec/<slug>.md` > `ai-skill-maps.md` > `docs/plans/active/<slug>/phase-*.md`.
- Note: `STEP-by-STEP.md` is strictly for the Human Architect; AI Agents must NOT read it.
- Implement exactly ONE Atomic Task per turn. Never generate incomplete stubs.
- Update the `🎫 Resume Ticket` and run `python scripts/validate_plans.py --fix` before concluding any turn.
<!-- HARNESS:END -->
EOF
        echo "  [+] Configured agent rule: ${rule_file}"
    fi
done

echo ""
echo "=========================================================="
echo " SUCCESS: NTC Micro Harness v2.0 installed successfully!"
echo "=========================================================="
echo "Next Steps:"
echo "  1. Draft requirements at SPEC.md using docs/templates/spec-template.md."
echo "  2. Start your AI Agent (Antigravity, Claude Code, Cursor, Windsurf) and prompt:"
echo '     "Read SPEC.md and AGENTS.md to perform Gate 1 & Gate 2."'
echo "  3. Validate and auto-sync planning documents at any time using:"
echo "     python scripts/validate_plans.py --fix"
echo ""
