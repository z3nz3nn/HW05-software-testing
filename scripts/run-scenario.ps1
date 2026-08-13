[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('Load', 'Stress', 'Spike', 'Soak')]
    [string]$Scenario,

    [string]$JMeterProperty = '',

    [switch]$Smoke
)

$ErrorActionPreference = 'Stop'
$repoRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$studentId = '23127373' # HUMAN REVIEW: confirm before submission.
$runDate = '20260814'
$planPath = Join-Path $repoRoot "test-plans\${studentId}_${Scenario}_${runDate}.jmx"
$jmeterPath = Join-Path $repoRoot '.tools\apache-jmeter-5.6.3\bin\jmeter.bat'
$backendDirectory = Join-Path $repoRoot 'runtime\eshop-sut\backend'

if (-not (Test-Path -LiteralPath $planPath)) { throw "Missing plan: $planPath" }
if (-not (Test-Path -LiteralPath $jmeterPath)) { throw "Missing JMeter: $jmeterPath" }

$mode = if ($Smoke) { 'smoke' } else { 'final' }
$resultDirectory = if ($Smoke) { Join-Path $repoRoot 'results\smoke' } else { Join-Path $repoRoot 'results' }
$htmlRoot = if ($Smoke) { Join-Path $repoRoot 'reports\html\smoke' } else { Join-Path $repoRoot 'reports\html' }
$resourceDirectory = Join-Path $repoRoot 'evidence\resources'
$logDirectory = Join-Path $repoRoot 'evidence\runtime-logs'
New-Item -ItemType Directory -Force -Path $resultDirectory, $htmlRoot, $resourceDirectory, $logDirectory | Out-Null

$scenarioKey = $Scenario.ToLowerInvariant()
$jtlPath = Join-Path $resultDirectory "${studentId}_${Scenario}_${runDate}.jtl"
$listenerPath = Join-Path $resultDirectory "listeners\${scenarioKey}-listener.jtl"
$htmlPath = Join-Path $htmlRoot "${studentId}_${Scenario}_${runDate}"
$resourcePath = Join-Path $resourceDirectory "${studentId}_${Scenario}_${runDate}.csv"
$backendOut = Join-Path $logDirectory "${scenarioKey}-backend.out.log"
$backendErr = Join-Path $logDirectory "${scenarioKey}-backend.err.log"
$jmeterOut = Join-Path $logDirectory "${scenarioKey}-jmeter-console.log"
$monitorStop = Join-Path $env:TEMP "hw05-${scenarioKey}-$PID.stop"

if (Test-Path -LiteralPath $jtlPath) { throw "Result already exists: $jtlPath" }
if (Test-Path -LiteralPath $htmlPath) { throw "HTML report already exists: $htmlPath" }
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $listenerPath) | Out-Null

$existingPort = Get-NetTCPConnection -LocalPort 3000 -State Listen -ErrorAction SilentlyContinue
if ($existingPort) {
    throw "Port 3000 is already in use by PID $($existingPort.OwningProcess). Stop it explicitly before this controlled run."
}

$backendProcess = $null
$monitorProcess = $null
try {
    $backendProcess = Start-Process -FilePath 'node.exe' -ArgumentList 'server.js' `
        -WorkingDirectory $backendDirectory -WindowStyle Hidden -PassThru `
        -RedirectStandardOutput $backendOut -RedirectStandardError $backendErr

    $ready = $false
    foreach ($attempt in 1..30) {
        Start-Sleep -Milliseconds 500
        try {
            $null = Invoke-RestMethod -Uri 'http://localhost:3000/api/products' -Method Get -TimeoutSec 2
            $ready = $true
            break
        } catch {
            if ($backendProcess.HasExited) { throw "Backend exited before becoming ready. See $backendErr" }
        }
    }
    if (-not $ready) { throw 'Backend did not become ready within 15 seconds.' }

    $loginBody = @{ email = 'admin@eshop.com'; password = 'Admin123!' } | ConvertTo-Json -Compress
    $login = Invoke-RestMethod -Uri 'http://localhost:3000/api/login' -Method Post -ContentType 'application/json' -Body $loginBody
    if (-not $login.token) { throw 'Admin login did not return a JWT.' }

    $monitorProcess = Start-Process -FilePath 'powershell.exe' -WindowStyle Hidden -PassThru -ArgumentList @(
        '-NoProfile',
        '-ExecutionPolicy', 'Bypass',
        '-File', (Join-Path $PSScriptRoot 'monitor-resource.ps1'),
        '-TargetPid', $backendProcess.Id,
        '-OutputCsv', $resourcePath,
        '-StopFile', $monitorStop
    )

    $arguments = @(
        '-n',
        '-t', $planPath,
        "-Jadmin_jwt=$($login.token)",
        "-Jscenario=$Scenario",
        "-Jcsv_file=$(Join-Path $repoRoot 'data\users.csv')",
        "-Jlistener_file=$listenerPath",
        '-l', $jtlPath,
        '-e',
        '-o', $htmlPath
    )
    foreach ($property in ($JMeterProperty -split ';' | Where-Object { $_.Trim() })) {
        if ($property -notmatch '^[A-Za-z0-9_.-]+=.+$') {
            throw "Invalid JMeter property override: $property"
        }
        $arguments += "-J$($property.Trim())"
    }

    & $jmeterPath @arguments 2>&1 | Tee-Object -FilePath $jmeterOut
    if ($LASTEXITCODE -ne 0) { throw "JMeter exited with code $LASTEXITCODE. See $jmeterOut" }
} finally {
    New-Item -ItemType File -Force -Path $monitorStop | Out-Null
    if ($monitorProcess -and -not $monitorProcess.HasExited) {
        $monitorProcess.WaitForExit(5000)
        if (-not $monitorProcess.HasExited) { Stop-Process -Id $monitorProcess.Id -Force }
    }
    if ($backendProcess -and -not $backendProcess.HasExited) {
        Stop-Process -Id $backendProcess.Id
        $backendProcess.WaitForExit(5000)
    }
    Remove-Item -LiteralPath $monitorStop -Force -ErrorAction SilentlyContinue
}

Write-Output "Scenario=$Scenario Mode=$mode"
Write-Output "JTL=$jtlPath"
Write-Output "HTML=$htmlPath"
Write-Output "Resources=$resourcePath"
