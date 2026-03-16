---
name: アクセストレード提携進捗
description: アクセストレードASPの3サイト登録状況と、承認後にアフィリエイトリンク一括挿入を行う予定
type: project
---

アクセストレードで3サイトの副サイト登録を進行中。

- **nambei-oyaji.com**: 承認済み（2026-03-16時点）
- **sim-hikaku.online**: 承認済み（2026-03-16時点）
- **otona-match.com**: 申請中（2026-03-16時点）

**Why:** アクセストレードはpovo、IIJmio、ahamo、HISモバイル、日本通信SIM、BIGLOBEモバイル、NUROモバイル、イオンモバイル等の格安SIM案件が多く、sim-hikaku.onlineの収益化に不可欠。

**How to apply:** otona-match.comの承認が降りたら、以下を一気に実行する：
1. 3サイトともアクセストレードでおすすめプログラムを提携申請
2. 取得したリンクURLを各サイトの `config/affiliate-links.json` に登録
3. 既に作成済みの `insert_affiliate_all.py` スクリプトで全記事に一括挿入

スクリプトの場所：
- `nambei-oyaji.com/scripts/publishing/insert_affiliate_all.py`
- `otona-match.com/scripts/insert_affiliate_all.py`
- `sim-hikaku.online/scripts/publishing/insert_affiliate_all.py`
