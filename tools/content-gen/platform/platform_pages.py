"""Kubernetes & platform engineering and API & microservices pages (Oct 2026 rewrite). Run from tools/content-gen/platform/."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'dr'))
sys.path.insert(0, os.path.join(HERE, '..', 'cloud'))
sys.path.insert(0, os.path.join(HERE, '..', 'genai'))
from tpl import page, crumb
from cloud_pages import N, F, sec, hero, table, ul, steps, figure
from genai_pages import cta, more_links, ghero, faqblock, cards, uc_hero

HOME = ("Home", "/")
SCRIPTS = ['/vk-platform-tools.js']

# =====================================================================================
# KUBERNETES
# =====================================================================================
KHUB = ("Kubernetes", "/portfolio/kubernetes-platform")
KB = '/solutions/k8s'
KP = [('platform-design', 'Platform design'), ('gitops-delivery', 'GitOps delivery'), ('k8s-security', 'Security'), ('multi-cluster', 'Multi-cluster and on-prem')]
KCTA = cta('Planning a Kubernetes platform, or fixing one?', 'Tell us how many applications and teams you have, how you deploy today and where it should run. We will come back with an honest view: whether Kubernetes fits, what a lean platform looks like, and what it takes to run.', 'Book a platform review', '/portfolio/kubernetes-platform', 'Back to Kubernetes')
def kmore(cur): return more_links('More Kubernetes guides:', KB, KP, cur, '<a href="/solutions/k8s/faq">Kubernetes FAQ</a> &middot; <a href="/use_cases/k8s-festive-scale">Use case: festive-season scale</a>')

def k_hub():
    b = hero((HOME, ("Solutions", "/solutions"), ("Kubernetes", None)), 'Kubernetes and platform engineering', 'Kubernetes where it helps, and an honest no where it does not',
             'Kubernetes is excellent at running many services for many teams, deploying often and scaling automatically. It is also complex. We help you decide whether you need it, then build a platform your developers like using and your team can actually run and upgrade.',
             actions=[('Book a platform review', '/contact'), ('Do we need Kubernetes?', '#k8scheck')])
    b += sec('''<span class="vk-eyebrow">What usually goes wrong</span><h2>Why Kubernetes platforms disappoint</h2>
            <div class="vk-grid" style="margin-top:22px">
                <div class="vk-card"><h3>Clusters everywhere</h3><p class="vk-muted">Every team built its own cluster its own way. Nobody knows which ones are patched.</p></div>
                <div class="vk-card"><h3>Upgrades nobody dares to do</h3><p class="vk-muted">Kubernetes releases about three versions a year. Clusters that fall behind lose support and become risky to upgrade.</p></div>
                <div class="vk-card"><h3>Developers still wait for tickets</h3><p class="vk-muted">The platform exists, but getting an environment or a deployment still needs a request to the infrastructure team.</p></div>
                <div class="vk-card"><h3>Security left at defaults</h3><p class="vk-muted">Containers run as root, any pod can talk to any other, and images are never scanned.</p></div>
            </div>''')
    b += sec('''<span class="vk-eyebrow">Try it</span><h2>Do we really need Kubernetes?</h2>
            <p class="vk-prose">Five questions, and an honest answer. Sometimes the right answer is virtual machines with good automation, or a managed container service.</p>
            <div class="vk-tool vk-placer vk-k8scheck"></div><noscript><p class="vk-muted">This tool needs JavaScript.</p></noscript>''', sid='k8scheck')
    b += sec('<span class="vk-eyebrow">The building blocks</span><h2>What a platform includes beyond Kubernetes</h2>' + table(['Layer', 'What it does', 'Common choices'],
        [['Clusters', 'Run the containers', 'Managed (EKS, AKS, GKE, OKE) or self-run (RKE2, OpenShift, kubeadm)'],
         ['Delivery', 'Get code from Git to production safely', 'CI pipelines, Argo CD or Flux'],
         ['Images', 'Store, scan and sign container images', 'Harbor, Trivy, cosign'],
         ['Networking', 'Route traffic in and between services', 'Ingress controllers, Gateway API, Cilium or Calico'],
         ['Security', 'Limit what can run and what it can reach', 'RBAC, network policies, Kyverno or OPA Gatekeeper'],
         ['Observability', 'Metrics, logs and traces', 'Prometheus, Grafana, Loki, OpenTelemetry'],
         ['Developer experience', 'Self-service templates and docs', 'Backstage or a simple internal portal']]))
    b += sec('<span class="vk-eyebrow">Go deeper</span><h2>Guides and examples</h2>' + cards([
        ('/solutions/k8s/platform-design', 'Platform design', 'How a production platform is laid out, managed or self-run, and how to size it.', 'Read the guide'),
        ('/solutions/k8s/gitops-delivery', 'GitOps delivery', 'Deploy from Git, with an animated rolling update, server failure and drift fix.', 'Read the guide'),
        ('/solutions/k8s/k8s-security', 'Security', 'The controls that matter, and keeping clusters upgraded.', 'Read the guide'),
        ('/solutions/k8s/multi-cluster', 'Multi-cluster and on-prem', 'When to run more than one cluster, and Kubernetes on OpenStack or bare metal.', 'Read the guide'),
        ('/use_cases/k8s-festive-scale', 'Use case: festive-season scale', 'An illustrative retailer moving 30 services to Kubernetes before its biggest sale.', 'Read the use case'),
        ('/solutions/k8s/faq', 'Kubernetes questions, answered', 'Managed or self-run, alternatives, cost, skills and more.', 'Read the FAQ')]) +
        '<p class="vk-small" style="margin-top:18px">Related: <a href="/portfolio/api-microservices">APIs and microservices</a>, <a href="/solutions/cloud/private-cloud-openstack">private cloud on OpenStack</a>. Full reference: <a href="/solutions/master_k8s">Kubernetes whitepaper</a>.</p>')
    b += sec('<span class="vk-eyebrow">How we work</span><h2>How a platform engagement runs</h2>' + steps([
        '<strong>Honest fit check.</strong> Applications, teams, release pace and skills. If Kubernetes is not the answer, we say so.',
        '<strong>Lean first platform.</strong> One or two clusters, GitOps delivery, basic security and monitoring. Nothing you will not use.',
        '<strong>First teams on board.</strong> Two or three friendly teams move real services and shape the templates.',
        '<strong>Harden.</strong> Policies, image scanning, backups and an upgrade routine.',
        '<strong>Scale out.</strong> More teams, self-service, and more clusters only where there is a reason.',
        '<strong>Hand over.</strong> Runbooks and upgrade practice with your platform team.']), prose=True)
    b += KCTA
    page('portfolio/kubernetes-platform.html', 'Kubernetes and Platform Engineering: Honest Fit, Lean Platforms, GitOps | Vakratron Systems',
         'Kubernetes explained plainly, with an honest "do we need it?" checker: what a platform includes, GitOps delivery, security, multi-cluster and on-premises Kubernetes.', b, scripts=SCRIPTS)

def k_design():
    d = dict(panels=('Platform services', 'Workload cluster'), rows=4, nodes={
        'dev': N('G', title='Developers', sub='push code, use templates', style='global', x=370, w=220),
        'portal': N('P', 0, title='Developer portal', sub='templates, docs, self-service'),
        'ci': N('P', 1, title='CI pipelines', sub='build, test, scan'),
        'reg': N('P', 2, title='Container registry', sub='scanned and signed images'),
        'gitops': N('P', 3, title='GitOps controller', sub='Argo CD or Flux'),
        'ing': N('D', 0, title='Ingress and gateway', sub='TLS, routing, rate limits'),
        'obs': N('D', 1, title='Observability', sub='metrics, logs, traces'),
        'ns': N('D', 2, title='Team namespaces', sub='quotas and network policies per team'),
        'cfg': N('D', 3, title='Cluster configuration', sub='policies, add-ons, secrets operator'),
    }, flows=[F('dev', 'P', 'traffic'), F('ci', 'reg', 'stream', 1), F('reg', 'ns', 'batch', 2), F('gitops', 'cfg', 'deploy', 3), F('obs', 'ci', 'hb', 4)])
    b = ghero(KHUB, KB, KP, 'platform-design', 'Kubernetes guide', 'Platform design',
              'A good platform makes the right way the easy way: developers get a working, secure environment from a template, deploy by merging to Git, and see their own metrics. Here is how such a platform is put together, and the early decisions that matter most.',
              [('Control plane', '3 nodes'), ('Delivery', 'GitOps'), ('Tenancy', 'Namespace per team'), ('Upgrades', '~3 Kubernetes releases a year')], 'Platform design')
    b += sec('<span class="vk-eyebrow">Reference architecture</span><h2>How the pieces fit together</h2>' + figure(d, 'Kubernetes platform reference architecture',
        'Developers never touch the cluster directly. Code goes through CI, images through the registry, and configuration through Git.',
        [('1', 'Build', 'CI builds the container image, runs tests and scans it for known vulnerabilities.'),
         ('2', 'Images', 'Only scanned, signed images from your registry are allowed to run.'),
         ('3', 'Configuration from Git', 'The GitOps controller applies everything the cluster runs from Git, including policies and add-ons.'),
         ('4', 'Feedback', 'Each team sees its own metrics, logs and alerts, so problems are found by the people who can fix them.'),
         ('', 'Team namespaces', 'Each team gets a namespace with resource quotas and network policies, created from a template.')]))
    b += sec('<h2>Managed or self-run?</h2>' + table(['', 'Managed Kubernetes (EKS, AKS, GKE, OKE)', 'Self-run (RKE2, OpenShift, kubeadm)'],
        [['Control plane', 'Run and upgraded by the provider', 'Run and upgraded by you'],
         ['Good for', 'Public cloud workloads, small platform teams', 'On-premises, private cloud, strict data rules'],
         ['Watch out for', 'Cloud cost and provider-specific features', 'Upgrade discipline and on-call ownership']]))
    b += sec('<h2>Sizing a first cluster</h2>' + ul([
        '<strong>Control plane:</strong> three nodes, so it survives one failure and can be upgraded one node at a time.',
        '<strong>Workers:</strong> enough capacity for peak load with one node lost, plus room for rolling updates.',
        '<strong>Node pools:</strong> separate pools for general workloads, memory-heavy workloads and GPUs if needed.',
        '<strong>Storage:</strong> a CSI driver for your storage (Ceph via Rook, vendor arrays, or cloud volumes) for stateful services.']), prose=True)
    b += kmore('platform-design') + KCTA
    page('solutions/k8s/platform-design.html', 'Kubernetes Platform Design: Architecture, Managed vs Self-Run, Sizing | Vakratron Systems',
         'How a production Kubernetes platform is put together: developer portal, CI, registry, GitOps, team namespaces, observability, managed vs self-run, and sizing a first cluster.', b)

def k_gitops():
    b = ghero(KHUB, KB, KP, 'gitops-delivery', 'Kubernetes guide', 'GitOps delivery',
              'With GitOps, Git is the single source of truth for what runs in your clusters. A controller watches Git and keeps the cluster matching it. Deployments become pull requests, rollbacks become reverts, and every change is reviewed and recorded.',
              [('Source of truth', 'Git'), ('Controller', 'Argo CD or Flux'), ('Rollback', 'Revert a commit'), ('Drift', 'Fixed automatically')], 'GitOps delivery')
    b += sec('''<span class="vk-eyebrow">See it working</span><h2>Release, fail, and drift</h2>
            <p class="vk-prose">Release a new version and watch pods update one at a time with no downtime. Lose a server and watch Kubernetes replace its pods. Then make a change directly in the cluster, bypassing Git, and watch the controller put it back.</p>
            <div class="vk-tool vk-gitops"></div><noscript><p class="vk-muted">This simulation needs JavaScript.</p></noscript>''')
    b += sec('<h2>How a change reaches production</h2>' + steps([
        'A developer opens a pull request that changes the image version or configuration.',
        'Automated checks run: policy tests, configuration validation, security scans.',
        'A reviewer approves and the change is merged.',
        'The controller applies it to the test environment, then to production after promotion.',
        'If something goes wrong, the commit is reverted and the controller rolls back.']), prose=True)
    b += sec('<h2>Good practice</h2>' + ul([
        '<strong>Separate application code from deployment configuration,</strong> usually in different repositories or folders.',
        '<strong>Promote between environments through Git,</strong> not by rebuilding images.',
        '<strong>Keep secrets out of Git.</strong> Use External Secrets with Vault or a cloud secret store, or encrypted Sealed Secrets.',
        '<strong>Turn on self-healing and pruning carefully,</strong> starting with non-production clusters.']), prose=True)
    b += sec('<h2>Typical tools</h2>' + table(['Area', 'Common choices'], [['Controllers', 'Argo CD, Flux'], ['Packaging', 'Helm, Kustomize'], ['Secrets', 'External Secrets Operator, HashiCorp Vault, Sealed Secrets'], ['Progressive delivery', 'Argo Rollouts, Flagger']]))
    b += kmore('gitops-delivery') + KCTA
    page('solutions/k8s/gitops-delivery.html', 'GitOps Delivery on Kubernetes: Argo CD, Flux, Rollbacks and Drift | Vakratron Systems',
         'How GitOps works on Kubernetes, with an interactive simulation of a rolling update, a server failure and automatic drift correction. Includes good practice and tools.', b, scripts=SCRIPTS)

def k_sec():
    b = ghero(KHUB, KB, KP, 'k8s-security', 'Kubernetes guide', 'Kubernetes security',
              'Out of the box, Kubernetes is permissive: containers can run as root and any pod can reach any other. A handful of controls, applied consistently from templates, closes most of the gaps. Keeping clusters upgraded closes most of the rest.',
              [('Default', 'Deny, then allow'), ('Images', 'Scanned and signed'), ('Policies', 'Enforced at admission'), ('Upgrades', 'Every few months')], 'Security')
    b += sec('<h2>The controls that matter most</h2>' + table(['Control', 'What it does', 'Common choices'],
        [['Access control (RBAC)', 'People and systems get only the permissions they need', 'Groups from your identity provider, no shared admin accounts'],
         ['Namespaces and quotas', 'Teams are separated and cannot use up the whole cluster', 'One namespace per team and environment'],
         ['Network policies', 'Pods can only talk to what they need to', 'Default-deny, with Cilium or Calico'],
         ['Pod security', 'Blocks root containers and risky settings', 'Pod Security Standards at the restricted level'],
         ['Image security', 'Only trusted, scanned images run', 'Trivy scanning, cosign signatures, a private registry'],
         ['Policy engine', 'Enforces your rules when anything is created', 'Kyverno or OPA Gatekeeper'],
         ['Secrets', 'Keeps passwords and keys out of Git and images', 'Vault or cloud secret stores via External Secrets'],
         ['Audit and runtime', 'Records changes and spots suspicious behaviour', 'API audit logs, Falco'],
         ['Benchmarks', 'Checks clusters against known good settings', 'CIS Kubernetes Benchmark with kube-bench']]))
    b += sec('<h2>Keeping clusters upgraded</h2>' + ul([
        'Kubernetes ships about three minor versions a year, and each is supported for roughly fourteen months.',
        'Clusters more than a couple of versions behind become hard to upgrade and lose security fixes.',
        'Upgrade on a schedule: non-production first, a short soak, then production. Practise it, so it becomes routine.',
        'Track deprecated APIs in your manifests before each upgrade, so applications do not break.']), prose=True)
    b += kmore('k8s-security') + KCTA
    page('solutions/k8s/k8s-security.html', 'Kubernetes Security: RBAC, Network Policies, Pod Security, Images, Upgrades | Vakratron Systems',
         'The Kubernetes security controls that matter most: RBAC, namespaces, network policies, pod security, image scanning and signing, policy engines, secrets, audit, benchmarks and upgrades.', b)

def k_multi():
    b = ghero(KHUB, KB, KP, 'multi-cluster', 'Kubernetes guide', 'Multi-cluster and on-premises Kubernetes',
              'One well-run cluster is better than five neglected ones. More clusters make sense for clear reasons: separating production, meeting data rules, or running close to users. When you do need several, manage them as one fleet.',
              [('Start with', 'As few clusters as possible'), ('Split for', 'Environment, region, rules'), ('Manage as', 'A fleet'), ('On-prem', 'OpenStack or bare metal')], 'Multi-cluster and on-prem')
    b += sec('<h2>When to add a cluster</h2>' + table(['Reason', 'Example', 'Alternative to consider first'],
        [['Separate production', 'Production and non-production on different clusters', 'Usually worth it'],
         ['Data rules', 'Customer data must stay in a specific location', 'Usually worth it'],
         ['Regions or sites', 'Users in two regions, or disaster recovery', 'Usually worth it'],
         ['Each team wants its own', 'Ten teams, ten clusters', 'Namespaces with quotas and policies on a shared cluster'],
         ['Different Kubernetes versions', 'One application cannot upgrade yet', 'Fix the application; old clusters become a risk']]))
    b += sec('<h2>Managing a fleet</h2>' + ul([
        'Build every cluster from the same code (Cluster API, Terraform or your distribution\'s tooling).',
        'Apply the same baseline policies and add-ons to every cluster from Git, for example with Argo CD ApplicationSets.',
        'Send metrics and logs from all clusters to one place.',
        'Upgrade the fleet in waves, with the same routine every time.']), prose=True)
    b += sec('<h2>Kubernetes on-premises</h2>' + table(['Topic', 'What to plan'],
        [['On OpenStack', 'Clusters created by Cluster API or Magnum, using Cinder for volumes and Octavia for load balancers. See <a href="/solutions/cloud/private-cloud-openstack">private cloud on OpenStack</a>.'],
         ['On bare metal', 'Best performance and GPU access; needs MetalLB or similar for load balancers and a plan for replacing failed hardware.'],
         ['Storage', 'Rook-Ceph or a vendor CSI driver for persistent volumes.'],
         ['Backup', 'Velero for cluster resources and volumes, with copies off the cluster. Disaster recovery for the platform: see <a href="/portfolio/dr-solutions">DR</a>.']]))
    b += kmore('multi-cluster') + KCTA
    page('solutions/k8s/multi-cluster.html', 'Multi-Cluster and On-Premises Kubernetes: Fleets, OpenStack, Bare Metal | Vakratron Systems',
         'When to run more than one Kubernetes cluster, how to manage clusters as a fleet, and how to run Kubernetes on OpenStack or bare metal with storage and backup.', b)

def k_faq():
    qa = [('Managed Kubernetes or run our own?', '<p>In public cloud, managed is almost always the right start. On-premises or with strict data rules, you run it yourself, ideally with a well-supported distribution and an upgrade routine.</p>'),
          ('What are the alternatives to Kubernetes?', '<p>Virtual machines with good automation (Ansible, Terraform), managed container services such as AWS ECS or Azure Container Apps, or a platform-as-a-service. For a handful of applications these are often simpler and cheaper.</p>'),
          ('Can databases run on Kubernetes?', '<p>Yes, with operators and good storage, and many teams do. For critical databases, many organisations still prefer managed databases or dedicated servers. Decide per database.</p>'),
          ('How many people does it take to run?', '<p>A small platform can be run by two or three people with good automation, especially on managed Kubernetes. Self-run, multi-cluster platforms need a dedicated team.</p>'),
          ('Does Kubernetes save money?', '<p>It can, by packing workloads more tightly and scaling down when idle. But it adds platform and people cost. The bigger gains are usually faster, safer delivery.</p>'),
          ('Where do we start?', '<p>With the <a href="/portfolio/kubernetes-platform#k8scheck">fit check</a>, then one lean cluster and two friendly teams.</p>')]
    b = hero((HOME, KHUB, ("FAQ", None)), 'Kubernetes guide', 'Kubernetes questions, answered', 'Short answers to the questions we hear most often about Kubernetes and platform engineering.')
    b += sec(faqblock(qa), prose=True) + kmore('faq') + KCTA
    page('solutions/k8s/faq.html', 'Kubernetes FAQ: Managed or Self-Run, Alternatives, Databases, Cost | Vakratron Systems',
         'Plain answers on Kubernetes: managed vs self-run, alternatives, databases on Kubernetes, team size, cost and where to start.', b)

def k_uc():
    b = uc_hero(KHUB, 'Use case: festive-season scale', 'Thirty services onto Kubernetes before the biggest sale of the year',
                'How we would help an online retailer whose traffic jumps several times over during the festive sale move its services to Kubernetes, without risking the sale itself.',
                [('Services', '~30'), ('Peak traffic', 'Several times normal'), ('Platform', 'Managed Kubernetes'), ('Deadline', 'Before the festive sale')])
    b += sec('''<span class="vk-eyebrow">The situation</span><h2>Over-provisioned all year, nervous all sale</h2>
            <p>The retailer ran about thirty services on virtual machines sized for the festive peak, so most of that capacity sat idle for eleven months. Releases needed a weekend and a war room. Last year, a slow recommendation service backed up checkout during the busiest hour.</p>''', prose=True)
    b += sec('<span class="vk-eyebrow">The approach</span><h2>What we would do</h2>' + steps([
        '<strong>Fit check:</strong> many services, weekly releases, big spikes and a team that already used containers. Kubernetes fits.',
        '<strong>Managed Kubernetes</strong> in the existing public cloud, with GitOps delivery from day one.',
        '<strong>Move low-risk services first</strong> (catalogue, search), then checkout and payments last.',
        '<strong>Autoscaling</strong> on request rate for customer-facing services, with tested upper limits.',
        '<strong>Timeouts and circuit breakers</strong> so a slow non-critical service cannot hold up checkout. See <a href="/portfolio/api-microservices#apisim">the API simulator</a>.',
        '<strong>Load test at twice the expected peak</strong> four weeks before the sale, and freeze changes in sale week.']), prose=True)
    b += sec('<span class="vk-eyebrow">What changes</span><h2>Targets and how they are checked</h2>' + table(['Measure', 'Target', 'Checked by'],
        [['Idle capacity outside the sale', 'Much lower', 'Monthly cloud bill and utilisation'],
         ['Release effort', 'Routine weekday releases', 'Deployment frequency and rollback count'],
         ['Checkout during peak', 'Unaffected by non-critical services', 'Load test results and sale-day monitoring']]))
    b += sec('<span class="vk-eyebrow">Trade-offs</span><h2>What we would flag</h2>' + ul([
        '<strong>The deadline is fixed.</strong> If checkout is not ready in time, it stays on virtual machines for this sale.',
        '<strong>Autoscaling needs warm-up.</strong> Pre-scale before known peaks; do not rely on reacting in the first minute.',
        '<strong>The database is the real limit.</strong> Scaling application pods does not help if the database cannot keep up.']), prose=True)
    b += KCTA
    page('use_cases/k8s-festive-scale.html', 'Use Case: Moving 30 Services to Kubernetes Before a Festive Sale | Vakratron Systems',
         'An illustrative scenario: an online retailer moving about thirty services to managed Kubernetes with GitOps, autoscaling and circuit breakers before its peak sale.', b)


# =====================================================================================
# API & MICROSERVICES
# =====================================================================================
PHUB = ("APIs and microservices", "/portfolio/api-microservices")
PB = '/solutions/api'
PP = [('api-design', 'API design and gateway'), ('monolith-or-microservices', 'Monolith or microservices?'), ('event-driven', 'Event-driven integration'), ('api-security', 'API security')]
PCTA = cta('Untangling integrations, or opening APIs to partners?', 'Tell us which systems need to talk, who will call your APIs, and what breaks today. We will come back with a plain view of the right structure, what to change first, and what to leave alone.', 'Book an integration review', '/portfolio/api-microservices', 'Back to APIs and microservices')
def pmore(cur): return more_links('More API guides:', PB, PP, cur, '<a href="/solutions/api/faq">API FAQ</a> &middot; <a href="/use_cases/partner-api-logistics">Use case: partner APIs</a>')

def p_hub():
    b = hero((HOME, ("Solutions", "/solutions"), ("APIs and microservices", None)), 'APIs and microservices', 'APIs that are easy to use, safe to open, and hard to break',
             'Most integration problems are not about technology. They come from point-to-point connections nobody documented, services split too early, and one slow system dragging others down with it. We help you design APIs and services that stay understandable as they grow.',
             actions=[('Book an integration review', '/contact'), ('See a gateway and circuit breaker at work', '#apisim')])
    b += sec('''<span class="vk-eyebrow">What usually goes wrong</span><h2>Why integration gets painful</h2>
            <div class="vk-grid" style="margin-top:22px">
                <div class="vk-card"><h3>Spaghetti connections</h3><p class="vk-muted">Every system talks directly to every other. Change one, and you find out what breaks in production.</p></div>
                <div class="vk-card"><h3>Microservices too early</h3><p class="vk-muted">A small team split one application into twenty services and got all of the complexity with none of the benefit.</p></div>
                <div class="vk-card"><h3>Nobody knows which APIs exist</h3><p class="vk-muted">Old versions and test endpoints stay open on the internet, with no owner and no monitoring.</p></div>
                <div class="vk-card"><h3>One slow service stops everything</h3><p class="vk-muted">A service waits forever on a slow dependency, threads pile up, and the failure spreads.</p></div>
            </div>''')
    b += sec('''<span class="vk-eyebrow">See it working</span><h2>Gateway checks, rate limits and a circuit breaker</h2>
            <p class="vk-prose">Send requests as a valid partner and as an unknown caller. Send a burst to hit the rate limit. Then switch the payments service to failing, and watch the circuit breaker stop the orders service from waiting on it.</p>
            <div class="vk-tool vk-apisim"></div><noscript><p class="vk-muted">This simulation needs JavaScript.</p></noscript>''', sid='apisim')
    b += sec('<span class="vk-eyebrow">Go deeper</span><h2>Guides and examples</h2>' + cards([
        ('/solutions/api/api-design', 'API design and gateway', 'Contracts, versioning, errors, idempotency and what the gateway should do.', 'Read the guide'),
        ('/solutions/api/monolith-or-microservices', 'Monolith or microservices?', 'An honest comparison, and when a modular monolith is the better answer.', 'Read the guide'),
        ('/solutions/api/event-driven', 'Event-driven integration', 'When to send events instead of calling APIs, and how to do it reliably.', 'Read the guide'),
        ('/solutions/api/api-security', 'API security', 'The OWASP API Top 10 risks and the controls that stop them.', 'Read the guide'),
        ('/use_cases/partner-api-logistics', 'Use case: partner APIs', 'An illustrative logistics company opening tracking APIs to 40 partners.', 'Read the use case'),
        ('/solutions/api/faq', 'API questions, answered', 'REST or GraphQL, gateways, versioning, legacy systems and more.', 'Read the FAQ')]) +
        '<p class="vk-small" style="margin-top:18px">Related: <a href="/portfolio/kubernetes-platform">Kubernetes</a> to run services. Full reference: <a href="/solutions/master_api">API whitepaper</a>.</p>')
    b += sec('<span class="vk-eyebrow">How we work</span><h2>How an integration engagement runs</h2>' + steps([
        '<strong>Map what talks to what.</strong> Every integration, its owner and what breaks if it stops.',
        '<strong>Decide the shape.</strong> Which domains need clear APIs, where events fit, and what should stay as it is.',
        '<strong>Put a gateway and catalogue in front.</strong> One place for keys, limits, documentation and monitoring.',
        '<strong>Change gradually.</strong> Replace the worst point-to-point links first, without a big-bang rewrite.',
        '<strong>Make failure safe.</strong> Timeouts, retries and circuit breakers on every call between services.',
        '<strong>Hand over.</strong> API guidelines, templates and review practice your teams can follow.']), prose=True)
    b += PCTA
    page('portfolio/api-microservices.html', 'APIs and Microservices: Design, Gateways, Events and Security | Vakratron Systems',
         'Plain guidance on APIs and microservices, with an interactive gateway and circuit-breaker demo: API design, monolith vs microservices, event-driven integration and API security.', b, scripts=SCRIPTS)

def p_design():
    d = dict(panels=('Edge and governance', 'Services'), rows=4, nodes={
        'callers': N('G', title='Apps, partners, internal teams', sub='call APIs with keys or tokens', style='global', x=370, w=220),
        'gw': N('P', 0, title='API gateway', sub='authentication, rate limits, routing'),
        'portal': N('P', 1, title='Developer portal', sub='docs, keys, sandbox'),
        'cat': N('P', 2, title='API catalogue', sub='every API, its owner and version'),
        'mon': N('P', 3, title='Monitoring', sub='latency, errors, usage per caller'),
        'orders': N('D', 0, title='Orders service', sub='timeouts and circuit breakers'),
        'pay': N('D', 1, title='Payments service', sub='idempotent: safe to retry'),
        'bus': N('D', 2, title='Event broker', sub='order placed, payment received'),
        'legacy': N('D', 3, title='Legacy systems', sub='reached through adapters'),
    }, flows=[F('callers', 'P', 'traffic'), F('gw', 'orders', 'stream', 1), F('orders', 'pay', 'stream', 2), F('pay', 'bus', 'stream', 3), F('bus', 'legacy', 'batch', 4), F('legacy', 'mon', 'hb')])
    b = ghero(PHUB, PB, PP, 'api-design', 'API guide', 'API design and gateway',
              'A good API is one a developer can use correctly from its documentation alone, and one you can change without breaking the people who depend on it. A gateway in front gives you one place to control and observe all of them.',
              [('Contract', 'OpenAPI, written first'), ('Versions', 'Never break callers'), ('Payments', 'Idempotency keys'), ('Every call', 'Has a timeout')], 'API design and gateway')
    b += sec('<span class="vk-eyebrow">Reference architecture</span><h2>How the pieces fit together</h2>' + figure(d, 'API and microservices reference architecture',
        'Callers only ever reach the gateway. Services call each other with timeouts, and share news through events.',
        [('1', 'Gateway to service', 'The gateway checks the key or token, applies rate limits and routes to the right service and version.'),
         ('2', 'Service to service', 'Every call has a timeout and a circuit breaker, so a slow dependency fails fast instead of spreading.'),
         ('3', 'Events', 'Services announce what happened ("payment received") instead of calling everyone who might care.'),
         ('4', 'Legacy', 'Older systems are wrapped by small adapters, so they can be replaced later without changing callers.')]))
    b += sec('<h2>Design rules we use</h2>' + table(['Rule', 'Why'],
        [['Write the contract first (OpenAPI)', 'Callers and providers agree before code exists; docs and tests come from it'],
         ['Never break existing callers', 'Add fields freely; remove or change them only in a new version, with notice'],
         ['Consistent errors', 'Same error format everywhere, with a clear code and message'],
         ['Idempotency keys for payments and orders', 'A retried request never charges or ships twice'],
         ['Pagination and filters', 'No endpoint returns everything at once'],
         ['Timeouts, retries with backoff, circuit breakers', 'Failures stay small and short']]))
    b += sec('<h2>Typical tools</h2>' + table(['Area', 'Common choices'],
        [['Gateways', 'Kong, Apache APISIX, cloud API gateways, Kubernetes Gateway API implementations'], ['Contracts', 'OpenAPI, AsyncAPI for events'],
         ['Resilience', 'Built into frameworks (for example Resilience4j) or a service mesh such as Istio or Linkerd'], ['Portal and catalogue', 'Backstage or the gateway\'s developer portal']]))
    b += pmore('api-design') + PCTA
    page('solutions/api/api-design.html', 'API Design and Gateways: Contracts, Versioning, Idempotency, Resilience | Vakratron Systems',
         'How to design APIs that last: contract-first with OpenAPI, non-breaking versioning, consistent errors, idempotency keys, timeouts and circuit breakers, with a gateway reference architecture.', b)

def p_mono():
    b = ghero(PHUB, PB, PP, 'monolith-or-microservices', 'API guide', 'Monolith or microservices?',
              'Microservices solve a specific problem: many teams needing to change and release parts of a system independently. If you do not have that problem, they mostly add cost. A well-structured monolith is often the better first answer.',
              [('Start with', 'A modular monolith'), ('Split when', 'Teams block each other'), ('For legacy', 'Strangler pattern'), ('Avoid', 'The distributed monolith')], 'Monolith or microservices?')
    b += sec('<h2>Honest comparison</h2>' + table(['', 'Modular monolith', 'Microservices'],
        [['Best for', 'One or a few teams, a product still taking shape', 'Many teams, parts with very different scale or release needs'],
         ['Deploy', 'One unit, simple', 'Many units, needs a platform and automation'],
         ['Data', 'One database, simple transactions', 'A database per service, harder consistency'],
         ['Failure', 'In-process calls rarely fail', 'Every network call can fail and must be handled'],
         ['Cost to run', 'Lower', 'Higher: platform, monitoring, more infrastructure']]))
    b += sec('<h2>Signs you should split a service out</h2>' + ul([
        'Teams wait on each other to release.',
        'One part needs to scale very differently from the rest.',
        'One part changes daily while the rest is stable.',
        'A clear business boundary exists, with its own data.']) +
        '<h2>Signs you split too early</h2>' + ul([
        'Every feature needs changes in several services at once.',
        'Services share a database.',
        'You cannot test anything without starting everything.']), prose=True)
    b += sec('<h2>Modernising a legacy system</h2>' + steps([
        'Put an API or gateway in front of the legacy system.',
        'Build new capabilities as separate services behind the same front.',
        'Move existing features out one at a time, routing traffic to the new version.',
        'Retire the old parts as they empty out. This is called the strangler pattern.']), prose=True)
    b += pmore('monolith-or-microservices') + PCTA
    page('solutions/api/monolith-or-microservices.html', 'Monolith or Microservices? An Honest Comparison | Vakratron Systems',
         'When microservices are worth it and when a modular monolith is the better answer: honest comparison, signs to split or not, and modernising legacy systems with the strangler pattern.', b)

def p_events():
    b = ghero(PHUB, PB, PP, 'event-driven', 'API guide', 'Event-driven integration',
              'An API call says "do this now and tell me the answer". An event says "this happened". When many systems need to react to the same thing, events keep them loosely connected: the sender does not need to know who is listening.',
              [('Use calls for', 'Questions needing an answer now'), ('Use events for', 'News others react to'), ('Brokers', 'Kafka, RabbitMQ, NATS'), ('Consumers', 'Must be idempotent')], 'Event-driven integration')
    b += sec('<h2>Call or event?</h2>' + table(['Situation', 'Use', 'Example'],
        [['Caller needs an answer to continue', 'API call', 'Check stock before confirming an order'],
         ['Several systems react to the same thing', 'Event', '"Order placed" updates warehouse, billing and notifications'],
         ['The receiver may be offline for a while', 'Event', 'A branch system that syncs every few minutes'],
         ['Very high volume of updates', 'Event stream', 'Tracking pings from thousands of vehicles']]))
    b += sec('<h2>Doing it reliably</h2>' + ul([
        '<strong>Outbox pattern:</strong> save the change and the event in the same database transaction, then publish, so you never update the database without telling others.',
        '<strong>Idempotent consumers:</strong> messages can arrive twice. Processing the same event twice must be harmless.',
        '<strong>Schemas:</strong> describe events with a schema and a registry, and evolve them without breaking consumers.',
        '<strong>Dead-letter queues:</strong> messages that keep failing go aside for a person to inspect, instead of blocking the rest.',
        '<strong>Ordering:</strong> decide where order matters, and partition events by the right key, such as order ID.']), prose=True)
    b += sec('<h2>Typical tools</h2>' + table(['Need', 'Common choices'],
        [['High-volume event streams', 'Apache Kafka'], ['Work queues and routing', 'RabbitMQ'], ['Lightweight messaging', 'NATS'], ['Schemas', 'AsyncAPI, a schema registry with Avro or JSON Schema']]))
    b += pmore('event-driven') + PCTA
    page('solutions/api/event-driven.html', 'Event-Driven Integration: When to Use Events, Outbox, Idempotency | Vakratron Systems',
         'When to use events instead of API calls, and how to do event-driven integration reliably: outbox pattern, idempotent consumers, schemas, dead-letter queues and ordering.', b)

def p_sec():
    b = ghero(PHUB, PB, PP, 'api-security', 'API guide', 'API security',
              'APIs expose your business logic and data directly. The most common API breaches are not clever hacks; they are missing checks, such as letting a logged-in user read someone else\'s record by changing an ID in the URL.',
              [('Top risk', 'Broken object-level authorisation'), ('Identity', 'OAuth 2.0 / OpenID Connect'), ('Partners', 'Keys plus mTLS'), ('Know', 'Every API you expose')], 'API security')
    b += sec('<h2>The risks that matter most</h2><p class="vk-prose">Based on the OWASP API Security Top 10 (2023).</p>' + table(['Risk', 'What it looks like', 'Control'],
        [['Broken object-level authorisation', 'Change /orders/1001 to /orders/1002 and see another customer\'s order', 'Check ownership of every object in the service, not only at the gateway'],
         ['Broken authentication', 'Weak tokens, keys in URLs, no expiry', 'OAuth 2.0 / OIDC, short-lived tokens, mTLS for partners'],
         ['Excessive data exposure', 'The API returns full records and the app hides fields', 'Return only the fields the caller needs'],
         ['No rate limits', 'Scraping, brute force, cost spikes', 'Limits per caller at the gateway'],
         ['Function-level authorisation', 'A normal user can call admin endpoints', 'Separate admin APIs and check roles on every endpoint'],
         ['Improper inventory', 'Old versions and test APIs still exposed', 'An API catalogue, and retire old versions on a schedule']]))
    b += sec('<h2>Also essential</h2>' + ul([
        'Validate every input against the API contract.',
        'Log every call with caller identity, and alert on unusual patterns.',
        'Test APIs for these risks before release, not after.',
        'Keep secrets and keys out of code and front-end apps.']), prose=True)
    b += pmore('api-security') + PCTA
    page('solutions/api/api-security.html', 'API Security: OWASP API Top 10 Risks and the Controls That Stop Them | Vakratron Systems',
         'Practical API security based on the OWASP API Security Top 10: object-level authorisation, authentication, data exposure, rate limits, function-level authorisation and API inventory.', b)

def p_faq():
    qa = [('REST, GraphQL or gRPC?', '<p>REST for most public and partner APIs: widely understood and easy to cache. GraphQL when many different front-ends need different shapes of data. gRPC for fast internal service-to-service calls.</p>'),
          ('Do we need an API gateway?', '<p>If you expose APIs to partners or the internet, yes. It gives you one place for authentication, rate limits, routing and monitoring.</p>'),
          ('Do we need a service mesh?', '<p>Not usually at first. Libraries and the gateway cover most needs. A mesh such as Istio or Linkerd helps when you have many services and need consistent encryption and traffic control between them.</p>'),
          ('How do we version APIs?', '<p>Avoid breaking changes. When one is unavoidable, publish a new version, run both for an agreed period, tell callers early, and track who still uses the old one.</p>'),
          ('Can our legacy systems take part?', '<p>Yes. Wrap them with small adapters or put the gateway in front, then modernise behind that front over time.</p>'),
          ('Should we rewrite our application as microservices?', '<p>Rarely in one go. See <a href="/solutions/api/monolith-or-microservices">monolith or microservices</a>.</p>')]
    b = hero((HOME, PHUB, ("FAQ", None)), 'API guide', 'API and microservices questions, answered', 'Short answers to the questions we hear most often about APIs, integration and microservices.')
    b += sec(faqblock(qa), prose=True) + pmore('faq') + PCTA
    page('solutions/api/faq.html', 'API and Microservices FAQ: REST vs GraphQL, Gateways, Mesh, Versioning | Vakratron Systems',
         'Plain answers on APIs and microservices: REST, GraphQL or gRPC, API gateways, service meshes, versioning, legacy systems and rewrites.', b)

def p_uc():
    b = uc_hero(PHUB, 'Use case: partner APIs', 'Opening shipment-tracking APIs to 40 partners',
                'How we would help a logistics company replace file transfers and one-off integrations with a single, secure set of APIs for its retail and marketplace partners.',
                [('Partners', '~40'), ('Today', 'Files and custom links'), ('Target', 'One API, one portal'), ('Key risk', 'One partner seeing another\'s data')])
    b += sec('''<span class="vk-eyebrow">The situation</span><h2>Forty partners, forty integrations</h2>
            <p>Each retail or marketplace partner had its own integration: some received hourly CSV files over SFTP, some called an old SOAP service, two had direct database access. Adding a partner took weeks. A missed file meant customers saw stale tracking.</p>''', prose=True)
    b += sec('<span class="vk-eyebrow">The approach</span><h2>What we would do</h2>' + steps([
        '<strong>One contract:</strong> a tracking API and a webhook for status changes, designed with three friendly partners and written in OpenAPI.',
        '<strong>Gateway and portal:</strong> partner sign-up, keys, sandbox and documentation in one place.',
        '<strong>Events behind the API:</strong> status changes published once, delivered to partner webhooks with retries.',
        '<strong>Strict object checks:</strong> every request verifies that the shipment belongs to the calling partner.',
        '<strong>Migrate partners in batches,</strong> keeping the old file feeds running until each partner is live.',
        '<strong>Retire direct database access first,</strong> because it is the highest risk.']), prose=True)
    b += sec('<span class="vk-eyebrow">What changes</span><h2>Targets and how they are checked</h2>' + table(['Measure', 'Target', 'Checked by'],
        [['Time to onboard a partner', 'Days instead of weeks', 'Onboarding records'],
         ['Tracking freshness', 'Minutes instead of hours', 'Event delivery metrics'],
         ['Partners seeing others\' data', 'Never', 'Automated authorisation tests on every release']]))
    b += sec('<span class="vk-eyebrow">Trade-offs</span><h2>What we would flag</h2>' + ul([
        '<strong>Partners move at their own pace.</strong> Old feeds may need to run for months.',
        '<strong>Webhooks need care.</strong> Partners\' endpoints go down; retries and a replay option are essential.',
        '<strong>Versioning discipline matters from day one,</strong> because forty partners will depend on the contract.']), prose=True)
    b += PCTA
    page('use_cases/partner-api-logistics.html', 'Use Case: Shipment-Tracking APIs for 40 Partners | Vakratron Systems',
         'An illustrative scenario: a logistics company replacing file transfers and custom links with one secure tracking API, webhooks and a partner portal.', b)


if __name__ == '__main__':
    k_hub(); k_design(); k_gitops(); k_sec(); k_multi(); k_faq(); k_uc()
    p_hub(); p_design(); p_mono(); p_events(); p_sec(); p_faq(); p_uc()
