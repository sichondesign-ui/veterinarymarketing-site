#!/usr/bin/env python3
"""Launch prep that needs no client decisions: favicon set, OG/Twitter meta, canonical (final domain), lang, theme-color,
robots.txt, sitemap.xml, branded 404. Adds noindex while the preview is public (remove at launch)."""
import re, sys, json, pathlib, subprocess, time
ROOT = pathlib.Path(sys.argv[1]); ICON_SVG = pathlib.Path(sys.argv[2]); LOGO_SVG = pathlib.Path(sys.argv[3])
DOMAIN = 'https://www.veterinarymarketing.com'
PREVIEW = 'https://sichondesign-ui.github.io/veterinarymarketing-site'

# final URL map from the README table
readme = (ROOT / 'README.md').read_text()
URLS = {}
for line in readme.splitlines():
    m = re.match(r'\| [^|]+ \| `([^`]+\.html)` \| `([^`]+)` \|', line)
    if m: URLS[m.group(1)] = m.group(2)
URLS.setdefault('blog.html', '/blog'); URLS.setdefault('privacy-policy.html', '/privacy-policy')

# ---------- icons + OG image (rendered with headless Chromium) ----------
from playwright.sync_api import sync_playwright
from PIL import Image
work = pathlib.Path('/tmp/iconsrv'); work.mkdir(exist_ok=True)
(work / 'icon.svg').write_bytes(ICON_SVG.read_bytes()); (work / 'logo.svg').write_bytes(LOGO_SVG.read_bytes())
(work / 'icon.html').write_text('<html><body style="margin:0;background:transparent"><div style="width:512px;height:512px;display:flex;align-items:center;justify-content:center"><img src="icon.svg" style="height:440px"></div></body></html>')
(work / 'tile.html').write_text('<html><body style="margin:0"><div style="width:512px;height:512px;background:#2F5694;border-radius:112px;display:flex;align-items:center;justify-content:center"><img src="icon.svg" style="height:360px;filter:brightness(0) invert(1)"></div></body></html>')
(work / 'og.html').write_text('''<html><head><meta charset="utf-8"></head><body style="margin:0"><div style="width:1200px;height:630px;background:#2F5694;position:relative;font-family:-apple-system,Helvetica,Arial,sans-serif;overflow:hidden">
<div style="position:absolute;right:-120px;top:-90px;width:560px;height:560px;border-radius:50%;background:rgba(116,155,234,0.25)"></div>
<div style="position:absolute;left:80px;top:84px;background:#fff;border-radius:28px;padding:28px 36px;display:inline-flex"><img src="logo.svg" style="height:84px"></div>
<div style="position:absolute;left:80px;top:268px;color:#fff;font-size:64px;font-weight:800;line-height:1.05;letter-spacing:-0.02em;max-width:900px">More of the clients<br>your practice wants.</div>
<div style="position:absolute;left:80px;top:440px;color:rgba(255,255,255,0.85);font-size:28px;line-height:1.3;max-width:900px">Websites, SEO, AEO and ads built exclusively for veterinary practices.</div>
<div style="position:absolute;left:80px;bottom:56px;display:flex;align-items:center;gap:14px;color:#fff;font-size:22px;font-weight:700"><span style="background:#F3B23E;color:#223E6B;border-radius:999px;padding:8px 18px">5.0 ★★★★★ on Google</span><span style="opacity:0.8">200+ veterinary practices served</span></div>
</div></body></html>''')
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8860', '-d', str(work)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(0.8)
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 512, 'height': 512}); pg.goto('http://127.0.0.1:8860/icon.html'); pg.wait_for_timeout(600); pg.screenshot(path=str(work / 'icon512.png'), omit_background=True)
        pg.goto('http://127.0.0.1:8860/tile.html'); pg.wait_for_timeout(600); pg.screenshot(path=str(work / 'tile512.png'), omit_background=True)
        pg = b.new_page(viewport={'width': 1200, 'height': 630}); pg.goto('http://127.0.0.1:8860/og.html'); pg.wait_for_timeout(800); pg.screenshot(path=str(work / 'og.png'))
        b.close()
finally: srv.terminate()
A = ROOT / 'assets'
icon = Image.open(work / 'icon512.png').convert('RGBA'); tile = Image.open(work / 'tile512.png').convert('RGBA')
icon.resize((32, 32), Image.LANCZOS).save(A / 'favicon-32.png'); icon.resize((16, 16), Image.LANCZOS).save(A / 'favicon-16.png')
icon.save(ROOT / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
tile.resize((180, 180), Image.LANCZOS).convert('RGB').save(A / 'apple-touch-icon.png')
tile.resize((192, 192), Image.LANCZOS).save(A / 'icon-192.png'); tile.save(A / 'icon-512.png')
(ROOT / 'favicon.svg').write_bytes(ICON_SVG.read_bytes())
Image.open(work / 'og.png').convert('RGB').save(A / 'og-default.jpg', 'JPEG', quality=86, optimize=True)
(ROOT / 'site.webmanifest').write_text(json.dumps({"name": "VeterinaryMarketing.com", "short_name": "VetMarketing", "icons": [{"src": "assets/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "assets/icon-512.png", "sizes": "512x512", "type": "image/png"}], "theme_color": "#2F5694", "background_color": "#ffffff", "display": "browser"}, indent=1))
print('icons + og image written')

# ---------- per-page head tags ----------
HEAD_MARK = '<!-- vm:head -->'
for p in sorted(ROOT.glob('*.html')):
    t = p.read_text()
    if HEAD_MARK in t: t = re.sub(r'<!-- vm:head -->.*?<!-- /vm:head -->\n', '', t, flags=re.S)
    title = re.search(r'<title>(.*?)</title>', t, re.S).group(1).strip()
    desc = re.search(r'<meta name="description" content="([^"]*)">', t).group(1)
    path = URLS.get(p.name, '/' + p.name[:-5])
    canonical = DOMAIN + path
    is404 = p.name == '404.html'
    tags = f'''{HEAD_MARK}
<html lang="en">
<meta name="robots" content="noindex, nofollow"><!-- PREVIEW ONLY: remove at launch -->
<link rel="canonical" href="{canonical}">
<link rel="icon" href="favicon.ico" sizes="32x32">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<meta name="theme-color" content="#2F5694">
<meta property="og:type" content="website">
<meta property="og:site_name" content="VeterinaryMarketing.com">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{DOMAIN}/assets/og-default.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{DOMAIN}/assets/og-default.jpg">
<!-- /vm:head -->
'''
    # the static head is the bundle's; put tags right after <meta charset> so crawlers see them without JS
    t = re.sub(r'(<meta charset="utf-8">\n)', r'\1' + tags.replace('\\', '\\\\'), t, count=1)
    t = t.replace('<html>\n<head>', '<html lang="en">\n<head>', 1)
    t = t.replace('<html lang="en">\n<meta name="robots"', '<meta name="robots"', 1)  # (the lang line inside tags was a placeholder)
    p.write_text(t)
print('head tags on', len(list(ROOT.glob('*.html'))), 'pages')

# ---------- robots + sitemap ----------
(ROOT / 'robots.txt').write_text(f'''# PREVIEW: blocked until launch. At launch replace with:
#   User-agent: *
#   Allow: /
#   Sitemap: {DOMAIN}/sitemap.xml
User-agent: *
Disallow: /
''')
today = time.strftime('%Y-%m-%d')
urls = ''.join(f'  <url><loc>{DOMAIN}{path}</loc><lastmod>{today}</lastmod></url>\n' for f, path in URLS.items() if (ROOT / f).exists())
(ROOT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
print('robots.txt + sitemap.xml written (', len(URLS), 'urls )')
