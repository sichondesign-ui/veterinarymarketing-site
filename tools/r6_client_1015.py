#!/usr/bin/env python3
"""Round 6: John's edit request of 10/15/2026 ("Corporate Website Edits 10/15/2026").

- Footer: new tagline copy + Meta / Google Ads / ChatGPT Ads / Bing Ads logos (white) on every page.
- Homepage hero: same four logos (blue) under the two CTA buttons.
- 8 service pages + 8 Areas-of-Focus pages: logos (blue) under "Or call us directly".
- Request Info modal: Frank & Floyd (outside the card) replaced by the merle dog INSIDE the card, in a header band.

Run from the repo root:  python3 tools/r6_client_1015.py .
Assets were pre-converted to assets/logo-*.webp and assets/req-dog-*.webp (tools/r6_assets.json).
"""
import re, sys, json, pathlib

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
A = json.load(open(ROOT / 'tools/r6_assets.json'))

SERVICE_PAGES = ['veterinary-websites', 'veterinary-seo-marketing', 'veterinary-aeo', 'veterinary-ppc-marketing',
                 'veterinary-chatgpt-ads', 'veterinary-social-media-marketing', 'veterinary-social-media-posting',
                 'veterinary-direct-mail-marketing']
FOCUS_PAGES = ['small-animal-practice-veterinary-marketing', 'veterinary-specialty-practice-marketing',
               'emergency-vet-practice-marketing', 'urgent-care-animal-practice-veterinary-marketing',
               'startup-practice-veterinary-marketing', 'mobile-practice-veterinary-marketing-strategies',
               'multi-location-practice-veterinary-marketing-strategies', 'equine-veterinary-marketing']

def sub(name, t, old, new, label, expect=1, regex=False):
    n = len(re.findall(old, t, flags=re.S)) if regex else t.count(old)
    assert n == expect, f'{name}: {label}: expected {expect} match(es), found {n}'
    return re.sub(old, new, t, flags=re.S) if regex else t.replace(old, new)

LOGOS = [('meta', 'Meta'), ('google-ads', 'Google Ads'), ('chatgpt-ads', 'ChatGPT Ads'), ('bing-ads', 'Bing Ads')]
def logo_row(tone, indent):
    suf = '-w' if tone == 'white' else ''
    imgs = ''.join(f'<img src="{A["logo-" + k + suf]}" alt="{label}" loading="lazy">' for k, label in LOGOS)
    return f'{indent}<div class="vm-platforms vm-platforms-{tone}" aria-label="Advertising platforms we work in">{imgs}</div>\n'

NEW_TAGLINE = ("We help 100’s of veterinarians get new clients online with custom-built websites, cloud hosting, built-in SEO, "
               "analytics, custom blog with social media integration, and our web management team to handle everything for you.")

# ------------------------------------------------------------------ every page: footer copy + footer logos + modal
n = 0
for p in sorted(ROOT.glob('*.html')):
    t = p.read_text()
    if 'big results.</p>' not in t: continue
    # footer tagline + logos
    old_tag = ('        <p style="font-size: 14.5px; line-height: 1.6; color: rgba(255,255,255,0.85); margin: 0 0 22px; max-width: 290px;">'
               'Marketing for veterinary practices. Only. Small budgets, no long-term contracts, big results.</p>\n')
    new_tag = (f'        <p style="font-size: 14.5px; line-height: 1.6; color: rgba(255,255,255,0.85); margin: 0 0 18px; max-width: 320px;">{NEW_TAGLINE}</p>\n'
               + logo_row('white', '        '))
    t = sub(p.name, t, old_tag, new_tag, 'footer-tagline')

    # modal: header band with the dog inside the card; drop Frank & Floyd
    if 'aria-label="Request information"' in t:
        t = sub(p.name, t, r'        <img class="vm-req-dog vm-req-dog-l"[^\n]*\n        <img class="vm-req-dog vm-req-dog-r"[^\n]*\n', '', 'drop-frank-floyd', regex=True)
        eyebrow = ('        <div style="font-family: \'polymath-text\', sans-serif; font-size: 12.5px; font-weight: 700; letter-spacing: 0.16em; '
                   'text-transform: uppercase; color: #2F5694; margin-bottom: 10px;">Request Information</div>\n')
        h3_done = ('          <h3 style="font-family: var(--vm-display); font-weight: var(--vm-display-weight, 800); font-size: 30px; line-height: 1.1; color: #223E6B; margin: 0 0 12px;">Thanks! We have received your request.</h3>\n')
        h3_form = ('          <h3 style="font-family: var(--vm-display); font-weight: var(--vm-display-weight, 800); font-size: 28px; line-height: 1.12; color: #223E6B; margin: 0 0 18px; text-wrap: balance;">Tell us a little about your practice</h3>\n')
        band = ('        <div class="vm-req-head">\n'
                '          <div class="vm-req-head-copy">\n'
                '            <div style="font-family: \'polymath-text\', sans-serif; font-size: 12.5px; font-weight: 700; letter-spacing: 0.16em; text-transform: uppercase; color: #2F5694; margin-bottom: 10px;">Request Information</div>\n'
                '            <sc-if value="{{ reqDone }}" hint-placeholder-val="{{ false }}"><h3 style="font-family: var(--vm-display); font-weight: var(--vm-display-weight, 800); font-size: 28px; line-height: 1.12; color: #223E6B; margin: 0; text-wrap: balance;">Thanks! We have received your request.</h3></sc-if>\n'
                '            <sc-if value="{{ reqForm }}" hint-placeholder-val="{{ true }}"><h3 style="font-family: var(--vm-display); font-weight: var(--vm-display-weight, 800); font-size: 28px; line-height: 1.12; color: #223E6B; margin: 0; text-wrap: balance;">Tell us a little about your practice</h3></sc-if>\n'
                '          </div>\n'
                f'          <img class="vm-req-pup" src="{A["req-dog"]}" alt="" aria-hidden="true">\n'
                '        </div>\n')
        t = sub(p.name, t, eyebrow, band, 'modal-band')
        t = sub(p.name, t, h3_done, '', 'modal-h3-done')
        t = sub(p.name, t, h3_form, '', 'modal-h3-form')
    p.write_text(t); n += 1
print(f'{n} pages: footer copy + logos, modal band')

# ------------------------------------------------------------------ homepage hero
p = ROOT / 'index.html'; t = p.read_text()
ctas_close = ('      <a href="https://wizard.veterinarymarketing.com/your-veterinary-practice" target="_blank" rel="noopener" style="white-space: nowrap; background: #fff;')
i = t.index(ctas_close); j = t.index('    </div>\n', i) + len('    </div>\n')
t = t[:j] + logo_row('blue', '    ').replace('class="vm-platforms vm-platforms-blue"', 'class="vm-platforms vm-platforms-blue vm-platforms-hero"') + t[j:]
p.write_text(t); print('index.html: hero logos')

# ------------------------------------------------------------------ service + focus pages: under "Or call us directly"
CALL = '<a href="tel:+18448440338" style="display: inline-flex; align-items: center; gap: 10px;'
for name in SERVICE_PAGES + FOCUS_PAGES:
    p = ROOT / f'{name}.html'; t = p.read_text()
    i = t.index(CALL); j = t.index('</a>\n', i) + len('</a>\n')
    assert 'Or call us directly' in t[i:j], name
    t = t[:j] + logo_row('blue', '        ') + t[j:]
    p.write_text(t)
print('16 service/focus pages: logos under the call row')

# ------------------------------------------------------------------ CSS
css_p = ROOT / 'assets/vm-r2.css'; css = css_p.read_text()
# retire r5 Frank & Floyd rules
css = sub('css', css, r'/\* Request Info modal: Frank and Floyd flank the card.*?@media \(min-width: 1040px\) \{ \.vm-req-dog \{ display: block; \} \}\n', '', 'drop-dog-css', regex=True)
MARK = '/* ---- r6 (10/15 client edits) ---- */'
if MARK not in css:
    css += f'''
{MARK}
/* Platform logos: Meta, Google Ads, ChatGPT Ads, Bing Ads */
.vm-platforms {{ display: flex; flex-wrap: wrap; align-items: center; gap: 12px 22px; }}
.vm-platforms img {{ height: 24px; width: auto; display: block; }}
.vm-platforms-blue img {{ opacity: 0.82; }}
.vm-platforms-white img {{ height: 20px; opacity: 0.9; }}
.vm-platforms-white {{ gap: 10px 18px; max-width: 320px; margin-bottom: 22px; }}
.vm-platforms-hero {{ justify-content: center; margin-top: 26px; }}
.sp-hero-ctas .vm-platforms, .fp-hero-ctas .vm-platforms {{ margin-top: 6px; padding-top: 18px; border-top: 1px solid rgba(34,62,107,0.14); }}
@media (max-width: 960px) {{ .sp-hero-ctas .vm-platforms, .fp-hero-ctas .vm-platforms {{ justify-content: center; }} }}
@media (max-width: 560px) {{ .vm-platforms img {{ height: 20px; }} .vm-platforms {{ gap: 10px 16px; }} }}
/* Request Info modal: header band with the dog inside the card */
.vm-req-head {{ position: relative; display: flex; align-items: flex-end; min-height: 168px; margin: -36px -36px 24px; padding: 28px 196px 22px 36px; box-sizing: border-box; background: linear-gradient(180deg, #EEF3FB 0%, #E4EBF8 100%); border-radius: 26px 26px 0 0; }}
.vm-req-head-copy {{ position: relative; z-index: 1; min-width: 0; }}
.vm-req-pup {{ position: absolute; right: 34px; bottom: 0; height: calc(100% - 10px); max-height: 190px; width: auto; pointer-events: none; }}
@media (max-width: 760px) {{
  .vm-req-head {{ margin: -72px -22px 20px; padding: 72px 128px 18px 22px; border-radius: 0; min-height: 0; }}
  .vm-req-pup {{ right: 10px; height: 118px; max-height: 118px; }}
}}
'''
    css_p.write_text(css); print('vm-r2.css: r6 rules')

# cache-bust
for p in ROOT.glob('*.html'):
    t = p.read_text(); t2 = re.sub(r'vm-r2\.(css|js)\?v=[0-9a-z]+"', r'vm-r2.\1?v=10"', t)
    if t2 != t: p.write_text(t2)
print('cache-bust -> v=10'); print('done')
