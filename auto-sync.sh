#!/bin/bash
# ============================================
# GitHub 自動同期スクリプト
# ファイル変更を検知して自動で commit & push
# 停止: Ctrl+C
# ============================================

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
CHECK_INTERVAL=10    # 変更チェック間隔（秒）
WAIT_AFTER_CHANGE=60 # 最後の変更から待機する秒数
BRANCH="main"

cd "$REPO_DIR" || { echo "[ERROR] リポジトリに移動できません: $REPO_DIR"; exit 1; }

echo "========================================"
echo " GitHub 自動同期 開始"
echo " リポジトリ: $REPO_DIR"
echo " チェック間隔: ${CHECK_INTERVAL}秒"
echo " push待機: ${WAIT_AFTER_CHANGE}秒"
echo " 停止: Ctrl+C"
echo "========================================"

cleanup() {
    echo ""
    echo "[INFO] 自動同期を停止しました。"
    exit 0
}
trap cleanup SIGINT SIGTERM

while true; do
    # 変更があるかチェック
    changes=$(git status --porcelain 2>/dev/null)

    if [ -n "$changes" ]; then
        echo ""
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 変更を検知しました。${WAIT_AFTER_CHANGE}秒待機します..."

        # 待機ループ: 追加変更がないか確認しながら待つ
        waited=0
        while [ $waited -lt $WAIT_AFTER_CHANGE ]; do
            sleep $CHECK_INTERVAL
            waited=$((waited + CHECK_INTERVAL))

            new_changes=$(git status --porcelain 2>/dev/null)
            if [ "$new_changes" != "$changes" ]; then
                # 追加変更があったのでタイマーリセット
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] 追加変更を検知。待機をリセットします..."
                changes="$new_changes"
                waited=0
            fi
        done

        # commit & push 実行
        timestamp=$(date '+%Y-%m-%d %H:%M:%S')
        echo "[${timestamp}] commit & push を実行します..."

        git add -A

        if git commit -m "auto-sync: ${timestamp}"; then
            if git push origin "$BRANCH"; then
                echo "[${timestamp}] GitHub に反映しました。"
            else
                echo "[${timestamp}] [ERROR] push に失敗しました。次のサイクルで再試行します。"
            fi
        else
            echo "[${timestamp}] [WARN] コミットする変更がありませんでした。"
        fi
    fi

    sleep $CHECK_INTERVAL
done
