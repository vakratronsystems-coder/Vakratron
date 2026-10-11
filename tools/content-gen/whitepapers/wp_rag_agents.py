"""Whitepaper content: RAG and agentic AI (Oct 2026).
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
DIAGRAM = dict(w=1120, h=490,
  zones=[
    dict(x=20, y=20, w=220, h=115, title='Document sources', kind='ext'),
    dict(x=260, y=20, w=840, h=115, title='Ingestion, runs on every change', kind='ai'),
    dict(x=20, y=155, w=220, h=320, title='People', kind='ext'),
    dict(x=260, y=155, w=560, h=320, title='Assistant and agent runtime', kind='ai'),
    dict(x=840, y=155, w=260, h=115, title='Search index', kind='dc'),
    dict(x=840, y=285, w=260, h=190, title='Enterprise systems', kind='ent'),
  ],
  nodes={
    'docs': N(35, 60, 190, 'Documents', 'portals, shares, scans', 'doc', 'slate'),
    'parse': N(280, 60, 230, 'Parse and OCR', 'tables kept as tables', 'scan', 'violet'),
    'split': N(560, 60, 230, 'Split and tag', 'headings, dates, access lists', 'grid', 'violet'),
    'embed': N(840, 60, 245, 'Embed', 'multilingual embedding model', 'model', 'violet'),
    'user': N(35, 195, 190, 'Employees', 'company sign-in', 'users', 'slate'),
    'appr': N(35, 400, 190, 'Approvers', 'high-risk actions only', 'person', 'pink'),
    'orch': N(275, 195, 240, 'Assistant or agent', 'plans steps, cites sources', 'robot', 'violet'),
    'ret': N(565, 195, 240, 'Retrieval', 'permission filter, then rerank', 'search', 'blue'),
    'tgw': N(275, 300, 240, 'Tool gateway (MCP)', 'approved tools, value limits', 'flow', 'blue'),
    'llm': N(565, 300, 240, 'LLM via gateway', 'self-hosted or approved API', 'llm', 'violet'),
    'aud': N(275, 400, 240, 'Audit trail', 'every step, call and approval', 'lock', 'slate'),
    'guard': N(565, 400, 240, 'Guardrails', 'injection and output checks', 'shield', 'pink'),
    'idx': N(855, 195, 230, 'Hybrid search index', 'keywords plus embeddings', 'storage', 'green'),
    'itsm': N(855, 325, 230, 'Service desk', 'tickets, unlocks, status', 'grid', 'green'),
    'erp': N(855, 400, 230, 'ERP and HR', 'read; changes need approval', 'building', 'green'),
  },
  flows=[
    dict(a='docs', b='parse', kind='data', n=1),
    dict(a='parse', b='split', kind='data'),
    dict(a='split', b='embed', kind='data'),
    dict(a='embed', b='idx', kind='data', n=2, sa=('b', 7.5), sb='t'),
    dict(a='user', b='orch', kind='traffic', n=3),
    dict(a='orch', b='ret', kind='control', n=4),
    dict(a='ret', b='idx', kind='data'),
    dict(a='orch', b='llm', kind='control', n=5, sa=('b', 80), sb='t', via=[(475, 277), (685, 277)], lpos=(580, 277)),
    dict(a='llm', b='guard', kind='control'),
    dict(a='orch', b='tgw', kind='control', sa=('b', -40), sb=('t', -40)),
    dict(a='tgw', b='itsm', kind='control', n=6, label='within limits', sa=('b', 80), via=[(475, 379), (830, 379), (830, 354)], lpos=(585, 379)),
    dict(a='tgw', b='erp', kind='control', sa=('b', 80), via=[(475, 379), (830, 379), (830, 429)]),
    dict(a='tgw', b='appr', kind='alert', n=7, sa='l', sb='r', via=[(250, 329), (250, 429)]),
    dict(a='tgw', b='aud', kind='mgmt', label='logged', sa=('b', -40), sb=('t', -40), lpos=(355, 379)),
  ])

META = dict(
    slug='rag-and-agentic-ai',
    title='From Document Assistant to AI Agent',
    subtitle='Building RAG and agents that are accurate, permission-aware and safe',
    topic='agents',
    area='RAG and agentic AI',
    version='Version 1.0, October 2026',
    pages='Approx. 15 pages',
    minutes=25,
    audience='CIOs, IT heads, enterprise and AI architects, security, risk and process owners',
    audience_web='CIOs, IT heads, enterprise and AI architects, and security, risk and process owners',
    pdf_name='Vakratron-RAG-and-Agentic-AI.pdf',
    help_title='How we can help with RAG and AI agents',
    help_items=['<strong>RAG or agent review:</strong> two to three weeks looking at your documents, systems, permissions and real questions, with a plain view of what can be done well and safely.',
                '<strong>Evaluation set and pilot:</strong> we build the test set with your teams, tune retrieval against it and run a measured pilot with one department.',
                '<strong>Agent design:</strong> tool inventory by risk, MCP server and tool gateway design, approval points, audit and a phased rollout plan.'],
    help_links=[('Ask for a RAG or agent review', '/contact?topic=agents'), ('Agentic AI solutions', '/portfolio/agentic-ai'), ('See a worked agent design', '/deployments/agentic-ai-accounts-payable')],
    desc='A practical whitepaper on retrieval-augmented generation and AI agents: when to use RAG, fine-tuning or agents, document ingestion and chunking, hybrid search and reranking, permission-aware retrieval, evaluation sets, MCP and a tool gateway, guardrails, prompt injection, human approvals, audit, cost formulas and a 36-point checklist.',
    inside=['When RAG, fine-tuning or an agent is the right answer, and how to move up one level at a time',
            'Document preparation and chunking: where most answer quality is won or lost',
            'Hybrid search and reranking, and how to measure whether retrieval works',
            'Permission-aware retrieval so people only get answers from documents they may read',
            'Agents with MCP and a tool gateway, with actions sorted by risk and human approval',
            'Cost per answer and cost per task formulas, with a worked example',
            'A 36-point checklist covering documents, retrieval, permissions, agents and operations'],
)

SECTIONS = []
def S(id, title, html):
    SECTIONS.append(dict(id=id, title=title, html=html))

S('summary', 'Executive summary', '''
<p>A language model on its own does not know your policies, products, contracts or tickets. Retrieval-augmented generation (RAG) fixes that: before answering, the system finds the relevant passages in your documents and the model answers from them, with sources. AI agents go one step further. They plan steps, use tools in your systems and take actions, such as raising a ticket or matching an invoice.</p>
<p>Both are now practical, and both fail in predictable ways: wrong or outdated answers, confidential documents surfacing for the wrong people, and agents that do something nobody approved. This paper is for the CIOs, architects and process owners who must make them work, and for the security and risk teams who must be comfortable with them.</p>
<div class="wp-keys"><h3>Five things to take away</h3><ol>
<li><strong>Document preparation decides quality.</strong> Clean parsing of tables and scans, sensible passages and current versions matter more than the choice of model.</li>
<li><strong>Measure retrieval, not impressions.</strong> A test set of 100 to 200 real questions tells you whether the right passage was found and whether the answer stuck to it.</li>
<li><strong>Permissions are checked at search time.</strong> A RAG system that ignores document permissions is a data leak with a chat interface.</li>
<li><strong>Agents are as safe as their tools.</strong> Narrow tools behind a gateway, actions sorted by risk, and a named person approving anything that changes access, money or customer data.</li>
<li><strong>Earn autonomy in stages.</strong> Shadow first, then read and draft, then low-risk actions, then approved actions. Move on only when the numbers say so.</li>
</ol></div>''')

S('why-it-goes-wrong', 'Why document assistants and agents disappoint', '''
<div class="keep"><p>The demo is easy: load fifty documents, ask ten questions, get good answers. Production is different. There are fifty thousand documents in five systems, several versions of each policy, scanned forms, tables, and people who should not see each other&rsquo;s files. The same problems appear again and again:</p>
''' + table(['What we find', 'What happens'], [
    ['Old and new versions indexed together', 'The 2022 travel policy and the 2025 one both match. The answer mixes them, confidently.'],
    ['Tables and scans converted badly', 'PDF tables become a stream of numbers; scanned forms have no text. The facts in them are never found.'],
    ['Everything in one index, no access lists', 'Anyone can get answers drawn from HR, legal or board documents.'],
    ['Keyword-free search', 'Searching by meaning alone misses policy numbers, product codes and names.'],
    ['No test set', 'Every change is judged by whoever tried a few questions that day. Quality drifts without anyone noticing.'],
    ['Agent with broad admin rights', 'One misunderstood request or one hidden instruction in an email becomes a real change in a real system.'],
    ['No trace of what the agent did', 'When something goes wrong, nobody can say which step, tool call or input caused it.'],
]) + '</div>' + callout('In short:', 'RAG fails in the documents and the search, not in the model. Agents fail in their permissions, not in their intelligence.'))

S('concepts', 'How RAG and agents actually work', '''
<h3>RAG is two pipelines</h3>
<p>The first pipeline <strong>prepares documents</strong>: connectors collect them with their permissions and dates, parsers turn them into clean text, they are split into passages, and each passage is turned into an embedding (a list of numbers that captures meaning) and stored in a search index. The second pipeline <strong>answers questions</strong>: it searches the index, passes the best few passages to the model, and the model answers only from them, cites them, and says when the answer is not there. Most quality problems start in the first pipeline, even though users notice them in the second.</p>
<h3>Splitting documents into passages</h3>
''' + ul(['<strong>Split by structure, not by character count.</strong> Sections and paragraphs make better passages than fixed blocks that cut a sentence or a table in half.',
          '<strong>Keep passages a sensible size:</strong> typically 200 to 500 words, with a small overlap of 10 to 15 percent so a fact on a boundary is not lost.',
          '<strong>Carry context with every passage:</strong> document title, section heading, date, version, owner and access list.',
          '<strong>Treat tables, slides and scans specially:</strong> layout-aware parsing keeps tables as tables; OCR output is quality-checked and unreadable pages are flagged, not indexed silently.']) + '''
<h3>Retrieval: hybrid search and reranking</h3>
<p>Search by meaning finds passages that say the same thing in different words. Keyword search finds exact terms such as &ldquo;Policy HR-114&rdquo;, part numbers and names, which meaning-based search often misses. <strong>Hybrid search</strong> runs both and merges the results. A <strong>reranker</strong>, a second smaller model, then re-scores the top 30 to 50 results by how well each answers the question, and the best 3 to 8 go to the model. Reranking is often the single biggest quality gain. If you already run OpenSearch, Elasticsearch or PostgreSQL with an embedding search extension, you probably do not need a separate search product to start.</p>
<h3>Agents: a loop with tools</h3>
<p>An agent repeats a simple loop: decide the next step, call a tool, read the result, decide whether the task is done. Tools are functions in your systems: &ldquo;look up user&rdquo;, &ldquo;find purchase order&rdquo;, &ldquo;create ticket&rdquo;. The model only proposes tool calls; software around it decides whether they run.</p>
<h3>MCP and the tool gateway</h3>
<p>The <strong>Model Context Protocol (MCP)</strong> is an open standard for connecting AI applications to tools and data. You build one small MCP server per system, exposing its <strong>tools</strong> (actions), <strong>resources</strong> (data to read) and <strong>prompts</strong>, and any MCP-capable agent can use it within the permissions you give. A <strong>tool gateway</strong> sits between agents and MCP servers. It is the one place where identity, allowed tools, value limits, rate limits, approvals and audit are enforced, so these rules do not depend on each agent behaving well.</p>''')

S('patterns', 'RAG, fine-tuning or an agent', '''
<div class="keep"><p>It helps to think of four levels. Each adds usefulness and risk, and each needs the controls of the levels below it.</p>
''' + table(['Level', 'What it does', 'Example', 'Risk if it goes wrong', 'Key controls'], [
    ['Chat assistant', 'Answers from what the model knows', 'Drafting, general questions', 'Wrong answer', 'Approved tool, usage policy'],
    ['RAG assistant', 'Answers from your documents, with sources', 'HR, IT and product policy questions', 'Wrong answer, or a leak if permissions are ignored', 'Permissions at search time, test set, citations'],
    ['Agent with read-only tools', 'Looks things up in your systems', 'Order status, log gathering, PO lookup', 'Wrong conclusion', 'Narrow read tools, tracing'],
    ['Agent that can act', 'Changes things in real systems', 'Unlock account, raise request, post invoice', 'A wrong change in a real system', 'Risk tiers, approvals, limits, audit, kill switch'],
], 'wp-compact') + '</div>' + '''
<p>Most organisations should move down this table one level at a time, proving each before adding the next.</p>
<h3>Which technique fits the problem</h3>
''' + table(['The problem', 'Use', 'Why'], [
    ['Answers must reflect our current policies, products or cases', 'RAG', 'Facts change. Looking them up keeps answers current and shows sources.'],
    ['Answers are right but in the wrong format or tone', 'Prompting with examples, then fine-tuning', 'Fine-tuning changes behaviour, not knowledge.'],
    ['The answer is in a system, not a document', 'Agent with read-only tools', 'A tool call returns the live value; an index would be out of date.'],
    ['The task ends in a change: a ticket, a posting, a request', 'Agent with action tools and approvals', 'Only tools can act, and actions need limits.'],
    ['A narrow, high-volume classification or extraction', 'Fine-tuned small model, possibly inside an agent', 'Cheaper and more consistent than a large general model.'],
]))

S('choosing', 'Choosing a starting point', '''
<p>Five questions, asked of each candidate process, usually make the choice clear:</p>
<ol class="wp-steps">
<li><strong>Where does the answer live?</strong> In documents, use RAG. In systems of record, use read-only tools. In both, an agent that can search documents and call tools.</li>
<li><strong>Does the task end in an action?</strong> If yes, list every action and its worst realistic outcome before going further.</li>
<li><strong>Is the action reversible?</strong> Adding a ticket comment is. Paying a supplier or deleting records is not. Irreversible actions always need a person.</li>
<li><strong>Is there a natural approval point?</strong> Good agent processes already have one, such as a manager approving access or an AP clerk releasing a payment.</li>
<li><strong>Can success be measured?</strong> Resolved tickets, matched invoices, correct answers. If not, you cannot tell whether the agent helps.</li>
</ol>
<div class="keep"><h3>Good first candidates</h3>
''' + table(['Process', 'Why it suits', 'Sensible first level'], [
    ['HR and IT policy questions', 'Frequent, document-based, easy to check', 'RAG assistant with permissions'],
    ['IT service desk triage and routine fixes', 'High volume, rule-based, clear approvals', 'Read-only agent, then low-risk actions'],
    ['Invoice to purchase order matching', 'Several systems, clear rules, an existing approver', 'Agent that prepares postings for approval'],
    ['Incident support for engineers', 'Gathering logs and metrics is slow by hand', 'Read-only agent that drafts a summary'],
    ['Tender and contract checks', 'Long documents compared with a requirement list', 'RAG with a structured checklist output'],
]) + '</div>' + callout('Avoid as a first project:', 'anything customer-facing that can change money or records, and any process where nobody can say what a correct outcome looks like.', 'warn'))

S('architecture', 'Reference architecture', '''
<p>The diagram combines a RAG assistant and an agent on one platform. Documents are prepared continuously; questions and tasks are handled by one runtime that can search, reason and, through a tool gateway, act within limits.</p>
[[DIAGRAM]]
<p class="wp-caption">Numbered flows: (1) connectors collect documents with their access lists and dates, (2) clean, tagged passages and their embeddings are written to the hybrid search index, (3) an employee asks a question or starts a task under their own identity, (4) retrieval returns only passages that person may read, reranked, (5) the model answers from those passages or plans the next step, with guardrails on every prompt and response, (6) tool calls go through the gateway to MCP servers within value and rate limits, (7) high-risk actions wait for a named approver. Every step is written to the audit trail.</p>
<h3>Typical components</h3>
<p>Call the LLM through your LLM gateway, not directly. Retrieval, permissions and tools are the long-lived parts; the model will change several times.</p>
''' + table(['Layer', 'Common choices'], [
    ['Parsing and OCR', 'Docling, Unstructured, Apache Tika, OCR with quality checks'],
    ['Embeddings', 'Open multilingual embedding models (BGE or E5 families) or a hosted embedding API'],
    ['Search index and reranking', 'OpenSearch or Elasticsearch, PostgreSQL with an embedding search extension, Qdrant, Milvus; a self-hosted cross-encoder reranker'],
    ['Agent framework', 'LangGraph, Semantic Kernel, LlamaIndex, or a small amount of your own code'],
    ['Tracing and evaluation', 'Langfuse or OpenTelemetry, Ragas for retrieval scores, recorded test tasks'],
]))

S('sizing', 'Sizing and cost', '''
<div class="keep"><h3>Index size</h3>
<div class="wp-formula">Passages &asymp; documents &times; pages per document &times; words per page &divide; (words per passage &times; (1 &minus; overlap))<br>Index storage &asymp; passages &times; (embedding bytes + passage text + metadata) &times; 1.5 to 2 for index structures</div></div>
<p>For 20,000 documents averaging 12 pages of 400 words, that is 96 million words. At 300-word passages with 15 percent overlap, about 96,000,000 &divide; 255, or roughly 376,000 passages. Each needs about 4 KB for a 1,024-dimension embedding, 2 KB of text and 0.5 KB of metadata, about 6.5 KB in all, so 376,000 &times; 6.5 KB &asymp; 2.4 GB, or 4 to 5 GB with index structures. The index is small. The work is in the documents.</p>
<p>Embedding the corpus once means about 125 million tokens; on a single L40S-class GPU at a planning rate of 5,000 to 10,000 tokens a second, that is roughly 3.5 to 7 hours. Daily changes of 1 to 2 percent take minutes.</p>
<div class="keep"><h3>Cost per answer and per task</h3>
<div class="wp-formula">Cost per answer = (input tokens &times; input price + output tokens &times; output price) &divide; 1,000,000<br>Cost per agent task = steps &times; cost per step + human review rate &times; review minutes &times; staff cost per minute</div></div>
<p>A RAG answer typically sends 500 tokens of instructions, a 50-token question and 6 passages of about 400 tokens: roughly 2,950 input tokens and 300 output. At a planning price of &#8377;80 per million input and &#8377;320 per million output for a mid-tier model, that is (2,950 &times; 80 + 300 &times; 320) &divide; 1,000,000 &asymp; <strong>&#8377;0.33 per answer</strong>.</p>
<div class="keep"><h3>A worked example</h3>
<p>An organisation of 3,000 employees deploys an HR and IT policy assistant, then an IT service desk agent for routine requests such as unlocks and VPN problems.</p>
''' + table(['', 'Policy assistant (RAG)', 'Service desk agent'], [
    ['Volume', '300 daily users &times; 2 questions &times; 22 days = 13,200 answers a month', '4,000 routine tickets a month'],
    ['Model cost', '13,200 &times; &#8377;0.33 &asymp; &#8377;4,400 a month', '6 steps &times; 6,000 tokens = 36,000 tokens at &#8377;120 per million blended &asymp; &#8377;4.3 a task'],
    ['Human review', 'Weekly sample of 50 answers', '20% of tasks &times; 3 minutes &times; &#8377;5 a minute = &#8377;3 a task'],
    ['Running cost', 'Search and platform &#8377;0.4 to 0.8 lakh, plus model: about &#8377;0.5 to 0.9 lakh a month', '4,000 &times; about &#8377;7.3 &asymp; &#8377;0.3 lakh, plus platform share'],
    ['Compared with', 'If a third would have been HR or IT emails at 10 minutes each: about 730 staff hours a month', 'Manual handling at 15 minutes &times; &#8377;5 a minute = &#8377;75 a ticket, &#8377;3 lakh a month'],
    ['One-time build, planning range', '&#8377;20 to 40 lakh, mostly documents, permissions and testing', '&#8377;25 to 50 lakh, mostly tools, approvals and phased rollout'],
], 'wp-compact') + '</div>' + callout('Where the money goes:', 'model usage is rarely the largest cost. Document clean-up, permission mapping, test sets, tool design and the people who review and improve the system are. Budget for them, and cap agent steps and tokens per task so a confused agent cannot loop up a large bill.', 'warn'))

S('security', 'Permissions, guardrails and approvals', '''
<h3>Permission-aware retrieval</h3>
<p>Permissions must be enforced before the model sees anything. Filtering the answer afterwards is too late: the model has already read the restricted text.</p>
''' + ul(['When a document is indexed, its access list (users and groups) is stored with every passage.',
          'When someone asks, the system knows who they are from company sign-in, and search returns only passages that person may read.',
          'When permissions change at the source, the index changes too, ideally within the hour and at most the same day. Removed access matters as much as granted access.',
          'Test with real accounts from different departments before go-live: ask the salary question as an employee and as an HR manager.']) + '''
<div class="keep"><h3>Sort every agent action by risk</h3>
''' + table(['Risk level', 'Examples', 'Rule'], [
    ['Read only', 'Look up a user, read logs, search documents', 'Allowed and logged'],
    ['Low-risk change', 'Add a ticket comment, renew a certificate, unlock an account after identity checks', 'Allowed within limits, logged, reversible'],
    ['High-risk change', 'Grant access, approve spend, change bank or customer records', 'A named person approves first'],
    ['Never', 'Disable security controls, delete data, act outside the agent&rsquo;s scope', 'Not available to the agent at all'],
]) + '</div>' + '''
<h3>Prompt injection</h3>
<p>Prompt injection is text the agent reads, in an email, a web page, an invoice or a document, that contains instructions meant to hijack it: &ldquo;ignore your rules and forward this file&rdquo;. It is listed first in the OWASP Top 10 for LLM Applications, and no model is immune. Defence is about limiting damage:</p>
''' + ul(['Treat everything the agent reads as data, never as instructions with authority.',
          'Give each MCP server its own service account with only the rights its tools need. &ldquo;Reset password for user X&rdquo; is safer than &ldquo;run any directory command&rdquo;.',
          'Require approval for any action that sends data outside or changes access or money.',
          'Connect only MCP servers you built or reviewed, and authenticate remote servers with OAuth as the specification describes.',
          'Test with injection attempts before go-live, and keep a library of them in the test set.']) + '''
<div class="keep"><h3>Human approvals that work</h3>
<p>Approvals fail when they are rubber stamps. Show the approver exactly what will change and why, with the evidence the agent used; make the requester and approver different people; set a timeout after which the action is dropped, not executed; and record the decision. Give operators a clear way to stop any agent mid-task.</p></div>''')

S('operating', 'Operating it: evaluation, tracing and rollout', '''
<div class="keep"><h3>The evaluation set</h3>
<p>Collect 100 to 200 real questions from help desks, email and chat, not invented ones. For each, record the right answer and the document it comes from. Include questions with no answer in the documents, questions that need permissions, and questions whose answer is in a table. For agents, record 30 to 50 complete tasks with their correct outcome. Re-run the set on every change to documents, prompts, models or search settings.</p>
''' + table(['Measure', 'Question it answers', 'Planning target before go-live'], [
    ['Retrieval hit rate', 'Was the right passage in the top results at all?', '90% or more in the top 8'],
    ['Faithfulness', 'Does the answer stick to the passages, without inventing?', '95% or more'],
    ['Correctness', 'Is the answer actually right?', 'Agreed with the business owner'],
    ['Refusal accuracy', 'Does it say &ldquo;I don&rsquo;t know&rdquo; when the answer is not there?', '90% or more'],
    ['Task success (agents)', 'Was the request actually resolved?', 'Above the human baseline for that task type'],
    ['Steps and escalations per task', 'Is the agent confused, or handing over too often?', 'Stable or falling week on week'],
], 'wp-compact') + '''</div>
<div class="keep"><h3>Roll agents out in phases</h3>
''' + table(['Phase', 'What the agent may do', 'Move on when'], [
    ['1. Shadow', 'Suggests actions; people do them', 'Suggestions are right most of the time'],
    ['2. Read and draft', 'Reads systems, drafts tickets and replies for people to send', 'Drafts need few edits'],
    ['3. Low-risk actions', 'Performs reversible, low-risk changes on its own', 'No harmful mistakes over an agreed period'],
    ['4. Approved actions', 'Prepares high-risk changes for one-click approval', 'Approvers trust the preparation'],
]) + '</div>' + '''
<h3>Day-2 routines</h3>
''' + ul(['Trace every request: retrieved passages, prompts, tool calls, results and approvals, linked by one request ID.',
          'Sync changed documents daily and remove deleted ones the same day. Give every source an owner who hears when their documents produce wrong answers; fixing the document is often the fastest fix.',
          'Review blocked actions and guardrail hits weekly. Each one is either an attack, a confused agent or a rule that needs changing.',
          'Track cost per answer and per task, and alert when an agent exceeds its step or token cap.']))

S('roadmap', 'A practical roadmap', '''
<div class="keep"><p>A first RAG assistant usually reaches production in 10 to 14 weeks. A first agent takes longer, because autonomy is earned in phases.</p>
''' + table(['Stage', 'Typical duration', 'Outcome'], [
    ['1. Discover', '2 to 3 weeks', 'Real questions collected, documents and owners mapped, permissions understood, first process chosen.'],
    ['2. Ingest and index', '3 to 4 weeks', 'Connectors, parsing, passages with access lists, hybrid index, daily sync.'],
    ['3. Tune and test', '2 to 3 weeks', 'Evaluation set built, retrieval and prompts tuned against it, permission tests passed.'],
    ['4. Pilot', '4 weeks', 'One department live, quality and deflected questions measured, document gaps fixed.'],
    ['5. Agent phases', '3 to 6 months', 'Tool inventory by risk, MCP servers and tool gateway, shadow, read and draft, then actions.'],
]) + '</div>')

S('mistakes', 'Ten common mistakes', '<ol class="wp-steps">' + ''.join('<li>' + m + '</li>' for m in [
    '<strong>Indexing everything at once.</strong> Start with well-owned, current documents for one department.',
    '<strong>Keeping old versions searchable.</strong> The model cannot tell which policy is current unless you tell it.',
    '<strong>Ignoring tables and scans.</strong> Many of the facts people ask about live there.',
    '<strong>Meaning-only search.</strong> Add keyword search for codes, numbers and names.',
    '<strong>Filtering permissions after the answer.</strong> The model has already seen the restricted text.',
    '<strong>No test set.</strong> Every change becomes a matter of opinion.',
    '<strong>Giving an agent broad admin rights.</strong> Narrow tools, own service accounts, least privilege.',
    '<strong>Trusting text the agent reads.</strong> Emails and documents can carry hidden instructions.',
    '<strong>Approvals without context.</strong> Approvers who cannot see what will change will approve anything.',
    '<strong>Skipping shadow mode.</strong> A few weeks of suggestions shows where the agent goes wrong at no cost.']) + '</ol>')

CHECKLIST = [
  ('Scope and ownership', ['One process chosen, with a named business owner',
                  '100 to 200 real questions or 30 to 50 real tasks collected',
                  'Correct outcome defined and agreed for each',
                  'Baseline time and cost measured before the pilot',
                  'Every action the agent could take listed with its worst realistic outcome',
                  'An owner named for every document source']),
  ('Documents and ingestion', ['Only current versions searchable, or versions clearly marked',
                  'Layout-aware parsing for tables; OCR quality checked on scans',
                  'Passages split by structure, with headings, dates and owners attached',
                  'Changed documents synced daily; deleted documents removed the same day',
                  'Personal data in documents identified and handled under the DPDP Act',
                  'Unreadable pages flagged, not silently indexed']),
  ('Retrieval and evaluation', ['Hybrid search with keywords and embeddings',
                  'Reranking on, number of passages tuned on the test set',
                  'Multilingual embeddings tested with real Hindi or mixed-language questions where relevant',
                  'Answers cite sources; &ldquo;I don&rsquo;t know&rdquo; when the answer is not there',
                  'Retrieval hit rate, faithfulness and refusal accuracy measured on every change',
                  'Questions with no answer and permission-sensitive questions in the test set']),
  ('Permissions and data protection', ['Access lists stored with every passage',
                  'Search filtered by the user&rsquo;s identity before the model sees anything',
                  'Permission changes, including removals, reach the index the same day',
                  'Tested with real accounts from several departments',
                  'Retention set for prompts, answers and traces',
                  'No shared conversation memory between users']),
  ('Agents and tools', ['One small MCP server per system, with narrow, clearly described tools',
                  'Own service account per server with least privilege',
                  'All tool calls through a tool gateway with value and rate limits',
                  'Actions sorted into read, low-risk, high-risk and never',
                  'Named approver for high-risk actions, with full context and a timeout',
                  'Prompt injection tests in the test set',
                  'A way for operators to stop any agent mid-task']),
  ('Operations', ['Every request traced end to end with one ID',
                  'Weekly review of a sample of answers and all blocked actions',
                  'Caps on steps and tokens per agent task, with alerts',
                  'Cost per answer and per task reported monthly',
                  'Phased rollout with written criteria for moving to the next phase']),
]
n_items = sum(len(i) for _, i in CHECKLIST)
S('checklist', 'RAG and agent readiness checklist (' + str(n_items) + ' points)',
  '<p>Use this list to score your current position. Anything you cannot tick with evidence is a gap worth closing.</p><div class="wp-check">' +
  ''.join('<div class="wp-check-group"><h3>' + g + '</h3><ul>' + ''.join('<li>' + i + '</li>' for i in items) + '</ul></div>' for g, items in CHECKLIST) + '</div>')

S('glossary', 'Glossary', table(['Term', 'Meaning'], [
    ['RAG', 'Retrieval-augmented generation: finding relevant passages and giving them to the model to answer from.'],
    ['Passage (chunk)', 'A section of a document, typically 200 to 500 words, indexed and retrieved as one unit.'],
    ['Embedding', 'A list of numbers representing the meaning of a passage or question, used for meaning-based search.'],
    ['Hybrid search', 'Combining keyword search with meaning-based search and merging the results.'],
    ['Reranker', 'A second model that re-scores retrieved passages by how well they answer the question.'],
    ['Retrieval hit rate', 'The share of test questions for which the right passage was among those retrieved.'],
    ['Faithfulness', 'Whether an answer sticks to the passages it was given, without invented content.'],
    ['Agent', 'A system that plans steps and uses tools to complete a task, not only to answer.'],
    ['MCP', 'Model Context Protocol: an open standard for connecting AI applications to tools and data through small servers.'],
    ['Tool gateway', 'The single point where agent tool calls are checked against identity, limits, approvals and logged.'],
    ['Prompt injection', 'Instructions hidden in text the model reads, intended to make it ignore its rules.'],
    ['Shadow mode', 'A phase where the agent only suggests actions and people carry them out.'],
]))
