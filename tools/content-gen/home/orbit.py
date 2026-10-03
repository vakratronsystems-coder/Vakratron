"""Animated 'ecosystem' hero visual for the home page: Vakratron logo at the centre, eight services in orbit."""
import math

W, H, CX, CY, R = 760, 660, 380, 330, 212
NODE_R = 38

ICONS = {
    'chip': '<rect x="7" y="7" width="10" height="10" rx="1.5"/><path d="M10 7V4M14 7V4M10 20v-3M14 20v-3M7 10H4M7 14H4M20 10h-3M20 14h-3"/>',
    'cloud': '<path d="M7 18h10.5a4 4 0 0 0 .3-8A6 6 0 0 0 6.2 11.3 3.4 3.4 0 0 0 7 18z"/>',
    'shield': '<path d="M12 3l7 3v5.5c0 4.6-3 7.8-7 9.5-4-1.7-7-4.9-7-9.5V6z"/><path d="M9 12l2 2 4-4"/>',
    'cube': '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M4 7.5l8 4.5 8-4.5M12 12v9"/>',
    'api': '<circle cx="12" cy="12" r="2.5"/><circle cx="5" cy="6" r="2"/><circle cx="19" cy="6" r="2"/><circle cx="5" cy="18" r="2"/><circle cx="19" cy="18" r="2"/><path d="M6.6 7.3l3.4 3M17.4 7.3l-3.4 3M6.6 16.7l3.4-3M17.4 16.7l-3.4-3"/>',
    'robot': '<rect x="5" y="8" width="14" height="10" rx="2.5"/><path d="M12 4v4M3 12v3M21 12v3"/><circle cx="9.5" cy="13" r="1"/><circle cx="14.5" cy="13" r="1"/>',
    'db': '<ellipse cx="12" cy="6" rx="7" ry="2.8"/><path d="M5 6v12c0 1.5 3.1 2.8 7 2.8s7-1.3 7-2.8V6M5 12c0 1.5 3.1 2.8 7 2.8s7-1.3 7-2.8"/>',
    'llm': '<path d="M4 5h16v11H10l-5 4v-4H4z"/><path d="M12 7.8l.9 1.9 1.9.9-1.9.9-.9 1.9-.9-1.9-1.9-.9 1.9-.9z"/>',
}
GROUP = {'infra': '#38bdf8', 'plat': '#a78bfa', 'ai': '#f472b6'}

# angle (deg, 0 = right, clockwise), key, label, icon, group, link, caption
SERVICES = [
    (-90, 'gpu', 'AI infrastructure', 'chip', 'infra', '/portfolio/ai-gpu-cloud', 'GPU clusters sized and built, from the fabric to the power and cooling.'),
    (-45, 'cloud', 'Cloud and|VMware exit', 'cloud', 'infra', '/portfolio/cloud-solutions', 'Private, public and hybrid cloud, and a safe move off VMware.'),
    (0, 'api', 'APIs', 'api', 'plat', '/portfolio/api-microservices', 'Clear, secure APIs that stay understandable as they grow.'),
    (45, 'k8s', 'Kubernetes', 'cube', 'plat', '/portfolio/kubernetes-platform', 'An honest fit check, then a lean platform your team can run.'),
    (90, 'dr', 'Disaster recovery', 'shield', 'infra', '/portfolio/dr-solutions', 'Recovery designed per application, and tested with your team.'),
    (135, 'agents', 'AI agents', 'robot', 'ai', '/portfolio/agentic-ai', 'Agents that do routine work within clear limits and approvals.'),
    (180, 'rag', 'RAG', 'db', 'ai', '/portfolio/rag-solutions', 'Answers from your own documents, with sources and permissions.'),
    (-135, 'llm', 'Enterprise|LLM', 'llm', 'ai', '/portfolio/enterprise-llm', 'The right model for each task, run where your data rules allow.'),
]

def pt(a, r):
    t = math.radians(a)
    return CX + r * math.cos(t), CY + r * math.sin(t)

def svg():
    o = [f'<svg class="vk-orbit-svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="vkorbt"><title id="vkorbt">Vakratron at the centre of eight connected services: AI infrastructure, cloud, APIs, Kubernetes, disaster recovery, AI agents, RAG and enterprise LLM</title>']
    o.append('''<defs>
        <radialGradient id="vkog" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#C2185B" stop-opacity="0.35"/><stop offset="60%" stop-color="#C2185B" stop-opacity="0.06"/><stop offset="100%" stop-color="#C2185B" stop-opacity="0"/></radialGradient>
        <radialGradient id="vkog2" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#38bdf8" stop-opacity="0.10"/><stop offset="100%" stop-color="#38bdf8" stop-opacity="0"/></radialGradient>
        <filter id="vkglow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    </defs>''')
    o.append(f'<circle cx="{CX}" cy="{CY}" r="300" fill="url(#vkog2)"/>')
    o.append(f'<circle cx="{CX}" cy="{CY}" r="170" fill="url(#vkog)"/>')
    # rings
    o.append(f'<g class="vk-ring r1"><circle cx="{CX}" cy="{CY}" r="292" fill="none" stroke="#334155" stroke-width="1" stroke-dasharray="2 10"/></g>')
    o.append(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="#1e293b" stroke-width="1.5"/>')
    o.append(f'<g class="vk-ring r2"><circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="#C2185B" stroke-opacity="0.45" stroke-width="1.5" stroke-dasharray="60 600"/></g>')
    o.append(f'<g class="vk-ring r3"><circle cx="{CX}" cy="{CY}" r="128" fill="none" stroke="#38bdf8" stroke-opacity="0.35" stroke-width="1" stroke-dasharray="4 8"/></g>')
    # spokes
    for i, (a, key, *_r) in enumerate(SERVICES):
        x1, y1 = pt(a, 84); x2, y2 = pt(a, R - NODE_R - 4)
        col = GROUP[SERVICES[i][4]]
        o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#1e293b" stroke-width="2"/>')
        o.append(f'<line class="vk-spoke" style="animation-delay:{i * 0.45:.2f}s" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="2.4" stroke-linecap="round"/>')
    # particles on the orbit
    path = f'M{CX},{CY - R} a{R},{R} 0 1,1 -0.1,0'
    for i, col in enumerate(['#f472b6', '#38bdf8', '#a78bfa']):
        o.append(f'<circle r="3.2" fill="{col}" filter="url(#vkglow)"><animateMotion class="vk-pm" dur="18s" repeatCount="indefinite" begin="{-i * 6}s" path="{path}"/></circle>')
    # centre
    o.append(f'<circle class="vk-pulse1" cx="{CX}" cy="{CY}" r="74" fill="none" stroke="#C2185B" stroke-width="1.5"/>')
    o.append(f'<circle class="vk-pulse2" cx="{CX}" cy="{CY}" r="74" fill="none" stroke="#C2185B" stroke-width="1.5"/>')
    o.append(f'<circle cx="{CX}" cy="{CY}" r="70" fill="#070d1c" stroke="#C2185B" stroke-opacity="0.8" stroke-width="2" filter="url(#vkglow)"/>')
    o.append(f'<image href="/images/logo.png" x="{CX - 46}" y="{CY - 50}" width="92" height="92" preserveAspectRatio="xMidYMid meet"/>')
    o.append(f'<text x="{CX}" y="{CY + 56}" text-anchor="middle" class="vk-ctext">VAKRATRON</text>')
    # nodes
    for i, (a, key, label, icon, grp, href, cap) in enumerate(SERVICES):
        x, y = pt(a, R); col = GROUP[grp]
        lx, ly = pt(a, R + NODE_R + 18)
        c = math.cos(math.radians(a)); s = math.sin(math.radians(a))
        anchor = 'start' if c > 0.3 else ('end' if c < -0.3 else 'middle')
        ly += 5 + (8 if s > 0.9 else (-2 if s < -0.9 else 0))
        aria = label.replace('|', ' ')
        o.append(f'<a href="{href}" class="vk-node" data-i="{i}" style="--c:{col}" aria-label="{aria}">')
        o.append(f'<circle class="halo" cx="{x:.1f}" cy="{y:.1f}" r="{NODE_R + 10}" fill="{col}" opacity="0"/>')
        o.append(f'<circle class="disc" cx="{x:.1f}" cy="{y:.1f}" r="{NODE_R}" fill="#0b1224" stroke="{col}" stroke-opacity="0.55" stroke-width="2"/>')
        o.append(f'<g transform="translate({x - 18:.1f},{y - 18:.1f}) scale(1.5)" fill="none" stroke="{col}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</g>')
        parts = label.split('|')
        if len(parts) > 1 and s < 0.9: ly -= 10
        spans = ''.join(f'<tspan x="{lx:.1f}" dy="{0 if k == 0 else 20}">{p}</tspan>' for k, p in enumerate(parts))
        o.append(f'<text class="vk-nlabel" x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}">{spans}</text>')
        o.append('</a>')
    o.append('</svg>')
    return ''.join(o)

def html():
    caps = ''.join(f'<span data-i="{i}" data-href="{s[5]}" data-label="{s[2].replace("|", " ")}" data-c="{GROUP[s[4]]}">{s[6]}</span>' for i, s in enumerate(SERVICES))
    return f'''<div class="vk-orbit">
                {svg()}
                <div class="vk-orbit-cap" aria-live="polite"><span class="vk-cdot"></span><span class="n"></span><span class="d"></span><a class="go" href="#">Explore &rarr;</a></div>
                <div class="vk-orbit-data" hidden>{caps}</div>
            </div>'''

JS = r"""/* vk-home.js: cycles the highlighted service in the home page orbit visual. */
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
"""

CSS = """
/* ---------- Home hero orbit visual ---------- */
main.vk .vk-orbit { position: relative; }
main.vk .vk-home-grid { grid-template-columns: 1fr 1.12fr !important; gap: 36px !important; }
@media (max-width: 1000px) { main.vk .vk-home-grid { grid-template-columns: 1fr !important; } }
main.vk .vk-orbit-svg { width: 100%; height: auto; display: block; overflow: visible; }
.vk-orbit .vk-ring { transform-box: view-box; transform-origin: 380px 330px; }
.vk-orbit .vk-ring.r1 { animation: vkSpin 120s linear infinite; }
.vk-orbit .vk-ring.r2 { animation: vkSpin 14s linear infinite; }
.vk-orbit .vk-ring.r3 { animation: vkSpin 40s linear infinite reverse; }
.vk-orbit .vk-spoke { stroke-dasharray: 8 220; stroke-dashoffset: 228; animation: vkSpoke 3.6s ease-in-out infinite; }
.vk-orbit .vk-pulse1, .vk-orbit .vk-pulse2 { transform-box: view-box; transform-origin: 380px 330px; animation: vkPulse 3.2s ease-out infinite; }
.vk-orbit .vk-pulse2 { animation-delay: 1.6s; }
.vk-orbit .vk-ctext { font-family: 'Space Grotesk', 'Inter', sans-serif; font-size: 11px; font-weight: 700; letter-spacing: 3px; fill: #94a3b8; }
.vk-orbit .vk-nlabel { font-family: 'Inter', sans-serif; font-size: 18px; font-weight: 600; fill: #cbd5e1; transition: fill .3s; }
.vk-orbit .vk-node { cursor: pointer; }
.vk-orbit .vk-node .disc, .vk-orbit .vk-node .halo { transition: all .35s ease; transform-box: fill-box; transform-origin: center; }
.vk-orbit .vk-node.on .disc { stroke-opacity: 1; fill: #111a2e; transform: scale(1.1); filter: url(#vkglow); }
.vk-orbit .vk-node.on .halo { opacity: 0.12; transform: scale(1.12); }
.vk-orbit .vk-node.on .vk-nlabel { fill: #fff; }
@keyframes vkSpin { to { transform: rotate(360deg); } }
@keyframes vkSpoke { 0% { stroke-dashoffset: 228; opacity: 0; } 10% { opacity: 1; } 70% { stroke-dashoffset: 0; opacity: 1; } 100% { stroke-dashoffset: 0; opacity: 0; } }
@keyframes vkPulse { 0% { transform: scale(1); opacity: .7; } 100% { transform: scale(1.7); opacity: 0; } }
main.vk .vk-orbit-cap { display: flex; flex-wrap: wrap; align-items: center; gap: 6px 10px; margin: 4px auto 0; max-width: 520px; padding: 12px 16px; border: 1px solid var(--vk-line); border-radius: 12px; background: rgba(11, 18, 36, 0.8); min-height: 64px; }
main.vk .vk-orbit-cap .vk-cdot { width: 9px; height: 9px; border-radius: 50%; background: #38bdf8; box-shadow: 0 0 10px currentColor; flex: none; }
main.vk .vk-orbit-cap .n { font-weight: 700 !important; color: #fff !important; font-size: 0.98rem !important; }
main.vk .vk-orbit-cap .d { flex: 1 1 100%; font-size: 0.88rem !important; color: #94a3b8 !important; line-height: 1.45 !important; order: 3; }
main.vk .vk-orbit-cap .go { margin-left: auto; font-size: 0.85rem !important; font-weight: 600 !important; }
@media (prefers-reduced-motion: reduce) {
  .vk-orbit .vk-ring, .vk-orbit .vk-spoke, .vk-orbit .vk-pulse1, .vk-orbit .vk-pulse2 { animation: none !important; }
  .vk-orbit .vk-spoke { stroke-dasharray: none; stroke-dashoffset: 0; opacity: .35; }
}
@media (max-width: 640px) { .vk-orbit .vk-nlabel { font-size: 23px; } }
"""
