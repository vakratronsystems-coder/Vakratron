"""Whitepaper content: APIs and microservices (Oct 2026).
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
DIAGRAM = dict(w=1120, h=462,
  zones=[
    dict(x=20, y=20, w=440, h=113, title='Callers', kind='ext'),
    dict(x=480, y=20, w=620, h=113, title='Governance and operations', kind='ext'),
    dict(x=20, y=147, w=250, h=305, title='Edge', kind='sec'),
    dict(x=290, y=147, w=490, h=305, title='Domain services', kind='dc'),
    dict(x=800, y=147, w=300, h=305, title='Events and ERP', kind='cloud'),
  ],
  nodes={
    'web': N(40, 60, 210, 'Web and mobile apps', 'customers and staff', 'phone', 'slate'),
    'partners': N(280, 60, 150, 'Partners', 'keys plus mTLS', 'building', 'slate'),
    'portal': N(510, 60, 190, 'Developer portal', 'catalogue, docs, keys', 'grid', 'pink'),
    'obs': N(860, 60, 220, 'Logs, metrics, traces', 'OpenTelemetry, trace IDs', 'chart', 'green'),
    'waf': N(40, 192, 210, 'WAF', 'OWASP rules, bot filter', 'firewall', 'pink'),
    'gw': N(40, 277, 210, 'API gateway', 'auth, limits, routing', 'lb', 'pink'),
    'idp': N(40, 362, 210, 'Identity provider', 'OAuth 2.0 and OIDC', 'key', 'pink'),
    'orders': N(305, 192, 215, 'Orders service', 'REST, own database', 'server', 'blue'),
    'pay': N(550, 192, 215, 'Payments service', 'idempotency keys', 'money', 'blue'),
    'inv': N(305, 277, 215, 'Inventory service', 'gRPC, own database', 'server', 'blue'),
    'cust': N(550, 277, 215, 'Customer service', 'syncs with ERP', 'person', 'blue'),
    'db': N(305, 362, 215, 'Service databases', 'one per service, not shared', 'storage', 'green'),
    'adapter': N(550, 362, 215, 'ERP adapter', 'anti-corruption layer', 'link', 'violet'),
    'broker': N(820, 192, 265, 'Event broker', 'Kafka topics by domain', 'queue', 'amber'),
    'cons': N(820, 277, 265, 'Consumers', 'billing, alerts, analytics', 'flow', 'amber'),
    'erp': N(820, 362, 265, 'Legacy ERP', 'SOAP and batch files', 'building', 'slate'),
  },
  flows=[
    dict(a='web', b='waf', kind='traffic', label='HTTPS', lpos=(145, 140)),
    dict(a='partners', b='waf', kind='traffic', sa=('b', 0), via=[(355, 140), (195, 140)], sb=('t', 50), label='mTLS', lpos=(275, 140)),
    dict(a='partners', b='portal', kind='control', n=1),
    dict(a='waf', b='gw', kind='traffic', n=2),
    dict(a='gw', b='idp', kind='control', label='validate token'),
    dict(a='gw', b='orders', kind='traffic', sa=('r', -14), via=[(280, 292), (280, 221)], sb='l'),
    dict(a='gw', b='inv', kind='traffic', sa=('r', 0), sb=('l', 0)),
    dict(a='orders', b='pay', kind='control', n=3),
    dict(a='pay', b='broker', kind='data', n=4),
    dict(a='broker', b='cons', kind='data', n=5),
    dict(a='cust', b='adapter', kind='control'),
    dict(a='adapter', b='erp', kind='batch', n=6),
    dict(a='broker', b='obs', kind='mgmt', sa=('t', 99.5), sb=('b', 82), label='lag, traces', lpos=(1052, 140)),
  ])

META = dict(
    slug='api-microservices-architecture',
    title='APIs and Microservices Without the Distributed Monolith',
    subtitle='Designing APIs, choosing between a modular monolith and microservices, and running integrations safely',
    topic='api',
    area='APIs and microservices',
    version='Version 1.0, October 2026',
    pages='Approx. 15 pages',
    minutes=25,
    audience='CIOs, enterprise and solution architects, engineering managers, integration and security teams',
    audience_web='CIOs, enterprise and solution architects, engineering managers, and integration and security teams',
    pdf_name='Vakratron-APIs-and-Microservices.pdf',
    help_title='How we can help with APIs and microservices',
    help_items=['<strong>Integration review:</strong> a map of what talks to what, where it breaks and what to fix first, in two to three weeks.',
                '<strong>Architecture and API design:</strong> service boundaries, gateway and event design, API guidelines, security controls and a cost view.',
                '<strong>Partner API launch:</strong> onboarding, keys and mTLS, rate limits, a developer portal and the monitoring to run it.'],
    help_links=[('Book an integration review', '/advisory#review'), ('APIs and microservices', '/portfolio/api-microservices'), ('See an AI integration with ERP', '/deployments/agentic-ai-accounts-payable')],
    desc='A practical whitepaper on APIs and microservices: monolith, modular monolith or microservices, API design and versioning, gateway patterns, event-driven integration, resilience patterns, API security, partner APIs, observability, governance, and a 36-point readiness checklist.',
    inside=['How to choose between a monolith, a modular monolith and microservices',
            'API design and versioning rules that keep callers working',
            'When to call an API and when to publish an event',
            'Timeouts, retries, circuit breakers and idempotency, explained simply',
            'Availability and event sizing formulas with a worked example',
            'API security based on the OWASP API Top 10, and opening APIs to partners',
            'A 36-point readiness checklist for integration and API programmes'],
)

SECTIONS = []
def S(id, title, html):
    SECTIONS.append(dict(id=id, title=title, html=html))

S('summary', 'Executive summary', '''
<p>Most integration problems are not about technology. They come from point-to-point connections nobody documented, services split before anyone knew where the boundaries were, and one slow system dragging others down with it. Microservices promised independent teams and faster releases. Many organisations got the opposite: a distributed monolith, where every change still touches several services, but now each call can fail over the network.</p>
<p>This paper is for the people who shape how systems talk to each other: CIOs, enterprise and solution architects, engineering managers, and the integration and security teams who keep it running. It sets out how to choose the right structure, design APIs that last, and make integrations safe to operate.</p>
<div class="wp-keys"><h3>Five things to take away</h3><ol>
<li><strong>Start with a modular monolith.</strong> Split a service out only when teams block each other, or one part needs very different scale or release pace. Microservices solve an organisational problem, not a technical one.</li>
<li><strong>Design the contract first.</strong> Write the API in OpenAPI before the code, and never break existing callers. Add fields freely; remove them only in a new version, with notice.</li>
<li><strong>Use events for news, calls for questions.</strong> When several systems react to the same thing, publish an event. Long chains of synchronous calls multiply failure.</li>
<li><strong>Make failure small.</strong> Every call has a timeout, retries are limited and idempotent, and circuit breakers stop one slow service from taking down the rest.</li>
<li><strong>Know every API you expose.</strong> Most API breaches are missing checks on APIs nobody remembered. Keep a catalogue, put a gateway in front, and check object ownership in every service.</li>
</ol></div>''')

S('why-it-goes-wrong', 'Why integration gets painful', '''
<p>Integration estates grow one project at a time. Each connection made sense when it was built; together they form a web that nobody can draw from memory. When we review integration estates, the technology varies but the problems repeat:</p>
''' + table(['What we find', 'What it leads to'], [
    ['Spaghetti connections', 'Every system talks directly to every other. Change one, and you find out what breaks in production.'],
    ['Microservices too early', 'A small team split one application into twenty services and got all of the complexity with none of the benefit.'],
    ['Shared databases', 'Services read and write each other&rsquo;s tables. No service can change its schema without a coordinated release.'],
    ['Long synchronous chains', 'One user request passes through six services. Any one of them being slow makes the whole request slow.'],
    ['No timeouts', 'A service waits forever on a slow dependency, threads pile up, and the failure spreads to everything that calls it.'],
    ['Unknown APIs', 'Old versions and test endpoints stay open on the internet, with no owner and no monitoring.'],
    ['Breaking changes', 'A field is renamed, partners&rsquo; integrations fail overnight, and nobody knew who was calling.'],
]) + callout('The distributed monolith:', 'services that must be deployed together, share data, and call each other in long chains. It has the coupling of a monolith and the failure modes of a distributed system. Avoiding it is the main aim of this paper.'))

S('concepts', 'Core concepts: boundaries, contracts and versions', '''
<h3>Boundaries come from the business</h3>
<p>A good service boundary follows a business capability with its own data and its own language: orders, payments, inventory, customers. Domain-driven design calls this a bounded context. Inside a boundary, things change together and can share a database. Across a boundary, they talk only through a published contract. If two parts of a system always change together, they belong in the same boundary, however large it looks.</p>
<p>Boundaries matter whether you run one deployable unit or fifty. A modular monolith uses the same boundaries as microservices, enforced as modules with separate schemas inside one application. That keeps the option to split later without paying for it now.</p>
<div class="keep"><h3>Contract-first API design</h3>
<p>A good API is one a developer can use correctly from its documentation alone, and one you can change without breaking the people who depend on it.</p>
''' + table(['Rule', 'Why it matters'], [
    ['Write the contract first, in OpenAPI (AsyncAPI for events)', 'Callers and providers agree before code exists; documentation, mocks and tests come from the same file.'],
    ['Model resources, not database tables', 'The API can stay stable while the storage behind it changes.'],
    ['One error format everywhere', 'A clear code, message and correlation ID; callers handle errors the same way for every API.'],
    ['Idempotency keys on payments and orders', 'A retried request never charges or ships twice.'],
    ['Pagination and filters on every list', 'No endpoint returns everything at once, so performance stays predictable.'],
    ['Validate every request against the contract', 'Bad input is rejected at the edge, not deep inside a service.'],
]) + '''</div>
<h3>Versioning without breaking callers</h3>
<p>Adding an optional field or a new endpoint is not a breaking change. Removing or renaming a field, changing a type, or tightening validation is. Avoid breaking changes; when one is unavoidable, publish a new major version (for example <code>/v2/</code>), run both for an agreed period, usually six to twelve months for partners, tell callers early, and use gateway logs to see exactly who still calls the old version before you retire it.</p>
<h3>REST, GraphQL or gRPC</h3>
''' + ul(['<strong>REST</strong> for most public and partner APIs: widely understood, easy to cache and secure.',
          '<strong>GraphQL</strong> when many front-ends need different shapes of the same data, behind a well-governed schema.',
          '<strong>gRPC</strong> for fast internal service-to-service calls with strict contracts.']))

S('options', 'Monolith, modular monolith or microservices', '''
<p>Microservices solve a specific problem: many teams needing to change and release parts of a system independently. If you do not have that problem, they mostly add cost. The honest comparison:</p>
''' + table(['', 'Traditional monolith', 'Modular monolith', 'Microservices'], [
    ['Best for', 'Small, stable applications', 'One to a few teams; a product still taking shape', 'Many teams; parts with very different scale or release needs'],
    ['Deployment', 'One unit', 'One unit, built from clear modules', 'Many units; needs a platform and automation'],
    ['Data', 'One shared schema', 'One database, a schema per module', 'A database per service; harder consistency'],
    ['Failure', 'In-process calls rarely fail', 'In-process calls rarely fail', 'Every network call can fail and must be handled'],
    ['Team independence', 'Low', 'Moderate', 'High, if boundaries are right'],
    ['Running cost', 'Lowest', 'Low', 'Higher: platform, monitoring, gateway, broker, people'],
    ['Main risk', 'Becomes a tangle', 'Module rules not enforced', 'The distributed monolith'],
], 'wp-compact') + '''
<h3>Signs you should split a service out</h3>
''' + ul(['Teams wait on each other to release, every week.',
          'One part needs to scale very differently from the rest, such as search or tracking.',
          'One part changes daily while the rest is stable.',
          'A clear business boundary exists, with its own data and its own owner.']) + '''
<h3>Signs you split too early</h3>
''' + ul(['Every feature needs changes in several services at once.',
          'Services share a database, or must be deployed together.',
          'You cannot test anything without starting everything.']))

S('decide', 'A decision framework', '''
<p>Three decisions shape most integration architectures. Make them per domain, not once for the whole organisation.</p>
<ol class="wp-steps">
<li><strong>How many deployable units?</strong> Count the teams that need to release independently. One team rarely needs more than one or two services. Split along business boundaries, one service per team at most to begin with.</li>
<li><strong>Call or event?</strong> If the caller needs an answer to continue, call an API. If the sender is announcing that something happened, publish an event and let others react.</li>
<li><strong>Change or wrap the legacy system?</strong> Put an API or adapter in front first. Rewrite only what blocks the business, one piece at a time.</li>
</ol>
''' + table(['Situation', 'Use', 'Example'], [
    ['Caller needs an answer to continue', 'API call', 'Check stock before confirming an order'],
    ['Several systems react to the same thing', 'Event', '&ldquo;Order placed&rdquo; updates warehouse, billing and notifications'],
    ['The receiver may be offline for a while', 'Event or queue', 'A branch system that syncs every few minutes'],
    ['Very high volume of updates', 'Event stream', 'Tracking pings from thousands of vehicles'],
    ['Long-running work with steps', 'Queue plus status API', 'Document processing or loan approval'],
]) + '''
<h3>Modernising a legacy system: the strangler pattern</h3>
<p>Put a gateway or API in front of the legacy system. Build new capabilities as separate services behind the same front. Move existing features out one at a time, routing traffic to the new version, and retire the old parts as they empty out. Callers never notice, and every step can be rolled back. Big-bang rewrites of core systems fail far more often than they succeed.</p>''')

S('architecture', 'Reference architecture', '''
<p>The diagram shows a typical shape once a few domains have their own services. Callers only ever reach the gateway. Services call each other sparingly and with timeouts, share news through events, and reach legacy systems only through adapters.</p>
[[DIAGRAM]]
<p class="wp-caption">Numbered flows: (1) partners register in the developer portal and receive keys and certificates, (2) all external traffic passes the WAF, then the gateway checks the token with the identity provider, applies rate limits and routes to the right service and version, (3) orders calls payments with a timeout, a limited retry carrying an idempotency key, and a circuit breaker, (4) payments publishes &ldquo;payment received&rdquo; through an outbox, (5) billing, alerts and analytics react independently, (6) the legacy ERP is reached only through an adapter that translates its model.</p>
<h3>Gateway patterns</h3>
''' + table(['Pattern', 'What it does', 'Use when'], [
    ['Edge gateway', 'One entry point for authentication, rate limits, routing and logging', 'Always, for anything exposed outside'],
    ['Backend for front-end', 'A thin API per channel (mobile, web) that shapes data for it', 'Channels need very different responses'],
    ['Partner gateway', 'Separate keys, mTLS, quotas and a portal for partners', 'You open APIs to third parties'],
    ['Service mesh', 'mTLS, retries and traffic control between services, outside the code', 'Many services, and a platform team to run it'],
], 'wp-compact') + '''
<p>Keep business logic out of the gateway. It should check, limit, route and record. Gateways that start transforming data and orchestrating calls become a new monolith that only one team understands. Common choices are Kong, Apache APISIX, a cloud API gateway, or a Kubernetes Gateway API implementation.</p>
<h3>Resilience patterns</h3>
''' + table(['Pattern', 'What it prevents', 'Rule of thumb'], [
    ['Timeout on every call', 'Threads waiting forever on a slow dependency', 'Set from the dependency&rsquo;s p99 latency; always shorter than the caller&rsquo;s own timeout'],
    ['Retry with backoff and jitter', 'Failing on brief network blips', 'Two retries at most, only on safe errors, and only at one layer'],
    ['Idempotency key', 'Double charges or duplicate orders when a retry succeeds twice', 'Client sends a unique key; the service stores and replays the first result'],
    ['Circuit breaker', 'Hammering a service that is already down', 'Open after a run of failures, fail fast, test again after a pause'],
    ['Bulkhead', 'One slow dependency using up all threads or connections', 'Separate pools per dependency'],
    ['Fallback', 'A whole page failing because one part did', 'Show cached or partial data where the business accepts it'],
], 'wp-compact') + '''
<div class="keep"><h3>Events, done reliably</h3>
<p>Kafka suits high-volume streams that several consumers read and may replay; RabbitMQ suits work queues and routing; NATS suits lightweight messaging. Whichever you use, five practices matter more than the product:</p></div>
''' + ul(['<strong>Outbox:</strong> save the change and the event in the same database transaction, then publish, so the database and the events never disagree.',
          '<strong>Idempotent consumers:</strong> messages can arrive twice; processing one twice must be harmless.',
          '<strong>Schemas:</strong> describe events with a schema registry (Avro or JSON Schema) and evolve them without breaking consumers.',
          '<strong>Dead-letter queues:</strong> messages that keep failing go aside for a person to inspect, instead of blocking the rest.',
          '<strong>Ordering:</strong> decide where order matters, and partition by the right key, such as order ID.']))

S('sizing', 'Sizing and cost', '''
<div class="keep"><h3>Availability of a call chain</h3>
<p>When a request depends on several services in sequence, their availabilities multiply:</p>
<div class="wp-formula">End-to-end availability = A1 &times; A2 &times; &hellip; &times; An</div>
<div class="wp-formula">Calls reaching the deepest service = (1 + retries per layer), raised to the power of the number of retrying layers</div></div>
<p>Six services at 99.9 percent each give 0.999<sup>6</sup> &asymp; 99.4 percent, or about 52 hours of failed requests a year instead of nine. And if three layers each retry twice, one user click can become 3 &times; 3 &times; 3 = 27 calls to the deepest service, exactly when it is struggling. Retry at one layer only.</p>
<h3>A worked example: placing an order</h3>
<p>An order passes through orders, payments, inventory, customer and notifications, each running at 99.9 percent availability.</p>
''' + table(['', 'Design A: all synchronous calls', 'Design B: two calls, the rest as events'], [
    ['Services the user waits on', '5', '2 (orders and payments)'],
    ['End-to-end availability', '0.999<sup>5</sup> &asymp; 99.5%', '0.999<sup>2</sup> &asymp; 99.8%'],
    ['Failed-order time per year', '8,760 &times; 0.005 &asymp; 44 hours', '8,760 &times; 0.002 &asymp; 18 hours'],
    ['If notifications is down', 'Orders fail', 'Orders succeed; notifications catch up later'],
    ['Response time', 'Sum of five calls', 'Sum of two calls'],
], 'wp-compact') + '''
<div class="keep"><h3>Sizing an event stream</h3>
<div class="wp-formula">Partitions &ge; peak messages per second &divide; messages per second one consumer can process</div>
<div class="wp-formula">Storage per day = message rate &times; message size &times; 86,400 seconds; total = per day &times; retention days &times; replicas</div></div>
<p>A logistics company tracks 20,000 vehicles that each send a ping every 30 seconds: about 670 messages a second, or roughly 1,340 at peak. If one consumer handles 200 a second, it needs at least 1,340 &divide; 200 &asymp; 7 partitions; plan 12 to 16 to allow growth, because partitions are hard to add later without reordering keys. At 1 KB per message, that is about 115 GB a day; seven days of retention with three replicas needs 115 &times; 7 &times; 3 &asymp; 2.4 TB.</p>
<h3>What microservices add to running cost</h3>
''' + table(['Item', 'Planning range per year'], [
    ['Container platform for 15 to 30 services, production and non-production', '&#8377;40 lakh to &#8377;1 crore in infrastructure'],
    ['Event broker cluster (three nodes) and schema registry', '&#8377;10 to &#8377;25 lakh'],
    ['Gateway and developer portal: open source, or commercial licences', '&#8377;0 to &#8377;60 lakh'],
    ['Observability storage for logs, metrics and traces', '&#8377;8 to &#8377;25 lakh'],
    ['Platform and SRE people: 2 to 4 engineers, fully loaded', '&#8377;50 lakh to &#8377;1.6 crore'],
], 'wp-compact') + '''
<p>These are planning ranges, not quotes. A well-built modular monolith for the same product might run on a few VMs and one database cluster for a small fraction of this. The extra spend is justified when it buys real team independence; if it does not, it is waste.</p>''')

S('security', 'Security and governance', '''
<p>APIs expose business logic and data directly. The most common API breaches are not clever attacks. They are missing checks, such as letting a logged-in user read someone else&rsquo;s record by changing an ID in the URL. The OWASP API Security Top 10 (2023) is a good working list:</p>
''' + table(['Risk', 'What it looks like', 'Control'], [
    ['Broken object-level authorisation', 'Change /orders/1001 to /orders/1002 and see another customer&rsquo;s order', 'Check ownership of every object in the service, not only at the gateway'],
    ['Broken authentication', 'Weak tokens, keys in URLs, no expiry', 'OAuth 2.0 and OIDC, short-lived tokens, mTLS for partners'],
    ['Excessive data exposure', 'The API returns full records and the app hides fields', 'Return only the fields the caller needs'],
    ['Unrestricted resource use', 'Scraping, brute force, sudden cost spikes', 'Rate limits and quotas per caller at the gateway'],
    ['Function-level authorisation', 'A normal user can call admin endpoints', 'Separate admin APIs; check roles on every endpoint'],
    ['Improper inventory', 'Old versions and test APIs still exposed', 'An API catalogue, and retire old versions on a schedule'],
], 'wp-compact') + '''
<h3>Identity and transport</h3>
''' + ul(['Users and apps get tokens from one identity provider using OAuth 2.0 and OIDC; tokens live minutes, not days.',
          'Machine-to-machine calls use the client credentials flow with narrow scopes, never a shared admin key.',
          'Partners use mTLS as well as tokens, so a leaked key alone is not enough.',
          'Inside the platform, encrypt service-to-service traffic with mTLS, through a mesh or the platform&rsquo;s network layer.',
          'Keep secrets and keys out of code and front-end apps; load them from a vault at run time.']) + '''
<h3>Opening APIs to partners</h3>
<p>Partner APIs are a product. Give partners a portal with documentation, a sandbox with realistic test data, self-service keys, published rate limits and a status page. Agree a deprecation policy in the contract. Measure usage per partner, because that is what tells you which versions you can retire and which partners need help.</p>
<h3>Governance that teams accept</h3>
<p>Publish short API guidelines and enforce them automatically: lint OpenAPI files in CI, run security tests before release, and register every API in the catalogue with an owner. Log every call with caller identity and alert on unusual patterns. For regulated sectors, RBI, SEBI and IRDAI expectations on access control and audit trails, CERT-In 6-hour incident reporting and the DPDP Act all assume you know which APIs touch personal data and who called them.</p>''')

S('operating', 'Operating it: day 2', '''
<h3>Observability across services</h3>
<p>In a distributed system, a single request touches several services, so logs alone are not enough. Give every request a trace ID at the gateway and pass it through every call and event, using OpenTelemetry. Collect three views for every service: the rate of requests, the rate of errors and the duration (the RED method), and for every event consumer, its lag. When something breaks, the trace shows which hop was slow, not just that the page was.</p>
<h3>Service levels and error budgets</h3>
<p>Set a service level objective per API that matters to users, for example 99.9 percent of requests succeed within 300 milliseconds over 30 days. The gap to 100 percent is the error budget: about 43 minutes a month. When a team has spent it, reliability work comes before new features. This turns reliability arguments into numbers.</p>
<h3>Release and change</h3>
''' + ul(['Deploy each service independently through its own pipeline; if two must always deploy together, merge them or fix the contract.',
          'Run consumer-driven contract tests (for example Pact) in CI, so a provider change that breaks a caller fails the build.',
          'Release behind feature flags or with canary traffic for high-risk changes.',
          'Track who calls each API version, and retire old versions on the published schedule.',
          'Review dead-letter queues daily; a growing queue is a silent outage.']) + '''
<h3>Ownership</h3>
<p>Every API and every event topic has a named owning team, recorded in the catalogue. The team that builds a service runs it and carries its alerts. A small central platform or integration team owns the gateway, broker, portal and guidelines, and reviews new APIs, but does not build every integration. Central teams that build everything become the bottleneck the architecture was meant to remove.</p>''')

S('roadmap', 'A practical roadmap', '''
<p>Integration improvement works best in steps that each deliver something, without a big-bang rewrite.</p>
''' + table(['Stage', 'Typical duration', 'Outcome'], [
    ['1. Map', '3 to 4 weeks', 'Every integration, its owner, protocol and what breaks if it stops. Exposed APIs found and listed.'],
    ['2. Decide the shape', '2 to 4 weeks', 'Domains and boundaries, where events fit, what stays as it is, API guidelines drafted.'],
    ['3. Front door', '4 to 8 weeks', 'Gateway, identity, rate limits, catalogue and portal in front of existing APIs. Unused endpoints closed.'],
    ['4. Make failure safe', '4 to 6 weeks', 'Timeouts, retries, circuit breakers and idempotency on critical paths; tracing end to end.'],
    ['5. Change gradually', 'Ongoing, by quarter', 'Worst point-to-point links replaced first; new features as services or modules; legacy strangled piece by piece.'],
    ['6. Hand over', '4 weeks, overlapping', 'Guidelines, templates, review practice and runbooks owned by your teams.'],
]))

S('mistakes', 'Ten common mistakes', '<ol class="wp-steps">' + ''.join('<li>' + m + '</li>' for m in [
    '<strong>Splitting before the boundaries are clear.</strong> The result is a distributed monolith that is harder to change than the original.',
    '<strong>Sharing a database between services.</strong> No service can change its own data without a coordinated release.',
    '<strong>Long chains of synchronous calls.</strong> Availability falls and latency adds up with every hop.',
    '<strong>Calls without timeouts.</strong> One slow dependency takes down everything upstream.',
    '<strong>Retrying at every layer.</strong> A small fault becomes a flood of traffic at the worst moment.',
    '<strong>Payments and orders without idempotency keys.</strong> A retry charges or ships twice.',
    '<strong>Breaking changes without a new version.</strong> Partners find out in production.',
    '<strong>Authorisation only at the gateway.</strong> Services trust any request that gets past it, and object-level checks are missed.',
    '<strong>Business logic in the gateway or the bus.</strong> A new central monolith that one team controls.',
    '<strong>No catalogue and no owners.</strong> Forgotten APIs stay open and unmonitored for years.']) + '</ol>')

CHECKLIST = [
  ('Architecture and boundaries', ['Domains and boundaries mapped to business capabilities, each with an owner',
                  'A written reason for every service split, tied to team or scale needs',
                  'No database shared between services or modules',
                  'User-facing requests wait on no more than two or three synchronous calls',
                  'Events used where several systems react to the same change',
                  'Legacy systems reached only through adapters or the gateway']),
  ('API design', ['Every API described in OpenAPI or AsyncAPI before build',
                  'One error format with correlation IDs across all APIs',
                  'Idempotency keys on payment, order and other write operations that matter',
                  'Pagination and filtering on every list endpoint',
                  'Versioning and deprecation policy published, with notice periods',
                  'Consumer-driven contract tests running in CI']),
  ('Resilience', ['Timeout on every outbound call, shorter than the caller&rsquo;s timeout',
                  'Retries limited, with backoff and jitter, at one layer only',
                  'Circuit breakers on calls to critical dependencies',
                  'Separate connection pools for each important dependency',
                  'Outbox pattern used where a database change must produce an event',
                  'Dead-letter queues monitored and reviewed daily']),
  ('Security', ['All external traffic through a WAF and the API gateway',
                  'OAuth 2.0 and OIDC with short-lived tokens; no keys in URLs',
                  'mTLS for partner and service-to-service traffic',
                  'Object-level authorisation checked inside every service',
                  'Rate limits and quotas per caller',
                  'APIs tested against the OWASP API Top 10 before release',
                  'Every call logged with caller identity and retained for audit']),
  ('Governance and partners', ['API catalogue with an owner for every API and event topic',
                  'Old versions and test endpoints found and retired on schedule',
                  'Developer portal with documentation, sandbox and self-service keys',
                  'Usage tracked per partner and per API version',
                  'API guidelines enforced by linting in CI']),
  ('Operations', ['Trace ID created at the gateway and passed through every call and event',
                  'Request rate, error rate and duration dashboards for every service',
                  'Consumer lag monitored for every event topic',
                  'Service level objectives and error budgets set for key APIs',
                  'Runbook for each critical integration, including how to replay events',
                  'Each service deployable on its own, with rollback practised']),
]
n_items = sum(len(i) for _, i in CHECKLIST)
S('checklist', 'API and integration readiness checklist (' + str(n_items) + ' points)',
  '<p>Use this list to score your current integration estate or a planned programme. Anything you cannot tick with evidence is a gap worth closing.</p><div class="wp-check">' +
  ''.join('<div class="wp-check-group"><h3>' + g + '</h3><ul>' + ''.join('<li>' + i + '</li>' for i in items) + '</ul></div>' for g, items in CHECKLIST) + '</div>')

S('glossary', 'Glossary', table(['Term', 'Meaning'], [
    ['Bounded context', 'A part of the business with its own data, rules and language; a natural service or module boundary.'],
    ['Modular monolith', 'One deployable application built from strictly separated modules, each owning its data.'],
    ['Distributed monolith', 'Services that must change and deploy together, with the downsides of both styles.'],
    ['Idempotency', 'Doing the same operation twice has the same effect as doing it once.'],
    ['Circuit breaker', 'A guard that stops calls to a failing dependency for a while, so callers fail fast.'],
    ['Outbox pattern', 'Writing an event to the same database transaction as the change, then publishing it.'],
    ['Strangler pattern', 'Replacing a legacy system gradually by routing features to new services behind one front.'],
    ['mTLS', 'Mutual TLS: both sides of a connection prove their identity with certificates.'],
    ['Error budget', 'The amount of failure a service level objective allows over a period.'],
]))
