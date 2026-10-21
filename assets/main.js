(function () {
  var d = document;
  d.documentElement.classList.add('js');

  var bar = d.querySelector('.progress');
  var sticky = d.querySelector('.sticky-cta');
  function onScroll() {
    var h = d.documentElement;
    var max = h.scrollHeight - h.clientHeight;
    if (bar && max > 0) bar.style.width = Math.min(100, (h.scrollTop / max) * 100) + '%';
    if (sticky) sticky.classList.toggle('show', h.scrollTop > 700);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  var btn = d.querySelector('.menu-btn');
  var nav = d.querySelector('.nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function countUp(el) {
    var target = parseFloat(el.getAttribute('data-count'));
    var suffix = el.getAttribute('data-suffix') || '';
    var decimals = (String(target).split('.')[1] || '').length;
    if (reduce) return;
    var start = null;
    var dur = 1400;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min(1, (ts - start) / dur);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = (target * eased).toFixed(decimals) + suffix;
      if (p < 1) requestAnimationFrame(step);
      else el.textContent = target.toFixed(decimals) + suffix;
    }
    requestAnimationFrame(step);
  }

  var items = d.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          var counters = e.target.querySelectorAll('[data-count]');
          counters.forEach(countUp);
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.15 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  var quiz = d.getElementById('tier-quiz');
  if (quiz) {
    var tiers = {
      starter: {
        name: 'Starter',
        price: '$97',
        text: 'You are at the very beginning. Starter gives you the core VA training so you can learn the basics at your own pace.'
      },
      spark: {
        name: 'Spark',
        price: '$180',
        text: 'You want your questions answered. Spark adds 2 hours of coaching calls, Discord access and 3 months of portal access.'
      },
      surge: {
        name: 'Surge',
        price: '$299',
        text: 'You want the most practice. Surge includes everything in Spark, plus more practice with host businesses.'
      }
    };
    var out = d.getElementById('quiz-result');
    function evaluate() {
      var data = new FormData(quiz);
      var a = data.get('q1'), b = data.get('q2'), c = data.get('q3');
      if (!a || !b || !c) return;
      var score = { starter: 0, spark: 0, surge: 0 };
      score[b] += 2;
      score[c] += 2;
      score[a] += 1;
      var pick = 'starter';
      if (score.spark >= score[pick]) pick = 'spark';
      if (score.surge > score[pick]) pick = 'surge';
      if (b === 'surge' && c === 'surge') pick = 'surge';
      var t = tiers[pick];
      out.innerHTML = '';
      var kick = d.createElement('div');
      kick.className = 'kicker';
      kick.textContent = 'Your match';
      var h = d.createElement('h3');
      h.textContent = t.name + ', ' + t.price + ' one time';
      var p = d.createElement('p');
      p.textContent = t.text;
      var a1 = d.createElement('a');
      a1.className = 'btn';
      var base = d.querySelector('.sticky-cta');
      a1.href = base ? base.getAttribute('href') : 'apply/';
      a1.textContent = 'Apply now';
      out.appendChild(kick);
      out.appendChild(h);
      out.appendChild(p);
      out.appendChild(a1);
      out.classList.add('show');
      d.querySelectorAll('.tier').forEach(function (el) {
        el.classList.toggle('pick', el.getAttribute('data-tier') === pick);
      });
    }
    quiz.addEventListener('change', evaluate);
  }

  var y = d.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
