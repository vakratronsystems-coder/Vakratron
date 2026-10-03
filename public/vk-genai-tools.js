/* vk-genai-tools.js: interactive tools for the LLM, RAG and agent pages.
   - .vk-llmcost   : hosted API vs self-hosted LLM monthly cost
   - .vk-ragflow   : animated retrieval flow with document permissions
   - .vk-agentloop : IT service desk agent with MCP tools, approval and a guardrail
   No dependencies. Styles live in vk-content.css. */
(function () {
  'use strict';
  function esc(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }
  var REDUCED = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function wait(ms) { return new Promise(function (r) { setTimeout(r, REDUCED ? ms * 0.3 : ms); }); }
  function inr(n) {
    if (n >= 1e7) return '₹' + (n / 1e7).toFixed(2) + ' Cr';
    if (n >= 1e5) return '₹' + (n / 1e5).toFixed(1) + ' L';
    return '₹' + Math.round(n).toLocaleString('en-IN');
  }

  /* ------------------------------------------------------------------ LLM cost calculator */
  var LF = [
    ['req', 'Requests per day', 20000, ''],
    ['tin', 'Average input tokens per request', 1500, 'Question plus any documents or history sent with it'],
    ['tout', 'Average output tokens per request', 400, 'Roughly 300 words'],
    ['pin', 'API price per million input tokens (US$)', 3, 'Typical list price for a large commercial model. Small models cost far less. Check current prices.'],
    ['pout', 'API price per million output tokens (US$)', 15, ''],
    ['fx', 'Exchange rate (₹ per US$)', 85, ''],
    ['gpus', 'Self-hosted: GPUs', 4, 'For example, a 70B-class open model at 8-bit on 2-GPU replicas'],
    ['gpucost', 'Self-hosted: cost per GPU per month (₹)', 150000, 'Owned and spread over 3 years with power and support, or rented. Roughly similar either way.'],
    ['ops', 'Self-hosted: people and tooling per month (₹)', 200000, 'Part of an engineer\'s time, monitoring, updates'],
    ['tps', 'Self-hosted: output tokens per second per GPU', 500, 'With batching (vLLM). Used only for the capacity check.']
  ];
  function initCost(root) {
    var h = '<div class="vk-tco-grid"><div class="vk-tco-in">';
    LF.forEach(function (f, i) {
      if (i === 0) h += '<h4>Your usage</h4>';
      if (i === 3) h += '<h4>Hosted API</h4>';
      if (i === 6) h += '<h4>Self-hosted open model</h4>';
      h += '<label><span>' + esc(f[1]) + '</span><input type="number" min="0" step="any" data-k="' + f[0] + '" value="' + f[2] + '">' + (f[3] ? '<em>' + esc(f[3]) + '</em>' : '') + '</label>';
    });
    h += '</div><div class="vk-tco-out" aria-live="polite"></div></div>';
    root.innerHTML = h;
    var out = root.querySelector('.vk-tco-out');
    function v(k) { var x = parseFloat(root.querySelector('[data-k="' + k + '"]').value); return isNaN(x) ? 0 : x; }
    function calc() {
      var days = 30, req = v('req');
      var api = (req * days * (v('tin') * v('pin') + v('tout') * v('pout')) / 1e6) * v('fx');
      var self = v('gpus') * v('gpucost') + v('ops');
      var perReqApi = req > 0 ? api / (req * days) : 0;
      var be = perReqApi > 0 ? Math.round(self / (perReqApi * days)) : 0;
      // capacity: assume the busiest hour carries 15% of daily traffic
      var peakTokPerSec = req * 0.15 * v('tout') / 3600;
      var cap = v('gpus') * v('tps');
      var max = Math.max(api, self) || 1;
      var verdict = api < self
        ? 'At this volume the <strong>hosted API is cheaper</strong> by about ' + inr(self - api) + ' a month. Self-hosting starts to pay off at roughly <strong>' + be.toLocaleString('en-IN') + ' requests a day</strong>, unless data rules require it anyway.'
        : '<strong>Self-hosting is cheaper</strong> by about ' + inr(api - self) + ' a month at this volume. Break-even is around <strong>' + be.toLocaleString('en-IN') + ' requests a day</strong>.';
      var capNote = peakTokPerSec > cap
        ? '<p class="vk-warn-line">Capacity check: the busiest hour needs about ' + Math.round(peakTokPerSec) + ' output tokens per second, more than ' + v('gpus') + ' GPUs can serve (~' + Math.round(cap) + '). Add GPUs, and the self-hosted cost goes up.</p>'
        : '<p class="vk-small vk-muted">Capacity check: the busiest hour needs about ' + Math.round(peakTokPerSec) + ' output tokens per second; ' + v('gpus') + ' GPUs give roughly ' + Math.round(cap) + '. OK.</p>';
      out.innerHTML = '<h4>Monthly cost</h4>' +
        '<div class="vk-cmp"><div class="r"><span class="l">Hosted API</span><span class="b"><i class="pub" style="width:' + (100 * api / max).toFixed(1) + '%"></i></span><span class="n">' + inr(api) + '</span></div>' +
        '<div class="r"><span class="l">Self-hosted</span><span class="b"><i class="pri" style="width:' + (100 * self / max).toFixed(1) + '%"></i></span><span class="n">' + inr(self) + '</span></div></div>' +
        '<p class="vk-tco-verdict">' + verdict + '</p>' + capNote +
        '<p class="vk-small vk-muted">Cost is only part of the decision. Data that may not leave your infrastructure, latency, and how much control you need over model versions often matter more. Taxes and setup effort are not included.</p>';
    }
    root.addEventListener('input', calc);
    calc();
  }

  /* ------------------------------------------------------------------ RAG flow */
  var DOCS = [
    { id: 'l26', t: 'Leave Policy 2026', who: ['emp', 'hr'], s: { leave: 0.92, pay: 0.10 } },
    { id: 'l23', t: 'Leave Policy 2023 (archived)', who: ['emp', 'hr'], old: true, s: { leave: 0.88, pay: 0.08 } },
    { id: 'hb', t: 'Employee Handbook', who: ['emp', 'hr'], s: { leave: 0.71, pay: 0.46 } },
    { id: 'tr', t: 'Travel Policy', who: ['emp', 'hr'], s: { leave: 0.33, pay: 0.22 } },
    { id: 'sb', t: 'Salary Bands 2026', who: ['hr'], s: { leave: 0.12, pay: 0.94 } },
    { id: 'cr', t: 'Compensation Review Guide', who: ['hr'], s: { leave: 0.18, pay: 0.82 } }
  ];
  var QS = {
    leave: 'How many days of annual leave do I get?',
    pay: 'What is the salary band for a senior engineer?'
  };
  var ANS = {
    leave: 'Full-time staff get <strong>24 days of annual leave</strong> a year, plus 12 days of sick leave. Up to 10 unused days can be carried into the next year.',
    payhr: 'The senior engineer band is <strong>Band E4</strong>. Offers above the midpoint need approval from the HR head.',
    payemp: 'I could not find this in the documents you have access to. For questions about pay, please contact HR.'
  };
  var STAGES = ['Question', 'Search', 'Permission check', 'Rank and freshness', 'Write the answer'];

  function initRag(root) {
    var busy = false;
    root.innerHTML =
      '<div class="vk-rag-ctl"><label>Signed in as ' +
      '<select data-k="who"><option value="emp">Employee</option><option value="hr">HR manager</option></select></label>' +
      '<label>Question <select data-k="q"><option value="leave">' + esc(QS.leave) + '</option><option value="pay">' + esc(QS.pay) + '</option></select></label>' +
      '<button type="button" class="vk-btn primary ask">&#9654; Ask</button></div>' +
      '<div class="vk-rag-stages">' + STAGES.map(function (s, i) { return '<div class="st" data-i="' + i + '"><span class="n">' + (i + 1) + '</span>' + esc(s) + '</div>'; }).join('') + '</div>' +
      '<div class="vk-rag-body"><div class="vk-rag-docs"><h4>Company documents</h4>' +
      DOCS.map(function (d) { return '<div class="doc" data-id="' + d.id + '"><span class="t">' + esc(d.t) + '</span><span class="a">' + (d.who.length === 1 ? 'HR only' : 'All staff') + '</span><span class="sc"></span></div>'; }).join('') +
      '</div><div class="vk-rag-ans"><h4>Answer</h4><div class="box"><p class="vk-muted">Choose who is asking and a question, then press Ask.</p></div><div class="note"></div></div></div>';
    var stages = root.querySelectorAll('.st'), box = root.querySelector('.vk-rag-ans .box'), note = root.querySelector('.vk-rag-ans .note');
    function sel(k) { return root.querySelector('[data-k="' + k + '"]').value; }
    function docEl(id) { return root.querySelector('.doc[data-id="' + id + '"]'); }
    function stage(i) { stages.forEach(function (s, j) { s.className = 'st' + (j < i ? ' done' : j === i ? ' on' : ''); }); }
    function reset() { root.querySelectorAll('.doc').forEach(function (d) { d.className = 'doc'; d.querySelector('.sc').textContent = ''; }); stage(-1); note.innerHTML = ''; }
    root.querySelector('.ask').addEventListener('click', async function () {
      if (busy) return; busy = true; this.disabled = true;
      reset();
      var who = sel('who'), q = sel('q');
      box.innerHTML = '<p>&ldquo;' + esc(QS[q]) + '&rdquo;</p>';
      stage(0); await wait(700);
      stage(1);
      var hits = DOCS.slice().sort(function (a, b) { return b.s[q] - a.s[q]; }).slice(0, 4);
      hits.forEach(function (d) { var e = docEl(d.id); e.classList.add('hit'); e.querySelector('.sc').textContent = 'match ' + Math.round(d.s[q] * 100) + '%'; });
      note.innerHTML = '<p>Search finds the 4 most relevant passages across all documents.</p>';
      await wait(1300);
      stage(2);
      var allowed = hits.filter(function (d) { return d.who.indexOf(who) >= 0; });
      hits.forEach(function (d) { if (d.who.indexOf(who) < 0) docEl(d.id).classList.add('blocked'); });
      note.innerHTML = hits.length > allowed.length
        ? '<p class="bad">' + (hits.length - allowed.length) + ' result(s) removed: this user is not allowed to see them. The model never receives them.</p>'
        : '<p>All results are documents this user is allowed to read.</p>';
      await wait(1400);
      stage(3);
      var ranked = allowed.filter(function (d) { return !d.old; }).filter(function (d) { return d.s[q] > 0.5; }).slice(0, 2);
      allowed.forEach(function (d) { if (d.old) docEl(d.id).classList.add('stale'); });
      ranked.forEach(function (d) { docEl(d.id).classList.add('pick'); });
      note.innerHTML += allowed.some(function (d) { return d.old; }) ? '<p class="warn">The archived 2023 policy is dropped in favour of the current one.</p>' : '';
      note.innerHTML += ranked.length ? '<p>The best ' + ranked.length + ' passage(s) are sent to the model, with their source.</p>' : '<p class="warn">Nothing relevant is left to answer from.</p>';
      await wait(1400);
      stage(4); await wait(900);
      var a = q === 'leave' ? ANS.leave : (who === 'hr' ? ANS.payhr : ANS.payemp);
      var cites = ranked.length ? '<div class="cites">' + ranked.map(function (d, i) { return '<span>[' + (i + 1) + '] ' + esc(d.t) + '</span>'; }).join('') + '</div>' : '';
      box.innerHTML = '<p class="q">&ldquo;' + esc(QS[q]) + '&rdquo;</p><p>' + a + '</p>' + cites;
      stage(5);
      busy = false; this.disabled = false;
    });
    root.addEventListener('change', function (e) { if (e.target.tagName === 'SELECT' && !busy) { reset(); box.innerHTML = '<p class="vk-muted">Press Ask.</p>'; } });
  }

  /* ------------------------------------------------------------------ agent loop */
  var SERVERS = [
    { id: 'dir', name: 'Directory', perm: 'read only' },
    { id: 'mon', name: 'Monitoring', perm: 'read only' },
    { id: 'vpn', name: 'VPN service', perm: 'renew certificates' },
    { id: 'idm', name: 'Access management', perm: 'changes need approval' },
    { id: 'tkt', name: 'Ticketing', perm: 'create and update' }
  ];
  function initAgent(root) {
    var state = 'idle';
    root.innerHTML =
      '<div class="vk-ag-req"><span class="k">Request from Priya (Finance)</span><p>&ldquo;My VPN keeps disconnecting, and I need access to the finance shared drive for the audit.&rdquo;</p></div>' +
      '<div class="vk-ag-body"><div class="vk-ag-log" aria-live="polite"><p class="vk-muted">Press <strong>Run agent</strong> to watch it work through the request.</p></div>' +
      '<div class="vk-ag-tools"><h4>Tools the agent can use (MCP servers)</h4>' +
      SERVERS.map(function (s) { return '<div class="srv" data-s="' + s.id + '"><span class="t">' + esc(s.name) + '</span><span class="p">' + esc(s.perm) + '</span></div>'; }).join('') +
      '<div class="srv blockedsrv" data-s="mfa"><span class="t">MFA settings</span><span class="p">not available to the agent</span></div></div></div>' +
      '<div class="vk-ag-ctl"><button type="button" class="vk-btn primary run">&#9654; Run agent</button><button type="button" class="vk-btn approve" disabled>Approve as manager</button><button type="button" class="vk-btn reject" disabled>Reject</button><button type="button" class="vk-btn reset">Reset</button></div>';
    var log = root.querySelector('.vk-ag-log'), run = root.querySelector('.run'), ap = root.querySelector('.approve'), rj = root.querySelector('.reject');
    function line(t, c) { var p = document.createElement('p'); p.className = c || ''; p.innerHTML = t; log.appendChild(p); log.scrollTop = log.scrollHeight; }
    function hit(id, cls) { var e = root.querySelector('[data-s="' + id + '"]'); if (!e) return; e.classList.add(cls || 'on'); setTimeout(function () { e.classList.remove('on'); }, 1200); }
    run.addEventListener('click', async function () {
      if (state !== 'idle') return; state = 'running'; run.disabled = true; log.innerHTML = '';
      line('<strong>Plan:</strong> two separate problems. 1) Fix the VPN. 2) Request access to the finance drive.', 'plan'); await wait(1100);
      line('&rarr; Directory: look up Priya&rsquo;s account and team.', 'call'); hit('dir'); await wait(1000);
      line('&larr; Active account, Finance team, manager: Rahul.', 'res'); await wait(800);
      line('&rarr; Monitoring: read VPN logs for her laptop.', 'call'); hit('mon'); await wait(1000);
      line('&larr; Connections drop every 20 minutes. Device certificate expired yesterday.', 'res'); await wait(900);
      line('&rarr; VPN service: renew the device certificate. Low risk, allowed without approval.', 'call'); hit('vpn'); await wait(1000);
      line('&#10003; Certificate renewed. Priya is asked to reconnect.', 'ok'); await wait(900);
      line('Thinking: the VPN would also be fixed by turning off multi-factor sign-in. Trying that.', 'plan'); await wait(1000);
      line('&#10007; Blocked by policy: changing MFA is not a tool this agent has. Nothing was changed.', 'bad'); hit('mfa', 'deny'); await wait(1200);
      line('&rarr; Access management: request read access to the finance drive.', 'call'); hit('idm'); await wait(900);
      line('&#9208; This changes access to financial data, so it needs a human. Waiting for Rahul (manager) to approve.', 'warn');
      state = 'waiting'; ap.disabled = false; rj.disabled = false;
    });
    async function decide(ok) {
      if (state !== 'waiting') return; state = 'running'; ap.disabled = true; rj.disabled = true;
      if (ok) {
        line('&#10003; Rahul approved: read-only access for 30 days.', 'ok'); await wait(800);
        line('&rarr; Access management: grant read access, expires in 30 days.', 'call'); hit('idm'); await wait(1000);
        line('&#10003; Access granted.', 'ok');
      } else {
        line('&#10007; Rahul rejected the request. No access was granted.', 'bad'); await wait(800);
      }
      await wait(600);
      line('&rarr; Ticketing: record everything that was done, and by whom.', 'call'); hit('tkt'); await wait(900);
      line('<strong>Done.</strong> Every tool call, the blocked action and the approval are in the audit log.', 'ok');
      state = 'done';
    }
    ap.addEventListener('click', function () { decide(true); });
    rj.addEventListener('click', function () { decide(false); });
    root.querySelector('.reset').addEventListener('click', function () {
      if (state === 'running') return;
      state = 'idle'; run.disabled = false; ap.disabled = true; rj.disabled = true;
      log.innerHTML = '<p class="vk-muted">Press <strong>Run agent</strong> to watch it work through the request.</p>';
    });
  }

  function boot() {
    Array.prototype.forEach.call(document.querySelectorAll('.vk-llmcost'), initCost);
    Array.prototype.forEach.call(document.querySelectorAll('.vk-ragflow'), initRag);
    Array.prototype.forEach.call(document.querySelectorAll('.vk-agentloop'), initAgent);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
