#!/usr/bin/env python3
"""Round 2, part 1: sitewide changes across every page in site-deployed/.
A1 CTAs->Request Info, A2 remove analysis bands, A3 nav, A4/A5 shared runtime hooks, A6 rating badge,
A7 all-8 services on focus pages, A8 all-8 focus on service pages. Idempotent: re-running is a no-op.
"""
import re, sys, json, pathlib

ROOT = pathlib.Path(sys.argv[1])
AM = json.load(open('tools/assetmap.json'))
PAGES = sorted(p for p in ROOT.glob('*.html'))
FOCUS = [p for p in PAGES if any(k in p.name for k in ['practice-veterinary-marketing', 'emergency-vet', 'equine-vet', 'veterinary-specialty'])]
SERVICE = [p for p in PAGES if p.name.startswith('veterinary-') and p not in FOCUS]
assert len(FOCUS) == 8 and len(SERVICE) == 8, (len(FOCUS), len(SERVICE))

REQ = 'href="#request-info" sc-camel-on-click="{{ openReq }}"'
WIZ = 'https://wizard.veterinarymarketing.com/your-veterinary-practice'
changes = {}

def log(p, k, n=1):
    changes.setdefault(p.name, {}); changes[p.name][k] = changes[p.name].get(k, 0) + n

def sub(p, t, pat, rep, k, count=0, flags=0, expect=None):
    new, n = re.subn(pat, rep, t, count=count, flags=flags)
    if expect is not None and n != expect:
        raise SystemExit(f"{p.name}: {k}: expected {expect} replacements, got {n}")
    if n: log(p, k, n)
    return new

for p in PAGES:
    t = p.read_text()
    orig = t
    name = p.name

    # ---------- shared runtime (A4 headline scrub, A5 counters, device frames CSS) ----------
    if 'assets/vm-r2.css' not in t:
        t = t.replace('</helmet>', '  <link rel="stylesheet" href="assets/vm-r2.css">\n  <script src="assets/vm-r2.js" defer></script>\n</helmet>', 1)
        log(p, 'runtime')
    # per-page counter observers are superseded by vm-r2.js (which supports data-from)
    t = sub(p, t, r"\n\s*document\.querySelectorAll\('\.(fp|sp)-count'\)\.forEach\(el => this\.countObserver\.observe\(el\)\);", '', 'drop-page-counter')

    # ---------- A3 nav: drop Free Competitive Analysis from header + mobile menu; Blog -> blog.html ----------
    t = sub(p, t, r'\s*<a href="free-veterinary-marketing-analysis\.html" style="\{\{ navFaStyle \}\}"[^>]*>Free Competitive Analysis</a>', '', 'nav-fa', expect=1 if name != 'blog.html' else 0)
    t = sub(p, t, r"\s*\{ label: 'Free Competitive Analysis', href: 'free-veterinary-marketing-analysis\.html' \},(?=\s*\{ label: 'Contact')", '', 'mobile-fa')
    t = t.replace("{ label: 'Our Blog', href: 'https://www.veterinarymarketing.com/blog' }", "{ label: 'Our Blog', href: 'blog.html' }")
    t = t.replace("{ label: 'Blog', href: 'https://www.veterinarymarketing.com/blog' }", "{ label: 'Blog', href: 'blog.html' }")
    if 'veterinarymarketing.com/blog' in t: log(p, 'WARN-blog-url-left')

    # ---------- A1 CTAs ----------
    if name == 'index.html':
        # hero secondary button stays on the wizard, new tab (John: homepage item 1)
        t = sub(p, t, r'<a href="' + re.escape(WIZ) + r'"(\s+style="[^"]*"\s+style-hover="background: #EDF7FC;[^"]*")>Free Competitive Analysis</a>',
                r'<a href="' + WIZ + r'" target="_blank" rel="noopener"\1>Free Competitive Analysis</a>', 'hero-wizard-newtab', expect=1)
        # every other wizard CTA on the homepage -> Request Info modal
        labels = {'Get your free competitive analysis →': 'Request information →', 'Start with a free analysis →': 'Request information →',
                  'Talk to our team →': 'Talk to our team →', 'Get my free analysis →': 'Request information →'}
        for old, new in labels.items():
            t = sub(p, t, r'<a href="' + re.escape(WIZ) + r'"([^>]*)>' + re.escape(old) + '</a>', r'<a ' + REQ + r'\1>' + new + '</a>', 'cta-' + old[:12])
    elif name == 'free-veterinary-marketing-analysis.html':
        t = sub(p, t, r'<a href="' + re.escape(WIZ) + r'"(?! target)', '<a href="' + WIZ + '" target="_blank" rel="noopener"', 'fa-newtab')
        # also any JS-built wizard links on this page open in a new tab (handled in template: check later)
    else:
        t = sub(p, t, r'<a href="' + re.escape(WIZ) + r'"([^>]*)>Book your free practice review →</a>', r'<a ' + REQ + r'\1>Request information →</a>', 'cta-book')
        t = sub(p, t, r'<a href="' + re.escape(WIZ) + r'"([^>]*)>Get started →</a>', r'<a ' + REQ + r'\1>Request information →</a>', 'cta-getstarted')
    if WIZ in t and name not in ('index.html', 'free-veterinary-marketing-analysis.html'):
        log(p, 'WARN-wizard-left')

    # ---------- A2 remove Free Competitive Analysis bands ----------
    if name in ('index.html', 'contact-us.html'):
        t = sub(p, t, r'\n<section id="analysis".*?</section>\n', '\n', 'drop-analysis-section', count=1, flags=re.S, expect=1)
    if p in SERVICE:
        t = sub(p, t, r'\s*<p class="vm-reveal"[^>]*>Not ready to talk yet\? Start with our <a href="free-veterinary-marketing-analysis\.html".*?</p>', '', 'drop-why-analysis-p', count=1, flags=re.S, expect=1)
    if p in FOCUS:
        t = sub(p, t, r'(<section id="book".*?class="fp-cta-peek"[^>]*>\s*<div[^>]*>)Free (?:practice|launch|hospital|group) review(</div>)', r'\1Next step\2', 'book-eyebrow', count=1, flags=re.S, expect=1)
        t = t.replace("Book a call and we'll review", "Request information and we'll review")

    # ---------- A6 rating badge: Google G + 5.0 + stars, no review count anywhere (John: stop hand-updating it) ----------
    t = sub(p, t, r'\s*<span style="[^"]*">\{\{ reviewCountLabel \}\}</span>', '', 'badge-count')
    t = sub(p, t, r'Read all \{\{ reviewCountLabel \}\} →', 'Read all our Google reviews →', 'badge-readall')
    if name == 'reviews.html':
        t = sub(p, t, r'(<div aria-label="Five out of five stars"[^>]*>★★★★★</div>)\s*<div style="[^"]*">\{\{ reviewCountLabel \}\}</div>', r'\1', 'reviews-card-count', expect=1)
    if '{{ reviewCountLabel }}' in t: log(p, 'WARN-count-left')

    # ---------- A7 focus pages: all 8 services, compact ----------
    if p in FOCUS:
        SVC8 = """[
        { name: 'Veterinary Websites', img: asset('assets/opt/svc-websites.webp'), href: 'veterinary-websites.html', body: 'Custom sites built around SEO, AEO and user experience. No templates, live in under 25 days.' },
        { name: 'Veterinary SEO', img: asset('assets/opt/svc-seo.webp'), href: 'veterinary-seo-marketing.html', body: 'A page for every service, local keywords, weekly posts and an optimized Google Business Profile.' },
        { name: 'Veterinary AEO', img: 'assets/%(aeo)s', href: 'veterinary-aeo.html', body: 'Get recommended by ChatGPT, Google AI Overviews and other AI tools when pet owners ask for a vet.' },
        { name: 'Google Ads / PPC', img: asset('assets/opt/svc-googleadwords.webp'), href: 'veterinary-ppc-marketing.html', body: 'Dedicated campaigns with a lower cost per click and no management fee on your ad spend.' },
        { name: 'ChatGPT Ads', img: 'assets/%(chat)s', href: 'veterinary-chatgpt-ads.html', body: 'Reach local pet owners while they ask AI for help. Target by zip code, track ROI.' },
        { name: 'Social Media Ads', img: asset('assets/opt/svc-social-media.webp'), href: 'veterinary-social-media-marketing.html', body: 'Meta Ads with precise local targeting, brand awareness campaigns and every dollar tracked.' },
        { name: 'Social Media Posting', img: 'assets/%(post)s', href: 'veterinary-social-media-posting.html', body: 'Custom content every week, made for your practice. No cookie-cutter posts.' },
        { name: 'Direct Mail', img: 'assets/directmail-b55a595947.png', href: 'veterinary-direct-mail-marketing.html', body: 'Postcards to website visitors who did not book, within 3 days, tracked in the same dashboard.' }
      ]""" % {'aeo': AM['aeo-logos'], 'chat': AM['chatgpt-card'], 'post': AM['posting-iphone']}
        IMGSTYLE = "imgStyle: { width: '100%', height: '100%', backgroundImage: `url(\"${asset(s.img)}\")`, backgroundSize: 'contain', backgroundPosition: 'center', backgroundRepeat: 'no-repeat', filter: 'drop-shadow(0 10px 16px rgba(34,62,107,0.18))' }"
        m = re.search(r"      services: \[\n.*?\n      \]\.map\(s => \(\{ \.\.\.s, imgStyle: \{[^\n]*\n", t, re.S)
        if m:  # small-animal: hand-written 4 services
            svc = "      services: " + SVC8 + ".map(s => ({ ...s, proof: 'Learn more →', " + IMGSTYLE + " })),\n"
            t = t[:m.start()] + svc + t[m.end():]
        else:  # data-driven focus pages: keep the segment-specific copy for the 4 services that had it
            m = re.search(r"      services: P\.services\.items\.map\(\(s, i\) => \(\{ \.\.\.s, name: svcMeta\[i\]\[0\], href: svcMeta\[i\]\[2\], imgStyle: \{[^\n]*\n", t)
            assert m, name + ': services block (P)'
            svc = "      services: " + SVC8 + ".map((s, i) => { const o = { 0: 0, 1: 1, 3: 2, 5: 3 }[i]; const src = o === undefined ? null : P.services.items[o]; return { ...s, body: src && src.body ? src.body : s.body, proof: 'Learn more →', " + IMGSTYLE + " }; }),\n"
            t = t[:m.start()] + svc + t[m.end():]
        log(p, 'services-8')
        # compact card markup
        t = sub(p, t, r'<div class="fp-svc" style="position: relative; display: grid; grid-template-columns: repeat\(2, minmax\(0, 1fr\)\); gap: 40px;">',
                '<div class="fp-svc vm-svc8" style="position: relative; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 18px;">', 'svc-grid', expect=1)
        t = sub(p, t, r'(<sc-for list="\{\{ services \}\}" as="svc" hint-placeholder-count=")4(">)', r'\g<1>8\2', 'svc-count', expect=1)
        t = sub(p, t, r'(<sc-for list="\{\{ services \}\}".*?<a href="\{\{ svc\.href \}\}" class="vm-reveal" style="display: flex; flex-direction: column; color: inherit; border: 1px solid rgba\(34,62,107,0\.16\); border-radius: 22px; padding: )38px 36px 40px;',
                r'\g<1>22px 20px 22px;', 'svc-pad', count=1, flags=re.S, expect=1)
        t = sub(p, t, r'(<sc-for list="\{\{ services \}\}".*?<div style="height: )220px; margin-bottom: 24px;', r'\g<1>120px; margin-bottom: 16px;', 'svc-img', count=1, flags=re.S, expect=1)
        t = sub(p, t, r'(<sc-for list="\{\{ services \}\}".*?<h3 style="font-family: var\(--vm-display\); font-weight: var\(--vm-display-weight, 800\); font-size: )23px; color: #223E6B; margin: 0 0 10px;', r'\g<1>18px; line-height: 1.2; color: #223E6B; margin: 0 0 8px;', 'svc-h3', count=1, flags=re.S, expect=1)
        t = sub(p, t, r'(<sc-for list="\{\{ services \}\}".*?<p style="font-size: )15px; line-height: 1\.6; color: #333333; margin: 0;">\{\{ svc\.body \}\}', r'\g<1>13.5px; line-height: 1.5; color: #333333; margin: 0;">{{ svc.body }}', 'svc-p', count=1, flags=re.S, expect=1)
        t = sub(p, t, r'(<sc-for list="\{\{ services \}\}".*?font-size: )15px; font-weight: 700; color: #2F5694; margin-top: auto; padding-top: 16px;">\{\{ svc\.proof \}\}', r'\g<1>13.5px; font-weight: 700; color: #2F5694; margin-top: auto; padding-top: 12px;">{{ svc.proof }}', 'svc-proof', count=1, flags=re.S, expect=1)
        t = sub(p, t, r'\.fp-svc \{ grid-template-columns: 1fr !important; \}', '.fp-svc { grid-template-columns: 1fr 1fr !important; gap: 12px !important; }', 'svc-css', expect=1)
        # A5: stats + reasons + hero 200+ counters
        t = sub(p, t, r"\{ value: '2 hrs', label: 'response time when you reach out' \}", "{ value: '< 2 hrs', from: '48', label: 'response time when you reach out' }", 'stat-2hrs', expect=1)
        t = sub(p, t, r'class="fp-count" data-count="\{\{ st\.value \}\}"', 'class="fp-count" data-count="{{ st.value }}" data-from="{{ st.from }}"', 'stat-from', expect=1)
        t = sub(p, t, r"\{ value: '2 hrs', title: '2-hour response time',", "{ value: '< 2 hrs', from: '48', title: '2-hour response time',", 'reason-2hrs', expect=1)
        t = sub(p, t, r"\{ value: '< 6 hrs', title: 'Website edits done fast',", "{ value: '< 6 hrs', from: '72', title: 'Website edits done fast',", 'reason-6hrs', expect=1)
        t = sub(p, t, r'(<sc-for list="\{\{ reasons \}\}" as="rs"[^>]*>\s*<div class="vm-reveal"[^>]*>\s*<div style="[^"]*")>\{\{ rs\.value \}\}', r'\1 data-count="{{ rs.countVal }}" data-from="{{ rs.from }}">{{ rs.value }}', 'reason-count', count=1, expect=1)
        t = sub(p, t, r"(      reasons: \[\n(?:.*\n){4}      \])\n", r"\1.map(r => ({ ...r, countVal: r.from ? r.value : '', from: r.from || '' })),\n", 'reason-map', count=1, expect=1)
        t = sub(p, t, r'(<div style="[^"]*")>200\+</div>', r'\1 data-count="200+">200+</div>', 'hero-200', count=1, expect=1)
        # stats template: `from` undefined renders "undefined"? ensure stats map carries from:''
        t = sub(p, t, r"(      stats: \[\n(?:.*\n){4}      \])(,\n)", r"\1.map(s => ({ ...s, from: s.from || '' }))\2", 'stats-map', count=1, expect=1)

    # ---------- A8 service pages: all 8 practice types, no "see all" link ----------
    if p in SERVICE:
        t = sub(p, t, r'\s*<a href="index\.html#focus" style="[^"]*" style-hover="[^"]*">See all eight practice types →</a>', '', 'drop-seeall', expect=1)
        t = sub(p, t, r"relatedFocus: P\.focus\.map\(f => \(\{ name: f\.name, why: f\.why, href: focusFiles\[f\.name\], short: focusShort\[f\.name\], imgStyle: \{ width: '120px', height: '120px',",
                "relatedFocus: focusNames.map(n => ({ name: n, why: (P.focus.find(f => f.name === n) || {}).why || '', href: focusFiles[n], short: focusShort[n], imgStyle: { width: '72px', height: '72px',", 'focus-8', expect=1)
        t = sub(p, t, r"(relatedFocus: focusNames\.map\(n => .*?)asset\(focusImgs\[f\.name\]\)", r"\1asset(focusImgs[n])", 'focus-8b', count=1, expect=1)
        t = sub(p, t, r'<div class="sp-focus" style="position: relative; display: grid; grid-template-columns: repeat\(2, minmax\(0, 1fr\)\); gap: 28px;">',
                '<div class="sp-focus vm-focus8" style="position: relative; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px;">', 'focus-grid', expect=1)
        t = sub(p, t, r'(<sc-for list="\{\{ relatedFocus \}\}" as="rf" hint-placeholder-count=")2(">)', r'\g<1>8\2', 'focus-count', expect=1)
        # compact card: image + name + link line (drop the long "why" sentence on the grid)
        t = sub(p, t, r'(<sc-for list="\{\{ relatedFocus \}\}".*?<a href="\{\{ rf\.href \}\}" class="vm-reveal" style="display: grid; grid-template-columns: )120px minmax\(0, 1fr\); gap: 24px; align-items: center; color: inherit; border: 1px solid rgba\(34,62,107,0\.16\); border-radius: 22px; padding: 22px 26px 22px 22px;',
                r'\g<1>72px minmax(0, 1fr); gap: 14px; align-items: center; color: inherit; border: 1px solid rgba(34,62,107,0.16); border-radius: 18px; padding: 14px 16px 14px 14px;', 'focus-card', count=1, flags=re.S, expect=1)
        t = sub(p, t, r'(<sc-for list="\{\{ relatedFocus \}\}".*?<h3 style="font-family: var\(--vm-display\); font-weight: var\(--vm-display-weight, 800\); font-size: )21px; color: #223E6B; margin: 0 0 8px;">\{\{ rf\.name \}\}</h3>\s*<p style="[^"]*">\{\{ rf\.why \}\}</p>\s*<div style="font-family: \'polymath-text\', sans-serif; font-size: 14\.5px;',
                r'\g<1>16px; line-height: 1.2; color: #223E6B; margin: 0 0 6px;">{{ rf.name }}</h3>\n          <div style="font-family: \'polymath-text\', sans-serif; font-size: 13px;', 'focus-card-body', count=1, flags=re.S, expect=1)
        t = sub(p, t, r'\.sp-focus \{ grid-template-columns: 1fr !important; \}', '.sp-focus { grid-template-columns: 1fr 1fr !important; gap: 10px !important; }', 'focus-css', expect=1)
        # A5: reasons counters on service pages (value/title/body triplets) + PPC specifics
        _old = "reasons: P.reasons.map((r) => ({ value: r[0], title: r[1], body: r[2] })),"
        _new = "reasons: P.reasons.map((r) => ({ value: r[0], title: r[1], body: r[2], from: r[3] || '', countVal: (r[3] !== undefined || /^[$<\\s]*[\\d,.]+[%+xM\\s]*$/.test(r[0])) && !/^(19|20)\\d\\d$/.test(r[0]) ? r[0] : '' })),"
        assert t.count(_old) == 1, name + ': sp-reason-map'
        t = t.replace(_old, _new); log(p, 'sp-reason-map')
        t = sub(p, t, r'(<sc-for list="\{\{ reasons \}\}" as="rs"[^>]*>\s*<div class="vm-reveal"[^>]*>\s*<div style="[^"]*")>\{\{ rs\.value \}\}', r'\1 data-count="{{ rs.countVal }}" data-from="{{ rs.from }}">{{ rs.value }}', 'sp-reason-count', count=1, expect=1)
        if name == 'veterinary-ppc-marketing.html':
            t = sub(p, t, r'\["0%","Fee on your ad spend",', '["0%","Fee on your ad spend",', 'ppc-0pct-check')  # ensure exists
            t = sub(p, t, r'\["0%","Fee on your ad spend","([^"]*)"\]', r'["0%","Fee on your ad spend","\1","20"]', 'ppc-0pct-from', expect=1)
            t = sub(p, t, r'\["1","Dedicated account manager","([^"]*)"\]', r'["✓","Dedicated account manager","\1"]', 'ppc-check', expect=1)
        for pg in ('veterinary-chatgpt-ads.html', 'veterinary-social-media-marketing.html'):
            if name == pg:
                t = sub(p, t, r'\["1","Dedicated account manager","([^"]*)"\]', r'["✓","Dedicated account manager","\1"]', 'check-dam', expect=1)
        if name == 'veterinary-social-media-posting.html':
            t = sub(p, t, r'\["2 hrs","Response time","([^"]*)"\]', r'["< 2 hrs","Response time","\1","48"]', 'posting-2hrs', expect=1)

    if t != orig:
        p.write_text(t)

for k, v in changes.items():
    warn = {a: b for a, b in v.items() if a.startswith('WARN')}
    print(f"{k:58s} {sum(v.values()):3d} edits" + (f"  {warn}" if warn else ''))
