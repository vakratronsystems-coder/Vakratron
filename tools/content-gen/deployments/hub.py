"""/deployment-scenarios hub page (new design)."""
from scenario import page, crumb

def card(s):
    facts = dict(s['facts'])
    chips = ''.join('<span>' + v + '</span>' for k, v in s['facts'][:2])
    return ('<a class="vk-card vk-hubcard" href="/deployments/' + s['slug'] + '">'
            '<span class="vk-label"><span>' + s['eyebrow'] + '</span></span>'
            '<h3>' + s['short'] + '</h3>'
            '<p class="vk-muted">' + s['card'] + '</p>'
            '<div class="vk-hubchips">' + chips + '</div>'
            '<span class="vk-go">Read the design &rarr;</span></a>')

def build_hub(groups):
    total = sum(len(i) for _, _, i in groups)
    jump = ''.join('<a href="#g' + str(n) + '">' + t + ' <em>' + str(len(i)) + '</em></a>' for n, (t, _, i) in enumerate(groups))
    body = '''
        <div class="vk-wrap vk-hero">
            ''' + crumb(('Home', '/'), ('Deployment scenarios', None)) + '''
            <span class="vk-eyebrow">Reference deployments</span>
            <h1>How we would design it, worked end to end</h1>
            <p class="vk-lead">''' + str(total) + ''' worked designs for the situations enterprise and government teams bring to us. Each one starts from a real-world problem and walks through the options, the architecture, the sizing arithmetic, the delivery plan, the risks and the outcomes the design is built to reach.</p>
            <div class="vk-dp-jump">''' + jump + '''</div>
        </div>
        <div class="vk-sec"><div class="vk-wrap">
            <div class="vk-grid vk-hubhow">
                <div class="vk-card"><span class="vk-dp-metric">1</span><h3>The situation</h3><p class="vk-muted">What is going wrong, and what cannot be compromised while fixing it.</p></div>
                <div class="vk-card"><span class="vk-dp-metric">2</span><h3>Options and architecture</h3><p class="vk-muted">The choices weighed honestly, and a diagram of the design that was chosen.</p></div>
                <div class="vk-card"><span class="vk-dp-metric">3</span><h3>Sizing and delivery</h3><p class="vk-muted">The arithmetic behind every number, and a plan with gates and a way back.</p></div>
                <div class="vk-card"><span class="vk-dp-metric">4</span><h3>Risks and outcomes</h3><p class="vk-muted">What could go wrong, how the design handles it, and what it is built to deliver.</p></div>
            </div>
        </div></div>'''
    for n, (title, sub, items) in enumerate(groups):
        body += '''
        <div class="vk-sec" id="g''' + str(n) + '''"><div class="vk-wrap">
            <span class="vk-eyebrow">''' + sub + '''</span>
            <h2>''' + title + '''</h2>
            <div class="vk-grid vk-hubgrid" style="margin-top:18px">''' + ''.join(card(s) for s in items) + '''</div>
        </div></div>'''
    body += '''
        <div class="vk-sec"><div class="vk-wrap">
            <div class="vk-note vk-dp-disclaimer"><strong>About these pages.</strong> Each is a reference deployment: a worked design built from requirements we see repeatedly in that kind of organisation, not a description of a specific client. Figures are design targets and planning estimates, confirmed against your own workloads during assessment.</div>
        </div></div>
        <div class="vk-sec"><div class="vk-wrap">
            <div class="vk-cta">
                <h2>Facing something close to one of these?</h2>
                <p class="vk-muted">Tell us what you are planning and which scenario is nearest. We will come back with a plain first view of how it would apply to your environment.</p>
                <div class="vk-actions">
                    <a class="vk-btn primary" href="/contact">Talk to us</a>
                    <a class="vk-btn" href="/solutions">Explore solutions</a>
                </div>
            </div>
        </div></div>'''
    page('deployment-scenarios.html', 'Deployment scenarios | Reference deployments for cloud, DR and AI | Vakratron',
         'Worked reference deployments for private cloud, data centre consolidation, disaster recovery, SOC, GPU platforms, LLM gateways, agentic AI and MLOps: problem, options, architecture, sizing, delivery, risks and outcomes.',
         body)
