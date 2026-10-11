"""Render a whitepaper module to (1) the web page and (2) a print HTML used to make the PDF.
Usage: python3 wp_render.py wp_dcdr [print_out_path]"""
import os, sys, importlib, html as H
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'dr'))
sys.path.insert(0, os.path.join(HERE, '..', 'deployments'))
from tpl import page, crumb
from diagram import render as render_diagram

def form_box(m, where):
    return '''
            <div class="wp-dl" data-wp="''' + m['slug'] + '''" data-where="''' + where + '''">
                <div class="wp-dl-head"><i class="fa-solid fa-file-pdf"></i><div><strong>Download the full PDF</strong><span>''' + m['pages'] + ''', including the 40-point readiness checklist</span></div></div>
                <form class="wp-dl-form" novalidate>
                    <input type="text" name="website" class="vk-cf-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
                    <div class="wp-dl-fields">
                        <input type="text" name="name" placeholder="Full name *" autocomplete="name" required>
                        <input type="email" name="email" placeholder="Work email *" autocomplete="email" required>
                        <input type="tel" name="phone" placeholder="Mobile with country code *" value="+91 " autocomplete="tel" required>
                        <input type="text" name="company" placeholder="Organisation" autocomplete="organization">
                        <input type="text" name="role" placeholder="Your role" autocomplete="organization-title">
                    </div>
                    <div class="wp-dl-otp" hidden>
                        <p>We sent a 6-digit code to <strong class="wp-dl-mail"></strong>. Enter it to get the PDF.</p>
                        <input type="text" name="otp" inputmode="numeric" autocomplete="one-time-code" maxlength="6" placeholder="6-digit code">
                        <div class="wp-dl-links"><button type="button" class="wp-dl-resend">Send a new code</button><button type="button" class="wp-dl-change">Change email</button></div>
                    </div>
                    <p class="wp-dl-err" hidden></p>
                    <button type="submit" class="vk-btn primary wp-dl-btn">Email me a code</button>
                    <p class="wp-dl-note">We confirm your email with a one-time code, then the PDF downloads straight away. No newsletters unless you ask.</p>
                </form>
                <div class="wp-dl-done" hidden>
                    <p><strong>Your copy is ready.</strong> The download has started, and we have emailed you the link too.</p>
                    <a class="vk-btn primary wp-dl-get" href="#" target="_blank" rel="noopener">Download again</a>
                </div>
            </div>'''

def section_html(s, web=True):
    h = s['html']
    if '[[DIAGRAM]]' in h:
        h = h.replace('[[DIAGRAM]]', '<figure class="wp-fig"><div class="wp-fig-scroll">' + render_diagram(MOD.DIAGRAM, MOD.META['title']) + '</div></figure>')
    return h

def web_checklist():
    groups = MOD.CHECKLIST
    first_g, first_items = groups[0]
    rest = groups[1:]
    out = '<p>Use this list to score your current position. Anything you cannot tick with evidence is a gap worth closing.</p>'
    out += '<div class="wp-check"><div class="wp-check-group"><h3>' + first_g + '</h3><ul>' + ''.join('<li>' + i + '</li>' for i in first_items) + '</ul></div></div>'
    out += '<div class="wp-locked"><div class="wp-locked-list">' + ''.join('<span><i class="fa-solid fa-lock"></i> ' + g + ' <em>' + str(len(i)) + ' points</em></span>' for g, i in rest) + '</div>'
    out += '<p>The remaining ' + str(sum(len(i) for _, i in rest)) + ' points are in the PDF, laid out as a printable checklist.</p><a class="vk-btn primary" href="#download">Get the full checklist</a></div>'
    return out

def build_web():
    m = MOD.META
    toc = ''.join('<a href="#' + s['id'] + '">' + s['title'] + '</a>' for s in MOD.SECTIONS)
    facts = [('Reading time', str(m['minutes']) + ' minutes'), ('Length', m['pages']), ('Edition', m['version'].replace('Version ', 'v')), ('Format', 'Web and PDF')]
    body = '''
        <div class="vk-wrap vk-hero wp-hero">
            ''' + crumb(('Home', '/'), ('Whitepapers', '/whitepapers'), (m['area'], None)) + '''
            <span class="vk-eyebrow">Whitepaper &middot; ''' + m['area'] + '''</span>
            <h1>''' + m['title'] + '''</h1>
            <p class="vk-lead">''' + m['subtitle'] + '''. Written for ''' + m['audience_web'] + '''.</p>
            <div class="vk-facts">''' + ''.join('<div class="vk-fact"><span class="k">' + k + '</span><span class="v">' + v + '</span></div>' for k, v in facts) + '''</div>
        </div>
        <div class="vk-sec" id="download"><div class="vk-wrap"><div class="wp-intro">
            <div class="vk-card wp-inside"><h2>What is inside</h2><ul class="vk-av-list">''' + ''.join('<li>' + i + '</li>' for i in m['inside']) + '''</ul>
                <a class="wp-readlink" href="#''' + MOD.SECTIONS[0]['id'] + '''">Or start reading online &darr;</a></div>
            ''' + form_box(m, 'top') + '''
        </div></div></div>
        <div class="vk-sec"><div class="vk-wrap"><div class="wp-layout">
            <aside class="wp-toc"><span>Contents</span>''' + toc + '''<a class="wp-toc-dl" href="#download"><i class="fa-solid fa-file-arrow-down"></i> Download PDF</a></aside>
            <article class="wp-article">'''
    for i, s in enumerate(MOD.SECTIONS):
        inner = web_checklist() if s['id'] == 'checklist' else section_html(s)
        body += '\n                <div class="wp-sec" id="' + s['id'] + '"><span class="wp-num">' + str(i + 1).zfill(2) + '</span><h2>' + s['title'] + '</h2>' + inner + '</div>'
        if s['id'] == 'patterns':
            body += '''
                <div class="wp-inline-cta"><div><strong>Taking this to a meeting?</strong> Get the PDF to share with your team: same content, printable checklist, no clutter.</div><a class="vk-btn primary" href="#download">Download the PDF</a></div>'''
    body += '''
                <div class="wp-sec wp-about"><h2>About Vakratron Systems</h2><p>Vakratron Systems is a vendor-neutral infrastructure design firm. We design data centre, disaster recovery, cloud, GPU and AI platforms for enterprises and government buyers, write our assumptions down, and stay with a design until it is running and tested.</p>
                <div class="vk-actions"><a class="vk-btn primary" href="/advisory#review">Ask for a DR review</a><a class="vk-btn" href="/portfolio/dr-solutions">DR solutions</a><a class="vk-btn" href="/deployments/core-banking-dr">See a worked DR design</a></div></div>
            </article>
        </div></div></div>'''
    page('whitepapers/' + m['slug'] + '.html', m['title'] + ' | Whitepaper | Vakratron', m['desc'], body, scripts=['/vk-whitepaper.js?v=1'])

def build_print(out):
    m = MOD.META
    parts = ['''<!DOCTYPE html><html><head><meta charset="utf-8"><title>''' + H.escape(m['title']) + '''</title><link rel="stylesheet" href="wp-print.css"></head><body>
<section class="cover"><div class="cover-top"><img src="logo.png" alt=""><span>VAKRATRON SYSTEMS</span></div>
<div class="cover-mid"><span class="eyebrow">Whitepaper &middot; ''' + m['area'] + '''</span><h1>''' + m['title'] + '''</h1><p class="sub">''' + m['subtitle'] + '''</p></div>
<div class="cover-bot"><div><strong>Written for</strong><br>''' + m['audience'] + '''</div><div><strong>''' + m['version'] + '''</strong><br>vakratronsys.com</div></div></section>
<section class="toc"><h2>Contents</h2><ol>''' + ''.join('<li><span>' + s['title'] + '</span></li>' for s in MOD.SECTIONS) + '''<li><span>About Vakratron Systems</span></li></ol>
<div class="inside"><h3>What you will take away</h3><ul>''' + ''.join('<li>' + i + '</li>' for i in m['inside']) + '''</ul></div></section>''']
    for i, s in enumerate(MOD.SECTIONS):
        parts.append('<section class="sec' + (' break' if s['id'] in ('summary', 'checklist') else '') + '" id="' + s['id'] + '"><span class="num">' + str(i + 1).zfill(2) + '</span><h2>' + s['title'] + '</h2>' + section_html(s, web=False) + '</section>')
    parts.append('''<section class="sec break about"><h2>About Vakratron Systems</h2>
<p>Vakratron Systems LLP is a vendor-neutral infrastructure design firm, recognised as a startup by DPIIT. We design data centre, disaster recovery, cloud, GPU and AI platforms for enterprises and government buyers. Every design starts from the workload, compares realistic options with their costs, writes its assumptions down, and is tested before handover.</p>
<h3>How we can help with disaster recovery</h3><ul>
<li><strong>DR review:</strong> an independent gap review of your current set-up in two to three weeks, with a ranked list of what to fix.</li>
<li><strong>DR design:</strong> tiering, pattern per tier, reference architecture, sizing and a cost model you can take to vendors.</li>
<li><strong>Drill support:</strong> planning and running your first isolated or full failover, with measured RPO and RTO.</li></ul>
<div class="contact"><div><strong>Talk to us</strong><br>connect@vakratronsys.com</div><div><strong>Online</strong><br>vakratronsys.com/advisory</div></div>
<p class="fine">This paper gives general guidance based on common enterprise requirements. Figures are planning ranges, not quotations. Apply them to your environment with care, or ask us to help. &copy; 2026 Vakratron Systems LLP.</p></section></body></html>''')
    import re
    keep = lambda t: re.sub(r'(<h3>[^<]*</h3>\s*<p>.*?</p>)', r'<div class="keep">\1</div>', t, flags=re.S)
    keep2 = lambda t: re.sub(r'(<span class="num">[^<]*</span><h2>[^<]*</h2>\s*<p>.*?</p>)', r'<div class="keep">\1</div>', t, flags=re.S)
    parts = [parts[0]] + [keep2(keep(x)) for x in parts[1:]]
    head, cover_and_toc = parts[0].split('<section class="cover">', 1)
    cover, rest_first = cover_and_toc.split('</section>', 1)
    open(out.replace('.html', '-cover.html'), 'w', encoding='utf-8').write(head.replace('</head>', '<style>@page { margin: 0; }</style></head>') + '<section class="cover">' + cover + '</section></body></html>')
    open(out, 'w', encoding='utf-8').write(head + rest_first + '\n'.join(parts[1:]))
    print('print html', out)

MOD = importlib.import_module(sys.argv[1] if len(sys.argv) > 1 else 'wp_dcdr')
build_web()
if len(sys.argv) > 2:
    build_print(sys.argv[2])
