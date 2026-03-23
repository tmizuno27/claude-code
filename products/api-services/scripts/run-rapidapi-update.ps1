# RapidAPI Studio Auto Update (24 APIs)
Write-Host "=== RapidAPI Studio Auto Update ===" -ForegroundColor Cyan
Write-Host ""

# Build path with Unicode chars
$myDrive = $env:USERPROFILE + "\" + [char]0x30DE + [char]0x30A4 + [char]0x30C9 + [char]0x30E9 + [char]0x30A4 + [char]0x30D6
$apiDir = "$myDrive\GitHub\claude-code\products\api-services"
$debugProfile = "$env:USERPROFILE\chrome-debug-profile"

# Step 1: Kill Chrome
Write-Host "Step 1: Stopping Chrome..." -ForegroundColor Yellow
Get-Process chrome -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 5
Write-Host "Chrome stopped." -ForegroundColor Green

# Step 2: Launch Chrome with remote debugging + separate user data dir
Write-Host "Step 2: Launching Chrome with remote debugging..." -ForegroundColor Yellow
$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
Start-Process $chromePath -ArgumentList "--remote-debugging-port=9222","--user-data-dir=$debugProfile","https://rapidapi.com/studio/"
Write-Host "Waiting for Chrome to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Step 3: Check port with retry
for ($i = 0; $i -lt 10; $i++) {
    $port = netstat -an | Select-String "9222.*LISTENING"
    if ($port) {
        Write-Host "Chrome remote debugging OK (port 9222)" -ForegroundColor Green
        break
    }
    Write-Host "Waiting for port 9222... ($($i+1)/10)" -ForegroundColor Yellow
    Start-Sleep -Seconds 3
}

$portFinal = netstat -an | Select-String "9222.*LISTENING"
if (-not $portFinal) {
    Write-Host "ERROR: Port 9222 not available. Exiting." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
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
Set-Location $apiDir
python "$apiDir\scripts\rapidapi_studio_updater.py"

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Green
Read-Host "Press Enter to exit"
