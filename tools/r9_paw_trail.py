#!/usr/bin/env python3
"""Round 9: paw-print cursor trail per the 10/22 spec (assets/paw-trail.js).

- Removes the interim trail from build 12 (vm-r2.js + .vm-paw-trail CSS).
- Adds data-surface="dark" to dark sections: footer, CTA cards, Testimonial band, dark zig-zag blocks, homepage trust
  band, contact form band, mobile menu / modal backdrops are left alone (trail pauses over dialogs anyway).
- Includes <script defer src="assets/paw-trail.js"> before </body> on every page.

Run from the repo root:  python3 tools/r9_paw_trail.py .
"""
import re, sys, pathlib

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')

# 1. strip the interim trail
js = ROOT / 'assets/vm-r2.js'; j = js.read_text()
a = j.find('(function vmPawTrail() {'); b = j.find('(function vmStoryBlend() {')
assert a > 0 and b > a
j = j[:a] + j[b:]
js.write_text(j)
css = ROOT / 'assets/vm-r2.css'; c = css.read_text()
c = re.sub(r'/\* Paw-print cursor trail \(desktop pointers only\) \*/\n\.vm-paw-trail \{[^\n]*\n@keyframes vmPawFade \{[^\n]*\n@media \(prefers-reduced-motion: reduce\), \(pointer: coarse\) \{ \.vm-paw-trail \{ display: none; \} \}\n', '', c)
assert '.vm-paw-trail' not in c
css.write_text(c)
print('interim trail removed')

# 2. dark surfaces + script tag
DARK_BG = re.compile(r'background:\s*(#2F5694|#223E6B|linear-gradient\([^;"]*#(?:2F5694|223E6B))', re.I)
n = 0; marks = 0
for p in sorted(ROOT.glob('*.html')):
    t = p.read_text()
    if '</body>' not in t: continue
    def mark(m):
        global marks
        tag = m.group(0)
        if 'data-surface=' in tag: return tag
        st = re.search(r'style="([^"]*)"', tag)
        if st and DARK_BG.search(st.group(1)):
            marks += 1
            return tag[:-1] + ' data-surface="dark">'
        return tag
    t = re.sub(r'<(?:section|footer|div class="sp-cta-card[^"]*")[^>]*>', mark, t)
    if '<footer id="contact"' in t and 'data-surface="dark"' not in t[t.find('<footer id="contact"'):t.find('<footer id="contact"') + 200]:
        t = t.replace('<footer id="contact" style="background: #223E6B;">', '<footer id="contact" style="background: #223E6B;" data-surface="dark">', 1); marks += 1
    if 'assets/paw-trail.js' not in t:
        t = t.replace('</body>', '<script defer src="assets/paw-trail.js?v=1"></script>\n</body>', 1)
    p.write_text(t); n += 1
print(f'{n} pages: script tag; {marks} dark surfaces marked')

# 3. cache-bust vm-r2
n = 0
for p in sorted(ROOT.glob('*.html')):
    t = p.read_text(); t2 = re.sub(r'(vm-r2\.(?:css|js))\?v=\d+', r'\1?v=17', t)
    if t2 != t: p.write_text(t2); n += 1
print(f'{n} pages cache-busted to v=17')
