param(
    [ValidateSet('check', 'login')]
    [string]$Action = 'check',
    [string]$RuntimeRoot = (Join-Path ([IO.Path]::GetTempPath()) 'pmp-hermes-runtime-20261006')
)
$ErrorActionPreference = 'Stop'
$pmpHome = Join-Path $RuntimeRoot 'pmp-home'
$pmpLauncher = Join-Path $RuntimeRoot 'bin\hermes.exe'
if (-not (Test-Path -LiteralPath $pmpLauncher -PathType Leaf)) {
    throw 'Independent runtime is missing. Do not substitute a previous Hermes installation.'
}
$pmpSavedHome = $env:HERMES_HOME
$pmpSavedPath = $env:Path
$pmpSavedEncoding = [Console]::OutputEncoding
if (-not (Test-Path -LiteralPath $pmpHome -PathType Container)) {
    & python -X utf8 (Join-Path $PSScriptRoot 'consumer.py') init-home --home $pmpHome
    if ($LASTEXITCODE -ne 0) { throw 'Could not create the standalone restricted Hermes home' }
}
Push-Location $pmpHome
try {
    # Use this isolated home as its own Hermes root, not a named profile under
    # RuntimeRoot\profiles. In the pinned Hermes build, first-time Codex OAuth
    # in an empty named profile can be reported as added without being persisted.
    $env:HERMES_HOME = $pmpHome
    $env:Path = (Join-Path $RuntimeRoot 'bin') + ';' + $pmpSavedPath
    [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
    # Compare only config bytes; never inspect or display credential contents.
    & python -X utf8 (Join-Path $PSScriptRoot 'consumer.py') check-home --home $pmpHome
    if ($LASTEXITCODE -ne 0) { throw 'Restriction config mismatch' }
    $pmpVersion = & $pmpLauncher --version
    if ($LASTEXITCODE -ne 0 -or ($pmpVersion -join "`n") -notmatch 'vgit\.e97923c\b') {
        throw 'Pinned runtime version check failed; inspect changes before proceeding'
    }
    $pmpVersion | Write-Output
    $pmpTools = & $pmpLauncher tools --summary
    if ($LASTEXITCODE -ne 0 -or ($pmpTools -join "`n") -notmatch 'CLI\s+\(0/\d+\)') {
        throw 'Zero-tool profile check failed. Do not authenticate or run the replay.'
    }
    $pmpTools | Write-Output
    if ($Action -eq 'login') {
        # Human OAuth only: no paid API, credential copying, model call or fallback.
        & $pmpLauncher auth add openai-codex --no-browser --timeout 180
        if ($LASTEXITCODE -ne 0) { throw 'Subscription OAuth did not complete; no retry performed' }
        $pmpAuthStatus = (& $pmpLauncher auth status openai-codex 2>&1 | Out-String)
        if ($LASTEXITCODE -ne 0 -or $pmpAuthStatus -match 'logged out') {
            throw 'Hermes did not confirm the OAuth credential in this isolated home; no model call or retry performed'
        }
        'OAuth credential confirmed by Hermes auth status; account details suppressed.' | Write-Output
    }
} finally {
    Pop-Location
    [Environment]::SetEnvironmentVariable('HERMES_HOME', $pmpSavedHome, 'Process')
    [Environment]::SetEnvironmentVariable('Path', $pmpSavedPath, 'Process')
    [Console]::OutputEncoding = $pmpSavedEncoding
}
