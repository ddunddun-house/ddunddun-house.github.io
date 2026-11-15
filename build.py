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
    {
        "slug": "phonap", "dir": "PhonAp",
        "name": {"ko": "폰압", "en": "PhonAp", "ja": "フォンアップ"},
        "tagline": "자꾸 손이 가는 앱을 정한 시간 동안 압수하는 앱 잠금",
        "privacy": {"ko": "개인정보처리방침.md", "en": "PrivacyPolicy_en.md", "ja": "PrivacyPolicy_ja.md"},
        "faq": {
            "ko": [
                ("급하게 풀어야 해요", "압수 화면의 '풀고 싶어요'를 눌러 미션을 하거나, 그 아래 '비상 해제'를 써 주세요. 비상 해제는 일주일에 한 번, 미션 없이 30분 풀리고 연속 기록은 끊겨요."),
                ("설정 앱에서 스크린타임 권한을 끄면요?", "iOS에서는 어떤 앱도 설정 앱을 막을 수 없어서 차단이 풀려요. 폰압은 이를 우회로 기록하고 연속 기록을 끊어요."),
                ("구매를 복원하고 싶어요", "설정 → 프로 → 구매 복원."),
                ("구독을 해지하고 싶어요", "iPhone 설정 → Apple 계정 → 구독, 또는 폰압 설정 → 프로 → 구독 관리에서 해지할 수 있어요."),
                ("말하기 미션 소리는 어디로 가나요?", "기기 안에서만 인식하고, 저장하거나 밖으로 보내지 않아요."),
            ],
            "en": [
                ("Emergency unlock", "tap 'I want to unlock' on the lock screen to do a mission, or use 'Emergency unlock': once a week, 30 minutes without a mission, and your streak resets."),
                ("Restore purchases", "Settings → Pro → Restore purchases."),
                ("Cancel a subscription", "iPhone Settings → Apple Account → Subscriptions."),
            ],
            "ja": [
                ("緊急解除", "没収画面の「解除したい」からミッションに進むか、「緊急解除」を使ってください。週1回、ミッションなしで30分解除され、連続記録は途切れます。"),
                ("購入の復元", "設定 → プロ → 購入を復元。"),
                ("サブスクの解約", "iPhoneの設定 → Appleアカウント → サブスクリプション。"),
            ],
        },
    },
    {
        "slug": "chaekbangul", "dir": "ChaekBangul",
        "name": {"ko": "책방울", "en": "Chaekbangul", "ja": "チェクパンウル"},
        "tagline": "좋은 문장은 형광펜으로 줍고, 읽은 책을 오래 기억하는 독서 노트",
        "privacy": {"ko": "개인정보처리방침.md", "en": "PrivacyPolicy_en.md", "ja": "PrivacyPolicy_ja.md"},
        "faq": {
            "ko": [
                ("책 검색이 안 돼요", "책 검색은 내 카카오 REST API 키를 연결해야 쓸 수 있어요. 책 추가 또는 설정 → 책 정보에서 '카카오 책 검색 연결'의 따라 하기 안내를 봐 주세요. 연결하지 않아도 직접 추가와 바코드로 책을 담을 수 있어요."),
                ("페이지 글자를 잘 못 읽어요", "페이지가 화면에 꽉 차고 밝게 찍히도록 해 주세요. 세로쓰기(일본어 세로 글)는 읽지 못할 수 있어요. 그럴 때는 직접 입력해 주세요."),
                ("구매를 복원하고 싶어요", "오늘 화면 왼쪽 위 톱니 → 설정 → 책방울 프로 → 구매 복원."),
                ("구독을 해지하고 싶어요", "iPhone 설정 → Apple 계정 → 구독, 또는 책방울 설정 → 책방울 프로 → 구독 관리에서 해지할 수 있어요."),
                ("기록이 다른 기기에도 보이나요?", "같은 Apple 계정으로 iCloud에 로그인한 기기끼리 자동으로 맞춰져요. 운영자 서버에는 저장되지 않아요."),
            ],
            "en": [
                ("Book search", "English and Japanese versions add books by typing the title. The app draws a cover, or you can use your own photo."),
                ("Restore purchases", "Today → gear icon (top left) → Settings → Chaekbangul Pro → Restore Purchases."),
                ("Cancel a subscription", "iPhone Settings → Apple Account → Subscriptions."),
                ("Sync", "devices signed in to the same Apple Account with iCloud stay in sync. Nothing is stored on developer servers."),
            ],
            "ja": [
                ("本の追加", "英語版・日本語版はタイトルを入力して追加します。表紙はアプリが描くか、自分の写真を使えます。縦書きのページは読み取れないことがあります。"),
                ("購入の復元", "今日の画面の左上の歯車 → 設定 → チェクパンウル プロ → 購入を復元。"),
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
