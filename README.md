# VeterinaryMarketing.com – Site Preview

Static preview build of the new veterinarymarketing.com. Plain HTML pages with shared, content-hashed assets in `assets/`
(unpacked from the Claude Design single-file export), so the folder can be served by GitHub Pages, Netlify or any static host with no build step.

## Hosting on GitHub Pages
1. Push this folder's contents to the repository root (or a `docs/` folder).
2. Settings → Pages → Deploy from a branch → pick the branch (and `/` or `/docs`).
3. The site is live at `https://<user>.github.io/<repo>/`. `index.html` is the homepage; every other page is linked
   from the header and footer.

Testimonial videos (YouTube / Vimeo) play in the on-page lightbox once hosted over https. They will not play when a
file is double-clicked from disk; that is a YouTube rule for `file://` pages, not a bug.

## Pages (22)
| Page | File | Final URL |
| --- | --- | --- |
| Homepage | `index.html` | `/` |
| About Us | `about.html` | `/about` |
| Reviews & Testimonials | `reviews.html` | `/reviews` |
| Contact Us | `contact-us.html` | `/contact-us` |
| Conferences & Speaking | `conferences.html` | `/conferences` |
| Free Competitive Analysis | `free-veterinary-marketing-analysis.html` | `/free-veterinary-marketing-analysis` |
| Services: Veterinary Websites | `veterinary-websites.html` | `/services/veterinary-websites` |
| Services: Veterinary SEO | `veterinary-seo-marketing.html` | `/services/veterinary-seo-marketing` |
| Services: Veterinary AEO | `veterinary-aeo.html` | `/services/veterinary-aeo` |
| Services: Google Ads / PPC | `veterinary-ppc-marketing.html` | `/services/veterinary-ppc-marketing` |
| Services: ChatGPT Ads | `veterinary-chatgpt-ads.html` | `/services/veterinary-chatgpt-ads` |
| Services: Social Media Ads | `veterinary-social-media-marketing.html` | `/services/veterinary-social-media-marketing` |
| Services: Social Media Posting | `veterinary-social-media-posting.html` | `/services/veterinary-social-media-posting` |
| Services: Direct Mail | `veterinary-direct-mail-marketing.html` | `/services/veterinary-direct-mail-marketing` |
| Focus: Small Animal General Practice | `small-animal-practice-veterinary-marketing.html` | `/areas-of-focus/small-animal-practice-veterinary-marketing` |
| Focus: Specialty Practice | `veterinary-specialty-practice-marketing.html` | `/areas-of-focus/veterinary-specialty-practice-marketing` |
| Focus: Emergency Care | `emergency-vet-practice-marketing.html` | `/areas-of-focus/emergency-vet-practice-marketing` |
| Focus: Urgent Care | `urgent-care-animal-practice-veterinary-marketing.html` | `/areas-of-focus/urgent-care-animal-practice-veterinary-marketing` |
| Focus: Startup Practice Support | `startup-practice-veterinary-marketing.html` | `/areas-of-focus/startup-practice-veterinary-marketing` |
| Focus: Mobile Clinics | `mobile-practice-veterinary-marketing-strategies.html` | `/areas-of-focus/mobile-practice-veterinary-marketing-strategies` |
| Focus: Multi-Location Practices | `multi-location-practice-veterinary-marketing-strategies.html` | `/areas-of-focus/multi-location-practice-veterinary-marketing-strategies` |
| Focus: Equine Practices | `equine-veterinary-marketing.html` | `/areas-of-focus/equine-veterinary-marketing` |

File names are flat so the folder works from any host path; focus pages use the slugs John confirmed on 10/07.

## Forms and embeds (production to-dos)
- **Request Info** (header, footer and in-copy buttons) opens an on-page modal with the same 9 questions as the live
  HubSpot form, in 3 steps. For production, post to HubSpot (Forms API or embed) from inside this modal; no separate page.
- **Contact Us** form uses the same 9 fields in a single card. Wire to the same HubSpot form.
- **Free Competitive Analysis** CTAs go to the analysis tool: `https://wizard.veterinarymarketing.com/your-veterinary-practice`.
  The analysis page's form hands off to the same URL.
- **Conferences speaking request** is a demo form; John will supply a HubSpot form.
- Blog and Privacy Policy are now pages in this build (`blog.html` demo content, `privacy-policy.html` live text). Case Studies is retired (redirect `/case-studies` → `/reviews`).
- Redirect `/services/veterinary-copy-writing` → `/services/veterinary-websites`.

## Build notes
- This is the review build: each page is self-contained (fonts and images embedded), 8-18 MB per page. The production
  build will be unpacked: shared /assets, no unpack loader, ~140 KB HTML per page.
- Adobe Fonts (polymath, visby) are embedded here for review only. Production must load them from the client's Typekit
  kit (use.typekit.net) per the license; need the kit ID from John.
- Forms are front-end only. Production needs a submit target (HubSpot Forms API) and a spam measure (reCAPTCHA or Turnstile).

## Open items for John
- Screen videos for the MacBook / iMac / iPhone frames on the service pages (Websites ×2, Google Ads, AEO, Social Media Ads, Social Media Posting). Labeled device placeholders are in place.
- Social Media Ads page has no graphics yet; device placeholders only.
- Request Info modal: the image you referenced in the review was not in the content folder. Send it and it goes in the modal's intro panel.
- Blog page shows 16 demo posts for layout review only. The live blog loads from the CMS.
- Artwork for the Veterinary AEO, ChatGPT Ads and Social Media Posting service cards now uses the 10/13 graphics.
- A larger headshot of John is now on the Conferences page (1000px).
- Confirm founding year: the About page history photo carries a "2019 · veterinary only, ever since" badge that isn't in the copy doc.
- Reviews page shows every written Google review (7 truncated in the export link out to Google) plus 11 videos. Review counts are no longer shown anywhere, so nothing to hand-update.

## Launch checklist (not live yet; queued)
Done in this build: favicon set (`favicon.ico`, `favicon.svg`, apple-touch, manifest icons), Open Graph + Twitter cards with a default share image (`assets/og-default.jpg`), canonical URLs pointing at the final veterinarymarketing.com paths, `lang="en"`, theme-color, `robots.txt`, `sitemap.xml`, branded `404.html`.

**Preview guard — remove at launch:** every page carries `<meta name="robots" content="noindex, nofollow">` and `robots.txt` is `Disallow: /` so the GitHub preview is never indexed. Both are marked `PREVIEW ONLY` in the files.

Still needed before launch, each requires something from John or the build platform:
- Forms: Request Info modal, Contact form and Conference booking only flip a "thanks" state. They need HubSpot embeds / endpoints; the SMS opt-in must map to the field his texting vendor reads.
- Fonts: Typekit files are self-hosted here (52 files), which Adobe's license does not permit in production. Use the Adobe Fonts kit for the domain.
- Analytics / tracking: GA4 or GTM, HubSpot tracking code, Meta pixel. None present.
- Redirects: old nested URLs (`/services/...`, `/areas-of-focus/...`, `/case-studies`, `/services/veterinary-copy-writing`) to the final structure.
- Content: 6 device-frame video placeholders, Social Media Ads graphics, Request Info modal image, 16 demo blog posts, "2019" badge on About, legal-entity naming on the Privacy page (APV Marketing LLC / support@apvetmarketing.com).
- Rendering: pages are client-rendered by the Claude Design runtime; the raw HTML a crawler receives is a template. Fine for a preview; the production site should be the Webflow build (or a static render).

## Changelog
### 2026-10-13 – build 7c
- Homepage hero: new two-dog image (John, 10/13) replaces the dog-and-cat.
### 2026-10-13 – build 7b (launch prep)
- Favicon/app icons, OG/Twitter meta + default share image, canonical, lang, theme-color, robots.txt, sitemap.xml, 404 page. Preview noindex guard.
### 2026-10-13 – build 7 (client review 10/08 + answers 10/13)
This build was edited directly in this repo. The Claude Design export is retired; `tools/` holds the scripts that applied these changes.
- Sitewide: every "free analysis / practice review / wizard" CTA now opens the Request Info modal. The wizard link survives only on the Free Competitive Analysis page (opens in a new tab) and as the homepage hero's secondary button (new tab).
- Sitewide: Free Competitive Analysis bands removed from the homepage, Contact page and all 8 service pages. The page itself remains and is linked from the footer; it is no longer in the header or mobile menu.
- Sitewide: Google rating shows the G logo, 5.0 and five stars with no review count, including the floating badge and the Reviews page.
- Sitewide: every section headline darkens word by word as it scrolls into view (`assets/vm-r2.js`), honoring reduced-motion.
- Sitewide: animated counters (`assets/vm-r2.js`): 200+ counts up on every Areas-of-Focus page; "< 2 hrs" counts down from 48, "< 6 hrs" from 72; Google Ads page counts $20M+ up and 0% fee down from 20%; "1 dedicated account manager" is now a checkmark.
- Areas-of-Focus pages: services section lists all 8 services as compact cards.
- Service pages: practice-types section lists all 8 practice types; the "See all eight" link is gone. Content sections now alternate text/media (zig-zag) with real assets from the 10/13 folder and the old site, or a labeled device-frame placeholder where John is supplying a screen video.
- About: history photo swapped (the coffee-walk crop cut heads off at the source), office gallery tiles equalized, orphan perk card centered.
- Contact: simple form (first name, last name, email, phone, practice name) with the SMS opt-in checkbox and John's consent wording.
- Conferences: 4-photo "On the road" collage, "Mon" placeholder stat replaced with "100s of practices supported", 1000px headshot.
- Reviews: Google logo lock-up in the hero card and section header.
- Specialty Practice: hero headline rebalanced (no more one word per line).
- Privacy & Terms page ported from the live site (`privacy-policy.html`, May 15 2025 text, minus the stray culture paragraph at the top of the live page). All Privacy Policy / Terms links, including the SMS consent, now stay on-site.
- About: the Las Olas strip reused the history photo; swapped to the team high-five photo.
- New Blog hub page (`blog.html`) with 16 demo posts, featured post, category tags, infinite scroll with a Load more fallback. Linked from the About menu and footer.
### 2026-10-08 – build 6a (repo package)
- Unpacked single-file bundles into shared assets; pages are 25–140 KB instead of 9–17 MB each.
- 8 service pages: "See all practice types" link repointed from the removed `areas-of-focus.html` to `index.html#focus`.
### 2026-10-08 – build 6
- Header on every page starts full-width and glides into the sticky pill on scroll, matching the homepage.
- Homepage trust band plays the brand collage video (assets/collage-video.mp4, 7.6 MB, muted loop, team photo poster). First external asset in the build; keep the assets/ folder next to the HTML.
- Mobile menu: sub-panel no longer bleeds into the visible edge while closed.

### 2026-10-08 – build 5
- Homepage: 24 images that were built dynamically (focus cards, team gallery, core-value illustrations) are now embedded. Dead brand video replaced with a slow-pan team photo.
- "See all eight practice types" links go to the homepage Areas of Focus section; the internal areas-of-focus review page is no longer in the build.
- Contact Us relaid out: centered headline with Frank and Floyd (embedded, no CDN), dark request-form band, contact details as plain text on blue.
- Mobile menu: top-level links only, chevron items slide in a sub-panel with Back. Active-page indicator in desktop nav, dropdowns and mobile menu.
- Header About dropdown now mirrors the footer Company column: About Us, Reviews, Conferences, Our Blog. Case Studies retired.
- Form fields bottom-align in two-column layouts; Contact form goes single-column at 720px.
- About: core-value illustrations and gallery tiles embedded, history photo re-cropped, Las Olas street photo, careers CTA opens mail client.
- Service pages: "Built for your kind of practice" cards use the approved focus photos.
### 2026-10-07 – build 4 (client answers)
- New Reviews page (11 video testimonials + every Google review) and Contact Us page (hero with Floyd and Frank,
  redesigned request form, phone / email / address / careers).
- Request Info now opens a 3-step modal on every page instead of linking to the live analysis page.
- Header and footer: Case Studies removed, Reviews and Contact go to the new pages, Services / Areas of Focus are
  dropdown-only (nothing in the main nav anchors back to the homepage).
- SEO page: #1 ranking screenshot (Ocean Animal Hospital, "emergency vet in Cocoa Beach") added to the Real results block.
- Free Analysis: CTAs and form hand off to the wizard; unattributed quote replaced with Golden Heart's Google review.
- Focus pages renamed to the confirmed slugs. Real page titles and meta descriptions in every file's static head.
### 2026-10-07 – build 3 (first repo package)
-   template holes; fixed mobile heading overflow (long unbreakable "VeterinaryMarketing.com" in section headings),
  the Conferences booking form on phones, and the About office gallery.
- All 11 testimonial video links verified (YouTube and Vimeo IDs resolve).
- Page titles and meta descriptions on every page.
### 2026-10-07 – build 2
- Services updated to the new list (added AEO, ChatGPT Ads, Social Media Posting; Social Media → Social Media Ads;
  Copywriting removed) in header, footer, homepage cards and focus-page service blocks.
- Header and footer rebuilt to the 10/07 sitemap.
- 8 service pages built from the Services copy with the 25-link internal linking map.
- New About Us, Conferences & Speaking and Free Marketing Analysis pages.
- "Under 25 days" and (844) 844-0338 used consistently.
### 2026-10-06 – build 1
- Homepage, Areas of Focus index and 8 focus pages. Em dashes removed; Small Animal CTAs added.
