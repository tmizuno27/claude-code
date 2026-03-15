---
name: blog-frontpage-design
description: トップページデザイン（PC版完成状態）の技術詳細。Cocoonテーマ上書き対策・CSS値・構成
type: project
---

## トップページデザイン（PC版完成 2026-03-14）

**ファイル**: `claude-code/nambei-oyaji.com/theme/new-front-page.html` → WordPress page ID:47

### Cocoon対策（最重要）
- Cocoonテーマがh1/h2/h3のfont-sizeを強制上書きする → **全見出しに`!important`必須**
- h1-h4のborder/background/paddingもCocoonデフォルトで装飾される → global resetで`.nao-home h1-h4 { border:none!important; background:none!important; padding:0!important; }`
- `.nao-full`クラスで全幅: `width:100vw!important; position:relative; left:50%; transform:translateX(-50%)`
- CSS custom propertiesの色（`var(--nao-black)`等）がCocoon内で透明になる場合あり → 直接hex値+!importantで対処

### 主要CSS値（参考デザインと一致済み）
- Hero h1: **72px !important**, font-weight:700, line-height:1.05, letter-spacing:-0.025em
- Hero overtitle: 21px, Hero description: 21px
- Section h2: **56px !important**, line-height:1.07
- Theme card h3: **28px !important**, border-radius:28px, padding:40px 48px 36px
- Pillar icons: SVGアイコン in 72px白角丸ラップ（emojiではない）
- Latest Stories: gradient背景 `linear-gradient(180deg, #e8e8ed 0%, #d2d2d7 40%, #c7c7cc 100%)`、glassmorphismカード（aspect-ratio:1/1, backdrop-filter:blur(20px)）、静的6枚3x2
- Popular numbers: 48px, gradient fill (`background:linear-gradient(135deg,#d2d2d7,#e8e8ed); -webkit-background-clip:text`)、border: `rgba(0,0,0,0.06)`
- Topics: 白背景、17px font-size name、3x2グリッド
- Author: gradient bg, 140px avatar, 36px name, SVG国旗バッジ
- CTA: 黒背景, 56px h2白, 72px padding, 両ボタン青(nao-btn-primary)
- Footer: **ライトグレー** (#f5f5f7), Apple風、12px text, #6e6e73 links
- Buttons: padding:14px 32px, font-size:17px, font-weight:400, border-radius:980px
- Section padding: 72px (--nao-section-py)

### モバイル（768px以下）
- Hero h1: 40px !important
- Section h2: 36px !important
- CTA h2: 36px !important
- Grid→1列

### WordPress構成
- ページ本体: `new-front-page.html`の内容をREST APIでpage 47に投稿
- ウィジェット `custom_html-2`: IntersectionObserver（`.nao-anim`→`.nao-visible`）+ 最新記事/人気記事のfetch（※現在は静的カードに変更済み）
- `<script>`タグはentry-content内では実行されない → JSはウィジェット経由

**Why:** 参考デザイン（front-page-preview.html）との完全一致がゴール。Cocoonの上書きが最大の障壁だった
**How to apply:** トップページ修正時は必ず`!important`を付け、Puppeteerで計算値を検証すること
