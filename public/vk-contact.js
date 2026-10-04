/* Contact page: 4-step enquiry. Posts to /api/contact with the SAME core fields
   (name, email, phone, company, reason) the email + Google Sheet automation uses.
   Extra fields (stage, timeline, orgType, role, message, sourcePage) are optional. */
(function () {
  var root = document.getElementById('vk-contact');
  if (!root) return;
  var form = document.getElementById('cfForm');
  var steps = root.querySelectorAll('.vk-cf-step');
  var back = document.getElementById('cfBack'), next = document.getElementById('cfNext'), send = document.getElementById('cfSend');
  var bar = document.getElementById('cfBar'), stepNo = document.getElementById('cfStepNo');
  var msg = document.getElementById('cfMsg'), msgCount = document.getElementById('cfMsgCount');
  var hintsBox = document.getElementById('cfHints');
  var loadedAt = Date.now();
  function getToken() {
    return fetch('/api/form-token', { cache: 'no-store' }).then(function (r) { return r.json(); })
      .then(function (d) { return d && d.token; }).catch(function () { return null; });
  }
  var tokenP = getToken();
  var cur = 1;
  var sel = { reason: '', reasonKey: '', stage: '', timeline: '', orgType: '' };

  var HINTS = {
    ai: ['Model size (for example 70B)', 'Training or inference?', 'Number of users', 'On-premises or cloud?'],
    dr: ['Number of critical applications', 'Target RTO and RPO', 'Current backup tool', 'Is a second site available?'],
    cloud: ['Number of VMs', 'Current platform', 'Public cloud already in use?', 'Data residency needs'],
    vmware: ['Number of VMs and hosts', 'Licence renewal date', 'Storage type', 'Downtime allowed'],
    llm: ['Use case', 'How sensitive is the data?', 'Users per day', 'API or self-hosted?'],
    rag: ['Document types', 'Roughly how many documents', 'Who may see what?', 'Languages'],
    agents: ['Task to automate', 'Systems it must touch', 'Human approval needed?', 'Volume per day'],
    k8s: ['Number of applications', 'How you deploy today', 'Clusters today', 'Cloud or on-premises?'],
    api: ['Who calls the APIs', 'Calls per day', 'Current stack', 'Security requirements'],
    tender: ['Buyer or department type', 'Bid deadline', 'Scope in one line', 'Budget range'],
    review: ['What needs reviewing', 'Vendor or SI involved', 'Decision deadline'],
    other: ['What you are trying to do', 'Deadline']
  };
  var REF = [[/dc-dr|dr-|disaster/, 'dr'], [/vmware/, 'vmware'], [/cloud/, 'cloud'], [/ai-infra|ai-gpu|gpu/, 'ai'],
             [/\/llm|enterprise-llm|claims/, 'llm'], [/rag|hr-policy/, 'rag'], [/agent/, 'agents'],
             [/k8s|kubernetes/, 'k8s'], [/\/api|microservices|partner-api/, 'api']];

  var sourcePage = '';
  try {
    if (document.referrer) {
      var r = new URL(document.referrer);
      if (r.host === location.host) sourcePage = r.pathname;
    }
  } catch (e) {}
  var qTopic = '';
  try { qTopic = new URLSearchParams(location.search).get('topic') || ''; } catch (e) {}

  function chipsOf(group) { return root.querySelectorAll('.vk-chip[data-group="' + group + '"]'); }
  function pick(btn) {
    var g = btn.getAttribute('data-group');
    var already = btn.getAttribute('aria-pressed') === 'true';
    chipsOf(g).forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
    if (already && g !== 'reason') { sel[g] = ''; return; }
    btn.setAttribute('aria-pressed', 'true');
    sel[g] = btn.getAttribute('data-value');
    if (g === 'reason') { sel.reasonKey = btn.getAttribute('data-key'); renderHints(); hideErr(1); }
  }
  root.addEventListener('click', function (e) {
    var b = e.target.closest('.vk-chip');
    if (!b || !root.contains(b)) return;
    e.preventDefault();
    pick(b);
    if (b.getAttribute('data-group') === 'reason' && cur === 1) setTimeout(function () { go(2); }, 220);
  });

  function preselect(key) {
    var b = root.querySelector('.vk-chip[data-group="reason"][data-key="' + key + '"]');
    if (b) pick(b);
  }
  if (qTopic) preselect(qTopic);
  else if (sourcePage) { for (var i = 0; i < REF.length; i++) { if (REF[i][0].test(sourcePage)) { preselect(REF[i][1]); break; } } }

  function renderHints() {
    var list = HINTS[sel.reasonKey] || HINTS.other;
    hintsBox.innerHTML = '';
    list.forEach(function (h) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'vk-hint'; b.textContent = '+ ' + h;
      b.addEventListener('click', function () {
        var v = msg.value;
        if (v && !/\n$/.test(v)) v += '\n';
        msg.value = v + h + ': ';
        b.classList.add('used');
        msg.focus();
        msg.setSelectionRange(msg.value.length, msg.value.length);
        count();
      });
      hintsBox.appendChild(b);
    });
  }
  renderHints();
  function count() { msgCount.textContent = msg.value.length; }
  msg.addEventListener('input', count);

  function hideErr(n) { var e = root.querySelector('[data-err="' + n + '"]'); if (e) e.classList.remove('on'); }
  function showErr(n, text) { var e = root.querySelector('[data-err="' + n + '"]'); if (!e) return; if (text) e.textContent = text; e.classList.add('on'); }

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function summary() {
    var parts = [['Topic', sel.reason, 1], ['Stage', sel.stage, 2], ['When', sel.timeline, 2], ['You are', sel.orgType, 2]];
    var h = parts.filter(function (p) { return p[1]; }).map(function (p) {
      return '<button type="button" class="vk-cf-sum" data-goto="' + p[2] + '"><span>' + p[0] + '</span>' + esc(p[1]) + ' <em>edit</em></button>';
    }).join('');
    if (msg.value.trim()) h += '<button type="button" class="vk-cf-sum" data-goto="3"><span>Note</span>' + esc(msg.value.trim().slice(0, 60)) + (msg.value.trim().length > 60 ? '&hellip;' : '') + ' <em>edit</em></button>';
    document.getElementById('cfSummary').innerHTML = h;
  }
  root.addEventListener('click', function (e) {
    var s = e.target.closest('.vk-cf-sum');
    if (s) { e.preventDefault(); go(+s.getAttribute('data-goto')); }
  });

  function go(n) {
    if (n > cur && cur === 1 && !sel.reason) { showErr(1); return; }
    cur = Math.max(1, Math.min(4, n));
    steps.forEach(function (s) { s.classList.toggle('on', +s.getAttribute('data-step') === cur); });
    stepNo.textContent = cur;
    bar.style.width = (cur * 25) + '%';
    back.style.visibility = cur === 1 ? 'hidden' : 'visible';
    next.hidden = cur === 4;
    send.hidden = cur !== 4;
    if (cur === 4) summary();
    var top = root.getBoundingClientRect().top + window.scrollY - 110;
    if (window.scrollY > top) window.scrollTo({ top: top, behavior: 'smooth' });
    if (cur === 4 && window.innerWidth > 760) form.querySelector('input[name="name"]').focus();
  }
  back.addEventListener('click', function () { go(cur - 1); });
  next.addEventListener('click', function () { go(cur + 1); });
  go(1);

  form.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && e.target.tagName === 'INPUT' && cur < 4) { e.preventDefault(); go(cur + 1); }
  });

  function field(n) { return form.querySelector('[name="' + n + '"]'); }
  form.addEventListener('input', function (e) { if (e.target.classList.contains('bad')) { e.target.classList.remove('bad'); hideErr(4); } });
  function clientCheck() {
    var name = field('name').value.trim(), email = field('email').value.trim(), phone = field('phone').value.trim();
    if (name.length < 3) return ['name', 'Please enter your full name.'];
    if (!/^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(email)) return ['email', 'Please enter a valid email address.'];
    var d = phone.replace(/\D/g, '');
    if (d.length < 7 || d.length > 15) return ['phone', 'Please enter a valid phone number with country code.'];
    return null;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (cur !== 4) { go(cur + 1); return; }
    hideErr(4);
    form.querySelectorAll('.bad').forEach(function (x) { x.classList.remove('bad'); });
    var bad = clientCheck();
    if (bad) { field(bad[0]).classList.add('bad'); field(bad[0]).focus(); showErr(4, bad[1]); return; }

    var payload = {
      name: field('name').value.trim(),
      email: field('email').value.trim(),
      phone: field('phone').value.trim(),
      company: field('company').value.trim(),
      reason: sel.reason || 'Something else',
      stage: sel.stage, timeline: sel.timeline, orgType: sel.orgType,
      role: field('role').value.trim(),
      message: msg.value.trim(),
      sourcePage: sourcePage,
      website: field('website').value,
      formLoadedAt: loadedAt
    };
    send.disabled = true; back.disabled = true;
    var label = send.innerHTML;
    send.innerHTML = 'Sending&hellip;';
    tokenP.then(function (t) {
      if (t) return t;
      return getToken().then(function (t2) { return new Promise(function (ok) { setTimeout(function () { ok(t2); }, 3200); }); });
    }).then(function (t) {
      payload.formToken = t;
      return fetch('/api/contact', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    })
      .then(function (r) { return r.json().catch(function () { return { success: false }; }); })
      .then(function (res) {
        if (res && res.success) {
          var first = payload.name.split(' ')[0];
          document.getElementById('cfDoneTitle').textContent = 'Thank you, ' + first + '. We have it.';
          document.getElementById('cfDoneText').textContent = 'Your note about “' + payload.reason + '” has reached us. A confirmation is on its way to ' + payload.email + '.';
          form.hidden = true;
          root.querySelector('.vk-cf-top').hidden = true;
          document.getElementById('cfDone').hidden = false;
          root.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } else {
          showErr(4, (res && res.error) || 'Something went wrong. Please try again, or email connect@vakratronsys.com.');
        }
      })
      .catch(function () { showErr(4, 'Could not reach the server. Please check your connection, or email connect@vakratronsys.com.'); })
      .then(function () { send.disabled = false; back.disabled = false; send.innerHTML = label; });
  });
})();
