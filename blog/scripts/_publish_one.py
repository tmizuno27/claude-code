"""食文化の記事1本だけをWordPressに即時公開する一時スクリプト"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from wp_publisher import load_config, parse_front_matter, publish_to_wordpress, save_wp_log, load_wp_log

target = Path(__file__).parent.parent / "outputs" / "articles" / "2026-03-03" / "article-paraguay-shokubunka.md"
content = target.read_text(encoding="utf-8")
fm, body = parse_front_matter(content)
article = {
    "path": target,
    "relative_path": str(target.relative_to(Path(__file__).parent.parent)),
    "front_matter": fm,
    "body": body,
}
config = load_config()

# secrets.json から認証情報をマージ
secrets_path = Path(__file__).parent.parent / "config" / "secrets.json"
with open(secrets_path, "r", encoding="utf-8") as f:
    secrets = __import__("json").load(f)
config["wordpress"]["username"] = secrets["wordpress"]["username"]
config["wordpress"]["app_password"] = secrets["wordpress"]["app_password"]

result = publish_to_wordpress(config, article, status="publish")
if result:
    wp_log = load_wp_log()
    wp_log["posts"].append(result)
    save_wp_log(wp_log)
    url = result["url"]
    edit_url = result["edit_url"]
    print(f"SUCCESS: {url}")
    print(f"EDIT: {edit_url}")
else:
    print("FAILED")
    sys.exit(1)
