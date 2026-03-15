---
name: X API認証情報の管理
description: X (Twitter) APIトークンの保管場所と再生成履歴
type: reference
---

- **認証ファイル**: `claude-code/nambei-oyaji.com/config/x-credentials.json`（.gitignore対象、Git非追跡）
- **必要な4つのキー**: api_key, api_key_secret, access_token, access_token_secret
- **アカウント**: @nambei_oyaji
- **Developer Portal**: developer.x.com → プロジェクト → アプリ → Keys and tokens

## トークン再生成履歴
- **2026-03-13**: 401 Unauthorized で自動投稿が停止。Consumer Key + Access Token を全て再生成して復旧
  - 原因: トークン失効（詳細不明）
  - 対処: Developer Portal で4つ全て Regenerate → x-credentials.json を更新
