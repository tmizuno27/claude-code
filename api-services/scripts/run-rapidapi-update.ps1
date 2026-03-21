# RapidAPI Studio 全24本API リスティング自動更新
# 使い方: PowerShellで実行するだけ

Write-Host "=== RapidAPI Studio 自動更新 ===" -ForegroundColor Cyan
Write-Host ""

# Step 1: Chromeを全て閉じる
Write-Host "Step 1: Chrome を停止します..." -ForegroundColor Yellow
Get-Process chrome -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 3

# Step 2: Chromeをリモートデバッグモードで起動
Write-Host "Step 2: Chrome をリモートデバッグモードで起動..." -ForegroundColor Yellow
Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--remote-debugging-port=9222", "https://rapidapi.com/studio/"
Start-Sleep -Seconds 10

# Step 3: ポート確認
$port = netstat -an | Select-String "9222.*LISTENING"
if ($port) {
    Write-Host "Chrome リモートデバッグ接続OK (port 9222)" -ForegroundColor Green
} else {
    Write-Host "警告: port 9222 が見つかりません。Chromeが起動するまで待ちます..." -ForegroundColor Red
    Start-Sleep -Seconds 10
}

# Step 4: RapidAPI Studioにログイン済みか確認
Write-Host ""
Write-Host "=== ブラウザで RapidAPI Studio が表示されていることを確認してください ===" -ForegroundColor Cyan
Write-Host "もしログインが必要なら、ログインしてからEnterを押してください。"
Write-Host ""
Read-Host ">>> 準備ができたらEnterキーを押してください"

# Step 5: Python更新スクリプト実行
Write-Host ""
Write-Host "Step 5: 全24本のAPIリスティングを更新中..." -ForegroundColor Yellow
Set-Location "$env:USERPROFILE\マイドライブ\GitHub\claude-code\api-services"
python scripts/rapidapi_studio_updater.py

Write-Host ""
Write-Host "=== 完了 ===" -ForegroundColor Green
Read-Host "Enterで終了"
