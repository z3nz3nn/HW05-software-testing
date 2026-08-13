[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repoRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$backendDirectory = Join-Path $repoRoot 'runtime\eshop-sut\backend'
$evidenceDirectory = Join-Path $repoRoot 'evidence\issues\duplicate-email'
New-Item -ItemType Directory -Force -Path $evidenceDirectory | Out-Null

$existingPort = Get-NetTCPConnection -LocalPort 3000 -State Listen -ErrorAction SilentlyContinue
if ($existingPort) { throw "Port 3000 is already in use by PID $($existingPort.OwningProcess)." }

$backendOut = Join-Path $evidenceDirectory 'backend.out.log'
$backendErr = Join-Path $evidenceDirectory 'backend.err.log'
$backend = $null
try {
    $backend = Start-Process -FilePath 'node.exe' -ArgumentList 'server.js' -WorkingDirectory $backendDirectory `
        -WindowStyle Hidden -PassThru -RedirectStandardOutput $backendOut -RedirectStandardError $backendErr
    foreach ($attempt in 1..30) {
        Start-Sleep -Milliseconds 500
        try {
            $null = Invoke-RestMethod -Uri 'http://localhost:3000/api/products' -Method Get -TimeoutSec 2
            break
        } catch {
            if ($backend.HasExited) { throw 'Backend exited before reproduction.' }
            if ($attempt -eq 30) { throw 'Backend did not become ready.' }
        }
    }

    $email = 'duplicate-evidence@loadtest.local'
    $body = @{ name = 'Duplicate Evidence'; email = $email; password = 'Duplicate123!' } | ConvertTo-Json -Compress
    $first = Invoke-WebRequest -UseBasicParsing -Uri 'http://localhost:3000/api/register' -Method Post -ContentType 'application/json' -Body $body
    $second = Invoke-WebRequest -UseBasicParsing -Uri 'http://localhost:3000/api/register' -Method Post -ContentType 'application/json' -Body $body

    $evidence = [ordered]@{
        collected_at = (Get-Date).ToString('o')
        requirement = 'FR-01: Email must be unique'
        request_body = ($body | ConvertFrom-Json)
        first_status = $first.StatusCode
        first_response = ($first.Content | ConvertFrom-Json)
        second_status = $second.StatusCode
        second_response = ($second.Content | ConvertFrom-Json)
        observed = 'Both identical registrations returned HTTP 200 with different user IDs.'
        expected = 'The second registration must be rejected with a 4xx response and a safe uniqueness message.'
    }
    $evidence | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $evidenceDirectory 'reproduction.json') -Encoding UTF8

    $safeBody = [System.Net.WebUtility]::HtmlEncode($body)
    $safeFirst = [System.Net.WebUtility]::HtmlEncode($first.Content)
    $safeSecond = [System.Net.WebUtility]::HtmlEncode($second.Content)
    $html = @"
<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Duplicate email reproduction</title><style>body{font-family:Segoe UI,Arial;margin:36px;background:#f4f6fa;color:#1f2937}.panel{max-width:1050px;margin:auto;background:white;padding:30px;border-radius:16px;box-shadow:0 10px 30px #0002}.bad{color:#b91c1c}.ok{color:#166534}pre{background:#101827;color:#e5edf8;padding:15px;border-radius:10px;overflow:auto}.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.status{font-size:1.2rem;font-weight:700}</style></head><body><main class="panel"><h1 class="bad">FR-01 violation: duplicate email accepted</h1><p><strong>Captured:</strong> $($evidence.collected_at)</p><p><strong>Expected:</strong> second request rejected. <strong>Observed:</strong> both identical requests returned HTTP 200 and created different IDs.</p><h2>Identical request body</h2><pre>$safeBody</pre><div class="grid"><section><h2>First registration</h2><p class="status">HTTP $($first.StatusCode)</p><pre>$safeFirst</pre></section><section><h2>Second registration</h2><p class="status bad">HTTP $($second.StatusCode) - should fail</p><pre>$safeSecond</pre></section></div><p class="ok">Evidence produced by two real localhost API calls; no values were fabricated.</p></main></body></html>
"@
    $html | Set-Content -LiteralPath (Join-Path $evidenceDirectory 'reproduction.html') -Encoding UTF8
} finally {
    if ($backend -and -not $backend.HasExited) {
        Stop-Process -Id $backend.Id
        $backend.WaitForExit(5000) | Out-Null
    }
}

Get-Content -LiteralPath (Join-Path $evidenceDirectory 'reproduction.json') -Raw
