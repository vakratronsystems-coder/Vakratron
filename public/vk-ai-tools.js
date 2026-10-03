/* vk-ai-tools.js: interactive tools for the AI infrastructure pages.
   - .vk-gpucalc  : how many GPUs do I need? (memory-based estimate)
   - .vk-trainsim : distributed training job with checkpoints and a node failure
   No dependencies. Styles live in vk-content.css. */
(function () {
  'use strict';
  function esc(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }
  var REDUCED = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ------------------------------------------------------------------ GPU sizing calculator */
  // Llama 3-class architectures: params (B), layers, KV heads, head dim
  var MODELS = {
    '8': { p: 8, layers: 32, kvh: 8, hd: 128, name: '~8B (Llama 3 8B class)' },
    '70': { p: 70, layers: 80, kvh: 8, hd: 128, name: '~70B (Llama 3 70B class)' },
    '405': { p: 405, layers: 126, kvh: 8, hd: 128, name: '~405B (Llama 3.1 405B class)' }
  };
  var GPUS = {
    h100: { name: 'NVIDIA H100 SXM 80 GB', mem: 80, nodeKw: 10.2, perNode: 8 },
    h200: { name: 'NVIDIA H200 SXM 141 GB', mem: 141, nodeKw: 10.2, perNode: 8 },
    a100: { name: 'NVIDIA A100 SXM 80 GB', mem: 80, nodeKw: 6.5, perNode: 8 },
    l40s: { name: 'NVIDIA L40S 48 GB (PCIe)', mem: 48, nodeKw: 4.5, perNode: 8 }
  };
  var PREC = { '2': 'BF16 / FP16 (2 bytes)', '1': 'FP8 / INT8 (1 byte)', '0.5': 'INT4 (0.5 byte)' };

  function sel(name, opts, val) {
    return '<select data-k="' + name + '">' + opts.map(function (o) { return '<option value="' + o[0] + '"' + (o[0] === val ? ' selected' : '') + '>' + esc(o[1]) + '</option>'; }).join('') + '</select>';
  }
  function initCalc(root) {
    root.innerHTML = '<div class="vk-calc-grid"><div class="vk-calc-in">' +
      '<label><span>What do you want to do?</span>' + sel('use', [['infer', 'Run the model (inference)'], ['lora', 'Fine-tune with LoRA'], ['full', 'Full fine-tune']], 'infer') + '</label>' +
      '<label><span>Model size</span>' + sel('model', Object.keys(MODELS).map(function (k) { return [k, MODELS[k].name]; }), '70') + '</label>' +
      '<label><span>GPU</span>' + sel('gpu', Object.keys(GPUS).map(function (k) { return [k, GPUS[k].name]; }), 'h100') + '</label>' +
      '<label class="vk-only-infer"><span>Weight precision</span>' + sel('prec', [['2', PREC['2']], ['1', PREC['1']], ['0.5', PREC['0.5']]], '2') + '</label>' +
      '<label class="vk-only-infer"><span>Users served at the same moment</span><input type="number" min="1" data-k="users" value="32"></label>' +
      '<label class="vk-only-infer"><span>Context length per request (tokens)</span>' + sel('ctx', [['4096', '4,000 (chat)'], ['8192', '8,000'], ['32768', '32,000 (long documents)'], ['131072', '128,000']], '8192') + '</label>' +
      '</div><div class="vk-calc-out" aria-live="polite"></div></div>';
    var out = root.querySelector('.vk-calc-out');
    function g(k) { return root.querySelector('[data-k="' + k + '"]').value; }
    function calc() {
      var use = g('use'), m = MODELS[g('model')], gpu = GPUS[g('gpu')];
      root.querySelectorAll('.vk-only-infer').forEach(function (el) { el.style.display = use === 'infer' ? '' : 'none'; });
      var parts = [], total, notes = [];
      if (use === 'infer') {
        var bytes = parseFloat(g('prec')), users = Math.max(1, parseInt(g('users'), 10) || 1), ctx = parseInt(g('ctx'), 10);
        var kvBytes = bytes < 2 ? 1 : 2; // FP8 KV cache when weights are quantised
        var weights = m.p * bytes;                                  // GB
        var kvPerTok = 2 * m.layers * m.kvh * m.hd * kvBytes;       // bytes
        var kv = kvPerTok * ctx * users / 1e9;                      // GB, worst case: every user at full context
        var over = (weights + kv) * 0.1;
        parts = [['Model weights', weights], ['KV cache (' + users + ' users x ' + (ctx / 1000).toFixed(0) + 'k tokens)', kv], ['Runtime overhead', over]];
        total = weights + kv + over;
        notes.push('KV cache assumes every user is at full context at the same moment. Real traffic usually needs less, so treat this as the safe upper bound.');
      } else if (use === 'lora') {
        var w = m.p * 2, act = m.p * 2 * 0.3;
        parts = [['Model weights (BF16, frozen)', w], ['Adapters, optimizer and activations', act]];
        total = w + act;
        notes.push('QLoRA, which loads the base model in 4-bit, can cut this by roughly a half to two-thirds.');
      } else {
        var st = m.p * 16, act2 = st * 0.2;
        parts = [['Weights, gradients and optimizer (~16 bytes per parameter)', st], ['Activations (with checkpointing)', act2]];
        total = st + act2;
        notes.push('This is the minimum memory. More GPUs than this mainly make training faster, which is usually the real constraint.');
      }
      var usable = gpu.mem * 0.9;
      var n = Math.max(1, Math.ceil(total / usable));
      var gpusNeeded = n <= 8 ? [1, 2, 4, 8].filter(function (x) { return x >= n; })[0] : Math.ceil(n / 8) * 8;
      var nodes = Math.ceil(gpusNeeded / gpu.perNode);
      var kw = gpusNeeded >= gpu.perNode ? nodes * gpu.nodeKw : gpu.nodeKw * (0.3 + 0.7 * gpusNeeded / gpu.perNode);
      if (nodes > 1 && use !== 'infer') notes.push('Training across ' + nodes + ' nodes needs a high-speed GPU fabric: typically one 400 Gb/s InfiniBand or RoCE port per GPU.');
      if (nodes > 1 && use === 'infer') notes.push('The model does not fit in one node. Serving across nodes works but is slower; a larger-memory GPU or lower precision may keep it in one node.');
      if (gpu.nodeKw >= 10 && gpusNeeded >= 4) notes.push('A full 8-GPU node of this type draws about ' + gpu.nodeKw + ' kW. Many enterprise racks are built for 5 to 10 kW, so check power and cooling before ordering.');
      var max = Math.max.apply(null, parts.map(function (p) { return p[1]; })) || 1;
      var rows = parts.map(function (p) {
        return '<div class="vk-mem-row"><span class="l">' + esc(p[0]) + '</span><span class="b"><i style="width:' + (100 * p[1] / total).toFixed(1) + '%"></i></span><span class="n">' + Math.round(p[1]) + ' GB</span></div>';
      }).join('');
      out.innerHTML = '<div class="vk-calc-big"><div><span class="k">GPU memory needed</span><span class="v">~' + Math.round(total).toLocaleString('en-IN') + ' GB</span></div>' +
        '<div><span class="k">GPUs</span><span class="v">' + gpusNeeded + ' &times; ' + gpu.mem + ' GB</span></div>' +
        '<div><span class="k">Servers</span><span class="v">' + nodes + ' &times; ' + gpu.perNode + '-GPU</span></div>' +
        '<div><span class="k">Power (approx.)</span><span class="v">~' + kw.toFixed(1) + ' kW</span></div></div>' +
        '<div class="vk-mem">' + rows + '</div>' +
        '<ul class="vk-calc-notes">' + notes.map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') + '</ul>' +
        '<p class="vk-small vk-muted">A first estimate based on memory only, using Llama 3-class model shapes and about 90% usable GPU memory. Throughput, latency targets and redundancy usually add GPUs. We size properly from your real workload.</p>';
    }
    root.addEventListener('change', calc); root.addEventListener('input', calc);
    calc();
  }

  /* ------------------------------------------------------------------ training job simulator */
  function initTrain(root) {
    var NODES = 4, TOTAL = 1000, STEP = 10;
    var step = 0, lastCk = 0, every = 200, timer = null, running = false, failed = -1, phase = 0, spareUsed = false, lost = 0;
    var h = '<div class="vk-train-board"><div class="vk-train-nodes">';
    for (var i = 0; i < NODES; i++) {
      h += '<div class="vk-tnode" data-n="' + i + '"><span class="t">Node ' + (i + 1) + '</span><div class="g">' + new Array(9).join('<i></i>') + '</div></div>';
    }
    h += '<div class="vk-tnode spare" data-n="spare"><span class="t">Spare node</span><div class="g">' + new Array(9).join('<i></i>') + '</div></div>';
    h += '</div><div class="vk-train-fabric"><span>GPU fabric: 400 Gb/s per GPU</span></div><div class="vk-train-store"><span>Parallel storage: datasets and checkpoints</span></div></div>' +
      '<div class="vk-train-bar"><div class="p"><i></i><b></b></div><div class="vk-train-stats"></div></div>' +
      '<div class="vk-train-ctl"><button type="button" class="vk-btn primary go">&#9654; Start training</button><button type="button" class="vk-btn fail" disabled>Fail a node</button><button type="button" class="vk-btn reset">Reset</button>' +
      '<label class="ck">Checkpoint every <select><option value="100">100 steps</option><option value="200" selected>200 steps</option><option value="400">400 steps</option></select></label></div>' +
      '<div class="vk-train-log" aria-live="polite"><p class="vk-muted">Four 8-GPU nodes train one model together. Every step, each GPU works on its own slice of data, then all 32 GPUs share their results over the fabric. Start the job, then try failing a node.</p></div>';
    root.innerHTML = h;
    var bar = root.querySelector('.vk-train-bar .p i'), mark = root.querySelector('.vk-train-bar .p b'), stats = root.querySelector('.vk-train-stats');
    var go = root.querySelector('.go'), fail = root.querySelector('.fail'), log = root.querySelector('.vk-train-log'), ckSel = root.querySelector('select');
    var board = root.querySelector('.vk-train-board');
    function line(t, c) { var p = document.createElement('p'); p.className = c || ''; p.innerHTML = t; log.appendChild(p); log.scrollTop = log.scrollHeight; }
    function draw() {
      bar.style.width = (100 * step / TOTAL) + '%';
      mark.style.left = (100 * lastCk / TOTAL) + '%';
      stats.innerHTML = '<span>Step <strong>' + step + '</strong> of ' + TOTAL + '</span><span>Last checkpoint: <strong>' + lastCk + '</strong></span><span>Work lost to failures: <strong>' + lost + ' steps</strong></span>';
      board.setAttribute('data-phase', running ? ['load', 'compute', 'sync'][phase] : (step >= TOTAL ? 'done' : 'idle'));
    }
    function tick() {
      phase = (phase + 1) % 3;
      if (phase === 0) {
        step = Math.min(TOTAL, step + STEP);
        if (step % every === 0 && step > lastCk) {
          lastCk = step; board.classList.add('ckpt'); setTimeout(function () { board.classList.remove('ckpt'); }, 600);
          line('&#128190; Checkpoint saved at step ' + step + '.', 'ok');
        }
      }
      draw();
      if (step >= TOTAL) { stop(); line('<strong>Training finished.</strong> ' + (lost ? lost + ' steps had to be redone after the failure.' : 'No work was lost.'), 'ok'); go.disabled = true; fail.disabled = true; }
    }
    function start() {
      if (running || step >= TOTAL) return;
      if (step === 0 && !log.querySelector('.ok,.bad,.warn')) log.innerHTML = '';
      running = true; go.disabled = true; fail.disabled = failed >= 0 && spareUsed ? true : false;
      every = parseInt(ckSel.value, 10); ckSel.disabled = true;
      line('Training running: load data, compute on all GPUs, synchronise over the fabric. Repeat.');
      timer = setInterval(tick, REDUCED ? 260 : 130);
    }
    function stop() { running = false; clearInterval(timer); draw(); }
    fail.addEventListener('click', function () {
      if (!running) return;
      stop(); fail.disabled = true;
      failed = 2;
      var n = root.querySelector('[data-n="2"]'); n.classList.add('down');
      var redo = step - lastCk; lost += redo;
      line('&#10007; Node 3 failed at step ' + step + '. The whole job stops: every GPU depends on every other GPU in each step.', 'bad');
      setTimeout(function () {
        line('The scheduler marks node 3 as down and brings in the spare node.', 'warn');
        root.querySelector('[data-n="spare"]').classList.add('in'); spareUsed = true;
        setTimeout(function () {
          line('&#8634; Job restarts from the last checkpoint (step ' + lastCk + '). ' + redo + ' steps of work are redone.', 'warn');
          step = lastCk; draw();
          setTimeout(function () { go.disabled = false; start(); }, REDUCED ? 300 : 900);
        }, REDUCED ? 300 : 1100);
      }, REDUCED ? 300 : 1000);
    });
    go.addEventListener('click', start);
    root.querySelector('.reset').addEventListener('click', function () {
      stop(); step = 0; lastCk = 0; lost = 0; failed = -1; spareUsed = false; phase = 0;
      root.querySelectorAll('.vk-tnode').forEach(function (n) { n.classList.remove('down', 'in'); });
      go.disabled = false; fail.disabled = true; ckSel.disabled = false;
      log.innerHTML = '<p class="vk-muted">Reset. Pick a checkpoint interval, start the job, then try failing a node. Compare how much work is lost with checkpoints every 100 steps versus every 400.</p>';
      draw();
    });
    draw();
  }

  function boot() {
    Array.prototype.forEach.call(document.querySelectorAll('.vk-gpucalc'), initCalc);
    Array.prototype.forEach.call(document.querySelectorAll('.vk-trainsim'), initTrain);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
