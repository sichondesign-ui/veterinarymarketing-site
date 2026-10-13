#!/usr/bin/env python3
"""Round 2: new Blog hub page (demo content, 16 posts, infinite scroll) built on the conferences page chrome."""
import re, sys, json, pathlib
ROOT = pathlib.Path(sys.argv[1]); AM = json.load(open('tools/assetmap.json'))
src = (ROOT / 'conferences.html').read_text()

POSTS = [
 ("AEO", "How AI search decides which vet to recommend (and how to be the one it picks)", "ChatGPT and Google AI Overviews don't rank pages the way Google does. Here's what they actually read, and the five things on your site that move the needle.", "Oct 9, 2026", "7 min", "focus-specialty-bac11be06c.webp"),
 ("SEO", "“Vet near me” is 11 searches. Here's how to win all of them.", "Pet owners don't search once. They search eleven different ways, from “emergency vet open now” to “cat dentist.” A page for each one is how you show up.", "Oct 2, 2026", "6 min", "focus-small-animal-7cbc7fa286.webp"),
 ("Google Ads", "Why your cost per click dropped 40% when we split the campaigns", "One campaign for everything is the most common Google Ads mistake we see in veterinary accounts. The fix is boring and it works.", "Sep 25, 2026", "5 min", "focus-urgent-0026c1194a.webp"),
 ("Practice Growth", "The number most practices never look at: conversion rate", "Marketing can bring in 50 new callers. If 20 book, that's not a marketing problem. How to measure it, and what to do once you can see it.", "Sep 18, 2026", "8 min", "gallery-7-463c8f254b.webp"),
 ("Websites", "A website in 25 days: what happens each week", "Wireframes, design, Webflow build, launch. Here's the actual calendar, and where practices usually slow it down.", "Sep 11, 2026", "4 min", "focus-startup-052158f88b.webp"),
 ("Social", "Posts that get a dental booked, not just a like", "Educational content that explains why a dental needs anesthesia converts better than a cute photo. Examples from three practices.", "Sep 4, 2026", "5 min", "gallery-2-0df849bef3.webp"),
 ("AEO", "Your Google Business Profile is now an AI data source", "Hours, services, Q&A and review replies are being read by AI tools. Here's how to fill them in so you get recommended.", "Aug 28, 2026", "6 min", "focus-emergency-6239ff858a.webp"),
 ("Practice Growth", "Opening a startup practice? Start marketing 90 days before the doors open", "A pre-launch sign-up list, a brand that's ready on day one, and the first 100 clients. What 30+ startup launches taught us.", "Aug 21, 2026", "7 min", "focus-mobile-0c2f527cfe.webp"),
 ("SEO", "Keyword cramming is costing you rankings", "If every page on your site says “veterinarian in [city]” twelve times, Google notices. What to write instead.", "Aug 14, 2026", "4 min", "gallery-10-2f4fa2dd43.webp"),
 ("Google Ads", "Capacity-aware ads for emergency hospitals", "Run ads when the lobby has room, pause them when you're on diversion. How we set it up, and the missed-call data that drives it.", "Aug 7, 2026", "6 min", "focus-equine-59bae4679a.webp"),
 ("Websites", "Please stop putting a “Book Appointment” button on your ER website", "Panicked owners don't book. They call and they drive. Why the template button hurts ERs, and what belongs above the fold instead.", "Jul 31, 2026", "5 min", "focus-multi-dd813239dd.webp"),
 ("Social", "What a month of social posting looks like for a small animal practice", "Dental month, parasite season, senior screenings. A real monthly calendar, post by post.", "Jul 24, 2026", "5 min", "gallery-3-029a9bb639.webp"),
 ("Practice Growth", "Direct mail still works, if it's tracked", "A postcard to someone who visited your site but didn't book, within 3 days. Response rates from the last 12 months.", "Jul 17, 2026", "4 min", "gallery-4-1dee894dee.webp"),
 ("AEO", "ChatGPT Ads are here. Should your practice be first?", "Early inventory, local targeting by zip code, and what the first veterinary campaigns are seeing.", "Jul 10, 2026", "6 min", AM["conf2"]),
 ("SEO", "Every page ranked: the service-page strategy", "Your homepage can't rank for everything. Why each service needs its own page, and how we link them so they lift each other.", "Jul 3, 2026", "6 min", AM["conf1"]),
 ("Practice Growth", "What we learned speaking to 400 practice managers this year", "The questions that came up at every conference, and the answers that changed how we work.", "Jun 26, 2026", "5 min", AM["conf3"]),
]

posts_js = json.dumps([{"tag": a, "title": b, "excerpt": c, "date": d, "read": e, "img": "assets/" + f} for a, b, c, d, e, f in POSTS], ensure_ascii=False)

TEMPLATE = '''<section id="top" data-screen-label="Blog hero" style="max-width: 1140px; margin: 0 auto; padding: 150px 32px 40px; box-sizing: border-box; position: relative;">
  <div aria-hidden="true" style="position: absolute; inset: 0; pointer-events: none; overflow: hidden;"><sc-for list="{{ pawsHero }}" as="bp" hint-placeholder-count="0"><span style="{{ bp.style }}"></span></sc-for></div>
  <div style="position: relative; max-width: 760px;">
    <div style="font-family: 'polymath-text', sans-serif; font-size: 13px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: #2F5694; margin-bottom: 14px;"><a href="index.html" style="color: #2F5694;" style-hover="color: #223E6B;">Home</a><span style="margin: 0 10px; opacity: 0.5;">/</span><span>Blog</span></div>
    <h1 style="font-family: var(--vm-display); font-weight: var(--vm-display-weight, 800); font-size: clamp(38px, 4.6vw, 62px); line-height: 1.04; color: #223E6B; margin: 0 0 18px; text-wrap: balance;">Veterinary marketing, explained</h1>
    <p style="font-size: 19px; line-height: 1.6; color: #333333; margin: 0 0 26px; max-width: 620px;">Practical notes from a team that works only with veterinary practices: what's working in search, ads and social right now, with real numbers.</p>
    <div class="vm-blog-tags" style="display: flex; flex-wrap: wrap; gap: 8px;">
      <sc-for list="{{ tags }}" as="tg" hint-placeholder-count="6"><span style="{{ tg.style }}">{{ tg.label }}</span></sc-for>
    </div>
  </div>
</section>

<section id="posts" data-screen-label="Posts" style="max-width: 1140px; margin: 0 auto; padding: 24px 32px 96px; box-sizing: border-box; position: relative;">
  <div class="vm-blog-grid">
    <sc-for list="{{ posts }}" as="po" hint-placeholder-count="7">
      <a href="#" class="{{ po.cls }}" sc-camel-on-click="{{ po.noop }}" aria-label="{{ po.title }}">
        <div class="vm-blog-thumb"><img src="{{ po.img }}" alt="" loading="lazy"></div>
        <div class="vm-blog-body">
          <div class="vm-blog-tag">{{ po.tag }}</div>
          <h3>{{ po.title }}</h3>
          <p>{{ po.excerpt }}</p>
          <div class="vm-blog-meta">{{ po.date }} · {{ po.read }} read</div>
        </div>
      </a>
    </sc-for>
  </div>
  <sc-if value="{{ loading }}" hint-placeholder-val="{{ false }}"><div class="vm-blog-loading" aria-live="polite"><span class="vm-blog-dot"></span><span class="vm-blog-dot"></span><span class="vm-blog-dot"></span><div style="margin-top: 10px;">Loading more posts…</div></div></sc-if>
  <sc-if value="{{ hasMore }}" hint-placeholder-val="{{ true }}"><div class="vm-blog-sentinel" aria-hidden="true"></div><div style="text-align: center; margin-top: 36px;"><button type="button" sc-camel-on-click="{{ loadMore }}" class="vm-pill" style="background: #fff; color: #223E6B; font-family: 'polymath-text', sans-serif; font-size: 15px; font-weight: 800; padding: 14px 28px; border-radius: 999px; border: 2px solid #223E6B; box-shadow: 0 4px 0 #223E6B; cursor: pointer;" style-hover="background: #EDF7FC; transform: translateY(-2px); box-shadow: 0 6px 0 #223E6B;">Load more posts</button></div></sc-if>
  <sc-if value="{{ allShown }}" hint-placeholder-val="{{ false }}"><p style="text-align: center; margin: 40px 0 0; font-family: 'polymath-text', sans-serif; font-size: 14px; color: #333333; opacity: 0.7;">You've reached the end. Demo content: 16 sample posts for layout review; the live blog will load from the CMS.</p></sc-if>
</section>

<section id="book" data-screen-label="CTA" style="max-width: 1140px; margin: 0 auto; padding: 0 32px 104px; box-sizing: border-box;">
  <div class="sp-cta-card vm-reveal" style="position: relative; background: #2F5694; border-radius: 32px; padding: 72px 64px; text-align: center; color: #fff; overflow: hidden;">
    <div style="font-family: 'polymath-text', sans-serif; font-size: 13px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: #F3B23E; margin-bottom: 16px;">Next step</div>
    <h2 style="font-family: var(--vm-display); font-weight: var(--vm-display-weight, 800); font-size: clamp(30px, 3.4vw, 44px); line-height: 1.1; color: #fff; margin: 0 auto 16px; max-width: 640px; text-wrap: balance;">Want this applied to your practice?</h2>
    <p style="font-size: 18px; line-height: 1.6; color: rgba(255,255,255,0.88); margin: 0 auto 28px; max-width: 560px;">Tell us a little about your practice and a real person will get back to you within two hours.</p>
    <div style="display: flex; flex-wrap: wrap; gap: 14px; justify-content: center; align-items: center;">
      <a href="#request-info" sc-camel-on-click="{{ openReq }}" class="vm-pill" style="display: inline-block; background: #F3B23E; color: #223E6B; font-family: 'polymath-text', sans-serif; font-size: 16px; font-weight: 800; padding: 15px 30px; border-radius: 999px; border: 2px solid #223E6B; box-shadow: 0 4px 0 #223E6B; transition: transform 0.2s, box-shadow 0.2s;" style-hover="background: #FFBA2E; transform: translateY(-2px); box-shadow: 0 6px 0 #223E6B;">Request more information →</a>
      <a href="tel:+18448440338" style="color: #fff; font-family: 'polymath-text', sans-serif; font-size: 15px; font-weight: 700;">Or call us directly: (844) 844-0338</a>
    </div>
  </div>
</section>

'''

t = src
a = t.find('<section id="top"'); b = t.find('<footer id="contact"'); assert a > 0 and b > a
t = t[:a] + TEMPLATE + t[b:]
t = t.replace('<title>Bundled Page</title>', '<title>Veterinary Marketing Blog | VeterinaryMarketing.com</title>')
t = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Practical veterinary marketing advice from VeterinaryMarketing.com: SEO, AEO, Google Ads, ChatGPT Ads, social media and websites for veterinary practices.">', t, count=1)
t = t.replace("const PAGE = { title: 'Veterinary Marketing Speaker | John Donato | VeterinaryMarketing.com' };", "const PAGE = { title: 'Veterinary Marketing Blog | VeterinaryMarketing.com' };")
# state + infinite scroll
t = t.replace("openMenu: null, submitted: false };", "openMenu: null, submitted: false, shown: 7, loading: false };", 1)
t = t.replace("    document.querySelectorAll('.vm-reveal').forEach(el => this.revealObserver.observe(el));\n  }\n  componentWillUnmount() {",
"""    document.querySelectorAll('.vm-reveal').forEach(el => this.revealObserver.observe(el));
    this.onBlogScroll = () => {
      const s = document.querySelector('.vm-blog-sentinel');
      if (!s || this.state.loading || this.state.shown >= BLOG_POSTS.length) return;
      if (s.getBoundingClientRect().top < window.innerHeight + 240) this.loadMore();
    };
    window.addEventListener('scroll', this.onBlogScroll, { passive: true });
    setTimeout(this.onBlogScroll, 400);
  }
  loadMore() {
    if (this.state.loading || this.state.shown >= BLOG_POSTS.length) return;
    this.setState({ loading: true });
    setTimeout(() => this.setState(s => ({ loading: false, shown: Math.min(BLOG_POSTS.length, s.shown + 6) })), 700);
  }
  componentDidUpdate() { if (this.revealObserver) document.querySelectorAll('.vm-reveal:not(.vm-in)').forEach(el => this.revealObserver.observe(el)); }
  componentWillUnmount() { window.removeEventListener('scroll', this.onBlogScroll);""", 1)
assert 'loadMore()' in t
# render values: posts etc. replace the conference-specific keys
k = t.find('    return { ...chrome,'); e = t.find('      submitted: this.state.submitted', k); assert k > 0 and e > k
tagColors = {"AEO": "#2F5694", "SEO": "#0B8043", "Google Ads": "#B3541E", "Practice Growth": "#223E6B", "Websites": "#7B4FA6", "Social": "#C2185B"}
vals = """    return { ...chrome,
      tags: %s.map(l => ({ label: l, style: 'font-family: \\'polymath-text\\', sans-serif; font-size: 12.5px; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; color: #223E6B; background: #fff; border: 1.5px solid rgba(34,62,107,0.18); border-radius: 999px; padding: 7px 13px;' })),
      posts: BLOG_POSTS.slice(0, this.state.shown).map((p, i) => ({ ...p, cls: 'vm-blog-card vm-reveal' + (i === 0 ? ' vm-blog-featured' : ''), noop: (e) => e.preventDefault() })),
      loading: !!this.state.loading,
      hasMore: this.state.shown < BLOG_POSTS.length,
      allShown: this.state.shown >= BLOG_POSTS.length && !this.state.loading,
      loadMore: () => this.loadMore(),
""" % json.dumps(list(tagColors))
t = t[:k] + vals + t[e:]
t = t.replace("const PAGE = {", "const BLOG_POSTS = " + posts_js + ";\nconst PAGE = {", 1)
# drop conferences-only helpers that are no longer referenced? leave them; harmless. Hero paws: pawsHero is provided by chrome? check
if 'pawsHero' not in t[:k]: pass
(ROOT / 'blog.html').write_text(t)
print('blog.html written', len(t))
