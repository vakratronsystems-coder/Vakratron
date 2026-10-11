"""Build all reference-deployment pages and the /deployment-scenarios hub.
Run from tools/content-gen/deployments/."""
import os, sys, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from scenario import build
from hub import build_hub

GROUPS = [
    ('Cloud and data centre', 'Moving, consolidating and running infrastructure', [
        's_cloud_repatriation', 's_hybrid_retail', 's_dc_consolidation', 's_db_consolidation', 's_edge_central']),
    ('Resilience and security', 'Recovery, ransomware and security operations', [
        's_core_banking_dr', 's_draas', 's_ransomware_vault', 's_soc_dc_dr']),
    ('AI infrastructure', 'GPU platforms built for real workloads', [
        's_airgapped_ai', 's_shared_gpu_research']),
    ('AI in business processes', 'Agents, LLMs and machine learning in production', [
        's_agentic_ap', 's_llm_gateway', 's_contact_centre_ai', 's_mlops']),
]

groups = []
for title, sub, mods in GROUPS:
    items = []
    for m in mods:
        s = importlib.import_module(m).S
        s['_group'] = title
        items.append(s)
    groups.append((title, sub, items))
allsc = [s for _, _, items in groups for s in items]

for s in allsc:
    same = [o for o in allsc if o['_group'] == s['_group'] and o['slug'] != s['slug']]
    rest = [o for o in allsc if o['_group'] != s['_group']]
    build(s, (same + rest)[:3])

build_hub(groups)

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
print('built', len(allsc), 'pages + hub; css ok')
