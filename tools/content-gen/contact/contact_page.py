"""Contact page (Oct 2026 rewrite). Step-by-step enquiry that posts to the SAME
/api/contact endpoint (name, email, phone, company, reason unchanged; extra fields optional).
Run from tools/content-gen/contact/."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'dr'))
from tpl import page, crumb

AREAS = [
    ('ai', 'AI infrastructure and GPU clusters', 'fa-microchip'),
    ('dr', 'Data centre and disaster recovery', 'fa-shield-halved'),
    ('cloud', 'Private, hybrid or multi-cloud', 'fa-cloud'),
    ('vmware', 'VMware exit or migration', 'fa-right-left'),
    ('llm', 'Enterprise LLM', 'fa-brain'),
    ('rag', 'RAG or document assistant', 'fa-file-lines'),
    ('agents', 'Agentic AI', 'fa-robot'),
    ('k8s', 'Kubernetes and platform engineering', 'fa-cubes'),
    ('api', 'APIs and microservices', 'fa-plug'),
    ('tender', 'Tender or RFP specification', 'fa-file-signature'),
    ('review', 'Architecture review or second opinion', 'fa-magnifying-glass'),
    ('other', 'Something else', 'fa-ellipsis'),
]
STAGE = ['Just exploring', 'Building a budget or business case', 'Writing a tender or RFP', 'Have a vendor proposal to check', 'Live system needs fixing']
TIME = ['This month', '1 to 3 months', '3 to 6 months', 'Later, or not fixed']
ORG = ['Government or PSU', 'Enterprise', 'Startup or product company', 'System integrator or partner']

def chips(group, items, icons=False):
    out = []
    for it in items:
        if icons:
            key, label, ic = it
            out.append('<button type="button" class="vk-chip vk-chip-lg" data-group="' + group + '" data-key="' + key + '" data-value="' + label + '" aria-pressed="false"><i class="fa-solid ' + ic + '"></i><span>' + label + '</span></button>')
        else:
            out.append('<button type="button" class="vk-chip" data-group="' + group + '" data-value="' + it + '" aria-pressed="false">' + it + '</button>')
    return '<div class="vk-chips' + (' vk-chips-lg' if icons else '') + '" role="group">' + ''.join(out) + '</div>'

FORM = '''
<div class="vk-cf" id="vk-contact">
  <div class="vk-cf-top">
    <div class="vk-cf-progress" aria-hidden="true"><span id="cfBar"></span></div>
    <div class="vk-cf-count"><span id="cfStepNo">1</span> of 4 &middot; about a minute</div>
  </div>
  <form id="cfForm" novalidate>
    <input type="text" name="website" class="vk-cf-hp" tabindex="-1" autocomplete="off" aria-hidden="true">

    <div class="vk-cf-step on" data-step="1">
      <h2>What is it about?</h2>
      <p class="vk-muted">Pick the closest one. You can add detail in a moment.</p>
      ''' + chips('reason', AREAS, icons=True) + '''
      <p class="vk-cf-err" data-err="1">Please pick one, or choose &ldquo;Something else&rdquo;.</p>
    </div>

    <div class="vk-cf-step" data-step="2">
      <h2>Where are you with it?</h2>
      <p class="vk-muted">Tap what fits. Each one helps us send the right person and the right first reply.</p>
      <h3>Stage</h3>''' + chips('stage', STAGE) + '''
      <h3>When do you need it?</h3>''' + chips('timeline', TIME) + '''
      <h3>You are</h3>''' + chips('orgType', ORG) + '''
    </div>

    <div class="vk-cf-step" data-step="3">
      <h2>Anything we should know?</h2>
      <p class="vk-muted">Optional, but a few lines here save a whole call. Tap a prompt to add it.</p>
      <div class="vk-cf-hints" id="cfHints"></div>
      <textarea name="message" id="cfMsg" rows="6" maxlength="2000" placeholder="For example: 3 data centres, about 400 VMs, VMware renewal due in March, need a plan the board can approve."></textarea>
      <div class="vk-cf-small"><span id="cfMsgCount">0</span> / 2000</div>
    </div>

    <div class="vk-cf-step" data-step="4">
      <h2>Where should we reply?</h2>
      <div class="vk-cf-summary" id="cfSummary"></div>
      <div class="vk-cf-grid">
        <label>Full name *<input type="text" name="name" autocomplete="name" required placeholder="Your name"></label>
        <label>Work email *<input type="email" name="email" autocomplete="email" required placeholder="name@company.com"></label>
        <label>Phone, with country code *<input type="tel" name="phone" autocomplete="tel" required value="+91 " placeholder="+91 98xxx xxxxx"></label>
        <label>Organisation<input type="text" name="company" autocomplete="organization" placeholder="Company or department"></label>
        <label class="wide">Your role<input type="text" name="role" autocomplete="organization-title" placeholder="For example: IT head, CTO, procurement, consultant"></label>
      </div>
      <p class="vk-cf-err" data-err="4" id="cfErr4"></p>
    </div>

    <div class="vk-cf-nav">
      <button type="button" class="vk-btn" id="cfBack">&larr; Back</button>
      <button type="button" class="vk-btn primary" id="cfNext">Next &rarr;</button>
      <button type="submit" class="vk-btn primary" id="cfSend">Send enquiry</button>
    </div>
  </form>

  <div class="vk-cf-done" id="cfDone" hidden>
    <div class="vk-cf-tick">&#10003;</div>
    <h2 id="cfDoneTitle">Thank you. We have it.</h2>
    <p class="vk-muted" id="cfDoneText"></p>
    <ol class="vk-steps">
      <li>An architect reads your note and checks what you have told us.</li>
      <li>You get a reply within one working day, usually with a first view or two or three sharp questions.</li>
      <li>If it makes sense, we set up a short call at a time that suits you.</li>
    </ol>
    <div class="vk-actions"><a class="vk-btn" href="/solutions">Explore solutions</a><a class="vk-btn" href="/">Back to home</a></div>
  </div>
</div>'''

SIDE = '''
<aside class="vk-cf-side">
  <div class="vk-card">
    <h3>What happens next</h3>
    <ol class="vk-steps">
      <li>An architect reads your note, not a sales queue.</li>
      <li>Reply within one working day.</li>
      <li>A short call only if it is useful to you.</li>
    </ol>
  </div>
  <div class="vk-card">
    <h3>Prefer email?</h3>
    <p class="vk-muted">Write to <a href="mailto:connect@vakratronsys.com">connect@vakratronsys.com</a>. Attachments such as an RVTools export, a vendor proposal or a tender draft are welcome.</p>
  </div>
  <div class="vk-card">
    <h3>Your details</h3>
    <p class="vk-muted">Used only to reply to this enquiry. We are happy to sign an NDA before you share anything sensitive.</p>
  </div>
</aside>'''

body = '''
        <div class="vk-wrap vk-hero vk-cf-hero">
            ''' + crumb(('Home', '/'), ('Contact', None)) + '''
            <span class="vk-eyebrow">Contact</span>
            <h1>Tell us what you are planning</h1>
            <p class="vk-lead">Four quick steps, mostly taps. It takes about a minute, and it means our first reply can be useful instead of a list of questions.</p>
        </div>
        <div class="vk-sec vk-cf-sec"><div class="vk-wrap"><div class="vk-cf-layout">''' + FORM + SIDE + '''</div></div></div>'''

page('contact.html', 'Contact Vakratron Systems | Tell us what you are planning',
     'Tell us about your GPU cluster, cloud move, DR plan, AI pilot or tender. Four quick steps; an architect replies within one working day.',
     body, scripts=['/vk-contact.js'])
