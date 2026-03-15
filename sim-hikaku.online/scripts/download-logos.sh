#!/bin/bash
# =============================================================================
# sim-hikaku.online ロゴ・画像ダウンロードスクリプト
# 格安SIMキャリア・eSIMサービスの公式ロゴ・OGP画像
# =============================================================================
# 使い方: bash scripts/download-logos.sh
# ※ プロキシなしのローカル環境で実行してください
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOGOS_DIR="$PROJECT_DIR/images/logos"
STOCK_DIR="$PROJECT_DIR/images/stock"
OGP_DIR="$PROJECT_DIR/images/ogp"

mkdir -p "$LOGOS_DIR" "$STOCK_DIR" "$OGP_DIR"

UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

download() {
    local url="$1"
    local output="$2"
    local desc="$3"

    if [ -f "$output" ]; then
        echo "  [SKIP] $desc (already exists)"
        return 0
    fi

    echo "  [DL] $desc"
    if curl -sL -A "$UA" -o "$output" --max-time 30 "$url"; then
        if [ ! -s "$output" ]; then
            echo "  [WARN] $desc - empty file, removed"
            rm -f "$output"
            return 1
        fi
        echo "  [OK] $desc ($(du -h "$output" | cut -f1))"
        return 0
    else
        echo "  [FAIL] $desc"
        rm -f "$output"
        return 1
    fi
}

download_ogp() {
    local url="$1"
    local output="$2"
    local desc="$3"

    if [ -f "$output" ]; then
        echo "  [SKIP] $desc OGP (already exists)"
        return 0
    fi

    echo "  [FETCH OGP] $desc ..."
    local html
    html=$(curl -sL -A "$UA" --max-time 15 "$url" 2>/dev/null)
    local ogp_url
    ogp_url=$(echo "$html" | grep -oP 'property="og:image"\s+content="\K[^"]+' | head -1)
    if [ -z "$ogp_url" ]; then
        ogp_url=$(echo "$html" | grep -oP 'content="\K[^"]+(?="\s+property="og:image")' | head -1)
    fi

    if [ -n "$ogp_url" ]; then
        case "$ogp_url" in
            http*) ;;
            //*) ogp_url="https:$ogp_url" ;;
            /*) ogp_url="$(echo "$url" | grep -oP 'https?://[^/]+')$ogp_url" ;;
        esac
        download "$ogp_url" "$output" "$desc OGP"
    else
        echo "  [WARN] $desc - og:image not found"
        return 1
    fi
}

download_favicon() {
    local domain="$1"
    local output="$2"
    local desc="$3"

    download "https://www.google.com/s2/favicons?domain=${domain}&sz=128" "$output" "$desc favicon"
}

echo "============================================="
echo "sim-hikaku.online 画像ダウンロード開始"
echo "============================================="

# =============================================================================
# 1. 大手キャリアサブブランド
# =============================================================================
echo ""
echo "--- 大手キャリアサブブランド ---"

# UQモバイル
download_ogp "https://www.uqwimax.jp/mobile/" "$OGP_DIR/uq-mobile-ogp.png" "UQ mobile"
download_favicon "uqwimax.jp" "$LOGOS_DIR/uq-mobile.png" "UQ mobile"

# ワイモバイル
download_ogp "https://www.ymobile.jp/" "$OGP_DIR/ymobile-ogp.png" "Y!mobile"
download_favicon "ymobile.jp" "$LOGOS_DIR/ymobile.png" "Y!mobile"

# =============================================================================
# 2. 大手キャリアオンライン専用プラン
# =============================================================================
echo ""
echo "--- オンライン専用プラン ---"

# ahamo
download_ogp "https://ahamo.com/" "$OGP_DIR/ahamo-ogp.png" "ahamo"
download_favicon "ahamo.com" "$LOGOS_DIR/ahamo.png" "ahamo"

# LINEMO
download_ogp "https://www.linemo.jp/" "$OGP_DIR/linemo-ogp.png" "LINEMO"
download_favicon "linemo.jp" "$LOGOS_DIR/linemo.png" "LINEMO"

# povo2.0
download_ogp "https://povo.jp/" "$OGP_DIR/povo-ogp.png" "povo2.0"
download_favicon "povo.jp" "$LOGOS_DIR/povo.png" "povo2.0"

# =============================================================================
# 3. 楽天モバイル
# =============================================================================
echo ""
echo "--- 楽天モバイル ---"

download_ogp "https://network.mobile.rakuten.co.jp/" "$OGP_DIR/rakuten-mobile-ogp.png" "rakuten mobile"
download_favicon "network.mobile.rakuten.co.jp" "$LOGOS_DIR/rakuten-mobile.png" "rakuten mobile"

# =============================================================================
# 4. MVNO（格安SIM）
# =============================================================================
echo ""
echo "--- MVNO（格安SIM） ---"

# mineo
download_ogp "https://mineo.jp/" "$OGP_DIR/mineo-ogp.png" "mineo"
download_favicon "mineo.jp" "$LOGOS_DIR/mineo.png" "mineo"

# IIJmio
download_ogp "https://www.iijmio.jp/" "$OGP_DIR/iijmio-ogp.png" "IIJmio"
download_favicon "iijmio.jp" "$LOGOS_DIR/iijmio.png" "IIJmio"

# HISモバイル
download_ogp "https://his-mobile.com/" "$OGP_DIR/his-mobile-ogp.png" "HIS mobile"
download_favicon "his-mobile.com" "$LOGOS_DIR/his-mobile.png" "HIS mobile"

# 日本通信SIM
download_ogp "https://www.nihontsushin.com/" "$OGP_DIR/nihon-tsushin-ogp.png" "nihon tsushin"
download_favicon "nihontsushin.com" "$LOGOS_DIR/nihon-tsushin.png" "nihon tsushin"

# TONEモバイル
download_ogp "https://tone.ne.jp/" "$OGP_DIR/tone-mobile-ogp.png" "TONE mobile"
download_favicon "tone.ne.jp" "$LOGOS_DIR/tone-mobile.png" "TONE mobile"

# BIGLOBEモバイル
download_ogp "https://join.biglobe.ne.jp/mobile/" "$OGP_DIR/biglobe-mobile-ogp.png" "BIGLOBE mobile"
download_favicon "biglobe.ne.jp" "$LOGOS_DIR/biglobe-mobile.png" "BIGLOBE mobile"

# NUROモバイル
download_ogp "https://mobile.nuro.jp/" "$OGP_DIR/nuro-mobile-ogp.png" "NURO mobile"
download_favicon "nuro.jp" "$LOGOS_DIR/nuro-mobile.png" "NURO mobile"

# イオンモバイル
download_ogp "https://aeonmobile.jp/" "$OGP_DIR/aeon-mobile-ogp.png" "AEON mobile"
download_favicon "aeonmobile.jp" "$LOGOS_DIR/aeon-mobile.png" "AEON mobile"

# LIBMO
download_ogp "https://www.libmo.jp/" "$OGP_DIR/libmo-ogp.png" "LIBMO"
download_favicon "libmo.jp" "$LOGOS_DIR/libmo.png" "LIBMO"

# J:COMモバイル
download_ogp "https://www.jcom.co.jp/service/mobile/" "$OGP_DIR/jcom-mobile-ogp.png" "J:COM mobile"
download_favicon "jcom.co.jp" "$LOGOS_DIR/jcom-mobile.png" "J:COM mobile"

# =============================================================================
# 5. eSIMサービス（海外旅行向け）
# =============================================================================
echo ""
echo "--- eSIMサービス ---"

# TRAVeSIM（提携済み）
download_ogp "https://travesim.com/" "$OGP_DIR/travesim-ogp.png" "TRAVeSIM"
download_favicon "travesim.com" "$LOGOS_DIR/travesim.png" "TRAVeSIM"

# Voye Global（提携済み）
download_ogp "https://voye.global/" "$OGP_DIR/voye-global-ogp.png" "Voye Global"
download_favicon "voye.global" "$LOGOS_DIR/voye-global.png" "Voye Global"

# Airalo
download_ogp "https://www.airalo.com/" "$OGP_DIR/airalo-ogp.png" "Airalo"
download_favicon "airalo.com" "$LOGOS_DIR/airalo.png" "Airalo"

# trifa
download_ogp "https://www.trifa.co.jp/" "$OGP_DIR/trifa-ogp.png" "trifa"
download_favicon "trifa.co.jp" "$LOGOS_DIR/trifa.png" "trifa"

# Ubigi
download_ogp "https://www.ubigi.com/" "$OGP_DIR/ubigi-ogp.png" "Ubigi"
download_favicon "ubigi.com" "$LOGOS_DIR/ubigi.png" "Ubigi"

# Holafly
download_ogp "https://www.holafly.com/ja" "$OGP_DIR/holafly-ogp.png" "Holafly"
download_favicon "holafly.com" "$LOGOS_DIR/holafly.png" "Holafly"

# =============================================================================
# 6. 大手キャリア（MNO）- 比較参考用
# =============================================================================
echo ""
echo "--- 大手キャリア（MNO） ---"

# NTTドコモ
download_ogp "https://www.docomo.ne.jp/" "$OGP_DIR/docomo-ogp.png" "docomo"
download_favicon "docomo.ne.jp" "$LOGOS_DIR/docomo.png" "docomo"

# au
download_ogp "https://www.au.com/" "$OGP_DIR/au-ogp.png" "au"
download_favicon "au.com" "$LOGOS_DIR/au.png" "au"

# SoftBank
download_ogp "https://www.softbank.jp/" "$OGP_DIR/softbank-ogp.png" "SoftBank"
download_favicon "softbank.jp" "$LOGOS_DIR/softbank.png" "SoftBank"

# =============================================================================
# 7. 汎用素材画像（Unsplash - フリー素材）
# =============================================================================
echo ""
echo "--- 汎用素材画像（Unsplash） ---"

# スマートフォン・SIM系
download "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=1200&q=80" \
    "$STOCK_DIR/smartphone-01.jpg" "smartphone"
download "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=1200&q=80" \
    "$STOCK_DIR/smartphone-app-02.jpg" "smartphone app"
download "https://images.unsplash.com/photo-1598128558393-70ff21f8be44?w=1200&q=80" \
    "$STOCK_DIR/smartphone-woman-03.jpg" "woman using phone"
download "https://images.unsplash.com/photo-1523206489230-c012c64b2b48?w=1200&q=80" \
    "$STOCK_DIR/smartphone-hand-04.jpg" "holding phone"

# SIMカード系
download "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=1200&q=80" \
    "$STOCK_DIR/sim-card-01.jpg" "SIM card"
download "https://images.unsplash.com/photo-1616348436168-de43ad0db179?w=1200&q=80" \
    "$STOCK_DIR/sim-card-02.jpg" "SIM card tray"

# 料金・お金系
download "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=1200&q=80" \
    "$STOCK_DIR/savings-money-01.jpg" "savings money"
download "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=1200&q=80" \
    "$STOCK_DIR/money-calculator-02.jpg" "money calculator"
download "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=1200&q=80" \
    "$STOCK_DIR/cost-comparison-03.jpg" "cost comparison"

# 速度・通信系
download "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1200&q=80" \
    "$STOCK_DIR/network-speed-01.jpg" "network speed"
download "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=1200&q=80" \
    "$STOCK_DIR/wifi-signal-02.jpg" "wifi signal"

# 海外旅行・eSIM系
download "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=1200&q=80" \
    "$STOCK_DIR/travel-01.jpg" "travel"
download "https://images.unsplash.com/photo-1503220317375-aabd7a8b9de4?w=1200&q=80" \
    "$STOCK_DIR/travel-airport-02.jpg" "travel airport"
download "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=1200&q=80" \
    "$STOCK_DIR/travel-abroad-03.jpg" "travel abroad"
download "https://images.unsplash.com/photo-1530521954074-e64f6810b32d?w=1200&q=80" \
    "$STOCK_DIR/travel-phone-04.jpg" "travel with phone"

# 家族・学生プラン系
download "https://images.unsplash.com/photo-1511895426328-dc8714191300?w=1200&q=80" \
    "$STOCK_DIR/family-01.jpg" "family"
download "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=1200&q=80" \
    "$STOCK_DIR/family-happy-02.jpg" "happy family"
download "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=1200&q=80" \
    "$STOCK_DIR/student-03.jpg" "student"

# 比較・選択系
download "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1200&q=80" \
    "$STOCK_DIR/comparison-checklist-01.jpg" "comparison checklist"
download "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1200&q=80" \
    "$STOCK_DIR/analysis-02.jpg" "analysis"

# 乗り換え・MNP系
download "https://images.unsplash.com/photo-1556742044-3c52d6e88c62?w=1200&q=80" \
    "$STOCK_DIR/switch-change-01.jpg" "switch change"

# パラグアイ・南米系（差別化コンテンツ用）
download "https://images.unsplash.com/photo-1619546952812-520e98064a52?w=1200&q=80" \
    "$STOCK_DIR/south-america-01.jpg" "south america"
download "https://images.unsplash.com/photo-1591985666643-5a1e77f4223c?w=1200&q=80" \
    "$STOCK_DIR/paraguay-02.jpg" "paraguay"

echo ""
echo "============================================="
echo "ダウンロード完了！"
echo "============================================="
echo ""
echo "保存先:"
echo "  ロゴ: $LOGOS_DIR/"
echo "  OGP: $OGP_DIR/"
echo "  素材: $STOCK_DIR/"
echo ""
echo "ファイル数:"
echo "  ロゴ: $(find "$LOGOS_DIR" -type f 2>/dev/null | wc -l) files"
echo "  OGP:  $(find "$OGP_DIR" -type f 2>/dev/null | wc -l) files"
echo "  素材: $(find "$STOCK_DIR" -type f 2>/dev/null | wc -l) files"
