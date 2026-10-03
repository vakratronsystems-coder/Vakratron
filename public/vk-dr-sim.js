/* vk-dr-sim.js: interactive DR pattern simulator.
   Usage: <div class="vk-drsim" data-start="pilot-light"></div> + this script.
   No dependencies. Styles live in vk-content.css (.vk-drsim). */
(function () {
  'use strict';
  var C = { run: '#38bdf8', idle: '#38bdf8', build: '#f59e0b', down: '#ef4444', backup: '#a5b4fc', off: '#64748b', none: '#334155', flow: '#C2185B', text: '#e2e8f0', muted: '#94a3b8' };
  var LAYERS = [['web', 'Web servers'], ['app', 'Application servers'], ['db', 'Database'], ['data', 'Storage']];
  var ROW_Y = { web: 130, app: 200, db: 270, data: 340 };
  var REDUCED = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function S(style, cap, label) { return { style: style, cap: cap, label: label }; }
  function FULL(l) { return S('run', 1, l || '4 of 4 running'); }
  var PRIMARY = { web: FULL(), app: FULL(), db: S('run', 1, 'Primary, read-write'), data: S('run', 1, 'Production data') };

  var P = {
    'backup-restore': {
      name: 'Backup & restore', cost: 1, rpo: 'Hours (since the last backup)', rto: 'Hours to days',
      summary: 'Only backup copies are kept at the DR site. After a disaster, servers are built, data is restored from the last backup, and then the applications are started.',
      daily: 'Nothing runs at DR. It only stores backup copies.',
      dr: { web: S('none', 0, 'Not built yet'), app: S('none', 0, 'Not built yet'), db: S('none', 0, 'Not built yet'), data: S('backup', 1, 'Backup copies (last night)') },
      flows: [{ row: 'data', type: 'batch', label: ['Backup copy', 'once a night'] }],
      steps: [
        ['Disaster declared. Primary site is lost.', 900, function () { }],
        ['Servers built or rented at the DR site', 2200, function (s) { s.d.web = S('build', 0.4, 'Being built'); s.d.app = S('build', 0.4, 'Being built'); s.d.db = S('build', 0.4, 'Being built'); }],
        ['Data restored from the last backup', 3000, function (s) { s.d.db = S('build', 0.8, 'Restoring data...'); }],
        ['Database and applications started', 1600, function (s) { s.d.db = S('run', 1, 'Running (data up to last backup)'); s.d.app = FULL(); s.d.web = FULL(); }],
        ['Users switched to DR (DNS change)', 900, function (s) { s.traffic = 'dr'; }]
      ]
    },
    'pilot-light': {
      name: 'Pilot light', cost: 2, rpo: 'Minutes', rto: 'A few hours',
      summary: 'Data is replicated all the time and a small database copy runs at DR. Web and application servers exist only as ready templates and are switched on during a disaster.',
      daily: 'A small database replica and replicated storage. Web and app servers are off.',
      dr: { web: S('off', 0, 'Off (template ready)'), app: S('off', 0, 'Off (template ready)'), db: S('idle', 0.35, 'Small replica, read-only'), data: S('idle', 1, 'Replicated copy') },
      flows: [{ row: 'db', type: 'stream', label: ['Continuous', 'replication'] }, { row: 'data', type: 'stream', label: ['Volume', 'replication'] }],
      steps: [
        ['Disaster declared. Primary site is lost.', 800, function () { }],
        ['Database replica promoted to primary', 1000, function (s) { s.d.db = S('run', 0.35, 'Promoted, read-write'); }],
        ['Web and app servers started from templates', 2000, function (s) { s.d.web = S('build', 0.5, 'Starting...'); s.d.app = S('build', 0.5, 'Starting...'); }],
        ['Database scaled up, apps running', 1400, function (s) { s.d.db = S('run', 1, 'Primary, read-write'); s.d.app = FULL(); s.d.web = FULL(); }],
        ['Users switched to DR (DNS change)', 800, function (s) { s.traffic = 'dr'; }]
      ]
    },
    'warm-standby': {
      name: 'Warm standby', cost: 3, rpo: 'Seconds to minutes', rto: 'Under an hour to a few hours',
      summary: 'A complete copy of the application runs at the DR site, but at reduced size. On failover it is scaled up and users are pointed to it.',
      daily: 'The full stack at about a quarter of production size.',
      dr: { web: S('idle', 0.25, '1 of 4 running'), app: S('idle', 0.25, '1 of 4 running'), db: S('idle', 1, 'Replica, read-only'), data: S('idle', 1, 'Replicated copy') },
      flows: [{ row: 'db', type: 'stream', label: ['Continuous', 'replication'] }, { row: 'data', type: 'stream', label: ['Volume', 'replication'] }],
      steps: [
        ['Disaster declared. Primary site is lost.', 700, function () { }],
        ['Database replica promoted to primary', 800, function (s) { s.d.db = S('run', 1, 'Promoted, read-write'); }],
        ['Web and app tiers scaled from 1 to 4 servers', 1300, function (s) { s.d.web = S('build', 0.6, 'Scaling up...'); s.d.app = S('build', 0.6, 'Scaling up...'); }],
        ['All tiers at full size', 700, function (s) { s.d.web = FULL(); s.d.app = FULL(); }],
        ['Users switched to DR (DNS change)', 600, function (s) { s.traffic = 'dr'; }]
      ]
    },
    'active-passive': {
      name: 'Active-passive', cost: 4, rpo: 'Near zero (synchronous)', rto: 'Minutes',
      summary: 'A full-size copy of production waits at the DR site, kept in sync. If the primary fails, the passive site takes over.',
      daily: 'A full-size copy, ready but not serving users.',
      dr: { web: S('idle', 1, '4 of 4 on standby'), app: S('idle', 1, '4 of 4 on standby'), db: S('idle', 1, 'Synchronous replica'), data: S('idle', 1, 'Synchronous copy') },
      flows: [{ row: 'db', type: 'sync', label: ['Synchronous', 'replication'] }, { row: 'data', type: 'sync', label: ['Synchronous', 'replication'] }],
      steps: [
        ['Primary failure detected', 600, function () { }],
        ['DR database promoted to primary', 600, function (s) { s.d.db = S('run', 1, 'Promoted, read-write'); }],
        ['Standby servers take over', 500, function (s) { s.d.web = FULL('4 of 4 serving'); s.d.app = FULL('4 of 4 serving'); s.d.data = S('run', 1, 'Now primary'); }],
        ['Users switched to DR', 500, function (s) { s.traffic = 'dr'; }]
      ]
    },
    'active-active': {
      name: 'Active-active', cost: 5, rpo: 'Near zero', rto: 'Near zero for users',
      summary: 'Both sites serve users at the same time. If one site fails, the other already has users and simply carries the full load.',
      daily: 'Two full sites, both serving users, each at about half load.',
      primaryOverride: { web: FULL('Serving ~50% of users'), app: FULL('Serving ~50% of users'), db: S('run', 1, 'Read-write'), data: S('run', 1, 'Production data') },
      dr: { web: FULL('Serving ~50% of users'), app: FULL('Serving ~50% of users'), db: S('run', 1, 'Read-write'), data: S('run', 1, 'Production data') },
      traffic: 'both',
      flows: [{ row: 'db', type: 'bi', label: ['Two-way', 'replication'] }, { row: 'data', type: 'bi', label: ['Two-way', 'replication'] }],
      steps: [
        ['One site fails', 500, function () { }],
        ['Load balancer sends all users to the surviving site', 600, function (s) { s.traffic = 'dr'; s.d.web = FULL('Serving 100% of users'); s.d.app = FULL('Serving 100% of users'); }]
      ]
    }
  };
  var ORDER = ['backup-restore', 'pilot-light', 'warm-standby', 'active-passive', 'active-active'];

  function clone(o) { return JSON.parse(JSON.stringify(o)); }
  function esc(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }

  var GEO = {
    d: { vw: 900, vh: 420, px: [20, 520], pw: 360, bx: 30, bw: 300, ux: 370, uw: 160, f1: 15, f2: 12.5, ft: 14, short: false },
    m: { vw: 420, vh: 420, px: [6, 234], pw: 180, bx: 10, bw: 160, ux: 150, uw: 120, f1: 16, f2: 12.5, ft: 14, short: true }
  };
  var SHORT = { web: 'Web', app: 'App', db: 'Database', data: 'Storage' };

  function compSVG(G, side, layer, title, c) {
    var px = G.px[side === 'p' ? 0 : 1], x = px + G.bx, y = ROW_Y[layer], w = G.bw, h = 54;
    var col = C[c.style] || C.run, out = '';
    var dash = (c.style === 'none' || c.style === 'off' || c.style === 'build') ? ' stroke-dasharray="6 5"' : '';
    out += '<g opacity="' + (c.style === 'none' ? 0.6 : 1) + '"' + (c.style === 'build' ? ' class="vk-pulse"' : '') + '>';
    out += '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="8" fill="#0f172a" stroke="' + col + '" stroke-width="1.5"' + dash + (c.style === 'idle' ? ' stroke-opacity="0.45"' : '') + '/>';
    if (c.cap > 0) out += '<rect class="vk-cap" x="' + (x + 1) + '" y="' + (y + 1) + '" width="' + Math.max(0, (w - 2) * c.cap) + '" height="' + (h - 2) + '" rx="7" fill="' + col + '" opacity="' + (c.style === 'idle' ? 0.06 : c.style === 'down' ? 0.12 : 0.24) + '"/>';
    out += '<text x="' + (x + 12) + '" y="' + (y + 23) + '" font-size="' + G.f1 + '" font-weight="600" fill="' + (c.style === 'none' ? C.muted : C.text) + '">' + esc(G.short ? SHORT[layer] : title) + '</text>';
    out += '<text x="' + (x + 12) + '" y="' + (y + 43) + '" font-size="' + G.f2 + '" fill="' + (c.style === 'down' ? '#fca5a5' : C.muted) + '">' + esc(G.short ? shortLabel(c.label) : c.label) + '</text>';
    return out + '</g>';
  }
  function shortLabel(l) {
    return l.replace(' (template ready)', '').replace(' (last night)', '').replace(' (data up to last backup)', '').replace('Serving ~50% of users', '~50% of users').replace('Serving 100% of users', '100% of users')
      .replace(', read-only', '').replace(', read-write', '').replace('Synchronous ', 'Sync ').replace('Production data', 'Live data').replace(' on standby', ' standby');
  }

  function flowSVG(G, f, stopped) {
    var y = ROW_Y[f.row] + 27, out = '', cls = 'vk-flow vk-' + f.type + (stopped ? ' vk-stopped' : '');
    var x1 = G.px[0] + G.bx + G.bw + 2, x2 = G.px[1] + G.bx - 2, mid = (x1 + x2) / 2;
    if (f.type === 'bi') {
      out += '<line class="' + cls + '" x1="' + x1 + '" y1="' + (y - 5) + '" x2="' + x2 + '" y2="' + (y - 5) + '" stroke="' + C.flow + '" stroke-width="3"/>';
      out += '<line class="' + cls + ' vk-rev" x1="' + x2 + '" y1="' + (y + 5) + '" x2="' + x1 + '" y2="' + (y + 5) + '" stroke="' + C.flow + '" stroke-width="3"/>';
    } else {
      out += '<line x1="' + x1 + '" y1="' + y + '" x2="' + (x2 - 4) + '" y2="' + y + '" stroke="#1e293b" stroke-width="3"/>';
      out += '<line class="' + cls + '" x1="' + x1 + '" y1="' + y + '" x2="' + (x2 - 4) + '" y2="' + y + '" stroke="' + C.flow + '" stroke-width="3" marker-end="url(#vkah)"/>';
    }
    if (!G.short) f.label.forEach(function (l, i) {
      out += '<text x="' + mid + '" y="' + (y - 26 + i * 13) + '" text-anchor="middle" font-size="11" fill="' + (stopped ? '#475569' : C.muted) + '">' + esc(l) + '</text>';
    });
    if (stopped) out += '<text x="' + mid + '" y="' + (y + 24) + '" text-anchor="middle" font-size="11" fill="#fca5a5">' + (G.short ? 'stop' : 'stopped') + '</text>';
    return out;
  }

  function trafficSVG(G, target, on) {
    var x = G.px[target === 'p' ? 0 : 1] + G.pw / 2, cx = G.ux + G.uw / 2, sx = target === 'p' ? cx - 25 : cx + 25;
    return '<path class="' + (on ? 'vk-flow vk-traffic' : '') + '" d="M' + sx + ',56 V70 H' + x + ' V86" fill="none" stroke="' + (on ? '#e2e8f0' : '#334155') + '" stroke-width="2"' + (on ? '' : ' stroke-dasharray="4 5"') + ' marker-end="url(#vkah2)"/>';
  }

  function render(el, st, pat) {
    var G = el.clientWidth && el.clientWidth < 600 ? GEO.m : GEO.d;
    var down = st.primaryDown, drLive = st.traffic === 'dr';
    var pc = G.px[0] + G.pw / 2, dc = G.px[1] + G.pw / 2;
    var h = '<svg viewBox="0 0 ' + G.vw + ' ' + G.vh + '" role="img" aria-label="' + esc(pat.name + ' disaster recovery pattern diagram') + '">';
    h += '<defs><marker id="vkah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="' + C.flow + '"/></marker>';
    h += '<marker id="vkah2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#cbd5e1"/></marker></defs>';
    h += '<g font-family="Inter, sans-serif">';
    h += '<rect x="' + G.ux + '" y="10" width="' + G.uw + '" height="46" rx="10" fill="#111a2e" stroke="#475569"/><text x="' + (G.ux + G.uw / 2) + '" y="38" text-anchor="middle" font-size="15" font-weight="600" fill="' + C.text + '">Users</text>';
    h += trafficSVG(G, 'p', !down && (st.traffic === 'primary' || st.traffic === 'both'));
    h += trafficSVG(G, 'd', drLive || st.traffic === 'both');
    h += '<rect x="' + G.px[0] + '" y="90" width="' + G.pw + '" height="318" rx="12" fill="#0b1224" stroke="' + (down ? C.down : '#334155') + '" stroke-width="' + (down ? 2 : 1) + '"/>';
    h += '<rect x="' + G.px[1] + '" y="90" width="' + G.pw + '" height="318" rx="12" fill="#0b1224" stroke="' + (drLive ? C.run : '#334155') + '" stroke-width="' + (drLive ? 2 : 1) + '"/>';
    h += '<text x="' + pc + '" y="116" text-anchor="middle" font-size="' + G.ft + '" font-weight="700" fill="' + (down ? '#fca5a5' : '#fff') + '">' + (down ? (G.short ? 'Primary: DOWN' : 'Primary site: DOWN') : 'Primary site') + '</text>';
    h += '<text x="' + dc + '" y="116" text-anchor="middle" font-size="' + G.ft + '" font-weight="700" fill="#fff">' + (drLive ? (G.short ? 'DR: serving users' : 'DR site: now serving users') : 'DR site') + '</text>';
    LAYERS.forEach(function (L) {
      h += compSVG(G, 'p', L[0], L[1], down ? S('down', 0.3, 'Unavailable') : st.p[L[0]]);
      h += compSVG(G, 'd', L[0], L[1], st.d[L[0]]);
    });
    pat.flows.forEach(function (f) { h += flowSVG(G, f, down); });
    if (down) { var bx = G.px[0] + G.pw - 14; h += '<g class="vk-boom"><circle cx="' + bx + '" cy="100" r="13" fill="' + C.down + '"/><text x="' + bx + '" y="105" text-anchor="middle" font-size="15" font-weight="700" fill="#fff">!</text></g>'; }
    el.innerHTML = h + '</g></svg>';
  }

  function dots(n) { var s = ''; for (var i = 1; i <= 5; i++) s += '<span class="' + (i <= n ? 'on' : '') + '"></span>'; return s; }

  function init(root) {
    var only = root.getAttribute('data-only');
    var cur = only || root.getAttribute('data-start') || 'pilot-light', run = 0, st;
    root.innerHTML =
      '<div class="vk-drsim-tabs" role="tablist" aria-label="DR patterns"></div>' +
      '<div class="vk-drsim-body"><div class="vk-drsim-fig"><div class="vk-drsim-svg"></div>' +
      '<div class="vk-drsim-legend"><span><i class="l-run"></i>Running</span><span><i class="l-idle"></i>Standby or reduced size</span><span><i class="l-off"></i>Off or not built</span><span><i class="l-build"></i>Being started</span><span><i class="l-flow"></i>Data copy</span></div></div>' +
      '<div class="vk-drsim-side"><div class="vk-drsim-info"><h3 class="vk-drsim-name"></h3><p class="vk-drsim-sum"></p>' +
      '<div class="vk-drsim-kv"><div><span class="k">Running at DR every day</span><span class="v vk-drsim-daily"></span></div>' +
      '<div><span class="k">Data you could lose (RPO)</span><span class="v vk-drsim-rpo"></span></div>' +
      '<div><span class="k">Time to recover (RTO)</span><span class="v vk-drsim-rto"></span></div>' +
      '<div><span class="k">Relative cost</span><span class="v vk-dots"></span></div></div></div>' +
      '<div class="vk-drsim-run"><div class="vk-drsim-btns"><button type="button" class="vk-btn primary vk-drsim-go">&#9654; Simulate a disaster</button><button type="button" class="vk-btn vk-drsim-reset">Reset</button></div>' +
      '<ol class="vk-drsim-steps" aria-live="polite"></ol></div></div></div>';
    var tabs = root.querySelector('.vk-drsim-tabs');
    if (only) tabs.style.display = 'none';
    ORDER.forEach(function (k) {
      var b = document.createElement('button');
      b.type = 'button'; b.textContent = P[k].name; b.setAttribute('role', 'tab'); b.setAttribute('data-k', k);
      b.addEventListener('click', function () { select(k); });
      tabs.appendChild(b);
    });
    var svgEl = root.querySelector('.vk-drsim-svg'), stepsEl = root.querySelector('.vk-drsim-steps'), go = root.querySelector('.vk-drsim-go');

    function baseState(k) {
      var p = P[k];
      return { p: clone(p.primaryOverride || PRIMARY), d: clone(p.dr), traffic: p.traffic || 'primary', primaryDown: false };
    }
    function select(k) {
      cur = k; run++; st = baseState(k);
      var p = P[k];
      Array.prototype.forEach.call(tabs.children, function (b) {
        var on = b.getAttribute('data-k') === k;
        b.classList.toggle('on', on); b.setAttribute('aria-selected', on ? 'true' : 'false');
      });
      root.querySelector('.vk-drsim-name').textContent = p.name;
      root.querySelector('.vk-drsim-sum').textContent = p.summary;
      root.querySelector('.vk-drsim-daily').textContent = p.daily;
      root.querySelector('.vk-drsim-rpo').textContent = p.rpo;
      root.querySelector('.vk-drsim-rto').textContent = p.rto;
      root.querySelector('.vk-dots').innerHTML = dots(p.cost);
      stepsEl.innerHTML = '<li class="hint">Press <strong>Simulate a disaster</strong> to see what happens when the primary site is lost.</li>';
      go.disabled = false;
      render(svgEl, st, p);
    }
    function simulate() {
      var p = P[cur], my = ++run, i = 0, speed = REDUCED ? 0.3 : 1;
      st = baseState(cur);
      st.primaryDown = true;
      st.traffic = 'none';
      go.disabled = true;
      stepsEl.innerHTML = p.steps.map(function (s) { return '<li>' + esc(s[0]) + '</li>'; }).join('') + '<li class="result"></li>';
      var lis = stepsEl.querySelectorAll('li');
      render(svgEl, st, p);
      (function next() {
        if (my !== run) return;
        if (i > 0) { lis[i - 1].className = 'done'; p.steps[i - 1][2](st); render(svgEl, st, p); }
        if (i === p.steps.length) {
          var r = lis[lis.length - 1];
          r.className = 'result show';
          r.innerHTML = '<strong>Service restored at DR.</strong> Data lost: ' + esc(p.rpo.toLowerCase()) + '. Downtime: ' + esc(p.rto.toLowerCase()) + '.';
          go.disabled = false;
          return;
        }
        lis[i].className = 'active';
        var d = p.steps[i][1] * speed;
        i++;
        setTimeout(next, d);
      })();
    }
    var rt; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { render(svgEl, st, P[cur]); }, 150); });
    go.addEventListener('click', simulate);
    root.querySelector('.vk-drsim-reset').addEventListener('click', function () { select(cur); });
    select(cur);
  }

  function boot() { Array.prototype.forEach.call(document.querySelectorAll('.vk-drsim'), init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
