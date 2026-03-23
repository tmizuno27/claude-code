# GitHub auto-sync script (PowerShell)
# Checks for changes and auto commit & push
# Runs every 1 minute via Task Scheduler

$RepoDir = 'C:\Users\tmizu\マイドライブ\GitHub\data'
$Branch = 'main'
$LogFile = Join-Path $RepoDir 'auto-sync.log'

Set-Location $RepoDir

$changes = git status --porcelain 2>&1

if ([string]::IsNullOrWhiteSpace($changes)) {
    exit 0
}

$ts = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
Add-Content -Path $LogFile -Value "[$ts] Changes detected: $changes" -Encoding UTF8

git add -A

$ts = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
$commitResult = git commit -m "auto-sync: $ts" 2>&1

if ($LASTEXITCODE -eq 0) {
    Add-Content -Path $LogFile -Value "[$ts] Commit OK" -Encoding UTF8
    $pushResult = git push origin $Branch 2>&1
    if ($LASTEXITCODE -eq 0) {
        Add-Content -Path $LogFile -Value "[$ts] Push OK - synced to GitHub" -Encoding UTF8
    } else {
        Add-Content -Path $LogFile -Value "[$ts] [ERROR] Push failed: $pushResult" -Encoding UTF8
    }
} else {
    Add-Content -Path $LogFile -Value "[$ts] [WARN] Nothing to commit: $commitResult" -Encoding UTF8
}