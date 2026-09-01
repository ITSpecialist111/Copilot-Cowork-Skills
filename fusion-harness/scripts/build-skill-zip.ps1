<#
.SYNOPSIS
    Packages the fusion-harness Cowork skill into a .zip with SKILL.md at the archive root.

.DESCRIPTION
    Cowork's "Upload skill" accepts a .zip or .skill archive whose root contains SKILL.md plus
    any companion files. This script validates the skill against the documented limits before
    packaging, so an invalid skill fails here rather than after upload.

.EXAMPLE
    ./scripts/build-skill-zip.ps1
    ./scripts/build-skill-zip.ps1 -OutFile C:\temp\fusion-harness.zip
#>
[CmdletBinding()]
param(
    [string]$SkillPath = (Split-Path $PSScriptRoot -Parent),
    [string]$OutFile   = (Join-Path (Split-Path $PSScriptRoot -Parent) 'dist\fusion-harness.zip')
)

$ErrorActionPreference = 'Stop'

$skillMd = Join-Path $SkillPath 'SKILL.md'
if (-not (Test-Path $skillMd)) { throw "no SKILL.md at $SkillPath" }

# ASKILL-P006: the frontmatter name must equal the folder name.
$lines = Get-Content $skillMd
if ($lines[0].Trim() -ne '---') { throw 'SKILL.md must start with a --- frontmatter delimiter' }
$end = 1; while ($end -lt $lines.Count -and $lines[$end].Trim() -ne '---') { $end++ }
if ($end -ge $lines.Count) { throw 'SKILL.md frontmatter is not closed with ---' }
$front = $lines[1..($end - 1)]

$nameLine = $front | Where-Object { $_ -match '^name:\s*(.+)$' } | Select-Object -First 1
if (-not $nameLine) { throw 'frontmatter is missing a name field (ASKILL-P004)' }
$name = ($nameLine -replace '^name:\s*', '').Trim().Trim('"', "'")

if (-not ($front | Where-Object { $_ -match '^description:' })) {
    throw 'frontmatter is missing a description field (ASKILL-P005)'
}
if ($name -cne (Split-Path $SkillPath -Leaf)) {
    throw "frontmatter name '$name' does not match folder '$(Split-Path $SkillPath -Leaf)' (ASKILL-P006)"
}
if ($name -notmatch '^[a-z0-9]+(-[a-z0-9]+)*$') {
    throw "name '$name' is not kebab-case (ASKILL-P007)"
}

# Only SKILL.md and references/ are uploadable skill content. Screenshots, the findings PDF and
# this script live alongside for the repo's benefit and must stay out of the archive.
$referencesDir = Join-Path $SkillPath 'references'
$companions = Get-ChildItem $referencesDir -Recurse -File
$totalMb = ($companions | Measure-Object Length -Sum).Sum / 1MB

if ((Get-Item $skillMd).Length -gt 1MB)       { throw 'SKILL.md exceeds the 1 MB limit' }
if ($companions.Count -gt 20)                 { throw "$($companions.Count) companion files; the limit is 20" }
if ($companions | Where-Object Length -gt 5MB){ throw 'a companion file exceeds the 5 MB limit' }
if ($totalMb -gt 10)                          { throw 'companion files exceed the 10 MB total limit' }

$oversized = $companions | Where-Object { $_.Name -match '^\.' -or $_.Name -match '[\\]' }
if ($oversized) { throw "invalid companion file name: $($oversized[0].Name)" }

$outDir = Split-Path $OutFile -Parent
if ($outDir -and -not (Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir | Out-Null }
if (Test-Path $OutFile) { Remove-Item $OutFile -Force }

Compress-Archive -Path $skillMd, $referencesDir -DestinationPath $OutFile

$words = (Get-Content $skillMd -Raw).Split([char[]]" `t`r`n", [StringSplitOptions]::RemoveEmptyEntries).Count
Write-Host "packaged $name -> $OutFile"
Write-Host "  SKILL.md      $words words (target under ~2,000)"
Write-Host "  companions    $($companions.Count) files, $([math]::Round($totalMb, 2)) MB"
