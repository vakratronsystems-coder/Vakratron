"""Usage: python3 check_one.py <module_name>
Renders the scenario page into /home/claude/dp/views/deployments/<slug>.html and the diagram to /home/claude/dp/check/<module>.png,
and prints basic checks (banned words, text overflow estimates, node overlaps, nodes outside zones/canvas)."""
import sys, os, re, importlib, subprocess, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import diagram
mod = importlib.import_module(sys.argv[1]); S = mod.S; D = S['diagram']
from scenario import build
build(S, [S])
os.makedirs('/home/claude/dp/check', exist_ok=True)
svg = diagram.render(D, S['h1'])
open('/home/claude/dp/check/%s.html' % sys.argv[1], 'w').write('<html><body style="margin:0;background:#020617">' + svg + '</body></html>')
# checks
txt = json.dumps(S, ensure_ascii=False)
for w in ['sovereign','matrix','vector','battle-tested','cutting edge','cutting-edge','revolutionary','tata','vayu','indiaai','seamless','leverage','robust','state-of-the-art','world-class','—']:
    if w in txt.lower(): print('BANNED/STYLE WORD:', w)
nodes = D['nodes']; probs = 0
for k, n in nodes.items():
    h = n.get('h', 58)
    tw = 53 + max(7.0 * len(n['title']), 5.2 * len(n.get('sub', ''))) + 8
    if tw > n['w']: print('TEXT TOO WIDE:', k, int(tw), '>', n['w']); probs += 1
    if n['x'] + n['w'] > D['w'] or n['y'] + h > D['h']: print('OUTSIDE CANVAS:', k); probs += 1
    inside = [z for z in D['zones'] if z['x'] <= n['x'] and z['y'] + 30 <= n['y'] and n['x'] + n['w'] <= z['x'] + z['w'] and n['y'] + h <= z['y'] + z['h']]
    if not inside: print('NOT INSIDE A ZONE (or overlaps zone title row):', k); probs += 1
ks = list(nodes)
for i in range(len(ks)):
    for j in range(i + 1, len(ks)):
        a, b = nodes[ks[i]], nodes[ks[j]]
        if a['x'] < b['x'] + b['w'] and b['x'] < a['x'] + a['w'] and a['y'] < b['y'] + 58 and b['y'] < a['y'] + 58:
            print('NODE OVERLAP:', ks[i], ks[j]); probs += 1
for f in D['flows']:
    for e in ('a', 'b'):
        if f[e] not in nodes: print('BAD FLOW REF', f)
    if f.get('kind') not in diagram.FLOW: print('BAD KIND', f)
for n in nodes.values():
    if n.get('icon', 'server') not in diagram.I: print('BAD ICON', n.get('icon'))
js = """const { chromium } = require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:%d,height:%d}});await p.goto('file:///home/claude/dp/check/%s.html');await p.waitForTimeout(300);await p.screenshot({path:'/home/claude/dp/check/%s.png',fullPage:true});await b.close();})();""" % (D['w'], D['h'] + 50, sys.argv[1], sys.argv[1])
open('/tmp/_shot.js', 'w').write(js)
r = subprocess.run('NODE_PATH=$(npm root -g) node /tmp/_shot.js', shell=True, capture_output=True, text=True)
print('screenshot:', '/home/claude/dp/check/%s.png' % sys.argv[1], r.stderr[-300:])
print('checks done, problems:', probs)
