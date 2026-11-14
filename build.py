#!/usr/bin/env python3
"""앱 정책·지원 페이지 생성기. 원본은 각 앱의 Docs/ 마크다운. 실행: python3 build.py"""
import html, os, re
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
a{color:var(--accent)}ul{padding-left:1.2em}li{margin:4px 0}nav.lang{margin-bottom:16px;font-size:.9rem}nav.lang a{margin-right:12px}
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

# --- 모아콕 ---
docs = os.path.join(DEV, "MoaKok", "Docs")
pol = {"ko": ("개인정보처리방침.md", "privacy.html"), "en": ("PrivacyPolicy_en.md", "privacy-en.html"), "ja": ("PrivacyPolicy_ja.md", "privacy-ja.html")}
nav = '<nav class="lang"><a href="privacy.html">한국어</a><a href="privacy-en.html">English</a><a href="privacy-ja.html">日本語</a></nav>'
for lang, (src, dst) in pol.items():
    raw = open(os.path.join(docs, src), encoding="utf-8").read()
    if lang == "ko":  # 내부용 문구(다른 파일 경로) 제거
        raw = re.sub(r" · 영어 Docs/\S+, 일본어 Docs/\S+", "", raw)
    t, m, b = md(raw)
    write(f"moakok/{dst}", page(lang, t, f'<h1>{inline(t)}</h1><div class="meta">{inline(m)}</div><div class="card">{b}</div>', nav))

issue = f"{REPO}/issues/new?title=%5B%EB%AA%A8%EC%95%84%EC%BD%95%5D%20"
support = f"""<h1>모아콕 고객 지원 · MoaKok Support · モアコク サポート</h1>
<div class="meta">링크·대화·메모를 카테고리별로 모으는 스티커 보관함</div>
<div class="card">
<h2>문의하기</h2>
<p>궁금한 점이나 문제가 있으면 <a href="{issue}">여기에서 문의를 남겨 주세요</a> (GitHub 계정 필요). 확인 후 답변드려요. 개인정보(전화번호·대화 내용 등)는 적지 말아 주세요.</p>
<h2>자주 묻는 질문</h2>
<ul>
<li><strong>공유 목록에 모아콕이 없어요</strong>: 공유 시트의 앱 줄을 왼쪽 끝까지 밀어 '더 보기' → '편집' → 모아콕 옆 + 를 눌러 즐겨찾기에 넣어 주세요.</li>
<li><strong>구매를 복원하고 싶어요</strong>: 설정 → 구매 → 구매 복원.</li>
<li><strong>구독을 해지하고 싶어요</strong>: iPhone 설정 → Apple 계정 → 구독에서 해지할 수 있어요.</li>
<li><strong>기록이 다른 기기에도 보이나요?</strong>: 같은 Apple 계정으로 iCloud에 로그인한 기기끼리 자동으로 맞춰져요. 운영자 서버에는 저장되지 않아요.</li>
<li><strong>알림이 안 와요</strong>: '나중에 다시 보기'에서 시간을 고른 스티커만 알려 드려요. iPhone 설정 → 알림 → 모아콕이 켜져 있는지 확인해 주세요.</li>
</ul>
<p><a href="privacy.html">개인정보처리방침</a></p>
</div>
<div class="card" style="margin-top:16px">
<h2>Contact (English)</h2>
<p>For questions or problems, <a href="{issue}">please leave a message here</a> (GitHub account required). Please don't include personal information.</p>
<ul>
<li><strong>Restore purchases</strong>: Settings → Purchase → Restore Purchases.</li>
<li><strong>Cancel a subscription</strong>: iPhone Settings → Apple Account → Subscriptions.</li>
<li><strong>Sync</strong>: devices signed in to the same Apple Account with iCloud stay in sync. Nothing is stored on developer servers.</li>
</ul>
<p><a href="privacy-en.html">Privacy Policy</a></p>
<h2>お問い合わせ（日本語）</h2>
<p>ご質問や不具合は<a href="{issue}">こちらからお送りください</a>（GitHubアカウントが必要です）。個人情報は書かないでください。</p>
<ul>
<li><strong>購入の復元</strong>：設定 → 購入 → 購入を復元。</li>
<li><strong>サブスクの解約</strong>：iPhoneの設定 → Appleアカウント → サブスクリプション。</li>
<li><strong>同期</strong>：同じAppleアカウントでiCloudにログインした端末同士で自動的に同期されます。運営者のサーバーには保存されません。</li>
</ul>
<p><a href="privacy-ja.html">プライバシーポリシー</a></p>
</div>"""
write("moakok/support.html", page("ko", "모아콕 고객 지원", support))

write("index.html", page("ko", "ddunddun-house", """<h1>ddunddun-house</h1><div class="meta">iOS 앱 정책·지원 페이지</div>
<div class="card"><h2>모아콕 (MoaKok)</h2><ul>
<li><a href="moakok/support.html">고객 지원 · Support</a></li>
<li><a href="moakok/privacy.html">개인정보처리방침</a> · <a href="moakok/privacy-en.html">Privacy Policy</a> · <a href="moakok/privacy-ja.html">プライバシーポリシー</a></li></ul></div>"""))
print("built")
