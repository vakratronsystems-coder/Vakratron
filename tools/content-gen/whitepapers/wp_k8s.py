"""Whitepaper content: Kubernetes and platform engineering (Oct 2026).
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
    dict(x=20, y=20, w=790, h=113, title='Teams and delivery', kind='ext'),
    dict(x=825, y=20, w=275, h=113, title='Users and partners', kind='ext'),
    dict(x=20, y=147, w=765, h=305, title='Production cluster', kind='dc'),
    dict(x=800, y=147, w=300, h=305, title='Shared platform services', kind='ent'),
  ],
  nodes={
    'portal': N(40, 60, 175, 'Developer portal', 'golden-path templates', 'grid', 'pink'),
    'git': N(243, 60, 175, 'Git repositories', 'code and config', 'git', 'slate'),
    'ci': N(446, 60, 155, 'CI pipeline', 'build, test, scan', 'flow', 'slate'),
    'reg': N(629, 60, 165, 'Image registry', 'scanned, signed', 'archive', 'pink'),
    'users': N(862, 60, 205, 'Customers and staff', 'web, mobile, APIs', 'users', 'slate'),
    'pol': N(40, 192, 185, 'Admission policy', 'Kyverno or Gatekeeper', 'shield', 'pink'),
    'gitops': N(246, 192, 190, 'GitOps controller', 'Argo CD or Flux', 'git', 'blue'),
    'gw': N(565, 192, 200, 'Ingress gateway', 'Gateway API, TLS', 'lb', 'blue'),
    'ta': N(40, 277, 225, 'Team A namespace', 'quota, network policy', 'k8s', 'blue'),
    'tb': N(290, 277, 225, 'Team B namespace', 'quota, network policy', 'k8s', 'blue'),
    'tc': N(540, 277, 225, 'Team C namespace', 'quota, network policy', 'k8s', 'blue'),
    'cp': N(40, 362, 225, 'Control plane', '3 nodes, etcd backed up', 'cog', 'violet'),
    'wk': N(290, 362, 225, 'Worker node pools', 'general, memory, GPU', 'server', 'violet'),
    'st': N(540, 362, 225, 'Persistent storage', 'CSI: Ceph or array', 'storage', 'green'),
    'obs': N(820, 192, 265, 'Observability', 'Prometheus, Loki, OpenTelemetry', 'chart', 'green'),
    'sec': N(820, 277, 265, 'Secrets', 'Vault via External Secrets', 'key', 'amber'),
    'bk': N(820, 362, 265, 'Backups', 'Velero, copies off the cluster', 'archive', 'green'),
  },
  flows=[
    dict(a='portal', b='git', kind='control', n=1),
    dict(a='git', b='ci', kind='batch', n=2),
    dict(a='ci', b='reg', kind='batch', n=3),
    dict(a='git', b='gitops', kind='control', sa=('b', 10.5), sb=('t', 0), n=4, lpos=(341, 163)),
    dict(a='gitops', b='pol', kind='control', n=5),
    dict(a='gitops', b='tb', kind='control', sb=('t', -61.5), label='sync'),
    dict(a='users', b='gw', kind='traffic', sa=('b', 0), via=[(964.5, 140), (665, 140)], sb=('t', 0), label='HTTPS', lpos=(817, 140)),
    dict(a='gw', b='tc', kind='traffic', sa=('b', 0), sb=('t', 12.5)),
    dict(a='gw', b='obs', kind='mgmt', n=6),
    dict(a='sec', b='tc', kind='control', n=7),
    dict(a='st', b='bk', kind='batch', n=8),
  ])

META = dict(
    slug='kubernetes-platform-engineering',
    title='Kubernetes and Platform Engineering: When, Why and How',
    subtitle='Deciding whether you need Kubernetes, and building a platform your teams will actually use',
    topic='k8s',
    area='Kubernetes and platform engineering',
    version='Version 1.0, October 2026',
    pages='Approx. 15 pages',
    minutes=26,
    audience='CIOs, IT heads, platform and infrastructure architects, engineering managers',
    audience_web='CIOs, IT heads, platform and infrastructure architects, and engineering managers',
    pdf_name='Vakratron-Kubernetes-Platform-Engineering.pdf',
    help_title='How we can help with Kubernetes and platform engineering',
    help_items=['<strong>Fit check and platform review:</strong> an honest view in two to three weeks of whether Kubernetes fits, or what to fix in the platform you already run.',
                '<strong>Lean platform design:</strong> cluster layout, tenancy, GitOps delivery, security baseline, sizing and a cost model, including the people needed to run it.',
                '<strong>First teams and upgrades:</strong> onboarding two or three teams onto golden paths, and setting up an upgrade routine your team can repeat.'],
    help_links=[('Book a platform review', '/advisory#assessment'), ('Kubernetes and platform engineering', '/portfolio/kubernetes-platform'), ('See an edge and central cloud design', '/deployments/edge-and-central-cloud')],
    desc='A practical whitepaper on Kubernetes and platform engineering: an honest fit test, the platform as a product, cluster design and sizing, multi-cluster and tenancy, GitOps delivery, security, observability, upgrades, golden paths, the team model, and a 36-point readiness checklist.',
    inside=['An honest fit test, including when not to use Kubernetes at all',
            'Four ways to run containers compared on effort, cost and control',
            'What a platform includes beyond the cluster, and how to run it as a product',
            'Cluster design, tenancy and when a second cluster is justified',
            'A sizing formula and a worked cost example, people included',
            'The security and upgrade routine that keeps a platform safe to run',
            'A 36-point readiness checklist for new and existing platforms'],
)

SECTIONS = []
def S(id, title, html):
    SECTIONS.append(dict(id=id, title=title, html=html))

S('summary', 'Executive summary', '''
<p>Kubernetes is very good at one job: running many services for many teams, deploying them often and scaling them automatically. It is also complex. Most of the disappointment we see does not come from Kubernetes itself. It comes from adopting it for the wrong reasons, building more platform than anyone needed, and then finding that nobody has the time or skill to keep it upgraded.</p>
<p>This paper is for the people who decide whether to invest in a container platform and have to defend that decision a year later. It covers when Kubernetes is the right answer, what a platform needs beyond the cluster, and how to run one without it becoming a second job for everybody.</p>
<div class="wp-keys"><h3>Five things to take away</h3><ol>
<li><strong>Start with an honest fit test.</strong> A handful of applications and one team rarely need Kubernetes. Virtual machines with good automation, or a managed container service, are often simpler and cheaper.</li>
<li><strong>Build a platform, not just a cluster.</strong> Developers need a working path from code to production: templates, delivery, security, monitoring and documentation. The cluster is perhaps a third of the work.</li>
<li><strong>Treat the platform as a product.</strong> It has users, a roadmap and measures of success. If developers still raise tickets to get an environment, the platform has not done its job.</li>
<li><strong>Fewer clusters, run well.</strong> One well-run production cluster beats five neglected ones. Add clusters for clear reasons, and manage them as one fleet from Git.</li>
<li><strong>Budget for day 2 from day 1.</strong> Kubernetes ships about three releases a year. Upgrades, security patches and on-call support are permanent work, and people usually cost more than the servers.</li>
</ol></div>''')

S('why-it-fails', 'Why Kubernetes platforms disappoint', '''
<p>The benefits of Kubernetes are real, but only when the platform is designed for the teams that use it and run by a team that owns it. When we review platforms that have not delivered, the same patterns appear:</p>
''' + table(['What we find', 'What it leads to'], [
    ['Adopted because everyone else did', 'Five applications, one team, and a platform that needs more care than the applications it runs.'],
    ['Clusters everywhere', 'Every team built its own cluster its own way. Nobody knows which ones are patched or who owns them.'],
    ['Upgrades nobody dares to do', 'Clusters fall three or four versions behind, lose security fixes, and an upgrade becomes a project instead of a routine.'],
    ['Developers still wait for tickets', 'The platform exists, but a namespace, a database or a DNS name still needs a request to the infrastructure team.'],
    ['Security left at defaults', 'Containers run as root, any pod can reach any other, images are never scanned and secrets sit in Git.'],
    ['Too many tools at once', 'Service mesh, three monitoring stacks and a portal in month one, before a single team is in production.'],
    ['No backup of the platform itself', 'Applications are backed up, but cluster configuration, secrets and persistent volumes are not.'],
]) + callout('In short:', 'most failed platforms were either not needed, or needed and never owned. The fix is a fit test at the start and a platform team with a clear mandate after it.'))

S('concepts', 'What a platform actually is', '''
<p>Kubernetes schedules containers across a pool of servers, restarts them when they fail, rolls out new versions gradually and scales them with load. It does this from declared desired state: you describe what should run, and controllers keep reality matching that description. That is why Git-based delivery fits it so well.</p>
<p>A cluster on its own is not a platform. A developer needs a path from code to a running, monitored, secure service without knowing how the cluster works. That path is made of several layers:</p>
''' + table(['Layer', 'What it does', 'Common choices'], [
    ['Clusters', 'Run the containers', 'Managed (EKS, AKS, GKE, OKE) or self-run (RKE2, OpenShift, Kubernetes on OpenStack, kubeadm)'],
    ['Delivery', 'Get code from Git to production safely', 'CI pipelines, Argo CD or Flux, Helm or Kustomize'],
    ['Images', 'Store, scan and sign container images', 'Harbor, Trivy, cosign'],
    ['Networking', 'Route traffic in and between services', 'Gateway API or ingress controller, Cilium or Calico'],
    ['Security', 'Limit what can run and what it can reach', 'RBAC, network policies, Kyverno or OPA Gatekeeper, Vault'],
    ['Observability', 'Metrics, logs and traces per team', 'Prometheus, Grafana, Loki, OpenTelemetry'],
    ['Developer experience', 'Self-service templates and documentation', 'Backstage or a simple internal portal'],
], 'wp-compact') + '''
<h3>The platform as a product</h3>
<p>Platform engineering means running these layers as an internal product. The platform team has customers (the development teams), a backlog, release notes and service levels. Its success is measured by what developers can do without asking: how long it takes a new service to reach production, how often teams deploy, how many deployments fail, and how quickly they recover. Those four measures are the DORA metrics, and they are a better test of a platform than the number of clusters or tools.</p>
<h3>Golden paths</h3>
<p>A golden path is a supported, documented way to do a common job, such as &ldquo;a Java API with a PostgreSQL database&rdquo; or &ldquo;a scheduled batch job&rdquo;. One template creates the repository, pipeline, deployment configuration, namespace, dashboards and alerts, with security settings already correct. Teams can leave the path, but the easy way and the right way are the same. Two or three good paths cover most of the work in a typical enterprise.</p>''')

S('options', 'The main options compared', '''
<p>There are four realistic ways to run containerised applications. The right choice depends on how many services and teams you have, where they must run, and how much platform work you are willing to own.</p>
''' + table(['Option', 'Best for', 'Effort to run', 'Watch out for'], [
    ['Virtual machines with automation (Ansible, Terraform, Packer)', 'A handful of applications, stable release pace, existing VM skills', 'Low to moderate', 'Slower environments and scaling; drift if automation is not enforced'],
    ['Managed container service or PaaS (ECS, Azure Container Apps, Cloud Run)', 'Small teams in one public cloud who want containers without a cluster', 'Low', 'Provider-specific features; limits on networking and tenancy'],
    ['Managed Kubernetes (EKS, AKS, GKE, OKE)', 'Many services and teams in public cloud', 'Moderate: provider runs the control plane, you run the rest', 'Cloud cost; you still own add-ons, upgrades of nodes and add-ons, and security'],
    ['Self-run Kubernetes (RKE2, OpenShift, Kubernetes on OpenStack or bare metal)', 'On-premises, private cloud, strict data rules, GPUs, edge sites', 'High: you run everything, including the control plane and etcd', 'Upgrade discipline, on-call ownership, hardware replacement'],
], 'wp-compact') + '''
<h3>Managed or self-run</h3>
<p>In public cloud, managed Kubernetes is almost always the right start. The provider runs and upgrades the control plane, and the platform team concentrates on what developers see. On-premises, in a private cloud or where data must stay in a specific place, you run Kubernetes yourself. Choose a well-supported distribution with a documented upgrade path, and plan for the people to run it before you buy hardware.</p>
<h3>Where Kubernetes runs on-premises</h3>
''' + ul(['<strong>On OpenStack:</strong> clusters built by Cluster API or Magnum, with Cinder for volumes and Octavia for load balancers. Good when tenants of an existing private cloud want clusters on demand.',
          '<strong>On VMware or KVM virtual machines:</strong> the simplest on-premises start, using familiar operations, with some overhead from the virtualisation layer.',
          '<strong>On bare metal:</strong> the best performance and direct GPU access. Needs MetalLB or similar for load balancers and a plan for replacing failed servers.']))

S('fit', 'Do you need Kubernetes? A fit test', '''
<p>Ask these five questions before committing. They take an afternoon and save months.</p>
<ol class="wp-steps">
<li><strong>How many services, and how many teams?</strong> Below roughly ten services and two teams, the platform overhead usually outweighs the benefit. Above thirty services or five teams, a shared platform starts to pay for itself.</li>
<li><strong>How often do you release?</strong> If most applications change monthly or less, automated VMs are enough. If teams want to deploy daily, independently, Kubernetes and GitOps help a great deal.</li>
<li><strong>Does load vary sharply?</strong> Festive sales, results days, month-end runs and campaign launches are where automatic scaling earns its keep.</li>
<li><strong>Where must it run?</strong> Public cloud only points to managed Kubernetes or a container service. On-premises, several sites or edge locations point to a self-run distribution with fleet management.</li>
<li><strong>Who will run it?</strong> If you cannot name at least two people who will own the platform, upgrade it and carry the pager, start with something simpler or a managed service.</li>
</ol>
''' + table(['Your situation', 'Usual answer'], [
    ['Under 10 services, 1 or 2 teams, monthly releases', 'Automated VMs or a managed container service'],
    ['10 to 30 services, a few teams, public cloud', 'Managed Kubernetes, one production cluster, lean add-ons'],
    ['30+ services, many teams, on-premises or regulated data', 'Self-run distribution, a platform team, golden paths'],
    ['Many edge or branch sites', 'Small standard clusters managed centrally from Git'],
    ['GPU training and inference', 'Kubernetes with GPU node pools, or a dedicated scheduler for large training jobs'],
]) + callout('Not every workload belongs on the platform.', 'Large commercial databases, licence-bound software and appliances are often better on VMs or managed services even when everything else moves. Decide per workload, not per organisation.', 'warn'))

S('architecture', 'Reference architecture', '''
<p>The diagram shows a lean production platform. Developers never change the cluster directly. Code goes through CI, images through the registry, and everything the cluster runs, including policies and add-ons, comes from Git.</p>
[[DIAGRAM]]
<p class="wp-caption">Numbered flows: (1) a team creates a new service from a portal template, which sets up the repository and configuration, (2) CI builds and tests on every merge, (3) images are scanned, signed and pushed to the private registry, (4) the GitOps controller watches Git, (5) every change passes admission policy before it is accepted, (6) traffic, metrics, logs and traces go to shared observability, (7) secrets come from Vault at run time, never from Git, (8) cluster resources and volumes are backed up off the cluster.</p>
<h3>Cluster design</h3>
''' + ul(['<strong>Control plane:</strong> three nodes, so it survives one failure and can be upgraded one node at a time. Back up etcd on a schedule and test the restore.',
          '<strong>Node pools:</strong> separate pools for general workloads, memory-heavy workloads and GPUs, with labels and taints so work lands in the right place.',
          '<strong>Networking:</strong> a CNI that enforces network policies (Cilium or Calico), Gateway API or an ingress controller for inbound traffic, and an agreed IP plan that does not clash with the corporate network.',
          '<strong>Storage:</strong> a CSI driver for your storage, such as Ceph via Rook, a vendor array or cloud volumes, with storage classes per performance tier.']) + '''
<div class="keep"><h3>GitOps delivery</h3>
<p>With GitOps, Git is the single source of truth for what runs. A controller such as Argo CD or Flux watches Git and keeps the cluster matching it. Deployments become pull requests and rollbacks become reverts, and every change is reviewed and recorded.</p></div>
''' + ul(['Keep application code and deployment configuration separate, in different repositories or folders.',
          'Promote between environments through Git, using the same image, never by rebuilding.',
          'Turn on automatic drift correction and pruning in non-production first, then in production once teams trust it.',
          'Use progressive delivery (Argo Rollouts or Flagger) for services where a bad release is expensive.']) + '''
<h3>Tenancy and multiple clusters</h3>
<p>Inside a cluster, give each team and environment a namespace with resource quotas, default-deny network policies and role bindings from your identity provider, all created from a template. Where tenants need stronger isolation, for example separate customers on a SaaS platform, virtual clusters (vCluster) or separate node pools add a further boundary. Add a whole cluster only for a clear reason:</p>
''' + table(['Reason for another cluster', 'Usually worth it?'], [
    ['Separate production from non-production', 'Yes'],
    ['Data must stay in a specific location', 'Yes'],
    ['Users in two regions, or disaster recovery', 'Yes'],
    ['Edge or plant sites that must run when the WAN is down', 'Yes, as small standard clusters'],
    ['Each team wants its own', 'No: use namespaces, quotas and policies'],
    ['One application cannot upgrade yet', 'No: fix the application; old clusters become a risk'],
]) + '''
<p>When there are several clusters, manage them as one fleet: build every cluster from the same code (Cluster API, Terraform or your distribution&rsquo;s tooling), apply the same baseline add-ons and policies from Git, for example with Argo CD ApplicationSets, send all telemetry to one place, and upgrade in waves.</p>''')

S('sizing', 'Sizing and cost', '''
<div class="keep"><h3>Worker capacity</h3>
<p>Size from what pods request at peak, not from what servers cost. A first estimate:</p>
<div class="wp-formula">Worker nodes = (peak pod requests + platform add-ons) &divide; target utilisation &divide; allocatable per node, rounded up, + 1 spare node</div></div>
<p>Work it out for CPU and memory separately and take the larger answer. The spare node lets the cluster survive one node failure and still have room for rolling updates. Target utilisation of 65 to 75 percent leaves headroom for spikes and for the scheduler to place pods.</p>
<h3>A worked example</h3>
<p>A retailer runs 30 services. At festive peak they average 4 replicas each, so 120 pods, each requesting 0.5 vCPU and 1 GiB of memory. Platform add-ons (ingress, GitOps, policy, monitoring, logging agents) need about 10 vCPU and 24 GiB.</p>
''' + table(['Step', 'CPU', 'Memory'], [
    ['Application pods at peak', '120 &times; 0.5 = 60 vCPU', '120 &times; 1 = 120 GiB'],
    ['Plus platform add-ons', '60 + 10 = 70 vCPU', '120 + 24 = 144 GiB'],
    ['At 70% target utilisation', '70 &divide; 0.7 = 100 vCPU', '144 &divide; 0.7 &asymp; 206 GiB'],
    ['Nodes of 16 vCPU, 64 GiB (about 15 vCPU, 58 GiB allocatable)', '100 &divide; 15 = 6.7, so 7', '206 &divide; 58 = 3.6, so 4'],
    ['Production workers (larger figure + 1 spare)', '7 + 1 = 8 nodes', 'CPU sets the size'],
], 'wp-compact') + '''
<p>Add three small control plane nodes if self-run, and a non-production cluster at roughly half the size. Outside the festive season, the cluster autoscaler can drop production to five or six workers, which is where the efficiency gain shows up.</p>
<h3>What it costs to run, per year</h3>
''' + table(['Item', 'Planning range (managed Kubernetes, Indian cloud region)'], [
    ['Production workers: 8 nodes at about &#8377;45,000 to &#8377;60,000 per month each', '&#8377;43 to &#8377;58 lakh'],
    ['Non-production: 4 nodes of the same size', '&#8377;22 to &#8377;29 lakh'],
    ['Control plane fees, load balancers, storage, log retention', '&#8377;12 to &#8377;22 lakh'],
    ['Optional support subscriptions for distribution or tools', '&#8377;0 to &#8377;40 lakh'],
    ['Platform team: 3 engineers, fully loaded', '&#8377;75 lakh to &#8377;1.2 crore'],
    ['<strong>Total</strong>', '<strong>About &#8377;1.5 to &#8377;2.5 crore</strong>'],
], 'wp-compact') + '''
<p>These are planning ranges, not quotes. Reserved or committed-use pricing usually cuts compute by 30 to 40 percent; on-premises hardware moves the cost into capital spend over three to five years. Notice that people are the largest single line. That is normal, and it is why the fit test asks who will run the platform before anything else.</p>
''' + callout('Does Kubernetes save money?', 'It can, by packing workloads more tightly and scaling down when idle. But it adds platform and people cost. The bigger gains are usually faster, safer releases and less time spent on environments, so measure those too.'))

S('security', 'Security and governance', '''
<p>Out of the box, Kubernetes is permissive: containers can run as root and any pod can reach any other. A small set of controls, applied by default from templates and enforced at admission, closes most of the gaps. Keeping clusters upgraded closes most of the rest.</p>
''' + table(['Control', 'What it does', 'Common choices'], [
    ['Access control', 'People and pipelines get only the permissions they need', 'RBAC bound to identity provider groups via OIDC, no shared admin accounts'],
    ['Namespaces and quotas', 'Teams are separated and cannot use up the cluster', 'One namespace per team and environment, from a template'],
    ['Network policies', 'Pods only talk to what they need to', 'Default deny, then allow, with Cilium or Calico'],
    ['Pod security', 'Blocks root containers and risky settings', 'Pod Security Standards at the restricted level'],
    ['Policy engine', 'Enforces your rules whenever anything is created', 'Kyverno or OPA Gatekeeper'],
    ['Secrets', 'Keeps passwords and keys out of Git and images', 'Vault or a cloud secret store via External Secrets'],
    ['Audit and runtime', 'Records changes and spots unusual behaviour', 'API audit logs to your SIEM, Falco'],
    ['Benchmarks', 'Checks clusters against known good settings', 'CIS Kubernetes Benchmark with kube-bench'],
], 'wp-compact') + '''
<h3>Software supply chain</h3>
<p>Attackers increasingly target the delivery pipeline rather than the running system. Protect the path from code to cluster:</p>
''' + ul(['Build images only in CI, from approved base images, and generate a software bill of materials (SBOM) for each.',
          'Scan images for known vulnerabilities on build and again on a schedule, because new CVEs appear after release.',
          'Sign images with cosign and have admission policy reject anything unsigned or from an unknown registry.',
          'Protect the CI system and Git itself: branch protection, required reviews, and short-lived credentials for pipelines.']) + '''
<h3>Governance without tickets</h3>
<p>Write policies as code, test them in CI like any other change, and run new policies in audit mode for a few weeks before enforcing them. Map controls to your obligations, such as CERT-In 6-hour incident reporting, which needs audit logs you can search quickly, and the DPDP Act, which needs you to know where personal data lives. Sector regulators such as RBI, SEBI and IRDAI expect evidence of access control, change records and patching; a GitOps platform produces most of that evidence as a side effect.</p>''')

S('operating', 'Operating it: day 2', '''
<h3>Observability</h3>
<p>Each team should see its own metrics, logs and alerts, so problems are found by the people who can fix them. Collect metrics with Prometheus, logs with Loki or your existing log platform, and traces with OpenTelemetry, and give every golden-path service a standard dashboard. Alert on what users feel, error rate and latency against a service level objective, not on every CPU spike. The platform team watches the platform itself: control plane health, etcd latency, node pressure, certificate expiry and GitOps sync failures.</p>
<h3>Upgrades as a routine</h3>
<p>Kubernetes ships about three minor versions a year, and each is supported upstream for roughly fourteen months. Managed services follow a similar window. A cluster more than two versions behind is hard to upgrade and is losing security fixes.</p>
''' + ul(['Upgrade on a calendar, every four to six months: non-production first, a short soak, then production.',
          'Check manifests for deprecated APIs before each upgrade, with tools such as Pluto or kubent, so applications do not break.',
          'Upgrade add-ons (CNI, ingress, GitOps, policy engine) on the same rhythm; they drift faster than the cluster.']) + '''
<h3>Backup and recovery</h3>
<p>Because cluster state lives in Git, most of a cluster can be rebuilt from code. What Git does not hold must be backed up: etcd snapshots, persistent volumes, and secrets that are not in an external store. Velero handles cluster resources and volumes, with copies kept off the cluster and ideally immutable. Rebuild a non-production cluster from scratch at least twice a year to prove it works.</p>
<h3>The team model</h3>
<p>A small platform on managed Kubernetes can be run by two or three engineers with good automation. A self-run, multi-cluster platform needs a dedicated team of four to eight, with on-call cover. Keep the split clear: the platform team owns clusters, add-ons, golden paths and upgrades; application teams own their services, their alerts and their on-call. A platform team that also runs everyone&rsquo;s applications becomes a bottleneck, which is exactly what platform engineering is meant to remove.</p>''')

S('roadmap', 'A practical roadmap', '''
<p>A first platform does not need to be big. It needs to be used. The pace is set by how quickly the first teams move real services, not by building the cluster.</p>
''' + table(['Stage', 'Typical duration', 'Outcome'], [
    ['1. Fit check', '2 to 3 weeks', 'Applications, teams, release pace and skills reviewed. A clear yes, no, or not yet, with the option chosen.'],
    ['2. Lean first platform', '6 to 10 weeks', 'One production and one non-production cluster, GitOps delivery, baseline security, monitoring, one golden path.'],
    ['3. First teams on board', '6 to 8 weeks', 'Two or three willing teams move real services and help shape the templates and documentation.'],
    ['4. Harden', '4 to 6 weeks', 'Policies enforced, image signing, backups tested, first planned upgrade done, on-call in place.'],
    ['5. Scale out', 'Ongoing, by quarter', 'More teams and golden paths, self-service portal, extra clusters only where a reason exists.'],
    ['6. Hand over', '4 weeks, overlapping', 'Runbooks, upgrade practice and platform backlog owned by your platform team.'],
]))

S('mistakes', 'Ten common mistakes', '<ol class="wp-steps">' + ''.join('<li>' + m + '</li>' for m in [
    '<strong>Adopting Kubernetes for a handful of applications.</strong> The platform becomes the biggest system you run.',
    '<strong>Building the cluster and calling it a platform.</strong> Developers still need delivery, templates and monitoring.',
    '<strong>One cluster per team.</strong> Patching and upgrading multiply; namespaces would have done the job.',
    '<strong>Falling behind on versions.</strong> Each skipped upgrade makes the next one harder and riskier.',
    '<strong>Changing clusters by hand.</strong> Changes made outside Git are lost or quietly overwritten.',
    '<strong>Leaving security at defaults.</strong> Root containers, open east-west traffic and unscanned images.',
    '<strong>Secrets in Git or in images.</strong> They are copied everywhere and almost impossible to rotate.',
    '<strong>Too many tools in the first months.</strong> A service mesh and three dashboards before the first team goes live.',
    '<strong>No resource requests or limits.</strong> One noisy service starves the rest and capacity planning becomes guesswork.',
    '<strong>No named platform owner.</strong> Without a team that owns upgrades and on-call, the platform slowly decays.']) + '</ol>')

CHECKLIST = [
  ('Fit and ownership', ['Fit test done, with service count, team count and release pace written down',
                  'Option chosen (VMs, container service, managed or self-run Kubernetes) with the reason recorded',
                  'Named platform owner and at least two engineers who carry the pager',
                  'Platform success measures agreed, such as lead time and deployment frequency',
                  'Workloads that stay off the platform listed, with reasons',
                  'Running cost, including people, approved for three years']),
  ('Cluster design', ['Production and non-production on separate clusters',
                  'Three control plane nodes, with etcd backups restored in a test',
                  'Worker capacity sized from peak requests, with one spare node',
                  'Separate node pools for general, memory-heavy and GPU workloads where needed',
                  'Pod and service IP ranges agreed with the network team',
                  'Storage classes defined per performance tier through a CSI driver']),
  ('Delivery and GitOps', ['Everything the cluster runs, including add-ons and policies, comes from Git',
                  'Application code and deployment configuration kept separate',
                  'Promotion between environments through Git, using the same image',
                  'Rollback by reverting a commit, practised at least once',
                  'Drift correction turned on, starting with non-production',
                  'Every cluster built from the same code']),
  ('Security', ['RBAC bound to identity provider groups, with no shared admin accounts',
                  'Default-deny network policies in every namespace',
                  'Pod Security Standards enforced at the restricted level',
                  'Images scanned on build and on a schedule, and signed',
                  'Admission policy rejects unsigned images and unknown registries',
                  'Secrets held in Vault or a cloud store, never in Git',
                  'API audit logs sent to the SIEM and searchable within hours']),
  ('Operations and day 2', ['Each team sees its own dashboards, logs and alerts',
                  'Alerts based on service level objectives, not raw resource use',
                  'Upgrade calendar set, with no cluster more than two versions behind',
                  'Deprecated APIs checked before every upgrade',
                  'Velero backups kept off the cluster and restored in a test',
                  'A non-production cluster rebuilt from code twice a year']),
  ('Developer experience', ['At least one golden path from template to production',
                  'A new service reaches production without a ticket',
                  'Platform documentation kept next to the templates and up to date',
                  'Resource requests and limits set by default in templates',
                  'Platform backlog reviewed with application teams every quarter']),
]
n_items = sum(len(i) for _, i in CHECKLIST)
S('checklist', 'Platform readiness checklist (' + str(n_items) + ' points)',
  '<p>Use this list to score a planned platform or one you already run. Anything you cannot tick with evidence is a gap worth closing.</p><div class="wp-check">' +
  ''.join('<div class="wp-check-group"><h3>' + g + '</h3><ul>' + ''.join('<li>' + i + '</li>' for i in items) + '</ul></div>' for g, items in CHECKLIST) + '</div>')

S('glossary', 'Glossary', table(['Term', 'Meaning'], [
    ['Pod', 'The smallest unit Kubernetes runs: one or more containers that share network and storage.'],
    ['Namespace', 'A named section of a cluster used to separate teams or environments, with its own quotas and permissions.'],
    ['Control plane and etcd', 'The components that manage the cluster; etcd is the database that holds all cluster state.'],
    ['GitOps', 'Running systems from declared state in Git, with a controller that keeps the cluster matching it.'],
    ['Admission policy', 'Rules checked when anything is created or changed in the cluster, such as rejecting unsigned images.'],
    ['CNI and CSI', 'Plug-in interfaces for container networking and for storage.'],
    ['Golden path', 'A supported, documented template for a common job, from repository to production.'],
    ['SBOM', 'Software bill of materials: a list of the components and versions inside an image.'],
    ['DORA metrics', 'Lead time for changes, deployment frequency, change failure rate and time to restore service.'],
]))
