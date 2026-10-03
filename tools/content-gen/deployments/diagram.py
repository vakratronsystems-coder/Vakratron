"""Enterprise reference-diagram renderer for deployment scenario pages.

zones: list of dict(x, y, w, h, title, kind, note='')
nodes: dict id -> dict(x, y, w, title, sub='', icon='server', tone='blue', state='run'|'off', tag='')
flows: list of dict(a, b, kind, label='', n=None, sa=None, sb=None, via=None)
  kind: traffic | data | sync | batch | control | alert | mgmt
  sa / sb: anchor side on a / b ('l','r','t','b') or (side, offset)
  via: explicit list of (x, y) points between start and end anchors
"""
from html import escape

NH = 58
TONE = {'blue': '#38bdf8', 'pink': '#f472b6', 'green': '#34d399', 'amber': '#fbbf24', 'violet': '#a78bfa', 'slate': '#94a3b8'}
ZONE = {
    'cloud': ('#fbbf24', 'rgba(251,191,36,0.04)'),
    'dc':    ('#38bdf8', 'rgba(56,189,248,0.04)'),
    'dr':    ('#a78bfa', 'rgba(167,139,250,0.05)'),
    'ext':   ('#94a3b8', 'rgba(148,163,184,0.04)'),
    'sec':   ('#f472b6', 'rgba(244,114,182,0.04)'),
    'ai':    ('#a78bfa', 'rgba(167,139,250,0.05)'),
    'ent':   ('#34d399', 'rgba(52,211,153,0.04)'),
}
FLOW = {  # colour, width, css class, dash, legend text
    'traffic': ('#e2e8f0', 1.8, 'vk-flow vk-traffic', None, 'User or API traffic'),
    'data':    ('#C2185B', 2.6, 'vk-flow vk-stream', None, 'Data / replication'),
    'sync':    ('#C2185B', 2.6, 'vk-flow vk-sync', None, 'Synchronous write'),
    'batch':   ('#a78bfa', 2.2, 'vk-flow vk-batch2', None, 'Scheduled copy'),
    'control': ('#38bdf8', 1.6, '', '6 5', 'Control / API call'),
    'alert':   ('#fbbf24', 1.8, 'vk-flow vk-hb', None, 'Exception / alert'),
    'mgmt':    ('#64748b', 1.4, '', '3 4', 'Logging / management'),
}

I = {
 'server': '<rect x="3" y="3" width="18" height="7" rx="1.5"/><rect x="3" y="14" width="18" height="7" rx="1.5"/><path d="M7 6.5h.01M7 17.5h.01M11 6.5h6M11 17.5h6"/>',
 'storage': '<ellipse cx="12" cy="5.5" rx="8" ry="2.8"/><path d="M4 5.5v13c0 1.5 3.6 2.8 8 2.8s8-1.3 8-2.8v-13M4 12c0 1.5 3.6 2.8 8 2.8s8-1.3 8-2.8"/>',
 'cloud': '<path d="M7 18.5h10.5a4 4 0 0 0 .4-8 6 6 0 0 0-11.6-1A4.6 4.6 0 0 0 7 18.5z"/>',
 'users': '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.4 2.7-6 6-6s6 2.6 6 6"/><circle cx="17.2" cy="9" r="2.4"/><path d="M16.4 14.3c2.6.4 4.6 2.7 4.6 5.7"/>',
 'firewall': '<rect x="3" y="4" width="18" height="16" rx="1.5"/><path d="M3 9.3h18M3 14.7h18M9 4v5.3M15 4v5.3M6 9.3v5.4M12 9.3v5.4M18 9.3v5.4M9 14.7V20M15 14.7V20"/>',
 'shield': '<path d="M12 3l8 3v6c0 4.6-3.4 8.3-8 9-4.6-.7-8-4.4-8-9V6z"/><path d="M8.5 12l2.4 2.4 4.6-4.8"/>',
 'eye': '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 'key': '<circle cx="7.5" cy="15.5" r="4.5"/><path d="M10.7 12.3L20 3M16 7l3 3M13.8 9.2l2 2"/>',
 'switch': '<rect x="2" y="7" width="20" height="10" rx="2"/><path d="M6 12h.01M9.5 12h.01M13 12h.01M16.5 12h3"/>',
 'lb': '<circle cx="12" cy="5" r="2.2"/><circle cx="5" cy="19" r="2.2"/><circle cx="12" cy="19" r="2.2"/><circle cx="19" cy="19" r="2.2"/><path d="M12 7.2v9.6M11 7l-5 10M13 7l5 10"/>',
 'gpu': '<rect x="2.5" y="6" width="19" height="11" rx="2"/><circle cx="9" cy="11.5" r="3"/><path d="M15 9h3.5M15 12h3.5M15 15h2M5 17v3M9 17v3M13 17v3M17 17v3"/>',
 'k8s': '<path d="M12 2.5l8.2 4.75v9.5L12 21.5l-8.2-4.75v-9.5z"/><circle cx="12" cy="12" r="2.6"/><path d="M12 5.5v3.9M12 14.6v3.9M6.3 8.7l3.4 2M14.3 13.3l3.4 2M6.3 15.3l3.4-2M14.3 10.7l3.4-2"/>',
 'llm': '<path d="M11 3l1.8 5.2L18 10l-5.2 1.8L11 17l-1.8-5.2L4 10l5.2-1.8z"/><path d="M18.5 15l.8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8z"/>',
 'robot': '<rect x="4" y="8" width="16" height="11" rx="3"/><circle cx="9" cy="13.5" r="1.3"/><circle cx="15" cy="13.5" r="1.3"/><path d="M12 8V4.5M10 4.5h4M2 12.5v3M22 12.5v3"/>',
 'doc': '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
 'queue': '<rect x="3" y="4" width="18" height="4" rx="1"/><rect x="3" y="10" width="18" height="4" rx="1"/><rect x="3" y="16" width="18" height="4" rx="1"/>',
 'chart': '<path d="M4 4v16h16"/><path d="M8 16v-4M12 16V8M16 16v-6"/>',
 'lock': '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
 'archive': '<rect x="3" y="4" width="18" height="5" rx="1"/><path d="M5 9v11h14V9M10 13h4"/>',
 'git': '<circle cx="6" cy="6" r="2.2"/><circle cx="6" cy="18" r="2.2"/><circle cx="18" cy="8" r="2.2"/><path d="M6 8.2v7.6M18 10.2c0 4-6 3-10.4 6.4"/>',
 'globe': '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/>',
 'building': '<path d="M4 21V5l8-3v19M12 8l8 3v10M2 21h20M7 8h2M7 12h2M7 16h2M15 13h2M15 17h2"/>',
 'vm': '<rect x="3" y="4" width="18" height="13" rx="2"/><path d="M8 21h8M12 17v4M7 9l3 2-3 2M12 13h5"/>',
 'link': '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
 'flow': '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/><path d="M10 6.5h4.5a3 3 0 0 1 3 3V14"/>',
 'search': '<circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.3-4.3"/>',
 'grid': '<rect x="3" y="3" width="7.5" height="7.5" rx="1.5"/><rect x="13.5" y="3" width="7.5" height="7.5" rx="1.5"/><rect x="3" y="13.5" width="7.5" height="7.5" rx="1.5"/><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="1.5"/>',
 'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7.5l9 6 9-6"/>',
 'check': '<circle cx="12" cy="12" r="9"/><path d="M8 12.3l2.7 2.7L16 9.5"/>',
 'person': '<circle cx="10" cy="7.5" r="3.8"/><path d="M3 21c0-4 3.1-7 7-7 1.4 0 2.7.4 3.8 1.1M15.5 18l2 2 4-4.2"/>',
 'money': '<rect x="2.5" y="6" width="19" height="12" rx="2"/><circle cx="12" cy="12" r="2.8"/><path d="M6 9.5v5M18 9.5v5"/>',
 'scan': '<path d="M4 8V5a1 1 0 0 1 1-1h3M16 4h3a1 1 0 0 1 1 1v3M20 16v3a1 1 0 0 1-1 1h-3M8 20H5a1 1 0 0 1-1-1v-3M7 12h10"/>',
 'cog': '<circle cx="12" cy="12" r="3"/><path d="M12 2.5v3M12 18.5v3M21.5 12h-3M5.5 12h-3M18.7 5.3l-2.1 2.1M7.4 16.6l-2.1 2.1M18.7 18.7l-2.1-2.1M7.4 7.4L5.3 5.3"/>',
 'radar': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><path d="M12 12l6-6"/><circle cx="12" cy="12" r="1"/>',
 'bolt': '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
 'phone': '<rect x="7" y="2.5" width="10" height="19" rx="2"/><path d="M11 18h2"/>',
 'mic': '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21"/>',
 'factory': '<path d="M3 21V10l5 3V10l5 3V10l5 3V4h3v17z"/><path d="M7 17h2M12 17h2M17 17h2"/>',
 'model': '<circle cx="5" cy="6" r="2"/><circle cx="5" cy="18" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="19" cy="6" r="2"/><circle cx="19" cy="18" r="2"/><path d="M7 6.8l3.2 4M7 17.2l3.2-4M14 11.2l3.2-4M14 12.8l3.2 4"/>',
}


def anchor(n, side, off=0):
    x, y, w, h = n['x'], n['y'], n['w'], n.get('h', NH)
    if side == 'r': return (x + w, y + h / 2 + off)
    if side == 'l': return (x, y + h / 2 + off)
    if side == 't': return (x + w / 2 + off, y)
    return (x + w / 2 + off, y + h)


def auto_sides(A, B):
    ax, ay = A['x'] + A['w'] / 2, A['y'] + NH / 2
    bx, by = B['x'] + B['w'] / 2, B['y'] + NH / 2
    if abs(bx - ax) >= abs(by - ay) * 1.4:
        return ('r', 'l') if bx > ax else ('l', 'r')
    return ('b', 't') if by > ay else ('t', 'b')


def side_of(v):
    if v is None: return None, 0
    if isinstance(v, tuple): return v
    return v, 0


def route(f, nodes):
    A, B = nodes[f['a']], nodes[f['b']]
    sa, oa = side_of(f.get('sa')); sb, ob = side_of(f.get('sb'))
    da, db = auto_sides(A, B)
    sa = sa or da; sb = sb or db
    s = anchor(A, sa, oa); t = anchor(B, sb, ob)
    if f.get('via'):
        return [s] + list(f['via']) + [t]
    if abs(s[0] - t[0]) < 0.5 or abs(s[1] - t[1]) < 0.5:
        return [s, t]
    if sa in ('l', 'r') and sb in ('l', 'r'):
        mx = (s[0] + t[0]) / 2
        return [s, (mx, s[1]), (mx, t[1]), t]
    if sa in ('t', 'b') and sb in ('t', 'b'):
        my = (s[1] + t[1]) / 2
        return [s, (s[0], my), (t[0], my), t]
    if sa in ('l', 'r'):
        return [s, (t[0], s[1]), t]
    return [s, (s[0], t[1]), t]


def pd(pts):
    return 'M' + ' L'.join('%.1f,%.1f' % p for p in pts)


def longest_mid(pts):
    best, bl, horiz = None, -1, True
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        l = abs(x2 - x1) + abs(y2 - y1)
        if l > bl:
            bl, best, horiz = l, ((x1 + x2) / 2, (y1 + y2) / 2), abs(y2 - y1) < 0.5
    return best, horiz


def node_svg(nid, n):
    c = TONE.get(n.get('tone', 'blue'))
    off = n.get('state') == 'off'
    h = n.get('h', NH)
    x, y, w = n['x'], n['y'], n['w']
    o = ['<g class="dg-node" opacity="%s">' % ('0.72' if off else '1')]
    o.append('<rect x="%s" y="%s" width="%s" height="%s" rx="10" fill="#0f172a" stroke="%s" stroke-width="1.4"%s/>' % (x, y, w, h, c, ' stroke-dasharray="5 4"' if off else ''))
    o.append('<rect x="%s" y="%s" width="32" height="32" rx="8" fill="%s" fill-opacity="0.14"/>' % (x + 11, y + (h - 32) / 2, c))
    o.append('<g transform="translate(%s %s)" fill="none" stroke="%s" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">%s</g>' % (x + 15, y + (h - 24) / 2, c, I[n.get('icon', 'server')]))
    tx = x + 53
    if n.get('sub'):
        o.append('<text x="%s" y="%s" font-size="12.5" font-weight="600" fill="#f1f5f9">%s</text>' % (tx, y + h / 2 - 3, escape(n['title'])))
        o.append('<text x="%s" y="%s" font-size="10.5" fill="#94a3b8">%s</text>' % (tx, y + h / 2 + 13, escape(n['sub'])))
    else:
        o.append('<text x="%s" y="%s" font-size="12.5" font-weight="600" fill="#f1f5f9">%s</text>' % (tx, y + h / 2 + 4, escape(n['title'])))
    if n.get('tag'):
        tw = 9 + 6.2 * len(n['tag'])
        o.append('<rect x="%s" y="%s" width="%s" height="15" rx="7.5" fill="#020617" stroke="%s"/>' % (x + w - tw - 8, y - 7.5, tw, '#fbbf24' if off else c))
        o.append('<text x="%s" y="%s" text-anchor="middle" font-size="8.5" font-weight="700" letter-spacing="0.06em" fill="%s">%s</text>' % (x + w - tw / 2 - 8, y + 3.3, '#fbbf24' if off else c, escape(n['tag'])))
    o.append('</g>')
    return ''.join(o)


def render(d, label):
    W, H = d['w'], d['h']
    nodes = d['nodes']
    o = ['<svg class="vk-dg" viewBox="0 0 %s %s" role="img" aria-label="%s" xmlns="http://www.w3.org/2000/svg">' % (W, H + 46, escape(label)), '<defs>']
    used = []
    for f in d['flows']:
        if f['kind'] not in used: used.append(f['kind'])
    for k in used:
        col = FLOW[k][0]
        o.append('<marker id="dg-%s" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker>' % (k, col))
    o.append('</defs><g font-family="Inter, sans-serif">')
    for z in d['zones']:
        c, fill = ZONE[z['kind']]
        o.append('<rect x="%s" y="%s" width="%s" height="%s" rx="14" fill="%s" stroke="%s" stroke-opacity="0.45" stroke-dasharray="%s"/>' % (z['x'], z['y'], z['w'], z['h'], fill, c, '6 5' if z.get('dashed') else '0'))
        o.append('<circle cx="%s" cy="%s" r="4" fill="%s"/>' % (z['x'] + 18, z['y'] + 20, c))
        o.append('<text x="%s" y="%s" font-size="11" font-weight="700" letter-spacing="0.08em" fill="%s">%s</text>' % (z['x'] + 29, z['y'] + 24, c, escape(z['title'].upper())))
        if z.get('note'):
            o.append('<text x="%s" y="%s" text-anchor="end" font-size="10.5" fill="#64748b">%s</text>' % (z['x'] + z['w'] - 14, z['y'] + 24, escape(z['note'])))
    labels, badges = [], []
    for f in d['flows']:
        col, sw, cls, dash, _ = FLOW[f['kind']]
        pts = route(f, nodes)
        da = ' stroke-dasharray="%s"' % dash if dash else ''
        if cls:
            o.append('<path d="%s" fill="none" stroke="#1e293b" stroke-width="%s"/>' % (pd(pts), sw))
        start = ' marker-start="url(#dg-%s)"' % f['kind'] if f.get('both') else ''
        o.append('<path class="%s" d="%s" fill="none" stroke="%s" stroke-width="%s"%s marker-end="url(#dg-%s)"%s/>' % (cls, pd(pts), col, sw, da, f['kind'], start))
        (mx, my), horiz = longest_mid(pts)
        if f.get('lpos'): mx, my = f['lpos']
        if f.get('label'):
            labels.append((mx, my, f['label'], col, f.get('n')))
        elif f.get('n'):
            badges.append((mx, my, f['n'], col))
    for nid, n in nodes.items():
        o.append(node_svg(nid, n))
    for mx, my, text, col, num in labels:
        tw = 6.0 * len(text) + 14 + (20 if num else 0)
        x0 = mx - tw / 2
        o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="18" rx="9" fill="#020617" stroke="%s" stroke-opacity="0.7"/>' % (x0, my - 9, tw, col))
        tx = x0 + 9
        if num:
            o.append('<circle cx="%.1f" cy="%.1f" r="7" fill="%s"/><text x="%.1f" y="%.1f" text-anchor="middle" font-size="9" font-weight="700" fill="#020617">%s</text>' % (x0 + 10, my, col, x0 + 10, my + 3.2, num))
            tx = x0 + 21
        o.append('<text x="%.1f" y="%.1f" font-size="10" fill="#e2e8f0">%s</text>' % (tx, my + 3.5, escape(text)))
    for mx, my, num, col in badges:
        o.append('<circle cx="%.1f" cy="%.1f" r="10" fill="#020617" stroke="%s" stroke-width="1.5"/><text x="%.1f" y="%.1f" text-anchor="middle" font-size="10.5" font-weight="700" fill="#fff">%s</text>' % (mx, my, col, mx, my + 3.8, num))
    # legend
    lx, ly = 20, H + 22
    for k in used:
        col, sw, cls, dash, text = FLOW[k]
        da = ' stroke-dasharray="%s"' % dash if dash else (' stroke-dasharray="3 5"' if cls else '')
        o.append('<path d="M%s,%s h26" stroke="%s" stroke-width="%s"%s/>' % (lx, ly, col, sw, da))
        o.append('<text x="%s" y="%s" font-size="10.5" fill="#94a3b8">%s</text>' % (lx + 32, ly + 3.5, text))
        lx += 52 + 5.8 * len(text)
    o.append('</g></svg>')
    return ''.join(o)
