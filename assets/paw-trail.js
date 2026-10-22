/* VeterinaryMarketing.com — paw-print cursor trail (spec 10/22).
   Mouse only. Off under prefers-reduced-motion and below MIN_VW. Pauses over interactive UI.
   Pool of POOL spans in one fixed container; prints fade + shrink over LIFE_MS. */
(function () {
  'use strict';

  // ---- tuning knobs ----
  var STEP_PX = 90;      // distance between prints
  var GAIT_PX = 14;      // left/right offset
  var WOBBLE_DEG = 8;    // random rotation jitter
  var LIFE_MS = 1400;    // fade duration (keep in sync with CSS)
  var POOL = 24;         // max live prints
  var MIN_VW = 1024;     // disable below this width

  var PAW_SVG = 'assets/paw-fill-1e3d9826c2.svg';
  var LIGHT = '#749BEA';
  var DARK = 'rgba(255,255,255,0.35)';
  var PAUSE_SEL = 'a, button, input, select, textarea, label, nav, [role="dialog"], [data-no-paws]';

  function init() {
    if (!window.matchMedia) return;
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    var style = document.createElement('style');
    style.textContent =
      '@keyframes vmPawFade{from{opacity:.35;transform:translate(-50%,-50%) rotate(var(--r)) scale(1)}to{opacity:0;transform:translate(-50%,-50%) rotate(var(--r)) scale(.85)}}' +
      '.vm-paw-layer{position:fixed;inset:0;pointer-events:none;z-index:9000;overflow:hidden}' +
      '.vm-paw{position:absolute;width:22px;height:20px;-webkit-mask:url(' + PAW_SVG + ') center/contain no-repeat;mask:url(' + PAW_SVG + ') center/contain no-repeat;will-change:transform,opacity;visibility:hidden}' +
      '.vm-paw.is-live{visibility:visible;animation:vmPawFade ' + LIFE_MS + 'ms ease-out forwards}';
    document.head.appendChild(style);

    var layer = document.createElement('div');
    layer.className = 'vm-paw-layer';
    layer.setAttribute('aria-hidden', 'true');
    var pool = [];
    for (var i = 0; i < POOL; i++) {
      var s = document.createElement('span');
      s.className = 'vm-paw';
      s.addEventListener('animationend', function () { this.classList.remove('is-live'); this.style.visibility = 'hidden'; });
      layer.appendChild(s); pool.push(s);
    }
    document.body.appendChild(layer);

    var slot = 0, side = 1, last = null, pending = null, raf = 0;

    function isDark(x, y) {
      var el = document.elementFromPoint(x, y);
      return !!(el && el.closest && el.closest('[data-surface="dark"]'));
    }
    function overUI(x, y) {
      var el = document.elementFromPoint(x, y);
      return !!(el && el.closest && el.closest(PAUSE_SEL));
    }
    function stamp(x, y, ang, dark) {
      var el = pool[slot]; slot = (slot + 1) % POOL;
      el.classList.remove('is-live'); void el.offsetWidth;   // restart the animation
      el.style.left = x + 'px'; el.style.top = y + 'px';
      el.style.background = dark ? DARK : LIGHT;
      el.style.setProperty('--r', (ang * 180 / Math.PI + 90 + (Math.random() * 2 - 1) * WOBBLE_DEG) + 'deg');
      el.style.visibility = 'visible';
      el.classList.add('is-live');
    }
    function tick() {
      raf = 0;
      var e = pending; pending = null; if (!e) return;
      var x = e.clientX, y = e.clientY;
      if (!last) { last = { x: x, y: y }; return; }
      var dx = x - last.x, dy = y - last.y, d = Math.hypot(dx, dy);
      if (d < STEP_PX) return;
      if (overUI(x, y)) { last = { x: x, y: y }; return; }
      var ang = Math.atan2(dy, dx);
      side = -side;
      var mx = (last.x + x) / 2 + Math.cos(ang + Math.PI / 2) * GAIT_PX * side;
      var my = (last.y + y) / 2 + Math.sin(ang + Math.PI / 2) * GAIT_PX * side;
      stamp(mx, my, ang, isDark(mx, my));
      last = { x: x, y: y };
    }
    document.addEventListener('pointermove', function (e) {
      if (e.pointerType && e.pointerType !== 'mouse') return;
      if (window.innerWidth < MIN_VW) return;
      pending = e;
      if (!raf) raf = requestAnimationFrame(tick);
    }, { passive: true });
    document.addEventListener('pointerleave', function () { last = null; });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
