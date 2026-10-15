#!/usr/bin/env python3
"""Round 5: John's edit request of 10/14/2026 (Google Doc "Corporate Website Edit Request").

Run from the repo root:  python3 tools/r5_client_1014.py .

New graphics were pre-converted to assets/*-1014-*.webp (trimmed of transparent padding, 2000px wide, q88).
Every substitution asserts its expected hit count so a drifted template fails loudly instead of silently.
"""
import re, sys, json, pathlib, glob

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
NEW = {k: pathlib.Path(v).name for k, v in {
    'aeo-logos':       glob.glob(str(ROOT / 'assets/aeo-logos-1014-*.webp'))[0],
    'aeo-devices':     glob.glob(str(ROOT / 'assets/aeo-devices-1014-*.webp'))[0],
    'chatgpt-card':    glob.glob(str(ROOT / 'assets/chatgpt-card-1014-*.webp'))[0],
    'posting-devices': glob.glob(str(ROOT / 'assets/posting-devices-1014-*.webp'))[0],
    'posting-results': glob.glob(str(ROOT / 'assets/posting-results-1014-*.webp'))[0],
}.items()}
A = lambda k: 'assets/' + NEW[k]

SERVICE_PAGES = ['veterinary-websites', 'veterinary-seo-marketing', 'veterinary-aeo', 'veterinary-ppc-marketing',
                 'veterinary-chatgpt-ads', 'veterinary-social-media-marketing', 'veterinary-social-media-posting',
                 'veterinary-direct-mail-marketing']
FOCUS_PAGES = ['small-animal-practice-veterinary-marketing', 'veterinary-specialty-practice-marketing',
               'emergency-vet-practice-marketing', 'urgent-care-animal-practice-veterinary-marketing',
               'startup-practice-veterinary-marketing', 'mobile-practice-veterinary-marketing-strategies',
               'multi-location-practice-veterinary-marketing-strategies', 'equine-veterinary-marketing']

def sub(name, t, old, new, label, expect=1, regex=False):
    n = len(re.findall(old, t)) if regex else t.count(old)
    assert n == expect, f'{name}: {label}: expected {expect} match(es), found {n}'
    return re.sub(old, new, t) if regex else t.replace(old, new)

def page(name):
    p = ROOT / f'{name}.html'; return p, p.read_text()

# ---------------------------------------------------------------- 1. Homepage service cards (AEO, ChatGPT Ads, Social Media Posting)
p, t = page('index')
t = sub('index', t, "img: asset('assets/placeholder-aeo.png')", f"img: '{A('aeo-logos')}'", 'card-aeo')
t = sub('index', t, "img: asset('assets/placeholder-chatgpt-ads.png')", f"img: '{A('chatgpt-card')}'", 'card-chatgpt')
t = sub('index', t, "img: asset('assets/placeholder-social-posting.png')", f"img: '{A('posting-devices')}'", 'card-posting')
# "enlarge these graphics a little": taller art box, and let it use the card's horizontal padding
t = sub('index', t, '<div style="height: 220px; margin-bottom: 24px;">\n          <div role="img" aria-label="{{ svc.name }} example"',
        '<div class="vm-svc-art" style="height: 272px; margin: 0 -16px 22px;">\n          <div role="img" aria-label="{{ svc.name }} example"', 'card-art-box')
p.write_text(t); print('index.html: 3 cards swapped, art box 220 -> 272px')

# ---------------------------------------------------------------- 2. Service pages
HERO = {'veterinary-aeo': ('aeo-devices', 'Your practice recommended inside an AI Overview on desktop and phone'),
        'veterinary-chatgpt-ads': ('chatgpt-card', 'A sponsored ChatGPT Ads placement for a veterinary practice'),
        'veterinary-social-media-posting': ('posting-results', 'Monthly social media posting results for a veterinary practice')}
for name in SERVICE_PAGES:
    p, t = page(name)
    # hero graphic + alt
    if name in HERO:
        key, alt = HERO[name]
        t = sub(name, t, r'"heroImg":"assets/placeholder-[a-z-]+\.png","heroAlt":"[^"]*"',
                f'"heroImg":"{A(key)}","heroAlt":"{alt}"', 'hero-img', regex=True)
    # hero media column gets a hook class; sizing lives in vm-r2.css (desktop only)
    t = sub(name, t, '    <div class="vm-reveal" style="position: relative;">\n      <div style="position: relative; padding-top: 80%;">',
            '    <div class="vm-reveal sp-hero-media" style="position: relative;">\n      <div style="position: relative; padding-top: 80%;">', 'hero-media-hook')
    # response-time stat: count DOWN 24 -> 2 (was counting up 0 -> 2 on these pages)
    t = sub(name, t, "{ value: '2 hrs', label: 'response time when you reach out' }",
            "{ value: '< 2 hrs', from: '24', label: 'response time when you reach out' }", 'stat-2hrs')
    t = sub(name, t, 'class="sp-count" data-count="{{ st.value }}"', 'class="sp-count" data-count="{{ st.value }}" data-from="{{ st.from }}"', 'stat-from')
    # zig-zag media: new trimmed artwork where the same graphic was used; drop blocks that would duplicate the new hero
    m = re.search(r'    const R2_MEDIA = (\{.*?\});\n', t);
    if m:
        media = json.loads(m.group(1))
        if name == 'veterinary-aeo':
            media['0']['src'] = A('aeo-logos'); media.pop('3')          # devices now in the hero
        if name == 'veterinary-social-media-posting':
            media['0']['src'] = A('posting-devices'); media.pop('2')    # monthly results now in the hero
            t = sub(name, t, '["< 2 hrs","Response time","', '["< 2 hrs","Response time","', 'posting-reason-marker')
            t = sub(name, t, r'(\["< 2 hrs","Response time","[^"]*",)"48"\]', r'\1"24"]', 'posting-reason-24', regex=True)
        t = t[:m.start(1)] + json.dumps(media) + t[m.end(1):]
    p.write_text(t); print(f'{name}.html: hero={"swapped" if name in HERO else "kept"}, stat 24->2, media hook')

# ---------------------------------------------------------------- 3. Focus pages: 48 -> 24
for name in FOCUS_PAGES:
    p, t = page(name)
    t = sub(name, t, "{ value: '< 2 hrs', from: '48',", "{ value: '< 2 hrs', from: '24',", 'focus-24', expect=2)
    p.write_text(t)
print('8 focus pages: response-time counters 48 -> 24')

# ---------------------------------------------------------------- 4. Blog: no category chips, no card labels, no featured post
p, t = page('blog')
t = sub('blog', t, r'    <div class="vm-blog-tags" style="display: flex; flex-wrap: wrap; gap: 8px;">\n.*?\n    </div>\n', '', 'blog-chips', regex=True)
t = sub('blog', t, '          <div class="vm-blog-tag">{{ po.tag }}</div>\n', '', 'blog-card-tag')
t = sub('blog', t, "cls: 'vm-blog-card vm-reveal' + (i === 0 ? ' vm-blog-featured' : '')", "cls: 'vm-blog-card vm-reveal'", 'blog-featured')
p.write_text(t); print('blog.html: chips, card labels and featured post removed')

# ---------------------------------------------------------------- 5. Request Info modal, every page that has it
DOGS = ('        <img class="vm-req-dog vm-req-dog-l" src="assets/dog-frank-e21c1a9aab.png" alt="" aria-hidden="true">\n'
        '        <img class="vm-req-dog vm-req-dog-r" src="assets/dog-floyd-9224c77315.webp" alt="" aria-hidden="true">\n')
n_pages = 0
for p in sorted(ROOT.glob('*.html')):
    t = p.read_text()
    if 'aria-label="Request information"' not in t: continue
    # step 2: type="url" rejected "mypractice.com" (no scheme) and silently blocked Next, so step 3 was unreachable
    t = sub(p.name, t, 'name="practice_website" type="url" style=', 'name="practice_website" type="text" inputmode="url" autocomplete="url" placeholder="yourpractice.com" style=', 'url-field')
    # Frank and Floyd flank the card (desktop only; see vm-r2.css)
    anchor = '        <button sc-camel-on-click="{{ closeReq }}" aria-label="Close"'
    if 'vm-req-dog' not in t:
        t = sub(p.name, t, anchor, DOGS + anchor, 'modal-dogs')
    p.write_text(t); n_pages += 1
print(f'{n_pages} pages: modal URL field fixed, Frank & Floyd added')

# ---------------------------------------------------------------- 6. Shared CSS
css_p = ROOT / 'assets/vm-r2.css'; css = css_p.read_text()
MARK = '/* ---- r5 (10/14 client edits) ---- */'
if MARK not in css:
    css += f'''
{MARK}
/* Conferences collage: wide bottom tile cropped heads off at desktop width; anchor the crop near the top */
.vm-collage > div:nth-child(4) img {{ object-position: center 18%; }}
/* Service hero: larger media column on desktop so the graphics are legible */
@media (min-width: 961px) {{
  .sp-hero:has(.sp-hero-media) {{ grid-template-columns: minmax(0, 0.95fr) minmax(0, 1.15fr) !important; gap: 40px !important; }}
  .sp-hero-media {{ margin: 0 -48px 0 -8px; }}
}}
/* Request Info modal: Frank and Floyd flank the card (hidden on narrow screens; the modal is a full sheet there) */
.vm-req-dog {{ display: none; position: absolute; bottom: -2px; width: 200px; height: auto; pointer-events: none; }}
.vm-req-dog-l {{ right: 100%; margin-right: 22px; }}
.vm-req-dog-r {{ left: 100%; margin-left: 22px; }}
@media (min-width: 1040px) {{ .vm-req-dog {{ display: block; }} }}
/* Homepage service cards: art box margin collapses back on phones */
@media (max-width: 560px) {{ .vm-svc-art {{ height: 200px !important; margin: 0 0 18px !important; }} }}
'''
    css_p.write_text(css); print('vm-r2.css: r5 rules appended')
print('done')
