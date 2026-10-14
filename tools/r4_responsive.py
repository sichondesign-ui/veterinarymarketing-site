#!/usr/bin/env python3
"""Responsive audit round (10/14): 11 items. Idempotent per file via markers; run after `git checkout` for a clean apply."""
import re, sys, pathlib
ROOT = pathlib.Path(sys.argv[1]); PAGES = sorted(ROOT.glob('*.html'))
PHONE_SVG = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"></path></svg>'
ABOUT_LINKS = "[{ label: 'About Us', href: 'about.html' }, { label: 'Reviews', href: 'reviews.html' }, { label: 'Conferences', href: 'conferences.html' }, { label: 'Our Blog', href: 'blog.html' }]"
log = {}
def note(p, k): log.setdefault(p.name, []).append(k)
def must(t, old, new, p, k, count=1):
    n = t.count(old); assert n == count, (p.name, k, n); note(p, k); return t.replace(old, new)

for p in PAGES:
    t = p.read_text(); o = t
    # ---- (6) + (11) mobile menu: About sub-panel, tap-to-call row ----
    if "{ label: 'About', href: 'about.html' }, { label: 'Services', sub: 'services' }" in t:
        t = must(t, "{ label: 'About', href: 'about.html' }, { label: 'Services', sub: 'services' }, { label: 'Areas of Focus', sub: 'focus' }, { label: 'Reviews', href: 'reviews.html' },",
                 "{ label: 'About', sub: 'about' }, { label: 'Services', sub: 'services' }, { label: 'Areas of Focus', sub: 'focus' },", p, 'menu-about-sub')
        t = re.sub(r"const on = isHere\(l\.href\) \|\| \(l\.sub === 'services'", "const on = isHere(l.href) || (l.sub === 'about' && " + ABOUT_LINKS + ".some(a => isHere(a.href))) || (l.sub === 'services'", t, count=1); note(p, 'menu-about-on')
        t = must(t, "mobileSubTitle: this.state.mobileSub === 'focus' ? 'Areas of Focus' : 'Services',", "mobileSubTitle: this.state.mobileSub === 'about' ? 'About' : this.state.mobileSub === 'focus' ? 'Areas of Focus' : 'Services',", p, 'menu-sub-title')
        t = re.sub(r"mobileSubLinks: this\.state\.mobileSub === 'focus' \?", "mobileSubLinks: this.state.mobileSub === 'about' ? " + ABOUT_LINKS + " : this.state.mobileSub === 'focus' ?", t, count=1); note(p, 'menu-sub-links')
        m = re.search(r'(</sc-for>\n\s*<a href="#request-info" sc-camel-on-click="\{\{ openReq \}\}" style="[^"]*">Request Info</a>)', t); assert m, p.name
        call = ('\n        <a href="tel:+18448440338" class="vm-mob-call" style="display: flex; align-items: center; justify-content: center; gap: 9px; margin-top: 12px; padding: 12px 14px; border-radius: 12px; border: 1.5px solid rgba(34,62,107,0.18); color: #223E6B; font-family: \'polymath-text\', sans-serif; font-size: 15px; font-weight: 800; text-decoration: none;">'
                '<span style="width: 32px; height: 32px; border-radius: 50%; background: #F3B23E; border: 2px solid #223E6B; display: inline-flex; align-items: center; justify-content: center; color: #223E6B;">' + PHONE_SVG + '</span>Call (844) 844-0338</a>')
        t = t[:m.end()] + call + t[m.end():]; note(p, 'menu-call')
    # ---- (10) modal → full-screen sheet on mobile; (7) stats hairline; (8) focus grid 2-up; CSS hooks for all ----
    if 'vm-r4-css' not in t:
        css = '''  <style data-vm-r4-css>
    @media (max-width: 760px) {
      /* (10) Request Info becomes a full-screen sheet */
      [role="dialog"][aria-label="Request information"] { padding: 0 !important; align-items: stretch !important; background: #fff !important; }
      [role="dialog"][aria-label="Request information"] > div { width: 100% !important; min-height: 100dvh; border-radius: 0 !important; border: 0 !important; box-shadow: none !important; padding: 72px 22px 40px !important; }
      [role="dialog"][aria-label="Request information"] > div > button[aria-label="Close"] { position: fixed !important; top: 14px !important; right: 14px !important; z-index: 2; }
      /* (7) stats strip reads as four quadrants */
      .fp-stats > div:nth-child(n+3), .sp-stats > div:nth-child(n+3) { border-top: 1px solid #D9E2F0; }
      .fp-stats > div:nth-child(2n), .sp-stats > div:nth-child(2n) { border-right: 0 !important; }
    }
    @media (max-width: 560px) {
      /* (8) practice-type cards stay 2-up, stacked, equal height */
      .vm-focus8 { grid-template-columns: 1fr 1fr !important; gap: 10px !important; }
      .vm-focus8 > a { grid-template-columns: 1fr !important; gap: 10px !important; text-align: center; align-content: start; padding: 16px 12px 14px !important; }
      .vm-focus8 > a > div:first-child { margin: 0 auto; }
      .vm-focus8 h3 { font-size: 15px !important; }
    }
  </style>
'''
        t = must(t, '  <link rel="stylesheet" href="assets/vm-r2.css">', css + '  <link rel="stylesheet" href="assets/vm-r2.css">', p, 'r4-css')
    # ---- (1)(2) homepage #reviews side padding; (5) hero CTAs side by side; (4) clip the trust-band paw ----
    if p.name == 'index.html':
        t = must(t, '#reviews { padding: 72px 0 !important; }', '#reviews { padding: 72px 20px !important; }', p, 'reviews-pad')
        t = must(t, '.vm-hero-ctas { flex-direction: column !important; align-items: stretch !important; max-width: 320px; margin: 0 auto !important; }\n      .vm-hero-ctas > a { text-align: center; }',
                 '.vm-hero-ctas { gap: 10px !important; justify-content: center; padding: 0 4px; }\n      .vm-hero-ctas > a { flex: 1 1 0; text-align: center; padding: 13px 8px !important; font-size: 14px !important; }\n      .vm-lbl-full { display: none; } .vm-lbl-short { display: inline; }', p, 'hero-ctas')
        t = must(t, '<!-- /vm:head -->', '<!-- /vm:head -->\n<style>.vm-lbl-short { display: none; }</style>', p, 'lbl-css')
        t = re.sub(r'(target="_blank" rel="noopener"[^>]*>)Free Competitive Analysis(</a>)', r'\1<span class="vm-lbl-full">Free Competitive Analysis</span><span class="vm-lbl-short">Free Analysis</span>\2', t, count=1); note(p, 'hero-lbl')
        t = must(t, '#about { grid-template-columns: 1fr !important; }', '#about { grid-template-columns: 1fr !important; overflow: hidden; }', p, 'about-clip')
    # ---- (3) About hero photo smaller on mobile ----
    if p.name == 'about.html':
        t = must(t, '.sp-hero { grid-template-columns: 1fr !important; gap: 40px !important; padding-top: 128px !important; }',
                 '.sp-hero { grid-template-columns: 1fr !important; gap: 40px !important; padding-top: 128px !important; }\n      #top .sp-hero > div.vm-reveal { width: 76%; max-width: 340px; margin: 0 auto; }', p, 'about-hero')
    # ---- (9) Reviews hero: blob photo + floating rating card ----
    if p.name == 'reviews.html':
        a = t.find('    <div class="vm-reveal" style="position: relative; display: flex; justify-content: center;'); b = t.find('  </div>\n</section>', a)
        assert a > 0 and b > a, 'reviews hero visual'
        old_card = t[a:b]
        href = re.search(r'<a href="(https://www\.google\.com/search[^"]*)"', old_card).group(1)
        new = f'''    <div class="vm-reveal rv-hero-visual" style="position: relative; width: min(100%, 440px); margin: 0 auto; aspect-ratio: 1;">
      <div aria-hidden="true" style="position: absolute; right: -8%; top: -10%; width: 42%; height: 40%; background: #749BEA; opacity: 0.25; -webkit-mask: url(&quot;assets/paw-fill-1e3d9826c2.svg&quot;) center / contain no-repeat; mask: url(&quot;assets/paw-fill-1e3d9826c2.svg&quot;) center / contain no-repeat; transform: rotate(22deg);"></div>
      <img src="assets/gallery-4-1dee894dee.webp" alt="A VeterinaryMarketing.com team member smiling at her laptop" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: center 30%; display: block; background: #D9E2F0; border-radius: 58% 42% 46% 54% / 48% 56% 44% 52%; filter: drop-shadow(0 30px 40px rgba(34,62,107,0.22));">
      <a href="{href}" target="_blank" rel="noopener" style="position: absolute; left: -6%; bottom: 6%; display: flex; flex-direction: column; align-items: flex-start; gap: 4px; background: #fff; border: 2px solid #223E6B; box-shadow: 0 6px 0 #223E6B; border-radius: 22px; padding: 18px 22px 16px; color: #223E6B; text-decoration: none; transition: transform 0.2s;" style-hover="transform: translateY(-3px);">
        <div style="display: flex; align-items: center; gap: 8px;"><svg width="22" height="22" viewBox="0 0 48 48" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.1H42V20H24v8h11.3C33.7 32.7 29.3 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.9 1.2 8 3l5.7-5.7C34.3 6.1 29.4 4 24 4 13 4 4 13 4 24s9 20 20 20 20-9 20-20c0-1.3-.1-2.7-.4-3.9z"></path><path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 18.9 12 24 12c3.1 0 5.9 1.2 8 3l5.7-5.7C34.3 6.1 29.4 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"></path><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.3 0-9.7-3.4-11.3-8.1l-6.5 5C9.5 39.6 16.2 44 24 44z"></path><path fill="#1976D2" d="M43.6 20.1H42V20H24v8h11.3c-.8 2.2-2.2 4.1-4.1 5.5l6.2 5.2C36.9 39.2 44 34 44 24c0-1.3-.1-2.7-.4-3.9z"></path></svg><span style="font-family: var(--vm-display); font-weight: var(--vm-display-weight, 800); font-size: 40px; line-height: 1;">5.0</span></div>
        <div aria-label="Five out of five stars" style="font-size: 22px; letter-spacing: 3px; color: #F3B23E; line-height: 1;">★★★★★</div>
        <div style="font-family: 'polymath-text', sans-serif; font-size: 13px; color: #2F5694; font-weight: 700; margin-top: 4px;">Read them on Google ↗</div>
      </a>
    </div>
'''
        t = t[:a] + new + t[b:]; note(p, 'reviews-hero')
        t = must(t, '.rv-hero { padding-bottom: 56px !important; }', '.rv-hero { padding-bottom: 56px !important; } .rv-hero-visual { width: 78% !important; max-width: 320px !important; } .rv-hero-visual > a { left: -4% !important; padding: 14px 16px 12px !important; }', p, 'reviews-hero-mobile')
    if t != o: p.write_text(t)
for k, v in log.items(): print(f'{k:58s} {", ".join(v)}')
