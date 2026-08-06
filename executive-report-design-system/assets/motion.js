/* ===========================================================================
   Executive report design system - the frozen motion engine.

   Copy this verbatim into an inline <script> at the end of <body>. It is
   progressive enhancement and nothing more: every final figure is already real
   text in the HTML, so with scripting disabled the report is complete and
   correct. The engine reads that text, replays the arrival, then writes the
   identical string back. It can never invent, round or corrupt a figure.
   =========================================================================== */

/* ===========================================================================
   MOTION ENGINE — inline, dependency-free, progressive enhancement.

   Design rules, in order of importance:
     1. The HTML already contains every final value as real text. This script
        reads that text, replays the arrival, then writes the identical string
        back. It can never invent, round or corrupt a figure.
     2. If scripting is off, the report is complete. Nothing here is required.
     3. Print always shows settled values. Counting stops on beforeprint.
     4. prefers-reduced-motion is honoured: values are set, not counted.
     5. Animation is triggered per page as it scrolls into view, so a nine-page
        report does not burn its whole performance on load.
   =========================================================================== */
(function () {
  'use strict';

  var root = document.documentElement;
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Split "$1.9M" into "$" / 1.9 / "M", "4/8" into "" / 4 / "/8".
  var NUM = /-?\d[\d,]*\.?\d*/;
  function parse(text) {
    var m = NUM.exec(text);
    if (!m) return null;
    var raw = m[0];
    var decimals = (raw.split('.')[1] || '').length;
    return {
      prefix: text.slice(0, m.index),
      suffix: text.slice(m.index + raw.length),
      value: parseFloat(raw.replace(/,/g, '')),
      decimals: decimals,
      grouped: raw.indexOf(',') > -1,
      original: text
    };
  }

  function format(spec, n) {
    var body = spec.decimals
      ? n.toFixed(spec.decimals)
      : (spec.grouped ? Math.round(n).toLocaleString('en-GB') : String(Math.round(n)));
    return spec.prefix + body + spec.suffix;
  }

  var running = [];

  function count(el, spec, delay) {
    var duration = 1500;
    var start = null;
    el.classList.add('is-counting');

    function frame(now) {
      if (start === null) start = now;
      var t = (now - start - delay) / duration;
      if (t < 0) { el.__raf = requestAnimationFrame(frame); return; }
      if (t >= 1) {
        el.textContent = spec.original;      // exact original string, always
        el.classList.remove('is-counting');
        el.__raf = null;
        return;
      }
      // Ease-out quint: fast arrival, long graceful settle.
      var eased = 1 - Math.pow(1 - t, 5);
      el.textContent = format(spec, spec.value * eased);
      el.__raf = requestAnimationFrame(frame);
    }
    el.__raf = requestAnimationFrame(frame);
    running.push(el);
  }

  function settleAll() {
    running.forEach(function (el) {
      if (el.__raf) { cancelAnimationFrame(el.__raf); el.__raf = null; }
      if (el.__spec) el.textContent = el.__spec.original;
      el.classList.remove('is-counting');
    });
    running.length = 0;
  }

  // ---------------------------------------------------------------- prepare
  var counters = [].slice.call(document.querySelectorAll('.kpi-value, .compare-value, .count-up'));
  counters.forEach(function (el) {
    var spec = parse(el.textContent.trim());
    if (spec) { el.__spec = spec; el.classList.add('rise'); }
  });

  // Blocks that rise into place.
  var risers = [].slice.call(document.querySelectorAll(
    '.kpi-card, .num-card, .flow-step, .highlight-card, .panel, .compare-col, .risk-callout, .toc-item, .status-item'
  ));
  risers.forEach(function (el) { el.classList.add('rise'); });

  // Bars: park the authored width, hand it back on reveal.
  var bars = [].slice.call(document.querySelectorAll('.bar-fill'));
  bars.forEach(function (el) {
    el.style.setProperty('--target', el.style.width || '0%');
  });

  // Trend lines: measure the path so it can draw itself.
  var trends = [].slice.call(document.querySelectorAll('.trend'));
  trends.forEach(function (svg) {
    var line = svg.querySelector('.line');
    if (!line || !line.getTotalLength) return;
    var len = Math.ceil(line.getTotalLength());
    line.style.strokeDasharray = len;
    svg.style.setProperty('--len', len);
    [].slice.call(svg.querySelectorAll('.dot')).forEach(function (d, i) {
      d.style.setProperty('--delay', (900 + i * 90) + 'ms');
    });
  });

  root.classList.add('js-motion');
  document.body.classList.add('js-motion');

  // ---------------------------------------------------------------- reveal
  function reveal(page) {
    if (page.__revealed) return;
    page.__revealed = true;

    var i = 0;
    [].slice.call(page.querySelectorAll('.rise')).forEach(function (el) {
      var delay = Math.min(i * 55, 480);
      el.style.setProperty('--delay', delay + 'ms');
      el.classList.add('is-in');
      if (el.__spec && !still) count(el, el.__spec, delay);
      i++;
    });

    [].slice.call(page.querySelectorAll('.bar-fill')).forEach(function (el, n) {
      el.style.setProperty('--delay', (220 + n * 110) + 'ms');
      el.classList.add('is-in');
    });

    [].slice.call(page.querySelectorAll('.trend')).forEach(function (el) {
      el.classList.add('is-in');
    });
  }

  var pages = [].slice.call(document.querySelectorAll('.page'));

  if (still || !('IntersectionObserver' in window)) {
    pages.forEach(reveal);
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { reveal(e.target); io.unobserve(e.target); }
      });
    }, { threshold: 0.18 });
    pages.forEach(function (p) { io.observe(p); });
  }

  // ---------------------------------------------------------------- print
  window.addEventListener('beforeprint', function () {
    pages.forEach(reveal);
    settleAll();
  });
  if (window.matchMedia) {
    var mq = window.matchMedia('print');
    var onChange = function (e) { if (e.matches) { pages.forEach(reveal); settleAll(); } };
    if (mq.addEventListener) mq.addEventListener('change', onChange);
    else if (mq.addListener) mq.addListener(onChange);
  }

  // Replay control, screen only.
  var replay = document.getElementById('replay');
  if (replay) {
    replay.addEventListener('click', function () {
      settleAll();
      pages.forEach(function (p) {
        p.__revealed = false;
        [].slice.call(p.querySelectorAll('.rise')).forEach(function (el) { el.classList.remove('is-in'); });
        [].slice.call(p.querySelectorAll('.bar-fill')).forEach(function (el) { el.classList.remove('is-in'); });
        [].slice.call(p.querySelectorAll('.trend')).forEach(function (el) { el.classList.remove('is-in'); });
      });
      // Let the browser paint the reset state before replaying.
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          var top = window.scrollY;
          pages.forEach(function (p) {
            var r = p.getBoundingClientRect();
            if (r.bottom > 0 && r.top < window.innerHeight) reveal(p);
          });
          void top;
        });
      });
    });
  }
})();
