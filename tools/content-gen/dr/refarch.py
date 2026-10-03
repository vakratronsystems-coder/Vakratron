"""Static reference-architecture SVG renderer for DR pattern pages.

A diagram is described as:
  panels: titles for the two site panels
  rows:   number of rows inside each panel
  nodes:  id -> dict(zone='P'|'D'|'G'|'B', row=int, col='full'|'l'|'r', x=, w= (G/B only), title, sub, style)
  flows:  list of dict(a=id, b=id, n=badge number or None, kind=stream|sync|batch|bi|ondemand|traffic|failover|hb|deploy)
Styles: run, idle, off, none, backup.
"""
from html import escape

COL = {'run': '#38bdf8', 'idle': '#38bdf8', 'off': '#64748b', 'none': '#475569', 'backup': '#a5b4fc', 'global': '#94a3b8', 'witness': '#fbbf24'}
FILL_OP = {'run': 0.24, 'idle': 0.05, 'backup': 0.16, 'witness': 0.1}
FLOW = {
    'stream':   ('#C2185B', 3, 'vk-flow vk-stream', None),
    'sync':     ('#C2185B', 3, 'vk-flow vk-sync', None),
    'batch':    ('#C2185B', 3, 'vk-flow vk-batch2', None),
    'bi':       ('#C2185B', 3, 'vk-flow vk-bi', None),
    'ondemand': ('#f59e0b', 2, '', '7 5'),
    'traffic':  ('#e2e8f0', 2, 'vk-flow vk-traffic', None),
    'failover': ('#64748b', 2, '', '5 5'),
    'hb':       ('#fbbf24', 1.5, 'vk-flow vk-hb', None),
    'deploy':   ('#38bdf8', 1.5, '', '3 4'),
}
MARK = {'#C2185B': 'mk-pink', '#f59e0b': 'mk-amber', '#e2e8f0': 'mk-white', '#64748b': 'mk-slate', '#fbbf24': 'mk-gold', '#38bdf8': 'mk-blue'}

W = 960
PX = {'P': 20, 'D': 540}
PW = 400
TOP = 120          # panel top
ROW0 = 60          # first row offset inside panel
RH = 62            # node height
RS = 86            # row step


def layout(d):
    nodes = {}
    for nid, n in d['nodes'].items():
        z = n['zone']
        if z in ('P', 'D'):
            x0 = PX[z] + 18
            full = PW - 36
            half = (full - 14) / 2
            col = n.get('col', 'full')
            x = x0 if col in ('full', 'l') else x0 + half + 14
            w = full if col == 'full' else half
            y = TOP + ROW0 + n['row'] * RS
        elif z == 'G':
            x, w, y = n['x'], n['w'], 20
        else:  # B, below panels
            x, w, y = n['x'], n['w'], panel_bottom(d) + 34
        nodes[nid] = dict(n, x=x, y=y, w=w, h=RH if z in ('P', 'D') else 54)
    return nodes


def panel_bottom(d):
    return TOP + ROW0 + d['rows'] * RS - (RS - RH) + 22


def height(d):
    h = panel_bottom(d) + 20
    if any(n['zone'] == 'B' for n in d['nodes'].values()):
        h += 34 + 54 + 10
    return h


def node_svg(n):
    st = n.get('style', 'run')
    c = COL.get(st, COL['run'])
    dash = ' stroke-dasharray="6 5"' if st in ('off', 'none') else ''
    out = [f'<g opacity="{0.75 if st == "none" else 1}">']
    sop = ' stroke-opacity="0.45"' if st == 'idle' else ''
    out.append(f'<rect x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{n["h"]}" rx="9" fill="#0f172a" stroke="{c}" stroke-width="1.5"{dash}{sop}/>')
    if st in FILL_OP:
        out.append(f'<rect x="{n["x"]+1}" y="{n["y"]+1}" width="{n["w"]-2}" height="{n["h"]-2}" rx="8" fill="{c}" opacity="{FILL_OP[st]}"/>')
    cx = n['x'] + n['w'] / 2
    ty = n['y'] + (24 if n.get('sub') else n['h'] / 2 + 5)
    out.append(f'<text x="{cx}" y="{ty}" text-anchor="middle" font-size="14" font-weight="600" fill="{"#cbd5e1" if st == "none" else "#f1f5f9"}">{escape(n["title"])}</text>')
    if n.get('sub'):
        out.append(f'<text x="{cx}" y="{n["y"]+44}" text-anchor="middle" font-size="11.5" fill="#94a3b8">{escape(n["sub"])}</text>')
    out.append('</g>')
    return ''.join(out)


def anchor(n, side):
    if side == 'r': return (n['x'] + n['w'], n['y'] + n['h'] / 2)
    if side == 'l': return (n['x'], n['y'] + n['h'] / 2)
    if side == 't': return (n['x'] + n['w'] / 2, n['y'])
    return (n['x'] + n['w'] / 2, n['y'] + n['h'])


def route(a, b, nodes, d, off=0):
    """Return list of points for a flow from node a to node b."""
    A, B = nodes[a] if a in nodes else None, nodes[b] if b in nodes else None
    if b in ('P', 'D'):  # to a panel top
        sx, sy = anchor(A, 'b')
        tx, ty = PX[b] + PW / 2, TOP
        if A['zone'] == 'G' and A['x'] > 700: tx += 110
        sx = sx + (-30 if b == 'P' else 30) if A['zone'] == 'G' and A['w'] > 120 else sx
        my = (sy + ty) / 2
        return [(sx, sy), (sx, my), (tx, my), (tx, ty)]
    if a in ('P', 'D'):
        raise ValueError
    za, zb = A['zone'], B['zone']
    if za == 'B':  # witness to panel bottom
        sx, sy = anchor(A, 't')
        sx += -40 if zb == 'P' else 40
        tx, ty = PX[zb] + PW / 2, panel_bottom(d)
        my = (sy + ty) / 2
        return [(sx, sy), (sx, my), (tx, my), (tx, ty)]
    if za == 'G' and zb in ('P', 'D'):
        sx, sy = anchor(A, 'b')
        tx, ty = PX[zb] + PW / 2, TOP
        return [(sx, sy), (sx, sy + 20), (tx, sy + 20), (tx, ty)]
    if za != zb:  # across panels
        left, right = (A, B) if A['x'] < B['x'] else (B, A)
        sx, sy = anchor(left, 'r'); tx, ty = anchor(right, 'l')
        sy += off; ty += off
        pts = [(sx, sy), (tx, ty)] if abs(sy - ty) < 1 else [(sx, sy), (W / 2, sy), (W / 2, ty), (tx, ty)]
        return pts if left is A else pts[::-1]
    # same panel
    if A['row'] == B['row']:
        left, right = (A, B) if A['x'] < B['x'] else (B, A)
        pts = [anchor(left, 'r'), anchor(right, 'l')]
        return pts if left is A else pts[::-1]
    up = A['y'] > B['y']
    s = anchor(A, 't' if up else 'b'); t = anchor(B, 'b' if up else 't')
    if abs(s[0] - t[0]) < 1:
        return [s, t]
    my = (s[1] + t[1]) / 2
    return [s, (s[0], my), (t[0], my), t]


def path_d(pts):
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)


def longest_mid(pts):
    best, bl = None, -1
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        l = abs(x2 - x1) + abs(y2 - y1)
        if l > bl: bl, best = l, ((x1 + x2) / 2, (y1 + y2) / 2)
    return best


def render(d, label):
    nodes = layout(d)
    H = height(d)
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{escape(label)}">', '<defs>']
    for col, mid in MARK.items():
        o.append(f'<marker id="{mid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{col}"/></marker>')
    o.append('</defs><g font-family="Inter, sans-serif">')
    pb = panel_bottom(d)
    for z, title in zip(('P', 'D'), d['panels']):
        o.append(f'<rect x="{PX[z]}" y="{TOP}" width="{PW}" height="{pb-TOP}" rx="14" fill="#0b1224" stroke="#334155"/>')
        o.append(f'<text x="{PX[z]+PW/2}" y="{TOP+34}" text-anchor="middle" font-size="15" font-weight="700" fill="#fff">{escape(title)}</text>')
    badges = []
    for f in d['flows']:
        col, sw, cls, dash = FLOW[f['kind']]
        mk = MARK[col]
        if f['kind'] == 'bi':
            for off, rev in ((-5, False), (5, True)):
                pts = route(f['a'], f['b'], nodes, d, off)
                if rev: pts = pts[::-1]
                o.append(f'<path class="{cls}" d="{path_d(pts)}" fill="none" stroke="{col}" stroke-width="{sw}" marker-end="url(#{mk})"/>')
            pts = route(f['a'], f['b'], nodes, d)
        else:
            pts = route(f['a'], f['b'], nodes, d)
            if cls and 'vk-flow' in cls and f['kind'] not in ('traffic', 'hb'):
                o.append(f'<path d="{path_d(pts)}" fill="none" stroke="#1e293b" stroke-width="{sw}"/>')
            da = f' stroke-dasharray="{dash}"' if dash else ''
            o.append(f'<path class="{cls}" d="{path_d(pts)}" fill="none" stroke="{col}" stroke-width="{sw}"{da} marker-end="url(#{mk})"/>')
        if f.get('n'):
            badges.append((longest_mid(pts), f['n'], col))
    for nid, n in nodes.items():
        o.append(node_svg(n))
    for (x, y), num, col in badges:
        o.append(f'<circle cx="{x}" cy="{y}" r="11" fill="#020617" stroke="{col}" stroke-width="1.5"/><text x="{x}" y="{y+4}" text-anchor="middle" font-size="11.5" font-weight="700" fill="#fff">{num}</text>')
    o.append('</g></svg>')
    return ''.join(o)
