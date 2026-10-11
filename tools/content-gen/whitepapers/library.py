"""/whitepapers library page (new design) and a build-all for the web pages.
Run from tools/content-gen/whitepapers/: python3 library.py"""
import os, sys, importlib, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'dr'))
from tpl import page, crumb

ORDER = ['wp_dcdr', 'wp_cloud', 'wp_gpu', 'wp_llm', 'wp_rag_agents', 'wp_k8s', 'wp_api']
ICONS = {'wp_dcdr': 'fa-shield-halved', 'wp_cloud': 'fa-cloud', 'wp_gpu': 'fa-microchip', 'wp_llm': 'fa-brain',
         'wp_rag_agents': 'fa-robot', 'wp_k8s': 'fa-cubes', 'wp_api': 'fa-plug'}

def build_web_pages():
    for m in ORDER:
        r = subprocess.run([sys.executable, os.path.join(HERE, 'wp_render.py'), m], cwd=HERE, capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr[-400:])

def card(m, M):
    n = sum(len(i) for _, i in M.CHECKLIST)
    return ('<a class="vk-card wp-libcard" href="/whitepapers/' + M.META['slug'] + '">'
            '<span class="wp-libic"><i class="fa-solid ' + ICONS[m] + '"></i></span>'
            '<span class="vk-eyebrow">' + M.META['area'] + '</span>'
            '<h3>' + M.META['title'] + '</h3>'
            '<p class="vk-muted">' + M.META['subtitle'] + '.</p>'
            '<div class="vk-hubchips"><span>' + str(M.META['minutes']) + ' min read</span><span>' + M.META['pages'].replace('Approx. ', '') + ' PDF</span><span>' + str(n) + '-point checklist</span></div>'
            '<span class="vk-go">Read online or download &rarr;</span></a>')

def build_library():
    mods = [(m, importlib.import_module(m)) for m in ORDER]
    total = sum(sum(len(i) for _, i in M.CHECKLIST) for _, M in mods)
    body = '''
        <div class="vk-wrap vk-hero">
            ''' + crumb(('Home', '/'), ('Whitepapers', None)) + '''
            <span class="vk-eyebrow">Resources</span>
            <h1>Whitepapers you can take into the meeting</h1>
            <p class="vk-lead">Seven practical guides for CIOs, IT heads and architects. Each one explains the options in plain English, shows the sizing and cost arithmetic, sets out a reference architecture and a roadmap, and ends with a readiness checklist you can use the next morning. Read them online, or download the PDF to share with your team.</p>
            <div class="vk-facts">
                <div class="vk-fact"><span class="k">Whitepapers</span><span class="v">''' + str(len(mods)) + '''</span></div>
                <div class="vk-fact"><span class="k">Checklist points</span><span class="v">''' + str(total) + '''</span></div>
                <div class="vk-fact"><span class="k">Reading</span><span class="v">Free, online</span></div>
                <div class="vk-fact"><span class="k">PDF</span><span class="v">After email check</span></div>
            </div>
        </div>
        <div class="vk-sec"><div class="vk-wrap">
            <div class="vk-grid wp-libgrid">''' + ''.join(card(m, M) for m, M in mods) + '''</div>
        </div></div>
        <div class="vk-sec"><div class="vk-wrap">
            <span class="vk-eyebrow">More ways to go deeper</span>
            <h2>Beyond the whitepapers</h2>
            <div class="vk-grid" style="margin-top:18px">
                <a class="vk-card" href="/deployment-scenarios"><h3>Deployment scenarios</h3><p class="vk-muted">Fifteen worked designs, from core banking DR to an AI agent for accounts payable, with architecture, sizing and delivery plans.</p><span class="vk-go">See the scenarios &rarr;</span></a>
                <a class="vk-card" href="/#tools"><h3>Interactive tools</h3><p class="vk-muted">GPU sizing, DR pattern simulator, VMware wave planner, LLM cost calculator and more. No sign-up.</p><span class="vk-go">Try the tools &rarr;</span></a>
                <a class="vk-card" href="/advisory"><h3>Talk it through</h3><p class="vk-muted">A short, fixed-scope review or workshop when a decision is coming up and you want an independent view.</p><span class="vk-go">Ways to work with us &rarr;</span></a>
            </div>
        </div></div>
        <div class="vk-sec"><div class="vk-wrap">
            <div class="vk-cta">
                <h2>Working on one of these right now?</h2>
                <p class="vk-muted">Tell us what you are deciding and by when. We will come back within one working day with a plain first view.</p>
                <div class="vk-actions"><a class="vk-btn primary" href="/contact">Talk to us</a><a class="vk-btn" href="/solutions">Explore solutions</a></div>
            </div>
        </div></div>'''
    page('whitepapers.html', 'Whitepapers | Practical guides to cloud, DR, GPU and AI infrastructure | Vakratron',
         'Free practical whitepapers on disaster recovery, private cloud, GPU infrastructure, enterprise LLMs, RAG and AI agents, Kubernetes and APIs, each with a readiness checklist.',
         body)

if __name__ == '__main__':
    build_web_pages()
    build_library()
