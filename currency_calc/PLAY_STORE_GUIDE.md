# Google Play Store 公開ガイド

## 全体の流れ

```
1. 環境セットアップ → 2. ビルド確認 → 3. 署名キー作成 → 4. リリースビルド
→ 5. Play Console登録 → 6. アプリ登録 → 7. ストア掲載情報 → 8. リリース
```

---

## Step 1: Flutter 環境セットアップ

### 1-1. Flutter SDK インストール

1. **https://docs.flutter.dev/get-started/install/windows/mobile** にアクセス
2. 「Download Flutter SDK」をクリック
3. ダウンロードしたZIPを `C:\flutter` に展開
4. 環境変数 PATH に `C:\flutter\bin` を追加
   - Windows設定 → システム → 詳細情報 → 環境変数の詳細設定
   - Path → 編集 → 新規 → `C:\flutter\bin`

### 1-2. Android SDK (Android Studio経由)

1. **https://developer.android.com/studio** から Android Studio をダウンロード・インストール
2. 初回起動でSDKが自動的にインストールされる
3. SDK Manager で以下を確認：
   - Android SDK Platform (API 35)
   - Android SDK Build-Tools
   - Android SDK Command-line Tools

### 1-3. VSCode 拡張機能

VSCode で以下の拡張機能をインストール：
- **Flutter** (Dart-Code.flutter)
- **Dart** (Dart-Code.dart-code)

### 1-4. 環境確認

```bash
flutter doctor
```

すべてのチェックが ✓ になることを確認。

---

## Step 2: プロジェクトセットアップ

```bash
cd "c:\Users\tmizu\マイドライブ\cloude-code\currency_calc"

# setup_and_build.bat を実行（推奨）
.\setup_and_build.bat

# または手動で：
flutter create --org com.personal --project-name currency_calc .
flutter pub get
```

### デバッグ実行で動作確認

```bash
# エミュレータで実行
flutter run

# または実機をUSB接続して
flutter run -d <デバイスID>

# 接続デバイス一覧
flutter devices
```

---

## Step 3: アプリ署名キー作成

Google Play に公開するアプリには署名が必要です。

```bash
cd android

# キーストア作成（パスワードは忘れないように）
keytool -genkey -v -keystore keystore.jks -storetype JKS -keyalg RSA -keysize 2048 -validity 10000 -alias currency_calc
```

質問に答える：
- キーストアのパスワード → 任意のパスワード（メモしておく）
- 姓名 → あなたの名前
- 組織単位 → 空欄でOK
- 組織名 → 空欄でOK
- 都市名 → 空欄でOK
- 州名 → 空欄でOK
- 国番号 → JP

### key.properties ファイル作成

`android/key.properties` を作成：

```properties
storePassword=（設定したパスワード）
keyPassword=（設定したパスワード）
keyAlias=currency_calc
storeFile=keystore.jks
```

⚠️ **重要**: `keystore.jks` と `key.properties` は絶対にGitにコミットしないでください。

---

## Step 4: リリースビルド

```bash
cd "c:\Users\tmizu\マイドライブ\cloude-code\currency_calc"

# クリーンビルド
flutter clean
flutter pub get

# AABビルド（Play Store用）
flutter build appbundle --release

# APKビルド（テスト用）
flutter build apk --release
```

出力ファイル：
- AAB: `build/app/outputs/bundle/release/app-release.aab`
- APK: `build/app/outputs/flutter-apk/app-release.apk`

テスト用APKは実機に直接インストールして確認できます。

---

## Step 5: Google Play Developer アカウント登録

1. **https://play.google.com/console/signup** にアクセス
2. Googleアカウントでログイン
3. 登録料 **$25（一回払い）** を支払い
4. デベロッパー名を入力
5. 連絡先情報を入力
6. 本人確認を完了

※ アカウントが有効化されるまで最大48時間かかる場合あり

---

## Step 6: Play Console でアプリ作成

1. **Play Console** (https://play.google.com/console) にログイン
2. 「アプリを作成」をクリック
3. 以下を入力：
   - **アプリ名**: CurrencyCalc
   - **デフォルト言語**: 日本語
   - **アプリまたはゲーム**: アプリ
   - **無料または有料**: 無料
4. デベロッパーポリシーに同意

---

## Step 7: ストア掲載情報

### 7-1. アプリの基本情報

| 項目 | 内容 |
|------|------|
| アプリ名 | CurrencyCalc - 通貨計算機 |
| 簡単な説明 | JPY/USD/PYG 3通貨をリアルタイムで簡単換算 |

### 7-2. 詳しい説明（例）

```
毎日の通貨換算をシンプルに。

CurrencyCalcは、日本円(JPY)・米ドル(USD)・パラグアイグアラニー(PYG)の
3通貨間を電卓感覚でサクサク換算できるアプリです。

【特徴】
• 電卓スタイルの直感的なUI
• リアルタイム為替レート自動取得
• 3通貨同時表示で一目瞭然
• オフラインでもキャッシュレートで利用可能
• ダーク/ライトモード対応

【対応通貨】
• 🇯🇵 日本円 (JPY)
• 🇺🇸 米ドル (USD)
• 🇵🇾 パラグアイグアラニー (PYG)
```

### 7-3. 必要な画像

| 種類 | サイズ | 枚数 |
|------|--------|------|
| アプリアイコン | 512x512 px | 1枚 |
| スクリーンショット | 任意（縦長推奨） | 2〜8枚 |
| フィーチャーグラフィック | 1024x500 px | 1枚 |

**スクリーンショットの撮り方:**
```bash
# エミュレータで実行中にスクリーンショットを撮る
flutter screenshot --out=screenshot1.png
```

### 7-4. コンテンツレーティング

Play Console の「コンテンツのレーティング」でアンケートに回答。
通貨計算アプリなので、基本的にすべて「いいえ」で回答 → 「全年齢」になります。

### 7-5. プライバシーポリシー

個人使用アプリでも必要。シンプルなもので大丈夫です。
Google Sites 等で無料ページを作成し、URLを設定。

---

## Step 8: アプリのリリース

### 8-1. 内部テスト（推奨）

1. Play Console → 「テスト」→「内部テスト」
2. 「新しいリリースを作成」
3. `app-release.aab` をアップロード
4. リリース名（例: 1.0.0）を入力
5. テスターのメールアドレスを追加（自分のGmail）
6. 「リリースの確認」→「公開開始」

テストリンクが発行され、自分の端末でインストール・テスト可能。

### 8-2. 製品版リリース

テストで問題なければ：

1. Play Console →「製品版」→「新しいリリースを作成」
2. 内部テストと同じAABを使用（または「リリースを昇格」）
3. 国/地域を選択（日本のみ、もしくは全世界）
4. 「リリースの確認」→「公開開始」

※ Google の審査（通常数時間〜数日）後に公開されます。

---

## トラブルシューティング

### flutter doctor で問題がある場合
```bash
# Android ライセンスの同意
flutter doctor --android-licenses

# Flutter をアップデート
flutter upgrade
```

### ビルドエラーが出る場合
```bash
flutter clean
flutter pub get
flutter build appbundle --release
```

### デバイスが認識されない場合
- USB デバッグを有効にする（設定→開発者向けオプション）
- 「ビルド番号」を7回タップで開発者向けオプションが表示される

---

## ファイル一覧（重要なもの）

```
currency_calc/
├── lib/                          # ← Dartソースコード
│   ├── main.dart
│   ├── models/currency.dart
│   ├── services/exchange_rate_service.dart
│   ├── providers/calculator_provider.dart
│   ├── screens/calculator_screen.dart
│   └── widgets/
│       ├── currency_display.dart
│       └── calculator_keypad.dart
├── android/
│   ├── app/
│   │   ├── build.gradle.kts      # ← Android ビルド設定
│   │   ├── proguard-rules.pro
│   │   └── src/main/AndroidManifest.xml
│   ├── key.properties            # ← 署名キー設定（自分で作成）
│   └── keystore.jks              # ← 署名キー（自分で作成）
├── pubspec.yaml                  # ← パッケージ設定
├── setup_and_build.bat           # ← セットアップスクリプト
├── build_release.bat             # ← リリースビルドスクリプト
└── PLAY_STORE_GUIDE.md           # ← このガイド
```
