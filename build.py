#!/usr/bin/env python3
"""앱 정책·지원 페이지 생성기. 원본은 각 앱의 Docs/ 마크다운. 실행: python3 build.py"""
import html, os, re, urllib.parse
ROOT = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.dirname(ROOT)
REPO = "https://github.com/ddunddun-house/ddunddun-house.github.io"

CSS = """
:root{--bg:#FFF8F0;--card:#FFFFFF;--ink:#2B2522;--muted:#7A6E66;--accent:#FF6F61;--line:#F0E4D8}
@media (prefers-color-scheme:dark){:root{--bg:#1D1A18;--card:#272320;--ink:#F3ECE6;--muted:#B5A99F;--accent:#FF8A7E;--line:#3A3430}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.7 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Hiragino Sans","Noto Sans KR",sans-serif}
main{max-width:760px;margin:0 auto;padding:32px 16px 64px}
h1{font-size:1.6rem;line-height:1.3;margin:0 0 4px}h2{font-size:1.1rem;margin:28px 0 8px}
.meta{color:var(--muted);font-size:.9rem;margin-bottom:20px}.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:20px 22px}
a{color:var(--accent);overflow-wrap:anywhere}p,li{overflow-wrap:anywhere}ul{padding-left:1.2em}li{margin:4px 0}nav.lang{margin-bottom:16px;font-size:.9rem}nav.lang a{margin-right:12px}
footer{color:var(--muted);font-size:.85rem;margin-top:28px}
"""

def inline(t):
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(https?://[^\s)（）]+)", r'<a href="\1">\1</a>', t)
    return t

def md(text):
    out, lst = [], False
    lines = text.strip().split("\n")
    title = lines[0].lstrip("# ").strip()
    meta = lines[1].strip() if len(lines) > 1 and not lines[1].startswith("#") else ""
    for line in lines[2 if meta else 1:]:
        s = line.strip()
        if s.startswith("- "):
            if not lst: out.append("<ul>"); lst = True
            out.append(f"<li>{inline(s[2:])}</li>"); continue
        if lst: out.append("</ul>"); lst = False
        if not s: continue
        if s.startswith("## "): out.append(f"<h2>{inline(s[3:])}</h2>")
        else: out.append(f"<p>{inline(s)}</p>")
    if lst: out.append("</ul>")
    return title, meta, "\n".join(out)

def page(lang, title, body, langs=""):
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><style>{CSS}</style></head>
<body><main>{langs}{body}<footer>© 2026 ddunddun-house</footer></main></body></html>
"""

def write(rel, content):
    p = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(content)

# ---------------------------------------------------------------------------
# 앱 목록. 새 앱은 여기에 한 항목만 추가한다(app-factory release 모드 10단계).
#   slug: 주소 폴더(https://ddunddun-house.github.io/<slug>/), dir: 02_devApp 안 앱 폴더
#   privacy: 언어별 원본 마크다운(앱 Docs/ 기준). 없는 언어는 빼면 그 언어 페이지를 안 만든다.
#   faq: 지원 페이지 질문(언어별 [(질문, 답)]). ko는 '자주 묻는 질문', en/ja는 짧게.
# ---------------------------------------------------------------------------
APPS = [
    {
        "slug": "moakok", "dir": "MoaKok",
        "name": {"ko": "모아콕", "en": "MoaKok", "ja": "モアコク"},
        "tagline": "링크·대화·메모를 카테고리별로 모으는 스티커 보관함",
        "privacy": {"ko": "개인정보처리방침.md", "en": "PrivacyPolicy_en.md", "ja": "PrivacyPolicy_ja.md"},
        "faq": {
            "ko": [
                ("공유 목록에 모아콕이 없어요", "공유 시트의 앱 줄을 왼쪽 끝까지 밀어 '더 보기' → '편집' → 모아콕 옆 + 를 눌러 즐겨찾기에 넣어 주세요."),
                ("구매를 복원하고 싶어요", "설정 → 구매 → 구매 복원."),
                ("구독을 해지하고 싶어요", "iPhone 설정 → Apple 계정 → 구독에서 해지할 수 있어요."),
                ("기록이 다른 기기에도 보이나요?", "같은 Apple 계정으로 iCloud에 로그인한 기기끼리 자동으로 맞춰져요. 운영자 서버에는 저장되지 않아요."),
                ("알림이 안 와요", "'나중에 다시 보기'에서 시간을 고른 스티커만 알려 드려요. iPhone 설정 → 알림 → 모아콕이 켜져 있는지 확인해 주세요."),
            ],
            "en": [
                ("Restore purchases", "Settings → Purchase → Restore Purchases."),
                ("Cancel a subscription", "iPhone Settings → Apple Account → Subscriptions."),
                ("Sync", "devices signed in to the same Apple Account with iCloud stay in sync. Nothing is stored on developer servers."),
            ],
            "ja": [
                ("購入の復元", "設定 → 購入 → 購入を復元。"),
                ("サブスクの解約", "iPhoneの設定 → Appleアカウント → サブスクリプション。"),
                ("同期", "同じAppleアカウントでiCloudにログインした端末同士で自動的に同期されます。運営者のサーバーには保存されません。"),
            ],
        },
    },
]

FILES = {"ko": "privacy.html", "en": "privacy-en.html", "ja": "privacy-ja.html"}
LABEL = {"ko": "한국어", "en": "English", "ja": "日本語"}
PTITLE = {"ko": "개인정보처리방침", "en": "Privacy Policy", "ja": "プライバシーポリシー"}
SEP = {"ko": ": ", "en": ": ", "ja": "："}


def faq_list(items):
    return "<ul>\n" + "\n".join(f"<li><strong>{inline(q)}</strong>{SEP['ja'] if any(ord(c) > 0x3000 for c in q) and not any('가' <= c <= '힣' for c in q) else ': '}{inline(a)}</li>" for q, a in items) + "\n</ul>"


def build_app(app):
    slug, docs = app["slug"], os.path.join(DEV, app["dir"], "Docs")
    langs = [l for l in ("ko", "en", "ja") if l in app["privacy"]]
    nav = '<nav class="lang">' + "".join(f'<a href="{FILES[l]}">{LABEL[l]}</a>' for l in langs) + "</nav>"
    for lang in langs:
        raw = open(os.path.join(docs, app["privacy"][lang]), encoding="utf-8").read()
        raw = re.sub(r" · 영어 Docs/\S+, 일본어 Docs/\S+", "", raw)  # 내부용 문구 제거
        t, m, b = md(raw)
        write(f"{slug}/{FILES[lang]}", page(lang, t, f'<h1>{inline(t)}</h1><div class="meta">{inline(m)}</div><div class="card">{b}</div>', nav))
    n = app["name"]
    title = urllib.parse.quote(f"[{n['ko']}] ")
    issue = f"{REPO}/issues/new?title={title}"
    heads = " · ".join(x for x in (f"{n['ko']} 고객 지원", f"{n.get('en')} Support" if "en" in langs else "", f"{n.get('ja')} サポート" if "ja" in langs else "") if x)
    body = f"""<h1>{heads}</h1>
<div class="meta">{inline(app['tagline'])}</div>
<div class="card">
<h2>문의하기</h2>
<p>궁금한 점이나 문제가 있으면 <a href="{issue}">여기에서 문의를 남겨 주세요</a> (GitHub 계정 필요). 확인 후 답변드려요. 개인정보(전화번호·대화 내용 등)는 적지 말아 주세요.</p>
<h2>자주 묻는 질문</h2>
{faq_list(app['faq'].get('ko', []))}
<p><a href="privacy.html">개인정보처리방침</a></p>
</div>"""
    extra = ""
    if "en" in langs:
        extra += f"""
<h2>Contact (English)</h2>
<p>For questions or problems, <a href="{issue}">please leave a message here</a> (GitHub account required). Please don't include personal information.</p>
{faq_list(app['faq'].get('en', []))}
<p><a href="privacy-en.html">Privacy Policy</a></p>"""
    if "ja" in langs:
        extra += f"""
<h2>お問い合わせ（日本語）</h2>
<p>ご質問や不具合は<a href="{issue}">こちらからお送りください</a>（GitHubアカウントが必要です）。個人情報は書かないでください。</p>
{faq_list(app['faq'].get('ja', []))}
<p><a href="privacy-ja.html">プライバシーポリシー</a></p>"""
    if extra:
        body += f'\n<div class="card" style="margin-top:16px">{extra}\n</div>'
    write(f"{slug}/support.html", page("ko", f"{n['ko']} 고객 지원", body))


for app in APPS:
    build_app(app)

cards = ""
for app in APPS:
    n, s = app["name"], app["slug"]
    langs = [l for l in ("ko", "en", "ja") if l in app["privacy"]]
    links = " · ".join(f'<a href="{s}/{FILES[l]}">{PTITLE[l]}</a>' for l in langs)
    cards += f"""
<div class="card"><h2>{n['ko']} ({n.get('en', '')})</h2><ul>
<li><a href="{s}/support.html">고객 지원 · Support</a></li>
<li>{links}</li></ul></div>"""
write("index.html", page("ko", "ddunddun-house", f'<h1>ddunddun-house</h1><div class="meta">iOS 앱 정책·지원 페이지</div>{cards}'))
print("built", ", ".join(a["slug"] for a in APPS))
