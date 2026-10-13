#!/usr/bin/env python3
"""Round 2, part 3: page-specific fixes (About, Contact, Reviews, Conferences, Specialty, Free Analysis, modal note)."""
import re, sys, json, pathlib
ROOT = pathlib.Path(sys.argv[1]); AM = json.load(open('tools/assetmap.json'))
G_SVG = '<svg width="22" height="22" viewBox="0 0 48 48" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.1H42V20H24v8h11.3C33.7 32.7 29.3 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.9 1.2 8 3l5.7-5.7C34.3 6.1 29.4 4 24 4 13 4 4 13 4 24s9 20 20 20 20-9 20-20c0-1.3-.1-2.7-.4-3.9z"></path><path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 18.9 12 24 12c3.1 0 5.9 1.2 8 3l5.7-5.7C34.3 6.1 29.4 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"></path><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.3 0-9.7-3.4-11.3-8.1l-6.5 5C9.5 39.6 16.2 44 24 44z"></path><path fill="#1976D2" d="M43.6 20.1H42V20H24v8h11.3c-.8 2.2-2.2 4.1-4.1 5.5l6.2 5.2C36.9 39.2 44 34 44 24c0-1.3-.1-2.7-.4-3.9z"></path></svg>'

def edit(name, fn):
    p = ROOT / name; t = p.read_text(); n = fn(t); assert n != t, name + ': no change'; p.write_text(n); print('ok', name)

def must(t, old, new, count=1):
    assert t.count(old) == count, (old[:70], t.count(old)); return t.replace(old, new)

# ---------- About ----------
def about(t):
    # perks: 7 cards in a 3-col grid -> center the orphan on the last row
    t = must(t, '  <link rel="stylesheet" href="assets/vm-r2.css">', '  <style>.ab-perks > :last-child:nth-child(3n + 1) { grid-column: 2; }\n    @media (max-width: 960px) { .ab-perks > :last-child:nth-child(3n + 1) { grid-column: auto; } }</style>\n  <link rel="stylesheet" href="assets/vm-r2.css">')
    # history photo: the coffee-walk crop cuts heads off at the source; use the kitchen-table photo instead
    t = must(t, '<img src="assets/gallery-1-b7c998f76f.webp" alt="Two VeterinaryMarketing.com team members walking with coffee outside the office"',
             '<img src="assets/gallery-7-463c8f254b.webp" alt="Two VeterinaryMarketing.com team members working together at a laptop"')
    # office gallery: equal tile heights (was 260/190 staggered -> uneven gutters)
    t = must(t, "height: tall ? '260px' : '190px'", "height: '210px'")
    return t
edit('about.html', about)

# ---------- Contact: simple form + SMS opt-in ----------
def contact(t):
    m = re.search(r'(          <form sc-camel-on-submit="\{\{ onContactSubmit \}\}" class="ct-form"[^>]*>\n)(.*?)(            <div style="[^"]*">\n              <button type="submit")', t, re.S)
    assert m, 'contact form'
    lab = re.search(r'<label style="([^"]*)">What’s your name\?<input name="name" type="text" required="required" style="([^"]*)">', t); assert lab
    LS, IS = lab.group(1), lab.group(2)
    def field(label, name, typ, req=True, auto=''):
        rq = ' required="required"' if req else ''
        ac = (' autocomplete="' + auto + '"') if auto else ''
        return '            <label style="' + LS + '">' + label + '<input name="' + name + '" type="' + typ + '"' + rq + ac + ' style="' + IS + '"></label>\n'
    fields = (field('First name', 'first_name', 'text', auto='given-name') + field('Last name', 'last_name', 'text', auto='family-name') +
              field('Email', 'email', 'email', auto='email') + field('Phone number', 'phone', 'tel', auto='tel') +
              field('Practice name', 'practice_name', 'text', auto='organization') +
              '            <label style="grid-column: 1 / -1; display: flex; align-items: flex-start; gap: 12px; font-family: \'polymath-text\', sans-serif; font-size: 13.5px; line-height: 1.5; color: #333333; font-weight: 500; cursor: pointer;">'
              '<input name="sms_opt_in" type="checkbox" value="yes" style="margin-top: 3px; width: 18px; height: 18px; flex: 0 0 auto; accent-color: #2F5694;">'
              '<span>I agree to receive SMS &amp; emails from VeterinaryMarketing.com. Msg &amp; data rates may apply. Reply STOP to opt out of SMS. See <a href="https://www.veterinarymarketing.com/privacy-policy" target="_blank" rel="noopener" style="color: #2F5694; font-weight: 700; text-decoration: underline; text-underline-offset: 2px;">Privacy Policy</a> &amp; <a href="https://www.veterinarymarketing.com/privacy-policy" target="_blank" rel="noopener" style="color: #2F5694; font-weight: 700; text-decoration: underline; text-underline-offset: 2px;">Terms</a>.</span></label>\n')
    t = t[:m.start(2)] + fields + t[m.end(2):]
    t = must(t, '>Tell us a little about your practice</h2>\n          <form sc-camel-on-submit="{{ onContactSubmit }}"', '>Send us a message</h2>\n          <form sc-camel-on-submit="{{ onContactSubmit }}"')
    t = t.replace('>Request information →</button>\n              <div', '>Send →</button>\n              <div', 1)
    return t
edit('contact-us.html', contact)

# ---------- Reviews: Google logo lock-up, no counts ----------
def reviews(t):
    t = must(t, '<div style="font-family: \'polymath-text\', sans-serif; font-size: 13px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: #2F5694; margin-bottom: 16px;">Google reviews</div>',
             '<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 16px;">' + G_SVG + '<span style="font-family: \'polymath-text\', sans-serif; font-size: 13px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: #2F5694;">Google reviews</span></div>')
    # hero rating card: G mark above the score
    m = re.search(r'(<div style="[^"]*">)Google Reviews(</div>\s*<div style="[^"]*">)5\.0(</div>)', t); assert m, 'reviews hero card'
    t = t[:m.start()] + '<div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 6px;">' + G_SVG.replace('width="22" height="22"', 'width="30" height="30"') + '<span style="font-family: \'polymath-text\', sans-serif; font-size: 14px; font-weight: 800; letter-spacing: 0.14em; text-transform: uppercase;">Google Reviews</span></div>' + m.group(2) + '5.0' + m.group(3) + t[m.end():]
    return t
edit('reviews.html', reviews)

# ---------- Conferences: collage, stat fix, headshot ----------
def conferences(t):
    t = must(t, "{ value: 'Mon', title: 'Practical, not theoretical'", "{ value: '100s', title: 'Practical, not theoretical'")
    t = t.replace("body: 'Attendees leave with steps they can use right away.'", "body: 'Of practices supported. Attendees leave with steps they can use right away.'", 1)
    t = must(t, '<img src="assets/john-donato-dbd9c335ff.jpg" alt="John Donato, CEO and Founder of VeterinaryMarketing.com" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover;',
             f'<img src="assets/{AM["john"]}" alt="John Donato, CEO and Founder of VeterinaryMarketing.com" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: center 18%;')
    collage = f'''
<section id="on-the-road" data-screen-label="Conference photos" class="sp-section" style="max-width: 1140px; margin: 0 auto; padding: 24px 32px 96px; box-sizing: border-box; position: relative;">
  <div class="sp-sechead vm-reveal" style="display: flex; align-items: flex-end; justify-content: space-between; gap: 40px; margin-bottom: 36px;">
    <div>
      <div style="font-family: 'polymath-text', sans-serif; font-size: 13px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: #2F5694; margin-bottom: 16px;">On the road</div>
      <h2 style="font-family: var(--vm-display); font-weight: var(--vm-display-weight, 800); font-size: clamp(30px, 3.2vw, 42px); line-height: 1.1; color: #223E6B; margin: 0; max-width: 560px; text-wrap: balance;">From the stage to the exhibit hall</h2>
    </div>
    <p style="font-size: 17px; line-height: 1.6; color: #333333; max-width: 380px; margin: 0 0 6px;">A few moments from recent veterinary conferences. New photos get added after every event.</p>
  </div>
  <div class="vm-collage vm-reveal">
    <div><img src="assets/{AM["conf4"]}" alt="John Donato speaking at a veterinary conference" loading="lazy"></div>
    <div><img src="assets/{AM["conf1"]}" alt="John Donato presenting to veterinary professionals" loading="lazy"></div>
    <div><img src="assets/{AM["conf2"]}" alt="Conference session on veterinary marketing" loading="lazy"></div>
    <div><img src="assets/{AM["conf3"]}" alt="John Donato on stage at a veterinary speaking engagement" loading="lazy"></div>
  </div>
</section>
'''
    t = must(t, '\n<section id="meet"', collage + '\n<section id="meet"')
    return t
edit('conferences.html', conferences)

# ---------- Specialty: hero headline rebalanced ----------
def specialty(t):
    t = must(t, '>Veterinary specialist marketing for practices that aren\'t like anyone else</h1>', '>Specialty veterinary marketing for practices unlike any other</h1>')
    return t
edit('veterinary-specialty-practice-marketing.html', specialty)

# ---------- Free Competitive Analysis: Request Info outnumbers the wizard ----------
def fa(t):
    # the hero already has "Schedule a call" (wizard, new tab); add a Request Info pill beside it
    m = re.search(r'(<a href="https://wizard\.veterinarymarketing\.com/your-veterinary-practice" target="_blank" rel="noopener" class="vm-pill" style="([^"]*)"[^>]*>Schedule a call →</a>)', t); assert m, 'fa hero cta'
    st = m.group(2).replace('background: #F3B23E;', 'background: #fff;')
    t = t[:m.end()] + '\n        <a href="#request-info" sc-camel-on-click="{{ openReq }}" class="vm-pill" style="' + st + '" style-hover="background: #EDF7FC; transform: translateY(-2px); box-shadow: 0 6px 0 #223E6B;">Request information →</a>' + t[m.end():]
    return t
edit('free-veterinary-marketing-analysis.html', fa)
