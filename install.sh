#!/usr/bin/env bash
# ==============================================================================
# NTC Micro Harness v2.1 (Plugin Edition) - Automated Bash Installer
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
    echo "[*] Fetching NTC Micro Harness v2.1 from ${REPO_GIT_URL} ..."
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
echo " Installing NTC Micro Harness v2.1 into: ${TARGET_DIR}"
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
    "prototypes/README.md"
    "prototypes/registry.md"
    "patterns/encoding-invariants.md"
    "plans/README.md"
    "plans/contract-registry.md"
    "plans/system-roadmap.md"
    "plans/active/README.md"
    "plans/completed/README.md"
    "templates/prd-template.md"
    "templates/architecture-template.md"
    "templates/application-runbook.md"
    "templates/contract-registry-template.md"
    "templates/ui-prototype-registry-template.md"
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

# 4. Install /ntc-* Slash Command Skills into workspace (.agents/skills/)
NTC_SKILLS=("ntc-init" "ntc-prototype" "ntc-spec" "ntc-modules" "ntc-plan" "ntc-run" "ntc-cr" "ntc-status")
for skill in "${NTC_SKILLS[@]}"; do
    SRC_SKILL="${SOURCE_DIR}/skills/${skill}/SKILL.md"
    DST_SKILL="${TARGET_DIR}/.agents/skills/${skill}/SKILL.md"
    if [ -f "${SRC_SKILL}" ]; then
        mkdir -p "$(dirname "${DST_SKILL}")"
        if [ ! -f "${DST_SKILL}" ]; then
            cp "${SRC_SKILL}" "${DST_SKILL}"
            echo "  [+] Installed slash skill /${skill} -> .agents/skills/${skill}/SKILL.md"
        fi
    fi
done

# 5. Agent rule files
AGENT_FILES=(".cursorrules" "CLAUDE.md" ".windsurfrules")
for rule_file in "${AGENT_FILES[@]}"; do
    DST_RULE="${TARGET_DIR}/${rule_file}"
    if [ ! -f "${DST_RULE}" ]; then
        cat << 'EOF' > "${DST_RULE}"
<!-- HARNESS:BEGIN -->
Always adhere strictly to the 6-Step Atomic Engineering Protocol defined in `AGENTS.md` and `docs/WORKFLOW.md`.
- Slash Commands: `/ntc-init` (Step 1: Git remote + Q&A -> `PRD.md` & `ARCHITECTURE.md`) -> `/ntc-prototype` (Step 2: HTML UI Prototypes `SCR-<MOD>-<NN>`) -> `/ntc-spec` (Step 3: Overall `SPEC.md` + `ai-skill-maps.md`) -> `/ntc-modules` (Step 4: `docs/modules-spec/<slug>.md` + `STEP-by-STEP.md`) -> `/ntc-plan` (Step 5: All Phase Dossiers WBS) -> `/ntc-run` (Step 6: `1 Turn = 1 Atomic Task`).
- Note: `STEP-by-STEP.md` is strictly for the Human Architect; AI Agents must NOT read it.
- Implement exactly ONE Atomic Task per turn (with 1:1 UI Prototype Parity for `SCR-<MOD>-<NN>` tasks and `/ntc-cr` Delta Change Request handling). Never generate incomplete stubs.
- Update the `🎫 Resume Ticket`, run `python scripts/validate_plans.py --fix`, and create an Atomic Git Commit checkpoint before concluding any turn.
<!-- HARNESS:END -->
EOF
        echo "  [+] Configured agent rule: ${rule_file}"
    fi
done

echo ""
echo "=========================================================="
echo " SUCCESS: NTC Micro Harness v2.1 (Plugin Edition) installed!"
echo "=========================================================="
echo "Start your project with the 6-Step /ntc-* Slash Commands:"
echo "  1. /ntc-init       -> Connect Git repo (optional) + Q&A -> PRD.md & ARCHITECTURE.md"
echo "  2. /ntc-prototype  -> Build & approve interactive HTML UI Prototypes (SCR-<MOD>-<NN>)"
echo "  3. /ntc-spec       -> Lock overall SPEC.md + Roadmap + Contracts + ai-skill-maps.md"
echo "  4. /ntc-modules    -> Author detailed docs/modules-spec/<slug>.md + STEP-by-STEP.md"
echo "  5. /ntc-plan       -> Pre-generate all Phase Dossiers & Level-4 Atomic WBS"
echo "  6. /ntc-run        -> Execute 1 Atomic Task per turn + 1:1 UI Parity + Auto Git Commit"
echo ""
