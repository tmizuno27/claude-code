@echo off
chcp 65001 >nul
echo ==========================================
echo  CurrencyCalc - セットアップ＆ビルドスクリプト
echo ==========================================
echo.

REM Step 1: Flutterがインストールされているか確認
where flutter >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Flutter SDK が見つかりません。
    echo.
    echo 以下の手順で Flutter をインストールしてください:
    echo 1. https://docs.flutter.dev/get-started/install/windows/mobile にアクセス
    echo 2. Flutter SDK をダウンロード
    echo 3. 展開したフォルダの flutter\bin を環境変数 PATH に追加
    echo 4. このスクリプトを再実行
    echo.
    pause
    exit /b 1
)

echo [OK] Flutter SDK が見つかりました
flutter --version
echo.

REM Step 2: Flutter doctor で環境チェック
echo [INFO] 開発環境を確認中...
flutter doctor
echo.

REM Step 3: プロジェクト初期化
echo [INFO] Flutterプロジェクトを初期化中...
cd /d "%~dp0"

REM flutter create で足りないファイルを生成（既存ファイルは上書きしない）
if not exist "android\settings.gradle" (
    echo [INFO] Android プロジェクトファイルを生成中...
    flutter create --org com.personal --project-name currency_calc .
)

REM Step 4: パッケージ取得
echo [INFO] パッケージを取得中...
flutter pub get
echo.

echo ==========================================
echo  セットアップ完了！
echo ==========================================
echo.
echo 次のステップ:
echo   デバッグ実行:   flutter run
echo   リリースビルド: build_release.bat を実行
echo.
pause
