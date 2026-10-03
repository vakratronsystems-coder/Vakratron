"""Page template for /deployments/<slug> reference-deployment pages."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'dr'))
sys.path.insert(0, HERE)
from tpl import page, crumb
from diagram import render

HUB = '/deployment-scenarios'

def table(head, rows, cls=''):
    th = ''.join('<th>' + h + '</th>' for h in head)
    tr = ''.join('<tr>' + ''.join('<td>' + c + '</td>' for c in r) + '</tr>' for r in rows)
    return '<div class="vk-table-wrap' + (' ' + cls if cls else '') + '"><table><thead><tr>' + th + '</tr></thead><tbody>' + tr + '</tbody></table></div>'

def sec(eyebrow, h2, inner, sid=None):
    i = ' id="' + sid + '"' if sid else ''
    return '\n        <div class="vk-sec"' + i + '><div class="vk-wrap"><span class="vk-eyebrow">' + eyebrow + '</span><h2>' + h2 + '</h2>' + inner + '</div></div>'

def build(sc, others):
    s = sc
    facts = '<div class="vk-facts">' + ''.join('<div class="vk-fact"><span class="k">' + k + '</span><span class="v">' + v + '</span></div>' for k, v in s['facts']) + '</div>'
    body = '''
        <div class="vk-wrap vk-hero">
            ''' + crumb(('Home', '/'), ('Deployment scenarios', HUB), (s['short'], None)) + '''
            <span class="vk-label vk-refdep"><span>Reference deployment</span></span>
            <span class="vk-eyebrow">''' + s['eyebrow'] + '''</span>
            <h1>''' + s['h1'] + '''</h1>
            <p class="vk-lead">''' + s['lead'] + '''</p>
            ''' + facts + '''
            <div class="vk-dp-jump">''' + ''.join('<a href="#' + a + '">' + t + '</a>' for a, t in [('situation', 'Situation'), ('options', 'Options'), ('architecture', 'Architecture'), ('sizing', 'Sizing'), ('delivery', 'Delivery'), ('risks', 'Risks'), ('outcomes', 'Outcomes')]) + '''</div>
        </div>'''

    body += '''
        <div class="vk-sec" id="situation"><div class="vk-wrap"><div class="vk-two">
            <div class="vk-prose"><span class="vk-eyebrow">The situation</span><h2>''' + s['situation_h2'] + '</h2>' + ''.join('<p>' + p + '</p>' for p in s['situation']) + '''</div>
            <div class="vk-card vk-dp-constraints"><h3>What could not be compromised</h3><ul class="vk-dd vk-dd-do">''' + ''.join('<li><span class="mk" aria-hidden="true">!</span><span>' + c + '</span></li>' for c in s['constraints']) + '''</ul></div>
        </div></div></div>'''

    body += sec('Options weighed', s['options_h2'], '<p class="vk-prose vk-muted">' + s['options_intro'] + '</p>' + table(['Option', 'What works', 'What does not', 'Verdict'], s['options'], 'vk-dp-options'), 'options')

    parts = ''.join('<tr><td><span class="vk-num">' + str(i + 1) + '</span> ' + t + '</td><td>' + d + '</td></tr>' for i, (t, d) in enumerate(s['parts']))
    body += sec('Target architecture', s['arch_h2'], '<p class="vk-prose vk-muted">' + s['arch_intro'] + '</p>' +
        '<figure class="vk-fig vk-refarch vk-dgfig"><span class="vk-scroll-hint">Scroll sideways to see the whole diagram &rarr;</span><div class="vk-refarch-scroll">' + render(s['diagram'], s['h1']) + '</div><figcaption>' + s['arch_caption'] + '</figcaption></figure>' +
        '<div class="vk-table-wrap"><table><thead><tr><th>Building block</th><th>Why it is there</th></tr></thead><tbody>' + parts + '</tbody></table></div>', 'architecture')

    body += sec('Sizing, worked out', s['sizing_h2'], '<p class="vk-prose vk-muted">' + s['sizing_intro'] + '</p>' + table(s['sizing_head'], s['sizing']) + ('<p class="vk-prose vk-small vk-muted">' + s['sizing_note'] + '</p>' if s.get('sizing_note') else ''), 'sizing')

    ph = ''.join('<div class="vk-phase"><span class="n">' + str(i + 1) + '</span><h3>' + t + '</h3><p class="vk-dp-dur">' + dur + '</p><p>' + d + '</p><p class="g"><strong>Gate:</strong> ' + g + '</p></div>' for i, (t, dur, d, g) in enumerate(s['phases']))
    body += sec('How it is delivered', s['delivery_h2'], '<p class="vk-prose vk-muted">' + s['delivery_intro'] + '</p><div class="vk-phases vk-dp-phases">' + ph + '</div>' + ('<div class="vk-note"><strong>Way back:</strong> ' + s['rollback'] + '</div>' if s.get('rollback') else ''), 'delivery')

    body += sec('Risks, handled up front', s['risks_h2'], table(['Risk', 'What could happen', 'How the design handles it'], s['risks']), 'risks')

    body += sec('What was optimised', s['opt_h2'], '<div class="vk-grid" style="margin-top:18px">' + ''.join('<div class="vk-card"><span class="vk-dp-metric">' + m + '</span><h3>' + t + '</h3><p class="vk-muted">' + d + '</p></div>' for m, t, d in s['optimised']) + '</div>')

    body += sec('Outcomes', s['outcomes_h2'], table(['Measure', 'Before', 'Design target'], s['outcomes'], 'vk-dp-outcomes') + '<p class="vk-prose vk-small vk-muted">' + s['outcomes_note'] + '</p>', 'outcomes')

    body += sec('Skills this draws on', 'What a team needs to deliver this', '<div class="vk-dp-skills">' + ''.join('<div class="vk-card"><h3>' + t + '</h3><p class="vk-muted">' + d + '</p></div>' for t, d in s['skills']) + '</div>')

    more = ''.join('<a class="vk-card" href="/deployments/' + o['slug'] + '"><span class="vk-label"><span>' + o['eyebrow'] + '</span></span><h3>' + o['short'] + '</h3><p class="vk-muted">' + o['card'] + '</p><span class="vk-go">Read &rarr;</span></a>' for o in others if o['slug'] != s['slug'])
    body += '''
        <div class="vk-sec"><div class="vk-wrap">
            <div class="vk-note vk-dp-disclaimer"><strong>About this page.</strong> This is a reference deployment: a worked design built from requirements we see repeatedly in this kind of organisation. It is not a description of a specific client. Figures are design targets and planning estimates; real numbers depend on your workloads and are confirmed during assessment. We are glad to walk through how it would apply to your environment.</div>
        </div></div>'''
    if more:
        body += sec('More reference deployments', 'Other scenarios', '<div class="vk-grid" style="margin-top:18px">' + more + '</div>')
    body += '''
        <div class="vk-sec"><div class="vk-wrap">
            <div class="vk-cta">
                <h2>''' + s['cta_h2'] + '''</h2>
                <p class="vk-muted">''' + s['cta_p'] + '''</p>
                <div class="vk-actions">
                    <a class="vk-btn primary" href="/contact?topic=''' + s['topic'] + '''">Talk to us</a>
                    <a class="vk-btn" href="''' + HUB + '''">All deployment scenarios</a>
                </div>
            </div>
        </div></div>'''
    page('deployments/' + s['slug'] + '.html', s['title'], s['desc'], body)
