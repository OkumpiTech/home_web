/* ==========================================================================
   Okumpi — site behaviour
   Navbar state · mobile menu · testimonial carousel · reveal-on-scroll ·
   stat counters · newsletter capture (AJAX)
   ========================================================================== */
(function () {
  'use strict';

  /* ---------------- Navbar scroll state ---------------- */
  var navbar = document.getElementById('navbar');
  function onScroll() {
    if (!navbar) return;
    navbar.classList.toggle('scrolled', window.scrollY > 40);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------------- Mobile menu ---------------- */
  var toggle = document.getElementById('navToggle');
  var panel = document.getElementById('mobilePanel');
  var toggleIcon = document.getElementById('navToggleIcon');
  if (toggle && panel) {
    toggle.addEventListener('click', function () {
      var open = panel.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
      if (toggleIcon) {
        toggleIcon.innerHTML = '<use href="#i-' + (open ? 'close' : 'menu') + '"/>';
      }
    });
    panel.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        panel.classList.remove('open');
        document.body.style.overflow = '';
        if (toggleIcon) toggleIcon.innerHTML = '<use href="#i-menu"/>';
      });
    });
  }

  /* ---------------- Testimonial carousel ---------------- */
  var track = document.getElementById('tTrack');
  var prev = document.getElementById('tPrev');
  var next = document.getElementById('tNext');
  var dotsWrap = document.getElementById('tDots');

  function cardStep() {
    var card = track && track.querySelector('.t-card');
    if (!card) return 0;
    var gap = parseFloat(getComputedStyle(track).gap) || 18;
    return card.getBoundingClientRect().width + gap;
  }

  function pageCount() {
    if (!track) return 0;
    var step = cardStep();
    if (!step) return 0;
    var visible = Math.max(1, Math.round((track.clientWidth + 18) / step));
    var total = track.querySelectorAll('.t-card').length;
    return Math.max(1, Math.ceil(total / visible));
  }

  function currentPage() {
    var step = cardStep();
    if (!step) return 0;
    var visible = Math.max(1, Math.round((track.clientWidth + 18) / step));
    return Math.round(track.scrollLeft / (step * visible));
  }

  function renderDots() {
    if (!dotsWrap || !track) return;
    var pages = pageCount();
    dotsWrap.innerHTML = '';
    for (var i = 0; i < pages; i++) {
      var b = document.createElement('button');
      b.className = 't-dot' + (i === currentPage() ? ' active' : '');
      b.setAttribute('aria-label', 'Go to testimonials page ' + (i + 1));
      (function (idx) {
        b.addEventListener('click', function () {
          var step = cardStep();
          var visible = Math.max(1, Math.round((track.clientWidth + 18) / step));
          track.scrollTo({ left: idx * step * visible, behavior: 'smooth' });
        });
      })(i);
      dotsWrap.appendChild(b);
    }
  }

  function syncDots() {
    if (!dotsWrap) return;
    var dots = dotsWrap.children;
    var cur = currentPage();
    for (var i = 0; i < dots.length; i++) {
      dots[i].classList.toggle('active', i === cur);
    }
  }

  if (track) {
    renderDots();
    var scrollTimer;
    track.addEventListener('scroll', function () {
      clearTimeout(scrollTimer);
      scrollTimer = setTimeout(syncDots, 80);
    }, { passive: true });
    window.addEventListener('resize', function () {
      clearTimeout(scrollTimer);
      scrollTimer = setTimeout(renderDots, 150);
    });
    if (prev) prev.addEventListener('click', function () {
      track.scrollBy({ left: -cardStep(), behavior: 'smooth' });
    });
    if (next) next.addEventListener('click', function () {
      track.scrollBy({ left: cardStep(), behavior: 'smooth' });
    });
  }

  /* ---------------- Reveal on scroll ---------------- */
  var revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && revealEls.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------------- Stat counters ---------------- */
  var counters = document.querySelectorAll('[data-count]');
  if ('IntersectionObserver' in window && counters.length) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        cio.unobserve(e.target);
        var el = e.target;
        var target = parseInt(el.getAttribute('data-count'), 10) || 0;
        var suffix = el.getAttribute('data-suffix') || '';
        var dur = 1400;
        var start = null;
        function tick(ts) {
          if (!start) start = ts;
          var p = Math.min(1, (ts - start) / dur);
          var eased = 1 - Math.pow(1 - p, 3);
          el.textContent = Math.round(target * eased) + suffix;
          if (p < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
      });
    }, { threshold: 0.5 });
    counters.forEach(function (el) { cio.observe(el); });
  }

  /* ---------------- Newsletter capture (AJAX) ---------------- */
  document.querySelectorAll('form[data-capture]').forEach(function (form) {
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var msgEl = form.parentElement.querySelector('.capture-msg');
      var btn = form.querySelector('button[type="submit"]');
      var data = new FormData(form);
      if (btn) btn.disabled = true;
      fetch(form.action, {
        method: 'POST',
        body: data,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      }).then(function (r) { return r.json(); }).then(function (res) {
        if (msgEl) {
          msgEl.textContent = res.message;
          msgEl.classList.toggle('error', !res.ok);
          msgEl.classList.add('show');
        }
        if (res.ok) form.reset();
      }).catch(function () {
        // graceful fallback: normal submit
        form.removeEventListener('submit', arguments.callee);
        form.submit();
      }).finally(function () {
        if (btn) btn.disabled = false;
      });
    });
  });

  /* ---------------- Auto-hide toasts ---------------- */
  document.querySelectorAll('.toast').forEach(function (t) {
    setTimeout(function () {
      t.style.transition = 'opacity .5s ease, transform .5s ease';
      t.style.opacity = '0';
      t.style.transform = 'translateY(8px)';
      setTimeout(function () { t.remove(); }, 550);
    }, 5200);
  });
})();
