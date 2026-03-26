---
name: Vercelデプロイ前の確認必須
description: デプロイ前にプロジェクトID・ディレクトリを必ず確認。keisan-toolsとpseo-saasの混同事故（2026-03-26）の再発防止
type: feedback
---

Vercelデプロイ前に必ず `.vercel/project.json` の projectId と projectName を確認してから実行すること。

**Why:** 2026-03-26にpseo-saas（AI Tool Compare）を誤ってkeisan-toolsのVercelプロジェクト「site」にデプロイし、keisan-tools.comにpSEOの内容が表示される事故が発生。両プロジェクトのサブディレクトリ名が同じ `site/` だったことが原因。

**How to apply:**
1. デプロイ前: `cat .vercel/project.json` でprojectNameとprojectIdを確認
2. デプロイ前: `package.json` の name フィールドも照合
3. デプロイ後: 本番URLにアクセスして表示内容が正しいことを確認
4. 特にkeisan-tools (`site/`) と pseo-saas (`site/`) は混同リスクが高いので要注意
