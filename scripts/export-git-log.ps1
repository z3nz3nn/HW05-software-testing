param(
    [string]$OutputPath = "git-commit-log.txt"
)

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$resolvedOutput = if ([System.IO.Path]::IsPathRooted($OutputPath)) {
    $OutputPath
} else {
    Join-Path $repoRoot $OutputPath
}

Push-Location $repoRoot
try {
    $lines = git log --date=iso-strict --pretty=format:"%h | %ad | %an | %s"
    if ($LASTEXITCODE -ne 0) {
        throw "git log failed with exit code $LASTEXITCODE"
    }

    $header = @(
        "HW05 Git commit history"
        "Generated: $([DateTimeOffset]::Now.ToString('o'))"
        "Repository: $repoRoot"
        ""
    )
    [System.IO.File]::WriteAllLines(
        $resolvedOutput,
        @($header + $lines),
        [System.Text.UTF8Encoding]::new($false)
    )
    Write-Output $resolvedOutput
} finally {
    Pop-Location
}
