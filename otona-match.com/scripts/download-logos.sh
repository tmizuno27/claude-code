#!/bin/bash
# =============================================================================
# otona-match.com ロゴ・画像ダウンロードスクリプト
# マッチングアプリ・出会い系・婚活サービスの公式ロゴ・OGP画像
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
        # ファイルサイズチェック（0バイトなら削除）
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

# OGP画像を取得するヘルパー関数
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
        # 相対URLの場合はベースURLを付加
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

# Favicon取得
download_favicon() {
    local domain="$1"
    local output="$2"
    local desc="$3"

    download "https://www.google.com/s2/favicons?domain=${domain}&sz=128" "$output" "$desc favicon"
}

echo "============================================="
echo "otona-match.com 画像ダウンロード開始"
echo "============================================="

# =============================================================================
# 1. マッチングアプリ系ロゴ・OGP
# =============================================================================
echo ""
echo "--- マッチングアプリ系 ---"

# marrish（マリッシュ）
download_ogp "https://marrish.com/" "$OGP_DIR/marrish-ogp.png" "marrish"
download_favicon "marrish.com" "$LOGOS_DIR/marrish.png" "marrish"
download "https://marrish.com/img/common/logo.png" "$LOGOS_DIR/marrish-logo.png" "marrish logo"

# Pairs（ペアーズ）
download_ogp "https://www.pairs.lv/" "$OGP_DIR/pairs-ogp.png" "Pairs"
download_favicon "pairs.lv" "$LOGOS_DIR/pairs.png" "Pairs"

# Omiai
download_ogp "https://fb.omiai-jp.com/" "$OGP_DIR/omiai-ogp.png" "Omiai"
download_favicon "omiai-jp.com" "$LOGOS_DIR/omiai.png" "Omiai"

# with（ウィズ）
download_ogp "https://with.is/" "$OGP_DIR/with-ogp.png" "with"
download_favicon "with.is" "$LOGOS_DIR/with.png" "with"

# タップル
download_ogp "https://tapple.me/" "$OGP_DIR/tapple-ogp.png" "tapple"
download_favicon "tapple.me" "$LOGOS_DIR/tapple.png" "tapple"

# ゼクシィ縁結び
download_ogp "https://zexy-enmusubi.net/" "$OGP_DIR/zexy-enmusubi-ogp.png" "zexy-enmusubi"
download_favicon "zexy-enmusubi.net" "$LOGOS_DIR/zexy-enmusubi.png" "zexy-enmusubi"

# youbride（ユーブライド）
download_ogp "https://youbride.jp/" "$OGP_DIR/youbride-ogp.png" "youbride"
download_favicon "youbride.jp" "$LOGOS_DIR/youbride.png" "youbride"

# Match.com
download_ogp "https://jp.match.com/" "$OGP_DIR/match-ogp.png" "Match.com"
download_favicon "jp.match.com" "$LOGOS_DIR/match.png" "Match.com"

# Tinder
download_ogp "https://tinder.com/ja" "$OGP_DIR/tinder-ogp.png" "Tinder"
download_favicon "tinder.com" "$LOGOS_DIR/tinder.png" "Tinder"

# Bumble
download_ogp "https://bumble.com/ja" "$OGP_DIR/bumble-ogp.png" "Bumble"
download_favicon "bumble.com" "$LOGOS_DIR/bumble.png" "Bumble"

# =============================================================================
# 2. 出会い系サイト系ロゴ・OGP
# =============================================================================
echo ""
echo "--- 出会い系サイト系 ---"

# ワクワクメール
download_ogp "https://550909.com/" "$OGP_DIR/wakuwaku-mail-ogp.png" "wakuwaku-mail"
download_favicon "550909.com" "$LOGOS_DIR/wakuwaku-mail.png" "wakuwaku-mail"

# ハッピーメール
download_ogp "https://happymail.co.jp/" "$OGP_DIR/happy-mail-ogp.png" "happy-mail"
download_favicon "happymail.co.jp" "$LOGOS_DIR/happy-mail.png" "happy-mail"

# PCMAX
download_ogp "https://pcmax.jp/" "$OGP_DIR/pcmax-ogp.png" "PCMAX"
download_favicon "pcmax.jp" "$LOGOS_DIR/pcmax.png" "PCMAX"

# YYC
download_ogp "https://yyc.co.jp/" "$OGP_DIR/yyc-ogp.png" "YYC"
download_favicon "yyc.co.jp" "$LOGOS_DIR/yyc.png" "YYC"

# Jメール
download_ogp "https://mintj.com/" "$OGP_DIR/jmail-ogp.png" "Jmail"
download_favicon "mintj.com" "$LOGOS_DIR/jmail.png" "Jmail"

# イククル
download_ogp "https://www.194964.com/" "$OGP_DIR/ikukuru-ogp.png" "ikukuru"
download_favicon "194964.com" "$LOGOS_DIR/ikukuru.png" "ikukuru"

# =============================================================================
# 3. 婚活サービス系ロゴ・OGP
# =============================================================================
echo ""
echo "--- 婚活サービス系 ---"

# パートナーエージェント
download_ogp "https://www.p-a.jp/" "$OGP_DIR/partner-agent-ogp.png" "partner-agent"
download_favicon "p-a.jp" "$LOGOS_DIR/partner-agent.png" "partner-agent"

# ブライダルネット
download_ogp "https://www.bridalnet.co.jp/" "$OGP_DIR/bridalnet-ogp.png" "bridalnet"
download_favicon "bridalnet.co.jp" "$LOGOS_DIR/bridalnet.png" "bridalnet"

# ゼクシィ縁結びエージェント
download_ogp "https://zexy-en-soudan.net/" "$OGP_DIR/zexy-en-soudan-ogp.png" "zexy-en-soudan"
download_favicon "zexy-en-soudan.net" "$LOGOS_DIR/zexy-en-soudan.png" "zexy-en-soudan"

# オーネット
download_ogp "https://onet.co.jp/" "$OGP_DIR/onet-ogp.png" "onet"
download_favicon "onet.co.jp" "$LOGOS_DIR/onet.png" "onet"

# ツヴァイ
download_ogp "https://www.zwei.com/" "$OGP_DIR/zwei-ogp.png" "zwei"
download_favicon "zwei.com" "$LOGOS_DIR/zwei.png" "zwei"

# naco-do
download_ogp "https://naco-do.com/" "$OGP_DIR/naco-do-ogp.png" "naco-do"
download_favicon "naco-do.com" "$LOGOS_DIR/naco-do.png" "naco-do"

# スマリッジ
download_ogp "https://s-marriage.jp/" "$OGP_DIR/s-marriage-ogp.png" "s-marriage"
download_favicon "s-marriage.jp" "$LOGOS_DIR/s-marriage.png" "s-marriage"

# エン婚活エージェント
download_ogp "https://en-konkatsu.com/" "$OGP_DIR/en-konkatsu-ogp.png" "en-konkatsu"
download_favicon "en-konkatsu.com" "$LOGOS_DIR/en-konkatsu.png" "en-konkatsu"

# =============================================================================
# 4. 汎用素材画像（Unsplash - フリー素材）
# =============================================================================
echo ""
echo "--- 汎用素材画像（Unsplash） ---"

# カップル・恋愛系
download "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?w=1200&q=80" \
    "$STOCK_DIR/couple-dating-01.jpg" "couple dating"
download "https://images.unsplash.com/photo-1529333166437-7750a6dd5a70?w=1200&q=80" \
    "$STOCK_DIR/couple-cafe-02.jpg" "couple cafe"
download "https://images.unsplash.com/photo-1522098543979-ffc7f79a56c4?w=1200&q=80" \
    "$STOCK_DIR/couple-walking-03.jpg" "couple walking"
download "https://images.unsplash.com/photo-1543807535-eceef0bc6599?w=1200&q=80" \
    "$STOCK_DIR/couple-romantic-04.jpg" "couple romantic"
download "https://images.unsplash.com/photo-1518199266791-5375a83190b7?w=1200&q=80" \
    "$STOCK_DIR/couple-sunset-05.jpg" "couple sunset"

# スマホ操作系
download "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=1200&q=80" \
    "$STOCK_DIR/smartphone-use-01.jpg" "smartphone use"
download "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=1200&q=80" \
    "$STOCK_DIR/smartphone-app-02.jpg" "smartphone app"
download "https://images.unsplash.com/photo-1598128558393-70ff21f8be44?w=1200&q=80" \
    "$STOCK_DIR/smartphone-woman-03.jpg" "woman using phone"

# 30代・40代系
download "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1200&q=80" \
    "$STOCK_DIR/man-30s-01.jpg" "man 30s"
download "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=1200&q=80" \
    "$STOCK_DIR/woman-30s-01.jpg" "woman 30s"
download "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=1200&q=80" \
    "$STOCK_DIR/woman-smile-02.jpg" "woman smile"
download "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=1200&q=80" \
    "$STOCK_DIR/man-casual-02.jpg" "man casual"

# 婚活・結婚式系
download "https://images.unsplash.com/photo-1519741497674-611481863552?w=1200&q=80" \
    "$STOCK_DIR/wedding-01.jpg" "wedding"
download "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=1200&q=80" \
    "$STOCK_DIR/wedding-rings-02.jpg" "wedding rings"
download "https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6?w=1200&q=80" \
    "$STOCK_DIR/wedding-couple-03.jpg" "wedding couple"

# 安全・セキュリティ系
download "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=1200&q=80" \
    "$STOCK_DIR/security-01.jpg" "security"
download "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=1200&q=80" \
    "$STOCK_DIR/privacy-02.jpg" "privacy"

# 比較・選択系
download "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1200&q=80" \
    "$STOCK_DIR/comparison-checklist-01.jpg" "comparison checklist"
download "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1200&q=80" \
    "$STOCK_DIR/analysis-02.jpg" "analysis"

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
