#!/usr/bin/env python3
"""On-page SEO audit for the build. Run after every content change:
    python3 tools/seo_audit.py .            # static checks only
    python3 tools/seo_audit.py . --render   # also render
    python3 tools/seo_audit.py . --render --pages=index.html,about.html   # subset each page (headless Chromium) for H1/H2/word count/alt coverage

Checks, per page: title + meta description present and within length; one H1; target keyword (from tools/seo_targets.json)
in title, H1, meta description and first 150 words; canonical present; OG tags present; images without alt;
internal links in/out; orphan pages. Writes tools/seo_report.md and prints a summary. Exit code 1 if any page has an error."""
import sys, re, json, pathlib, subprocess, time, html

ROOT = pathlib.Path(sys.argv[1]).resolve(); RENDER = '--render' in sys.argv
TARGETS = json.load(open(ROOT / 'tools' / 'seo_targets.json'))
pages = sorted(p for p in ROOT.glob('*.html') if p.name != '404.html')
only = [a.split('=',1)[1] for a in sys.argv if a.startswith('--pages=')]
if only: pages = [p for p in pages if p.name in only[0].split(',')]
SKIP_INLINKS = {'privacy-policy.html', 'blog.html', 'free-veterinary-marketing-analysis.html'}  # footer-only / utility pages

def strip(s): return html.unescape(re.sub(r'<[^>]+>', ' ', s or '')).strip()
def norm(s): return re.sub(r'[^a-z0-9 ]+', ' ', (s or '').lower())

static = {}
for p in pages:
    t = p.read_text()
    title = strip((re.search(r'<title>(.*?)</title>', t, re.S) or [None, ''])[1])
    desc = (re.search(r'<meta name="description" content="([^"]*)">', t) or [None, ''])[1]
    canonical = (re.search(r'<link rel="canonical" href="([^"]*)">', t) or [None, ''])[1]
    og = len(re.findall(r'property="og:', t))
    noindex = 'noindex' in t
    links = [l.split('#')[0] for l in re.findall(r'href="([^"#]+\.html)(?:#[^"]*)?"', t)]
    static[p.name] = dict(title=title, desc=desc, canonical=canonical, og=og, noindex=noindex, out=set(links) - {p.name})

rendered = {}
if RENDER:
    from playwright.sync_api import sync_playwright
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8877', '-d', str(ROOT)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(0.8)
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch()
            for p in pages:
                pg = b.new_page(viewport={'width': 1366, 'height': 900})
                pg.goto(f'http://127.0.0.1:8877/{p.name}', wait_until='load', timeout=60000); pg.wait_for_timeout(500)
                for y in range(0, pg.evaluate('document.body.scrollHeight') + 1, 900): pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(25)
                pg.wait_for_timeout(250)
                rendered[p.name] = pg.evaluate('''() => {
                  const main = document.body.innerText;
                  const h1 = [...document.querySelectorAll('h1')].map(h => h.innerText.trim());
                  const h2 = [...document.querySelectorAll('h2')].map(h => h.innerText.trim());
                  const imgs = [...document.images].filter(i => i.getBoundingClientRect().width > 0);
                  const noalt = imgs.filter(i => !i.hasAttribute('alt')).length;
                  const emptyalt = imgs.filter(i => i.getAttribute('alt') === '').length;
                  const first = main.split(/\\s+/).slice(0, 150).join(' ');
                  const links = [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')).filter(h => h && /\\.html/.test(h) && !/^https?:/.test(h)).map(h => h.split('#')[0]);
                  return { h1, h2, words: main.split(/\\s+/).length, imgs: imgs.length, noalt, emptyalt, first150: first, out: [...new Set(links)] };
                }''')
                pg.close()
            b.close()
    finally: srv.terminate()

# inbound links (rendered if available, else static)
inbound = {p.name: set() for p in pages}
for src, s in static.items():
    outs = set(rendered.get(src, {}).get('out', [])) or s['out']
    for dst in outs:
        if dst in inbound and dst != src: inbound[dst].add(src)

rows, errors, warns = [], 0, 0
for p in pages:
    s = static[p.name]; r = rendered.get(p.name, {}); kw = TARGETS.get(p.name, {}); issues = []
    target = kw.get('keyword', ''); variants = [target] + kw.get('variants', []) if target else []
    def has(text): return any(norm(v) in norm(text) for v in variants if v)
    if not s['title']: issues.append('ERR no <title>')
    elif len(s['title']) > 65: issues.append(f'WARN title {len(s["title"])} chars (>65 may truncate)')
    if not s['desc']: issues.append('ERR no meta description')
    elif not (120 <= len(s['desc']) <= 165): issues.append(f'WARN description {len(s["desc"])} chars (aim 120–160)')
    if not s['canonical']: issues.append('ERR no canonical')
    if s['og'] < 4: issues.append('WARN OG tags missing')
    if target:
        if not has(s['title']): issues.append(f'ERR keyword not in title')
        if not has(s['desc']): issues.append('WARN keyword not in description')
        if r:
            if not r['h1']: issues.append('ERR no H1')
            elif len(r['h1']) > 1: issues.append(f'ERR {len(r["h1"])} H1s')
            elif not has(r['h1'][0]): issues.append('ERR keyword not in H1')
            if not has(r['first150']): issues.append('WARN keyword not in first 150 words')
    elif p.name not in ('privacy-policy.html', 'blog.html', 'contact-us.html', 'reviews.html', 'about.html', 'index.html', 'free-veterinary-marketing-analysis.html', 'conferences.html'):
        issues.append('WARN no target keyword set in seo_targets.json')
    if r:
        if r['noalt']: issues.append(f'ERR {r["noalt"]} img without alt attribute')
        if r['words'] < 300: issues.append(f'WARN thin page ({r["words"]} words)')
    if p.name not in SKIP_INLINKS and p.name != 'index.html' and len(inbound[p.name]) < 2: issues.append(f'WARN only {len(inbound[p.name])} inbound link(s)')
    errors += sum(1 for i in issues if i.startswith('ERR')); warns += sum(1 for i in issues if i.startswith('WARN'))
    rows.append((p.name, target, s['title'], len(s['title']), len(s['desc']), (r.get('h1') or ['—'])[0][:70], r.get('words', ''), len(inbound[p.name]), issues))

out = ['# SEO audit', f'Generated {time.strftime("%Y-%m-%d %H:%M")} · {len(pages)} pages · {errors} errors · {warns} warnings' + (' · rendered' if RENDER else ' · static only (add --render for H1/word counts)'), '',
       '| Page | Target keyword | Title (len) | Desc len | H1 | Words | In-links | Issues |', '|---|---|---|---|---|---|---|---|']
for name, target, title, tl, dl, h1, words, inl, issues in rows:
    out.append(f'| {name} | {target or "—"} | {title[:60]} ({tl}) | {dl} | {h1} | {words} | {inl} | {"<br>".join(issues) or "OK"} |')
if static.get('index.html', {}).get('noindex'): out += ['', '> Pages currently carry `noindex` (preview guard). Remove before launch.']
(ROOT / 'tools' / 'seo_report.md').write_text('\n'.join(out) + '\n')
for name, *_rest in rows:
    issues = _rest[-1]; print(f'{name:58s} {"OK" if not issues else " | ".join(issues)}')
print(f'\n{errors} errors, {warns} warnings → tools/seo_report.md')
sys.exit(1 if errors else 0)
