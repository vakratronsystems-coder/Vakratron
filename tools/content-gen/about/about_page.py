"""About page (Oct 2026 rewrite). Firm-centred: no individual names, photos or titles.
Run from tools/content-gen/about/."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'dr'))
sys.path.insert(0, os.path.join(HERE, '..', 'cloud'))
from tpl import page, crumb
from blueprint import SVG, CAPTION
from cloud_pages import sec, table

def card(title, text, href=None, label=None):
    lab = '<span class="vk-label"><span>' + label + '</span></span>' if label else ''
    if href:
        return '<a class="vk-card" href="' + href + '">' + lab + '<h3>' + title + '</h3><p class="vk-muted">' + text + '</p><span class="vk-go">Open &rarr;</span></a>'
    return '<div class="vk-card">' + lab + '<h3>' + title + '</h3><p class="vk-muted">' + text + '</p></div>'

def checklist(items, kind):
    mark = '&#10003;' if kind == 'do' else '&#10005;'
    return '<ul class="vk-dd vk-dd-' + kind + '">' + ''.join('<li><span class="mk" aria-hidden="true">' + mark + '</span><span>' + i + '</span></li>' for i in items) + '</ul>'

DO = [
    'Start from your workloads, data and constraints, and size from those.',
    'Compare at least two realistic options, with cost and risk for each.',
    'Write every sizing and cost assumption down, so your team can check it.',
    'Test failover, restores and load before handover, and share the results.',
    'Hand over documents and runbooks your own team can maintain.',
]
DONT = [
    'Recommend Kubernetes, fine-tuning or a second data centre when you do not need it.',
    'Tie a design to one vendor without showing you the alternative.',
    'Quote performance or recovery numbers we have not tested.',
    'Leave you with a platform only we can operate.',
    'Use your name, data or project in our marketing without written approval.',
]

ENGAGE = [
    ['<strong>Architecture review</strong>', 'You have a design, a vendor proposal or a running platform and want an independent view.', 'A findings report: risks, gaps, what to fix first, and what can wait.'],
    ['<strong>Design and sizing</strong>', 'You are planning something new: a GPU cluster, private cloud, DR site or AI platform.', 'HLD, LLD, sizing workings and a bill of quantities you can take to vendors.'],
    ['<strong>Tender and RFP support</strong>', 'You are a government or PSU buyer writing a specification, or evaluating bids.', 'A vendor-neutral specification, evaluation criteria and a technical comparison of responses.'],
    ['<strong>Build and migration oversight</strong>', 'The design is approved and a system integrator is building it.', 'Stage-by-stage checks, migration waves with a way back, and test sign-off.'],
    ['<strong>DR readiness and testing</strong>', 'You have DR on paper but have not proved it recently.', 'A planned DR drill, measured recovery times, and a short list of fixes.'],
]

PROOF = [
    ('DR patterns, side by side', 'Five recovery patterns with reference architectures and a simulator showing what happens when the primary site fails.', '/portfolio/dr-solutions'),
    ('GPU cluster sizing', 'A calculator that turns model size and users into GPUs, power and rack space, with the workings shown.', '/portfolio/ai-gpu-cloud#gpucalc'),
    ('VMware exit planning', 'How a VMware estate moves to KVM in waves, and what each wave depends on.', '/solutions/cloud/vmware-to-kvm-migration'),
    ('Private RAG architecture', 'How a document assistant is built so people only see answers from documents they are allowed to read.', '/solutions/rag/rag-architecture'),
    ('Do we need Kubernetes?', 'A short checker that gives an honest answer, including when the answer is no.', '/portfolio/kubernetes-platform#k8scheck'),
    ('Worked scenarios', 'Problem, design, architecture and results for common requirements, written end to end.', '/use_cases/dr-hospital-group'),
]

SECTORS = [
    ('Government and PSU', 'Specifications, evaluation support and data residency inside India.'),
    ('Banking and insurance', 'DR to regulator expectations, private AI on sensitive documents.'),
    ('Healthcare', 'Recovery tiers for clinical systems, records kept on-premises.'),
    ('Manufacturing and energy', 'Plant and head-office systems, hybrid cloud, site resilience.'),
    ('Education and research', 'Shared GPU capacity, fair scheduling between teams.'),
    ('AI product companies', 'Right-sizing GPU spend, moving from API to self-hosted when it pays.'),
]

FACTS = [
    ['Legal name', 'Vakratron Systems LLP'],
    ['Entity type', 'Limited Liability Partnership, incorporated 18 August 2020'],
    ['Startup recognition', 'DPIIT-recognised startup, certificate no. DIPP247647'],
    ['MSME registration', 'Udyam-registered micro enterprise, UDYAM-DL-07-0001129'],
    ['Enquiries', '<a href="mailto:connect@vakratronsys.com">connect@vakratronsys.com</a>'],
]

LEAD = 'Vakratron Systems designs data centre, disaster recovery, cloud, GPU and AI platforms for enterprises and government buyers. We are not tied to a vendor, we put our assumptions on paper, and we stay with a design until it is running and tested.'
FACTS_TOP = [('Founded', '2020'), ('Solution areas', '8'), ('Approach', 'Vendor-neutral'), ('Recognition', 'DPIIT startup')]
facts_html = '<div class="vk-facts">' + ''.join('<div class="vk-fact"><span class="k">' + k + '</span><span class="v">' + v + '</span></div>' for k, v in FACTS_TOP) + '</div>'

body = '''
        <div class="vk-wrap vk-hero vk-ahero">
            ''' + crumb(('Home', '/'), ('About', None)) + '''
            <div class="vk-ahero-grid">
                <div>
                    <span class="vk-eyebrow">About Vakratron</span>
                    <h1>An infrastructure design firm that writes its reasoning down</h1>
                    <p class="vk-lead">''' + LEAD + '''</p>
                    <div class="vk-actions"><a class="vk-btn primary" href="/contact">Talk to us</a><a class="vk-btn" href="/solutions">See what we do</a></div>
                </div>
                <figure class="vk-bpfig">''' + SVG + CAPTION + '''</figure>
            </div>
            ''' + facts_html + '''
        </div>'''

body += sec('''
            <span class="vk-eyebrow">Why we exist</span>
            <h2>Most designs reach you through someone selling the hardware</h2>
            <p>That is not a criticism of vendors or integrators. It is simply how the market works: the people who design an infrastructure platform are often the same people who supply it, so the design leans towards what they sell.</p>
            <p>The result is familiar. GPU clusters sized for a brochure rather than a workload. DR sites that have never been failed over. Private clouds with licence costs nobody modelled. Kubernetes where a few virtual machines would have done the job.</p>
            <p>Vakratron sits on your side of the table. Our job is the design and whether it works for you: the right size, the right cost, and something your own team can run after we step back.</p>''', prose=True)

body += sec('''
            <span class="vk-eyebrow">What you can hold us to</span>
            <h2>What we do, and what we will not do</h2>
            <div class="vk-two" style="margin-top:22px">
                <div class="vk-card"><h3>We will</h3>''' + checklist(DO, 'do') + '''</div>
                <div class="vk-card"><h3>We will not</h3>''' + checklist(DONT, 'dont') + '''</div>
            </div>''')

body += sec('''
            <span class="vk-eyebrow">Who you will work with</span>
            <h2>One senior architect, from first call to handover</h2>
            <p>Every engagement is led by a senior architect who stays with it throughout. They run the workshops, own the design and are the person you call when something does not add up. You meet them on the first call. Their background and relevant experience are shared with you directly once an NDA is in place.</p>
            <p>Where a piece of work needs a specialist, for example facility power and cooling or a particular vendor platform, we tell you who is doing that part and in what role. You will never find an unknown subcontractor on your project.</p>''', prose=True)

body += sec('''
            <span class="vk-eyebrow">Judge the work, not the brochure</span>
            <h2>How we think is already on this site</h2>
            <p class="vk-prose vk-muted">You do not have to take our word for anything. Most of our method is published here, open to anyone, with no sign-up.</p>
            <div class="vk-grid" style="margin-top:18px">''' + ''.join(card(t, d, h) for t, d, h in PROOF) + '''</div>''')

body += sec('''
            <span class="vk-eyebrow">Ways to work with us</span>
            <h2>Engagements, and what you get from each</h2>
            ''' + table(['Engagement', 'When it fits', 'What you get'], ENGAGE))

body += sec('''
            <span class="vk-eyebrow">Who we work with</span>
            <h2>Sectors where getting infrastructure wrong is expensive</h2>
            <div class="vk-grid" style="margin-top:18px">''' + ''.join(card(t, d) for t, d in SECTORS) + '''</div>''')

body += sec('''
            <span class="vk-eyebrow">Company facts</span>
            <h2>Registered, recognised, and easy to verify</h2>
            ''' + table(['', ''], FACTS).replace('<thead><tr><th></th><th></th></tr></thead>', '') + '''
            <p class="vk-muted" style="margin-top:14px">Certificates and registration documents are on our <a href="/credentials">company documents</a> page. Procurement declarations for a specific tender are provided on request.</p>''')

body += '''
        <div class="vk-sec"><div class="vk-wrap">
            <div class="vk-cta">
                <h2>Have a design you want a second opinion on?</h2>
                <p class="vk-muted">Send us a vendor proposal, an existing HLD or just a few lines about what you are planning. We will come back with a plain first view: what looks right, what we would question, and what we would test.</p>
                <div class="vk-actions">
                    <a class="vk-btn primary" href="/contact">Talk to us</a>
                    <a class="vk-btn" href="/solutions">Explore solutions</a>
                </div>
            </div>
        </div></div>'''

page('about.html', 'About Vakratron Systems | Vendor-neutral infrastructure design',
     'Vakratron Systems LLP designs data centre, DR, cloud, GPU and AI platforms for enterprises and government buyers. Vendor-neutral, assumptions written down, tested before handover.',
     body)
