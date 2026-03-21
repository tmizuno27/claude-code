# RapidAPI Studio Auto Update (24 APIs)
Write-Host "=== RapidAPI Studio Auto Update ===" -ForegroundColor Cyan
Write-Host ""

# Step 1: Kill Chrome
Write-Host "Step 1: Stopping Chrome..." -ForegroundColor Yellow
Get-Process chrome -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 3

# Step 2: Launch Chrome with remote debugging
Write-Host "Step 2: Launching Chrome with remote debugging..." -ForegroundColor Yellow
Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--remote-debugging-port=9222", "https://rapidapi.com/studio/"
Start-Sleep -Seconds 10

# Step 3: Check port
$port = netstat -an | Select-String "9222.*LISTENING"
if ($port) {
    Write-Host "Chrome remote debugging OK (port 9222)" -ForegroundColor Green
} else {
    Write-Host "Warning: port 9222 not found. Waiting..." -ForegroundColor Red
    Start-Sleep -Seconds 10
}

# Step 4: Wait for login
Write-Host ""
Write-Host "=== Check that RapidAPI Studio is loaded in the browser ===" -ForegroundColor Cyan
Write-Host "If you need to log in, do so now and press Enter."
Write-Host ""
Read-Host "Press Enter when ready"

# Step 5: Run Python updater
Write-Host ""
Write-Host "Step 5: Updating all 24 API listings..." -ForegroundColor Yellow
$scriptDir = Join-Path $env:USERPROFILE "マイドライブ\GitHub\claude-code\api-services"
Set-Location $scriptDir
python scripts/rapidapi_studio_updater.py

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Green
Read-Host "Press Enter to exit"
