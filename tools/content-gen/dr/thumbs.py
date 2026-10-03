"""Mini schematic thumbnails + linked cards for the five DR patterns (hub page)."""

ROWS = ['Web', 'App', 'DB', 'Data']
PAT = [
    ('backup-restore', 'Backup and restore', 1, 'Only backup copies at DR. Servers are built after the disaster.', 'Hours', 'Hours to days',
     [('none', 0), ('none', 0), ('none', 0), ('backup', 1)], [(3, 'batch')], ('Primary', 'DR')),
    ('pilot-light', 'Pilot light', 2, 'Data and a small database run at DR. Servers start from templates.', 'Minutes', 'A few hours',
     [('off', 0), ('off', 0), ('idle', 0.35), ('idle', 1)], [(2, 'stream'), (3, 'stream')], ('Primary', 'DR')),
    ('warm-standby', 'Warm standby', 3, 'The full stack runs at DR at reduced size and is scaled up.', 'Seconds to minutes', 'Under an hour to a few hours',
     [('idle', 0.25), ('idle', 0.25), ('idle', 1), ('idle', 1)], [(2, 'stream'), (3, 'stream')], ('Primary', 'DR')),
    ('active-passive', 'Active-passive', 4, 'A full-size synchronised copy takes over within minutes.', 'Near zero', 'Minutes',
     [('idle', 1), ('idle', 1), ('idle', 1), ('idle', 1)], [(2, 'sync'), (3, 'sync')], ('Primary', 'DR')),
    ('active-active', 'Active-active', 5, 'Both sites serve users. Losing one is close to invisible.', 'Near zero', 'Near zero',
     [('run', 1), ('run', 1), ('run', 1), ('run', 1)], [(2, 'bi'), (3, 'bi')], ('Site A', 'Site B')),
]
COL = {'run': '#38bdf8', 'idle': '#38bdf8', 'off': '#64748b', 'none': '#475569', 'backup': '#a5b4fc'}


def bar(x, y, w, h, st, cap, label):
    c = COL[st]
    o = []
    dash = ' stroke-dasharray="4 3"' if st in ('off', 'none') else ''
    sop = ' stroke-opacity="0.45"' if st == 'idle' else ''
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#0f172a" stroke="{c}" stroke-width="1.2"{dash}{sop}/>')
    if cap:
        op = {'run': 0.35, 'idle': 0.22, 'backup': 0.25}.get(st, 0.2)
        o.append(f'<rect x="{x+1}" y="{y+1}" width="{(w-2)*cap:.1f}" height="{h-2}" rx="3" fill="{c}" opacity="{op}"/>')
    o.append(f'<text x="{x+7}" y="{y+h/2+3.5}" font-size="10" fill="{"#64748b" if st in ("off","none") else "#cbd5e1"}">{label}</text>')
    return ''.join(o)


def thumb(dr, flows, titles):
    o = ['<svg viewBox="0 0 240 132" aria-hidden="true"><g font-family="Inter, sans-serif">']
    for x, t in ((6, titles[0]), (136, titles[1])):
        o.append(f'<rect x="{x}" y="4" width="98" height="124" rx="8" fill="#0b1224" stroke="#334155"/>')
        o.append(f'<text x="{x+49}" y="19" text-anchor="middle" font-size="10.5" font-weight="600" fill="#fff">{t}</text>')
    ys = [27, 52, 77, 102]
    for i, (lab, y) in enumerate(zip(ROWS, ys)):
        o.append(bar(13, y, 84, 20, 'run', 1, lab))
        st, cap = dr[i]
        o.append(bar(143, y, 84, 20, st, cap, lab))
    for row, kind in flows:
        y = ys[row] + 10
        if kind == 'bi':
            o.append(f'<line class="vk-flow vk-bi" x1="98" y1="{y-3}" x2="142" y2="{y-3}" stroke="#C2185B" stroke-width="2"/>')
            o.append(f'<line class="vk-flow vk-bi" x1="142" y1="{y+3}" x2="98" y2="{y+3}" stroke="#C2185B" stroke-width="2"/>')
        else:
            cls = {'batch': 'vk-batch3', 'stream': 'vk-stream', 'sync': 'vk-sync'}[kind]
            o.append(f'<line class="vk-flow {cls}" x1="98" y1="{y}" x2="142" y2="{y}" stroke="#C2185B" stroke-width="2"/>')
    o.append('</g></svg>')
    return ''.join(o)


def dots(n):
    return ''.join(f'<span class="{"on" if i <= n else ""}"></span>' for i in range(1, 6))


def cards():
    out = ['<div class="vk-patterns vk-refarch">']
    for slug, name, cost, line, rpo, rto, dr, flows, titles in PAT:
        out.append(f'''<a class="vk-card vk-pat" href="/solutions/dc-dr/{slug}">
                    <div class="vk-pat-thumb">{thumb(dr, flows, titles)}</div>
                    <span class="vk-muted vk-small">Pattern {cost} of 5</span>
                    <h3>{name}</h3>
                    <p>{line}</p>
                    <div class="vk-pat-meta"><span><b>RPO</b> {rpo}</span><span><b>RTO</b> {rto}</span></div>
                    <div class="vk-pat-cost"><span class="vk-muted vk-small">Cost</span><span class="vk-dots">{dots(cost)}</span></div>
                    <span class="vk-go">View architecture &rarr;</span>
                </a>''')
    out.append('</div>')
    return '\n                '.join(out)


CSS = """
/* ---------- Pattern cards with mini diagrams (hub) ---------- */
main.vk .vk-patterns { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 14px; margin-top: 22px; }
main.vk a.vk-pat { display: flex; flex-direction: column; padding: 14px; }
main.vk .vk-pat-thumb { background: #070d1c; border: 1px solid var(--vk-line); border-radius: 10px; padding: 6px; margin-bottom: 12px; }
main.vk .vk-pat-thumb svg { width: 100%; height: auto; display: block; }
main.vk a.vk-pat h3 { margin: 2px 0 6px !important; }
main.vk a.vk-pat p { font-size: 0.88rem !important; line-height: 1.5 !important; margin-bottom: 10px; }
main.vk .vk-pat-meta { display: grid; gap: 2px; margin-bottom: 8px; }
main.vk .vk-pat-meta span, main.vk .vk-pat-meta b { font-size: 0.82rem !important; color: var(--vk-muted) !important; }
main.vk .vk-pat-meta b { color: #fff !important; font-weight: 600 !important; margin-right: 4px; }
main.vk .vk-pat-cost { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
main.vk .vk-pat .vk-go { margin-top: auto; padding-top: 8px; }
main.vk .vk-dots { display: inline-flex !important; gap: 5px; }
main.vk .vk-dots span { width: 10px; height: 10px; border-radius: 50%; border: 1px solid #475569; display: inline-block; }
main.vk .vk-dots span.on { background: var(--vk-accent); border-color: var(--vk-accent); }
.vk-refarch .vk-flow.vk-batch3 { stroke-dasharray: 10 120; animation: vkBatch3 2.6s linear infinite; }
@keyframes vkBatch3 { from { stroke-dashoffset: 10; } to { stroke-dashoffset: -120; } }
"""
