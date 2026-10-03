/* vk-home.js: cycles the highlighted service in the home page orbit visual. */
(function () {
  'use strict';
  function init(root) {
    var nodes = root.querySelectorAll('.vk-node'), data = root.querySelectorAll('.vk-orbit-data span');
    var n = root.querySelector('.vk-orbit-cap .n'), d = root.querySelector('.vk-orbit-cap .d'), go = root.querySelector('.vk-orbit-cap .go'), dot = root.querySelector('.vk-orbit-cap .vk-cdot');
    var i = 0, timer = null, reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    function show(k) {
      nodes.forEach(function (el, j) { el.classList.toggle('on', j === k); });
      var s = data[k]; n.textContent = s.getAttribute('data-label'); d.textContent = s.textContent; go.setAttribute('href', s.getAttribute('data-href'));
      dot.style.background = s.getAttribute('data-c'); dot.style.boxShadow = '0 0 10px ' + s.getAttribute('data-c');
    }
    function start() { stop(); timer = setInterval(function () { i = (i + 1) % nodes.length; show(i); }, 2600); }
    function stop() { if (timer) clearInterval(timer); timer = null; }
    nodes.forEach(function (el, j) {
      el.addEventListener('mouseenter', function () { stop(); i = j; show(j); });
      el.addEventListener('focus', function () { stop(); i = j; show(j); });
      el.addEventListener('mouseleave', function () { if (!reduced) start(); });
    });
    show(0); if (!reduced) start(); else { var sv = root.querySelector('svg'); if (sv && sv.pauseAnimations) sv.pauseAnimations(); }
  }
  function boot() { Array.prototype.forEach.call(document.querySelectorAll('.vk-orbit'), init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
