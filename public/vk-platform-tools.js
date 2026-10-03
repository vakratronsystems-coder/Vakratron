/* vk-platform-tools.js: interactive tools for the Kubernetes and API pages.
   - .vk-k8scheck : do you really need Kubernetes?
   - .vk-gitops   : GitOps rolling update, node failure and drift correction
   - .vk-apisim   : API gateway checks, rate limiting and a circuit breaker
   No dependencies. Styles live in vk-content.css. */
(function () {
  'use strict';
  function esc(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }
  var REDUCED = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function wait(ms) { return new Promise(function (r) { setTimeout(r, REDUCED ? ms * 0.3 : ms); }); }

  /* ------------------------------------------------------------------ Kubernetes checker */
  var KQ = [
    { q: 'How many services or applications will run on it?', o: [['One to three', -2, 'With only a few applications, Kubernetes adds more work than it saves.'], ['Ten or more', 1, 'Many services is where a shared platform starts to pay off.'], ['Dozens, across several teams', 2, 'Dozens of services across teams is the classic case for Kubernetes.']] },
    { q: 'How often do you release?', o: [['A few times a year', -2, 'Infrequent releases do not need a deployment platform built for speed.'], ['Monthly', 0, 'Monthly releases work fine with or without Kubernetes.'], ['Weekly or daily', 2, 'Frequent releases benefit from automated, repeatable deployments.']] },
    { q: 'How does demand change?', o: [['Steady and predictable', -1, 'Steady load does not need automatic scaling.'], ['Some daily or seasonal peaks', 1, 'Peaks benefit from automatic scaling of services.'], ['Large, sudden spikes', 2, 'Sudden spikes are where autoscaling earns its keep.']] },
    { q: 'Does your team already know containers?', o: [['Not yet', -2, 'Without container skills, start with containers on simpler platforms and grow into Kubernetes.'], ['Some experience', 0, 'Some container experience is a reasonable starting point with good support.'], ['Yes, we use them today', 2, 'Existing container skills make Kubernetes much easier to adopt.']] },
    { q: 'Who will run the platform?', o: [['Nobody has time for it', -2, 'A platform nobody owns decays. Consider a managed Kubernetes service or a simpler option.'], ['Part of one person\'s job', 0, 'Part-time ownership can work with a managed Kubernetes service.'], ['A dedicated platform team', 2, 'A dedicated platform team is what makes self-run Kubernetes succeed.']] }
  ];
  function initK8s(root) {
    var ans = [];
    var h = '<div class="vk-placer-qs">';
    KQ.forEach(function (q, i) {
      h += '<fieldset class="vk-q"><legend><span class="vk-num">' + (i + 1) + '</span> ' + esc(q.q) + '</legend>';
      q.o.forEach(function (o, j) { h += '<label><input type="radio" name="vkk' + i + '" value="' + j + '"> <span>' + esc(o[0]) + '</span></label>'; });
      h += '</fieldset>';
    });
    h += '</div><div class="vk-placer-out" aria-live="polite"><p class="vk-muted">Answer the questions for an honest view.</p></div>';
    root.innerHTML = h;
    var out = root.querySelector('.vk-placer-out');
    root.addEventListener('change', function (e) {
      if (!e.target.name) return;
      ans[+e.target.name.slice(3)] = +e.target.value;
      var n = ans.filter(function (a) { return a !== undefined; }).length;
      if (n < KQ.length) { out.innerHTML = '<p class="vk-muted">' + n + ' of ' + KQ.length + ' answered.</p>'; return; }
      var score = 0, why = [];
      KQ.forEach(function (q, i) { var o = q.o[ans[i]]; score += o[1]; why.push(o[2]); });
      var v = score >= 5 ? ['Kubernetes is likely worth it', 'Your situation has the scale, pace and skills where a Kubernetes platform pays back its complexity.', '/solutions/k8s/platform-design', 'See how a platform is designed']
        : score >= 0 ? ['Kubernetes could work, start managed and small', 'There are real benefits, but also real gaps. A managed Kubernetes service and a small first platform lower the risk.', '/solutions/k8s/platform-design', 'See a lean platform design']
        : ['Probably not yet', 'Kubernetes would likely add more work than it removes today. Virtual machines with good automation, or a managed container service, may serve you better. We will say so if that is the case.', '/solutions/k8s/faq', 'Read the alternatives'];
      out.innerHTML = '<span class="vk-eyebrow">Our honest view</span><h3>' + v[0] + '</h3><p>' + v[1] + '</p><p><strong>Why:</strong></p><ul>' + why.map(function (w) { return '<li>' + esc(w) + '</li>'; }).join('') + '</ul><a class="vk-btn primary" href="' + v[2] + '">' + v[3] + ' &rarr;</a>';
    });
  }

  /* ------------------------------------------------------------------ GitOps simulator */
  function initGitops(root) {
    var nodes = [[], [], []], ver = 1, busy = false, down = -1, replicas = 6;
    for (var i = 0; i < replicas; i++) nodes[i % 3].push({ v: 1, st: '' });
    root.innerHTML =
      '<div class="vk-go-flow"><div class="box git"><span class="t">Git repository</span><span class="s">desired state</span><span class="vv">checkout-service: <b>v1</b>, replicas: <b>6</b></span></div>' +
      '<div class="arrow"><span>watches</span></div><div class="box argo"><span class="t">GitOps controller</span><span class="s">Argo CD or Flux</span><span class="vv st">In sync</span></div>' +
      '<div class="arrow"><span>applies</span></div><div class="box cluster"><span class="t">Kubernetes cluster</span><div class="kn"></div></div></div>' +
      '<div class="vk-go-ctl"><button type="button" class="vk-btn primary push">Release a new version</button><button type="button" class="vk-btn kill">Lose a server</button><button type="button" class="vk-btn drift">Someone edits the cluster by hand</button><button type="button" class="vk-btn reset">Reset</button></div>' +
      '<div class="vk-wave-log" aria-live="polite"><p class="vk-muted">Git holds the desired state. The controller keeps the cluster matching it. Try each button.</p></div>';
    var kn = root.querySelector('.kn'), log = root.querySelector('.vk-wave-log'), vv = root.querySelector('.git .vv'), st = root.querySelector('.argo .st'), argo = root.querySelector('.argo');
    function line(t, c) { var p = document.createElement('p'); p.className = c || ''; p.innerHTML = t; log.appendChild(p); log.scrollTop = log.scrollHeight; }
    function draw() {
      kn.innerHTML = nodes.map(function (n, i) {
        return '<div class="node' + (i === down ? ' down' : '') + '"><span class="nt">Server ' + (i + 1) + '</span><div class="pods">' +
          n.map(function (p) { return '<span class="pod v' + p.v + ' ' + p.st + '">v' + p.v + '</span>'; }).join('') + '</div></div>';
      }).join('');
      vv.innerHTML = 'checkout-service: <b>v' + ver + '</b>, replicas: <b>' + replicas + '</b>';
    }
    function setSync(t, cls) { st.textContent = t; argo.className = 'box argo ' + (cls || ''); }
    function all() { var a = []; nodes.forEach(function (n) { n.forEach(function (p) { a.push(p); }); }); return a; }
    function lock(b) { busy = b; root.querySelectorAll('.vk-go-ctl .vk-btn').forEach(function (x) { if (!x.classList.contains('reset')) x.disabled = b; }); }
    root.querySelector('.push').addEventListener('click', async function () {
      if (busy) return; lock(true); if (!log.querySelector('p:not(.vk-muted)')) log.innerHTML = '';
      ver++; draw();
      line('A developer merges a change in Git: version ' + ver + '.'); setSync('Out of sync', 'warn'); await wait(900);
      line('The controller notices and starts a rolling update, one pod at a time.');
      setSync('Syncing...', 'warn');
      var pods = all().filter(function (p) { return p.v !== ver; });
      for (var i = 0; i < pods.length; i++) {
        pods[i].st = 'starting'; pods[i].v = ver; draw(); await wait(450);
        pods[i].st = ''; draw();
      }
      setSync('In sync', 'ok'); line('&#10003; All pods run v' + ver + '. Users never saw downtime. To roll back, revert the commit in Git.', 'ok');
      lock(false);
    });
    root.querySelector('.kill').addEventListener('click', async function () {
      if (busy) return; lock(true); if (!log.querySelector('p:not(.vk-muted)')) log.innerHTML = '';
      var idx = down === -1 ? 1 : down; down = idx;
      var lost = nodes[idx].length; nodes[idx].forEach(function (p) { p.st = 'dead'; }); draw();
      line('&#10007; Server ' + (idx + 1) + ' fails. ' + lost + ' pods are lost.', 'bad'); await wait(1000);
      line('Kubernetes sees fewer pods than the ' + replicas + ' requested and starts replacements on the healthy servers.', 'warn');
      nodes[idx] = []; draw(); await wait(500);
      for (var i = 0; i < lost; i++) {
        var tgt = nodes.map(function (n, j) { return j; }).filter(function (j) { return j !== idx; }).sort(function (a, b) { return nodes[a].length - nodes[b].length; })[0];
        var p = { v: ver, st: 'starting' }; nodes[tgt].push(p); draw(); await wait(500); p.st = ''; draw();
      }
      line('&#10003; Back to ' + replicas + ' pods within seconds, without anyone being paged.', 'ok');
      await wait(800); down = -1; draw(); line('Server ' + (idx + 1) + ' is repaired and rejoins, ready for new work.');
      lock(false);
    });
    root.querySelector('.drift').addEventListener('click', async function () {
      if (busy) return; lock(true); if (!log.querySelector('p:not(.vk-muted)')) log.innerHTML = '';
      line('Someone scales the service down to 2 pods directly in the cluster, bypassing Git.', 'warn');
      var a = all(), removed = 0;
      for (var n = 2; n >= 0 && removed < 4; n--) { while (nodes[n].length && removed < 4) { nodes[n].pop(); removed++; } }
      draw(); setSync('Drift detected', 'bad'); await wait(1300);
      line('The controller sees the cluster no longer matches Git, and puts it back.', 'warn');
      for (var i = 0; i < removed; i++) {
        var tgt = [0, 1, 2].sort(function (x, y) { return nodes[x].length - nodes[y].length; })[0];
        var p = { v: ver, st: 'starting' }; nodes[tgt].push(p); draw(); await wait(450); p.st = ''; draw();
      }
      setSync('In sync', 'ok'); line('&#10003; Restored to 6 pods. Changes only stick when they go through Git, where they are reviewed and recorded.', 'ok');
      lock(false);
    });
    root.querySelector('.reset').addEventListener('click', function () {
      if (busy) return;
      nodes = [[], [], []]; ver = 1; down = -1; for (var i = 0; i < replicas; i++) nodes[i % 3].push({ v: 1, st: '' });
      setSync('In sync', ''); log.innerHTML = '<p class="vk-muted">Git holds the desired state. The controller keeps the cluster matching it. Try each button.</p>'; draw();
    });
    draw();
  }

  /* ------------------------------------------------------------------ API request simulator */
  function initApi(root) {
    var c = { ok: 0, e401: 0, e429: 0, e503: 0 }, tokens = 10, br = 'closed', fails = 0, payDown = false, openedAt = 0, busy = false;
    root.innerHTML =
      '<div class="vk-api-ctl"><label>Caller <select data-k="key"><option value="ok">Partner app with valid key</option><option value="none">Unknown caller, no key</option></select></label>' +
      '<label class="tg"><input type="checkbox" data-k="down"> Payments service is failing</label></div>' +
      '<div class="vk-api-flow"><div class="box" data-b="client"><span class="t">Caller</span></div><span class="ar"></span>' +
      '<div class="box" data-b="gw"><span class="t">API gateway</span><span class="s">key check, rate limit 10/min</span></div><span class="ar"></span>' +
      '<div class="box" data-b="orders"><span class="t">Orders service</span><span class="s br">circuit breaker: <b>closed</b></span></div><span class="ar"></span>' +
      '<div class="box" data-b="pay"><span class="t">Payments service</span><span class="s ps">healthy</span></div></div>' +
      '<div class="vk-api-count"><span class="ok">200 OK: <b data-c="ok">0</b></span><span class="e401">401 rejected: <b data-c="e401">0</b></span><span class="e429">429 too many: <b data-c="e429">0</b></span><span class="e503">503 fast fail: <b data-c="e503">0</b></span><span class="tok">Rate-limit tokens left: <b data-c="tok">10</b></span></div>' +
      '<div class="vk-go-ctl"><button type="button" class="vk-btn primary one">Send 1 request</button><button type="button" class="vk-btn burst">Send a burst of 15</button><button type="button" class="vk-btn reset">Reset</button></div>' +
      '<div class="vk-wave-log" aria-live="polite"><p class="vk-muted">Send requests and watch the gateway and the circuit breaker. Then switch the payments service to failing.</p></div>';
    var log = root.querySelector('.vk-wave-log');
    function line(t, cl) { var p = document.createElement('p'); p.className = cl || ''; p.innerHTML = t; log.appendChild(p); while (log.children.length > 40) log.removeChild(log.firstChild); log.scrollTop = log.scrollHeight; }
    function flash(b, cl) { var e = root.querySelector('[data-b="' + b + '"]'); e.classList.add(cl); setTimeout(function () { e.classList.remove(cl); }, 350); }
    function draw() {
      ['ok', 'e401', 'e429', 'e503'].forEach(function (k) { root.querySelector('[data-c="' + k + '"]').textContent = c[k]; });
      root.querySelector('[data-c="tok"]').textContent = tokens;
      var b = root.querySelector('.br'); b.innerHTML = 'circuit breaker: <b>' + br + '</b>'; b.className = 's br ' + br.replace(' ', '');
      var ps = root.querySelector('.ps'); ps.textContent = payDown ? 'failing' : 'healthy'; ps.className = 's ps' + (payDown ? ' bad' : '');
    }
    var refill = setInterval(function () { if (tokens < 10) { tokens++; draw(); } }, 6000);
    async function one(n) {
      var key = root.querySelector('[data-k="key"]').value;
      flash('client', 'on'); await wait(120); flash('gw', 'on');
      if (key !== 'ok') { c.e401++; line('#' + n + ' 401: no valid API key. Stopped at the gateway; no service was touched.', 'bad'); return; }
      if (tokens <= 0) { c.e429++; line('#' + n + ' 429: rate limit reached. The gateway protects the services behind it.', 'warn'); return; }
      tokens--; await wait(120); flash('orders', 'on');
      if (br === 'open') {
        if (Date.now() - openedAt > 8000) { br = 'half open'; line('Breaker half open: letting one test request through.', 'warn'); }
        else { c.e503++; line('#' + n + ' 503 in milliseconds: breaker is open, so Orders does not wait on a failing service.', 'warn'); return; }
      }
      await wait(120); flash('pay', payDown ? 'bad' : 'on');
      if (payDown) {
        fails++; c.e503++;
        if (br === 'half open' || fails >= 3) { br = 'open'; openedAt = Date.now(); fails = 0; line('#' + n + ' 503 after a 2-second timeout. Too many failures: <strong>breaker opens</strong>.', 'bad'); }
        else line('#' + n + ' 503 after waiting 2 seconds for Payments to time out.', 'bad');
        return;
      }
      if (br === 'half open') { br = 'closed'; line('Test request succeeded: breaker closes.', 'ok'); }
      fails = 0; c.ok++; line('#' + n + ' 200 OK', 'ok');
    }
    var count = 0;
    async function run(k) {
      if (busy) return; busy = true;
      if (!log.querySelector('p:not(.vk-muted)')) log.innerHTML = '';
      for (var i = 0; i < k; i++) { count++; await one(count); draw(); await wait(k > 1 ? 160 : 0); }
      busy = false;
    }
    root.querySelector('.one').addEventListener('click', function () { run(1); });
    root.querySelector('.burst').addEventListener('click', function () { run(15); });
    root.querySelector('[data-k="down"]').addEventListener('change', function (e) { payDown = e.target.checked; if (!payDown) line('Payments service recovered. The breaker will test it on its next half-open request.'); draw(); });
    root.querySelector('.reset').addEventListener('click', function () {
      if (busy) return;
      c = { ok: 0, e401: 0, e429: 0, e503: 0 }; tokens = 10; br = 'closed'; fails = 0; count = 0;
      log.innerHTML = '<p class="vk-muted">Send requests and watch the gateway and the circuit breaker. Then switch the payments service to failing.</p>'; draw();
    });
    draw();
  }

  function boot() {
    Array.prototype.forEach.call(document.querySelectorAll('.vk-k8scheck'), initK8s);
    Array.prototype.forEach.call(document.querySelectorAll('.vk-gitops'), initGitops);
    Array.prototype.forEach.call(document.querySelectorAll('.vk-apisim'), initApi);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
