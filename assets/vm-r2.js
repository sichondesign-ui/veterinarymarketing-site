/* VeterinaryMarketing.com — shared round-2 runtime
 * 1) Animated counters: any element with [data-count]; optional [data-from] (count down from a higher number).
 * 2) Headline scrub: every <h2> darkens word-by-word as it scrolls into view (same effect as the homepage).
 * Honors prefers-reduced-motion: final values rendered immediately, no animation.
 */
(function () {
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var LIT_DEFAULT = '#223E6B';

  /* ---------- counters ---------- */
  var counted = new WeakSet();
  function fmt(n, dec, grouped) {
    var s = n.toFixed(dec);
    if (grouped) { var p = s.split('.'); p[0] = p[0].replace(/\B(?=(\d{3})+(?!\d))/g, ','); s = p.join('.'); }
    return s;
  }
  function runCounter(el) {
    if (counted.has(el)) return;
    var raw = String(el.getAttribute('data-count') || '').trim();
    var m = raw.match(/^([^\d]*)([\d,]+(?:\.\d+)?)(.*)$/);
    if (!m) return;
    counted.add(el);
    var grouped = m[2].indexOf(',') >= 0;
    var target = parseFloat(m[2].replace(/,/g, ''));
    var dec = (m[2].split('.')[1] || '').length;
    var fromAttr = el.getAttribute('data-from');
    var from = fromAttr !== null && fromAttr !== '' ? parseFloat(String(fromAttr).replace(/[^\d.]/g, '')) : 0;
    if (isNaN(from)) from = 0;
    var pre = m[1], suf = m[3];
    if (reduced) { el.textContent = pre + fmt(target, dec, grouped) + suf; return; }
    var t0 = performance.now(), dur = 1400;
    el.textContent = pre + fmt(from, dec, grouped) + suf;
    function tick(now) {
      var p = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      el.textContent = pre + fmt(from + (target - from) * e, dec, grouped) + suf;
      if (p < 1) requestAnimationFrame(tick); else el.textContent = raw;
    }
    requestAnimationFrame(tick);
  }
  var countIO = 'IntersectionObserver' in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (en) { if (en.isIntersecting) { countIO.unobserve(en.target); runCounter(en.target); } });
  }, { threshold: 0.5 }) : null;
  function armCounters() {
    document.querySelectorAll('[data-count]').forEach(function (el) {
      if (counted.has(el) || el.__vmArmed) return;
      if (!String(el.getAttribute('data-count') || '').trim()) return;
      el.__vmArmed = true;
      if (countIO) countIO.observe(el); else runCounter(el);
    });
  }

  /* ---------- headline scrub ---------- */
  function rgba(c, a) {
    var m = String(c).match(/rgba?\(([^)]+)\)/);
    if (!m) return 'rgba(34,62,107,' + a + ')';
    var p = m[1].split(',').map(function (x) { return x.trim(); });
    return 'rgba(' + p[0] + ',' + p[1] + ',' + p[2] + ',' + a + ')';
  }
  function wrapHeadings() {
    document.querySelectorAll('h2').forEach(function (h) {
      if (h.classList.contains('vm-cta-head') || h.__vmWrapped) return;
      // The page renderer wraps bound text in <span class="sc-interp">; wrap inside it. Otherwise only plain-text
      // headings (optionally with <br>). Skip anything still holding a template token.
      var host = h;
      var kids = Array.prototype.slice.call(h.childNodes).filter(function (n) { return !(n.nodeType === 3 && !n.textContent.trim()); });
      if (kids.length === 1 && kids[0].nodeType === 1 && kids[0].classList && kids[0].classList.contains('sc-interp')) host = kids[0];
      var ok = true;
      host.childNodes.forEach(function (n) { if (n.nodeType === 1 && n.tagName !== 'BR') ok = false; });
      var text = host.textContent || '';
      if (!ok || !text.trim() || text.indexOf('{{') >= 0) return;
      var lit = getComputedStyle(h).color || LIT_DEFAULT;
      var isLight = /rgb\((2[2-5]\d|1[89]\d),\s*(2[2-5]\d|1[89]\d),\s*(2[2-5]\d|1[89]\d)/.test(lit) || lit === 'white';
      var dim = isLight ? rgba(lit, 0.3) : rgba(lit, 0.18);
      var html = '';
      host.childNodes.forEach(function (n) {
        if (n.nodeType === 1) { html += '<br>'; return; }
        var words = n.textContent.split(/(\s+)/);
        words.forEach(function (w) {
          if (!w) return;
          if (/^\s+$/.test(w)) { html += w; return; }
          html += '<span data-w="1">' + w.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</span>';
        });
      });
      h.__vmWrapped = true;
      host.innerHTML = html;
      h.classList.add('vm-cta-head');
      h.setAttribute('data-lit', lit);
      h.setAttribute('data-dim', dim);
    });
  }
  function scrub() {
    var vh = window.innerHeight;
    document.querySelectorAll('h2.vm-cta-head').forEach(function (el) {
      var spans = el.querySelectorAll('span[data-w]');
      if (!spans.length) return;
      var r = el.getBoundingClientRect();
      var p = reduced ? 1 : Math.min(1, Math.max(0, (vh * 0.88 - r.top) / (vh * 0.34)));
      var lit = Math.round(p * spans.length);
      var litC = el.getAttribute('data-lit') || LIT_DEFAULT, dimC = el.getAttribute('data-dim') || 'rgba(34,62,107,0.16)';
      spans.forEach(function (sp, i) { sp.style.color = i < lit ? litC : dimC; });
    });
  }

  /* ---------- boot: the page renders client-side, so poll until content exists, then watch for changes ---------- */
  var raf = null;
  function onScroll() { if (raf) return; raf = requestAnimationFrame(function () { raf = null; scrub(); }); }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  var pending = null;
  function refresh() { wrapHeadings(); armCounters(); scrub(); }
  function schedule() { if (pending) return; pending = setTimeout(function () { pending = null; refresh(); }, 120); }
  function boot() {
    refresh();
    new MutationObserver(schedule).observe(document.body, { childList: true, subtree: true });
    window.VM_R2 = { refresh: refresh };
  }
  // Escape closes the Request Info / video dialogs on pages whose own script doesn't handle it
  window.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var btn = document.querySelector('[role="dialog"] button[aria-label="Close"], [role="dialog"] button[aria-label="Close video"]');
    if (btn) btn.click();
  });
  var tries = 0;
  (function wait() {
    if (document.body && document.querySelector('h2, [data-count]')) { boot(); return; }
    if (++tries < 100) setTimeout(wait, 100);
  })();
})();
