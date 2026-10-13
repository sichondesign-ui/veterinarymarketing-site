"""audit2.py <dir> <port> <outdir> [pages,...] — desktop+mobile audit with scroll-through; checks errors, 404s, broken imgs,
horizontal overflow, leftover wizard links, remaining '91 reviews', nav FA link, and the Request Info modal opening."""
import sys, re, json, pathlib, subprocess, time, urllib.parse
from playwright.sync_api import sync_playwright
D, PORT, OUT = pathlib.Path(sys.argv[1]), sys.argv[2], pathlib.Path(sys.argv[3]); OUT.mkdir(parents=True, exist_ok=True)
pages = sys.argv[4].split(',') if len(sys.argv) > 4 else sorted(p.name for p in D.glob('*.html'))
srv = subprocess.Popen([sys.executable, '-m', 'http.server', PORT, '-d', str(D)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(0.8)
base = f'http://127.0.0.1:{PORT}/'
try:
  with sync_playwright() as p:
    b = p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    for name in pages:
        errs, failed = [], []
        ctx = b.new_context(viewport={'width': 1366, 'height': 900}); pg = ctx.new_page()
        pg.on('console', lambda m: errs.append(m.text[:160]) if m.type == 'error' and '%7B%7B' not in m.text and '404' not in m.text else None)
        pg.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)[:200]))
        pg.on('response', lambda r: failed.append(f'{r.status} {r.url[-60:]}') if r.status >= 400 and '%7B%7B' not in r.url else None)
        pg.goto(base + name, wait_until='load', timeout=60000); pg.wait_for_timeout(1000)
        h = pg.evaluate('document.body.scrollHeight')
        for y in range(0, h + 1, 450): pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(70)
        pg.wait_for_timeout(900)
        info = pg.evaluate('''() => {
          const links=[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href'));
          const broken=[...document.images].filter(i=>i.getAttribute('src') && i.complete && i.naturalWidth===0 && i.getBoundingClientRect().width>0).map(i=>i.getAttribute('src').slice(0,60));
          const txt=document.body.innerText;
          return {scrollW:document.documentElement.scrollWidth, clientW:document.documentElement.clientWidth, links, broken,
            wizard: links.filter(l=>l&&l.includes('wizard.veterinarymarketing.com')).length,
            wizardNewTab:[...document.querySelectorAll('a[href*="wizard.veterinarymarketing.com"]')].every(a=>a.target==='_blank'),
            reviews91: (txt.match(/91 (reviews|five-star)/g)||[]).length,
            navFA: [...document.querySelectorAll('nav a')].some(a=>/Free Competitive Analysis/.test(a.textContent)),
            h2wrapped: document.querySelectorAll('h2.vm-cta-head').length, h2: document.querySelectorAll('h2').length,
            counters: [...document.querySelectorAll('[data-count]')].filter(e=>e.getAttribute('data-count')).map(e=>e.textContent.trim()).slice(0,8),
            posts: document.querySelectorAll('.vm-blog-card').length, textLen: txt.length }
        }''')
        # modal check
        modal = None
        try:
            pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(300)
            pg.click('nav a.vm-nav-cta', timeout=3000); pg.wait_for_timeout(500)
            modal = pg.evaluate("()=>!!document.querySelector('[role=dialog][aria-label=\"Request information\"]')")
            pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
        except Exception as e: modal = 'ERR ' + str(e)[:60]
        pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(300)
        pg.screenshot(path=str(OUT / (name[:-5] + '-d.png')))
        pg.set_viewport_size({'width': 390, 'height': 844}); pg.wait_for_timeout(700)
        mob = pg.evaluate("()=>({scrollW:document.documentElement.scrollWidth, clientW:document.documentElement.clientWidth})")
        pg.screenshot(path=str(OUT / (name[:-5] + '-m.png')))
        internal = [l for l in info['links'] if l and not re.match(r'^(https?:|mailto:|tel:|#|javascript:)', l)]
        missing = sorted({l for l in internal if urllib.parse.urlparse(l).path and not (D / urllib.parse.urlparse(l).path.split('#')[0]).exists()})
        flags = []
        if info['scrollW'] > info['clientW']: flags.append('OVERFLOW-D')
        if mob['scrollW'] > mob['clientW']: flags.append(f"OVERFLOW-M({mob['scrollW']})")
        if info['wizard'] and name not in ('index.html', 'free-veterinary-marketing-analysis.html'): flags.append(f"WIZARD×{info['wizard']}")
        if info['wizard'] and not info['wizardNewTab']: flags.append('WIZARD-SAMETAB')
        if info['reviews91']: flags.append('91')
        if info['navFA']: flags.append('NAV-FA')
        if missing: flags.append('MISSING:' + ','.join(missing))
        if info['broken']: flags.append('BROKEN:' + ','.join(info['broken'][:3]))
        if errs: flags.append('ERR:' + errs[0][:80])
        if failed: flags.append('FAIL:' + failed[0])
        if modal is not True: flags.append(f'MODAL:{modal}')
        print(f"{name:58s} h2 {info['h2wrapped']}/{info['h2']} cnt={len(info['counters'])} posts={info['posts']} {' '.join(flags) or 'OK'}")
        ctx.close()
    b.close()
finally:
    srv.terminate()
