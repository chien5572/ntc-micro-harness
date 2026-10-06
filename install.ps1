<#
.SYNOPSIS
    Automated installation script for NTC Micro Harness (Windows PowerShell).
.DESCRIPTION
    Installs the Atomic Engineering Protocol (Microservices Edition) into a target project.
.PARAMETER TargetPath
    Path to the target project directory. Defaults to current directory.
.PARAMETER AgentRules
    Configure agent rule files: 'all', 'claude', 'cursor', 'windsurf', 'none'. Default is 'all'.
.PARAMETER Force
    Overwrite existing files if present.
.EXAMPLE
    .\install.ps1 -TargetPath "C:\Projects\MyService"
#>
[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$TargetPath = ".",

    [Parameter()]
    [string[]]$AgentRules = @("all"),

    [Parameter()]
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$sourceRoot = $PSScriptRoot
$resolvedTarget = (Resolve-Path -Path $TargetPath -ErrorAction SilentlyContinue)
if (-not $resolvedTarget) {
    New-Item -ItemType Directory -Path $TargetPath -Force | Out-Null
    $resolvedTarget = (Resolve-Path -Path $TargetPath)
}
$targetPath = $resolvedTarget.Path

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Installing NTC Micro Harness into: $targetPath" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Install or update AGENTS.md
$srcAgents = Join-Path $sourceRoot "AGENTS.md"
$dstAgents = Join-Path $targetPath "AGENTS.md"

if (-not (Test-Path $dstAgents) -or $Force) {
    Copy-Item -Path $srcAgents -Destination $dstAgents -Force
    Write-Host "  [+] Created AGENTS.md" -ForegroundColor Green
} else {
    $existing = Get-Content -Path $dstAgents -Raw -Encoding UTF8
    if ($existing -match "<!-- HARNESS:BEGIN -->") {
        Write-Host "  [.] AGENTS.md already contains Harness block (skipping)" -ForegroundColor Yellow
    } else {
        $block = Get-Content -Path $srcAgents -Raw -Encoding UTF8
        "$existing`n`n$block" | Set-Content -Path $dstAgents -Encoding UTF8
        Write-Host "  [+] Appended Harness protocol block to existing AGENTS.md" -ForegroundColor Green
    }
}

# 2. Copy docs structure
$srcDocs = Join-Path $sourceRoot "docs"
$dstDocs = Join-Path $targetPath "docs"

$docsItems = @(
    "WORKFLOW.md",
    "README.md",
    "patterns\encoding-invariants.md",
    "plans\README.md",
    "plans\contract-registry.md",
    "plans\system-roadmap.md",
    "plans\active\README.md",
    "plans\completed\README.md",
    "plans\modules\README.md",
    "templates\application-runbook.md",
    "templates\contract-registry-template.md",
    "templates\decision.md",
    "templates\exec-plan.md",
    "templates\module-roadmap-template.md",
    "templates\phase-dossier-template.md",
    "templates\spec-template.md",
    "templates\system-roadmap-template.md"
)

foreach ($item in $docsItems) {
    $src = Join-Path $srcDocs $item
    $dst = Join-Path $dstDocs $item
    if (Test-Path $src) {
        $dstDir = Split-Path -Path $dst -Parent
        if (-not (Test-Path $dstDir)) {
            New-Item -ItemType Directory -Path $dstDir -Force | Out-Null
        }
        if (-not (Test-Path $dst) -or $Force) {
            Copy-Item -Path $src -Destination $dst -Force
            Write-Host "  [+] Created docs\$item" -ForegroundColor Green
        } else {
            Write-Host "  [.] docs\$item already exists (skipping)" -ForegroundColor Yellow
        }
    }
}

# 3. Copy scripts/validate-plans.ps1
$srcScript = Join-Path $sourceRoot "scripts\validate-plans.ps1"
$dstScript = Join-Path $targetPath "scripts\validate-plans.ps1"
if (Test-Path $srcScript) {
    $dstScriptDir = Split-Path -Path $dstScript -Parent
    if (-not (Test-Path $dstScriptDir)) {
        New-Item -ItemType Directory -Path $dstScriptDir -Force | Out-Null
    }
    if (-not (Test-Path $dstScript) -or $Force) {
        Copy-Item -Path $srcScript -Destination $dstScript -Force
        Write-Host "  [+] Created scripts\validate-plans.ps1" -ForegroundColor Green
    }
}

# 4. Agent rule integrations
$agentTemplates = @{
    "CLAUDE.md" = @"
# Claude Code Instructions

<!-- HARNESS:BEGIN -->
Always adhere strictly to the Atomic Engineering Protocol defined in `AGENTS.md` and `docs/WORKFLOW.md`.
- Read `SPEC.md` and `AGENTS.md` first. Never start coding without an approved System Roadmap and Phase Dossier.
- Enforce the 5-Stage Gated Lifecycle and Single Atomic Task Turn (1 Turn = 1 Micro-task).
- Always verify work with executable proof before completing a task.
- Update the `🎫 Resume Ticket` before yielding your turn.
<!-- HARNESS:END -->
"@
    ".cursorrules" = @"
# Cursor Agent Rules

<!-- HARNESS:BEGIN -->
Always adhere strictly to the Atomic Engineering Protocol defined in `AGENTS.md` and `docs/WORKFLOW.md`.
- Hierarchy of Truth: SPEC.md > AGENTS.md > docs/plans/system-roadmap.md > docs/plans/active/<module>/phase-*.md.
- Never write production code during Gate 1 (Specification Ingestion) or Gate 2 (Roadmap Alignment).
- Implement exactly ONE Atomic Task per turn. Never generate incomplete stubs (no TODOs).
- Update the `🎫 Resume Ticket` in the active dossier before concluding any turn.
<!-- HARNESS:END -->
"@
    ".windsurfrules" = @"
# Windsurf Cascade Rules

<!-- HARNESS:BEGIN -->
Adhere strictly to the Atomic Engineering Protocol defined in `AGENTS.md` and `docs/WORKFLOW.md`.
- Read SPEC.md and AGENTS.md before taking any architectural actions.
- Maintain single-module boundaries and contract-first invariants.
- Update the `🎫 Resume Ticket` in the active phase dossier before yielding.
<!-- HARNESS:END -->
"@
}

if ($AgentRules -notcontains "none") {
    foreach ($ruleName in $agentTemplates.Keys) {
        $shouldInstall = ($AgentRules -contains "all") -or ($AgentRules -contains $ruleName.TrimStart('.').Split('r')[0].ToLower())
        if ($shouldInstall) {
            $ruleDst = Join-Path $targetPath $ruleName
            $content = $agentTemplates[$ruleName]
            if (-not (Test-Path $ruleDst) -or $Force) {
                Set-Content -Path $ruleDst -Value $content -Encoding UTF8
                Write-Host "  [+] Configured agent rule: $ruleName" -ForegroundColor Green
            } else {
                $cur = Get-Content -Path $ruleDst -Raw -Encoding UTF8
                if ($cur -notmatch "<!-- HARNESS:BEGIN -->") {
                    "$cur`n`n$content" | Set-Content -Path $ruleDst -Encoding UTF8
                    Write-Host "  [+] Appended harness rule to: $ruleName" -ForegroundColor Green
                }
            }
        }
    }
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " SUCCESS: NTC Micro Harness installed successfully!" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor White
Write-Host "  1. Draft your project requirements in `SPEC.md` using `docs/templates/spec-template.md`."
Write-Host "  2. Start your AI Agent (Antigravity, Claude Code, Cursor, Windsurf) and prompt:"
Write-Host "     'Read SPEC.md and AGENTS.md to collaboratively build our System Roadmap.'" -ForegroundColor Yellow
Write-Host "  3. Validate planning documents at any time using:"
Write-Host "     powershell -ExecutionPolicy Bypass -File scripts/validate-plans.ps1`n"
