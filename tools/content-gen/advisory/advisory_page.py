"""/advisory: one page replacing the 12 STA pages (Oct 2026).
Run from tools/content-gen/advisory/."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'dr'))
from tpl import page, crumb

def ul(items):
    return '<ul class="vk-av-list">' + ''.join('<li>' + i + '</li>' for i in items) + '</ul>'

def steps(items):
    return '<ol class="vk-av-steps">' + ''.join('<li><span class="w">' + w + '</span><span>' + t + '</span></li>' for w, t in items) + '</ol>'

OFFERS = [
  dict(id='review', cta='Ask for an architecture review', icon='fa-magnifying-glass-chart', topic='review',
    title='Architecture review',
    line='An independent second opinion on a design, a vendor proposal or a platform that is already running.',
    chips=[('Duration', '2 to 3 weeks'), ('Your team&rsquo;s time', 'About 6 hours in total'), ('Format', 'Remote, one optional on-site day')],
    fits=['A vendor or system integrator has sent a proposal and you want to know if the sizing and the price are right before you sign.',
          'A platform is live but slow, expensive or fragile, and nobody can say exactly why.',
          'Your board or auditors want an independent view of a design before approving the budget.'],
    looks=['Sizing against the real workload: compute, storage, network and GPU, not just the bill of quantities',
           'Single points of failure and what actually happens when each part fails',
           'Recovery: whether the promised RTO and RPO are achievable with this design',
           'Security architecture: segmentation, identity, privileged access, logging',
           'Licensing and running cost over five years, not just the purchase price',
           'Operations: monitoring, upgrades, and whether your team can run it'],
    runs=[('Week 1', 'We read the documents and run two short workshops with your architects and the vendor if needed.'),
          ('Week 2', 'We check the design against workload data, walk through failure scenarios and model the cost.'),
          ('Week 3', 'We walk you through the findings and answer questions from your team and leadership.')],
    gets=['Findings report with an executive summary a non-technical reader can follow',
          'Risk table: every issue rated by impact and effort, with what to fix first',
          'Questions to put back to the vendor before you sign',
          'Revised sizing or BoQ direction where the original is off'],
    needs=['The proposal, HLD or LLD, and any sizing sheets', 'Inventory or monitoring exports for the workloads involved', 'Two or three people for short workshops']),
  dict(id='assessment', cta='Ask for a technology assessment', icon='fa-clipboard-check', topic='review',
    title='Technology assessment',
    line='A full health check of your infrastructure estate, with a practical roadmap for the next 12 to 18 months.',
    chips=[('Duration', '4 to 6 weeks'), ('Your team&rsquo;s time', '6 to 10 interviews of an hour each'), ('Format', 'Mix of on-site and remote')],
    fits=['You are planning next year&rsquo;s infrastructure budget and want it based on facts.',
          'A new CIO or IT head wants an honest baseline of what they have inherited.',
          'You know some things need to change (an ageing data centre, rising cloud bills, untested DR) but not in what order.'],
    looks=['Data centre, compute and virtualisation, including hardware nearing end of support',
           'Storage, backup and the last time a restore was actually tested',
           'Network and connectivity between sites, offices and cloud',
           'Cloud usage and spend: what runs where, and what it costs',
           'Disaster recovery readiness for each critical application',
           'Security controls and operations maturity',
           'Readiness for AI workloads: data, GPUs, skills and governance'],
    runs=[('Weeks 1 to 2', 'Discovery: tool exports, inventory, monitoring data and interviews with the people who run each area.'),
          ('Weeks 3 to 4', 'Analysis: each area scored for maturity, gaps listed, risks rated, quick wins identified.'),
          ('Weeks 5 to 6', 'Roadmap: options with cost ranges, sequencing and a review session with leadership.')],
    gets=['Current-state report covering every area above',
          'A maturity score per area, so progress can be measured next year',
          'Gap and risk list, ranked',
          '12 to 18 month roadmap with cost ranges and dependencies',
          'Quick wins that can be done in the first 90 days'],
    needs=['A sponsor who can open doors internally', 'Read-only exports from inventory, monitoring and backup tools', 'Interviews with infrastructure, application, security and finance owners']),
  dict(id='discovery', cta='Plan a discovery workshop', icon='fa-users-gear', topic='other',
    title='Discovery workshop',
    line='A short, structured workshop to turn an idea into a clear scope before you go to vendors.',
    chips=[('Duration', '2 to 3 days, plus a week to write up'), ('Your team&rsquo;s time', 'The workshop days'), ('Format', 'On-site preferred')],
    fits=['You want to start something new, such as a private cloud, a DR site or an AI platform, but the requirements are still loose.',
          'Different teams want different things and need one agreed direction.',
          'You need a realistic budget range before writing a tender or asking for quotes.'],
    looks=['Business goals and what success looks like in numbers',
           'The applications and data involved, and how they depend on each other',
           'Non-functional needs: performance, availability, RTO and RPO, compliance, data location',
           'Constraints: budget, timelines, skills, existing contracts',
           'Two or three realistic options, with their trade-offs'],
    runs=[('Day 1', 'Goals, constraints and the current landscape, with business and IT owners in the room.'),
          ('Day 2', 'Requirements and options, worked through with architects, security and operations.'),
          ('Day 3 and write-up', 'Agree the direction, then we write it up within a week.')],
    gets=['Workshop summary with decisions and open questions',
          'Requirements list, functional and non-functional',
          'First high-level design direction with the options compared',
          'A budget range and a sensible next step'],
    needs=['Business owner, IT head, application owners, security and finance for the relevant sessions', 'Any existing documents, even rough ones']),
  dict(id='tender', cta='Discuss tender support', icon='fa-file-signature', topic='tender',
    title='Tender and RFP support',
    line='Help to write a vendor-neutral specification and to evaluate the responses fairly.',
    chips=[('Duration', 'Depends on the tender'), ('Your team&rsquo;s time', 'Review cycles at each stage'), ('Format', 'Remote, with meetings as needed')],
    fits=['A government department or PSU needs a technical specification for GeM or an open tender.',
          'An enterprise is running an RFP and wants the requirements and scoring to be fair and defensible.',
          'Bids have come in and you need an independent technical comparison.'],
    looks=['Requirements written as outcomes, not as one vendor&rsquo;s datasheet',
           'Eligibility and technical criteria that do not exclude capable bidders without reason',
           'A bill of quantities that matches the workload',
           'Scoring that can be defended in a pre-bid meeting or an audit'],
    runs=[('Before release', 'Specification, BoQ, eligibility and evaluation criteria drafted and reviewed with you.'),
          ('Pre-bid', 'Help with responses to bidder queries and any corrigendum.'),
          ('Evaluation', 'Technical comparison of bids against the published criteria.')],
    gets=['Vendor-neutral technical specification', 'Bill of quantities with sizing workings', 'Evaluation criteria and scoring sheet', 'Technical comparison report on the bids received'],
    needs=['The purpose and budget of the procurement', 'Any earlier specifications or reference documents', 'A named officer for review cycles']),
]

CHOOSER = [
    ['A vendor proposal is on your desk and you need to decide soon', '<a href="#review">Architecture review</a>'],
    ['You want a clear picture of your whole estate and a plan for next year', '<a href="#assessment">Technology assessment</a>'],
    ['You have an idea for a new platform but the scope is still loose', '<a href="#discovery">Discovery workshop</a>'],
    ['You need to buy through a tender and want a fair, defensible specification', '<a href="#tender">Tender and RFP support</a>'],
]

FAQ = [
    ('How is an engagement priced?', 'Each one is a fixed fee for a fixed scope, agreed before work starts. The fee depends mainly on the size of the estate or design involved. A 30-minute call is usually enough for us to quote.'),
    ('Do you need access to our systems?', 'No admin access is needed. We work from documents, read-only exports from your tools and conversations with your team. Anything sensitive can be shared after an NDA is signed.'),
    ('Will you push us towards a particular vendor?', 'No. Recommendations are based on your workload and constraints. Where more than one product would work, we say so and compare them. If we have a commercial relationship with any vendor we mention, we tell you upfront.'),
    ('What happens after the engagement?', 'The report is yours to use however you like, including with another partner. If you want, we can stay involved to oversee the build, but there is no obligation.'),
    ('Can you work with our existing system integrator?', 'Yes. We often review an integrator&rsquo;s design or work alongside them. Our job is to make the design right, not to replace anyone.'),
    ('Is this only for large organisations?', 'No. A review of a single proposal or a two-day workshop suits mid-size organisations well. The scope is sized to the decision you need to make.'),
]

def offer_html(o, n):
    chips = ''.join('<div class="vk-fact"><span class="k">' + k + '</span><span class="v">' + v + '</span></div>' for k, v in o['chips'])
    return '''
        <div class="vk-sec vk-av-offer" id="''' + o['id'] + '''"><div class="vk-wrap">
            <div class="vk-av-head"><span class="vk-av-ic"><i class="fa-solid ''' + o['icon'] + '''"></i></span><div>
                <span class="vk-eyebrow">Offering ''' + str(n) + ''' of 4</span>
                <h2>''' + o['title'] + '''</h2>
                <p class="vk-lead">''' + o['line'] + '''</p></div></div>
            <div class="vk-facts">''' + chips + '''</div>
            <div class="vk-av-grid">
                <div class="vk-card"><h3>When it fits</h3>''' + ul(o['fits']) + '''</div>
                <div class="vk-card"><h3>What we look at</h3>''' + ul(o['looks']) + '''</div>
                <div class="vk-card"><h3>How it runs</h3>''' + steps(o['runs']) + '''</div>
                <div class="vk-card vk-av-gets"><h3>What you get</h3>''' + ul(o['gets']) + '''<h3 class="vk-av-need">What we need from you</h3>''' + ul(o['needs']) + '''</div>
            </div>
            <div class="vk-actions"><a class="vk-btn primary" href="/contact?topic=''' + o['topic'] + '''">''' + o['cta'] + '''</a><a class="vk-btn" href="#choose">Compare the four</a></div>
        </div></div>'''

SAMPLE = '''
            <div class="vk-av-sample">
                <div class="vk-av-doc">
                    <div class="vk-av-doc-top"><span>Architecture review: findings</span><span class="tag">Sample, illustrative</span></div>
                    <p class="vk-av-doc-sum"><strong>Summary.</strong> The proposed design meets the stated capacity, but recovery depends on one storage array, and GPU nodes are sized for a model twice the size of the one planned. Fixing the first is essential before sign-off; the second saves about a fifth of the hardware cost.</p>
                    <table><thead><tr><th>#</th><th>Finding</th><th>Impact</th><th>Effort</th><th>When</th></tr></thead><tbody>
                        <tr><td>1</td><td>All tiers share one storage array: a single failure stops every application</td><td><span class="r hi">High</span></td><td><span class="r lo">Low</span></td><td>Before sign-off</td></tr>
                        <tr><td>2</td><td>GPU count sized for a 140B model; plan is a 70B model with batching</td><td><span class="r hi">High</span></td><td><span class="r lo">Low</span></td><td>Before sign-off</td></tr>
                        <tr><td>3</td><td>DR runbook assumes a network path that does not exist in the LLD</td><td><span class="r md">Medium</span></td><td><span class="r md">Medium</span></td><td>Before go-live</td></tr>
                        <tr><td>4</td><td>Admin access to hypervisors not routed through the PAM tool</td><td><span class="r md">Medium</span></td><td><span class="r lo">Low</span></td><td>Before go-live</td></tr>
                        <tr><td>5</td><td>Monitoring covers servers but not storage latency</td><td><span class="r lo">Low</span></td><td><span class="r lo">Low</span></td><td>First 90 days</td></tr>
                    </tbody></table>
                </div>
                <div class="vk-av-doc-notes">
                    <h3>What a report looks like</h3>
                    <p class="vk-muted">Every finding says what is wrong, why it matters, how hard it is to fix and when it should be fixed. No padding, no generic best-practice lists.</p>
                    ''' + ul(['Written for two readers: a one-page summary for leadership, detail for engineers',
                              'Every number shows its working, so your team can check it',
                              'Findings ranked, so you know what to do first']) + '''
                </div>
            </div>'''

body = '''
        <div class="vk-wrap vk-hero">
            ''' + crumb(('Home', '/'), ('Advisory', None)) + '''
            <span class="vk-eyebrow">Advisory</span>
            <h1>An independent view before you commit</h1>
            <p class="vk-lead">Short, fixed-scope engagements for the moments when a wrong infrastructure decision would be expensive: a vendor proposal to check, an estate to assess, a new platform to scope, or a tender to write. Each one ends with a written report your team can act on.</p>
            <div class="vk-facts">
                <div class="vk-fact"><span class="k">Engagements</span><span class="v">4, each fixed scope</span></div>
                <div class="vk-fact"><span class="k">Length</span><span class="v">2 days to 6 weeks</span></div>
                <div class="vk-fact"><span class="k">Pricing</span><span class="v">Fixed fee, agreed upfront</span></div>
                <div class="vk-fact"><span class="k">Approach</span><span class="v">Vendor-neutral</span></div>
            </div>
            <div class="vk-dp-jump">''' + ''.join('<a href="#' + o['id'] + '">' + o['title'] + '</a>' for o in OFFERS) + '''<a href="#faq">Questions</a></div>
        </div>
        <div class="vk-sec" id="choose"><div class="vk-wrap">
            <span class="vk-eyebrow">Which one do you need?</span>
            <h2>Start from where you are</h2>
            <div class="vk-table-wrap"><table><thead><tr><th>If this sounds like you</th><th>Start with</th></tr></thead><tbody>''' + ''.join('<tr><td>' + a + '</td><td>' + b + '</td></tr>' for a, b in CHOOSER) + '''</tbody></table></div>
            <p class="vk-muted vk-small" style="margin-top:12px">Not sure? Describe the situation on the <a href="/contact">contact page</a> and we will suggest the smallest engagement that answers your question.</p>
        </div></div>'''
for n, o in enumerate(OFFERS, 1):
    body += offer_html(o, n)

body += '''
        <div class="vk-sec" id="method"><div class="vk-wrap">
            <span class="vk-eyebrow">How every engagement works</span>
            <h2>Same four steps, whatever the size</h2>
            <div class="vk-phases">
                <div class="vk-phase"><span class="n">1</span><h3>Understand</h3><p>Your goals, constraints and deadlines, in your words, before any technology is discussed.</p></div>
                <div class="vk-phase"><span class="n">2</span><h3>Measure</h3><p>Real data from your environment: utilisation, growth, failure history, cost. Not assumptions.</p></div>
                <div class="vk-phase"><span class="n">3</span><h3>Compare</h3><p>Realistic options side by side, each with cost, risk and what it asks of your team.</p></div>
                <div class="vk-phase"><span class="n">4</span><h3>Recommend</h3><p>A written recommendation with the reasoning shown, and a plan you can act on.</p></div>
            </div>
        </div></div>
        <div class="vk-sec" id="sample"><div class="vk-wrap">
            <span class="vk-eyebrow">What you receive</span>
            <h2>A report your team can act on the next morning</h2>''' + SAMPLE + '''
        </div></div>
        <div class="vk-sec" id="faq"><div class="vk-wrap">
            <span class="vk-eyebrow">Common questions</span>
            <h2>Before you get in touch</h2>
            <div class="vk-av-faq">''' + ''.join('<details><summary>' + q + '</summary><p>' + a + '</p></details>' for q, a in FAQ) + '''</div>
        </div></div>
        <div class="vk-sec"><div class="vk-wrap">
            <div class="vk-cta">
                <h2>Have a decision coming up?</h2>
                <p class="vk-muted">Tell us what you are deciding and by when. We will come back within one working day with the engagement that fits and a fixed quote.</p>
                <div class="vk-actions">
                    <a class="vk-btn primary" href="/contact?topic=review">Talk to us</a>
                    <a class="vk-btn" href="/deployment-scenarios">See worked designs</a>
                </div>
            </div>
        </div></div>'''

page('advisory.html', 'Advisory | Architecture reviews, technology assessments, discovery workshops | Vakratron',
     'Fixed-scope advisory engagements: architecture reviews of designs and vendor proposals, technology assessments with a 12 to 18 month roadmap, discovery workshops and vendor-neutral tender support.',
     body)
