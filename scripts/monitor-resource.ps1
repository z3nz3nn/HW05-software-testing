[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [int]$TargetPid,

    [Parameter(Mandatory = $true)]
    [string]$OutputCsv,

    [Parameter(Mandatory = $true)]
    [string]$StopFile,

    [int]$IntervalSeconds = 1
)

$ErrorActionPreference = 'Stop'
$logicalProcessors = [Environment]::ProcessorCount
$outputFullPath = [System.IO.Path]::GetFullPath($OutputCsv)
$stopFullPath = [System.IO.Path]::GetFullPath($StopFile)
$outputDirectory = Split-Path -Parent $outputFullPath
New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null

$previousCpuSeconds = $null
$previousTimestamp = $null
$firstRow = $true

while (-not (Test-Path -LiteralPath $stopFullPath)) {
    $process = Get-Process -Id $TargetPid -ErrorAction SilentlyContinue
    if ($null -eq $process) { break }

    $timestamp = Get-Date
    $cpuSeconds = $process.TotalProcessorTime.TotalSeconds
    $cpuPercent = 0.0
    if ($null -ne $previousCpuSeconds) {
        $elapsedWallSeconds = ($timestamp - $previousTimestamp).TotalSeconds
        if ($elapsedWallSeconds -gt 0) {
            $cpuPercent = (($cpuSeconds - $previousCpuSeconds) / $elapsedWallSeconds / $logicalProcessors) * 100
        }
    }

    $row = [pscustomobject]@{
        timestamp_iso       = $timestamp.ToString('o')
        pid                 = $TargetPid
        node_cpu_percent    = [math]::Round($cpuPercent, 3)
        working_set_mb      = [math]::Round($process.WorkingSet64 / 1MB, 3)
        private_memory_mb   = [math]::Round($process.PrivateMemorySize64 / 1MB, 3)
        handles             = $process.HandleCount
        threads             = $process.Threads.Count
    }

    if ($firstRow) {
        $row | Export-Csv -LiteralPath $outputFullPath -NoTypeInformation -Encoding UTF8
        $firstRow = $false
    } else {
        $row | Export-Csv -LiteralPath $outputFullPath -NoTypeInformation -Encoding UTF8 -Append
    }

    $previousCpuSeconds = $cpuSeconds
    $previousTimestamp = $timestamp
    Start-Sleep -Seconds $IntervalSeconds
}

