"""Build all reference-deployment pages. Run from tools/content-gen/deployments/."""
import os, sys, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from scenario import build

MODULES = ['s_cloud_repatriation', 's_agentic_ap']
SC = []
for m in MODULES:
    try:
        SC.append(importlib.import_module(m).S)
    except ModuleNotFoundError:
        pass
for s in SC:
    build(s, SC)

# CSS part
root = os.path.join(HERE, '..', '..', '..')
css = os.path.join(root, 'public', 'vk-content.css')
t = open(css, encoding='utf-8', newline='').read()
new = open(os.path.join(HERE, 'dp.css.part'), encoding='utf-8').read().strip()
A, B = '/* === DEPLOYMENT SCENARIOS === */', '/* === END DEPLOYMENT SCENARIOS === */'
if A in t:
    t = t[:t.index(A)] + new + t[t.index(B) + len(B):]
else:
    t = t.rstrip('\n') + '\n' + new + '\n'
open(css, 'w', encoding='utf-8', newline='').write(t)
print('css ok')
