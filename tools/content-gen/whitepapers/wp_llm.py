"""Whitepaper content: Enterprise LLM strategy (Oct 2026).
Plain HTML fragments. Rendered to the web page and the PDF by wp_render.py."""

def table(head, rows, cls=''):
    th = ''.join('<th>' + h + '</th>' for h in head)
    tr = ''.join('<tr>' + ''.join('<td>' + c + '</td>' for c in r) + '</tr>' for r in rows)
    return '<div class="wp-table' + (' ' + cls if cls else '') + '"><table><thead><tr>' + th + '</tr></thead><tbody>' + tr + '</tbody></table></div>'

def ul(items):
    return '<ul>' + ''.join('<li>' + i + '</li>' for i in items) + '</ul>'

def callout(title, body, kind=''):
    return '<div class="wp-callout' + (' ' + kind if kind else '') + '"><strong>' + title + '</strong> ' + body + '</div>'

N = lambda x, y, w, title, sub='', icon='server', tone='blue', **k: dict(x=x, y=y, w=w, title=title, sub=sub, icon=icon, tone=tone, **k)
DIAGRAM = dict(w=1120, h=470,
  zones=[
    dict(x=20, y=20, w=220, h=430, title='Applications and users', kind='ext'),
    dict(x=260, y=20, w=560, h=290, title='LLM gateway, in your network', kind='ai'),
    dict(x=260, y=340, w=560, h=110, title='Observability and governance', kind='sec'),
    dict(x=840, y=20, w=260, h=290, title='Self-hosted models on GPUs', kind='dc'),
    dict(x=840, y=340, w=260, h=110, title='Approved external API', kind='cloud', dashed=True),
  ],
  nodes={
    'chat': N(35, 60, 190, 'Staff assistant', 'browser and Teams', 'users', 'slate'),
    'apps': N(35, 150, 190, 'Business apps', 'claims, CRM, ITSM', 'grid', 'slate'),
    'rag': N(35, 240, 190, 'RAG service', 'policy documents', 'search', 'slate'),
    'dev': N(35, 330, 190, 'Developers', 'one key per team', 'git', 'slate'),
    'gw': N(280, 60, 255, 'Gateway entry point', 'company sign-in, team keys', 'lb', 'violet'),
    'bud': N(550, 60, 255, 'Budgets and limits', 'per team, per month', 'money', 'amber'),
    'pii': N(280, 145, 255, 'PII redaction', 'Aadhaar, PAN, account numbers', 'shield', 'pink'),
    'guard': N(550, 145, 255, 'Guardrails', 'injection and content filters', 'shield', 'pink'),
    'rt': N(280, 230, 255, 'Router', 'by data class, task and cost', 'flow', 'violet'),
    'cat': N(550, 230, 255, 'Model catalogue', 'approved versions only', 'doc', 'blue'),
    'big': N(855, 60, 230, 'Large model (70B)', 'vLLM, FP8, 4 GPUs', 'llm', 'blue'),
    'small': N(855, 145, 230, 'Small model (8B)', 'extraction and routing', 'llm', 'blue'),
    'emb': N(855, 230, 230, 'Embedding model', 'for RAG search', 'model', 'blue'),
    'ext': N(855, 378, 230, 'Commercial model', 'Public and Internal only', 'cloud', 'amber'),
    'log': N(280, 378, 255, 'Audit log and traces', 'retention set by policy', 'lock', 'slate'),
    'eval': N(550, 378, 255, 'Evaluation and cost', 'test set, dashboards', 'chart', 'slate'),
  },
  flows=[
    dict(a='chat', b='gw', kind='traffic', n=1),
    dict(a='apps', b='gw', kind='traffic', via=[(250, 179), (250, 89)]),
    dict(a='rag', b='gw', kind='traffic', via=[(250, 269), (250, 89)]),
    dict(a='dev', b='gw', kind='traffic', via=[(250, 359), (250, 89)]),
    dict(a='gw', b='bud', kind='control'),
    dict(a='gw', b='pii', kind='data', n=2),
    dict(a='pii', b='guard', kind='control'),
    dict(a='pii', b='rt', kind='data', n=3),
    dict(a='rt', b='cat', kind='control'),
    dict(a='rt', b='big', kind='data', n=4, label='Confidential stays in house', sa=('b', 100), via=[(507, 300), (830, 300), (830, 89)], lpos=(680, 300)),
    dict(a='rt', b='small', kind='data', sa=('b', 100), via=[(507, 300), (830, 300), (830, 174)]),
    dict(a='rt', b='emb', kind='data', sa=('b', 100), via=[(507, 300), (830, 300), (830, 259)]),
    dict(a='rt', b='ext', kind='traffic', n=5, label='redacted first', sa=('b', 40), via=[(447, 325), (830, 325), (830, 407)], lpos=(680, 325)),
    dict(a='rt', b='log', kind='mgmt', n=6, label='logged', sa=('b', -60), sb=('t', -60), lpos=(347, 325)),
    dict(a='log', b='eval', kind='mgmt'),
  ])

META = dict(
    slug='enterprise-llm-strategy',
    title='Running LLMs in the Enterprise',
    subtitle='Choosing between API and self-hosted models, governing them, and keeping costs predictable',
    topic='llm',
    area='Enterprise LLM',
    version='Version 1.0, October 2026',
    pages='Approx. 15 pages',
    minutes=26,
    audience='CIOs, IT heads, enterprise and AI architects, security, risk and data protection teams',
    audience_web='CIOs, IT heads, enterprise and AI architects, and security, risk and data protection teams',
    pdf_name='Vakratron-Enterprise-LLM-Strategy.pdf',
    help_title='How we can help with enterprise LLMs',
    help_items=['<strong>LLM review:</strong> a two to three week look at your use cases, data rules and current usage, with a plain recommendation on models, hosting and cost.',
                '<strong>Model comparison:</strong> we build a test set from your real work with your teams and score two or three candidate models on quality, speed and cost.',
                '<strong>Platform design:</strong> gateway, redaction, budgets, GPU sizing and an operating model, written down so you can take it to vendors or build it yourselves.'],
    help_links=[('Ask for an LLM review', '/contact?topic=llm'), ('Enterprise LLM solutions', '/portfolio/enterprise-llm'), ('See a worked LLM gateway design', '/deployments/enterprise-llm-gateway')],
    desc='A practical whitepaper on running large language models in the enterprise: use-case triage, API versus self-hosted versus hybrid with a cost crossover formula, model selection and testing, serving and quantisation, fine-tuning versus RAG, an LLM gateway for routing, redaction and budgets, the DPDP Act, and a 36-point checklist.',
    inside=['A simple way to triage use cases by value, risk and how easily answers can be checked',
            'Public API, private endpoint, self-hosted and hybrid compared on data, quality and cost',
            'A cost crossover formula: the daily token volume at which your own GPUs pay off',
            'How to choose and test models on your own work, not on leaderboards',
            'When to prompt, when to use RAG and when fine-tuning is worth it',
            'An LLM gateway design for routing, PII redaction, budgets and audit, with DPDP Act points',
            'A 36-point readiness checklist for platform, security and operations'],
)

SECTIONS = []
def S(id, title, html):
    SECTIONS.append(dict(id=id, title=title, html=html))

S('summary', 'Executive summary', '''
<p>Most organisations already use large language models. Often the first use is unofficial: staff pasting documents into free chat tools on personal accounts. The question for IT leadership is no longer whether to use LLMs, but how: which tasks, which models, where they run, what data they may see, and how anyone knows the answers are good enough and the bill is under control.</p>
<p>This paper sets out a practical approach for the IT leaders who decide and the security, risk and data protection teams who sign off.</p>
<div class="wp-keys"><h3>Five things to take away</h3><ol>
<li><strong>Start from tasks, not models.</strong> Pick a few frequent, well-defined tasks where answers can be checked. A narrow task done well beats &ldquo;AI everywhere&rdquo; done badly.</li>
<li><strong>Test on your own examples.</strong> A test set of 100 to 300 real cases, with answers agreed by the people who do the work, is the single most valuable asset in an LLM programme.</li>
<li><strong>Self-hosting is a data and volume decision.</strong> It pays off on cost only above a daily token volume you can calculate. Below that, data rules are the only good reason.</li>
<li><strong>Put one gateway in front of every model.</strong> Sign-in, redaction, routing, budgets and logging in one place, so models can change without changing every application.</li>
<li><strong>Treat models like any other production change.</strong> New models and prompts go through test, approval and gradual rollout, with a quick way back.</li>
</ol></div>''')

S('why-it-goes-wrong', 'Why LLM projects stall', '''
<div class="keep"><p>LLM pilots are easy to start and hard to finish. A demo on ten hand-picked questions impresses in a week; handling thousands of messy, real requests safely and at a known cost takes discipline most pilots skip. The same problems recur:</p>
''' + table(['What we find', 'What happens'], [
    ['No approved option for staff', 'People use whatever is free. Customer data and internal documents leave the company without anyone deciding they should.'],
    ['Pilot judged on easy questions', 'Real users ask vague, multi-part and out-of-scope questions. Quality drops, and nobody measured it before go-live.'],
    ['Every app calls the model directly', 'Keys are scattered in code, nobody can see total usage, and changing the model means changing every application.'],
    ['Long prompts on the largest model', 'Whole documents are sent with every request to the most expensive model. Monthly cost becomes a board-level question.'],
    ['Fine-tuning to teach facts', 'Months go into training a model to &ldquo;know&rdquo; policies that change every quarter, when the real need was to look them up.'],
    ['No owner after go-live', 'Quality drifts after a model update or a document change, and complaints are the first warning.'],
]) + '</div>' + callout('In short:', 'most LLM failures are not model failures. They come from unclear tasks, untested quality, uncontrolled access to data and unmanaged cost.'))

S('concepts', 'The building blocks, explained properly', '''
<h3>Tokens and context</h3>
<p>Models read and write in <strong>tokens</strong>, pieces of words. In English one token is roughly three quarters of a word, so 1,000 words is about 1,300 tokens. Hindi and other Indian languages in their own scripts often take two to four times as many tokens for the same meaning on many models, which raises cost and fills the context faster. The <strong>context window</strong> is how many tokens the model considers at once. Output tokens usually cost three to five times more than input.</p>
<h3>Model size</h3>
<p>Small open models of around 8 billion parameters (8B) are fast and cheap, and handle extraction, classification and routing well. Models around 70B handle most drafting, summarising and question answering. The largest commercial models lead on complex reasoning and long documents.</p>
<h3>Serving</h3>
<p>An open model runs on a <strong>model server</strong> such as vLLM or NVIDIA Triton with TensorRT-LLM. Three techniques let one server handle hundreds of users rather than a few:</p>
''' + ul(['<strong>Continuous batching:</strong> requests join and leave the batch at every step, so the GPU stays busy instead of waiting for the slowest request.',
          '<strong>Paged KV cache:</strong> the memory that holds each conversation&rsquo;s context is allocated in small blocks, so many more requests fit on one GPU.',
          '<strong>Prefix caching:</strong> a long system prompt or a shared document is processed once and reused across requests.']) + '''
<p>Two numbers describe the user experience: <strong>time to first token</strong> (how long before the answer starts, ideally under one to two seconds for chat) and <strong>output tokens per second per user</strong> (reading speed is about 10 to 15; 30 or more feels instant).</p>
<h3>Quantisation</h3>
<p>Quantisation stores weights in fewer bits. FP8 halves memory against 16-bit with little measurable quality loss on most tasks, and runs natively on H100, H200 and L40S GPUs. 4-bit formats such as AWQ halve it again but can hurt accuracy, especially in Indian languages. Re-run the test set on any quantised model.</p>
<div class="keep"><h3>Prompting, RAG or fine-tuning</h3>
<p>These are often confused. They solve different problems and are usually used together:</p>
''' + table(['The problem', 'Try first', 'Why'], [
    ['The model does not know our policies, products or cases', 'RAG: look up the relevant passages and give them to the model', 'Facts change. Looking them up at question time keeps answers current and lets you show sources.'],
    ['Answers are in the wrong format or tone', 'Better prompts with two or three good examples, then fine-tuning', 'Examples in the prompt fix most format problems. Fine-tune only if it still drifts.'],
    ['A narrow task repeated thousands of times a day', 'Fine-tune a small model', 'A small fine-tuned model can match a large general one on one task at a fraction of the cost.'],
    ['Specialised language, such as legal or internal jargon', 'RAG plus a glossary, then fine-tuning if needed', 'Retrieval supplies the facts; fine-tuning helps the model use the terms naturally.'],
]) + '</div>' + '''
<p>Fine-tuning today usually means <strong>LoRA</strong>: training a small set of extra weights rather than the whole model. It needs hundreds to a few thousand good examples, fits on one 8-GPU server for a 70B model, and usually has to be repeated when the base model changes.</p>''')

S('patterns', 'API, private endpoint, self-hosted or hybrid', '''
<div class="keep"><p>There are four ways to give the organisation access to LLMs. They differ in where data goes, which models are available, how cost behaves as usage grows, and how much the IT team has to run.</p>
''' + table(['Option', 'Where data goes', 'Models', 'Cost behaviour', 'What you run'], [
    ['Public API', 'To the provider, under its enterprise terms', 'Strongest commercial models', 'Pure per-token; grows in line with use', 'Almost nothing'],
    ['Private cloud endpoint', 'Stays in your cloud tenancy and chosen region', 'Commercial models offered in that region', 'Per-token or reserved capacity', 'Cloud networking, keys, access'],
    ['Self-hosted open model', 'Never leaves your network', 'Open-weight models (Llama, Mistral, Qwen, Gemma and others)', 'Mostly fixed; cheap per token at high use', 'GPUs, model servers, platform, upgrades'],
    ['Hybrid behind a gateway', 'Decided per request by data class', 'Both', 'Fixed base plus per-token for the rest', 'Gateway and a smaller GPU estate'],
], 'wp-compact') + '''</div>
<h3>Public API</h3>
<p>The fastest start and the strongest models. The questions are contractual: whether prompts are retained or used for training, where they are processed, and what cost looks like at ten times today&rsquo;s volume. Enterprise agreements usually exclude training on your data; consumer terms often do not.</p>
<h3>Private cloud endpoint</h3>
<p>Commercial models deployed inside your own cloud account, in an Indian region where available. Data stays within your tenancy, under controls you already use. Check which models each region offers.</p>
<h3>Self-hosted open model</h3>
<p>An open-weight model on your own GPUs. Data never leaves infrastructure you control, versions change only when you decide, and it can run air-gapped. In exchange you run GPUs, serving and upgrades, and open models may trail the best commercial ones on the hardest tasks. Read each licence: some restrict use above a user count.</p>
<h3>Hybrid behind a gateway</h3>
<p>Most organisations end up here: confidential and personal data goes to self-hosted models, while redacted public and internal content may use a commercial model. A gateway makes the choice per request.</p>''')

S('choosing', 'Choosing: use cases first, then models', '''
<div class="keep"><h3>Triage the use cases</h3>
<p>Score each candidate on frequency, value, data sensitivity and how easily a person can check the output. The best first projects are frequent, valuable and easy to check.</p>
''' + table(['Use case type', 'Examples', 'Risk', 'Typical first approach'], [
    ['Draft for a person to edit', 'Email replies, meeting notes, first drafts of reports', 'Low: a person reviews', 'API or private endpoint; light controls'],
    ['Answer from documents', 'Policy and product questions, IT and HR help', 'Medium: wrong or leaked answers', 'RAG with permissions and sources'],
    ['Extract and classify', 'Claim forms, invoices, tickets, KYC documents', 'Medium: errors flow into systems', 'Small or fine-tuned model, confidence thresholds'],
    ['Customer-facing conversation', 'Service chat, contact centre assist', 'High: brand and conduct risk', 'Assist an agent first, then limited self-service'],
    ['Decisions about people', 'Credit, claims, hiring, eligibility', 'Very high: fairness and regulation', 'Decision support only; a person decides'],
], 'wp-compact') + '''</div>
<h3>Five questions that decide hosting</h3>
<ol class="wp-steps">
<li><strong>May this data leave our network?</strong> Classify the data each use case touches. If personal, customer financial or restricted government data is involved, sector rules and your own policy may decide for you.</li>
<li><strong>What is the daily token volume, now and in a year?</strong> Compare it with the crossover point in the sizing section. Below it, APIs are cheaper.</li>
<li><strong>Does an open model pass the test set?</strong> If only a frontier commercial model meets the quality bar, self-hosting the task is not yet an option.</li>
<li><strong>Is there a hard latency, availability or air-gap requirement?</strong> Plants, defence and some government networks cannot depend on an internet path.</li>
<li><strong>Can we run GPUs well?</strong> If no team owns drivers, serving and capacity, budget for one or use a managed private option.</li>
</ol>
<div class="keep"><h3>Testing models on your own work</h3>
<p>Collect 100 to 300 real examples with the answer a good employee would give, including messy and out-of-scope cases, where models differ most. Define &ldquo;good&rdquo;: correct facts, right format, and &ldquo;I don&rsquo;t know&rdquo; when it should. Score two or three candidates automatically and by reviewers, then weigh cost and speed. A model 3 percent better but ten times dearer is rarely right. Keep the test set: a new model version can then be judged in an afternoon.</p></div>''')

S('architecture', 'Reference architecture', '''
<p>The diagram shows a hybrid platform built around one LLM gateway. Applications never call a model directly: the gateway knows who is asking, cleans the request, picks a model, enforces budgets and records what happened.</p>
[[DIAGRAM]]
<p class="wp-caption">Numbered flows: (1) every application and user calls one gateway endpoint, authenticated by company sign-in or a team key, (2) each request passes PII redaction and guardrails, (3) the router reads the data class tag and task type, (4) Confidential and Restricted requests go only to self-hosted models, with the small model handling extraction and routing, (5) Public and Internal requests may go to an approved commercial model after redaction, (6) every request, model choice and cost is logged for audit and evaluation.</p>
<h3>What the gateway does</h3>
''' + table(['Function', 'In practice'], [
    ['Identity and access', 'Company sign-in for people, one key per team for applications. Groups decide which models and data classes each team may use.'],
    ['Redaction', 'Personal data is masked before any model sees it: names, phone numbers, Aadhaar, PAN, bank account and IFSC codes, using Microsoft Presidio plus rules for Indian identifiers.'],
    ['Routing', 'By data class, task and cost: small model for extraction, larger model for drafting, commercial model only for permitted classes. Fallback to a second model if one is down.'],
    ['Budgets and limits', 'Monthly budget per team with alerts at 50, 80 and 100 percent, a cap on tokens per request, and rate limits so one runaway job cannot starve everyone else.'],
    ['Logging', 'Who asked, which model answered, tokens, cost, latency and guardrail decisions. Prompt text is kept only as long as policy allows.'],
]) + callout('Common tools:', 'LiteLLM or an API gateway with LLM routing, vLLM on Kubernetes with the NVIDIA GPU Operator, Presidio and NeMo Guardrails, and Langfuse or OpenTelemetry for traces. All are replaceable; the pattern is what matters.'))

S('sizing', 'Sizing and cost', '''
<div class="keep"><h3>The cost crossover</h3>
<p>An API costs a fixed amount per token. A self-hosted model costs roughly the same each month whether it is busy or idle. The volume at which the two are equal is the crossover:</p>
<div class="wp-formula">Crossover tokens per day = monthly self-hosted cost (&#8377;) &times; 1,000,000 &divide; (active days per month &times; blended API price per million tokens (&#8377;))</div></div>
<p>The blended price mixes input and output at your real ratio. For a frontier-class model at &#8377;250 per million input tokens and &#8377;1,250 per million output, a 3:1 input to output mix blends to (3 &times; 250 + 1,250) &divide; 4 = &#8377;500 per million. Mid-tier commercial models are often a quarter of that or less.</p>
<div class="keep"><h3>What self-hosting costs per month</h3>
<p>Planning ranges for one 8-GPU H100 server running a 70B-class model in FP8 as two 4-GPU replicas:</p>
''' + table(['Item', 'Basis', 'Monthly, planning range'], [
    ['Server, networking and storage share', '&#8377;2.6 to 3.2 crore, over 48 months', '&#8377;5.4 to 6.7 lakh'],
    ['Power and cooling', 'About 10.2 kW &times; 1.5 PUE &times; 730 hours = 11,200 kWh at &#8377;8 to 10', '&#8377;0.9 to 1.1 lakh'],
    ['Rack space in a data centre or colocation', 'One high-density rack position', '&#8377;0.8 to 1.5 lakh'],
    ['Support, software and spares', 'Hardware support, enterprise software where used', '&#8377;0.5 to 1.0 lakh'],
    ['Platform engineering', 'About 1.5 people across GPUs, serving and gateway', '&#8377;2.5 to 3.5 lakh'],
    ['<strong>Total</strong>', '', '<strong>&#8377;10 to 14 lakh, midpoint &#8377;12 lakh</strong>'],
]) + '''</div>
<p>With &#8377;12 lakh a month, 22 working days and a frontier-class API at &#8377;500 per million tokens, the crossover is 12,00,000 &times; 1,000,000 &divide; (22 &times; 500), or about <strong>110 million tokens a day</strong>. Against a mid-tier API at &#8377;120 per million it rises to about 450 million tokens a day, which is more than one server can handle. Self-hosting wins on cost only when the task needs a large model and volume is high.</p>
<div class="keep"><h3>GPU memory</h3>
<div class="wp-formula">GPU memory needed &asymp; model weights + (KV cache per token &times; context length &times; concurrent requests) + 10 to 20% overhead</div></div>
<p>A 70B model&rsquo;s weights need about 140 GB in 16-bit, 70 GB in FP8 and 35 to 40 GB in 4-bit; its KV cache is about 0.33 MB per token. On four 80 GB H100s (320 GB), FP8 weights take 70 GB and overhead about 40 GB, leaving roughly 210 GB for cache: about 640,000 tokens, or around 80 concurrent requests at 8,000 tokens of context each.</p>
<h3>A worked example</h3>
<p>A financial services firm plans two uses. A staff assistant: 1,500 daily users &times; 12 questions &times; 4,000 tokens (3,500 in, 500 out) = 72 million tokens a day. Loan file summaries: 1,000 files &times; 30,000 tokens (28,000 in, 2,000 out) = 30 million a day. Total about 102 million tokens a day, or 2,244 million a month over 22 working days.</p>
''' + table(['', 'Frontier API', 'Mid-tier API', 'Self-hosted 70B, one server'], [
    ['Monthly cost at 102 M tokens a day', '2,244 &times; &#8377;500 = &#8377;11.2 lakh', '2,244 &times; &#8377;120 = &#8377;2.7 lakh', '&#8377;10 to 14 lakh'],
    ['Monthly cost at 3 times the volume', '&#8377;33.7 lakh', '&#8377;8.1 lakh', '&#8377;20 to 24 lakh, with a second server'],
    ['Passes the test set?', 'Yes', 'For the assistant, not for summaries', 'Yes, after prompt tuning'],
    ['Customer data leaves the network?', 'Yes, under contract', 'Yes, under contract', 'No'],
], 'wp-compact') + '''
<p>Peak load check: 11 million output tokens over a 9-hour day, doubled for the busy hour, is about 680 tokens a second, within one server&rsquo;s planning capacity of around 2,000. The sensible answer is hybrid: loan files hold customer financial data, so they run self-hosted; the assistant uses the mid-tier API on redacted internal content, and moves in-house if volume grows.</p>
''' + callout('Costs that are often missed:', 'long prompts repeated on every call, evaluation runs, a fallback for availability, GPU refresh after four to five years, and the people to run it.', 'warn'))

S('security', 'Security, data protection and the DPDP Act', '''
<h3>Data protection in India</h3>
<p>The Digital Personal Data Protection Act, 2023 and its Rules, whose main obligations phase in through 2026 and 2027, apply to personal data in prompts, documents and logs just as to any other system. In practice:</p>
''' + ul(['<strong>Purpose and notice:</strong> personal data in an LLM workflow needs a lawful basis and a stated purpose. Training a model on customer data collected for servicing is a new purpose.',
          '<strong>Minimisation:</strong> redact personal data the task does not need before it reaches any model, internal or external.',
          '<strong>Retention and erasure:</strong> prompts and traces containing personal data are personal data. Set retention periods; make erasure reach logs and indexes.',
          '<strong>Security safeguards and breach reporting:</strong> reasonable safeguards are a legal duty, and breaches must be reported to the Data Protection Board and affected people. CERT-In expects cyber incidents to be reported within 6 hours.',
          '<strong>Processors:</strong> an API provider processing personal data on your behalf needs a contract that matches your obligations.',
          '<strong>Sector rules:</strong> RBI, IRDAI and SEBI requirements on outsourcing, data location and audit may be stricter than the Act. Check them per use case.']) + '''
<h3>Threats specific to LLMs</h3>
''' + table(['Threat', 'Control'], [
    ['Prompt injection: hidden instructions in a document or email', 'Treat retrieved text as data; limit what the model can do; filter outputs; test with attack examples.'],
    ['Leakage across users', 'Permissions enforced at retrieval time; no shared conversation memory between users.'],
    ['Sensitive data in logs', 'Redact before logging; restrict who can read traces; time-limited retention.'],
    ['Unapproved models and keys', 'All traffic through the gateway; outbound access to AI services blocked except via the gateway.'],
    ['Untrusted model files', 'Download from known sources, verify checksums, prefer safetensors format, scan containers.'],
]) + callout('A useful reference:', 'the OWASP Top 10 for LLM Applications lists prompt injection first. Use it as the basis of the security review before go-live.'))

S('operating', 'Operating it: evaluation, monitoring and change', '''
<p>An LLM system that worked in March can be worse in June without anyone touching it: the provider updates the model, documents change, users ask new things.</p>
<h3>Measure quality all the time</h3>
''' + ul(['<strong>Offline:</strong> re-run the test set before every change to model, prompt, retrieval or redaction rules. No change goes live with a lower score without a written reason.',
          '<strong>Online:</strong> thumbs up or down with an optional comment, plus a weekly sample of 30 to 50 live answers reviewed by people who know the work.',
          '<strong>Drift:</strong> alert on falling scores, rising complaints, more refusals or a change in answer length after any change.']) + '''
<h3>Watch the platform</h3>
''' + table(['Metric', 'Why it matters', 'Typical alert'], [
    ['Time to first token, 95th percentile', 'Users feel this first', 'Above 2 seconds for chat'],
    ['GPU memory and cache use', 'Full cache means queued requests', 'Above 90% for 15 minutes'],
    ['Queue length and rejected requests', 'Capacity is short', 'Any sustained queue at busy hour'],
    ['Tokens and cost per team', 'Budgets and surprises', '80% of monthly budget'],
    ['Error and fallback rate', 'A model or provider is failing', 'Above 1% of requests'],
], 'wp-compact') + '''
<h3>Change models safely</h3>
<p>Keep a catalogue of approved models with version, licence, allowed data classes and test score. A new version passes the test set and a security check, then takes a small share of gateway traffic before full rollout, with a one-step rollback. Pin API model versions where possible.</p>''')

S('roadmap', 'A practical roadmap', '''
<div class="keep"><p>A first production use case typically takes 10 to 14 weeks.</p>
''' + table(['Stage', 'Typical duration', 'Outcome'], [
    ['1. Triage', '2 weeks', 'Use cases scored, one or two chosen with business owners, data classified, baseline time and cost measured.'],
    ['2. Test and compare', '3 to 4 weeks', 'Test set of 100 to 300 real cases, two or three models scored on quality, speed and cost, hosting decision.'],
    ['3. Guarded build', '3 to 5 weeks', 'Gateway with sign-in, redaction, routing, budgets and logging; GPU platform if self-hosting; security review.'],
    ['4. Pilot', '4 weeks', 'Real users in one department, quality and time saved measured against baseline, issues fixed.'],
    ['5. Scale and operate', 'Ongoing', 'More use cases on the same gateway, monthly quality review, model catalogue and change process in use.'],
]) + '</div>' + callout('Order matters:', 'build the gateway with the first use case, not after the fifth. Retrofitting it later is slow and rarely complete.'))

S('mistakes', 'Ten common mistakes', '<ol class="wp-steps">' + ''.join('<li>' + m + '</li>' for m in [
    '<strong>No approved option for staff.</strong> Shadow use of public tools continues with company data.',
    '<strong>Choosing a model from a leaderboard.</strong> Test on your own examples instead.',
    '<strong>Testing only on easy questions.</strong> Real users find the edge cases on day one.',
    '<strong>Fine-tuning to teach facts.</strong> Use RAG for anything that changes.',
    '<strong>Self-hosting below the crossover without a data reason.</strong> GPUs sit idle and cost more than the API would.',
    '<strong>Applications calling models directly.</strong> No central view of usage, cost or data flows.',
    '<strong>Sending whole documents on every call.</strong> Retrieve the relevant passages and cache shared prompts.',
    '<strong>Logging everything forever.</strong> Logs become the largest store of personal data in the company.',
    '<strong>Letting the provider change the model silently.</strong> Pin versions and re-test before switching.',
    '<strong>No owner after go-live.</strong> Quality drifts and nobody notices until users stop using it.']) + '</ol>')

CHECKLIST = [
  ('Use cases and ownership', ['An approved LLM option available to staff, with a usage policy',
                  'Use cases scored on frequency, value, data sensitivity and ease of checking',
                  'A named business owner for each use case in production',
                  'Baseline time and cost measured before the pilot',
                  'Decisions about people kept with people, with the model as support only',
                  'A shared register of LLM use cases, models and data classes']),
  ('Data and compliance', ['Data classes defined, with which may go to external APIs',
                  'Lawful basis and purpose recorded for personal data in each use case',
                  'Redaction of personal data before any model, including Indian identifiers',
                  'Retention periods set for prompts, answers and traces',
                  'Erasure requests reach logs and indexes',
                  'Provider contracts cover training use, retention, location and breach notice',
                  'Sector rules (RBI, IRDAI, SEBI or others) checked per use case']),
  ('Models and evaluation', ['Test set of 100 to 300 real cases per use case, with agreed answers',
                  'Out-of-scope and hard cases included in the test set',
                  'At least two models compared on quality, speed and cost',
                  'Quantised models re-tested before use',
                  'Model licences reviewed for your use and scale',
                  'Model catalogue with version, licence, allowed data classes and score']),
  ('Platform and serving', ['Model servers with continuous batching and prefix caching',
                  'GPU memory sized for weights, cache and peak concurrency',
                  'Second replica, second server or API fallback for availability',
                  'Model files from known sources, checksums verified',
                  'Busy-hour load tested before go-live']),
  ('Gateway, cost and security', ['All model traffic through one gateway; direct outbound access blocked',
                  'Company sign-in for people, one key per team for applications',
                  'Routing by data class enforced, not advisory',
                  'Monthly budgets per team with alerts at 50, 80 and 100 percent',
                  'Caps on tokens per request and rate limits per team',
                  'Prompt injection tested using the OWASP Top 10 for LLM Applications',
                  'Logs readable only by named roles']),
  ('Operations and change', ['Test set re-run before every model, prompt or retrieval change',
                  'Weekly review of a sample of live answers',
                  'Alerts on latency, cache use, errors, cost and guardrail hits',
                  'Gradual rollout and one-step rollback for model changes',
                  'Quarterly cost review against the crossover point']),
]
n_items = sum(len(i) for _, i in CHECKLIST)
S('checklist', 'Enterprise LLM readiness checklist (' + str(n_items) + ' points)',
  '<p>Use this list to score your current position. Anything you cannot tick with evidence is a gap worth closing.</p><div class="wp-check">' +
  ''.join('<div class="wp-check-group"><h3>' + g + '</h3><ul>' + ''.join('<li>' + i + '</li>' for i in items) + '</ul></div>' for g, items in CHECKLIST) + '</div>')

S('glossary', 'Glossary', table(['Term', 'Meaning'], [
    ['Token', 'A piece of a word. Models read, write and are priced in tokens; about 1,300 tokens per 1,000 English words.'],
    ['Time to first token', 'How long a user waits before the answer starts to appear.'],
    ['Continuous batching', 'Serving technique that adds and removes requests at every step to keep the GPU busy.'],
    ['KV cache', 'GPU memory holding the processed context of each active request.'],
    ['Quantisation', 'Storing model weights in fewer bits (FP8, 4-bit) to save memory and speed up serving.'],
    ['RAG', 'Retrieval-augmented generation: finding relevant passages and giving them to the model to answer from.'],
    ['LoRA', 'A fine-tuning method that trains a small set of extra weights instead of the whole model.'],
    ['LLM gateway', 'A single entry point for all model traffic that handles access, redaction, routing, budgets and logging.'],
    ['Prompt injection', 'Instructions hidden in text the model reads, intended to make it ignore its rules.'],
    ['Data Fiduciary', 'Under the DPDP Act, the organisation that decides why and how personal data is processed.'],
]))
