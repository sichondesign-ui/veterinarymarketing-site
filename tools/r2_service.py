#!/usr/bin/env python3
"""Round 2, part 2: service pages. A9 zig-zag content sections with a media column (real asset, or a
device-frame placeholder for the screen videos John is supplying). Also shortens the practice-type card link."""
import re, sys, json, pathlib
ROOT = pathlib.Path(sys.argv[1]); AM = json.load(open('tools/assetmap.json'))
A = lambda k: 'assets/' + AM[k]

def img(key, kind='plain', alt=''): return {'t': 'img', 'src': A(key) if key in AM else key, 'kind': kind, 'alt': alt}
def dev(kind, title, note='Screen video coming from VeterinaryMarketing.com'): return {'t': 'dev', 'kind': kind, 'title': title, 'note': note}

MEDIA = {  # page -> {block index: media}; blocks that already carry a bullet panel are left alone
  'veterinary-websites.html': {0: dev('mac', 'Website walkthrough'), 2: img('web-goldenheart', 'plain', 'Custom veterinary website design shown on desktop and phone'), 4: dev('imac', 'Live site demo')},
  'veterinary-seo-marketing.html': {0: img('assets/seo-rank-proof-16216d07b6.webp', 'photo', 'Ocean Animal Hospital ranking #1 for emergency vet in Cocoa Beach'), 1: img('laptop-video', 'plain', 'Veterinary SEO results on a laptop'), 2: img('seo2', 'plain', 'Service pages ranking for local searches'), 3: img('seo-map', 'plain', 'Local map pack ranking')},
  'veterinary-aeo.html': {0: img('aeo-logos', 'plain', 'ChatGPT, Claude, Gemini, Copilot and Perplexity'), 3: img('aeo-devices', 'plain', 'Your practice recommended inside an AI Overview on desktop and phone'), 4: dev('phone', 'AI search demo')},
  'veterinary-ppc-marketing.html': {0: dev('mac', 'Google Ads dashboard'), 2: img('ads-laptop', 'plain', 'Google Ads campaign results on a laptop'), 3: img('laptop', 'plain', 'Transparent ROI dashboard')},
  'veterinary-chatgpt-ads.html': {0: img('chatgpt-main', 'plain', 'A ChatGPT Ads placement for a veterinary practice'), 4: img('chatgpt-portal', 'plain', 'Vet-near-me results inside ChatGPT')},
  'veterinary-social-media-marketing.html': {1: img('social-mkt', 'plain', 'Facebook and Instagram ads for a veterinary practice'), 2: dev('phone', 'Ad creative in feed')},
  'veterinary-social-media-posting.html': {0: img('posting-devices', 'plain', 'Custom social posts across devices'), 1: img('posting-iphone', 'plain', 'A weekly post for your practice'), 2: img('posting-results', 'plain', 'Monthly posting results'), 4: dev('phone', 'Posts in feed')},
  'veterinary-direct-mail-marketing.html': {1: img('dm', 'plain', 'Custom postcards for a veterinary practice'), 2: img('slides', 'plain', 'Print design samples'), 3: img('brand-rep', 'plain', 'Logo and brand design for veterinarians')},
}

MEDIA_TPL = '''        <sc-if value="{{ b.hasMedia }}" hint-placeholder-val="{{ false }}">
          <div class="{{ b.mediaClass }}" style="{{ b.mediaStyle }}">
            <sc-if value="{{ b.mediaIsImg }}" hint-placeholder-val="{{ true }}"><img src="{{ b.mediaSrc }}" alt="{{ b.mediaAlt }}" loading="lazy"></sc-if>
            <sc-if value="{{ b.mediaIsDevice }}" hint-placeholder-val="{{ false }}">
              <div class="{{ b.deviceClass }}"><div class="vm-screen"><div class="vm-label"><div class="vm-play" aria-hidden="true"></div><strong>{{ b.deviceTitle }}</strong><span>{{ b.deviceNote }}</span></div></div></div>
            </sc-if>
          </div>
        </sc-if>
'''

for name, media in MEDIA.items():
    p = ROOT / name; t = p.read_text(); n0 = t
    # 1) media data
    js = json.dumps({str(k): v for k, v in media.items()})
    assert '    const blocks = P.blocks.map((b, i) => {' in t, name
    t = t.replace('    const blocks = P.blocks.map((b, i) => {', '    const R2_MEDIA = ' + js + ';\n    const blocks = P.blocks.map((b, i) => {', 1)
    # 2) mapper: media-aware flip + grid
    if 'const hasImage = !!b.image;' in t:   # SEO page: fold its one inline image into the media system
        t = t.replace('      const hasImage = !!b.image;\n      const flip = (hasPanel || hasImage) && i % 2 === 1;',
                      "      const md = R2_MEDIA[String(i)] || null; const hasMedia = !hasPanel && !!md; const hasImage = false;\n      const flip = (hasPanel || hasMedia) && i % 2 === 1;", 1)
        t = t.replace("((hasPanel || hasImage) ? 'minmax(0, 1fr) minmax(0, 1fr)' : 'minmax(0, 760px)')", "((hasPanel || hasMedia) ? 'minmax(0, 1fr) minmax(0, 1fr)' : 'minmax(0, 760px)')", 1)
    else:
        assert 'const flip = hasPanel && i % 2 === 1;' in t, name
        t = t.replace('      const flip = hasPanel && i % 2 === 1;', "      const md = R2_MEDIA[String(i)] || null; const hasMedia = !hasPanel && !!md;\n      const flip = (hasPanel || hasMedia) && i % 2 === 1;", 1)
        assert "(hasPanel ? 'minmax(0, 1fr) minmax(0, 1fr)' : 'minmax(0, 760px)')" in t, name
        t = t.replace("(hasPanel ? 'minmax(0, 1fr) minmax(0, 1fr)' : 'minmax(0, 760px)')", "((hasPanel || hasMedia) ? 'minmax(0, 1fr) minmax(0, 1fr)' : 'minmax(0, 760px)')", 1)
    # 3) media props appended after panelStyle
    m = re.search(r"\n(        panelStyle: 'order: ' \+ \(flip \? 1 : 2\)[^\n]*\n)", t); assert m, name + ' panelStyle'
    props = ("        hasMedia, mediaIsImg: hasMedia && md.t === 'img', mediaIsDevice: hasMedia && md.t === 'dev',\n"
             "        mediaClass: 'vm-media vm-reveal' + (hasMedia && md.t === 'img' ? ' vm-media-' + (md.kind || 'plain') : ''),\n"
             "        mediaStyle: 'order: ' + (flip ? 1 : 2) + ';',\n"
             "        mediaSrc: hasMedia && md.t === 'img' ? md.src : '', mediaAlt: hasMedia ? (md.alt || '') : '',\n"
             "        deviceClass: 'vm-dev vm-dev-' + (hasMedia && md.t === 'dev' ? md.kind : 'mac'), deviceTitle: hasMedia && md.t === 'dev' ? md.title : '', deviceNote: hasMedia && md.t === 'dev' ? md.note : '',\n")
    t = t[:m.end()] + props + t[m.end():]
    # 4) template: media column after the panel block (before the grid closes)
    closer = '        </sc-if>\n      </div>\n    </div>\n  </section>\n</sc-for>\n'
    if name == 'veterinary-seo-marketing.html':
        closer_seo = re.search(r'        <sc-if value="\{\{ b\.hasImage \}\}"[^\n]*\n      </div>\n    </div>\n  </section>\n</sc-for>\n', t); assert closer_seo, 'seo closer'
        t = t[:closer_seo.start()] + MEDIA_TPL + '      </div>\n    </div>\n  </section>\n</sc-for>\n' + t[closer_seo.end():]
    else:
        assert t.count(closer) == 1, (name, t.count(closer))
        t = t.replace(closer, '        </sc-if>\n' + MEDIA_TPL + '      </div>\n    </div>\n  </section>\n</sc-for>\n', 1)
    # 5) practice-type card: shorter link text
    t = t.replace('Read the {{ rf.short }} page →', 'Learn more →')
    # 6) mobile: single column already handled by .sp-2col rule? ensure order resets on narrow screens
    if '.sp-2col > *' not in t:
        t = t.replace('</style>\n</helmet>', '    @media (max-width: 860px) { .sp-2col { grid-template-columns: 1fr !important; gap: 36px !important; } .sp-2col > * { order: 0 !important; } }\n  </style>\n</helmet>', 1)
    assert t != n0
    p.write_text(t); print(name, 'media blocks:', sorted(media))
