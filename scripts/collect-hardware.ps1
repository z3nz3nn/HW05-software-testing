[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repoRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$outputDirectory = Join-Path $repoRoot 'evidence\hardware'
New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null

$computer = Get-CimInstance Win32_ComputerSystem
$cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
$os = Get-CimInstance Win32_OperatingSystem
$gpu = Get-CimInstance Win32_VideoController | Select-Object -First 1
$disks = Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | ForEach-Object {
    [pscustomobject]@{
        drive = $_.DeviceID
        size_gb = [math]::Round($_.Size / 1GB, 2)
        free_gb = [math]::Round($_.FreeSpace / 1GB, 2)
    }
}

# `java -version` writes its version banner to stderr even on success. Let cmd
# merge the streams so Windows PowerShell does not inject a NativeCommandError
# record into the captured evidence.
$javaVersion = (& cmd.exe /d /c "java -version 2>&1" | Out-String).Trim()

$report = [ordered]@{
    collected_at = (Get-Date).ToString('o')
    hostname = $env:COMPUTERNAME
    manufacturer = $computer.Manufacturer
    model = $computer.Model
    os = $os.Caption
    os_version = $os.Version
    cpu = $cpu.Name
    physical_cores = $cpu.NumberOfCores
    logical_processors = $cpu.NumberOfLogicalProcessors
    ram_gb = [math]::Round($computer.TotalPhysicalMemory / 1GB, 2)
    gpu = $gpu.Name
    disks = @($disks)
    java = $javaVersion
    node = (& node --version | Out-String).Trim()
    jmeter = 'Apache JMeter 5.6.3 (SHA-512 verified portable binary)'
}

$jsonPath = Join-Path $outputDirectory 'hardware-report.json'
$markdownPath = Join-Path $outputDirectory 'hardware-report.md'
$htmlPath = Join-Path $outputDirectory 'hardware-report.html'
$dxdiagPath = Join-Path $outputDirectory 'dxdiag.txt'

$report | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

$diskRows = ($report.disks | ForEach-Object { "| $($_.drive) | $($_.size_gb) | $($_.free_gb) |" }) -join "`n"
$markdown = @"
# Hardware report

Collected at: `$($report.collected_at)`

| Field | Value |
| --- | --- |
| Hostname | `$($report.hostname)` |
| Manufacturer/model | `$($report.manufacturer) $($report.model)` |
| OS | `$($report.os) $($report.os_version)` |
| CPU | `$($report.cpu)` |
| Cores / logical processors | `$($report.physical_cores) / $($report.logical_processors)` |
| RAM | `$($report.ram_gb) GB` |
| GPU | `$($report.gpu)` |
| Java | `$($report.java -replace "`r?`n", '; ')` |
| Node.js | `$($report.node)` |
| JMeter | `$($report.jmeter)` |

## Fixed disks

| Drive | Size GB | Free GB at capture |
| --- | ---: | ---: |
$diskRows

> **HUMAN REVIEW REQUIRED:** Open `dxdiag`, verify the hostname/specification, and capture the required screenshot. The raw `dxdiag.txt` is generated alongside this table.
"@
$markdown | Set-Content -LiteralPath $markdownPath -Encoding UTF8

$html = @"
<!doctype html><html lang="en"><head><meta charset="utf-8"><title>HW05 Hardware Evidence</title>
<style>body{font-family:Segoe UI,Arial,sans-serif;margin:40px;background:#f5f7fb;color:#172033}.card{max-width:980px;margin:auto;background:white;border-radius:18px;padding:32px;box-shadow:0 12px 36px #1e293b20}h1{margin-top:0;color:#173b6c}table{border-collapse:collapse;width:100%}th,td{border-bottom:1px solid #dbe3ef;padding:11px;text-align:left}th{width:32%;color:#36506f}.tag{display:inline-block;background:#e7f0ff;color:#174b91;padding:5px 10px;border-radius:999px;font-weight:600}.review{margin-top:24px;padding:14px 18px;border-left:5px solid #d97706;background:#fff7e6}</style></head><body><main class="card"><span class="tag">Real local capture</span><h1>HW05 Hardware Evidence</h1><table>
<tr><th>Collected</th><td>$($report.collected_at)</td></tr><tr><th>Hostname</th><td>$($report.hostname)</td></tr>
<tr><th>System</th><td>$($report.manufacturer) $($report.model)</td></tr><tr><th>OS</th><td>$($report.os) $($report.os_version)</td></tr>
<tr><th>CPU</th><td>$($report.cpu)</td></tr><tr><th>Cores / logical</th><td>$($report.physical_cores) / $($report.logical_processors)</td></tr>
<tr><th>RAM</th><td>$($report.ram_gb) GB</td></tr><tr><th>GPU</th><td>$($report.gpu)</td></tr><tr><th>Java</th><td>$([System.Net.WebUtility]::HtmlEncode(($report.java -replace "`r?`n", '; ')))</td></tr><tr><th>Node.js</th><td>$($report.node)</td></tr><tr><th>JMeter</th><td>$($report.jmeter)</td></tr>
</table><div class="review"><strong>Manual evidence still required:</strong> open dxdiag and capture its GUI with the hostname visible.</div></main></body></html>
"@
$html | Set-Content -LiteralPath $htmlPath -Encoding UTF8

$dxdiagProcess = Start-Process -FilePath 'dxdiag.exe' -ArgumentList '/dontskip', '/t', $dxdiagPath -WindowStyle Hidden -PassThru
$dxdiagProcess.WaitForExit(60000) | Out-Null
if (-not (Test-Path -LiteralPath $dxdiagPath)) { throw 'dxdiag did not produce its text report.' }

Write-Output $markdownPath
Write-Output $dxdiagPath
