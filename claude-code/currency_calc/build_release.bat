@echo off
chcp 65001 >nul
echo ==========================================
echo  CurrencyCalc - リリースビルド
echo ==========================================
echo.

cd /d "%~dp0"

REM Step 1: 署名キーの確認
if not exist "android\key.properties" (
    echo [INFO] 署名キーを作成します...
    echo.

    REM keytoolでキーストア作成
    if not exist "android\keystore.jks" (
        echo キーストアを生成中...
        keytool -genkey -v -keystore android\keystore.jks -storetype JKS -keyalg RSA -keysize 2048 -validity 10000 -alias currency_calc
        echo.
    )

    REM key.properties作成
    echo storePassword=（上で設定したパスワード）> android\key.properties
    echo keyPassword=（上で設定したパスワード）>> android\key.properties
    echo keyAlias=currency_calc>> android\key.properties
    echo storeFile=keystore.jks>> android\key.properties
    echo.
    echo [重要] android\key.properties を編集して、実際のパスワードを入力してください。
    echo        編集後、このスクリプトを再実行してください。
    echo.
    pause
    exit /b 0
)

REM Step 2: クリーンビルド
echo [INFO] クリーンビルド実行中...
flutter clean
flutter pub get
echo.

REM Step 3: AABビルド (Google Play用)
echo [INFO] App Bundle (AAB) をビルド中...
flutter build appbundle --release
echo.

if exist "build\app\outputs\bundle\release\app-release.aab" (
    echo ==========================================
    echo  ビルド成功！
    echo ==========================================
    echo.
    echo AABファイル: build\app\outputs\bundle\release\app-release.aab
    echo.
    echo このファイルを Google Play Console にアップロードしてください。
) else (
    echo [ERROR] ビルドに失敗しました。エラーメッセージを確認してください。
)

echo.

REM Step 4: APKもビルド（テスト用）
echo [INFO] テスト用APKもビルド中...
flutter build apk --release
echo.

if exist "build\app\outputs\flutter-apk\app-release.apk" (
    echo テスト用APK: build\app\outputs\flutter-apk\app-release.apk
    echo （実機に直接インストールしてテストできます）
)

echo.
pause
