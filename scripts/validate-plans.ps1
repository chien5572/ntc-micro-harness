<#
.SYNOPSIS
    Validates the Harness planning hierarchy (Microservices Edition).

.DESCRIPTION
    Mechanically enforces the structural rules defined in AGENTS.md and
    docs/WORKFLOW.md:
      - required harness documents and templates exist;
      - AGENTS.md keeps exactly one HARNESS:BEGIN / HARNESS:END block;
      - Module Registry rows are well-formed; the reserved SYS module exists;
        non-PLANNED modules have a blueprint in docs/plans/modules/;
      - Contract Registry rows are well-formed; providers/consumers are
        registered modules; AVAILABLE contracts have an existing spec file;
      - Global Phases reference registered modules;
      - docs/plans/active|completed contain only <module-slug>/ folders with
        phase-<NN>-<slug>.md or plan-<slug>.md files; at most one active phase
        dossier per module; no flat (legacy) dossiers;
      - active dossiers carry a Resume Ticket naming the right module;
        Major/Atomic Task IDs use the <MOD>-P<NN> prefix of their file;
        archived dossiers have no unchecked Atomic Tasks;
      - Module Blueprint phase tables agree with the dossiers on disk;
      - the Active Work Pointer lists exactly the active phase dossiers.

    Exit code 0 = valid (warnings allowed), 1 = violations found.

.PARAMETER Root
    Repository root. Defaults to the parent directory of this script.

.EXAMPLE
    powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate-plans.ps1
#>
[CmdletBinding()]
param(
    [string]$Root = ''
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

# $PSScriptRoot is not available in param defaults on Windows PowerShell 5.1.
if ([string]::IsNullOrEmpty($Root)) {
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $Root = Split-Path -Parent $scriptDir
}
$Root = (Resolve-Path -LiteralPath $Root).ProviderPath

$EmDash = [string][char]0x2014
$script:Errors = New-Object System.Collections.Generic.List[string]
$script:Warnings = New-Object System.Collections.Generic.List[string]

$ModuleStatuses   = @('PLANNED', 'BLUEPRINT_REVIEW', 'READY', 'IN_PROGRESS', 'COMPLETED')
$GlobalStatuses   = @('PENDING', 'ACTIVE', 'COMPLETED')
$PhaseStatuses    = @('PENDING', 'ACTIVE', 'BLOCKED', 'COMPLETED')
$ContractStatuses = @('DRAFT', 'AVAILABLE', 'DEPRECATED')
$ContractTypes    = @('REST', 'gRPC', 'Event', 'Schema', 'Library')

$CodePattern     = '^[A-Z]{2,5}$'
$SlugPattern     = '^[a-z0-9]+(-[a-z0-9]+)*$'
$PhaseFilePattern = '^phase-(\d{2})-[a-z0-9]+(-[a-z0-9]+)*\.md$'
$PlanFilePattern  = '^plan-[a-z0-9]+(-[a-z0-9]+)*\.md$'

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

function Add-Violation {
    param([string]$Rule, [string]$Where, [string]$Message, [string]$Fix)
    $script:Errors.Add(("[{0}] {1}: {2}`n      -> {3}" -f $Rule, $Where, $Message, $Fix))
}

function Add-Warning {
    param([string]$Rule, [string]$Where, [string]$Message, [string]$Fix)
    $script:Warnings.Add(("[{0}] {1}: {2}`n      -> {3}" -f $Rule, $Where, $Message, $Fix))
}

function Get-RepoPath {
    param([string]$Relative)
    return (Join-Path $Root ($Relative -replace '/', [System.IO.Path]::DirectorySeparatorChar))
}

function Read-Lines {
    param([string]$Relative)
    return [System.IO.File]::ReadAllLines((Get-RepoPath $Relative), [System.Text.Encoding]::UTF8)
}

# Returns @{ Found = bool; Lines = string[] } for the body of the first level-1/2
# heading matching $HeadingPattern (until the next level-1/2 heading). Headings
# inside fenced code blocks are ignored.
function Get-Section {
    param([string[]]$Lines, [string]$HeadingPattern)
    $body = New-Object System.Collections.Generic.List[string]
    $inside = $false
    $inFence = $false
    foreach ($line in $Lines) {
        if ($line -match '^\s*```') { $inFence = -not $inFence }
        if (-not $inFence -and $line -match '^#{1,2}\s') {
            if ($inside) { break }
            if ($line -match $HeadingPattern) { $inside = $true; continue }
        }
        if ($inside) { $body.Add($line) }
    }
    return @{ Found = $inside; Lines = $body.ToArray() }
}

function Split-Row {
    param([string]$Line)
    $trimmed = $Line.Trim()
    if ($trimmed.StartsWith('|')) { $trimmed = $trimmed.Substring(1) }
    if ($trimmed.EndsWith('|')) { $trimmed = $trimmed.Substring(0, $trimmed.Length - 1) }
    return @($trimmed.Split('|') | ForEach-Object { $_.Trim() })
}

function Clear-Cell {
    param([string]$Cell)
    return ($Cell -replace '`', '').Trim()
}

function Test-Placeholder {
    param([string]$Cell)
    $c = Clear-Cell $Cell
    return ($c -eq '' -or $c -eq $EmDash -or $c -eq '-' -or $c -eq '...' -or $c -match '^\*.*\*$')
}

# Parses the first markdown table in $Lines. Returns @{ Found; Headers; Rows }
# where each row is a hashtable keyed by header name (raw cell text).
function Get-Table {
    param([string[]]$Lines)
    $headers = $null
    $rows = New-Object System.Collections.Generic.List[hashtable]
    $state = 'seek'
    foreach ($line in $Lines) {
        $isRow = $line.Trim().StartsWith('|')
        if ($state -eq 'seek') {
            if ($isRow) { $headers = @(Split-Row $line); $state = 'separator' }
            continue
        }
        if ($state -eq 'separator') { $state = 'rows'; continue }
        if (-not $isRow) { break }
        $cells = @(Split-Row $line)
        $row = @{}
        for ($i = 0; $i -lt $headers.Count; $i++) {
            if ($i -lt $cells.Count) { $row[$headers[$i]] = $cells[$i] } else { $row[$headers[$i]] = '' }
        }
        $rows.Add($row)
    }
    return @{ Found = ($null -ne $headers); Headers = $headers; Rows = $rows.ToArray() }
}

function Assert-Headers {
    param($Table, [string[]]$Required, [string]$Where)
    $ok = $true
    foreach ($h in $Required) {
        if (-not ($Table.Headers -contains $h)) {
            Add-Violation 'TABLE_HEADER' $Where "missing column '$h'" 'Restore the table header names from the matching template in docs/templates/.'
            $ok = $false
        }
    }
    return $ok
}

# Returns @{ Table; Where } or $null after reporting a violation.
function Get-RequiredTable {
    param([string]$Relative, [string]$HeadingPattern, [string]$HeadingLabel, [string[]]$Required)
    $section = Get-Section (Read-Lines $Relative) $HeadingPattern
    $where = "$Relative ($HeadingLabel)"
    if (-not $section.Found) {
        Add-Violation 'SECTION_MISSING' $Relative "heading '$HeadingLabel' not found" 'Restore the section heading from the matching template in docs/templates/.'
        return $null
    }
    $table = Get-Table $section.Lines
    if (-not $table.Found) {
        Add-Violation 'TABLE_MISSING' $where 'no markdown table found' 'Restore the table from the matching template in docs/templates/.'
        return $null
    }
    if (-not (Assert-Headers $table $Required $where)) { return $null }
    return @{ Table = $table; Label = $where; Section = $section }
}

function Get-DossierFiles {
    param([string]$Area, [string]$Slug)
    $dir = Get-RepoPath "docs/plans/$Area/$Slug"
    if (-not (Test-Path -LiteralPath $dir -PathType Container)) { return @() }
    return @(Get-ChildItem -LiteralPath $dir -File | Where-Object { $_.Name -match $PhaseFilePattern })
}

# ---------------------------------------------------------------------------
# 1. Required documents
# ---------------------------------------------------------------------------

$required = @(
    'AGENTS.md',
    'docs/WORKFLOW.md',
    'docs/plans/README.md',
    'docs/plans/system-roadmap.md',
    'docs/plans/contract-registry.md',
    'docs/plans/modules/README.md',
    'docs/plans/active/README.md',
    'docs/plans/completed/README.md',
    'docs/templates/spec-template.md',
    'docs/templates/system-roadmap-template.md',
    'docs/templates/contract-registry-template.md',
    'docs/templates/module-roadmap-template.md',
    'docs/templates/phase-dossier-template.md',
    'docs/templates/exec-plan.md'
)
foreach ($rel in $required) {
    if (-not (Test-Path -LiteralPath (Get-RepoPath $rel) -PathType Leaf)) {
        Add-Violation 'REQUIRED_FILE' $rel 'required harness document is missing' 'Restore it from the harness distribution or its template.'
    }
}

$roadmapRel = 'docs/plans/system-roadmap.md'
$registryRel = 'docs/plans/contract-registry.md'
$hasRoadmap = Test-Path -LiteralPath (Get-RepoPath $roadmapRel) -PathType Leaf
$hasRegistry = Test-Path -LiteralPath (Get-RepoPath $registryRel) -PathType Leaf

# ---------------------------------------------------------------------------
# 2. AGENTS.md harness markers
# ---------------------------------------------------------------------------

if (Test-Path -LiteralPath (Get-RepoPath 'AGENTS.md') -PathType Leaf) {
    $agents = Read-Lines 'AGENTS.md'
    $begin = @($agents | Select-String -SimpleMatch '<!-- HARNESS:BEGIN -->')
    $end = @($agents | Select-String -SimpleMatch '<!-- HARNESS:END -->')
    if ($begin.Count -ne 1 -or $end.Count -ne 1) {
        Add-Violation 'HARNESS_MARKERS' 'AGENTS.md' ("expected exactly one BEGIN and one END marker, found {0} and {1}" -f $begin.Count, $end.Count) 'Keep a single <!-- HARNESS:BEGIN --> ... <!-- HARNESS:END --> block.'
    }
    elseif ($begin[0].LineNumber -gt $end[0].LineNumber) {
        Add-Violation 'HARNESS_MARKERS' 'AGENTS.md' 'HARNESS:END appears before HARNESS:BEGIN' 'Reorder the markers.'
    }
}

# ---------------------------------------------------------------------------
# 3. Module Registry
# ---------------------------------------------------------------------------

$slugToCode = @{}
$codeToSlug = @{}
$moduleStatus = @{}

if ($hasRoadmap) {
    $reg = Get-RequiredTable $roadmapRel '^## 2\. Module Registry' '## 2. Module Registry' @('Code', 'Slug', 'Code Root', 'Blueprint', 'Status')
    if ($null -ne $reg) {
        foreach ($row in $reg.Table.Rows) {
            if (Test-Placeholder $row['Code']) { continue }
            $code = Clear-Cell $row['Code']
            $slug = Clear-Cell $row['Slug']
            $status = Clear-Cell $row['Status']
            $where = "$($reg.Label) row '$code'"
            if ($code -notmatch $CodePattern) {
                Add-Violation 'MODULE_CODE' $where "module code '$code' is not 2-5 uppercase letters" 'Use a code such as AUTH or ORD (docs/WORKFLOW.md section 2).'
                continue
            }
            if ($slug -notmatch $SlugPattern) {
                Add-Violation 'MODULE_SLUG' $where "slug '$slug' is not lowercase kebab-case" 'Use a slug such as auth or order-history.'
                continue
            }
            if ($codeToSlug.ContainsKey($code)) {
                Add-Violation 'MODULE_DUPLICATE' $where "module code '$code' is registered twice" 'Module codes are assigned once and never reused.'
                continue
            }
            if ($slugToCode.ContainsKey($slug)) {
                Add-Violation 'MODULE_DUPLICATE' $where "slug '$slug' is registered twice" 'Module slugs are assigned once and never reused.'
                continue
            }
            $codeToSlug[$code] = $slug
            $slugToCode[$slug] = $code
            $moduleStatus[$code] = $status

            if ($ModuleStatuses -cnotcontains $status) {
                Add-Violation 'MODULE_STATUS' $where "status '$status' is not one of $($ModuleStatuses -join ' | ')" 'Use a status from the template legend.'
            }
            $expectedBlueprint = "docs/plans/modules/$slug.md"
            $blueprint = Clear-Cell $row['Blueprint']
            if ($blueprint -ne $expectedBlueprint) {
                Add-Violation 'BLUEPRINT_PATH' $where "blueprint path '$blueprint' should be '$expectedBlueprint'" 'Blueprints live at docs/plans/modules/<module-slug>.md.'
            }
            if ($status -ne 'PLANNED' -and -not (Test-Path -LiteralPath (Get-RepoPath $expectedBlueprint) -PathType Leaf)) {
                Add-Violation 'BLUEPRINT_MISSING' $where "status is '$status' but $expectedBlueprint does not exist" 'Create the blueprint from docs/templates/module-roadmap-template.md (Gate 3) or set status to PLANNED.'
            }
        }
        if (-not $codeToSlug.ContainsKey('SYS') -or $codeToSlug['SYS'] -ne 'system') {
            Add-Violation 'SYS_RESERVED' $reg.Label "reserved pseudo-module 'SYS' / 'system' is not registered" 'Register SYS with slug system for cross-cutting work.'
        }
    }
}

# Blueprint files must belong to registered modules.
$modulesDir = Get-RepoPath 'docs/plans/modules'
if (Test-Path -LiteralPath $modulesDir -PathType Container) {
    foreach ($f in @(Get-ChildItem -LiteralPath $modulesDir -File -Filter '*.md')) {
        if ($f.Name -eq 'README.md') { continue }
        $slug = [System.IO.Path]::GetFileNameWithoutExtension($f.Name)
        if (-not $slugToCode.ContainsKey($slug)) {
            Add-Violation 'BLUEPRINT_ORPHAN' "docs/plans/modules/$($f.Name)" "slug '$slug' is not in the Module Registry" 'Register the module in docs/plans/system-roadmap.md or remove the file.'
        }
    }
    foreach ($d in @(Get-ChildItem -LiteralPath $modulesDir -Directory)) {
        Add-Violation 'BLUEPRINT_LAYOUT' "docs/plans/modules/$($d.Name)/" 'blueprints are flat files, not folders' 'Use docs/plans/modules/<module-slug>.md; dossiers belong in docs/plans/active/<module-slug>/.'
    }
}

# ---------------------------------------------------------------------------
# 4. Contract Registry
# ---------------------------------------------------------------------------

if ($hasRegistry) {
    $ct = Get-RequiredTable $registryRel '^## 1\. Contracts' '## 1. Contracts' @('Contract ID', 'Type', 'Provider', 'Consumers', 'Spec Path', 'Version', 'Status')
    if ($null -ne $ct) {
        $seen = @{}
        foreach ($row in $ct.Table.Rows) {
            if (Test-Placeholder $row['Contract ID']) { continue }
            $id = Clear-Cell $row['Contract ID']
            $where = "$($ct.Label) row '$id'"
            if ($id -notmatch '^CT-([A-Z]{2,5})-(\d{2})$') {
                Add-Violation 'CONTRACT_ID' $where "contract ID '$id' does not match CT-<PROVIDER>-<NN>" 'Rename it, e.g. CT-AUTH-01.'
                continue
            }
            $idProvider = $Matches[1]
            if ($seen.ContainsKey($id)) {
                Add-Violation 'CONTRACT_DUPLICATE' $where "contract ID '$id' is registered twice" 'Contract IDs are unique; bump the version instead of duplicating.'
            }
            $seen[$id] = $true
            $provider = Clear-Cell $row['Provider']
            if ($provider -ne $idProvider) {
                Add-Violation 'CONTRACT_PROVIDER' $where "provider '$provider' does not match the ID prefix '$idProvider'" 'The provider code is part of the contract ID.'
            }
            if ($slugToCode.Count -gt 0 -and -not $codeToSlug.ContainsKey($provider)) {
                Add-Violation 'CONTRACT_PROVIDER' $where "provider '$provider' is not a registered module" 'Register the module in the Module Registry first.'
            }
            $consumersCell = Clear-Cell $row['Consumers']
            if (-not (Test-Placeholder $consumersCell)) {
                foreach ($c in ($consumersCell -split ',')) {
                    $c = $c.Trim()
                    if ($c -eq '') { continue }
                    if ($c -eq $provider) {
                        Add-Violation 'CONTRACT_CONSUMER' $where "provider '$c' is listed as its own consumer" 'Remove it from Consumers.'
                    }
                    elseif ($slugToCode.Count -gt 0 -and -not $codeToSlug.ContainsKey($c)) {
                        Add-Violation 'CONTRACT_CONSUMER' $where "consumer '$c' is not a registered module" 'Register the module or fix the code.'
                    }
                }
            }
            $type = Clear-Cell $row['Type']
            if ($ContractTypes -cnotcontains $type) {
                Add-Violation 'CONTRACT_TYPE' $where "type '$type' is not one of $($ContractTypes -join ' | ')" 'Use a type from the registry legend.'
            }
            $version = Clear-Cell $row['Version']
            if ($version -notmatch '^\d+\.\d+\.\d+$') {
                Add-Warning 'CONTRACT_VERSION' $where "version '$version' is not MAJOR.MINOR.PATCH" 'Use semantic versioning so change control can detect breaking changes.'
            }
            $status = Clear-Cell $row['Status']
            if ($ContractStatuses -cnotcontains $status) {
                Add-Violation 'CONTRACT_STATUS' $where "status '$status' is not one of $($ContractStatuses -join ' | ')" 'Use DRAFT, AVAILABLE, or DEPRECATED.'
            }
            $spec = Clear-Cell $row['Spec Path']
            if ($status -eq 'AVAILABLE') {
                if ((Test-Placeholder $spec) -or -not (Test-Path -LiteralPath (Get-RepoPath $spec))) {
                    Add-Violation 'CONTRACT_SPEC' $where "status is AVAILABLE but spec '$spec' does not exist" 'Codify the spec at the declared path (Contract-First) or set status back to DRAFT.'
                }
            }
        }
    }
}

# ---------------------------------------------------------------------------
# 5. Global Phase Sequence
# ---------------------------------------------------------------------------

if ($hasRoadmap) {
    $gp = Get-RequiredTable $roadmapRel '^## 3\. Global Phase Sequence' '## 3. Global Phase Sequence' @('GP', 'Participating Module Phases', 'Status')
    if ($null -ne $gp) {
        $seenGp = @{}
        foreach ($row in $gp.Table.Rows) {
            if (Test-Placeholder $row['GP']) { continue }
            $id = Clear-Cell $row['GP']
            $where = "$($gp.Label) row '$id'"
            if ($id -notmatch '^GP-\d{2}$') {
                Add-Violation 'GP_ID' $where "global phase ID '$id' does not match GP-<NN>" 'Rename it, e.g. GP-01.'
                continue
            }
            if ($seenGp.ContainsKey($id)) {
                Add-Violation 'GP_DUPLICATE' $where "global phase '$id' appears twice" 'Global phase IDs are unique.'
            }
            $seenGp[$id] = $true
            $status = Clear-Cell $row['Status']
            if ($GlobalStatuses -cnotcontains $status) {
                Add-Violation 'GP_STATUS' $where "status '$status' is not one of $($GlobalStatuses -join ' | ')" 'Use PENDING, ACTIVE, or COMPLETED.'
            }
            foreach ($m in [regex]::Matches($row['Participating Module Phases'], '\b([A-Z]{2,5})-P(\d{2})\b')) {
                $code = $m.Groups[1].Value
                if ($slugToCode.Count -gt 0 -and -not $codeToSlug.ContainsKey($code)) {
                    Add-Violation 'GP_MODULE' $where "phase '$($m.Value)' references unregistered module '$code'" 'Register the module or fix the phase ID.'
                }
                elseif ($status -eq 'COMPLETED' -and $codeToSlug.ContainsKey($code)) {
                    $done = @(Get-DossierFiles 'completed' $codeToSlug[$code] | Where-Object { $_.Name -match ('^phase-' + $m.Groups[2].Value + '-') })
                    if ($done.Count -eq 0) {
                        Add-Violation 'GP_COMPLETION' $where "marked COMPLETED but '$($m.Value)' has no dossier in docs/plans/completed/$($codeToSlug[$code])/" 'A global phase completes only when all its module phases are archived (docs/WORKFLOW.md 5.2).'
                    }
                }
            }
        }
    }
}

# ---------------------------------------------------------------------------
# 6. active/ and completed/ layout + dossier content
# ---------------------------------------------------------------------------

$activeDossiers = New-Object System.Collections.Generic.List[string]   # repo-relative paths
$dossierIndex = @{}   # "<area>|<slug>|<NN>" -> file name

foreach ($area in @('active', 'completed')) {
    $areaDir = Get-RepoPath "docs/plans/$area"
    if (-not (Test-Path -LiteralPath $areaDir -PathType Container)) { continue }

    foreach ($f in @(Get-ChildItem -LiteralPath $areaDir -File)) {
        if ($f.Name -eq 'README.md') { continue }
        Add-Violation 'FLAT_DOSSIER' "docs/plans/$area/$($f.Name)" 'files must live inside a module folder' "Move it to docs/plans/$area/<module-slug>/."
    }

    foreach ($dir in @(Get-ChildItem -LiteralPath $areaDir -Directory)) {
        $slug = $dir.Name
        $dirRel = "docs/plans/$area/$slug"
        if (-not $slugToCode.ContainsKey($slug)) {
            Add-Violation 'MODULE_FOLDER' "$dirRel/" "folder '$slug' is not a registered module slug" 'Register the module in docs/plans/system-roadmap.md or rename the folder.'
            continue
        }
        $code = $slugToCode[$slug]

        foreach ($sub in @(Get-ChildItem -LiteralPath $dir.FullName -Directory)) {
            Add-Violation 'NESTED_FOLDER' "$dirRel/$($sub.Name)/" 'module folders must not contain sub-folders' 'Keep dossiers directly in the module folder.'
        }

        $phaseFiles = New-Object System.Collections.Generic.List[object]
        foreach ($f in @(Get-ChildItem -LiteralPath $dir.FullName -File)) {
            $rel = "$dirRel/$($f.Name)"
            if ($f.Name -match $PhaseFilePattern) {
                $nn = $Matches[1]
                $phaseFiles.Add($f)
                $key = "$area|$slug|$nn"
                if ($dossierIndex.ContainsKey($key)) {
                    Add-Violation 'PHASE_DUPLICATE' $rel "phase $nn already has dossier '$($dossierIndex[$key])'" 'Keep a single dossier per module phase.'
                }
                $dossierIndex[$key] = $f.Name
                if ($area -eq 'active') { $activeDossiers.Add($rel) }

                $content = Read-Lines $rel
                $prefix = "$code-P$nn"

                if ($area -eq 'active') {
                    if (-not ($content | Where-Object { $_ -match '^## .*Resume Ticket' })) {
                        Add-Violation 'RESUME_TICKET' $rel 'no "## ... Resume Ticket" section' 'Restore the Resume Ticket block from docs/templates/phase-dossier-template.md.'
                    }
                    $moduleLine = @($content | Where-Object { $_ -match '^\s*- \*\*Module:\*\*' })
                    if ($moduleLine.Count -eq 0) {
                        Add-Violation 'RESUME_TICKET' $rel 'Resume Ticket has no "- **Module:**" field' "Add '- **Module:** ``$code``' to the Resume Ticket."
                    }
                    elseif ((Clear-Cell ($moduleLine[0] -replace '^\s*- \*\*Module:\*\*', '')) -ne $code) {
                        Add-Violation 'RESUME_TICKET' $rel "Resume Ticket module '$((Clear-Cell ($moduleLine[0] -replace '^\s*- \*\*Module:\*\*', '')))' does not match folder module '$code'" "Set '- **Module:** ``$code``'."
                    }
                    if (-not ($content | Where-Object { $_ -match 'Immediate Next Atomic Action' })) {
                        Add-Violation 'RESUME_TICKET' $rel 'Resume Ticket has no "Immediate Next Atomic Action"' 'Restore the field from the template.'
                    }
                }

                $lineNo = 0
                foreach ($line in $content) {
                    $lineNo++
                    if ($line -match '^### Major Task (\S+?):') {
                        if ($Matches[1] -notmatch ('^' + [regex]::Escape($prefix) + '\.\d+$')) {
                            Add-Violation 'TASK_ID' "${rel}:$lineNo" "Major Task ID '$($Matches[1])' should be $prefix.<M>" 'Use the <MOD>-P<NN>.<M> format matching this dossier.'
                        }
                    }
                    elseif ($line -match '^\s*- \[([ xX])\] \*\*Atomic Task (\S+?):\*\*') {
                        $checked = $Matches[1] -ne ' '
                        $taskId = $Matches[2]
                        if ($taskId -notmatch ('^' + [regex]::Escape($prefix) + '\.\d+\.\d+$')) {
                            Add-Violation 'TASK_ID' "${rel}:$lineNo" "Atomic Task ID '$taskId' should be $prefix.<M>.<A>" 'Use the <MOD>-P<NN>.<M>.<A> format matching this dossier.'
                        }
                        if ($area -eq 'completed' -and -not $checked) {
                            Add-Violation 'ARCHIVE_INCOMPLETE' "${rel}:$lineNo" "archived dossier has unchecked Atomic Task '$taskId'" 'Only verified phases may be archived; move it back to active/ or complete the task.'
                        }
                    }
                }
            }
            elseif ($f.Name -match $PlanFilePattern) {
                continue
            }
            else {
                Add-Violation 'DOSSIER_NAME' $rel 'file name must be phase-<NN>-<slug>.md or plan-<slug>.md' 'Rename the file (docs/WORKFLOW.md section 2).'
            }
        }

        if ($area -eq 'active' -and $phaseFiles.Count -gt 1) {
            Add-Violation 'ONE_ACTIVE_PHASE' "$dirRel/" ("{0} active phase dossiers: {1}" -f $phaseFiles.Count, (($phaseFiles | ForEach-Object { $_.Name }) -join ', ')) 'Each module holds at most one active phase; archive or remove the others.'
        }
    }
}

foreach ($key in @($dossierIndex.Keys)) {
    $parts = $key.Split('|')
    if ($parts[0] -eq 'active' -and $dossierIndex.ContainsKey("completed|$($parts[1])|$($parts[2])")) {
        Add-Violation 'PHASE_BOTH_AREAS' "docs/plans/active/$($parts[1])/$($dossierIndex[$key])" "phase $($parts[2]) exists in both active/ and completed/" 'A dossier is moved (not copied) to completed/.'
    }
}

# ---------------------------------------------------------------------------
# 7. Module Blueprints vs dossiers on disk
# ---------------------------------------------------------------------------

foreach ($code in @($codeToSlug.Keys)) {
    $slug = $codeToSlug[$code]
    $bpRel = "docs/plans/modules/$slug.md"
    $hasBlueprint = Test-Path -LiteralPath (Get-RepoPath $bpRel) -PathType Leaf
    $diskActive = @(Get-DossierFiles 'active' $slug)
    $diskDone = @(Get-DossierFiles 'completed' $slug)

    if (-not $hasBlueprint) {
        if (($diskActive.Count + $diskDone.Count) -gt 0) {
            Add-Violation 'BLUEPRINT_MISSING' $bpRel "module '$code' has phase dossiers but no blueprint" 'Create the blueprint (Gate 3) before starting phases (Gate 4).'
        }
        continue
    }

    $bp = Get-RequiredTable $bpRel '^## 7\. Module Phase Sequence' '## 7. Module Phase Sequence' @('Phase', 'Status')
    if ($null -eq $bp) { continue }

    $planned = @{}
    foreach ($row in $bp.Table.Rows) {
        if (Test-Placeholder $row['Phase']) { continue }
        $phase = Clear-Cell $row['Phase']
        $where = "$($bp.Label) row '$phase'"
        if ($phase -notmatch ('^' + [regex]::Escape($code) + '-P(\d{2})$')) {
            Add-Violation 'PHASE_ID' $where "phase ID '$phase' should be $code-P<NN>" 'Use this module''s code as the phase prefix.'
            continue
        }
        $nn = $Matches[1]
        if ($planned.ContainsKey($nn)) {
            Add-Violation 'PHASE_DUPLICATE' $where "phase '$phase' appears twice" 'Phase IDs are unique within a module.'
        }
        $status = Clear-Cell $row['Status']
        $planned[$nn] = $status
        if ($PhaseStatuses -cnotcontains $status) {
            Add-Violation 'PHASE_STATUS' $where "status '$status' is not one of $($PhaseStatuses -join ' | ')" 'Use PENDING, ACTIVE, BLOCKED, or COMPLETED.'
            continue
        }
        $inActive = $dossierIndex.ContainsKey("active|$slug|$nn")
        $inDone = $dossierIndex.ContainsKey("completed|$slug|$nn")
        if ($status -eq 'ACTIVE' -and -not $inActive) {
            Add-Violation 'PHASE_SYNC' $where "status is ACTIVE but no docs/plans/active/$slug/phase-$nn-*.md exists" 'Instantiate the dossier (Gate 4) or correct the status.'
        }
        if ($status -eq 'COMPLETED' -and -not $inDone) {
            Add-Violation 'PHASE_SYNC' $where "status is COMPLETED but no docs/plans/completed/$slug/phase-$nn-*.md exists" 'Archive the verified dossier or correct the status.'
        }
        if (($status -eq 'PENDING') -and ($inActive -or $inDone)) {
            Add-Violation 'PHASE_SYNC' $where 'status is PENDING but a dossier exists on disk' 'Set the status to ACTIVE / BLOCKED / COMPLETED to match the dossier location.'
        }
    }

    foreach ($f in $diskActive) {
        $null = $f.Name -match $PhaseFilePattern
        $nn = $Matches[1]
        if (-not $planned.ContainsKey($nn)) {
            Add-Violation 'PHASE_SYNC' "docs/plans/active/$slug/$($f.Name)" "phase $code-P$nn is not in the blueprint's phase sequence" "Add $code-P$nn to $bpRel section 7."
        }
        elseif (@('ACTIVE', 'BLOCKED') -cnotcontains $planned[$nn]) {
            Add-Violation 'PHASE_SYNC' "docs/plans/active/$slug/$($f.Name)" "blueprint status for $code-P$nn is '$($planned[$nn])', expected ACTIVE or BLOCKED" "Update $bpRel section 7."
        }
    }
    foreach ($f in $diskDone) {
        $null = $f.Name -match $PhaseFilePattern
        $nn = $Matches[1]
        if (-not $planned.ContainsKey($nn)) {
            Add-Violation 'PHASE_SYNC' "docs/plans/completed/$slug/$($f.Name)" "phase $code-P$nn is not in the blueprint's phase sequence" "Add $code-P$nn to $bpRel section 7."
        }
        elseif ($planned[$nn] -ne 'COMPLETED') {
            Add-Violation 'PHASE_SYNC' "docs/plans/completed/$slug/$($f.Name)" "blueprint status for $code-P$nn is '$($planned[$nn])', expected COMPLETED" "Update $bpRel section 7."
        }
    }

    if ($diskActive.Count -gt 0 -and $moduleStatus[$code] -ne 'IN_PROGRESS') {
        Add-Warning 'MODULE_STATUS_SYNC' $roadmapRel "module '$code' has an active dossier but registry status is '$($moduleStatus[$code])'" 'Set the module status to IN_PROGRESS.'
    }
}

# ---------------------------------------------------------------------------
# 8. Active Work Pointer
# ---------------------------------------------------------------------------

if ($hasRoadmap) {
    $pointer = Get-Section (Read-Lines $roadmapRel) '^## 5\. Active Work Pointer'
    if (-not $pointer.Found) {
        Add-Violation 'SECTION_MISSING' $roadmapRel "heading '## 5. Active Work Pointer' not found" 'Restore the section from docs/templates/system-roadmap-template.md.'
    }
    else {
        $text = $pointer.Lines -join "`n"
        $listed = @{}
        foreach ($m in [regex]::Matches($text, 'docs/plans/active/[a-z0-9-]+/phase-\d{2}-[a-z0-9-]+\.md')) { $listed[$m.Value] = $true }
        foreach ($rel in $activeDossiers) {
            if (-not $listed.ContainsKey($rel)) {
                Add-Violation 'POINTER_SYNC' "$roadmapRel (## 5. Active Work Pointer)" "active dossier '$rel' is not listed" 'Add it to the Active Work Pointer table (docs/WORKFLOW.md section 4).'
            }
        }
        foreach ($rel in @($listed.Keys)) {
            if (-not $activeDossiers.Contains($rel)) {
                Add-Violation 'POINTER_SYNC' "$roadmapRel (## 5. Active Work Pointer)" "points to '$rel', which is not in docs/plans/active/" 'Remove the stale entry or fix the path (the dossier may have been archived).'
            }
        }
        if (-not ($pointer.Lines | Where-Object { $_ -match '^\s*- \*\*Current Stage:\*\*' })) {
            Add-Violation 'POINTER_FIELD' "$roadmapRel (## 5. Active Work Pointer)" 'missing "- **Current Stage:**"' 'Restore the field from the template.'
        }
        if (-not ($pointer.Lines | Where-Object { $_ -match '^\s*- \*\*Current Focus:\*\*' })) {
            Add-Violation 'POINTER_FIELD' "$roadmapRel (## 5. Active Work Pointer)" 'missing "- **Current Focus:**"' 'Restore the field from the template.'
        }
    }
}

# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

Write-Host ("Harness plan validation: {0}" -f $Root)
Write-Host ("  modules registered: {0}; active phase dossiers: {1}" -f $codeToSlug.Count, $activeDossiers.Count)

foreach ($w in $script:Warnings) { Write-Host "WARN  $w" -ForegroundColor Yellow }
foreach ($e in $script:Errors) { Write-Host "ERROR $e" -ForegroundColor Red }

if ($script:Errors.Count -gt 0) {
    Write-Host ("FAILED: {0} violation(s), {1} warning(s)." -f $script:Errors.Count, $script:Warnings.Count) -ForegroundColor Red
    exit 1
}
Write-Host ("PASSED: 0 violations, {0} warning(s)." -f $script:Warnings.Count) -ForegroundColor Green
exit 0
