# X自動投稿 Task Scheduler登録スクリプト
# 各スロットの基準時刻(JST)の30分前にタスクを起動し、
# Pythonスクリプト内で0〜60分のランダム遅延をかけることで
# 基準時刻の前後30分にバラけた投稿を実現する
#
# 基準時刻(JST) → タスク起動(JST) → タスク起動(PYT, 夏時間UTC-3)
#   morning  07:00 →  06:30 JST  →  18:30 PYT (前日)
#   noon     12:00 →  11:30 JST  →  23:30 PYT (前日)
#   evening  20:30 →  20:00 JST  →  08:00 PYT

# パスを Unicode コードポイントで構築（Task Scheduler経由での日本語パス問題を回避）
$ma = [char]0x30DE
$i  = [char]0x30A4
$do = [char]0x30C9
$ri = [char]0x30E9
$bu = [char]0x30D6
$iv = [char]0x30A4  # duplicate but for clarity
$driveFolder = "C:\Users\tmizu\${ma}${i}${do}${ri}${iv}${bu}"
$scriptDir = "$driveFolder\GitHub\claude-code\blog\scripts\social"
$pythonExe = "python"
$logDir = "$driveFolder\GitHub\claude-code\blog\outputs\social"

$slots = @(
    @{ Name = "XAutoPost-Morning"; Slot = "morning"; Hour = 18; Minute = 30 },
    @{ Name = "XAutoPost-Noon";    Slot = "noon";    Hour = 23; Minute = 30 },
    @{ Name = "XAutoPost-Evening"; Slot = "evening"; Hour = 8;  Minute = 0  }
)

foreach ($s in $slots) {
    $taskName = $s.Name
    $slot = $s.Slot
    $hour = $s.Hour
    $minute = $s.Minute

    # 既存タスクを削除
    $existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    if ($existing) {
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
        Write-Host "既存タスク '$taskName' を削除しました"
    }

    # コマンド: pythonスクリプト実行、ログをファイルに追記
    $argument = "-u `"$scriptDir\x_auto_post.py`" --slot $slot >> `"$logDir\x-auto-post.log`" 2>&1"

    $action = New-ScheduledTaskAction -Execute $pythonExe -Argument $argument
    $trigger = New-ScheduledTaskTrigger -Daily -At "${hour}:${minute}"
    $settings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -StartWhenAvailable `
        -ExecutionTimeLimit (New-TimeSpan -Hours 2)

    Register-ScheduledTask `
        -TaskName $taskName `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Description "X自動投稿 ($slot) - 南米おやじ @nambei_oyaji" `
        -RunLevel Limited

    Write-Host "タスク '$taskName' を登録しました (毎日 ${hour}:${minute} PYT)"
}

Write-Host ""
Write-Host "=== 登録完了 ==="
Write-Host "  XAutoPost-Morning : 18:30 PYT → JST 06:30-07:30頃に投稿"
Write-Host "  XAutoPost-Noon    : 23:30 PYT → JST 11:30-12:30頃に投稿"
Write-Host "  XAutoPost-Evening : 08:00 PYT → JST 20:00-21:00頃に投稿"
