"""Home page (Oct 2026 rewrite). Run from tools/content-gen/home/.
Keeps the existing chat widget (HTML, CSS and script extracted from the old page) with plain-language copy."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
VIEWS = os.path.join(HERE, '..', '..', '..', 'views')

def rd(n): return open(os.path.join(HERE, n), encoding='utf-8').read()

chat_css = rd('chat.css')
chat_html = rd('chat.html')
chat_js = rd('chat.js.html')
for a, b in [
    ('System Online. Greetings from Vakratron Systems Core Infrastructure Pipeline. How can I assist you with accelerated compute tables, hypervisor failovers, or high-density cloud blueprints today?',
     'Hi, I am Vakratron\'s assistant. Ask me about GPU sizing, private cloud, VMware migration, disaster recovery or AI. To talk to our team, just type "connect".'),
    ('placeholder="Input prompt token..."', 'placeholder="Ask a question..."'),
    ('<h3><span></span> Vakratron Core AI</h3>', '<h3><span></span> Ask Vakratron</h3>'),
    ('title="Query AI Architecture"', 'title="Ask a question"'),
    ('<!-- 🦾 ULTRA-ISOLATED STATIC VAKRATRON AI INFRASTRUCTURE TRIGGER (REPLACED) -->', '<!-- Chat assistant -->'),
    ('<!-- 🦾 VAKRATRON CHAT WINDOW WINDOW -->', ''),
]:
    chat_html = chat_html.replace(a, b)
for a, b in [
    ('"⚡ System Action: Redirecting token matrix to the Sovereign Advisory Desk..."', '"Taking you to our contact page..."'),
    ('"Execution Defect: Unable to pipeline calculated tokens from LLM core."', '"Sorry, I could not get an answer just now. Please try again, or use the contact page."'),
    ('"Network Fault: Endpoint connectivity degraded or blocked."', '"I cannot reach the server right now. Please try again in a moment."'),
]:
    chat_js = chat_js.replace(a, b)

# ------------------------------------------------------------------ hero stack visual
LAYERS = [
    ('AI applications', 'LLMs, answers from documents, agents', [('Enterprise LLM', '/portfolio/enterprise-llm'), ('RAG', '/portfolio/rag-solutions'), ('Agents', '/portfolio/agentic-ai')]),
    ('Application platform', 'Containers, APIs, delivery', [('Kubernetes', '/portfolio/kubernetes-platform'), ('APIs', '/portfolio/api-microservices')]),
    ('Cloud platform', 'Private, public and hybrid', [('Private cloud', '/solutions/cloud/private-cloud-openstack'), ('Hybrid', '/solutions/cloud/hybrid-cloud'), ('VMware exit', '/solutions/cloud/vmware-to-kvm-migration')]),
    ('Compute and network', 'GPU clusters, fabric, storage', [('GPU clusters', '/portfolio/ai-gpu-cloud'), ('Fabric', '/solutions/ai-infra/ai-network-fabric'), ('Storage', '/solutions/ai-infra/ai-storage')]),
    ('Data centre', 'Power, cooling, racks', [('Power and cooling', '/solutions/ai-infra/power-and-cooling')]),
]
def stack():
    rows = ''
    for i, (t, s, links) in enumerate(LAYERS):
        chips = ''.join(f'<a href="{h}">{n}</a>' for n, h in links)
        rows += f'<div class="vk-layer" style="--d:{(len(LAYERS) - 1 - i) * 0.55:.2f}s"><div class="lt"><span class="t">{t}</span><span class="s">{s}</span></div><div class="lc">{chips}</div></div>'
    return f'''<div class="vk-stack" aria-label="The layers we design, from data centre to AI applications">
                <div class="vk-stack-layers">{rows}</div>
                <a class="vk-stack-side" href="/portfolio/dr-solutions"><span>Disaster recovery across every layer</span></a>
            </div>'''

PROBLEMS = [
    ('&ldquo;Our VMware renewal quote is several times last year\'s.&rdquo;', 'A safe, wave-by-wave move to KVM, with a way back at every step.', '/solutions/cloud/vmware-to-kvm-migration'),
    ('&ldquo;The GPUs are ordered, but our data centre cannot power them.&rdquo;', 'Power, cooling and rack planning before the servers arrive.', '/solutions/ai-infra/power-and-cooling'),
    ('&ldquo;We have a DR site. We have never actually failed over.&rdquo;', 'DR that is designed per application and tested with your team.', '/portfolio/dr-solutions'),
    ('&ldquo;Staff are pasting customer data into public AI tools.&rdquo;', 'An approved, private way to use LLMs, with guardrails.', '/portfolio/enterprise-llm'),
    ('&ldquo;We need a tender specification that survives technical evaluation.&rdquo;', 'Requirements turned into clear, vendor-neutral specifications and BoQs.', '#government'),
    ('&ldquo;Everyone says we need Kubernetes. Do we?&rdquo;', 'An honest check, and sometimes an honest no.', '/portfolio/kubernetes-platform#k8scheck'),
]
SOLUTIONS = [
    ('fa-solid fa-microchip', 'AI infrastructure and GPU clusters', 'Size and build GPU clusters for training and inference, including fabric, storage, power and cooling.', '/portfolio/ai-gpu-cloud'),
    ('fa-solid fa-cloud', 'Cloud and VMware exit', 'Private, public and hybrid cloud, and a safe move off VMware to KVM.', '/portfolio/cloud-solutions'),
    ('fa-solid fa-shield-halved', 'Disaster recovery', 'Recovery targets per application, the right DR pattern, and real failover tests.', '/portfolio/dr-solutions'),
    ('fa-solid fa-brain', 'Enterprise LLM', 'Choose, host and govern language models where your data rules allow.', '/portfolio/enterprise-llm'),
    ('fa-solid fa-database', 'Answers from your documents (RAG)', 'Questions answered from your own documents, with sources and permissions.', '/portfolio/rag-solutions'),
    ('fa-solid fa-robot', 'AI agents and MCP', 'Agents that do routine work through your systems, with limits and approvals.', '/portfolio/agentic-ai'),
    ('fa-solid fa-cubes', 'Kubernetes and platforms', 'An honest fit check, then a lean platform your team can run.', '/portfolio/kubernetes-platform'),
    ('fa-solid fa-network-wired', 'APIs and integration', 'Clear, secure APIs and services that stay understandable as they grow.', '/portfolio/api-microservices'),
]
TOOLS = [
    ('DR pattern simulator', 'Watch five DR patterns recover from a site failure.', '/portfolio/dr-solutions#see-it-work'),
    ('GPU sizing calculator', 'GPUs, servers and power for a model size.', '/portfolio/ai-gpu-cloud#gpucalc'),
    ('Training failure simulation', 'What a node failure costs a training job.', '/solutions/ai-infra/gpu-training-cluster'),
    ('Where should this workload run?', 'Private, public or hybrid, with reasons.', '/portfolio/cloud-solutions#placer'),
    ('VMware to KVM waves', 'A migration with a failed test and rollback.', '/solutions/cloud/vmware-to-kvm-migration'),
    ('Private vs public cost', 'Five-year cost with your own numbers.', '/solutions/cloud/cloud-cost'),
    ('API or self-hosted LLM cost', 'Monthly cost and break-even volume.', '/portfolio/enterprise-llm#llmcost'),
    ('Ask your documents', 'Same question, different answers by role.', '/portfolio/rag-solutions#ragflow'),
    ('IT service desk agent', 'An agent that is blocked and asks for approval.', '/portfolio/agentic-ai#agentloop'),
    ('Do we need Kubernetes?', 'Five questions, honest answer.', '/portfolio/kubernetes-platform#k8scheck'),
    ('GitOps in action', 'Release, server failure and drift correction.', '/solutions/k8s/gitops-delivery'),
    ('Gateway and circuit breaker', 'Rate limits and failing fast.', '/portfolio/api-microservices#apisim'),
]
USECASES = [
    ('Hospital group DR', 'Tiered recovery for HIS, lab and imaging.', '/use_cases/dr-hospital-group'),
    ('Leaving VMware', '300 VMs to OpenStack in six waves.', '/use_cases/cloud-vmware-exit'),
    ('Private LLM on 32 GPUs', 'Sizing inference and fine-tuning for 2,000 staff.', '/use_cases/private-llm-gpu-platform'),
    ('HR policy assistant', 'Answers in English and Hindi, with permissions.', '/use_cases/hr-policy-assistant'),
    ('IT service desk agent', 'From shadow mode to approved actions.', '/use_cases/it-service-desk-agent'),
    ('Festive-season scale', '30 services onto Kubernetes before the sale.', '/use_cases/k8s-festive-scale'),
]

def body():
    problems = ''.join(f'<a class="vk-card vk-prob" href="{h}"><p class="q">{q}</p><p class="a">{a}</p><span class="vk-go">See how we approach it &rarr;</span></a>' for q, a, h in PROBLEMS)
    sols = ''.join(f'<a class="vk-card vk-sol" href="{h}"><span class="ic"><i class="{i}"></i></span><h3>{t}</h3><p>{d}</p><span class="vk-go">Explore &rarr;</span></a>' for i, t, d, h in SOLUTIONS)
    tools = ''.join(f'<a class="vk-tool-link" href="{h}"><span class="t">{t}</span><span class="d">{d}</span></a>' for t, d, h in TOOLS)
    ucs = ''.join(f'<a class="vk-card" href="{h}"><span class="vk-label"><span>Illustrative scenario</span></span><h3>{t}</h3><p>{d}</p><span class="vk-go">Read &rarr;</span></a>' for t, d, h in USECASES)
    return f'''
        <div class="vk-wrap vk-hero vk-home-hero">
            <div class="vk-home-grid">
                <div>
                    <span class="vk-eyebrow">AI infrastructure, cloud and data-centre consulting</span>
                    <h1>Infrastructure decisions you will not have to undo</h1>
                    <p class="vk-lead">We help government bodies, PSUs and enterprises in India plan and build GPU infrastructure, private and hybrid cloud, and disaster recovery. We start from your workloads and constraints, explain the trade-offs in plain language, and design systems your own team can run.</p>
                    <div class="vk-actions">
                        <a class="vk-btn primary" href="/contact">Book a consultation</a>
                        <a class="vk-btn" href="/solutions">Explore our solutions</a>
                    </div>
                </div>
                {stack()}
            </div>
        </div>

        <div class="vk-wrap">
            <div class="vk-proof">
                <div><span class="v">13+ years</span><span class="k">designing enterprise and government infrastructure</span></div>
                <div><span class="v">8 areas</span><span class="k">from data centre to AI, designed by one team</span></div>
                <div><span class="v">Vendor-neutral</span><span class="k">designs compare options, not just one product</span></div>
                <div><a href="/credentials"><span class="v">DPIIT-recognised</span><span class="k">startup, and Udyam-registered MSME</span></a></div>
            </div>
        </div>

        <div class="vk-sec"><div class="vk-wrap">
            <span class="vk-eyebrow">Sound familiar?</span>
            <h2>What people usually come to us with</h2>
            <div class="vk-grid vk-probs" style="margin-top:22px">{problems}</div>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <span class="vk-eyebrow">What we do</span>
            <h2>Eight solution areas, one joined-up design</h2>
            <p class="vk-prose">GPU clusters need the right data centre. Private clouds need disaster recovery. AI assistants need the right model and the right documents. We design these together, so the parts fit.</p>
            <div class="vk-sols">{sols}</div>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <span class="vk-eyebrow">Try them now, no sign-up</span>
            <h2>Interactive tools and simulations</h2>
            <p class="vk-prose">Most consulting websites describe. Ours lets you try: size a GPU cluster, compare cloud costs with your own numbers, watch a disaster recovery or a VMware migration play out, or see how an AI agent is kept within limits.</p>
            <div class="vk-tools">{tools}</div>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap"><div class="vk-prose">
            <span class="vk-eyebrow">How we work</span>
            <h2>Four steps, with something you can use at each one</h2>
        </div>
            <div class="vk-phases">
                <div class="vk-phase"><span class="n">1</span><h3>Assess</h3><p>Your workloads, current platform, data centre and constraints, in a few focused workshops.</p><p class="g"><strong>You get:</strong> a plain findings report and the options worth considering.</p></div>
                <div class="vk-phase"><span class="n">2</span><h3>Design</h3><p>Architecture, sizing and cost, with the assumptions written down so your team can check them.</p><p class="g"><strong>You get:</strong> design document, bill of materials and cost model.</p></div>
                <div class="vk-phase"><span class="n">3</span><h3>Build</h3><p>Built from code, tested for failure, and migrated in stages with a way back.</p><p class="g"><strong>You get:</strong> a working platform and test results.</p></div>
                <div class="vk-phase"><span class="n">4</span><h3>Run</h3><p>Monitoring, runbooks and an upgrade routine, handed over to your team.</p><p class="g"><strong>You get:</strong> runbooks, training, and support if you want it.</p></div>
            </div>
        </div></div>

        <div class="vk-sec" id="government"><div class="vk-wrap">
            <div class="vk-two">
                <div>
                    <span class="vk-eyebrow">For government and PSU buyers</span>
                    <h2>Specifications that hold up in evaluation, and in production</h2>
                    <p>Public procurement needs technical documents that are complete, fair to more than one vendor, and defensible when questioned. We help departments and PSUs turn what they need into specifications that work.</p>
                </div>
                <div>
                    <ul>
                        <li>Requirements gathered from users and turned into clear technical specifications</li>
                        <li>Vendor-neutral sizing, bill of quantities and bill of materials</li>
                        <li>Technical compliance sheets and evaluation criteria</li>
                        <li>Support with pre-bid queries and technical evaluation</li>
                        <li>Review of designs and acceptance tests after award</li>
                    </ul>
                    <a class="vk-btn primary" href="/contact">Discuss a requirement</a>
                </div>
            </div>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <span class="vk-eyebrow">How we think</span>
            <h2>What you can expect from us</h2>
            <div class="vk-grid" style="margin-top:22px">
                <div class="vk-card"><h3>Workload first</h3><p class="vk-muted">We start from what you need to run, not from a product we want to sell.</p></div>
                <div class="vk-card"><h3>An honest no</h3><p class="vk-muted">If you do not need Kubernetes, fine-tuning or a second data centre, we will say so.</p></div>
                <div class="vk-card"><h3>Tested, not assumed</h3><p class="vk-muted">Failover, restores and load are tested before handover, with results you can see.</p></div>
                <div class="vk-card"><h3>Yours to run</h3><p class="vk-muted">Plain documents and runbooks your own team can maintain after we leave.</p></div>
            </div>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <span class="vk-eyebrow">Examples</span>
            <h2>How we approach real problems</h2>
            <p class="vk-prose vk-muted">These are illustrative scenarios built from common requirements, not specific client engagements. They show how we think a problem through, step by step.</p>
            <div class="vk-grid" style="margin-top:18px">{ucs}</div>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <div class="vk-cta">
                <h2>Tell us what you are planning</h2>
                <p class="vk-muted">A GPU cluster, a cloud move, a DR review, an AI pilot or a tender specification. Send us a few lines about it, and we will come back with a plain first view of the options.</p>
                <div class="vk-actions">
                    <a class="vk-btn primary" href="/contact">Book a consultation</a>
                    <a class="vk-btn" href="/solutions">Explore our solutions</a>
                </div>
            </div>
        </div></div>'''


HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vakratron Systems | AI Infrastructure, Cloud and Disaster Recovery Consulting</title>
    <meta name="description" content="Vakratron Systems helps government bodies, PSUs and enterprises in India plan and build GPU infrastructure, private and hybrid cloud, VMware exits, disaster recovery and enterprise AI, in plain language.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://vakratronsys.com/">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://vakratronsys.com/">
    <meta property="og:title" content="Vakratron Systems | AI Infrastructure, Cloud and DR Consulting">
    <meta property="og:description" content="GPU clusters, private and hybrid cloud, VMware exit, disaster recovery and enterprise AI, designed for government and enterprise in India.">
    <meta property="og:image" content="https://vakratronsys.com/images/hero.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="/style.css">
    <link rel="stylesheet" href="/vk-content.css">
    <style>
/* Chat assistant (kept from the previous home page) */
'''

def build():
    html = HEAD + chat_css + '''    </style>
</head>
<body class="home">
    <header></header>

    <main class="vk">''' + body() + '''
    </main>

    ''' + chat_html + '''
    <footer></footer>

    ''' + chat_js + '''    <script src="/vakra-loader.js"></script>
</body>
</html>
'''
    open(os.path.join(VIEWS, 'index.html'), 'w', encoding='utf-8', newline='\n').write(html)
    print('wrote index.html', len(html))

CSS = """
/* ---------- Home page ---------- */
main.vk .vk-home-hero { padding-top: 40px; padding-bottom: 36px; }
main.vk .vk-home-grid { display: grid; grid-template-columns: 1.05fr 1fr; gap: 48px; align-items: center; }
main.vk .vk-home-hero h1 { font-size: clamp(2.2rem, 4.6vw, 3.4rem) !important; }
main.vk .vk-stack { display: grid; grid-template-columns: 1fr 54px; gap: 10px; }
main.vk .vk-stack-layers { display: grid; gap: 8px; }
main.vk .vk-layer { position: relative; display: grid; grid-template-columns: 1fr auto; gap: 10px; align-items: center; background: #0a1020; border: 1px solid #334155; border-radius: 12px; padding: 12px 14px; overflow: hidden; animation: vkLayerGlow 2.75s ease-in-out infinite; animation-delay: var(--d); }
main.vk .vk-layer::before { content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 3px; background: #C2185B; opacity: .35; animation: vkLayerBar 2.75s ease-in-out infinite; animation-delay: var(--d); }
main.vk .vk-layer .lt { display: grid; }
main.vk .vk-layer .t { font-weight: 600 !important; color: #fff !important; font-size: 0.98rem !important; }
main.vk .vk-layer .s { font-size: 0.8rem !important; color: #94a3b8 !important; }
main.vk .vk-layer .lc { display: flex; flex-wrap: wrap; gap: 6px; justify-content: flex-end; }
main.vk .vk-layer .lc a { font-size: 0.76rem !important; color: #cbd5e1 !important; border: 1px solid #334155; border-radius: 999px; padding: 3px 10px; text-decoration: none !important; white-space: nowrap; }
main.vk .vk-layer .lc a:hover { border-color: #C2185B; color: #fff !important; }
main.vk a.vk-stack-side { writing-mode: vertical-rl; transform: rotate(180deg); display: flex; align-items: center; justify-content: center; border: 1px dashed rgba(56, 189, 248, 0.5); border-radius: 12px; background: rgba(56, 189, 248, 0.06); text-decoration: none !important; }
main.vk a.vk-stack-side span { font-size: 0.8rem !important; color: #7dd3fc !important; letter-spacing: 0.04em !important; font-weight: 600 !important; }
main.vk a.vk-stack-side:hover { background: rgba(56, 189, 248, 0.14); }
@keyframes vkLayerGlow { 0%, 60%, 100% { border-color: #334155; box-shadow: none; } 20% { border-color: rgba(194, 24, 91, 0.7); box-shadow: 0 0 22px rgba(194, 24, 91, 0.18); } }
@keyframes vkLayerBar { 0%, 60%, 100% { opacity: .35; } 20% { opacity: 1; } }
main.vk .vk-proof { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1px; background: var(--vk-line); border: 1px solid var(--vk-line); border-radius: 14px; overflow: hidden; margin-bottom: 8px; }
main.vk .vk-proof > div { background: #070d1c; padding: 18px 20px; }
main.vk .vk-proof .v { display: block; font-size: 1.3rem !important; font-weight: 700 !important; color: #fff !important; }
main.vk .vk-proof .k { display: block; font-size: 0.85rem !important; color: #94a3b8 !important; line-height: 1.45 !important; }
main.vk .vk-proof a { text-decoration: none !important; }
main.vk .vk-probs { grid-template-columns: repeat(3, 1fr); }
main.vk a.vk-prob .q { color: #fff !important; font-size: 1.05rem !important; font-weight: 500 !important; line-height: 1.5 !important; margin-bottom: 10px; }
main.vk a.vk-prob .a { color: #94a3b8 !important; font-size: 0.92rem !important; }
main.vk .vk-sols { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-top: 22px; }
main.vk a.vk-sol { display: flex; flex-direction: column; }
main.vk a.vk-sol .ic { width: 42px; height: 42px; border-radius: 10px; display: inline-flex; align-items: center; justify-content: center; background: rgba(194, 24, 91, 0.1); border: 1px solid rgba(194, 24, 91, 0.3); margin-bottom: 14px; }
main.vk a.vk-sol .ic i { color: #f472b6; font-size: 1.05rem; }
main.vk a.vk-sol p { font-size: 0.9rem !important; flex: 1; }
main.vk .vk-tools { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 22px; }
main.vk a.vk-tool-link { display: grid; gap: 4px; padding: 14px 16px; border: 1px solid var(--vk-line); border-radius: 10px; background: var(--vk-surface); text-decoration: none !important; position: relative; transition: border-color .2s, transform .2s; }
main.vk a.vk-tool-link::after { content: "\\25B6"; position: absolute; right: 14px; top: 14px; font-size: 0.7rem; color: #C2185B; }
main.vk a.vk-tool-link:hover { border-color: rgba(194, 24, 91, 0.55); transform: translateY(-2px); }
main.vk a.vk-tool-link .t { color: #fff !important; font-weight: 600 !important; font-size: 0.95rem !important; padding-right: 18px; }
main.vk a.vk-tool-link .d { color: #94a3b8 !important; font-size: 0.83rem !important; line-height: 1.45 !important; }
main.vk .vk-phases { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-top: 8px; }
main.vk .vk-phase { position: relative; background: var(--vk-surface); border: 1px solid var(--vk-line); border-radius: 12px; padding: 20px; }
main.vk .vk-phase .n { display: inline-flex; width: 32px; height: 32px; border-radius: 50%; align-items: center; justify-content: center; background: var(--vk-accent); color: #fff !important; font-weight: 700 !important; margin-bottom: 10px; }
main.vk .vk-phase p { font-size: 0.9rem !important; }
main.vk .vk-phase p.g { color: #cbd5e1 !important; border-top: 1px solid var(--vk-line); padding-top: 10px; margin-top: 10px; }
main.vk #government .vk-btn { margin-top: 8px; }
@media (prefers-reduced-motion: reduce) { main.vk .vk-layer, main.vk .vk-layer::before { animation: none; } }
@media (max-width: 1000px) {
  main.vk .vk-home-grid { grid-template-columns: 1fr; gap: 28px; }
  main.vk .vk-sols, main.vk .vk-tools { grid-template-columns: repeat(2, 1fr); }
  main.vk .vk-phases { grid-template-columns: repeat(2, 1fr); }
  main.vk .vk-probs { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 640px) {
  main.vk .vk-proof { grid-template-columns: 1fr 1fr; }
  main.vk .vk-sols, main.vk .vk-tools, main.vk .vk-phases, main.vk .vk-probs { grid-template-columns: 1fr; }
  main.vk .vk-stack { grid-template-columns: 1fr 40px; }
  main.vk .vk-layer { grid-template-columns: 1fr; }
  main.vk .vk-layer .lc { justify-content: flex-start; }
}
"""

if __name__ == '__main__':
    build()
