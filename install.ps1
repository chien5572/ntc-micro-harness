<#
.SYNOPSIS
    Automated installation script for NTC Micro-Harness v2.1 Plugin Edition (Windows PowerShell / PowerShell Core).
.DESCRIPTION
    Installs the 6-Step Atomic Engineering Protocol & `/ntc-*` Plugin into:
      1. Global Antigravity Plugin directory (`~/.gemini/config/plugins/ntc-micro-harness`) for Antigravity 2.0, IDE, and CLI (`agy`).
      2. Target project workspace (`.` by default).
.PARAMETER TargetPath
    Path to the target project directory. Defaults to current directory (`.`).
.PARAMETER RepoUrl
    Optional Git remote repository URL to connect (`origin`) right up front.
.PARAMETER PluginOnly
    Only install the global Antigravity plugin (`~/.gemini/config/plugins/ntc-micro-harness`) without modifying the current folder.
.PARAMETER NoPlugin
    Skip installing the global Antigravity plugin.
.PARAMETER AgentRules
    Configure agent rule files: 'all', 'claude', 'cursor', 'windsurf', 'none'. Default is 'all'.
.PARAMETER Force
    Overwrite existing files if present.
#>
[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$TargetPath = ".",

    [Parameter()]
    [string]$RepoUrl = "",

    [Parameter()]
    [switch]$PluginOnly,

    [Parameter()]
    [switch]$NoPlugin,

    [Parameter()]
    [string[]]$AgentRules = @("all"),

    [Parameter()]
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$RepoGitUrl = "https://github.com/chien5572/ntc-micro-harness.git"
$RepoZipUrl = "https://github.com/chien5572/ntc-micro-harness/archive/refs/heads/main.zip"
$ntcSkills = @("ntc-init", "ntc-prototype", "ntc-spec", "ntc-modules", "ntc-plan", "ntc-run", "ntc-cr", "ntc-status")

$tempExtractDir = $null
$sourceRoot = $PSScriptRoot

function Install-GlobalAntigravityPlugin([string]$srcRoot) {
    $globalPluginDir = Join-Path $HOME ".gemini\config\plugins\ntc-micro-harness"
    New-Item -ItemType Directory -Path $globalPluginDir -Force | Out-Null
    foreach ($pFile in @("plugin.json", ".claude-plugin\plugin.json", "assets\logo.svg", "rules\AGENTS.md", "README.md", "README.vi.md")) {
        $sP = Join-Path $srcRoot $pFile
        $dP = Join-Path $globalPluginDir $pFile
        if (Test-Path $sP) {
            New-Item -ItemType Directory -Path (Split-Path $dP -Parent) -Force | Out-Null
            Copy-Item -Path $sP -Destination $dP -Force
        }
    }
    foreach ($skill in $ntcSkills) {
        $sS = Join-Path $srcRoot "skills\$skill\SKILL.md"
        $dS = Join-Path $globalPluginDir "skills\$skill\SKILL.md"
        if (Test-Path $sS) {
            New-Item -ItemType Directory -Path (Split-Path $dS -Parent) -Force | Out-Null
            Copy-Item -Path $sS -Destination $dS -Force
        }
    }
    Write-Host "  [+] Installed Global Antigravity Plugin (2.0 / IDE / CLI) at: $globalPluginDir" -ForegroundColor Green
}

try {
    if ([string]::IsNullOrWhiteSpace($sourceRoot) -or -not (Test-Path (Join-Path $sourceRoot "AGENTS.md")) -or -not (Test-Path (Join-Path $sourceRoot "docs\WORKFLOW.md"))) {
        $tempExtractDir = Join-Path ([System.IO.Path]::GetTempPath()) ("ntc-harness-" + [Guid]::NewGuid().ToString("N"))
        New-Item -ItemType Directory -Path $tempExtractDir -Force | Out-Null
        Write-Host "[*] Fetching NTC Micro-Harness v2.1 from $RepoGitUrl ..." -ForegroundColor Cyan

        $gitCmd = Get-Command git -ErrorAction SilentlyContinue
        if ($gitCmd) {
            $cloneDir = Join-Path $tempExtractDir "repo"
            git clone --depth 1 --quiet $RepoGitUrl $cloneDir
            $sourceRoot = $cloneDir
        } else {
            $zipPath = Join-Path $tempExtractDir "harness.zip"
            Invoke-WebRequest -Uri $RepoZipUrl -OutFile $zipPath -UseBasicParsing
            Expand-Archive -Path $zipPath -DestinationPath $tempExtractDir -Force
            $extracted = Get-ChildItem -Path $tempExtractDir -Directory | Where-Object { Test-Path (Join-Path $_.FullName "AGENTS.md") } | Select-Object -First 1
            if (-not $extracted) {
                throw "Failed to extract NTC Micro-Harness archive."
            }
            $sourceRoot = $extracted.FullName
        }
    }

    if ($PluginOnly) {
        Write-Host "==========================================================" -ForegroundColor Cyan
        Write-Host " Installing NTC Micro-Harness v2.1 Global Plugin Only" -ForegroundColor Cyan
        Write-Host "==========================================================" -ForegroundColor Cyan
        Install-GlobalAntigravityPlugin -srcRoot $sourceRoot
        Write-Host "`nSUCCESS: Restart Antigravity 2.0 / Antigravity IDE / agy CLI to use /ntc-* commands.`n" -ForegroundColor Green
        return
    }

    $resolvedTarget = (Resolve-Path -Path $TargetPath -ErrorAction SilentlyContinue)
    if (-not $resolvedTarget) {
        New-Item -ItemType Directory -Path $TargetPath -Force | Out-Null
        $resolvedTarget = (Resolve-Path -Path $TargetPath)
    }
    $targetPath = $resolvedTarget.Path

    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host " Installing NTC Micro-Harness v2.1 into: $targetPath" -ForegroundColor Cyan
    Write-Host "==========================================================" -ForegroundColor Cyan

    # 0. Optional Git Repo Connection
    if (-not [string]::IsNullOrWhiteSpace($RepoUrl)) {
        if (-not (Test-Path (Join-Path $targetPath ".git"))) {
            Push-Location $targetPath
            git init | Out-Null
            Pop-Location
            Write-Host "  [+] Initialized Git repository in $targetPath" -ForegroundColor Green
        }
        Push-Location $targetPath
        $hasOrigin = git remote | Where-Object { $_ -eq "origin" }
        if ($hasOrigin) {
            git remote set-url origin $RepoUrl
        } else {
            git remote add origin $RepoUrl
        }
        Pop-Location
        Write-Host "  [+] Connected Git remote 'origin' -> $RepoUrl" -ForegroundColor Green
    }

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
        "modules-spec\README.md",
        "prototypes\README.md",
        "prototypes\registry.md",
        "patterns\encoding-invariants.md",
        "plans\README.md",
        "plans\contract-registry.md",
        "plans\system-roadmap.md",
        "plans\active\README.md",
        "plans\completed\README.md",
        "templates\prd-template.md",
        "templates\architecture-template.md",
        "templates\application-runbook.md",
        "templates\contract-registry-template.md",
        "templates\ui-prototype-registry-template.md",
        "templates\decision.md",
        "templates\exec-plan.md",
        "templates\module-spec-template.md",
        "templates\ai-skill-maps-template.md",
        "templates\step-by-step-template.md",
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

    # 3. Copy scripts/validate_plans.py
    $srcScript = Join-Path $sourceRoot "scripts\validate_plans.py"
    $dstScript = Join-Path $targetPath "scripts\validate_plans.py"
    if (Test-Path $srcScript) {
        $dstScriptDir = Split-Path -Path $dstScript -Parent
        if (-not (Test-Path $dstScriptDir)) {
            New-Item -ItemType Directory -Path $dstScriptDir -Force | Out-Null
        }
        if (-not (Test-Path $dstScript) -or $Force) {
            Copy-Item -Path $srcScript -Destination $dstScript -Force
            Write-Host "  [+] Created scripts\validate_plans.py" -ForegroundColor Green
        }
    }

    # 4. Copy /ntc-* Slash Command Skills into workspace (.agents/skills/)
    foreach ($skill in $ntcSkills) {
        $srcSkill = Join-Path $sourceRoot "skills\$skill\SKILL.md"
        $dstSkill = Join-Path $targetPath ".agents\skills\$skill\SKILL.md"
        if (Test-Path $srcSkill) {
            $dstSkillDir = Split-Path -Path $dstSkill -Parent
            if (-not (Test-Path $dstSkillDir)) {
                New-Item -ItemType Directory -Path $dstSkillDir -Force | Out-Null
            }
            if (-not (Test-Path $dstSkill) -or $Force) {
                Copy-Item -Path $srcSkill -Destination $dstSkill -Force
                Write-Host "  [+] Installed slash skill /$skill -> .agents\skills\$skill\SKILL.md" -ForegroundColor Green
            }
        }
    }

    # 5. Global Antigravity Plugin Installation (~/.gemini/config/plugins/ntc-micro-harness)
    if (-not $NoPlugin) {
        Install-GlobalAntigravityPlugin -srcRoot $sourceRoot
    }

    # 6. Agent rule integrations
    $agentTemplates = @{
        "CLAUDE.md" = @"
# Claude Code Instructions

<!-- HARNESS:BEGIN -->
Always adhere strictly to the 6-Step Atomic Engineering Protocol defined in `AGENTS.md` and `docs/WORKFLOW.md`.
- Slash Commands: `/ntc-init` (Step 1: Git remote + Q&A -> `PRD.md` & `ARCHITECTURE.md`) -> `/ntc-prototype` (Step 2: HTML UI Prototypes `SCR-<MOD>-<NN>`) -> `/ntc-spec` (Step 3: Overall `SPEC.md` + `ai-skill-maps.md`) -> `/ntc-modules` (Step 4: `docs/modules-spec/<slug>.md` + `STEP-by-STEP.md`) -> `/ntc-plan` (Step 5: All Phase Dossiers WBS) -> `/ntc-run` (Step 6: `1 Turn = 1 Atomic Task`).
- Note: `STEP-by-STEP.md` is strictly for the Human Architect; AI Agents must NOT read it.
- Enforce 1:1 UI Prototype Parity (`SCR-<MOD>-<NN>`), `/ntc-cr` (`CR-<NN>`) Delta Change Requests, and Single Atomic Task Turn (`1 Turn = 1 Task`).
- Update the `🎫 Resume Ticket`, run `python scripts/validate_plans.py --fix`, and create an Atomic Git Commit checkpoint before yielding.
<!-- HARNESS:END -->
"@
        ".cursorrules" = @"
# Cursor Agent Rules

<!-- HARNESS:BEGIN -->
Always adhere strictly to the 6-Step Atomic Engineering Protocol defined in `AGENTS.md` and `docs/WORKFLOW.md`.
- Slash Commands: `/ntc-init` -> `/ntc-prototype` -> `/ntc-spec` -> `/ntc-modules` -> `/ntc-plan` -> `/ntc-run` -> `/ntc-cr` -> `/ntc-status`.
- Never read `STEP-by-STEP.md` (Human-Only Playbook).
- Implement exactly ONE Atomic Task per turn (with 1:1 UI Prototype Parity for `SCR-<MOD>-<NN>` tasks). Never generate incomplete stubs (no TODOs).
- Update the `🎫 Resume Ticket`, run `python scripts/validate_plans.py --fix`, and create an Atomic Git Commit checkpoint before concluding any turn.
<!-- HARNESS:END -->
"@
        ".windsurfrules" = @"
# Windsurf Cascade Rules

<!-- HARNESS:BEGIN -->
Adhere strictly to the 6-Step Atomic Engineering Protocol defined in `AGENTS.md` and `docs/WORKFLOW.md`.
- Follow `/ntc-init` -> `/ntc-prototype` -> `/ntc-spec` -> `/ntc-modules` -> `/ntc-plan` -> `/ntc-run` (do not read `STEP-by-STEP.md`).
- Maintain single-module boundaries, contract-first invariants, 1:1 UI prototype parity, `/ntc-cr` delta change control, and the `/ntc-run` / `"tiếp tục"` state machine.
- Update the `🎫 Resume Ticket`, run `python scripts/validate_plans.py --fix`, and create an Atomic Git Commit checkpoint before yielding.
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
    Write-Host " SUCCESS: NTC Micro-Harness v2.1 (Plugin Edition) installed!" -ForegroundColor Cyan
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host "Start your project with the 6-Step /ntc-* Slash Commands:" -ForegroundColor White
    Write-Host "  1. /ntc-init       -> Connect Git repo (optional) + Q&A -> PRD.md & ARCHITECTURE.md" -ForegroundColor Yellow
    Write-Host "  2. /ntc-prototype  -> Build & approve interactive HTML UI Prototypes (SCR-<MOD>-<NN>)"
    Write-Host "  3. /ntc-spec       -> Lock overall SPEC.md + Roadmap + Contracts + ai-skill-maps.md"
    Write-Host "  4. /ntc-modules    -> Author detailed docs/modules-spec/<slug>.md + STEP-by-STEP.md"
    Write-Host "  5. /ntc-plan       -> Pre-generate all Phase Dossiers & Level-4 Atomic WBS"
    Write-Host "  6. /ntc-run        -> Execute 1 Atomic Task per turn + 1:1 UI Parity + Auto Git Commit`n"
} finally {
    if ($tempExtractDir -and (Test-Path $tempExtractDir)) {
        Remove-Item -Path $tempExtractDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}
