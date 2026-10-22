#!/usr/bin/env python3
"""Round 8 (build 12): John's "Corporate Website Edit 10/22/2026" — final pass before dev handoff.

Thank-you page
- Google reviews under the calendar (3 cards + link to all reviews), with a "you made the right call" line.
- Phone overflow fixed (page could be dragged sideways; the calendar card was wider than the viewport), card centered.
About
- Hero photo -> Why Us gap closed on phones.
Every page (phones)
- Footer bottom row: mascot centered above the copyright line (John's preferred option).
- Section run-ins tightened: fp/sp sections, zig-zag blocks, Dashboard, CTA card -> footer, footer grid -> bottom rule.
- Testimonial band: the paw decoration was clipped flat at the section's top edge (the "hard line"); it now sits inside
  the band on phones, and when the band follows a same-blue block the band's top padding collapses.
Every page (desktop)
- Paw-print cursor trail: light-blue paws alternate left/right behind the pointer and fade. Pointer devices only,
  off under prefers-reduced-motion. (John remembers it from the current live site; it was never in this build.)

Run from the repo root:  python3 tools/r8_client_1022.py .
"""
import re, sys, pathlib

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')

def sub(name, t, old, new, label, expect=1, regex=False):
    n = len(re.findall(old, t, flags=re.S)) if regex else t.count(old)
    if expect == 'all': expect = max(n, 1)
    assert n == expect, f'{name}: {label}: expected {expect} match(es), found {n}'
    return re.sub(old, new, t, flags=re.S) if regex else t.replace(old, new)

EYEBROW = "font-family: 'polymath-text', sans-serif; font-size: 13px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: #2F5694;"
DISPLAY = "font-family: var(--vm-display); font-weight: var(--vm-display-weight, 800);"
GSVG = ('<svg width="18" height="18" viewBox="0 0 48 48" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.1H42V20H24v8h11.3C33.7 32.7 29.3 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.9 1.2 8 3l5.7-5.7C34.3 6.1 29.4 4 24 4 13 4 4 13 4 24s9 20 20 20 20-9 20-20c0-1.3-.1-2.7-.4-3.9z"></path>'
        '<path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 18.9 12 24 12c3.1 0 5.9 1.2 8 3l5.7-5.7C34.3 6.1 29.4 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"></path>'
        '<path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.3 0-9.7-3.4-11.3-8.1l-6.5 5C9.5 39.6 16.2 44 24 44z"></path>'
        '<path fill="#1976D2" d="M43.6 20.1H42V20H24v8h11.3c-.8 2.2-2.2 4.1-4.1 5.5l6.2 5.2C36.9 39.2 44 34 44 24c0-1.3-.1-2.7-.4-3.9z"></path></svg>')

# ------------------------------------------------------------------ 1. thank-you: reviews + overflow
REVIEWS = [
    ('Veterinary Marketing has been amazing. They are so responsive and custom tailored.', 'Adele Hilliard', '#2F5694'),
    ('The team has been great and very responsive. The website they created is beautiful!', 'Andrew Quesada', '#749BEA'),
    ('These guys are great. They are quick, responsive, and professional. They understand the metrics of business. I highly recommend using them.', 'Concierge Vet Club', '#223E6B'),
]
def card(q, n, c):
    ini = ''.join(w[0] for w in n.split()[:2]).upper()
    return f'''      <div style="background: #F4F7FC; border-radius: 22px; padding: 28px; display: flex; flex-direction: column; gap: 16px;">
        <div style="display: flex; align-items: center; justify-content: space-between;"><div style="color: #F3B23E; font-size: 14px; letter-spacing: 3px;">★★★★★</div>{GSVG}</div>
        <p style="font-family: 'polymath-text', sans-serif; font-size: 16px; line-height: 1.6; color: #223E6B; margin: 0; flex: 1 1 auto;">“{q}”</p>
        <div style="display: flex; align-items: center; gap: 12px;"><div style="width: 40px; height: 40px; flex: 0 0 auto; border-radius: 50%; background: {c}; color: #fff; display: flex; align-items: center; justify-content: center; font-family: 'polymath-text', sans-serif; font-size: 13px; font-weight: 800;">{ini}</div><div style="font-size: 15px; font-weight: 700; color: #223E6B;">{n}</div></div>
      </div>
'''
REVIEWS_SECTION = f'''<section id="reviews" data-screen-label="Google reviews" style="max-width: 1140px; margin: 0 auto; padding: 8px 32px 24px; box-sizing: border-box;">
  <div class="vm-reveal" style="text-align: center; margin-bottom: 32px;">
    <div style="{EYEBROW} margin-bottom: 14px;">You’re in good company</div>
    <h2 style="{DISPLAY} font-size: clamp(28px, 3vw, 40px); line-height: 1.1; color: #223E6B; margin: 0 auto 14px; max-width: 640px; text-wrap: balance;">Practices like yours made the same call</h2>
    <div style="display: inline-flex; align-items: center; gap: 9px; background: #fff; border: 1px solid rgba(34,62,107,0.18); border-radius: 999px; padding: 9px 18px; white-space: nowrap;">{GSVG}<span style="font-family: 'polymath-text', sans-serif; font-size: 14px; font-weight: 800; color: #223E6B;">5.0</span><span style="color: #F3B23E; font-size: 12px; letter-spacing: 2px;">★★★★★</span><span style="font-family: 'polymath-text', sans-serif; font-size: 13px; color: #333333;">on Google</span></div>
  </div>
  <div class="vm-reviews3 vm-reveal" style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px;">
{''.join(card(*r) for r in REVIEWS)}  </div>
  <div class="vm-reveal" style="margin-top: 28px; text-align: center;">
    <a href="reviews.html" style="font-family: 'polymath-text', sans-serif; font-size: 15px; font-weight: 800; color: #2F5694; display: inline-flex; align-items: center; gap: 8px; border-bottom: 2px solid rgba(47,86,148,0.3); padding-bottom: 3px;" style-hover="color: #223E6B; border-color: #223E6B;">Read all our Google reviews →</a>
  </div>
</section>

'''
p = ROOT / 'thank-you.html'; t = p.read_text()
assert '<section id="reviews"' not in t
i = t.index('<section id="next"'); t = t[:i] + REVIEWS_SECTION + t[i:]
t = sub(p.name, t, '<section id="top" data-screen-label="Thank you" style="max-width: 1140px; margin: 0 auto; padding: 150px 32px 40px; box-sizing: border-box; position: relative;">',
        '<section id="top" data-screen-label="Thank you" style="max-width: 1140px; margin: 0 auto; padding: 150px 32px 40px; box-sizing: border-box; position: relative; overflow: hidden;">', 'top-overflow')
t = sub(p.name, t, '<section id="next" data-screen-label="What happens next" style="max-width: 1140px; margin: 0 auto; padding: 24px 32px 120px; box-sizing: border-box;">',
        '<section id="next" data-screen-label="What happens next" style="max-width: 1140px; margin: 0 auto; padding: 48px 32px 120px; box-sizing: border-box;">', 'next-pad')
p.write_text(t); print('thank-you.html: reviews, overflow')

# ------------------------------------------------------------------ 2. CSS
css = ROOT / 'assets/vm-r2.css'; c = css.read_text()
assert '---- r8' not in c
c += '''
/* ---- r8 (10/22 client edits, build 12) ---- */
/* Thank-you: no sideways scroll on phones; calendar card centered; reviews grid */
.vm-thanks { grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr); }
.vm-thanks > * { min-width: 0; }
.vm-cal-card { max-width: 100%; overflow: hidden; }
.meetings-iframe-container, .meetings-iframe-container iframe { max-width: 100% !important; }
@media (max-width: 900px) { .vm-thanks { grid-template-columns: minmax(0, 1fr) !important; } .vm-cal-card { margin: 0 auto; width: 100%; } .vm-reviews3 { grid-template-columns: 1fr !important; } }
/* Phones: HubSpot forces its iframe to 312px, so the calendar goes full-bleed (top/bottom rule, no side border) and the widget is centered */
@media (max-width: 600px) { .vm-cal-card { margin: 0 -32px !important; width: auto !important; max-width: none !important; border-left: 0 !important; border-right: 0 !important; border-radius: 0 !important; box-shadow: none !important; padding: 22px 0 18px !important; background: #F4F7FC !important; } .vm-cal-card > div:first-child, .vm-cal-card h2 { padding-left: 32px; padding-right: 32px; } .vm-cal-slot, .meetings-wrap, .meetings-iframe-container { display: flex; justify-content: center; } .meetings-iframe-container iframe { max-width: 100% !important; } }
/* Paw-print cursor trail (desktop pointers only) */
.vm-paw-trail { position: fixed; left: 0; top: 0; width: 30px; height: 27px; pointer-events: none; z-index: 9998; background: #749BEA; -webkit-mask: url("paw-fill-1e3d9826c2.svg") no-repeat center / contain; mask: url("paw-fill-1e3d9826c2.svg") no-repeat center / contain; opacity: 0; animation: vmPawFade 1.8s ease-out forwards; }
@keyframes vmPawFade { 0% { opacity: 0; transform: translate(-50%, -50%) rotate(var(--r)) scale(0.6); } 12% { opacity: 0.75; transform: translate(-50%, -50%) rotate(var(--r)) scale(1); } 100% { opacity: 0; transform: translate(-50%, -50%) rotate(var(--r)) scale(1); } }
@media (prefers-reduced-motion: reduce), (pointer: coarse) { .vm-paw-trail { display: none; } }
@media (max-width: 760px) {
  /* Footer: mascot centered above the copyright line */
  .vm-foot-bottom { align-items: center !important; text-align: center; gap: 16px !important; padding-top: 24px !important; }
  .vm-foot-bottom img { order: -1; height: 46px !important; }
  footer .vm-footer-grid { padding-bottom: 28px !important; }
  footer > div { padding-top: 52px !important; }
  /* About: hero photo runs straight into Why Us */
  #top .sp-hero:not(:has(.sp-hero-media)) { padding-bottom: 0 !important; }
  #why.sp-section { padding-top: 8px !important; }
  /* Focus + service pages: section run-ins */
  .fp-section, .sp-section { padding-top: 48px !important; padding-bottom: 48px !important; }
  #approach { padding-top: 48px !important; padding-bottom: 24px !important; }
  #approach .fp-2col { margin-bottom: 56px !important; }
  #dashboard { padding-top: 48px !important; padding-bottom: 48px !important; }
  #story { padding-top: 48px !important; padding-bottom: 48px !important; }
  #story > div[aria-hidden="true"]:first-child:not([style*="position: absolute"]) { display: none; }   /* 1px hairline rule on focus pages */
  #story > div[aria-hidden="true"][style*="position: absolute"] { top: 24px !important; }               /* service pages: paw no longer clipped at the band edge */
  #story.vm-after-same { padding-top: 8px !important; }
  #reviews.fp-section { padding-bottom: 16px !important; }
  #why.fp-section { padding-top: 24px !important; }
  #book { padding-bottom: 40px !important; }
  #book .sp-cta-card { padding-left: 24px !important; padding-right: 24px !important; }
  /* zig-zag blocks on service pages */
  section.sp-section[data-screen-label]:not(#why):not(#book) { padding-top: 44px !important; padding-bottom: 44px !important; }
  /* thank-you */
  #next { padding-top: 32px !important; padding-bottom: 72px !important; }
}
'''
css.write_text(c); print('vm-r2.css: r8 block')

# ------------------------------------------------------------------ 3. JS: paw trail + Testimonial band blend
js = ROOT / 'assets/vm-r2.js'; j = js.read_text()
assert 'vmPawTrail' not in j
j += r'''
/* ---- r8: paw-print cursor trail + Testimonial band blend ---- */
(function vmPawTrail() {
  if (!window.matchMedia || !matchMedia('(pointer: fine)').matches || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var last = null, side = 1, live = 0;
  document.addEventListener('mousemove', function (e) {
    if (last && Math.hypot(e.clientX - last.x, e.clientY - last.y) < 46) return;
    var ang = last ? Math.atan2(e.clientY - last.y, e.clientX - last.x) : -Math.PI / 2;
    last = { x: e.clientX, y: e.clientY };
    if (live > 14) return;
    side = -side;
    var ox = Math.cos(ang + Math.PI / 2) * 9 * side, oy = Math.sin(ang + Math.PI / 2) * 9 * side;
    var p = document.createElement('span'); p.className = 'vm-paw-trail'; p.setAttribute('aria-hidden', 'true');
    p.style.left = (e.clientX + ox) + 'px'; p.style.top = (e.clientY + oy) + 'px';
    p.style.setProperty('--r', (ang * 180 / Math.PI + 90) + 'deg');
    document.body.appendChild(p); live++;
    p.addEventListener('animationend', function () { p.remove(); live--; });
  }, { passive: true });
})();
(function vmStoryBlend() {
  var st = document.getElementById('story'); if (!st) return;
  var prev = st.previousElementSibling; if (!prev) return;
  var a = getComputedStyle(prev).backgroundColor, b = getComputedStyle(st).backgroundColor;
  if (a === b) st.classList.add('vm-after-same');
  else if (a && a !== 'rgba(0, 0, 0, 0)' && b && b !== 'rgba(0, 0, 0, 0)') st.style.backgroundImage = 'linear-gradient(180deg, ' + a + ' 0, ' + b + ' 120px)';
})();
'''
js.write_text(j); print('vm-r2.js: paw trail, story blend')

# ------------------------------------------------------------------ 4. cache-bust
n = 0
for p in sorted(ROOT.glob('*.html')):
    t = p.read_text(); t2 = re.sub(r'(vm-r2\.(?:css|js))\?v=\d+', r'\1?v=16', t)
    if t2 != t: p.write_text(t2); n += 1
print(f'{n} pages cache-busted to v=16')
