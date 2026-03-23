# Apify Actor 開発・公開・収益化ガイド

調査日: 2026-03-15

---

## 1. アカウント作成

- **プログラマティック作成: 不可**。Web UI（https://console.apify.com/sign-up）でメール+パスワード、またはGoogle/GitHub OAuthで作成する必要がある
- アカウント作成後、APIトークンを取得 → 以降はすべてCLI/APIで操作可能
- 無料プランあり（月$5分のプラットフォームクレジット付き）

## 2. Actor開発（ローカル）

### 対応言語
- **Python**（`apify` SDK — PyPI）
- **JavaScript / TypeScript**（`apify` SDK — npm）
- どちらでもOK。テンプレートが豊富

### 開発フロー（100% CLI）

```bash
# 1. CLIインストール
npm install -g apify-cli

# 2. ログイン（APIトークン）
apify login --token YOUR_API_TOKEN

# 3. プロジェクト作成（テンプレート選択）
apify create my-actor --template python-start
# または: --template javascript-start, python-crawlee, etc.

# 4. ローカル実行
cd my-actor
apify run

# 5. デプロイ（Apifyクラウドにpush + 自動ビルド）
apify push
```

### プロジェクト構造
- `.actor/actor.json` — Actor設定（名前、バージョン、入出力スキーマ）
- `src/main.py` or `src/main.js` — メインコード
- `requirements.txt` or `package.json` — 依存関係
- `.actor/input_schema.json` — 入力パラメータ定義

### CI/CD
- GitHub Actions対応: シークレットにAPIトークンを保存 → `apify push`で自動デプロイ
- ソースコード3MB以下 → 個別ファイルとしてアップロード（Web IDEで編集可能）
- 3MB超 → Zipファイルとしてアップロード

## 3. デプロイ・公開

### デプロイ（`apify push`）
```bash
apify push
```
- `.actor/actor.json`の設定に基づきクラウドにアップロード
- 自動ビルド実行
- トークンは `~/.apify/auth.json` に保存済み

### Store公開の必須項目
1. **アイコン** — Actor用アイコン画像
2. **Actor名** — わかりやすい名前
3. **説明文（Description）** — 短い概要
4. **README** — 詳細な使い方、入出力の説明
5. **カテゴリ** — 適切なカテゴリ選択

すべて入力すると「Publish to Store」ボタンが有効化 → 公開

### 公開後の義務
- **週約2時間**のメンテナンス（バグ修正、アップデート、ユーザーサポート）
- テスト（自動 or 手動）のセットアップ推奨

### 審査プロセス
- 厳密な手動レビューではなく、必須フィールド入力で公開可能
- ただし品質基準あり（ドキュメント充実、動作安定性）

## 4. 収益化・価格設定

### 3つの価格モデル

| モデル | 仕組み | Apify手数料 | 備考 |
|--------|--------|-------------|------|
| **Pay Per Event (PPE)** | 開発者が定義したイベント（結果1件、Actor起動等）ごとに課金 | プラットフォームコスト + 利益の20% | **推奨（主流）** |
| **Pay Per Result (PPR)** | 結果数に応じて課金。ユーザーはプラットフォーム使用料を払わない | プラットフォームコスト + 利益の20% | PPEに類似 |
| **Rental（レンタル）** | 月額固定料金 | 収益の20% | **2026年10月に廃止予定** |

### Rentalモデル廃止スケジュール
- **2026年4月1日**: 新規Rental Actor作成・価格変更不可
- **2026年10月1日**: Rental完全廃止、Pay-per-usageに強制移行

### 価格設定方法
1. Apify Console → Actor → Publication タブ
2. Monetization セクション → 請求・支払い情報入力
3. 価格モデル選択 → ウィザードに従って設定

### 注意事項
- 価格の大幅変更は**月1回まで**、変更は**14日後に有効化**
- 無料Actorと有料Actorの切り替えも可能

## 5. 支払い・ペイアウト

### 支払い方法

| 方法 | 最低支払額 | 備考 |
|------|-----------|------|
| **PayPal** | $20 | 最も手軽 |
| **Wire Transfer（SWIFT送金）** | $100 | チェコから送金。中継銀行手数料$10-50 |
| **Wise** | 不明 | アフィリエイトプログラムでは利用可能 |

### 支払いサイクル
1. **毎月11日**: 前月分のペイアウト請求書が自動生成
2. **3日間**: 開発者がレビュー（承認 or 修正依頼）
3. **14日**: 未対応なら自動承認
4. 承認後、まもなく送金

### KYC要件（本人確認）
- **必須**。KYC完了までペイアウト処理されない
- 必要書類:
  - 政府発行の身分証明書（パスポート等）
  - 住所証明
  - 税務書類
  - 実質的所有者情報（UBO）
- KYCに合格しない場合、アカウント停止・残高没収の可能性あり

### パラグアイ対応
- **明確な情報なし**。Apifyのドキュメントに国別制限リストは見つからず
- PayPalはパラグアイで利用可能（PayPal公式で対応国に含まれる）
- Wire Transfer（SWIFT）はパラグアイの銀行口座で受取可能
- **推奨**: 登録前にApifyサポートに確認するか、PayPalでの受取を前提にする

## 6. 収益ポテンシャル

- **トップ開発者**: 月$10,000以上のMRR
- **中堅開発者**: 月$1,000-2,000
- **マーケットプレイス規模**: 月間アクティブユーザー50,000人以上
- **開発者取り分**: 収益の80%（Apifyが20%手数料）

## 7. 自動化まとめ（CLI/APIでできること）

| 操作 | 自動化可能？ | 方法 |
|------|-------------|------|
| アカウント作成 | ❌ | Web UIのみ |
| ログイン | ✅ | `apify login --token` |
| Actor作成 | ✅ | `apify create` |
| ローカル実行 | ✅ | `apify run` |
| デプロイ | ✅ | `apify push` |
| CI/CDデプロイ | ✅ | GitHub Actions |
| Store公開 | ⚠️ | 初回はConsole UIで設定が必要。以降の更新はCLI |
| 価格設定 | ⚠️ | Console UIで設定 |
| KYC | ❌ | 手動（書類提出） |
| ペイアウト確認 | ✅ | API経由 |

## 8. 開発の流れ（実践チェックリスト）

1. [ ] Apifyアカウント作成（Web UI）
2. [ ] APIトークン取得
3. [ ] `npm install -g apify-cli`
4. [ ] `apify login --token <TOKEN>`
5. [ ] `apify create <name> --template python-start`
6. [ ] Actor開発・ローカルテスト（`apify run`）
7. [ ] `apify push` でデプロイ
8. [ ] Console UIでPublication設定（アイコン、説明、README、カテゴリ）
9. [ ] 「Publish to Store」で公開
10. [ ] Monetization設定（PPE推奨）
11. [ ] KYC書類提出
12. [ ] PayPal連携設定

---

## Sources

- [Deployment | Apify Docs](https://docs.apify.com/platform/actors/development/deployment)
- [Local Actor development](https://docs.apify.com/platform/actors/development/quick-start/locally)
- [Publishing your Actor](https://docs.apify.com/academy/deploying-your-code/deploying)
- [Apify CLI Reference](https://docs.apify.com/cli/docs/reference)
- [Monetize your Actor](https://docs.apify.com/platform/actors/publishing/monetize)
- [How Actor monetization works](https://docs.apify.com/academy/actor-marketing-playbook/store-basics/how-actor-monetization-works)
- [How developer payouts work](https://help.apify.com/en/articles/10057167-how-developer-payouts-work)
- [Store Publishing Terms](https://docs.apify.com/legal/store-publishing-terms-and-conditions)
- [Pay per event](https://docs.apify.com/platform/actors/publishing/monetize/pay-per-event)
- [Apify SDK Python](https://docs.apify.com/sdk/python/)
- [Actor Templates (GitHub)](https://github.com/apify/actor-templates)
- [Publish your Actor](https://docs.apify.com/platform/actors/publishing/publish)
- [Monetize your code](https://apify.com/partners/actor-developers)
- [CI/CD for Actors](https://use-apify.com/docs/apify-for-developers/apify-github-cicd)
