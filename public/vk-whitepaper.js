/* Whitepaper download: details -> emailed 6-digit code -> PDF link.
   Uses /api/form-token, /api/whitepaper/start and /api/whitepaper/download. */
(function () {
  var boxes = document.querySelectorAll('.wp-dl');
  if (!boxes.length) return;
  var loadedAt = Date.now();
  function getToken() {
    return fetch('/api/form-token', { cache: 'no-store' }).then(function (r) { return r.json(); })
      .then(function (d) { return d && d.token; }).catch(function () { return null; });
  }
  var tokenP = getToken();
  var sourcePage = location.pathname;
  try { if (document.referrer && new URL(document.referrer).host === location.host) sourcePage = new URL(document.referrer).pathname + ' > ' + location.pathname; } catch (e) {}
  function post(url, body) {
    return fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
      .then(function (r) { return r.json().catch(function () { return { success: false, error: 'The server sent an unexpected reply (HTTP ' + r.status + '). Please try again, or email connect@vakratronsys.com.' }; }); });
  }
  function withToken(p) {
    return tokenP.then(function (t) {
      if (t) return t;
      return getToken().then(function (t2) { return new Promise(function (ok) { setTimeout(function () { ok(t2); }, 3200); }); });
    }).then(function (t) { p.formToken = t; return p; });
  }

  boxes.forEach(function (box) {
    var slug = box.getAttribute('data-wp');
    var form = box.querySelector('.wp-dl-form');
    var fields = box.querySelector('.wp-dl-fields');
    var otpBox = box.querySelector('.wp-dl-otp');
    var otpIn = box.querySelector('input[name=otp]');
    var err = box.querySelector('.wp-dl-err');
    var btn = box.querySelector('.wp-dl-btn');
    var done = box.querySelector('.wp-dl-done');
    var otpToken = null;
    function f(n) { return form.querySelector('[name="' + n + '"]'); }
    function showErr(t) { err.textContent = t; err.hidden = false; }
    function hideErr() { err.hidden = true; }
    function setBusy(on, label) { btn.disabled = on; btn.innerHTML = on ? label : (otpToken ? 'Get the PDF' : 'Email me a code'); }
    function payload() {
      return { slug: slug, name: f('name').value.trim(), email: f('email').value.trim(), phone: f('phone').value.trim(),
               company: f('company').value.trim(), role: f('role').value.trim(), website: f('website').value,
               formLoadedAt: loadedAt, sourcePage: sourcePage };
    }
    function check() {
      var p = payload();
      if (p.name.length < 3) return ['name', 'Please enter your full name.'];
      if (!/^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(p.email)) return ['email', 'Please enter a valid email address.'];
      var d = p.phone.replace(/\D/g, '');
      if (d.length < 10 || d.length > 15) return ['phone', 'Please enter a mobile number with country code.'];
      return null;
    }
    function showOtp(on) {
      otpBox.hidden = !on; fields.hidden = on;
      if (on) { box.querySelector('.wp-dl-mail').textContent = f('email').value.trim(); otpIn.value = ''; setTimeout(function () { otpIn.focus(); }, 50); }
      setBusy(false);
    }
    function requestCode() {
      hideErr(); form.querySelectorAll('.bad').forEach(function (x) { x.classList.remove('bad'); });
      var bad = check(); if (bad) { f(bad[0]).classList.add('bad'); f(bad[0]).focus(); showErr(bad[1]); return; }
      setBusy(true, 'Sending code&hellip;');
      withToken(payload()).then(function (p) { return post('/api/whitepaper/start', p); }).then(function (res) {
        if (res && res.success && res.otpToken) { otpToken = res.otpToken; if (res.devCode) console.log('[dev] code', res.devCode); showOtp(true); }
        else { showErr((res && res.error) || 'Something went wrong. Please try again.'); setBusy(false); }
      }).catch(function () { showErr('Could not reach the server. Please check your connection.'); setBusy(false); });
    }
    function download() {
      hideErr();
      var code = otpIn.value.replace(/\D/g, '');
      if (code.length !== 6) { otpIn.classList.add('bad'); showErr('Please enter the 6-digit code from the email.'); return; }
      var p = payload(); p.otp = code; p.otpToken = otpToken;
      setBusy(true, 'Checking&hellip;');
      withToken(p).then(function (q) { return post('/api/whitepaper/download', q); }).then(function (res) {
        if (res && res.success && res.url) {
          form.hidden = true; done.hidden = false;
          var a = done.querySelector('.wp-dl-get'); a.href = res.url;
          window.open(res.url, '_blank', 'noopener');
          boxes.forEach(function (b) { if (b !== box) { b.querySelector('.wp-dl-form').hidden = true; var d = b.querySelector('.wp-dl-done'); d.hidden = false; d.querySelector('.wp-dl-get').href = res.url; } });
        } else {
          if (res && res.otp === 'expired') { otpToken = null; showOtp(false); }
          showErr((res && res.error) || 'Something went wrong. Please try again.'); setBusy(false);
        }
      }).catch(function () { showErr('Could not reach the server. Please check your connection.'); setBusy(false); });
    }
    box.querySelector('.wp-dl-resend').addEventListener('click', function () { otpToken = null; requestCode(); });
    box.querySelector('.wp-dl-change').addEventListener('click', function () { otpToken = null; hideErr(); showOtp(false); f('email').focus(); });
    otpIn.addEventListener('input', function () { otpIn.classList.remove('bad'); otpIn.value = otpIn.value.replace(/\D/g, '').slice(0, 6); });
    form.addEventListener('input', function (e) { if (e.target.classList.contains('bad')) { e.target.classList.remove('bad'); hideErr(); } });
    form.addEventListener('submit', function (e) { e.preventDefault(); if (otpToken) download(); else requestCode(); });
  });

  // highlight the current section in the contents list
  var links = document.querySelectorAll('.wp-toc a[href^="#"]');
  if ('IntersectionObserver' in window && links.length) {
    var map = {}; links.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting && map[e.target.id]) { links.forEach(function (a) { a.classList.remove('on'); }); map[e.target.id].classList.add('on'); } });
    }, { rootMargin: '-30% 0px -60% 0px' });
    document.querySelectorAll('.wp-sec[id]').forEach(function (s) { io.observe(s); });
  }
})();
