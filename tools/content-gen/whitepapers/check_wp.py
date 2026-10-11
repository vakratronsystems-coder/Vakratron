"""Usage: python3 check_wp.py <module>
Builds the web page and the PDF for one whitepaper module, renders previews and runs text checks.
Outputs in /home/claude/dp/wpcheck/<module>/: page.png (web, top part), pdf-sheet.png (all PDF pages), diagram.png, <slug>.pdf"""
import sys, os, re, json, subprocess, importlib, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
mod = sys.argv[1]
out = '/home/claude/dp/wpcheck/' + mod
os.makedirs(out, exist_ok=True)
pw = '/home/claude/dp/pdfwork'
r = subprocess.run(['python3', 'wp_render.py', mod, out + '/print.html'], cwd=HERE, capture_output=True, text=True)
print(r.stdout.strip(), r.stderr[-800:])
for f in ['wp-print.css', 'logo.png']:
    shutil.copy(os.path.join(pw, f), out)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'deployments'))
M = importlib.import_module(mod)
title = M.META['title']
r = subprocess.run('NODE_PATH=$(npm root -g) node %s/mkpdf2.js %s/print "x" "%s"' % (pw, out, title.replace('"', '')), shell=True, capture_output=True, text=True)
print(r.stderr[-500:])
from pypdf import PdfWriter, PdfReader
w = PdfWriter()
for f in [out + '/print-cover.pdf', out + '/print-body.pdf']:
    for pg in PdfReader(f).pages: w.add_page(pg)
w.add_metadata({'/Title': title, '/Author': 'Vakratron Systems', '/Subject': M.META['subtitle']})
pdf = out + '/' + M.META['slug'] + '.pdf'
w.write(pdf)
n = len(PdfReader(pdf).pages)
subprocess.run('rm -f %s/pg-*.png; pdftoppm -r 40 -png %s %s/pg 2>/dev/null' % (out, pdf, out), shell=True)
from PIL import Image
import glob
fs = sorted(glob.glob(out + '/pg-*.png')); ims = [Image.open(f) for f in fs]; W, H = ims[0].size
cols = 6; rows = (len(ims) + cols - 1) // cols
o = Image.new('RGB', (cols * W + (cols + 1) * 8, rows * H + (rows + 1) * 8), (90, 90, 90))
for i, im in enumerate(ims): o.paste(im, (8 + (i % cols) * (W + 8), 8 + (i // cols) * (H + 8)))
o.save(out + '/pdf-sheet.png')
import diagram
open(out + '/dg.html', 'w').write('<html><body style="margin:0;background:#020617">' + diagram.render(M.DIAGRAM, 'x') + '</body></html>')
js = "const { chromium } = require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:%d,height:%d}});await p.goto('file://%s/dg.html');await p.screenshot({path:'%s/diagram.png'});await b.close();})();" % (M.DIAGRAM['w'], M.DIAGRAM['h'] + 50, out, out)
open(out + '/dg.js', 'w').write(js)
subprocess.run('NODE_PATH=$(npm root -g) node %s/dg.js' % out, shell=True)
# text checks
txt = ' '.join(re.sub('<[^>]+>', ' ', s['html']) for s in M.SECTIONS)
words = len(txt.split())
probs = []
for b in ['sovereign', 'matrix', 'vector', 'battle-tested', 'battle tested', 'cutting edge', 'cutting-edge', 'revolutionary', 'seamless', 'leverage', 'robust', 'world-class', 'state-of-the-art', 'tata', 'vayu', 'indiaai', 'meity', '—']:
    if b in (txt + json.dumps(M.META)).lower(): probs.append('BANNED: ' + b)
if ' & ' in txt: probs.append('raw & in text')
need = ['slug', 'title', 'subtitle', 'topic', 'area', 'version', 'pages', 'minutes', 'audience', 'audience_web', 'desc', 'inside', 'help_title', 'help_items', 'help_links']
for k in need:
    if k not in M.META: probs.append('META missing ' + k)
nchk = sum(len(i) for _, i in M.CHECKLIST)
print('PDF pages', n, '| words', words, '| sections', len(M.SECTIONS), '| checklist points', nchk)
print('problems:', probs or 'none')
print('outputs:', out)
