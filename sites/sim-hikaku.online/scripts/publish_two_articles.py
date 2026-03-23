import requests
import re
from requests.auth import HTTPBasicAuth

WP_API = "https://sim-hikaku.online/wp-json/wp/v2"
WP_USER = "t.mizuno27@gmail.com"
WP_PASS = "P4A1 P4eh Nk0z 29An hS6H 9OHq"
auth = HTTPBasicAuth(WP_USER, WP_PASS)

AFFILIATE_LINKS = {
    "ymobile": "https://px.a8.net/svt/ejp?a8mat=4AZH48+1XNS3M+424K+BXIYQ",
    "his": "https://h.accesstrade.net/sp/cc?rk=0100pggx00ophx",
    "libmo": "https://h.accesstrade.net/sp/cc?rk=0100lmjk00ophx",
}


def inline_md(text):
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', text)
    text = re.sub(r'~~(.*?)~~', r'<del>\1</del>', text)
    def fix_link(m):
        lt = m.group(1)
        url = m.group(2)
        if url.startswith("/"):
            url = "https://sim-hikaku.online" + url
        return '<a href="' + url + '">' + lt + '</a>'
    text = re.sub(r'\[(.*?)\]\((.*?)\)', fix_link, text)
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    return text


def render_table(rows):
    out = ['<table style="width:100%; border-collapse:collapse; margin:15px 0;">']
    if rows:
        out.append("<thead><tr>")
        for c in rows[0]:
            out.append('<th style="padding:10px; border:1px solid #ddd; background:#f5f5f7; text-align:left;">' + inline_md(c) + '</th>')
        out.append("</tr></thead><tbody>")
        for row in rows[1:]:
            out.append("<tr>")
            for c in row:
                out.append('<td style="padding:10px; border:1px solid #ddd;">' + inline_md(c) + '</td>')
            out.append("</tr>")
        out.append("</tbody></table>")
    return "\n".join(out)


def md_to_html(md_text):
    parts = md_text.split("---", 2)
    if len(parts) >= 3:
        content = parts[2].strip()
    else:
        content = md_text.strip()

    lines = content.split("\n")
    html_lines = []
    in_table = False
    table_rows = []
    in_ul = False
    in_ol = False

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            html_lines.append("</ul>")
            in_ul = False
        if in_ol:
            html_lines.append("</ol>")
            in_ol = False

    def flush_table():
        nonlocal in_table, table_rows
        if in_table and table_rows:
            html_lines.append(render_table(table_rows))
        in_table = False
        table_rows = []

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # HTML pass-through
        if stripped.startswith("<") and not stripped.startswith("<span") and not stripped.startswith("</span"):
            flush_table()
            close_lists()
            html_lines.append(line)
            i += 1
            continue

        # Table
        if "|" in stripped and stripped.startswith("|") and stripped.endswith("|"):
            if not in_table:
                close_lists()
                in_table = True
                table_rows = []
            if re.match(r'^[\s|:\-]+$', stripped):
                i += 1
                continue
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            table_rows.append(cells)
            i += 1
            continue
        elif in_table:
            flush_table()

        # Headers
        hm = re.match(r'^(#{2,4})\s+(.*)', stripped)
        if hm:
            close_lists()
            level = len(hm.group(1))
            html_lines.append("<h" + str(level) + ">" + inline_md(hm.group(2)) + "</h" + str(level) + ">")
            i += 1
            continue

        # Blockquote
        if stripped.startswith("> "):
            close_lists()
            qt = inline_md(stripped[2:])
            html_lines.append('<blockquote style="border-left:3px solid #ccc; padding:10px 15px; margin:10px 0; color:#555; font-style:italic;">' + qt + '</blockquote>')
            i += 1
            continue

        # Unordered list
        if stripped.startswith("- "):
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            if not in_ul:
                html_lines.append("<ul>")
                in_ul = True
            html_lines.append("<li>" + inline_md(stripped[2:]) + "</li>")
            i += 1
            continue

        # Ordered list
        om = re.match(r'^(\d+)\.\s+(.*)', stripped)
        if om:
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if not in_ol:
                html_lines.append("<ol>")
                in_ol = True
            html_lines.append("<li>" + inline_md(om.group(2)) + "</li>")
            i += 1
            continue

        # Empty line
        if stripped == "":
            close_lists()
            i += 1
            continue

        # HR
        if stripped == "---":
            close_lists()
            html_lines.append("<hr>")
            i += 1
            continue

        # Comment
        if stripped.startswith("<!--"):
            i += 1
            continue

        # Paragraph
        close_lists()
        html_lines.append("<p>" + inline_md(stripped) + "</p>")
        i += 1

    close_lists()
    flush_table()

    return "\n".join(html_lines)


def insert_affiliate_cta(html):
    ymobile_cta = (
        '<div style="background:#fff8e1; border:2px solid #ffc107; border-radius:12px; '
        'padding:20px; margin:20px 0; text-align:center;">'
        '<p style="font-size:16px; font-weight:bold; margin-bottom:10px;">'
        '\u30ef\u30a4\u30e2\u30d0\u30a4\u30eb\u306e\u6700\u65b0\u30ad\u30e3\u30f3\u30da\u30fc\u30f3\u3092\u30c1\u30a7\u30c3\u30af</p>'
        '<a href="' + AFFILIATE_LINKS["ymobile"] + '" rel="nofollow" target="_blank" '
        'style="display:inline-block; background:#e4002b; color:#fff; padding:14px 40px; '
        'border-radius:8px; text-decoration:none; font-weight:bold; font-size:16px;">'
        '\u30ef\u30a4\u30e2\u30d0\u30a4\u30eb\u516c\u5f0f\u30b5\u30a4\u30c8\u306f\u3053\u3061\u3089</a></div>'
    )
    if "\u30ef\u30a4\u30e2\u30d0\u30a4\u30eb" in html:
        html = html + "\n" + ymobile_cta
    return html


def publish_article(wp_id, title, description, html_content):
    data = {
        "title": title,
        "content": html_content,
        "excerpt": description,
        "status": "publish",
    }
    resp = requests.post(
        WP_API + "/posts/" + str(wp_id),
        json=data,
        auth=auth,
        timeout=60,
    )
    if resp.status_code == 200:
        result = resp.json()
        return True, result.get("link", "")
    else:
        return False, "Error " + str(resp.status_code) + ": " + resp.text[:500]


def main():
    base = r"C:\Users\tmizu"
    base = base + "\\" + "\u30de\u30a4\u30c9\u30e9\u30a4\u30d6" + "\\GitHub\\claude-code\\sim-hikaku.online\\outputs"

    # Article 3: mineo
    print("=" * 60)
    print("Article 3: mineo hyoban (WP ID: 110)")
    print("=" * 60)
    with open(base + "\\mineo-hyoban.md", "r", encoding="utf-8") as f:
        md = f.read()
    html = md_to_html(md)
    html = insert_affiliate_cta(html)
    title3 = "mineo\u306e\u8a55\u5224\u30fb\u53e3\u30b3\u30df2026\u5e74\u6700\u65b0\uff5c\u30de\u30a4\u30d4\u30bf\u5897\u91cf\uff06\u30d1\u30b1\u30c3\u30c8\u653e\u984c3Mbps\u306e\u5b9f\u529b\u3092\u5fb9\u5e95\u691c\u8a3c"
    desc3 = "mineo\u306e\u8a55\u5224\u30fb\u53e3\u30b3\u30df\u30922026\u5e74\u6700\u65b0\u60c5\u5831\u3067\u5fb9\u5e95\u8abf\u67fb\u3002\u30de\u30a4\u30d4\u30bf\u5897\u91cf\u5f8c\u306e\u6599\u91d1\u3001\u30de\u30a4\u305d\u304f\u3001\u30d1\u30b1\u30c3\u30c8\u653e\u984c3Mbps\u5897\u901f\u306e\u52b9\u679c\u3001\u30e1\u30ea\u30c3\u30c89\u9078\u30fb\u30c7\u30e1\u30ea\u30c3\u30c87\u9078\u3067\u4e57\u308a\u63db\u3048\u5224\u65ad\u306e\u5b8c\u5168\u30ac\u30a4\u30c9\u3002"
    ok, res = publish_article(110, title3, desc3, html)
    print(("SUCCESS" if ok else "FAILED") + ": " + str(res))

    # Article 4: kazoku wari
    print()
    print("=" * 60)
    print("Article 4: kazoku wari (WP ID: 114)")
    print("=" * 60)
    with open(base + "\\kakuyasu-sim-kazoku-wari.md", "r", encoding="utf-8") as f:
        md = f.read()
    html = md_to_html(md)
    html = insert_affiliate_cta(html)
    title4 = "\u5bb6\u65cf\u5272\u304c\u304a\u5f97\u306a\u683c\u5b89SIM\u6bd4\u8f032026\u5e74\u6700\u65b0\uff5c\u30ef\u30a4\u30e2\u30d0\u30a4\u30eb\u30fbUQ\u30fbIIJmio\u30fbmineo\u30fb\u697d\u5929\u3092\u5fb9\u5e95\u6bd4\u8f03"
    desc4 = "\u5bb6\u65cf\u5272\u304c\u304a\u5f97\u306a\u683c\u5b89SIM\u30922026\u5e74\u6700\u65b0\u60c5\u5831\u3067\u5fb9\u5e95\u6bd4\u8f03\u3002\u30ef\u30a4\u30e2\u30d0\u30a4\u30eb\u5bb6\u65cf\u5272\u3001UQ\u30e2\u30d0\u30a4\u30eb\u81ea\u5b85\u30bb\u30c3\u30c8\u5272\u3001IIJmio\u30c7\u30fc\u30bf\u30b7\u30a7\u30a2\u3001mineo\u5bb6\u65cf\u5272\u3001\u697d\u5929\u30e2\u30d0\u30a4\u30eb\u6700\u5f37\u5bb6\u65cf\u5272\u306e\u5272\u5f15\u984d\u30fb\u6761\u4ef6\u30fb\u6ce8\u610f\u70b9\u3092\u7db2\u7f85\u3002\u5bb6\u65cf\u4eba\u6570\u5225\u30b7\u30df\u30e5\u30ec\u30fc\u30b7\u30e7\u30f3\u4ed8\u304d\u3002"
    ok, res = publish_article(114, title4, desc4, html)
    print(("SUCCESS" if ok else "FAILED") + ": " + str(res))


if __name__ == "__main__":
    main()
