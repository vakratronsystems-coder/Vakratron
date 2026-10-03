"""Enterprise LLM, RAG and Agentic AI pages (Oct 2026 rewrite). Run from tools/content-gen/genai/."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'dr'))
sys.path.insert(0, os.path.join(HERE, '..', 'cloud'))
from tpl import page, crumb
from cloud_pages import N, F, sec, hero, table, ul, steps, figure

HOME = ("Home", "/")
SCRIPTS = ['/vk-genai-tools.js']

def cta(title, text, btn, back_href, back_label):
    return f'''
        <div class="vk-sec"><div class="vk-wrap">
            <div class="vk-cta">
                <h2>{title}</h2>
                <p class="vk-muted">{text}</p>
                <div class="vk-actions">
                    <a class="vk-btn primary" href="/contact">{btn}</a>
                    <a class="vk-btn" href="{back_href}">{back_label}</a>
                </div>
            </div>
        </div></div>'''

def pills(base, pages, cur):
    return '<div class="vk-pills">' + ''.join(f'<a class="vk-pill{" on" if s == cur else ""}" href="{base}/{s}">{n}</a>' for s, n in pages) + '</div>'

def more_links(label, base, pages, cur, extra):
    links = ' &middot; '.join(f'<a href="{base}/{s}">{n}</a>' for s, n in pages if s != cur)
    return sec(f'<p class="vk-small"><strong>{label}</strong> {links} &middot; {extra}</p>')

def ghero(hub, base, pages, slug, eyebrow, title, lead, facts, crumbname):
    b = hero((HOME, hub, (crumbname, None)), eyebrow, title, lead, facts=facts)
    return b.replace(f'<span class="vk-eyebrow">{eyebrow}</span>', pills(base, pages, slug) + f'<span class="vk-eyebrow">{eyebrow}</span>', 1)

def faqblock(qa):
    return ''.join(f'<details><summary>{q}</summary><div>{a}</div></details>' for q, a in qa)

def cards(items):
    return '<div class="vk-grid" style="margin-top:22px">' + ''.join(f'<a class="vk-card" href="{h}"><h3>{t}</h3><p>{d}</p><span class="vk-go">{g} &rarr;</span></a>' for h, t, d, g in items) + '</div>'

def uc_hero(hubc, name, h1, lead, facts):
    f = ''.join(f'<div class="vk-fact"><span class="k">{k}</span><span class="v">{v}</span></div>' for k, v in facts)
    return f'''
        <div class="vk-wrap vk-hero">
            {crumb(HOME, hubc, (name, None))}
            <div class="vk-label"><span>Illustrative scenario</span></div>
            <h1>{h1}</h1>
            <p class="vk-lead">{lead}</p>
            <div class="vk-note"><p class="vk-small">This is a composite example built from common enterprise requirements. It is not a specific client engagement, and the figures are design targets for the scenario, not measured results.</p></div>
            <div class="vk-facts">{f}</div>
        </div>'''

# =====================================================================================
# ENTERPRISE LLM
# =====================================================================================
LHUB = ("Enterprise LLM", "/portfolio/enterprise-llm")
LB = '/solutions/llm'
LP = [('model-selection', 'Choosing a model'), ('private-llm-hosting', 'Private hosting'), ('fine-tuning', 'Fine-tuning'), ('llm-governance', 'Governance and LLMOps')]
LCTA = cta('Starting with LLMs, or stuck after a pilot?', 'Tell us the task you want AI to help with and any rules about where your data can go. We will come back with a plain recommendation: which kind of model, where to run it, roughly what it costs, and how to know if it is working.', 'Book an LLM review', '/portfolio/enterprise-llm', 'Back to enterprise LLM')
def lmore(cur): return more_links('More LLM guides:', LB, LP, cur, '<a href="/solutions/llm/faq">LLM FAQ</a> &middot; <a href="/use_cases/llm-claims-summarisation">Use case: claims summaries</a>')

def llm_hub():
    b = hero((HOME, ("Solutions", "/solutions"), ("Enterprise LLM", None)), 'Enterprise LLM', 'Large language models your business can actually trust',
             'Most organisations already use AI chatbots, often on personal accounts and with company data. The question is not whether to use LLMs, but how: which model, where it runs, what data it may see, and how you know the answers are good enough. We help you decide, then build it.',
             actions=[('Book an LLM review', '/contact'), ('API or self-hosted: compare cost', '#llmcost')])
    b += sec('''<span class="vk-eyebrow">What usually goes wrong</span><h2>Why LLM projects stall</h2>
            <div class="vk-grid" style="margin-top:22px">
                <div class="vk-card"><h3>Staff paste data into public tools</h3><p class="vk-muted">Without an approved option, people use whatever is free. Customer data and internal documents leave the company without anyone deciding they should.</p></div>
                <div class="vk-card"><h3>The pilot impressed, production did not</h3><p class="vk-muted">A demo on ten hand-picked questions looks great. Real users ask messier questions, and nobody measured quality before go-live.</p></div>
                <div class="vk-card"><h3>The bill arrived</h3><p class="vk-muted">Usage grew, every request sent long documents to an expensive model, and monthly API cost became a board-level question.</p></div>
                <div class="vk-card"><h3>Fine-tuning that did not help</h3><p class="vk-muted">Months went into fine-tuning a model to "know" company facts, when the real need was to look them up. See <a href="/solutions/llm/fine-tuning">when fine-tuning helps</a>.</p></div>
            </div>''')
    b += sec('<span class="vk-eyebrow">Your options</span><h2>Three ways to use an LLM</h2>' + table(['Option', 'What it means', 'Good for', 'Watch out for'],
        [['Public AI service', 'Calling a commercial model over the internet', 'Fast start, strongest models, no infrastructure', 'Where data goes, contract terms, cost at high volume'],
         ['Private cloud endpoint', 'The same commercial models deployed in your own cloud account and region', 'Data stays in your cloud tenancy, enterprise contracts', 'Which models are available in which region; still per-token pricing'],
         ['<a href="/solutions/llm/private-llm-hosting">Self-hosted open model</a>', 'An open-weight model running on your own GPUs', 'Strict data rules, steady high volume, full control over versions', 'You run the GPUs and the model platform; open models may trail the best commercial ones']]) +
        '<p class="vk-small vk-muted">Many organisations use more than one: a self-hosted model for sensitive data, and a commercial API for everything else, behind one gateway.</p>')
    b += sec('''<span class="vk-eyebrow">Try it</span><h2>Hosted API or self-hosted: what will it cost?</h2>
            <p class="vk-prose">Enter your expected usage. The calculator compares a month of API charges with the cost of running an open model on your own GPUs, and checks whether those GPUs can keep up at the busiest hour.</p>
            <div class="vk-tool vk-llmcost"></div><noscript><p class="vk-muted">This calculator needs JavaScript.</p></noscript>''', sid='llmcost')
    b += sec('<span class="vk-eyebrow">Go deeper</span><h2>Guides and examples</h2>' + cards([
        ('/solutions/llm/model-selection', 'Choosing a model', 'Open or commercial, large or small, and how to test models on your own tasks.', 'Read the guide'),
        ('/solutions/llm/private-llm-hosting', 'Private hosting', 'Running open models inside your network: gateway, guardrails, model servers.', 'Read the guide'),
        ('/solutions/llm/fine-tuning', 'Fine-tuning', 'When it helps, when retrieval is the better answer, and what data you need.', 'Read the guide'),
        ('/solutions/llm/llm-governance', 'Governance and LLMOps', 'Evaluation, guardrails, logging, access and data protection.', 'Read the guide'),
        ('/use_cases/llm-claims-summarisation', 'Use case: claims summaries', 'An illustrative scenario: an insurer summarising claim files with a private model.', 'Read the use case'),
        ('/solutions/llm/faq', 'LLM questions, answered', 'Data safety, cost, Indian languages, hallucinations and more.', 'Read the FAQ')]) +
        '<p class="vk-small" style="margin-top:18px">Related: <a href="/portfolio/rag-solutions">RAG</a> to answer from your own documents, <a href="/portfolio/agentic-ai">agentic AI</a> to take actions, and <a href="/portfolio/ai-gpu-cloud">GPU infrastructure</a> to run it all. Full reference: <a href="/solutions/master_entll">LLM whitepaper</a>.</p>')
    b += sec('<span class="vk-eyebrow">How we work</span><h2>How an LLM engagement runs</h2>' + steps([
        '<strong>Pick one task.</strong> A specific job with a clear owner, such as summarising claim files or drafting replies. Not "use AI everywhere".',
        '<strong>Build a test set.</strong> 100 to 300 real examples with good answers, agreed with the people who do the work today.',
        '<strong>Compare options.</strong> Two or three models, hosted and self-hosted, scored on the test set for quality, speed and cost.',
        '<strong>Build with guardrails.</strong> Gateway, access control, logging and data masking from day one.',
        '<strong>Pilot with real users.</strong> Measure quality and time saved against the baseline, and fix what users report.',
        '<strong>Run it.</strong> Monitoring, regular re-testing, and a process for changing models safely.']), prose=True)
    b += LCTA
    page('portfolio/enterprise-llm.html', 'Enterprise LLM: Choosing, Hosting and Governing Large Language Models | Vakratron Systems',
         'Plain guidance on using LLMs in the enterprise: public API, private endpoint or self-hosted model, an API vs self-hosted cost calculator, model selection, fine-tuning and governance.', b, scripts=SCRIPTS)

def llm_selection():
    b = ghero(LHUB, LB, LP, 'model-selection', 'LLM guide', 'Choosing a model',
              'There is no single best model. The right one is the cheapest model that does your task well enough, on infrastructure your data rules allow. The only reliable way to find it is to test candidates on your own examples.',
              [('Start from', 'Your task, not a leaderboard'), ('Test on', '100-300 real examples'), ('Compare', 'Quality, speed, cost'), ('Revisit', 'Every few months')], 'Choosing a model')
    b += sec('<h2>The main choices</h2>' + table(['Question', 'Options', 'How to decide'],
        [['Commercial or open-weight?', 'Commercial models via API; open models (Llama, Mistral, Qwen and others) you can run yourself', 'Data rules and volume first. Open models are good enough for many enterprise tasks today.'],
         ['How big?', 'Small (around 8B parameters), medium (around 70B), very large', 'Use the smallest that passes your test set. Small models are far cheaper and faster.'],
         ['General or specialised?', 'General chat models, code models, embedding models for search', 'Use specialised models where they exist, especially for search embeddings.'],
         ['Which languages?', 'English-first models, multilingual models', 'If users write in Hindi or other Indian languages, test that explicitly. Quality varies a lot.'],
         ['Licence', 'Apache 2.0 and similar, or custom community licences', 'Read the licence. Some restrict use above a user count or in certain products.']]))
    b += sec('<h2>How we test models</h2>' + steps([
        '<strong>Collect real examples.</strong> Questions or documents from the actual workflow, with the answers a good employee would give.',
        '<strong>Define what good means.</strong> Correct facts, right format, right tone, says "I don\'t know" when it should.',
        '<strong>Run each candidate.</strong> Same prompts, same examples, recorded outputs.',
        '<strong>Score.</strong> Automatic checks where possible, plus review by the people who do the work.',
        '<strong>Weigh cost and speed.</strong> A model 3% better but 10 times more expensive is rarely the right choice.']) +
        '<p>Keep the test set. When a new model version arrives, you can re-run it in an afternoon and decide with evidence.</p>', prose=True)
    b += sec('<h2>Common mistakes</h2>' + ul([
        '<strong>Choosing from public leaderboards.</strong> General benchmarks say little about your documents and your users.',
        '<strong>Testing only on easy examples.</strong> Include the messy, ambiguous and edge cases. That is where models differ.',
        '<strong>Locking in one model forever.</strong> Put a gateway in front so the model behind it can change without changing every application.']), prose=True)
    b += lmore('model-selection') + LCTA
    page('solutions/llm/model-selection.html', 'Choosing an LLM: Open vs Commercial, Size, Languages and Testing | Vakratron Systems',
         'How to choose a large language model for an enterprise task: open vs commercial, model size, Indian languages, licences, and a practical way to test models on your own examples.', b)

def llm_hosting():
    d = dict(panels=('Your applications and controls', 'LLM platform (inside your network)'), rows=4, nodes={
        'users': N('G', title='Staff and systems', sub='chat, documents, business apps', style='global', x=370, w=220),
        'apps': N('P', 0, title='Assistants and applications', sub='call the LLM through one API'),
        'siem': N('P', 1, title='Audit logs and security monitoring', sub='who asked what, and when'),
        'idp': N('P', 2, title='Identity provider', sub='groups decide who may use which model'),
        'docs': N('P', 3, title='Approved data sources', sub='used through RAG, not training'),
        'gw': N('D', 0, title='LLM gateway', sub='sign-in, quotas, routing, logging'),
        'gr': N('D', 1, title='Guardrails', sub='mask personal data, filter content'),
        'ms': N('D', 2, title='Model servers', sub='open models on your GPUs'),
        'reg': N('D', 3, title='Model registry and test results', sub='only approved versions are served'),
    }, flows=[F('users', 'P', 'traffic'), F('apps', 'gw', 'stream', 1), F('gw', 'gr', 'stream', 2), F('gr', 'ms', 'stream', 3), F('gr', 'siem', 'hb', 4), F('reg', 'ms', 'batch', 5)])
    b = ghero(LHUB, LB, LP, 'private-llm-hosting', 'LLM guide', 'Private LLM hosting',
              'Running an open model inside your own network means prompts, documents and answers never leave infrastructure you control. It also means you run the platform. Here is what a sound private LLM platform includes beyond the model itself.',
              [('Data', 'Stays in your network'), ('Model servers', 'vLLM, Triton'), ('Must have', 'Gateway, guardrails, logs'), ('Can be', 'Fully air-gapped')], 'Private hosting')
    b += sec('<span class="vk-eyebrow">Reference architecture</span><h2>How the pieces fit together</h2>' + figure(d, 'Private LLM hosting reference architecture',
        'Every request passes through the gateway and guardrails before it reaches a model, and every request is logged.',
        [('1', 'One entry point', 'Applications never call a model directly. They call the gateway, which checks who is asking and how much they may use.'),
         ('2', 'Guardrails', 'Personal data such as Aadhaar or account numbers can be masked before the model sees it, and harmful content filtered on the way out.'),
         ('3', 'Model servers', 'Open models served on your GPUs. See the <a href="/solutions/ai-infra/gpu-inference-platform">inference platform guide</a> for sizing.'),
         ('4', 'Audit trail', 'Requests and decisions are logged to your security monitoring, so you can answer "who asked what" later.'),
         ('5', 'Approved models only', 'A new model or version is served only after it passes your test set.')]))
    b += sec('<h2>Air-gapped deployments</h2>' + ul([
        'Models, container images and updates are brought in through a controlled, scanned transfer process.',
        'No component needs internet access at runtime: no telemetry, no licence checks against external servers.',
        'Plan how updates reach the platform before it is built. Air-gapped systems that cannot be updated become insecure.']) +
        '<p>Air-gapping suits defence, some government and some financial workloads. For most organisations, a private network with strict outbound rules is enough.</p>', prose=True)
    b += sec('<h2>Typical tools</h2>' + table(['Layer', 'Common choices'],
        [['Model servers', 'vLLM, NVIDIA Triton with TensorRT-LLM, Text Generation Inference'],
         ['Gateway', 'LiteLLM or an API gateway with LLM routing, quotas and logging'],
         ['Guardrails', 'Microsoft Presidio for personal data, NVIDIA NeMo Guardrails, custom rules'],
         ['Platform', 'Kubernetes with NVIDIA GPU Operator'], ['Observability', 'Prometheus, Grafana, Langfuse or OpenTelemetry traces']]))
    b += lmore('private-llm-hosting') + LCTA
    page('solutions/llm/private-llm-hosting.html', 'Private LLM Hosting: Gateway, Guardrails, Model Servers, Air-Gapped Options | Vakratron Systems',
         'How to run open LLMs inside your own network: reference architecture with gateway, guardrails, model servers, registry and audit logging, plus air-gapped deployment.', b)

def llm_finetune():
    b = ghero(LHUB, LB, LP, 'fine-tuning', 'LLM guide', 'Fine-tuning: when it helps, and when it does not',
              'Fine-tuning changes how a model behaves. It is good at teaching style, format and specialised tasks. It is poor at teaching facts that change, such as policies, prices or product details. Most enterprise projects need retrieval first, and fine-tuning only sometimes.',
              [('First try', 'Better prompts'), ('For your facts', 'RAG'), ('For style and format', 'Fine-tuning'), ('Usual method', 'LoRA')], 'Fine-tuning')
    b += sec('<h2>Which approach fits your problem?</h2>' + table(['The problem', 'Try first', 'Why'],
        [['The model does not know our policies or products', '<a href="/portfolio/rag-solutions">RAG</a>', 'Facts change. Looking them up at question time keeps answers current and shows sources.'],
         ['Answers are in the wrong format or tone', 'Better prompts and examples, then fine-tuning', 'A few good examples in the prompt often fix it. Fine-tune if it still drifts.'],
         ['A narrow, repeated task (classify, extract, route)', 'Fine-tune a small model', 'A small fine-tuned model can match a large general one at a fraction of the cost.'],
         ['Specialised language (legal, medical, internal jargon)', 'RAG plus a glossary, then fine-tuning if needed', 'Fine-tuning helps the model use terms naturally once retrieval supplies the facts.']]))
    b += sec('<h2>What fine-tuning takes</h2>' + ul([
        '<strong>Data:</strong> hundreds to a few thousand high-quality examples of input and ideal output. Quality matters far more than quantity.',
        '<strong>Method:</strong> usually LoRA, which trains a small set of extra weights instead of the whole model. Cheaper, faster and easier to roll back.',
        '<strong>Compute:</strong> LoRA on a 70B-class model fits on one 8-GPU server; on an 8B model, a single GPU can be enough. See the <a href="/portfolio/ai-gpu-cloud#gpucalc">GPU calculator</a>.',
        '<strong>Evaluation:</strong> the same test set used for model selection, so you can prove the fine-tuned model is actually better.',
        '<strong>Maintenance:</strong> when the base model is updated, the fine-tuning usually has to be repeated.']), prose=True)
    b += lmore('fine-tuning') + LCTA
    page('solutions/llm/fine-tuning.html', 'LLM Fine-Tuning: When It Helps, When to Use RAG Instead | Vakratron Systems',
         'When fine-tuning an LLM is worth it and when retrieval (RAG) or better prompting is the right answer, plus what fine-tuning takes: data, LoRA, compute and evaluation.', b)

def llm_gov():
    b = ghero(LHUB, LB, LP, 'llm-governance', 'LLM guide', 'Governance and LLMOps',
              'Once an LLM is in use, someone has to answer simple questions: who can use it, what data it sees, how good its answers are this month, and what happens when a model changes. Governance is the set of controls that makes those answers easy.',
              [('Measure', 'Quality, monthly'), ('Control', 'Access by group'), ('Protect', 'Personal data'), ('Record', 'Every request')], 'Governance and LLMOps')
    b += sec('<h2>The controls we put in place</h2>' + table(['Area', 'What it means in practice'],
        [['Access', 'Use is tied to company sign-in. Groups decide which models and data each team may use.'],
         ['Data protection', 'Personal data is masked where it is not needed. Retention of prompts and answers follows your policy and, in India, the Digital Personal Data Protection Act, 2023.'],
         ['Quality', 'A test set is re-run on every model or prompt change, and a sample of live answers is reviewed every month.'],
         ['Safety', 'Filters for harmful content, and defences against prompt injection, which is the top risk in the OWASP Top 10 for LLM applications.'],
         ['Audit', 'Who asked what, which model answered, and what sources were used, kept for an agreed period.'],
         ['Cost', 'Usage and cost per team, with quotas and alerts.'],
         ['Change', 'New models and prompts go through test, approval and gradual rollout, with a quick way back.']]))
    b += sec('<h2>Measuring quality without guesswork</h2>' + ul([
        '<strong>Offline:</strong> the test set, scored automatically and by reviewers, before every change.',
        '<strong>Online:</strong> thumbs up or down from users, plus a small weekly sample reviewed by experts.',
        '<strong>Drift:</strong> watch for falling scores or rising complaints after model, prompt or data changes.']), prose=True)
    b += sec('<h2>Typical tools</h2>' + table(['Area', 'Common choices'],
        [['Tracing and evaluation', 'Langfuse, OpenTelemetry, Ragas for retrieval quality'], ['Personal data', 'Microsoft Presidio, custom rules for Indian identifiers'],
         ['Guardrails', 'NVIDIA NeMo Guardrails, gateway policies'], ['Cost and usage', 'Gateway metrics with Prometheus and Grafana']]))
    b += lmore('llm-governance') + LCTA
    page('solutions/llm/llm-governance.html', 'LLM Governance and LLMOps: Access, Data Protection, Quality, Audit | Vakratron Systems',
         'Practical LLM governance: access by group, personal-data masking, DPDP Act considerations, quality testing, prompt-injection defences, audit trails, cost control and safe model changes.', b)

def llm_faq():
    qa = [('Is it safe to use ChatGPT-style tools with company data?', '<p>It depends on the service and contract. Consumer tools may keep or use data in ways you have not agreed to. Enterprise offerings and private deployments give you control over retention and location. Give staff an approved option, or they will use unapproved ones.</p>'),
          ('Will an LLM make things up?', '<p>Yes, sometimes. Grounding answers in your documents with RAG, asking for sources, and allowing "I don\'t know" reduce it a lot. For important decisions, a person should check the output.</p>'),
          ('Do open models work in Hindi and other Indian languages?', '<p>Some do well, some do not, and quality varies by language and task. Test with real examples from your users before choosing.</p>'),
          ('Hosted API or our own GPUs?', '<p>Hosted APIs are usually cheaper at low and medium volume and give the strongest models. Self-hosting makes sense for strict data rules or steady high volume. Use the <a href="/portfolio/enterprise-llm#llmcost">cost calculator</a> with your numbers.</p>'),
          ('Do we need to fine-tune a model on our data?', '<p>Usually not at first. To answer from your documents, use RAG. Fine-tune later for format, style or narrow repeated tasks. See <a href="/solutions/llm/fine-tuning">fine-tuning</a>.</p>'),
          ('How long does a first production use case take?', '<p>Typically eight to twelve weeks: test set and model comparison, a guarded build, and a pilot with real users. The test set is the step most often skipped, and the one that matters most.</p>')]
    b = hero((HOME, LHUB, ("FAQ", None)), 'LLM guide', 'LLM questions, answered', 'Short answers to the questions business and IT leaders ask us most often about large language models.')
    b += sec(faqblock(qa), prose=True) + lmore('faq') + LCTA
    page('solutions/llm/faq.html', 'Enterprise LLM FAQ: Data Safety, Hallucinations, Indian Languages, Cost | Vakratron Systems',
         'Plain answers on enterprise LLMs: using company data safely, hallucinations, Indian languages, hosted API vs own GPUs, fine-tuning and time to production.', b)

def llm_uc():
    b = uc_hero(LHUB, 'Use case: claims summaries', 'Summarising claim files with a private LLM',
                'How we would approach an insurer that wants claims handlers to spend less time reading and more time deciding, without sending health and personal data outside its own network.',
                [('Organisation', 'Mid-size general insurer'), ('Task', 'Summarise claim files'), ('Model', '70B-class open model'), ('Hosting', 'Private, on own GPUs')])
    b += sec('''<span class="vk-eyebrow">The situation</span><h2>Long files, short on time</h2>
            <p>Each health or motor claim arrives with 30 to 80 pages: forms, hospital bills, discharge summaries, surveyor reports and emails. Handlers spend much of their day reading before they can decide. The company wanted a one-page summary for each file, with the key facts and anything unusual flagged. Health and identity data could not leave its own infrastructure.</p>''', prose=True)
    b += sec('<span class="vk-eyebrow">The approach</span><h2>What we would do</h2>' + steps([
        '<strong>Define the summary with handlers.</strong> Ten fields every summary must contain, and the red flags they look for.',
        '<strong>Build a test set.</strong> 200 past claims, anonymised, with summaries written by senior handlers.',
        '<strong>Compare three open models</strong> at two sizes, scored by handlers on accuracy, missing facts and usefulness.',
        '<strong>Choose the smallest model that passes.</strong> In this scenario, a 70B-class model at 8-bit, served on the insurer\'s own GPUs.',
        '<strong>No fine-tuning at first.</strong> A clear prompt with two worked examples met the bar. Fine-tuning stays an option if format drifts.',
        '<strong>Guardrails.</strong> Personal identifiers masked in logs, every summary linked to its source pages, and the handler always makes the decision.']), prose=True)
    b += sec('<span class="vk-eyebrow">What changes</span><h2>Targets and how they are checked</h2>' + table(['Measure', 'Before', 'Target', 'Checked by'],
        [['Reading time per claim', 'About 25 minutes', 'About 10 minutes', 'Time study on a sample of claims'],
         ['Summary accuracy', 'Not applicable', '95% of key facts correct', 'Weekly review of 5% of summaries'],
         ['Data leaving the network', 'Not applicable', 'None', 'Network controls and audit logs']]))
    b += sec('<span class="vk-eyebrow">Trade-offs</span><h2>What we would flag</h2>' + ul([
        '<strong>Scanned documents.</strong> Poor scans need good OCR first, or the model summarises garbage.',
        '<strong>Handlers must still read the flagged pages.</strong> The summary speeds up reading; it does not replace judgement.',
        '<strong>The test set needs owners.</strong> Someone in claims must keep it current as products and rules change.']), prose=True)
    b += LCTA
    page('use_cases/llm-claims-summarisation.html', 'Use Case: Claim File Summaries with a Private LLM | Vakratron Systems',
         'An illustrative scenario: an insurer summarising long claim files with a privately hosted open LLM, including model testing, guardrails, targets and trade-offs.', b)


# =====================================================================================
# RAG
# =====================================================================================
RHUB = ("RAG", "/portfolio/rag-solutions")
RB = '/solutions/rag'
RP = [('rag-architecture', 'How RAG is built'), ('document-ingestion', 'Preparing documents'), ('retrieval-quality', 'Better retrieval'), ('access-control', 'Permissions'), ('rag-evaluation', 'Measuring answers')]
RCTA = cta('Want answers from your own documents?', 'Tell us where the documents live, who should be able to ask, and ten questions people ask today. We will come back with a plain view of what it takes to answer them well, and safely.', 'Book a RAG review', '/portfolio/rag-solutions', 'Back to RAG')
def rmore(cur): return more_links('More RAG guides:', RB, RP, cur, '<a href="/solutions/rag/faq">RAG FAQ</a> &middot; <a href="/use_cases/hr-policy-assistant">Use case: HR policy assistant</a>')

def rag_hub():
    b = hero((HOME, ("Solutions", "/solutions"), ("RAG", None)), 'Retrieval-augmented generation (RAG)', 'Answers from your documents, with sources, for the right people',
             'An LLM on its own does not know your policies, products or procedures. RAG fixes that: before answering, the system looks up the relevant passages in your documents and gives them to the model, which answers from them and shows where the answer came from. Done well, it is the most useful thing most organisations can build with AI.',
             actions=[('Book a RAG review', '/contact'), ('See how it works', '#ragflow')])
    b += sec('''<span class="vk-eyebrow">See it working</span><h2>Ask a question, and watch what happens</h2>
            <p class="vk-prose">Choose who is asking and a question. Watch the system search, remove documents the user is not allowed to see, prefer current documents over archived ones, and answer with sources. Then ask the salary question as an employee and as an HR manager.</p>
            <div class="vk-tool vk-ragflow"></div><noscript><p class="vk-muted">This demonstration needs JavaScript.</p></noscript>
            <p class="vk-small vk-muted">Demonstration data only.</p>''', sid='ragflow')
    b += sec('''<span class="vk-eyebrow">What usually goes wrong</span><h2>Why document chatbots disappoint</h2>
            <div class="vk-grid" style="margin-top:22px">
                <div class="vk-card"><h3>Wrong or outdated answers</h3><p class="vk-muted">Old versions of a policy sit next to new ones, and the system cannot tell which is current.</p></div>
                <div class="vk-card"><h3>Confidential documents leak</h3><p class="vk-muted">Everything was indexed together, so anyone can get answers drawn from HR or board documents.</p></div>
                <div class="vk-card"><h3>Tables and scans are lost</h3><p class="vk-muted">PDF tables, scanned forms and slides were converted badly, so the facts in them are never found.</p></div>
                <div class="vk-card"><h3>Nobody knows if it is good</h3><p class="vk-muted">There is no test set, so every change is judged by whoever tried a few questions that day.</p></div>
            </div>''')
    b += sec('<span class="vk-eyebrow">Go deeper</span><h2>Guides and examples</h2>' + cards([
        ('/solutions/rag/rag-architecture', 'How RAG is built', 'The two pipelines: preparing documents, and answering questions.', 'Read the guide'),
        ('/solutions/rag/document-ingestion', 'Preparing documents', 'Parsing PDFs, tables and scans, splitting into passages, keeping versions current.', 'Read the guide'),
        ('/solutions/rag/retrieval-quality', 'Better retrieval', 'Hybrid search, reranking and the choices that decide answer quality.', 'Read the guide'),
        ('/solutions/rag/access-control', 'Permissions', 'Making sure people only get answers from documents they are allowed to read.', 'Read the guide'),
        ('/solutions/rag/rag-evaluation', 'Measuring answers', 'Test sets, scores and how to know a change made things better.', 'Read the guide'),
        ('/use_cases/hr-policy-assistant', 'Use case: HR policy assistant', 'An illustrative scenario for 3,000 employees, in English and Hindi.', 'Read the use case'),
        ('/solutions/rag/faq', 'RAG questions, answered', 'Vector databases, accuracy, languages, cost and more.', 'Read the FAQ')]) +
        '<p class="vk-small" style="margin-top:18px">Related: <a href="/portfolio/enterprise-llm">enterprise LLM</a> for choosing and hosting the model, and <a href="/portfolio/agentic-ai">agentic AI</a> when answers should turn into actions.</p>')
    b += sec('<span class="vk-eyebrow">How we work</span><h2>How a RAG engagement runs</h2>' + steps([
        '<strong>Collect real questions.</strong> 100 to 200 questions people actually ask, with the right answers and source documents.',
        '<strong>Map the documents and their owners.</strong> Where they live, who may read them, which versions are current.',
        '<strong>Build ingestion carefully.</strong> Good parsing of PDFs, tables and scans, with permissions carried along.',
        '<strong>Tune retrieval against the test set.</strong> Chunking, hybrid search and reranking, measured, not guessed.',
        '<strong>Pilot with one department.</strong> Measure answer quality and deflected questions, and fix gaps in the documents themselves.',
        '<strong>Run it.</strong> Daily document sync, monthly quality checks and a clear owner for every source.']), prose=True)
    b += RCTA
    page('portfolio/rag-solutions.html', 'RAG Solutions: Answers from Your Documents, with Sources and Permissions | Vakratron Systems',
         'Retrieval-augmented generation explained in plain words, with an interactive demo: how answers are drawn from your documents with sources, respecting permissions and document versions.', b, scripts=SCRIPTS)

def rag_arch():
    d = dict(panels=('Preparing documents (runs continuously)', 'Answering a question'), rows=4, nodes={
        'src': N('P', 0, title='Document sources', sub='SharePoint, file shares, wikis, tickets'),
        'parse': N('P', 1, title='Parse and clean', sub='PDF, Word, tables, scans (OCR)'),
        'chunk': N('P', 2, title='Split and embed', sub='passages with title, date, permissions'),
        'idx': N('P', 3, title='Search index', sub='vector and keyword, with access lists'),
        'q': N('D', 0, title='Question', sub='plus who is asking'),
        'ret': N('D', 1, title='Retrieve', sub='hybrid search, filtered by permission'),
        'rr': N('D', 2, title='Rerank', sub='best and most current passages first'),
        'llm': N('D', 3, title='Answer', sub='LLM writes from the passages, with sources'),
        'user': N('G', title='Users', sub='ask in plain language', style='global', x=640, w=200),
    }, flows=[F('src', 'parse', 'stream', 1), F('parse', 'chunk', 'stream', 2), F('chunk', 'idx', 'stream', 3), F('user', 'D', 'traffic'), F('q', 'ret', 'stream'), F('idx', 'ret', 'bi', 4), F('ret', 'rr', 'stream', 5), F('rr', 'llm', 'stream', 6)])
    b = ghero(RHUB, RB, RP, 'rag-architecture', 'RAG guide', 'How RAG is built',
              'A RAG system is two pipelines. One prepares your documents so they can be searched. The other answers questions by searching those documents and passing the best passages to an LLM. Most quality problems start in the first pipeline, even though people notice them in the second.',
              [('Pipelines', 'Prepare, then answer'), ('Search', 'Vector plus keyword'), ('Answers', 'With sources'), ('Permissions', 'Checked at search time')], 'How RAG is built')
    b += sec('<span class="vk-eyebrow">Reference architecture</span><h2>The two pipelines</h2>' + figure(d, 'RAG reference architecture',
        'Left: documents are prepared continuously as they change. Right: each question is answered from the prepared index.',
        [('1', 'Collect', 'Connectors pull documents from where they live, with their permissions and last-modified dates.'),
         ('2', 'Parse', 'Text, tables and scanned pages are converted cleanly. This step decides more about quality than the choice of LLM.'),
         ('3', 'Split and embed', 'Documents are split into passages that keep their headings, and each passage gets an embedding for meaning-based search.'),
         ('4', 'Search', 'The question is matched by meaning and by keywords, and only passages the user may read are returned.'),
         ('5', 'Rerank', 'A second model reorders results by relevance, and current documents are preferred over archived ones.'),
         ('6', 'Answer', 'The LLM answers only from the passages it was given, cites them, and says when the answer is not there.')]))
    b += sec('<h2>Typical tools</h2>' + table(['Layer', 'Common choices'],
        [['Parsing', 'Unstructured, Docling, Apache Tika, OCR for scans'], ['Embeddings', 'Open multilingual embedding models (for example BGE or E5 families) or hosted embedding APIs'],
         ['Search index', 'OpenSearch or Elasticsearch, PostgreSQL with pgvector, Qdrant, Milvus'], ['Reranking', 'Cross-encoder rerankers'],
         ['Orchestration', 'LlamaIndex, LangChain or a small amount of custom code'], ['Model', 'See <a href="/portfolio/enterprise-llm">enterprise LLM</a>']]) +
        '<p class="vk-small vk-muted">If you already run OpenSearch, Elasticsearch or PostgreSQL, you probably do not need a separate vector database to start.</p>')
    b += rmore('rag-architecture') + RCTA
    page('solutions/rag/rag-architecture.html', 'RAG Architecture: Ingestion and Answering Pipelines Explained | Vakratron Systems',
         'How a retrieval-augmented generation system is built: document ingestion, parsing, chunking and embedding, hybrid search with permissions, reranking and grounded answers with sources.', b)

def rag_ingest():
    b = ghero(RHUB, RB, RP, 'document-ingestion', 'RAG guide', 'Preparing documents',
              'If a fact is mangled when a document is converted, no model can find it later. Document preparation is unglamorous and decides most of a RAG system\'s quality.',
              [('Hardest content', 'Tables and scans'), ('Keep', 'Headings and dates'), ('Remove', 'Old versions'), ('Sync', 'Daily or on change')], 'Preparing documents')
    b += sec('<h2>What makes documents hard</h2>' + table(['Content', 'Problem', 'What we do'],
        [['Tables in PDFs', 'Rows and columns get scrambled into a stream of numbers', 'Layout-aware parsing that keeps tables as tables'],
         ['Scanned forms', 'No text at all until OCR runs', 'OCR with quality checks; flag pages that cannot be read reliably'],
         ['Slides', 'Meaning is in layout and images', 'Extract text per slide and keep the slide title with it'],
         ['Many versions', 'Old and new policies contradict each other', 'Keep only current versions searchable, or mark versions clearly'],
         ['Long documents', 'A passage loses its context', 'Keep section headings with each passage']]))
    b += sec('<h2>Splitting into passages</h2>' + ul([
        '<strong>Split by structure, not by character count.</strong> Sections and paragraphs make better passages than fixed-size blocks.',
        '<strong>Keep passages a sensible size.</strong> Typically a few hundred words: big enough to carry meaning, small enough to be precise.',
        '<strong>Carry metadata.</strong> Document title, section, date, owner and permissions travel with every passage.']), prose=True)
    b += sec('<h2>Keeping it current</h2>' + ul([
        'Sync changed documents daily or as they change, and remove deleted ones from the index the same day.',
        'Give every source an owner who is told when their documents produce wrong answers.',
        'Often the fastest way to improve answers is to fix the documents themselves.']), prose=True)
    b += rmore('document-ingestion') + RCTA
    page('solutions/rag/document-ingestion.html', 'Preparing Documents for RAG: PDFs, Tables, Scans and Chunking | Vakratron Systems',
         'How to prepare documents for retrieval-augmented generation: parsing PDFs, tables, scans and slides, splitting into passages, metadata, versions and keeping the index current.', b)

def rag_retrieval():
    b = ghero(RHUB, RB, RP, 'retrieval-quality', 'RAG guide', 'Better retrieval',
              'If the right passage is not among the few sent to the model, the answer will be wrong or empty, however good the model is. Retrieval is where most of the tuning effort pays off.',
              [('Search', 'Hybrid: meaning plus keywords'), ('Then', 'Rerank'), ('Send to model', 'A few best passages'), ('Measure', 'Did the right passage come back?')], 'Better retrieval')
    b += sec('<h2>The choices that matter</h2>' + table(['Choice', 'What it does', 'Our usual default'],
        [['Hybrid search', 'Combines meaning-based (vector) search with keyword search', 'Always on. Keywords catch policy numbers, product codes and names that vector search misses.'],
         ['Reranking', 'A second model re-scores the top results for relevance', 'On for most use cases. Often the single biggest quality gain.'],
         ['Number of passages', 'How many passages the model sees', 'Start with 3 to 8, tuned on the test set'],
         ['Metadata filters', 'Restrict by department, date, document type or permission', 'Use whenever the question implies a scope'],
         ['Query rewriting', 'Turns a vague or follow-up question into a clear search', 'On for chat assistants with follow-up questions']]))
    b += sec('<h2>Languages</h2><p>For users who ask in Hindi or mix Hindi and English, use a multilingual embedding model and test with real questions. Keyword search on transliterated text needs extra care.</p>', prose=True)
    b += rmore('retrieval-quality') + RCTA
    page('solutions/rag/retrieval-quality.html', 'Improving RAG Retrieval: Hybrid Search, Reranking and Filters | Vakratron Systems',
         'How to improve retrieval in a RAG system: hybrid vector and keyword search, reranking, number of passages, metadata filters, query rewriting and multilingual search.', b)

def rag_access():
    b = ghero(RHUB, RB, RP, 'access-control', 'RAG guide', 'Permissions: the right answers for the right people',
              'A RAG system that ignores document permissions is a data leak with a chat interface. Anyone could ask about salaries, board decisions or customer data and get an answer. Permissions must be enforced before the model sees anything.',
              [('Check at', 'Search time'), ('Source of truth', 'Original document permissions'), ('Sync', 'With every change'), ('Test with', 'Real user roles')], 'Permissions')
    b += sec('<h2>How it works</h2>' + steps([
        'When a document is indexed, its access list (users and groups) is stored with every passage.',
        'When someone asks a question, the system knows who they are from company sign-in.',
        'Search only returns passages that person is allowed to read. Everything else is filtered out before the model is involved.',
        'When permissions change at the source, the index is updated too.']) +
        '<p>Try it in the <a href="/portfolio/rag-solutions#ragflow">interactive demo</a>: ask the salary question as an employee and as an HR manager.</p>', prose=True)
    b += sec('<h2>Mistakes to avoid</h2>' + ul([
        '<strong>Filtering after the model answers.</strong> Too late: the model has already seen the restricted text.',
        '<strong>One shared index for everything, with no access lists.</strong> Simple to build, unsafe to run.',
        '<strong>Forgetting removed access.</strong> When someone leaves a team, their access to its documents must disappear from the index too.',
        '<strong>Not testing with real roles.</strong> Test with accounts from different departments before go-live.']), prose=True)
    b += rmore('access-control') + RCTA
    page('solutions/rag/access-control.html', 'RAG Access Control: Enforcing Document Permissions | Vakratron Systems',
         'How to enforce document permissions in a RAG system so people only get answers from documents they may read: access lists in the index, filtering at search time, sync and testing.', b, scripts=[])

def rag_eval():
    b = ghero(RHUB, RB, RP, 'rag-evaluation', 'RAG guide', 'Measuring answers',
              'Without measurement, every change to a RAG system is a guess. A small, well-built test set turns quality into a number you can track and improve.',
              [('Test set', '100-200 real questions'), ('Check 1', 'Right passage found?'), ('Check 2', 'Answer faithful?'), ('Run', 'On every change')], 'Measuring answers')
    b += sec('<h2>What to measure</h2>' + table(['Measure', 'Question it answers', 'How'],
        [['Retrieval hit rate', 'Did the right passage come back at all?', 'Automatic, using the source marked in the test set'],
         ['Faithfulness', 'Does the answer stick to the passages, without inventing?', 'Automatic scoring plus expert review of a sample'],
         ['Correctness', 'Is the answer actually right?', 'Compared with the agreed answer'],
         ['Refusals', 'Does it say "I don\'t know" when the answer is not in the documents?', 'Include questions with no answer in the test set'],
         ['User feedback', 'Do people find it useful?', 'Thumbs up or down, plus comments']]))
    b += sec('<h2>Building the test set</h2>' + ul([
        'Collect real questions from help desks, email and chat, not invented ones.',
        'For each, record the right answer and the document it comes from.',
        'Include hard questions, questions with no answer, and questions that need permissions.',
        'Re-run it on every change to documents, prompts, models or search settings. Tools such as Ragas help automate scoring.']), prose=True)
    b += rmore('rag-evaluation') + RCTA
    page('solutions/rag/rag-evaluation.html', 'Evaluating RAG: Test Sets, Retrieval Hit Rate, Faithfulness | Vakratron Systems',
         'How to measure a RAG system: building a test set from real questions, retrieval hit rate, faithfulness, correctness, refusals and user feedback, re-run on every change.', b)

def rag_faq():
    qa = [('Do we need a vector database?', '<p>Not necessarily. OpenSearch, Elasticsearch and PostgreSQL with pgvector all support vector search. Start with what you run today; move to a dedicated vector database only if scale or features demand it.</p>'),
          ('How accurate will the answers be?', '<p>That depends mostly on document quality and retrieval, and it should be measured, not promised. With good documents and a tuned system, most answers to questions covered by the documents should be correct, and the rest should say they do not know.</p>'),
          ('Can it answer in Hindi?', '<p>Yes, with a multilingual embedding model and an LLM that handles Hindi well. Test with real questions from your users.</p>'),
          ('Will it show where answers come from?', '<p>It should. Every answer should cite the documents and sections it used, so users can check.</p>'),
          ('What does it cost to run?', '<p>Mostly the LLM usage and the search infrastructure. For a few thousand employees, running costs are usually modest compared with the time saved. The bigger cost is the initial work on documents and testing.</p>'),
          ('Can RAG take actions, like raising a ticket?', '<p>That is the next step: an agent that uses tools. See <a href="/portfolio/agentic-ai">agentic AI</a>.</p>')]
    b = hero((HOME, RHUB, ("FAQ", None)), 'RAG guide', 'RAG questions, answered', 'Short answers to the questions we hear most often about answering questions from company documents.')
    b += sec(faqblock(qa), prose=True) + rmore('faq') + RCTA
    page('solutions/rag/faq.html', 'RAG FAQ: Vector Databases, Accuracy, Hindi, Sources, Cost | Vakratron Systems',
         'Plain answers on retrieval-augmented generation: whether you need a vector database, accuracy, Hindi support, citing sources, running cost and taking actions.', b)

def rag_uc():
    b = uc_hero(RHUB, 'Use case: HR policy assistant', 'An HR policy assistant for 3,000 employees',
                'How we would build an assistant that answers HR and policy questions in English and Hindi, from current documents only, without exposing HR-only material.',
                [('Users', '~3,000 employees'), ('Languages', 'English and Hindi'), ('Sources', 'SharePoint and HR system'), ('Rule', 'Answer with sources, or say so')])
    b += sec('''<span class="vk-eyebrow">The situation</span><h2>The same questions, every day</h2>
            <p>The HR team answered hundreds of emails a month about leave, reimbursements, travel rules and benefits. Answers existed in policy documents, but there were several versions of many of them, some scanned, and some HR-only documents sat in the same folders as staff policies.</p>''', prose=True)
    b += sec('<span class="vk-eyebrow">The approach</span><h2>What we would do</h2>' + steps([
        '<strong>Collect 150 real questions</strong> from the HR mailbox, with the right answers marked by the HR team.',
        '<strong>Clean up sources with HR.</strong> Archive old versions, re-scan unreadable PDFs, and separate HR-only documents.',
        '<strong>Carry permissions into the index</strong> from Active Directory groups, so HR-only content is invisible to other staff.',
        '<strong>Hybrid search with reranking</strong> and a multilingual embedding model for Hindi questions.',
        '<strong>Answer only with sources.</strong> If nothing relevant is found, say so and point to the HR helpdesk.',
        '<strong>Pilot with two departments</strong>, then roll out company-wide.']), prose=True)
    b += sec('<span class="vk-eyebrow">What changes</span><h2>Targets and how they are checked</h2>' + table(['Measure', 'Target', 'Checked by'],
        [['Policy questions reaching the HR mailbox', 'Down by about half', 'Monthly mailbox volume by category'],
         ['Correct answers on the test set', '90% or better', 'Test set re-run on every change'],
         ['HR-only content shown to staff', 'Never', 'Permission tests with real accounts before each release']]))
    b += sec('<span class="vk-eyebrow">Trade-offs</span><h2>What we would flag</h2>' + ul([
        '<strong>Document owners are essential.</strong> When a policy changes, someone must update the source, or the assistant repeats the old rule.',
        '<strong>Some questions need a person.</strong> Personal cases and exceptions should be routed to HR, not answered by the assistant.',
        '<strong>Hindi quality needs its own testing.</strong> Include enough Hindi questions in the test set.']), prose=True)
    b += RCTA
    page('use_cases/hr-policy-assistant.html', 'Use Case: HR Policy Assistant with RAG for 3,000 Employees | Vakratron Systems',
         'An illustrative scenario: an HR policy assistant built with RAG, answering in English and Hindi from current documents with sources and strict permissions.', b)


# =====================================================================================
# AGENTIC AI
# =====================================================================================
AHUB = ("Agentic AI", "/portfolio/agentic-ai")
AB = '/solutions/agents'
AP = [('mcp-architecture', 'MCP architecture'), ('guardrails-and-approvals', 'Guardrails and approvals'), ('agent-operations', 'Running agents')]
ACTA = cta('Thinking about AI agents?', 'Tell us the process you would like to automate and the systems it touches. We will come back with a plain view of what an agent could safely do, what should stay with people, and how to start small.', 'Book an agent review', '/portfolio/agentic-ai', 'Back to agentic AI')
def amore(cur): return more_links('More agent guides:', AB, AP, cur, '<a href="/solutions/agents/faq">Agent FAQ</a> &middot; <a href="/use_cases/it-service-desk-agent">Use case: IT service desk agent</a>')

def ag_hub():
    b = hero((HOME, ("Solutions", "/solutions"), ("Agentic AI", None)), 'Agentic AI and MCP', 'AI agents that do real work, within clear limits',
             'An AI agent does not just answer. It plans steps, uses tools such as your ticketing, directory or ERP systems, and checks its own results. That makes it useful, and it also makes limits essential: what it may read, what it may change, and what a person must approve.',
             actions=[('Book an agent review', '/contact'), ('Watch an agent work', '#agentloop')])
    b += sec('''<span class="vk-eyebrow">See it working</span><h2>An IT service desk agent, step by step</h2>
            <p class="vk-prose">The agent fixes a VPN problem on its own, is blocked when it tries something outside its permissions, and stops to ask a manager before granting access to financial data. You decide whether the manager approves.</p>
            <div class="vk-tool vk-agentloop"></div><noscript><p class="vk-muted">This demonstration needs JavaScript.</p></noscript>''', sid='agentloop')
    b += sec('<span class="vk-eyebrow">Plain words</span><h2>Chatbot, assistant or agent?</h2>' + table(['', 'What it does', 'Example', 'Risk if it goes wrong'],
        [['Chatbot', 'Answers from what it knows', 'General questions', 'Wrong answer'],
         ['Assistant with RAG', 'Answers from your documents, with sources', 'Policy and product questions', 'Wrong answer, or a leak if permissions are ignored'],
         ['Agent with read-only tools', 'Looks things up in your systems to help', 'Checks order status, reads logs', 'Wrong conclusion'],
         ['Agent that can act', 'Changes things: creates tickets, resets accounts, updates records', 'Renews a certificate, raises a purchase request', 'A wrong change in a real system']]) +
        '<p>Most organisations should move down this table one step at a time, proving each level before adding the next.</p>')
    b += sec('<span class="vk-eyebrow">Go deeper</span><h2>Guides and examples</h2>' + cards([
        ('/solutions/agents/mcp-architecture', 'MCP architecture', 'How the Model Context Protocol connects agents to your systems, and how to design the servers.', 'Read the guide'),
        ('/solutions/agents/guardrails-and-approvals', 'Guardrails and approvals', 'Least privilege, human approval, prompt injection and audit.', 'Read the guide'),
        ('/solutions/agents/agent-operations', 'Running agents', 'Tracing, evaluation, cost and how to roll out safely.', 'Read the guide'),
        ('/use_cases/it-service-desk-agent', 'Use case: IT service desk agent', 'An illustrative scenario: from read-only helper to approved actions, in three phases.', 'Read the use case'),
        ('/solutions/agents/faq', 'Agent questions, answered', 'Autonomy, safety, cost and where agents work well today.', 'Read the FAQ')]) +
        '<p class="vk-small" style="margin-top:18px">Related: <a href="/portfolio/rag-solutions">RAG</a> for answering from documents, and <a href="/portfolio/enterprise-llm">enterprise LLM</a> for the model behind the agent. Full reference: <a href="/solutions/master_agentic">agentic AI whitepaper</a>.</p>')
    b += sec('<span class="vk-eyebrow">Where agents work today</span><h2>Good first candidates</h2>' + ul([
        '<strong>IT and HR service desks:</strong> triage, diagnosis, and routine fixes such as unlocks and certificate renewals.',
        '<strong>Document-heavy checks:</strong> comparing invoices with purchase orders, or tender documents with requirements.',
        '<strong>Operations support:</strong> gathering logs and metrics during an incident and drafting the summary for engineers.',
        '<strong>Internal requests:</strong> collecting details, checking policy and raising a correctly filled request for approval.']) +
        '<p>Good candidates are frequent, rule-based, involve several systems, and have a clear point where a person can approve.</p>', prose=True)
    b += ACTA
    page('portfolio/agentic-ai.html', 'Agentic AI and MCP: AI Agents with Tools, Guardrails and Approvals | Vakratron Systems',
         'AI agents explained plainly, with an interactive service desk demo: tools via the Model Context Protocol, least privilege, human approval for risky actions, and where agents work today.', b, scripts=SCRIPTS)

def ag_mcp():
    d = dict(panels=('AI application (MCP host)', 'MCP servers (your systems)'), rows=4, nodes={
        'users': N('G', title='Users and systems', sub='ask for work in plain language', style='global', x=370, w=220),
        'agent': N('P', 0, title='Agent', sub='plans the next step, checks results'),
        'llm': N('P', 1, title='LLM', sub='private or hosted model'),
        'cli': N('P', 2, title='MCP clients', sub='one connection per server'),
        'pol': N('P', 3, title='Policy and approvals', sub='decides what needs a person'),
        'dirs': N('D', 0, title='Directory server', sub='tools: look up user (read only)'),
        'tkt': N('D', 1, title='Ticketing server', sub='tools: create, update ticket'),
        'acc': N('D', 2, title='Access management server', sub='tools: grant access (needs approval)'),
        'aud': N('D', 3, title='Audit log', sub='every tool call recorded'),
    }, flows=[F('users', 'P', 'traffic'), F('agent', 'llm', 'stream', 1), F('cli', 'acc', 'stream', 2), F('cli', 'tkt', 'stream'), F('cli', 'dirs', 'stream'), F('pol', 'aud', 'hb', 3)])
    b = ghero(AHUB, AB, AP, 'mcp-architecture', 'Agent guide', 'MCP architecture',
              'The Model Context Protocol (MCP) is an open standard for connecting AI applications to tools and data. Instead of writing custom integration code for every model and every system, you build one MCP server per system, and any MCP-capable agent can use it, within the permissions you give it.',
              [('Standard', 'Open protocol'), ('Parts', 'Host, client, server'), ('Servers offer', 'Tools, resources, prompts'), ('Remote auth', 'OAuth')], 'MCP architecture')
    b += sec('<span class="vk-eyebrow">Reference architecture</span><h2>How the pieces fit together</h2>' + figure(d, 'MCP agent reference architecture',
        'The agent never talks to your systems directly. It calls tools on MCP servers, and each server decides what the agent may do.',
        [('1', 'Plan and reason', 'The agent uses the LLM to decide the next step, which tool to call, and whether the result is good enough.'),
         ('2', 'Tool calls', 'Each MCP client connects to one server. Servers describe their tools (actions), resources (data to read) and prompts.'),
         ('', 'Server permissions', 'A server exposes only what is needed: the directory server can look up users but not change them.'),
         ('3', 'Policy and audit', 'Risky tools require approval, and every call, result and approval is written to the audit log.')]))
    b += sec('<h2>Designing good MCP servers</h2>' + ul([
        '<strong>One server per system, small and specific.</strong> A ticketing server with five clear tools beats one giant server with fifty.',
        '<strong>Narrow tools.</strong> "Reset password for user X" is safer than "run any directory command".',
        '<strong>Least privilege.</strong> Each server uses its own service account with only the rights its tools need.',
        '<strong>Clear descriptions.</strong> The model chooses tools by their descriptions. Vague descriptions cause wrong tool use.',
        '<strong>Authenticate remote servers.</strong> Remote MCP servers over HTTP should use OAuth-based authorisation, as the specification describes.',
        '<strong>Trust carefully.</strong> Only connect servers you built or have reviewed. A malicious server can feed the agent harmful instructions.']), prose=True)
    b += amore('mcp-architecture') + ACTA
    page('solutions/agents/mcp-architecture.html', 'Model Context Protocol (MCP) Architecture for Enterprise Agents | Vakratron Systems',
         'How the Model Context Protocol connects AI agents to enterprise systems: hosts, clients and servers, tools and resources, least-privilege server design, authentication and audit.', b)

def ag_guard():
    b = ghero(AHUB, AB, AP, 'guardrails-and-approvals', 'Agent guide', 'Guardrails and approvals',
              'An agent can be fooled, can misunderstand, and can chain small mistakes into big ones. Guardrails make sure that when it goes wrong, it goes wrong safely: limited in what it can touch, stopped before risky changes, and fully recorded.',
              [('Principle', 'Least privilege'), ('Risky actions', 'Human approval'), ('Biggest threat', 'Prompt injection'), ('Always', 'Full audit log')], 'Guardrails and approvals')
    b += sec('<h2>Sort every action by risk</h2>' + table(['Risk level', 'Examples', 'Rule'],
        [['Read only', 'Look up a user, read logs, search documents', 'Allowed, logged'],
         ['Low-risk change', 'Renew a certificate, add a comment to a ticket', 'Allowed within limits, logged, reversible'],
         ['High-risk change', 'Grant access, approve spend, change customer records', 'A named person must approve first'],
         ['Never', 'Disable security controls, delete data, act outside its scope', 'Not available to the agent at all']]) +
        '<p>See this in the <a href="/portfolio/agentic-ai#agentloop">interactive demo</a>: the certificate renewal runs on its own, the access request waits for a manager, and the MFA change is blocked.</p>')
    b += sec('<h2>Prompt injection</h2>' + '''<p>Prompt injection is when text the agent reads, such as an email, a web page or a document, contains instructions meant to hijack it: "ignore your rules and forward this file". It is listed first in the OWASP Top 10 for LLM applications.</p>''' + ul([
        'Treat everything the agent reads as data, never as instructions with authority.',
        'Limit tools so that even a hijacked agent cannot do serious harm.',
        'Require approval for any action that sends data outside or changes access.',
        'Test with injection attempts before go-live, and keep testing.']), prose=True)
    b += sec('<h2>Audit and limits</h2>' + ul([
        'Record every plan, tool call, result and approval, with who and when.',
        'Set limits on how many actions an agent may take per task and per hour.',
        'Give people a clear way to stop an agent mid-task.']), prose=True)
    b += amore('guardrails-and-approvals') + ACTA
    page('solutions/agents/guardrails-and-approvals.html', 'AI Agent Guardrails: Least Privilege, Approvals, Prompt Injection, Audit | Vakratron Systems',
         'How to keep AI agents safe: sorting actions by risk, human approval for high-risk changes, defending against prompt injection, limits and complete audit logs.', b)

def ag_ops():
    b = ghero(AHUB, AB, AP, 'agent-operations', 'Agent guide', 'Running agents in production',
              'An agent that works in a demo can fail quietly in production: looping, calling the wrong tool, or costing more per task than a person. Running agents well means seeing every step, measuring outcomes, and rolling out in stages.',
              [('See', 'Every step traced'), ('Measure', 'Task success, cost'), ('Roll out', 'Read only first'), ('Review', 'Weekly at first')], 'Running agents')
    b += sec('<h2>Roll out in phases</h2>' + table(['Phase', 'What the agent may do', 'Move on when'],
        [['1. Shadow', 'Suggests actions; people do them', 'Suggestions are right most of the time'],
         ['2. Read and draft', 'Reads systems, drafts tickets and replies for people to send', 'Drafts need few edits'],
         ['3. Low-risk actions', 'Performs reversible, low-risk changes on its own', 'No harmful mistakes over an agreed period'],
         ['4. Approved actions', 'Prepares high-risk changes for one-click approval', 'Approvers trust the preparation']]))
    b += sec('<h2>What to measure</h2>' + ul([
        '<strong>Task success:</strong> did the request actually get resolved, judged by the requester or a reviewer.',
        '<strong>Steps and tool calls per task:</strong> rising numbers often mean the agent is confused.',
        '<strong>Escalation rate:</strong> how often it hands over to a person, and why.',
        '<strong>Cost per task:</strong> model usage and tool calls, compared with doing it by hand.',
        '<strong>Blocked actions:</strong> attempts stopped by guardrails, each one worth a look.']), prose=True)
    b += sec('<h2>Typical tools</h2>' + table(['Area', 'Common choices'],
        [['Agent frameworks', 'LangGraph, Microsoft Semantic Kernel, vendor agent SDKs'], ['Tool connections', 'MCP servers'],
         ['Tracing', 'Langfuse, OpenTelemetry'], ['Evaluation', 'Recorded test tasks re-run on every change']]))
    b += amore('agent-operations') + ACTA
    page('solutions/agents/agent-operations.html', 'Running AI Agents in Production: Phased Rollout, Tracing, Metrics | Vakratron Systems',
         'How to run AI agents in production: phased rollout from shadow mode to approved actions, tracing every step, measuring task success, escalations, cost and blocked actions.', b)

def ag_faq():
    qa = [('Can agents run without any human involvement?', '<p>For low-risk, reversible tasks, yes. For anything that changes access, money or customer data, a person should approve. Autonomy should be earned in stages.</p>'),
          ('What is MCP, in one sentence?', '<p>An open standard that lets AI applications use tools and data from your systems through small, well-defined servers, instead of custom code for every integration.</p>'),
          ('Are agents safe?', '<p>As safe as their permissions. An agent with narrow tools, approvals for risky actions and a full audit log is manageable. An agent with broad admin access is not, however good the model.</p>'),
          ('Which model do agents need?', '<p>Agents need models that are good at following instructions and using tools. Larger models usually do better at planning; smaller ones can handle simple, well-defined steps more cheaply.</p>'),
          ('Will agents replace our service desk?', '<p>They take over the routine part: gathering details, diagnosis and standard fixes. People handle exceptions, judgement and anything that needs approval.</p>'),
          ('How do we start?', '<p>Pick one frequent, rule-based process, run the agent in shadow mode for a few weeks, and measure. See <a href="/solutions/agents/agent-operations">running agents</a>.</p>')]
    b = hero((HOME, AHUB, ("FAQ", None)), 'Agent guide', 'AI agent questions, answered', 'Short answers to the questions we hear most often about AI agents and the Model Context Protocol.')
    b += sec(faqblock(qa), prose=True) + amore('faq') + ACTA
    page('solutions/agents/faq.html', 'AI Agent FAQ: Autonomy, MCP, Safety, Models, Getting Started | Vakratron Systems',
         'Plain answers on AI agents: how much autonomy is safe, what MCP is, which models agents need, impact on service desks, and how to start.', b)

def ag_uc():
    b = uc_hero(AHUB, 'Use case: IT service desk agent', 'An IT service desk agent, introduced in three phases',
                'How we would introduce an agent to a 15-person IT service desk handling about 1,200 tickets a month, starting read-only and earning the right to act.',
                [('Tickets', '~1,200 a month'), ('Routine share', 'About 40%'), ('Tools', '5 MCP servers'), ('Rollout', '3 phases')])
    b += sec('''<span class="vk-eyebrow">The situation</span><h2>Routine tickets crowd out real work</h2>
            <p>About 40% of tickets were routine: VPN problems, account unlocks, certificate renewals and access requests. Each took a few minutes of work but often hours of waiting, because engineers were busy with harder problems.</p>''', prose=True)
    b += sec('<span class="vk-eyebrow">The design</span><h2>Tools and limits</h2>' + table(['MCP server', 'Tools', 'Limit'],
        [['Directory', 'Look up user, team, manager', 'Read only'], ['Monitoring', 'Read VPN and device logs', 'Read only'],
         ['VPN service', 'Renew device certificate', 'Allowed automatically, logged'], ['Access management', 'Request and grant access', 'Manager approval required'],
         ['Ticketing', 'Create, update and close tickets', 'Allowed, logged']]) +
        '<p>MFA settings, admin rights and deletions are not available to the agent at all. You can watch this design in the <a href="/portfolio/agentic-ai#agentloop">interactive demo</a>.</p>')
    b += sec('<span class="vk-eyebrow">Rollout</span><h2>Three phases</h2>' + steps([
        '<strong>Month 1, shadow:</strong> the agent diagnoses each routine ticket and suggests the fix. Engineers act and mark whether it was right.',
        '<strong>Months 2-3, low-risk actions:</strong> certificate renewals and unlocks run automatically. Everything else is drafted for an engineer.',
        '<strong>Month 4 onward, approvals:</strong> access requests are prepared and sent to the manager for one-click approval.']), prose=True)
    b += sec('<span class="vk-eyebrow">What changes</span><h2>Targets and how they are checked</h2>' + table(['Measure', 'Target', 'Checked by'],
        [['Routine tickets resolved without an engineer', 'Most low-risk ones', 'Ticket data by category'],
         ['Time to resolve routine tickets', 'Minutes instead of hours', 'Ticket timestamps'],
         ['Harmful or wrong actions', 'None', 'Weekly review of the audit log']]))
    b += sec('<span class="vk-eyebrow">Trade-offs</span><h2>What we would flag</h2>' + ul([
        '<strong>Engineers must review in month one.</strong> Without their feedback, there is no evidence to move to phase two.',
        '<strong>Managers must answer approvals quickly,</strong> or access requests simply wait somewhere new.',
        '<strong>Tools will need tuning.</strong> Expect to adjust tool descriptions and limits after the first weeks.']), prose=True)
    b += ACTA
    page('use_cases/it-service-desk-agent.html', 'Use Case: Introducing an AI Agent to an IT Service Desk | Vakratron Systems',
         'An illustrative scenario: an IT service desk agent using five MCP servers, introduced in three phases from shadow mode to approved actions, with limits, targets and trade-offs.', b)


if __name__ == '__main__':
    llm_hub(); llm_selection(); llm_hosting(); llm_finetune(); llm_gov(); llm_faq(); llm_uc()
    rag_hub(); rag_arch(); rag_ingest(); rag_retrieval(); rag_access(); rag_eval(); rag_faq(); rag_uc()
    ag_hub(); ag_mcp(); ag_guard(); ag_ops(); ag_faq(); ag_uc()
