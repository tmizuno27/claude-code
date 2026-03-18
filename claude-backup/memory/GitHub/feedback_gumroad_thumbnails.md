---
name: Gumroad出品時はサムネイル・Cover画像を必ず含める
description: Gumroad商品出品時にサムネイル画像なしで出品しない。コンバージョン率が2倍違う。手動作業（Canva等）ではなくPython/Pillowで自動生成すること
type: feedback
---

Gumroad商品を出品する際は、必ずThumbnail（600x600px正方形）とCover画像（1280x720px横長）を含めること。

**Why:** サムネなしだとコンバージョン率が約半分に下がる。1本目のFreelance Business OSをサムネなしで出品してしまい、ユーザーから「なぜ提案しなかったのか」と指摘された。また、Canva等の手動ツールでの作成はユーザーの負担になるため却下された。

**How to apply:** 出品時は `generate_thumbnails.py` でPython/Pillowを使い自動生成する。ユーザーに手動作業を求めない。画像生成はClaude側で完結させること。
