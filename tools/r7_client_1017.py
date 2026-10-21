#!/usr/bin/env python3
"""Round 7 (build 11): Bill + John's edit request of 10/17/2026, answers of 10/21.

Every page
- Header: "Client Results" (reviews.html) added between Areas of Focus and Contact, desktop + mobile menu.
- Footer: animated white logo (re-encoded from the live site's GIF), partner badges (Google Partner / Microsoft
  Advertising Partner / Meta Business Partner) replace the platform-logo row, "Privacy & Terms of Use", © 2027,
  mascot aligned on phones.
- Request Info modal + Contact form: submit -> thank-you.html (was an inline "Thanks" state).
- Mobile menu: inactive slide page collapses (no empty space under the Call row).
- Mobile modal: bottom padding clears Safari / in-app browser toolbars.
New pages: thank-you.html (HubSpot Meetings placeholder), blog-post.html (article layout for the CMS hookup).
About: Why Us panel (company-wide stats) right after the hero; Core Values moved above the join-our-team CTA; hero photo
full width on phones.
Direct mail: new 10/19 mailer on the homepage card, 8 focus-page service grids, and the Direct Mail page (hero + sample).
Service + focus heroes on phones: tag only (no "Services /"), one short line, CTA, call, logos, image.
Focus pages: 10/21 one-liners from Bill; "Why us" headline gets a soft hyphen so the brand doesn't break mid-word.

Run from the repo root:  python3 tools/r7_client_1017.py .
Assets pre-converted (tools/r7_assets.json).
"""
import re, sys, json, pathlib, html

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
A = json.load(open(ROOT / 'tools/r7_assets.json'))

SERVICE_PAGES = ['veterinary-websites', 'veterinary-seo-marketing', 'veterinary-aeo', 'veterinary-ppc-marketing',
                 'veterinary-chatgpt-ads', 'veterinary-social-media-marketing', 'veterinary-social-media-posting',
                 'veterinary-direct-mail-marketing']
FOCUS_PAGES = ['small-animal-practice-veterinary-marketing', 'veterinary-specialty-practice-marketing',
               'emergency-vet-practice-marketing', 'urgent-care-animal-practice-veterinary-marketing',
               'startup-practice-veterinary-marketing', 'mobile-practice-veterinary-marketing-strategies',
               'multi-location-practice-veterinary-marketing-strategies', 'equine-veterinary-marketing']
FOCUS_SHORT = {  # Bill, 10/21
    'small-animal-practice-veterinary-marketing': 'You opened a practice to deliver quality medicine, not to manage Google rankings.',
    'veterinary-specialty-practice-marketing': 'You trained for the highest level of care, not to manage marketing full-time.',
    'emergency-vet-practice-marketing': 'You practice under the hardest conditions; your marketing should match that reality.',
    'urgent-care-animal-practice-veterinary-marketing': 'You fill the gap between booked clinics and long ER waits with quality care.',
    'startup-practice-veterinary-marketing': 'You’ve built the practice; now pet parents need to know you exist.',
    'mobile-practice-veterinary-marketing-strategies': 'You deliver quality medicine to the driveway; running it is the hard part.',
    'multi-location-practice-veterinary-marketing-strategies': 'You’ve grown locations that work; marketing the group is a different job.',
    'equine-veterinary-marketing': 'You practice quality medicine in barns and pastures, one handshake at a time.',
}

def sub(name, t, old, new, label, expect=1, regex=False):
    n = len(re.findall(old, t, flags=re.S)) if regex else t.count(old)
    if expect == 'all': expect = max(n, 1)
    assert n == expect, f'{name}: {label}: expected {expect} match(es), found {n}'
    return re.sub(old, new, t, flags=re.S) if regex else t.replace(old, new)

EYEBROW = "font-family: 'polymath-text', sans-serif; font-size: 13px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: #2F5694;"
DISPLAY = "font-family: var(--vm-display); font-weight: var(--vm-display-weight, 800);"
SHY = 'Veterinary­Marketing.com'

# ------------------------------------------------------------------ 1. every page: header, footer, modal, mobile menu
badges = (f'<div class="vm-badges" aria-label="Partner certifications">'
          f'<img src="{A["badge-google-w"]}" alt="Google Partner" loading="lazy">'
          f'<img src="{A["badge-bing-w"]}" alt="Microsoft Advertising Partner" loading="lazy">'
          f'<img src="{A["badge-meta-w"]}" alt="Meta Business Partner" loading="lazy"></div>')
n = 0
for p in sorted(ROOT.glob('*.html')):
    if p.name in ('thank-you.html', 'blog-post.html'): continue
    t = p.read_text()
    if '<footer id="contact"' not in t: continue
    # header: desktop
    t = sub(p.name, t, '<a href="contact-us.html" style="{{ navContactStyle }}" style-hover="background: rgba(34,62,107,0.07);">Contact</a>',
            '<a href="reviews.html" style="{{ navResultsStyle }}" style-hover="background: rgba(34,62,107,0.07);">Client Results</a>\n'
            '      <a href="contact-us.html" style="{{ navContactStyle }}" style-hover="background: rgba(34,62,107,0.07);">Contact</a>', 'nav-desktop')
    t = sub(p.name, t, "navContactStyle: activeStyle(isHere('contact-us.html')),",
            "navContactStyle: activeStyle(isHere('contact-us.html')),\n      navResultsStyle: activeStyle(isHere('reviews.html')),", 'nav-style', expect='all')
    # About's parent pill should not light up on the Reviews page now that Client Results has its own item
    t = sub(p.name, t, "activeParentStyle(isHere(m.href) || m.items.some(it => isHere(it.href)))",
            "activeParentStyle(isHere(m.href) || m.items.some(it => it.href !== 'reviews.html' && isHere(it.href)))", 'nav-parent')
    # header: mobile
    t = sub(p.name, t, r"\{ label: 'Areas of Focus', sub: 'focus' \}, \{ label: 'Contact', href: 'contact-us.html' \}(\s*)\]\.map\(",
            r"{ label: 'Areas of Focus', sub: 'focus' }, { label: 'Client Results', href: 'reviews.html' }, { label: 'Contact', href: 'contact-us.html' }\1].map(", 'nav-mobile', regex=True)
    t = sub(p.name, t, "(l.sub === 'about' && [{ label: 'About Us', href: 'about.html' }, { label: 'Reviews', href: 'reviews.html' }, { label: 'Conferences', href: 'conferences.html' }, { label: 'Our Blog', href: 'blog.html' }].some(a => isHere(a.href)))",
            "(l.sub === 'about' && [{ label: 'About Us', href: 'about.html' }, { label: 'Conferences', href: 'conferences.html' }, { label: 'Our Blog', href: 'blog.html' }].some(a => isHere(a.href)))", 'nav-mobile-about')
    # mobile menu: two slide pages; the one off-screen collapses so the panel is only as tall as the visible page
    t = sub(p.name, t, '<div style="{{ mobilePageStyle }}">', '<div style="{{ mobileTopPageStyle }}">', 'mob-page-a', expect=2)
    i = t.index('<div style="{{ mobileTopPageStyle }}">'); j = t.index('<div style="{{ mobileTopPageStyle }}">', i + 1)
    t = t[:j] + '<div style="{{ mobileSubPageStyle }}">' + t[j + len('<div style="{{ mobileTopPageStyle }}">'):]
    t = sub(p.name, t, "mobilePageStyle: 'width: 50%; flex: 0 0 50%; display: flex; flex-direction: column; gap: 2px; box-sizing: border-box; padding: 16px;',",
            "mobileTopPageStyle: 'width: 50%; flex: 0 0 50%; display: flex; flex-direction: column; gap: 2px; box-sizing: border-box; padding: 16px;' + (this.state.mobileSub ? ' height: 0; padding-top: 0; padding-bottom: 0; overflow: hidden;' : ''),\n"
            "      mobileSubPageStyle: 'width: 50%; flex: 0 0 50%; display: flex; flex-direction: column; gap: 2px; box-sizing: border-box; padding: 16px;' + (this.state.mobileSub ? '' : ' height: 0; padding-top: 0; padding-bottom: 0; overflow: hidden;'),", 'mob-page-style')
    # footer
    t = sub(p.name, t, '<img src="assets/logo-reverse-07040e3b40.svg" alt="Veterinary Marketing" style="height: 56px; margin-bottom: 20px;">',
            f'<img class="vm-foot-logo" src="{A["logo-anim-w"]}" alt="Veterinary Marketing" style="height: 60px; width: auto; margin-bottom: 20px;" loading="lazy">', 'footer-logo')
    t = sub(p.name, t, r'<div class="vm-platforms vm-platforms-white" aria-label="Advertising platforms we work in">.*?</div>\n', badges + '\n', 'footer-badges', regex=True)
    t = sub(p.name, t, 'style-hover="color: #749BEA;">Privacy Policy</a>', 'style-hover="color: #749BEA;">Privacy &amp; Terms of Use</a>', 'footer-privacy')
    t = sub(p.name, t, '© 2026 VeterinaryMarketing.com', '© 2027 VeterinaryMarketing.com', 'footer-year')
    t = sub(p.name, t, '<div style="border-top: 1px solid rgba(255,255,255,0.18); padding: 30px 0 38px; display: flex; align-items: center; justify-content: space-between; gap: 16px 24px; flex-wrap: wrap;">',
            '<div class="vm-foot-bottom" style="border-top: 1px solid rgba(255,255,255,0.18); padding: 30px 0 38px; display: flex; align-items: center; justify-content: space-between; gap: 16px 24px; flex-wrap: wrap;">', 'footer-bottom')
    # Request Info -> thank-you page
    t = sub(p.name, t, "this.setState({ reqDone: true }); },", "window.location.href = 'thank-you.html'; },", 'modal-redirect')
    if 'contactDone: true' in t:
        t = sub(p.name, t, "this.setState({ contactDone: true }); }", "window.location.href = 'thank-you.html'; }", 'contact-redirect')
    # "Why us" headline: let the brand break after "Veterinary" instead of anywhere
    t = t.replace('>VeterinaryMarketing.com</span>', '>' + SHY + '</span>')
    t = t.replace("choose VeterinaryMarketing.com'", "choose " + SHY + "'").replace('choose VeterinaryMarketing.com"', 'choose ' + SHY + '"')
    p.write_text(t); n += 1
print(f'{n} pages: header, footer, modal redirect, mobile menu')

# ------------------------------------------------------------------ 2. service pages: hero classes for the phone stack
for name in SERVICE_PAGES:
    p = ROOT / f'{name}.html'; t = p.read_text()
    t = sub(p.name, t, '<div style="display: flex; align-items: center; gap: 10px; font-family: \'polymath-text\', sans-serif; font-size: 13px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: #2F5694; margin-bottom: 20px;"><a href="index.html#services"',
            '<div class="vm-crumb" style="display: flex; align-items: center; gap: 10px; font-family: \'polymath-text\', sans-serif; font-size: 13px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: #2F5694; margin-bottom: 20px;"><a href="index.html#services"', 'crumb')
    t = sub(p.name, t, '<p style="font-family: \'polymath-text\', sans-serif; font-size: 17px; font-weight: 700; line-height: 1.4; color: #2F5694; margin: 0 0 22px; max-width: 560px;">{{ sub }}</p>',
            '<p class="vm-hero-sub" style="font-family: \'polymath-text\', sans-serif; font-size: 17px; font-weight: 700; line-height: 1.4; color: #2F5694; margin: 0 0 22px; max-width: 560px;">{{ sub }}</p>', 'hero-sub')
    t = sub(p.name, t, '<p style="font-size: 18px; line-height: 1.6; color: #333333; max-width: 560px; margin: 0 0 16px;"><sc-for list="{{ pr.segs }}"',
            '<p class="vm-hero-intro" style="font-size: 18px; line-height: 1.6; color: #333333; max-width: 560px; margin: 0 0 16px;"><sc-for list="{{ pr.segs }}"', 'hero-intro')
    t = sub(p.name, t, '<p style="font-size: 16.5px; font-weight: 700; line-height: 1.5; color: #223E6B; margin: 0;">{{ heroCta }}</p>',
            '<p class="vm-hero-lead" style="font-size: 16.5px; font-weight: 700; line-height: 1.5; color: #223E6B; margin: 0;">{{ heroCta }}</p>', 'hero-lead')
    p.write_text(t)
print('8 service pages: hero classes')

# ------------------------------------------------------------------ 3. focus pages: crumb + one-liner, mailer in the services grid
for name in FOCUS_PAGES:
    p = ROOT / f'{name}.html'; t = p.read_text()
    t = sub(p.name, t, 'color: #2F5694; margin-bottom: 20px;"><a href="index.html#focus"', 'color: #2F5694; margin-bottom: 20px;"><a href="index.html#focus"', 'crumb-present')
    t = sub(p.name, t, '<div style="display: flex; align-items: center; gap: 10px; font-family: \'polymath-text\', sans-serif; font-size: 13px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: #2F5694; margin-bottom: 20px;"><a href="index.html#focus"',
            '<div class="vm-crumb" style="display: flex; align-items: center; gap: 10px; font-family: \'polymath-text\', sans-serif; font-size: 13px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: #2F5694; margin-bottom: 20px;"><a href="index.html#focus"', 'crumb')
    long_p = '<p style="font-size: 19px; line-height: 1.6; color: #333333; max-width: 560px; margin: 0 0 32px;">'
    i = t.index('<div class="fp-hero-copy"'); j = t.index(long_p, i)
    assert j - i < 1500, f'{p.name}: hero paragraph not where expected'
    short = f'<p class="vm-hero-short" style="font-size: 19px; line-height: 1.6; color: #333333; max-width: 560px; margin: 0 0 32px;">{html.escape(FOCUS_SHORT[name], quote=False)}</p>\n      '
    t = t[:j] + short + long_p.replace('<p style=', '<p class="vm-hero-long" style=') + t[j + len(long_p):]
    t = sub(p.name, t, "img: 'assets/directmail-b55a595947.png'", f"img: '{A['mailer-card-1017']}'", 'mailer-grid')
    p.write_text(t)
print('8 focus pages: crumb, one-liner, mailer')

# ------------------------------------------------------------------ 4. homepage card + direct mail page
p = ROOT / 'index.html'; t = p.read_text()
t = sub(p.name, t, '"uploads/directmail.png": "assets/directmail-b55a595947.png"', f'"uploads/directmail.png": "{A["mailer-card-1017"]}"', 'mailer-home')
p.write_text(t)
p = ROOT / 'veterinary-direct-mail-marketing.html'; t = p.read_text()
t = sub(p.name, t, '"uploads/directmail.png": "assets/directmail-b55a595947.png"', f'"uploads/directmail.png": "{A["mailer-card-1017"]}"', 'mailer-dm-map')
t = sub(p.name, t, '"heroImg":"assets/direct-mail-hero-0ece8891e0.webp"', f'"heroImg":"{A["mailer-1017"]}"', 'mailer-dm-hero')
t = sub(p.name, t, '"src": "assets/dm-f2bc6d15cf.webp"', f'"src": "{A["mailer-1017"]}"', 'mailer-dm-sample')
p.write_text(t)
print('homepage + direct mail page: mailer')

# ------------------------------------------------------------------ 5. About: Why Us after the hero, Core Values above the CTA
p = ROOT / 'about.html'; t = p.read_text()
values = re.search(r'<section id="values" data-screen-label="Core values".*?</section>\n\n', t, re.S).group(0)
t = t.replace(values, '', 1)
values = values.replace('padding: 24px 32px 104px;', 'padding: 96px 32px 24px;', 1)
WHY = f'''<section id="why" data-screen-label="Why us" class="sp-section" style="max-width: 1140px; margin: 0 auto; padding: 24px 32px 96px; box-sizing: border-box; position: relative;">
  <div class="vm-reveal" style="position: relative; text-align: center; margin-bottom: 52px;">
    <div style="{EYEBROW} margin-bottom: 16px;">Why us</div>
    <h2 style="{DISPLAY} font-size: clamp(32px, 3.4vw, 46px); line-height: 1.1; color: #223E6B; margin: 0 auto; max-width: 640px; text-wrap: balance;">Why practices choose {SHY}</h2>
  </div>
  <div class="sp-grid4" style="position: relative; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 28px;">
    <sc-for list="{{{{ reasons }}}}" as="rs" hint-placeholder-count="4">
      <div class="vm-reveal" style="text-align: center; padding: 8px 12px;">
        <div style="{DISPLAY} font-size: 44px; line-height: 1; color: #2F5694; margin-bottom: 14px;" data-count="{{{{ rs.countVal }}}}" data-from="{{{{ rs.from }}}}">{{{{ rs.value }}}}</div>
        <h3 style="{DISPLAY} font-size: 19px; line-height: 1.25; color: #223E6B; margin: 0 0 8px;">{{{{ rs.title }}}}</h3>
        <p style="font-size: 15px; line-height: 1.6; color: #333333; margin: 0;">{{{{ rs.body }}}}</p>
      </div>
    </sc-for>
  </div>
</section>

'''
i = t.index('<section id="perks"'); t = t[:i] + WHY + t[i:]
i = t.index('<section id="book"'); t = t[:i] + values + t[i:]
# company-wide stats: same set John signed off on the focus pages
t = sub(p.name, t, "\n      values: [", """
      reasons: [
        { value: '2019', title: 'Veterinary only, since 2019', body: 'We work with veterinary practices and nobody else, so we know what pet owners ask and what makes them call.' },
        { value: '< 2 hrs', from: '24', title: '2-hour response time', body: 'When you reach out, you hear back fast, not days later.' },
        { value: '< 6 hrs', from: '72', title: 'Website edits done fast', body: 'Hours, staff, services: changed the same day you ask.' },
        { value: '5.0★', title: 'Five-star Google rating', body: 'From the practices we serve.' }
      ].map(r => ({ ...r, countVal: r.from ? r.value : '', from: r.from || '' })),
      values: [""", 'about-reasons')
# hero photo: full column width on phones (was 76% / 340px), and less dead space under it
t = sub(p.name, t, '#top .sp-hero > div.vm-reveal { width: 76%; max-width: 340px; margin: 0 auto; }',
        '#top .sp-hero > div.vm-reveal { width: 100%; max-width: 440px; margin: 0 auto; }', 'about-hero-img')
p.write_text(t)
print('about.html: why us, core values moved, hero image')

# ------------------------------------------------------------------ 6. blog: cards link to the article layout; placeholder label
p = ROOT / 'blog.html'; t = p.read_text()
t = sub(p.name, t, '<a href="#" class="{{ po.cls }}" sc-camel-on-click="{{ po.noop }}" aria-label="{{ po.title }}">',
        '<a href="blog-post.html" class="{{ po.cls }}" aria-label="{{ po.title }}">', 'blog-card-link')
t = sub(p.name, t, '<div class="vm-blog-body">\n          <h3>{{ po.title }}</h3>', '<div class="vm-blog-body">\n          <div class="vm-blog-tag vm-sample">Sample post</div>\n          <h3>{{ po.title }}</h3>', 'blog-sample-tag')
t = sub(p.name, t, 'You\'ve reached the end. Demo content: 16 sample posts for layout review; the live blog will load from the CMS.',
        'Sample posts for layout review. Live articles will load from the CMS John\'s developer is connecting.', 'blog-end-note')
t = sub(p.name, t, '<p style="font-size: 19px; line-height: 1.6; color: #333333; margin: 0 0 26px; max-width: 620px;">Practical notes from a team that works only with veterinary practices: what\'s working in search, ads and social right now, with real numbers.</p>',
        '<p style="font-size: 19px; line-height: 1.6; color: #333333; margin: 0 0 26px; max-width: 620px;">Practical notes from a team that works only with veterinary practices: what\'s working in search, ads and social right now, with real numbers.</p>\n'
        '    <p class="vm-sample-note" style="font-family: \'polymath-text\', sans-serif; font-size: 13px; font-weight: 700; color: #B3541E; background: #FFF4E5; border: 1px solid #F3B23E; border-radius: 10px; padding: 8px 12px; display: inline-block; margin: 0 0 20px;">Preview: the posts below are sample content for layout review. Real articles load from the CMS.</p>', 'blog-note')
p.write_text(t)
print('blog.html: cards link to article layout, sample labels')

# ------------------------------------------------------------------ 7. new pages from the privacy page chrome
def new_page(fname, title, desc, path, body, noindex_note, extra_js=''):
    src = (ROOT / 'privacy-policy.html').read_text()
    a = src.find('<section id="top"'); b = src.find('<footer id="contact"'); assert a > 0 and b > a
    t = src[:a] + body + src[b:]
    t = re.sub(r'<title>[^<]*</title>', f'<title>{html.escape(title)}</title>', t, count=1)
    t = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(desc)}">', t, count=1)
    t = t.replace('https://www.veterinarymarketing.com/privacy-policy', f'https://www.veterinarymarketing.com/{path}')
    t = t.replace('Privacy &amp; Terms of Use | VeterinaryMarketing.com', html.escape(title))
    t = t.replace("const PAGE = { title: 'Privacy & Terms of Use | VeterinaryMarketing.com' };", f"const PAGE = {{ title: {json.dumps(title)} }};{extra_js}")
    t = t.replace('<meta name="robots" content="noindex, nofollow"><!-- PREVIEW ONLY: remove at launch -->',
                  f'<meta name="robots" content="noindex, nofollow"><!-- {noindex_note} -->')
    (ROOT / fname).write_text(t); print(fname, 'written', len(t))

PILL = "class=\"vm-pill\" style=\"display: inline-block; background: #F3B23E; color: #223E6B; font-family: 'polymath-text', sans-serif; font-size: 16px; font-weight: 800; padding: 15px 30px; border-radius: 999px; border: 2px solid #223E6B; box-shadow: 0 4px 0 #223E6B; transition: transform 0.2s, box-shadow 0.2s;\" style-hover=\"background: #FFBA2E; transform: translateY(-2px); box-shadow: 0 6px 0 #223E6B;\""

THANKS = f'''<section id="top" data-screen-label="Thank you" style="max-width: 1140px; margin: 0 auto; padding: 150px 32px 40px; box-sizing: border-box; position: relative;">
  <div aria-hidden="true" style="position: absolute; inset: 0; pointer-events: none; overflow: hidden;"><sc-for list="{{{{ pawsHero }}}}" as="bp" hint-placeholder-count="0"><span style="{{{{ bp.style }}}}"></span></sc-for></div>
  <div class="vm-thanks" style="position: relative; display: grid; grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr); gap: 56px; align-items: start;">
    <div>
      <div style="{EYEBROW} margin-bottom: 14px;">Request received</div>
      <h1 style="{DISPLAY} font-size: clamp(38px, 4.6vw, 62px); line-height: 1.04; color: #223E6B; margin: 0 0 18px; text-wrap: balance;">Thank you! We’ve got your information.</h1>
      <p style="font-size: 19px; line-height: 1.6; color: #333333; margin: 0 0 14px; max-width: 520px;">A real person from our team will reach out within two business hours. Want to skip the wait? Pick a time on John’s calendar and we’ll talk about your practice right away.</p>
      <p style="font-size: 16.5px; line-height: 1.6; color: #333333; margin: 0 0 28px; max-width: 520px;">In a hurry? Call <a href="tel:+18448440338" style="color: #2F5694; font-weight: 700;">(844) 844-0338</a>.</p>
      <div style="display: flex; flex-wrap: wrap; gap: 14px; align-items: center;">
        <a href="index.html" {PILL}>Back to the homepage →</a>
        <a href="reviews.html" style="color: #2F5694; font-family: 'polymath-text', sans-serif; font-size: 15px; font-weight: 700;">See client results</a>
      </div>
    </div>
    <div class="vm-reveal vm-cal-card" style="position: relative; background: #fff; border: 2px solid #223E6B; border-radius: 28px; box-shadow: 0 6px 0 #223E6B; padding: 28px 28px 24px; box-sizing: border-box;">
      <div style="{EYEBROW} margin-bottom: 8px;">Schedule a call</div>
      <h2 style="{DISPLAY} font-size: 24px; line-height: 1.2; color: #223E6B; margin: 0 0 16px;">Pick a time with John Donato</h2>
      <div class="vm-cal-slot">
        <!-- Start of HubSpot Meetings Embed -->
        <div class="meetings-wrap">
          <div class="meetings-iframe-container" data-src="https://meetings.hubspot.com/john-donato?embed=true"></div>
        </div>
        <!-- End of HubSpot Meetings Embed -->
      </div>
    </div>
  </div>
</section>

<section id="next" data-screen-label="What happens next" style="max-width: 1140px; margin: 0 auto; padding: 24px 32px 120px; box-sizing: border-box;">
  <div class="vm-reveal" style="text-align: center; margin-bottom: 36px;">
    <div style="{EYEBROW} margin-bottom: 16px;">What happens next</div>
    <h2 style="{DISPLAY} font-size: clamp(28px, 3vw, 40px); line-height: 1.1; color: #223E6B; margin: 0 auto; max-width: 640px; text-wrap: balance;">Three steps, no pressure</h2>
  </div>
  <div class="vm-next3" style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px;">
    <sc-for list="{{{{ nextSteps }}}}" as="ns" hint-placeholder-count="3">
      <div class="vm-reveal" style="border: 1px solid rgba(34,62,107,0.16); border-radius: 22px; padding: 28px 26px 30px; background: #fff;">
        <div style="{DISPLAY} font-size: 36px; line-height: 1; color: #749BEA; margin-bottom: 14px;">{{{{ ns.n }}}}</div>
        <h3 style="{DISPLAY} font-size: 19px; line-height: 1.25; color: #223E6B; margin: 0 0 8px;">{{{{ ns.title }}}}</h3>
        <p style="font-size: 15px; line-height: 1.6; color: #333333; margin: 0;">{{{{ ns.body }}}}</p>
      </div>
    </sc-for>
  </div>
</section>

'''
NEXT_JS = """
const NEXT_STEPS = [
  { n: '01', title: 'We review your practice', body: 'Website, Google Business Profile, reviews and the competition in your area, before we ever get on a call.' },
  { n: '02', title: 'A 20-minute conversation', body: 'What you want more of, what has not worked, and what we would do first. No slides, no pressure.' },
  { n: '03', title: 'A plan with numbers', body: 'A written recommendation with pricing. Month to month, no long-term contract.' }
];"""
new_page('thank-you.html', 'Thank You | VeterinaryMarketing.com',
         'Thanks for reaching out to VeterinaryMarketing.com. Pick a time on our calendar to talk about your practice.',
         'thank-you', THANKS, 'thank-you page: keep noindex at launch', NEXT_JS)
t = (ROOT / 'thank-you.html').read_text()
k = t.find('    return {'); assert k > 0
# privacy page's renderVals returns a flat object; add our list
t = t[:k] + "    const nextSteps = NEXT_STEPS;\n" + t[k:]
t = t.replace('    return {', '    return { nextSteps,', 1)
t = t.rstrip()[:-len('</body></html>')] + '''<script>
// HubSpot Meetings: the page body is rendered by the runtime, so load the embed script once the container exists.
(function () {
  var tries = 0;
  function go() {
    if (document.querySelector('.meetings-iframe-container')) {
      var s = document.createElement('script'); s.src = 'https://static.hsappstatic.net/MeetingsEmbed/ex/MeetingsEmbedCode.js'; s.async = true; document.body.appendChild(s);
    } else if (tries++ < 100) { setTimeout(go, 100); }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go); else go();
})();
</script>
</body></html>\n'''
(ROOT / 'thank-you.html').write_text(t)

# -- article layout for the CMS hookup
ARTICLE_P = "font-size: 17.5px; line-height: 1.75; color: #333333; margin: 0 0 18px; text-wrap: pretty;"
ARTICLE_H2 = f"{DISPLAY} font-size: 26px; line-height: 1.2; color: #223E6B; margin: 36px 0 12px;"
POST = f'''<section id="top" data-screen-label="Article hero" style="max-width: 1140px; margin: 0 auto; padding: 150px 32px 24px; box-sizing: border-box; position: relative;">
  <div aria-hidden="true" style="position: absolute; inset: 0; pointer-events: none; overflow: hidden;"><sc-for list="{{{{ pawsHero }}}}" as="bp" hint-placeholder-count="0"><span style="{{{{ bp.style }}}}"></span></sc-for></div>
  <div style="position: relative; max-width: 780px;">
    <p class="vm-sample-note" style="font-family: 'polymath-text', sans-serif; font-size: 13px; font-weight: 700; color: #B3541E; background: #FFF4E5; border: 1px solid #F3B23E; border-radius: 10px; padding: 8px 12px; display: inline-block; margin: 0 0 20px;">Preview: article layout template. Title, image, body and author load from the CMS.</p>
    <div style="{EYEBROW} margin-bottom: 14px;"><a href="index.html" style="color: #2F5694;" style-hover="color: #223E6B;">Home</a><span style="margin: 0 10px; opacity: 0.5;">/</span><a href="blog.html" style="color: #2F5694;" style-hover="color: #223E6B;">Blog</a><span style="margin: 0 10px; opacity: 0.5;">/</span><span>AEO</span></div>
    <h1 style="{DISPLAY} font-size: clamp(34px, 4.2vw, 56px); line-height: 1.06; color: #223E6B; margin: 0 0 18px; text-wrap: balance;">How AI search decides which vet to recommend (and how to be the one it picks)</h1>
    <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 12px 18px; font-family: 'polymath-text', sans-serif; font-size: 14px; color: #333333;">
      <div style="display: flex; align-items: center; gap: 10px;"><img src="assets/john-donato-8761d2a176.webp" alt="John Donato" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover;"><span><strong style="color: #223E6B;">John Donato</strong> · Founder</span></div>
      <span style="opacity: 0.6;">Oct 9, 2026 · 7 min read</span>
    </div>
  </div>
</section>

<section id="article" data-screen-label="Article" style="max-width: 1140px; margin: 0 auto; padding: 24px 32px 96px; box-sizing: border-box;">
  <div class="vm-article" style="display: grid; grid-template-columns: minmax(0, 780px) minmax(0, 1fr); gap: 56px; align-items: start;">
    <article>
      <div style="aspect-ratio: 16 / 9; border-radius: 22px; overflow: hidden; background: #D9E2F0; margin: 0 0 32px;"><img src="assets/focus-specialty-bac11be06c.webp" alt="" style="width: 100%; height: 100%; object-fit: cover; display: block;"></div>
      <p style="{ARTICLE_P} font-size: 20px; color: #223E6B;">ChatGPT and Google AI Overviews don’t rank pages the way Google does. They read, summarize and recommend. Here is what they actually look at, and the five things on your site that move the needle.</p>
      <p style="{ARTICLE_P}">This is sample body copy so the layout can be reviewed. The real article text, headings, images and pull quotes will come from the CMS. Paragraph width is capped at 780px for comfortable reading, with 17.5px type and generous line height.</p>
      <h2 style="{ARTICLE_H2}">What AI search reads first</h2>
      <p style="{ARTICLE_P}">Sample paragraph. Hours, services, location pages and review replies are being read as structured facts about your practice. The clearer they are, the more often you are the answer.</p>
      <blockquote style="margin: 28px 0; padding: 22px 26px; border-left: 4px solid #F3B23E; background: #F4F7FC; border-radius: 0 18px 18px 0; {DISPLAY} font-size: 22px; line-height: 1.35; color: #223E6B;">“Pet owners don’t search once. They ask, and the tool answers with one or two names.”</blockquote>
      <h2 style="{ARTICLE_H2}">Five things to fix this month</h2>
      <p style="{ARTICLE_P}">Sample paragraph. A numbered list, images and embedded video all have styles in this layout, so whatever the CMS sends renders consistently.</p>
      <ol style="{ARTICLE_P} padding-left: 22px;"><li>Service pages with real detail, one per service.</li><li>Google Business Profile filled in completely, including Q&amp;A.</li><li>Reviews answered, every one.</li><li>Structured data on every page.</li><li>A phone number that is impossible to miss.</li></ol>
      <div style="margin-top: 40px; padding: 28px 30px; border-radius: 22px; background: #2F5694; color: #fff;">
        <div style="{EYEBROW} color: #F3B23E; margin-bottom: 10px;">Next step</div>
        <h3 style="{DISPLAY} font-size: 24px; line-height: 1.2; color: #fff; margin: 0 0 10px;">Want this applied to your practice?</h3>
        <p style="font-size: 16px; line-height: 1.6; color: rgba(255,255,255,0.88); margin: 0 0 18px;">Tell us a little about your practice and a real person will get back to you within two hours.</p>
        <a href="#request-info" sc-camel-on-click="{{{{ openReq }}}}" {PILL}>Request more information →</a>
      </div>
    </article>
    <aside class="vm-article-side" style="position: sticky; top: 110px;">
      <div style="border: 1px solid rgba(34,62,107,0.16); border-radius: 22px; padding: 22px 22px 24px; background: #fff; margin-bottom: 18px;">
        <div style="{EYEBROW} margin-bottom: 12px;">In this article</div>
        <a href="#article" style="display: block; font-family: 'polymath-text', sans-serif; font-size: 14.5px; font-weight: 700; color: #223E6B; padding: 6px 0;">What AI search reads first</a>
        <a href="#article" style="display: block; font-family: 'polymath-text', sans-serif; font-size: 14.5px; font-weight: 700; color: #223E6B; padding: 6px 0;">Five things to fix this month</a>
      </div>
      <div style="border: 1px solid rgba(34,62,107,0.16); border-radius: 22px; padding: 22px 22px 24px; background: #F4F7FC;">
        <div style="{EYEBROW} margin-bottom: 12px;">Related</div>
        <a href="veterinary-aeo.html" style="display: block; font-family: 'polymath-text', sans-serif; font-size: 14.5px; font-weight: 700; color: #2F5694; padding: 6px 0;">Veterinary AEO →</a>
        <a href="veterinary-seo-marketing.html" style="display: block; font-family: 'polymath-text', sans-serif; font-size: 14.5px; font-weight: 700; color: #2F5694; padding: 6px 0;">Veterinary SEO →</a>
        <a href="blog.html" style="display: block; font-family: 'polymath-text', sans-serif; font-size: 14.5px; font-weight: 700; color: #2F5694; padding: 6px 0;">All articles →</a>
      </div>
    </aside>
  </div>
</section>

'''
new_page('blog-post.html', 'Article | Veterinary Marketing Blog | VeterinaryMarketing.com',
         'Article layout template for the VeterinaryMarketing.com blog.', 'blog/article', POST, 'article template: CMS will set robots per post')

# ------------------------------------------------------------------ 8. CSS
css = ROOT / 'assets/vm-r2.css'; c = css.read_text()
assert '---- r7' not in c
c += '''
/* ---- r7 (10/17 client edits, build 11) ---- */
/* Footer: partner badges + animated logo + bottom row */
.vm-badges { display: flex; align-items: center; gap: 18px; margin-bottom: 22px; }
.vm-badges img { height: 54px; width: auto; display: block; }
.vm-badges img[alt="Meta Business Partner"] { height: 40px; }
.vm-foot-logo { object-fit: contain; object-position: left center; }
@media (max-width: 760px) {
  .vm-foot-bottom { flex-direction: column; align-items: flex-start !important; gap: 18px !important; }
  .vm-foot-bottom img { height: 44px !important; }
  .vm-badges { gap: 14px; }
  .vm-badges img { height: 46px; }
  .vm-badges img[alt="Meta Business Partner"] { height: 34px; }
}
/* Homepage hero: credibility logos stay on one line on phones */
@media (max-width: 560px) {
  .vm-platforms-hero { flex-wrap: nowrap !important; justify-content: center; gap: 0 12px !important; }
  .vm-platforms-hero img { height: 15px !important; }
  .vm-platforms-hero img[alt="Google Ads"] { height: 19px !important; }
}
@media (max-width: 380px) { .vm-platforms-hero img { height: 13px !important; } .vm-platforms-hero img[alt="Google Ads"] { height: 17px !important; } .vm-platforms-hero { gap: 0 9px !important; } }
/* Service + focus heroes on phones: tag only, one short line, then CTA / call / logos / image */
.vm-hero-short { display: none; }
@media (max-width: 760px) {
  .vm-crumb > a, .vm-crumb > a + span { display: none; }
  .vm-hero-sub, .vm-hero-intro ~ .vm-hero-intro, .vm-hero-lead, .vm-hero-long { display: none !important; }
  .vm-hero-short { display: block; }
  .vm-hero-intro, .vm-hero-short { font-size: 17px !important; margin-bottom: 22px !important; }
  .sp-hero-ctas .vm-platforms, .fp-hero-ctas .vm-platforms { flex-wrap: nowrap !important; gap: 0 12px !important; justify-content: center; }
  .sp-hero-ctas .vm-platforms img, .fp-hero-ctas .vm-platforms img { height: 16px !important; }
  .sp-hero-ctas .vm-platforms img[alt="Google Ads"], .fp-hero-ctas .vm-platforms img[alt="Google Ads"] { height: 20px !important; }
  /* (J1) focus pages: gap between "Read all our Google reviews" and Why Us cut by ~70% */
  #reviews.fp-section { padding-bottom: 20px !important; }
  #reviews.fp-section > .vm-reveal:last-child { margin-top: 24px !important; }
  #why.fp-section { padding-top: 28px !important; }
  /* Why Us headline: break after "Veterinary", never mid-word */
  #why h2 { overflow-wrap: normal !important; word-break: normal !important; hyphens: manual; }
  /* (J3) service pages: tighter run-in to the Testimonial band */
  #story { padding-top: 64px !important; padding-bottom: 64px !important; }
  /* (J4/6) About: hero photo fills the column, Why Us sits right under it */
  #top .sp-hero { padding-bottom: 40px !important; }
  #why.sp-section { padding-top: 24px !important; }
  /* Request Info sheet: keep the Next / Submit row clear of Safari and in-app browser toolbars */
  [role="dialog"][aria-label="Request information"] > div { padding-bottom: calc(96px + env(safe-area-inset-bottom, 0px)) !important; }
}
/* Thank-you + article pages */
@media (max-width: 900px) { .vm-thanks { grid-template-columns: 1fr !important; gap: 36px !important; } .vm-article { grid-template-columns: 1fr !important; } .vm-article-side { position: static !important; } .vm-next3 { grid-template-columns: 1fr !important; } }
/* HubSpot Meetings embed (John's code, 10/21) */
.meetings-wrap { height: auto !important; min-height: 0 !important; padding-bottom: 0 !important; margin-bottom: 0 !important; }
.meetings-iframe-container { width: 100%; height: auto !important; overflow: visible; }
.meetings-iframe-container iframe { width: 100% !important; border: 0; display: block; border-radius: 18px; }
@media (max-width: 767px) { .meetings-iframe-container { min-height: 600px; overflow: auto; -webkit-overflow-scrolling: touch; } .meetings-iframe-container iframe { min-height: 600px; } }
.vm-sample { color: #B3541E; letter-spacing: 0; text-transform: none; font-weight: 700; }
'''
css.write_text(c)
print('vm-r2.css: r7 block')

# ------------------------------------------------------------------ 9. cache-bust
n = 0
for p in sorted(ROOT.glob('*.html')):
    t = p.read_text(); t2 = re.sub(r'(vm-r2\.(?:css|js))\?v=\d+', r'\1?v=12', t)
    if t2 != t: p.write_text(t2); n += 1
print(f'{n} pages cache-busted to v=12')
