# VeterinaryMarketing.com – Site Preview

Static preview build of the new veterinarymarketing.com. Plain HTML pages with shared, content-hashed assets in `assets/`
(unpacked from the Claude Design single-file export, 224 MB → 23 MB), so the folder can be served by GitHub Pages, Netlify or any static host with no build step.

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
- Blog and Privacy Policy link to the live site. Case Studies is retired (redirect `/case-studies` → `/reviews`).
- Redirect `/services/veterinary-copy-writing` → `/services/veterinary-websites`.

## Build notes
- This is the review build: each page is self-contained (fonts and images embedded), 8-18 MB per page. The production
  build will be unpacked: shared /assets, no unpack loader, ~140 KB HTML per page.
- Adobe Fonts (polymath, visby) are embedded here for review only. Production must load them from the client's Typekit
  kit (use.typekit.net) per the license; need the kit ID from John.
- Forms are front-end only. Production needs a submit target (HubSpot Forms API) and a spam measure (reCAPTCHA or Turnstile).

## Open items for John
- Artwork for three service cards: Veterinary AEO, ChatGPT Ads, Social Media Posting (placeholders in place).
- A larger headshot of John for the Conferences page (current file is 200×200).
- Confirm founding year: the About page history photo carries a "2019 · veterinary only, ever since" badge that isn't in the copy doc.
- Reviews page shows 73 written Google reviews (7 were truncated in the export and link out to Google) plus 11 videos.

## Changelog
### 2026-10-08 – build 5a (repo package)
- Homepage trust band: self-hosted brand collage video (`assets/brand-collage.mp4`, 1280p muted loop, 7.6 MB) replaces the placeholder photo. Source: Collage Video.mp4 from the client archive.
- Unpacked single-file bundles into shared assets; pages are 25–140 KB instead of 9–17 MB each.
- 8 service pages: "See all practice types" link repointed from the removed `areas-of-focus.html` to `index.html#focus`.
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
