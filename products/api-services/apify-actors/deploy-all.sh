#!/bin/bash
# Apify Actor 一括デプロイスクリプト
# 使い方: bash deploy-all.sh [--dry-run]
#
# 前提条件:
#   npm install -g apify-cli
#   apify login  (APIトークンでログイン済み)

set -euo pipefail

ACTORS_DIR="$(cd "$(dirname "$0")" && pwd)"
DRY_RUN=false
FAILED=()
SUCCESS=()
SKIPPED=()

if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
  echo "=== DRY RUN MODE (デプロイは実行しません) ==="
  echo
fi

# apify CLI の存在確認
if ! command -v apify &> /dev/null; then
  echo "ERROR: apify CLI が見つかりません"
  echo "  npm install -g apify-cli"
  echo "  apify login"
  exit 1
fi

# ログイン確認
if ! apify info 2>/dev/null | grep -q "User"; then
  echo "ERROR: Apify にログインしていません"
  echo "  apify login"
  exit 1
fi

echo "=== Apify Actor 一括デプロイ開始 ==="
echo "ディレクトリ: $ACTORS_DIR"
echo

for actor_dir in "$ACTORS_DIR"/*/; do
  actor_name=$(basename "$actor_dir")

  # deploy-guide.md 等のファイルはスキップ
  if [[ ! -d "$actor_dir" ]]; then
    continue
  fi

  # .actor/actor.json の存在確認
  if [[ ! -f "$actor_dir/.actor/actor.json" ]]; then
    echo "[$actor_name] SKIP: .actor/actor.json が見つかりません"
    SKIPPED+=("$actor_name")
    continue
  fi

  echo "[$actor_name] デプロイ中..."

  if $DRY_RUN; then
    echo "  (dry-run) apify push を実行します"
    SUCCESS+=("$actor_name")
  else
    cd "$actor_dir"

    # Node.js の場合 npm install
    if [[ -f "package.json" ]] && [[ ! -d "node_modules" ]]; then
      echo "  npm install..."
      npm install --omit=dev 2>&1 | tail -1
    fi

    if apify push 2>&1; then
      echo "  OK"
      SUCCESS+=("$actor_name")
    else
      echo "  FAILED"
      FAILED+=("$actor_name")
    fi
  fi
  echo
done

echo "=== デプロイ結果サマリ ==="
echo "成功: ${#SUCCESS[@]} / スキップ: ${#SKIPPED[@]} / 失敗: ${#FAILED[@]}"
echo

if [[ ${#SUCCESS[@]} -gt 0 ]]; then
  echo "成功:"
  for name in "${SUCCESS[@]}"; do echo "  - $name"; done
fi

if [[ ${#SKIPPED[@]} -gt 0 ]]; then
  echo "スキップ:"
  for name in "${SKIPPED[@]}"; do echo "  - $name"; done
fi

if [[ ${#FAILED[@]} -gt 0 ]]; then
  echo "失敗:"
  for name in "${FAILED[@]}"; do echo "  - $name"; done
  echo
  echo "失敗したActorを個別にデプロイ:"
  for name in "${FAILED[@]}"; do
    echo "  cd $ACTORS_DIR/$name && apify push"
  done
  exit 1
fi

echo
echo "全Actor デプロイ完了!"
echo "確認: https://console.apify.com/actors"
