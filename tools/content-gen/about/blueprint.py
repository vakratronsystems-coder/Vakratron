"""Animated 'design on paper' blueprint for the About hero. Pure SVG + CSS, no JS."""

SVG = '''<svg class="vk-bp" viewBox="0 0 560 470" role="img" aria-labelledby="bpT bpD" xmlns="http://www.w3.org/2000/svg">
  <title id="bpT">How a Vakratron design comes together</title>
  <desc id="bpD">A design sheet draws itself: the workload and two sites appear, assumptions are written in the margin, two options are compared on cost, and the design is stamped as failover tested.</desc>
  <defs>
    <pattern id="bpGrid" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="rgba(56,189,248,0.07)" stroke-width="1"/></pattern>
    <linearGradient id="bpCard" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0d1630"/><stop offset="1" stop-color="#070c1c"/></linearGradient>
  </defs>
  <rect x="8" y="8" width="544" height="454" rx="18" fill="url(#bpCard)" stroke="rgba(255,255,255,0.09)"/>
  <rect x="8" y="8" width="544" height="454" rx="18" fill="url(#bpGrid)"/>
  <text x="32" y="42" class="bp-meta">HIGH-LEVEL DESIGN</text>
  <text x="528" y="42" class="bp-meta" text-anchor="end">rev 1.3 &#183; for review</text>
  <line x1="32" y1="56" x2="528" y2="56" stroke="rgba(255,255,255,0.08)"/>

  <!-- stage 1: workload and sites -->
  <g class="bp-s1">
    <rect x="195" y="76" width="170" height="50" rx="10" class="bp-box bp-blue"/>
    <text x="280" y="97" class="bp-h" text-anchor="middle">Your workload</text>
    <text x="280" y="115" class="bp-sub" text-anchor="middle">ERP &#183; clinical apps &#183; 3 TB</text>
  </g>
  <path class="bp-draw bp-d1" d="M280 126 V150 H140 V180"/>
  <path class="bp-draw bp-d1" d="M280 150 H420 V180"/>
  <g class="bp-s1">
    <rect x="50" y="180" width="180" height="96" rx="12" class="bp-box"/>
    <text x="66" y="203" class="bp-h">Primary site</text>
    <rect x="66" y="216" width="46" height="44" rx="5" class="bp-rack"/><rect x="118" y="216" width="46" height="44" rx="5" class="bp-rack"/><rect x="170" y="216" width="46" height="44" rx="5" class="bp-rack"/>
    <circle cx="76" cy="228" r="3" class="bp-led"/><circle cx="128" cy="228" r="3" class="bp-led"/><circle cx="180" cy="228" r="3" class="bp-led"/>
  </g>
  <g class="bp-s1">
    <rect x="330" y="180" width="180" height="96" rx="12" class="bp-box bp-dr"/>
    <text x="346" y="203" class="bp-h">DR site</text>
    <rect x="346" y="216" width="46" height="44" rx="5" class="bp-rack"/><rect x="398" y="216" width="46" height="44" rx="5" class="bp-rack"/><rect x="450" y="216" width="46" height="44" rx="5" class="bp-rack bp-dim"/>
    <circle cx="356" cy="228" r="3" class="bp-led bp-led-dr"/><circle cx="408" cy="228" r="3" class="bp-led bp-led-dr"/>
  </g>

  <!-- stage 2: assumptions written in the margin -->
  <g class="bp-s2">
    <path class="bp-flow" d="M230 238 H330"/>
    <text x="280" y="230" class="bp-sub" text-anchor="middle">async copy</text>
    <path d="M195 101 C182 101 178 96 172 92" class="bp-lead"/>
    <text x="34" y="82" class="bp-note">assume: 2 TB/day changes</text>
    <text x="34" y="98" class="bp-note">peak 400 users</text>
    <path d="M420 276 C420 292 430 298 440 300" class="bp-lead"/>
    <text x="352" y="316" class="bp-note">RPO 15 min &#183; RTO 1 h</text>
  </g>

  <!-- stage 3: options compared -->
  <g class="bp-s3">
    <rect x="32" y="306" width="262" height="124" rx="12" class="bp-box"/>
    <text x="48" y="330" class="bp-h">Options compared</text>
    <text x="48" y="356" class="bp-sub">A &#183; active-passive</text>
    <rect x="48" y="363" width="150" height="10" rx="5" class="bp-bar bp-bar-a"/>
    <text x="206" y="372" class="bp-sub">1.0&#215; cost</text>
    <text x="48" y="396" class="bp-sub">B &#183; active-active</text>
    <rect x="48" y="403" width="200" height="10" rx="5" class="bp-bar bp-bar-b"/>
    <text x="252" y="396" class="bp-sub" text-anchor="end">1.7&#215; cost</text>
    <g class="bp-pick"><rect x="160" y="344" width="58" height="17" rx="8.5" class="bp-chip"/><text x="189" y="356" class="bp-chiptx" text-anchor="middle">chosen</text></g>
  </g>

  <!-- stage 4: tested -->
  <g class="bp-s4">
    <g class="bp-stamp">
      <rect x="326" y="346" width="196" height="78" rx="10" class="bp-stamp-box"/>
      <text x="424" y="376" class="bp-stamp-h" text-anchor="middle">&#10003; FAILOVER TESTED</text>
      <text x="424" y="398" class="bp-stamp-s" text-anchor="middle">measured RTO 48 min</text>
      <text x="424" y="413" class="bp-stamp-s" text-anchor="middle">runbook handed over</text>
    </g>
  </g>
</svg>'''

CAPTION = '''<ol class="vk-bp-steps">
  <li class="c1"><span>1</span>Know the workload</li>
  <li class="c2"><span>2</span>Write assumptions down</li>
  <li class="c3"><span>3</span>Compare options</li>
  <li class="c4"><span>4</span>Test and hand over</li>
</ol>'''

CSS = '''/* === ABOUT BLUEPRINT === */
main.vk .vk-ahero-grid { display: grid; grid-template-columns: 1.05fr 1fr; gap: 40px; align-items: center; }
main.vk .vk-ahero-grid .vk-actions { margin-top: 22px; }
main.vk figure.vk-bpfig { margin: 0; }
main.vk svg.vk-bp { width: 100%; height: auto; display: block; filter: drop-shadow(0 30px 50px rgba(0,0,0,0.45)); }
main.vk .vk-bp text { font-family: 'Inter', sans-serif; }
main.vk .vk-bp .bp-meta { fill: #64748b; font-size: 10.5px; letter-spacing: 0.14em; font-weight: 600; }
main.vk .vk-bp .bp-h { fill: #f1f5f9; font-size: 13px; font-weight: 600; }
main.vk .vk-bp .bp-sub { fill: #94a3b8; font-size: 11px; }
main.vk .vk-bp .bp-box { fill: rgba(15,23,42,0.85); stroke: rgba(148,163,184,0.35); stroke-width: 1.2; }
main.vk .vk-bp .bp-blue { stroke: #38bdf8; }
main.vk .vk-bp .bp-rack { fill: rgba(56,189,248,0.08); stroke: rgba(56,189,248,0.35); }
main.vk .vk-bp .bp-dim { opacity: 0.45; }
main.vk .vk-bp .bp-led { fill: #34d399; }
main.vk .vk-bp .bp-led-dr { fill: #64748b; }
main.vk .vk-bp .bp-draw { fill: none; stroke: #38bdf8; stroke-width: 1.5; stroke-dasharray: 320; stroke-dashoffset: 320; }
main.vk .vk-bp .bp-flow { fill: none; stroke: #C2185B; stroke-width: 2; stroke-dasharray: 6 6; }
main.vk .vk-bp .bp-lead { fill: none; stroke: #f472b6; stroke-width: 1; stroke-dasharray: 3 3; }
main.vk .vk-bp .bp-note { fill: #f472b6; font-size: 11.5px; font-style: italic; }
main.vk .vk-bp .bp-bar { transform-box: fill-box; transform-origin: left center; }
main.vk .vk-bp .bp-bar-a { fill: #C2185B; }
main.vk .vk-bp .bp-bar-b { fill: #475569; }
main.vk .vk-bp .bp-chip { fill: rgba(52,211,153,0.15); stroke: #34d399; }
main.vk .vk-bp .bp-chiptx { fill: #34d399; font-size: 10px; font-weight: 700; letter-spacing: 0.05em; }
main.vk .vk-bp .bp-stamp { transform-box: fill-box; transform-origin: center; transform: rotate(-6deg); }
main.vk .vk-bp .bp-stamp-box { fill: rgba(194,24,91,0.12); stroke: #C2185B; stroke-width: 2; stroke-dasharray: 2 0; }
main.vk .vk-bp .bp-stamp-h { fill: #f9a8d4; font-size: 14px; font-weight: 800; letter-spacing: 0.08em; }
main.vk .vk-bp .bp-stamp-s { fill: #f9a8d4; font-size: 11px; opacity: 0.85; }

main.vk .vk-bp-steps { list-style: none !important; margin: 16px 0 0 !important; padding: 0 !important; display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
main.vk .vk-bp-steps li { margin: 0 !important; padding: 8px 10px !important; border-radius: 10px; border: 1px solid rgba(255,255,255,0.07); font-size: 0.78rem !important; line-height: 1.35; color: #64748b !important; display: flex; gap: 8px; align-items: flex-start; }
main.vk .vk-bp-steps li::before, main.vk .vk-bp-steps li::marker { content: none !important; display: none !important; }
main.vk .vk-bp-steps li span { flex: 0 0 18px; height: 18px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 0.7rem; font-weight: 700; background: rgba(255,255,255,0.06); color: #94a3b8; }

@media (prefers-reduced-motion: no-preference) {
  main.vk .vk-bp .bp-s1 { animation: bpIn1 16s ease infinite; }
  main.vk .vk-bp .bp-d1 { animation: bpDraw 16s ease infinite; }
  main.vk .vk-bp .bp-s2 { animation: bpIn2 16s ease infinite; }
  main.vk .vk-bp .bp-flow { animation: bpIn2 16s ease infinite, bpFlow 1s linear infinite; }
  main.vk .vk-bp .bp-s3 { animation: bpIn3 16s ease infinite; }
  main.vk .vk-bp .bp-bar-a { animation: bpGrowA 16s ease infinite; }
  main.vk .vk-bp .bp-bar-b { animation: bpGrowB 16s ease infinite; }
  main.vk .vk-bp .bp-pick { animation: bpPick 16s ease infinite; }
  main.vk .vk-bp .bp-s4 { animation: bpIn4 16s ease infinite; }
  main.vk .vk-bp .bp-stamp { animation: bpStamp 16s cubic-bezier(.2,1.4,.4,1) infinite; }
  main.vk .vk-bp .bp-led-dr { animation: bpLed 16s ease infinite; }
  main.vk .vk-bp-steps li { animation: bpCap 16s ease infinite; }
  main.vk .vk-bp-steps li span { animation: bpCapN 16s ease infinite; }
  main.vk .vk-bp-steps li.c2, main.vk .vk-bp-steps li.c2 span { animation-delay: 4s; }
  main.vk .vk-bp-steps li.c3, main.vk .vk-bp-steps li.c3 span { animation-delay: 8s; }
  main.vk .vk-bp-steps li.c4, main.vk .vk-bp-steps li.c4 span { animation-delay: 12s; }
}
@media (prefers-reduced-motion: reduce) {
  main.vk .vk-bp .bp-draw { stroke-dashoffset: 0; }
  main.vk .vk-bp .bp-led-dr { fill: #34d399; }
}
@keyframes bpIn1 { 0% { opacity: 0; } 4%, 94% { opacity: 1; } 100% { opacity: 0; } }
@keyframes bpDraw { 0% { stroke-dashoffset: 320; opacity: 1; } 10%, 94% { stroke-dashoffset: 0; opacity: 1; } 100% { stroke-dashoffset: 0; opacity: 0; } }
@keyframes bpIn2 { 0%, 25% { opacity: 0; } 30%, 94% { opacity: 1; } 100% { opacity: 0; } }
@keyframes bpFlow { to { stroke-dashoffset: -24; } }
@keyframes bpIn3 { 0%, 50% { opacity: 0; } 54%, 94% { opacity: 1; } 100% { opacity: 0; } }
@keyframes bpGrowA { 0%, 53% { transform: scaleX(0); } 61%, 100% { transform: scaleX(1); } }
@keyframes bpGrowB { 0%, 55% { transform: scaleX(0); } 64%, 100% { transform: scaleX(1); } }
@keyframes bpPick { 0%, 66% { opacity: 0; } 70%, 94% { opacity: 1; } 100% { opacity: 0; } }
@keyframes bpIn4 { 0%, 75% { opacity: 0; } 78%, 94% { opacity: 1; } 100% { opacity: 0; } }
@keyframes bpStamp { 0%, 75% { transform: rotate(-6deg) scale(1.5); } 80%, 100% { transform: rotate(-6deg) scale(1); } }
@keyframes bpLed { 0%, 77% { fill: #64748b; } 80%, 96% { fill: #34d399; } 100% { fill: #64748b; } }
@keyframes bpCap { 0% { color: #64748b; border-color: rgba(255,255,255,0.07); background: transparent; } 2%, 23% { color: #fff; border-color: rgba(194,24,91,0.55); background: rgba(194,24,91,0.10); } 25%, 100% { color: #64748b; border-color: rgba(255,255,255,0.07); background: transparent; } }
@keyframes bpCapN { 0% { background: rgba(255,255,255,0.06); color: #94a3b8; } 2%, 23% { background: #C2185B; color: #fff; } 25%, 100% { background: rgba(255,255,255,0.06); color: #94a3b8; } }

@media (max-width: 900px) {
  main.vk .vk-ahero-grid { grid-template-columns: 1fr; gap: 28px; }
}
@media (max-width: 560px) {
  main.vk .vk-bp-steps { grid-template-columns: 1fr 1fr; }
}
/* === END ABOUT BLUEPRINT === */'''
