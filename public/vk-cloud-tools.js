/* vk-cloud-tools.js: interactive tools for the cloud pages.
   - .vk-placer   : "Where should this workload run?" advisor
   - .vk-wavesim  : VMware to KVM migration wave simulator
   - .vk-tco      : private vs public cloud cost calculator
   No dependencies. Styles live in vk-content.css. */
(function () {
  'use strict';
  function esc(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }
  var REDUCED = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ------------------------------------------------------------------ placement advisor */
  var Q = [
    { q: 'Where must the data stay?', o: [
      ['Anywhere, no restriction', { pub: 2 }, 'No data-location rule, so public cloud is fully open to you.'],
      ['In India, with a provider we trust', { pub: 1, pri: 1, hyb: 1 }, 'Several public clouds have Indian regions, but some workloads may still need to stay on your own platform.'],
      ['On our own premises or a named data centre', { pri: 3, hyb: 1 }, 'A strict location rule points to a private platform for this data.']] },
    { q: 'How steady is the load?', o: [
      ['Steady, around the clock', { pri: 2, hyb: 1 }, 'Steady 24x7 load is where owned capacity usually costs less over three to five years.'],
      ['Growing steadily', { hyb: 2, pri: 1, pub: 1 }, 'Steady growth suits a private base with public cloud for the overflow.'],
      ['Spiky or seasonal', { pub: 2, hyb: 2 }, 'Spikes are what public cloud is best at: pay for the peak only while it lasts.']] },
    { q: 'Does the application need anything unusual?', o: [
      ['No, it runs on standard Linux or Windows VMs', { pub: 1 }, 'Standard VMs move easily, so the choice is mostly about cost and control.'],
      ['Some parts are tied to specific hardware or licences', { hyb: 2 }, 'Mixed requirements usually end in a hybrid split.'],
      ['Yes, legacy OS, appliances or licences tied to our hardware', { pri: 2, hyb: 1 }, 'Legacy and hardware-bound parts are easier to keep on a platform you control.']] },
    { q: 'Who will run the platform day to day?', o: [
      ['We have a strong infrastructure team', { pri: 2, hyb: 1 }, 'A capable operations team is what makes a private cloud work well.'],
      ['A small team that needs some help', { hyb: 2 }, 'A small team often does best running the steady core and using managed public services for the rest.'],
      ['We would rather not run infrastructure', { pub: 3 }, 'If you do not want to run infrastructure, public cloud managed services remove most of that work.']] },
    { q: 'How fast do you need new capacity?', o: [
      ['Within minutes', { pub: 2, hyb: 1 }, 'Capacity in minutes, without buying hardware, is a public cloud strength.'],
      ['Within days', { hyb: 1, pri: 1 }, 'Days is achievable on either model with some spare capacity planned in.'],
      ['Weeks is fine, we plan ahead', { pri: 2 }, 'If you plan capacity ahead, buying hardware is not a constraint.']] }
  ];
  var MODEL = {
    pri: { name: 'Private cloud', url: '/solutions/cloud/private-cloud-openstack', blurb: 'Run this workload on a private cloud you own or control, such as OpenStack on KVM.' },
    pub: { name: 'Public cloud', url: '/solutions/cloud/multi-cloud-landing-zone', blurb: 'Run this workload in a public cloud such as AWS, Azure or OCI, inside a well-governed landing zone.' },
    hyb: { name: 'Hybrid cloud', url: '/solutions/cloud/hybrid-cloud', blurb: 'Keep the steady core on your own platform and use public cloud where it is stronger.' }
  };

  function initPlacer(root) {
    var ans = [];
    var h = '<div class="vk-placer-qs">';
    Q.forEach(function (q, i) {
      h += '<fieldset class="vk-q"><legend><span class="vk-num">' + (i + 1) + '</span> ' + esc(q.q) + '</legend>';
      q.o.forEach(function (o, j) {
        h += '<label><input type="radio" name="vkq' + i + '" value="' + j + '"> <span>' + esc(o[0]) + '</span></label>';
      });
      h += '</fieldset>';
    });
    h += '</div><div class="vk-placer-out" aria-live="polite"><p class="vk-muted">Answer the questions to see a suggested starting point.</p></div>';
    root.innerHTML = h;
    var out = root.querySelector('.vk-placer-out');
    root.addEventListener('change', function (e) {
      if (!e.target.name) return;
      ans[+e.target.name.slice(3)] = +e.target.value;
      var answered = ans.filter(function (a) { return a !== undefined; }).length;
      var s = { pri: 0, pub: 0, hyb: 0 }, reasons = [];
      Q.forEach(function (q, i) {
        if (ans[i] === undefined) return;
        var o = q.o[ans[i]]; for (var k in o[1]) s[k] += o[1][k]; reasons.push(o[2]);
      });
      if (answered < Q.length) {
        out.innerHTML = '<p class="vk-muted">' + answered + ' of ' + Q.length + ' answered. Keep going to see a suggestion.</p>';
        return;
      }
      var best = 'hyb';
      if (s.pri > s[best]) best = 'pri';
      if (s.pub > s[best]) best = 'pub';
      var total = s.pri + s.pub + s.hyb;
      var bars = ['pri', 'hyb', 'pub'].map(function (k) {
        var pct = Math.round(100 * s[k] / total);
        return '<div class="vk-bar-row' + (k === best ? ' on' : '') + '"><span class="l">' + MODEL[k].name + '</span><span class="b"><i style="width:' + pct + '%"></i></span><span class="n">' + s[k] + '</span></div>';
      }).join('');
      out.innerHTML = '<span class="vk-eyebrow">Suggested starting point</span><h3>' + MODEL[best].name + '</h3><p>' + MODEL[best].blurb + '</p>' +
        '<div class="vk-bars">' + bars + '</div><p><strong>Why:</strong></p><ul>' + reasons.map(function (r) { return '<li>' + esc(r) + '</li>'; }).join('') + '</ul>' +
        '<p class="vk-small vk-muted">This is a starting point for a conversation, not a final answer. Real decisions also depend on cost, contracts and how the application is built.</p>' +
        '<a class="vk-btn primary" href="' + MODEL[best].url + '">See the ' + MODEL[best].name.toLowerCase() + ' design &rarr;</a>';
    });
  }

  /* ------------------------------------------------------------------ VMware to KVM wave simulator */
  var APPS = [
    { id: 'pilot', name: 'Pilot: test and tools', n: 3, col: '#94a3b8' },
    { id: 'intra', name: 'Intranet and file servers', n: 4, col: '#38bdf8' },
    { id: 'hr', name: 'HR and payroll', n: 4, col: '#a78bfa' },
    { id: 'crm', name: 'CRM', n: 5, col: '#f472b6' },
    { id: 'erp', name: 'ERP (database last)', n: 6, col: '#fbbf24' }
  ];
  var WAVES = [
    { app: 'pilot', fail: false, note: 'Low-risk servers first, to prove the conversion process and tooling.' },
    { app: 'intra', fail: false, note: 'Simple, well-understood workloads build confidence.' },
    { app: 'hr', fail: true, note: 'Payroll depends on a licence server, so it gets extra testing.' },
    { app: 'crm', fail: false, note: 'App, web and database for CRM move together so no live dependency is split.' },
    { app: 'erp', fail: false, note: 'The most critical system goes last, once the team has done four waves.' }
  ];
  var STEPS = [['Replicate and convert (virt-v2v)', 1400], ['Test run on KVM, side by side', 1400], ['Cutover in maintenance window', 1000]];

  function initWave(root) {
    var vms = [], wave = 0, busy = false, retried = {};
    APPS.forEach(function (a) { for (var i = 0; i < a.n; i++) vms.push({ app: a.id, col: a.col, where: 'v', st: '' }); });
    root.innerHTML =
      '<div class="vk-wave-board"><div class="vk-wave-side"><h4>VMware vSphere (source)</h4><div class="vk-vms" data-s="v"></div><p class="vk-wave-foot vk-small vk-muted">Stays live as the rollback until every wave is signed off.</p></div>' +
      '<div class="vk-wave-mid"><div class="vk-wave-arrow"><span>virt-v2v</span></div></div>' +
      '<div class="vk-wave-side"><h4>KVM / OpenStack (target)</h4><div class="vk-vms" data-s="k"></div><p class="vk-wave-foot vk-small vk-muted">Validated before any users move.</p></div></div>' +
      '<div class="vk-wave-legend">' + APPS.map(function (a) { return '<span><i style="background:' + a.col + '"></i>' + esc(a.name) + '</span>'; }).join('') + '</div>' +
      '<div class="vk-wave-ctl"><button type="button" class="vk-btn primary vk-wave-next">&#9654; Run wave 1</button><button type="button" class="vk-btn vk-wave-reset">Reset</button><span class="vk-wave-prog vk-small vk-muted"></span></div>' +
      '<div class="vk-wave-log" aria-live="polite"><p class="vk-muted">Press <strong>Run wave 1</strong>. Each wave moves one group of related servers: convert, test side by side, then cut over.</p></div>';
    var V = root.querySelector('[data-s="v"]'), K = root.querySelector('[data-s="k"]');
    var next = root.querySelector('.vk-wave-next'), log = root.querySelector('.vk-wave-log'), prog = root.querySelector('.vk-wave-prog');

    function draw() {
      V.innerHTML = ''; K.innerHTML = '';
      vms.forEach(function (vm) {
        var d = document.createElement('span');
        d.className = 'vk-vm ' + vm.st; d.style.setProperty('--c', vm.col);
        (vm.where === 'v' ? V : K).appendChild(d);
        if (vm.st === 'copy' || vm.st === 'test') { var g = d.cloneNode(); g.className = 'vk-vm ghost ' + vm.st; K.appendChild(g); }
      });
      prog.textContent = 'Waves done: ' + wave + ' of ' + WAVES.length;
    }
    function setApp(app, fn) { vms.forEach(function (vm) { if (vm.app === app) fn(vm); }); }
    function line(html, cls) { var p = document.createElement('p'); p.className = cls || ''; p.innerHTML = html; log.appendChild(p); log.scrollTop = log.scrollHeight; }
    function wait(ms) { return new Promise(function (r) { setTimeout(r, REDUCED ? ms * 0.3 : ms); }); }

    async function runWave() {
      if (busy || wave >= WAVES.length) return;
      busy = true; next.disabled = true;
      var w = WAVES[wave], app = APPS.filter(function (a) { return a.id === w.app; })[0];
      if (wave === 0) log.innerHTML = '';
      line('<strong>Wave ' + (wave + 1) + ': ' + esc(app.name) + '</strong> (' + app.n + ' VMs). ' + esc(w.note.split('.')[0]) + '.', 'h');
      setApp(w.app, function (vm) { vm.st = 'copy'; }); draw(); line(STEPS[0][0] + '...'); await wait(STEPS[0][1]);
      setApp(w.app, function (vm) { vm.st = 'test'; }); draw(); line(STEPS[1][0] + '...'); await wait(STEPS[1][1]);
      if (w.fail && !retried[w.app]) {
        retried[w.app] = true;
        setApp(w.app, function (vm) { vm.st = 'fail'; }); draw();
        line('&#10007; Test failed: licence server bound to the old MAC address. Users never moved.', 'bad');
        await wait(1200);
        setApp(w.app, function (vm) { vm.st = ''; }); draw();
        line('&#8634; Rolled back: the VMware copy is still the live one. Fix the licence binding, then retry.', 'warn');
        await wait(1200);
        line('Retrying wave ' + (wave + 1) + '...');
        setApp(w.app, function (vm) { vm.st = 'copy'; }); draw(); await wait(STEPS[0][1] * 0.7);
        setApp(w.app, function (vm) { vm.st = 'test'; }); draw(); await wait(STEPS[1][1] * 0.7);
      }
      line(STEPS[2][0] + '...'); await wait(STEPS[2][1]);
      setApp(w.app, function (vm) { vm.where = 'k'; vm.st = 'done'; }); draw();
      line('&#10003; Wave ' + (wave + 1) + ' signed off. Source VMs kept powered off for two weeks as a safety net.', 'ok');
      wave++;
      if (wave === WAVES.length) {
        line('<strong>All waves complete.</strong> After the final sign-off period, the VMware environment is decommissioned and its licences are not renewed.', 'ok');
        next.textContent = 'Migration complete';
      } else {
        next.innerHTML = '&#9654; Run wave ' + (wave + 1);
        next.disabled = false;
      }
      draw(); busy = false;
    }
    next.addEventListener('click', runWave);
    root.querySelector('.vk-wave-reset').addEventListener('click', function () {
      if (busy) return;
      wave = 0; retried = {}; vms.forEach(function (vm) { vm.where = 'v'; vm.st = ''; });
      next.disabled = false; next.innerHTML = '&#9654; Run wave 1';
      log.innerHTML = '<p class="vk-muted">Press <strong>Run wave 1</strong>. Each wave moves one group of related servers: convert, test side by side, then cut over.</p>';
      draw();
    });
    draw();
  }

  /* ------------------------------------------------------------------ TCO calculator */
  var F = [
    ['vms', 'Number of VMs', 120, 'Average size assumed: 4 vCPU, 16 GB RAM'],
    ['stor', 'Storage needed (TB, usable)', 40, ''],
    ['years', 'Period (years)', 5, '3 or 5 years is typical'],
    ['pubvm', 'Public cloud: price per VM per month (₹)', 12000, 'On-demand list price for a 4 vCPU / 16 GB VM in an Indian region is roughly in this range. Reserved or committed pricing is lower.'],
    ['pubdisc', 'Public cloud: discount from commitments (%)', 30, 'Savings plans or reserved instances'],
    ['pubstor', 'Public cloud: storage per TB per month (₹)', 8000, 'Block storage, SSD class'],
    ['pubegress', 'Public cloud: data transfer out per month (₹)', 50000, 'Often forgotten, and it grows'],
    ['srv', 'Private: price per server (₹)', 1500000, 'Dual-socket server with enough RAM for ~25 such VMs'],
    ['vmper', 'Private: VMs per server', 25, ''],
    ['storcost', 'Private: storage per usable TB (₹, one-time)', 50000, 'Ceph with three copies of the data'],
    ['rack', 'Private: colocation per rack per month (₹)', 100000, 'Space, power and cooling, about 8 servers per rack'],
    ['sw', 'Private: support and software per server per year (₹)', 150000, 'Hardware support, OS and platform subscriptions'],
    ['fte', 'Private: extra people (full-time staff)', 2, ''],
    ['ftecost', 'Private: cost per person per year (₹)', 2500000, '']
  ];
  function fmt(n) {
    if (n >= 1e7) return '₹' + (n / 1e7).toFixed(2) + ' Cr';
    if (n >= 1e5) return '₹' + (n / 1e5).toFixed(1) + ' L';
    return '₹' + Math.round(n).toLocaleString('en-IN');
  }
  function initTco(root) {
    var h = '<div class="vk-tco-grid"><div class="vk-tco-in">';
    F.forEach(function (f, i) {
      if (i === 0) h += '<h4>Your workload</h4>';
      if (i === 3) h += '<h4>Public cloud</h4>';
      if (i === 7) h += '<h4>Private cloud</h4>';
      h += '<label><span>' + esc(f[1]) + '</span><input type="number" min="0" step="any" data-k="' + f[0] + '" value="' + f[2] + '">' + (f[3] ? '<em>' + esc(f[3]) + '</em>' : '') + '</label>';
    });
    h += '</div><div class="vk-tco-out" aria-live="polite"></div></div>';
    root.innerHTML = h;
    var out = root.querySelector('.vk-tco-out');
    function v(k) { var el = root.querySelector('[data-k="' + k + '"]'); var x = parseFloat(el.value); return isNaN(x) ? 0 : x; }
    function calc() {
      var years = Math.max(1, Math.min(10, Math.round(v('years'))));
      var vms = v('vms');
      var pubYear = 12 * (vms * v('pubvm') * (1 - v('pubdisc') / 100) + v('stor') * v('pubstor') + v('pubegress'));
      var servers = Math.ceil(vms / Math.max(1, v('vmper'))) + 1 + 3; // +1 spare, +3 control nodes
      var racks = Math.ceil(servers / 8) + Math.ceil(v('stor') / 200);
      var capex = servers * v('srv') + v('stor') * v('storcost');
      var priYear = 12 * racks * v('rack') + servers * v('sw') + v('fte') * v('ftecost');
      var pub = [], pri = [], be = null;
      for (var y = 1; y <= years; y++) {
        pub.push(pubYear * y);
        pri.push(capex + priYear * y);
        if (be === null && pri[y - 1] <= pub[y - 1]) be = y;
      }
      var max = Math.max(pub[years - 1], pri[years - 1]) || 1;
      var rows = '';
      for (var i = 0; i < years; i++) {
        rows += '<div class="vk-tco-yr"><span class="y">Year ' + (i + 1) + '</span><div class="bars">' +
          '<span class="b pub" style="width:' + (100 * pub[i] / max).toFixed(1) + '%"><em>' + fmt(pub[i]) + '</em></span>' +
          '<span class="b pri" style="width:' + (100 * pri[i] / max).toFixed(1) + '%"><em>' + fmt(pri[i]) + '</em></span></div></div>';
      }
      var diff = pub[years - 1] - pri[years - 1];
      var verdict = diff > 0
        ? 'Over ' + years + ' years, private cloud comes out about <strong>' + fmt(diff) + '</strong> cheaper on these assumptions' + (be ? ', breaking even in year ' + be + '.' : '.')
        : 'Over ' + years + ' years, public cloud comes out about <strong>' + fmt(-diff) + '</strong> cheaper on these assumptions.';
      out.innerHTML = '<h4>Cumulative cost</h4><div class="vk-tco-legend"><span><i class="pub"></i>Public cloud</span><span><i class="pri"></i>Private cloud</span></div>' + rows +
        '<p class="vk-tco-verdict">' + verdict + '</p>' +
        '<p class="vk-small vk-muted">Private estimate assumes ' + servers + ' servers (including 3 control nodes and 1 spare) in ' + racks + ' rack(s), bought in year 1. Not included: migration effort, network links, DR, hardware refresh after 5 years, and taxes. Replace every default with your own quotes before using this for a decision.</p>';
    }
    root.addEventListener('input', calc);
    calc();
  }

  function boot() {
    Array.prototype.forEach.call(document.querySelectorAll('.vk-placer'), initPlacer);
    Array.prototype.forEach.call(document.querySelectorAll('.vk-wavesim'), initWave);
    Array.prototype.forEach.call(document.querySelectorAll('.vk-tco'), initTco);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
