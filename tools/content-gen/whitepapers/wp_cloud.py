"""Whitepaper content: Private and hybrid cloud strategy (Oct 2026).
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
DIAGRAM = dict(w=1120, h=465,
  zones=[
    dict(x=20, y=20, w=745, h=120, title='Users, identity and network', kind='ext'),
    dict(x=780, y=20, w=320, h=430, title='Public cloud landing zone', kind='cloud'),
    dict(x=20, y=154, w=235, h=296, title='VMware (retiring)', kind='ext', dashed=True),
    dict(x=270, y=154, w=495, h=296, title='Private cloud: OpenStack on KVM', kind='dc'),
  ],
  nodes={
    'idp': N(35, 62, 205, 'Directory and SSO', 'one identity, both clouds', 'key', 'slate'),
    'users': N(285, 62, 220, 'Users and teams', 'portal, API, Terraform', 'users', 'slate'),
    'wan': N(535, 62, 210, 'WAN and internet', 'branches, partners, users', 'globe', 'slate'),
    'vs': N(35, 199, 205, 'vSphere cluster', 'source VMs, rollback copy', 'vm', 'slate', state='off'),
    'v2v': N(35, 284, 205, 'virt-v2v toolkit', 'convert, test, cut over', 'flow', 'amber'),
    'vbk': N(35, 369, 205, 'Existing backup', 'protects VMware to the end', 'archive', 'slate'),
    'ctl': N(285, 199, 220, 'Control plane', '3 nodes: APIs, DB, queue', 'cog', 'blue'),
    'gw': N(535, 199, 210, 'OVN gateways', 'routing in and out', 'switch', 'blue'),
    'cmp': N(285, 284, 220, 'KVM compute nodes', 'N+1 spare, live migration', 'server', 'blue'),
    'bk': N(535, 284, 210, 'Backup target', 'immutable, own credentials', 'lock', 'pink'),
    'ceph': N(285, 369, 460, 'Ceph storage cluster', 'RBD block and RGW object, three copies', 'storage', 'green'),
    'lz': N(800, 62, 280, 'Guardrails', 'approved regions, encryption, tags', 'shield', 'amber'),
    'hub': N(800, 199, 280, 'Hub network and firewall', 'shared egress, private link in', 'firewall', 'amber'),
    'wl': N(800, 284, 280, 'Workload accounts', 'production, non-production, sandbox', 'cloud', 'amber'),
    'log': N(800, 369, 280, 'Central logging and cost', 'audit trail, budgets, tag reports', 'chart', 'amber'),
  },
  flows=[
    dict(a='users', b='ctl', kind='control', label='self-service', n=1, lpos=(395, 147)),
    dict(a='idp', b='ctl', kind='control', sa='r', via=[(262, 91), (262, 228)], sb='l'),
    dict(a='ctl', b='cmp', kind='control', label='schedule', n=2, lpos=(395, 270)),
    dict(a='cmp', b='ceph', kind='data', sb=('t', -120), label='VM disks', n=3, lpos=(395, 355)),
    dict(a='ceph', b='bk', kind='batch', sa=('t', 125), sb='b', label='nightly', n=4, lpos=(640, 355)),
    dict(a='wan', b='gw', kind='traffic', both=True),
    dict(a='gw', b='hub', kind='traffic', both=True, n=5),
    dict(a='lz', b='hub', kind='control'),
    dict(a='hub', b='wl', kind='traffic'),
    dict(a='wl', b='log', kind='mgmt'),
    dict(a='vs', b='v2v', kind='data'),
    dict(a='v2v', b='cmp', kind='data', n=6),
  ])

META = dict(
    slug='private-cloud-strategy',
    title='Private Cloud Without the Lock-in',
    subtitle='Deciding what runs where, building a private cloud on OpenStack, KVM and Ceph, leaving VMware in planned waves, and running hybrid',
    topic='cloud',
    area='Private and hybrid cloud',
    version='Version 1.0, October 2026',
    pages='Approx. 15 pages',
    minutes=27,
    audience='CIOs, IT heads, infrastructure and cloud architects, finance partners',
    audience_web='CIOs, IT heads, infrastructure and cloud architects, and the finance partners who sign off',
    pdf_name='Vakratron-Private-Cloud-Strategy.pdf',
    help_title='How we can help with private and hybrid cloud',
    help_items=['<strong>Cloud assessment:</strong> from your VM inventory export, a placement for every application, a five-year cost model and a migration order, in three to four weeks.',
                '<strong>Private cloud design:</strong> OpenStack, KVM and Ceph reference design, sizing, network plan, bill of materials and an upgrade plan your team can own.',
                '<strong>VMware exit plan:</strong> dependency-based waves, pilot wave, rollback rules and licence checks, with support through the first production waves.'],
    help_links=[('Ask for a cloud assessment', '/advisory#assessment'), ('Cloud solutions', '/portfolio/cloud-solutions'), ('See a worked private cloud move', '/deployments/public-to-private-cloud')],
    desc='A practical whitepaper on private and hybrid cloud: deciding what runs where, five-year cost with egress and licences, an OpenStack, KVM and Ceph reference design, leaving VMware in waves with rollback, landing zones, day-2 operations, FinOps and a 36-point checklist.',
    inside=['A five-question framework for deciding which workloads belong in private, public or hybrid cloud',
            'Private, public, hybrid and multi-cloud compared on cost, control and the skills each needs',
            'An OpenStack, KVM and Ceph reference design with starting sizes and the decisions that matter',
            'Compute, storage and five-year cost formulas with a worked 300-VM example, egress and licences included',
            'A wave-by-wave method for leaving VMware, with a rollback at every step',
            'Landing zones, upgrades and FinOps: running both clouds after go-live',
            'A 36-point checklist you can use with your team'],
)

SECTIONS = []
def S(id, title, html):
    SECTIONS.append(dict(id=id, title=title, html=html))

S('summary', 'Executive summary', '''
<p>Most organisations now run some workloads in a public cloud and some on infrastructure they control, and many are being pushed to rethink the second half by a VMware renewal. The question is no longer &ldquo;cloud or not&rdquo;. It is which workload runs where, at what five-year cost, and how to move without outages.</p>
<p>This paper covers placement, cost, a private cloud built on OpenStack, KVM and Ceph, a safe exit from VMware, and the landing zone and operating model that keep a hybrid estate under control.</p>
<div class="wp-keys"><h3>Five things to take away</h3><ol>
<li><strong>Decide placement per workload, in writing.</strong> Load shape, data movement, regulation, managed services and team skills decide where it belongs. A blanket &ldquo;cloud first&rdquo; or &ldquo;all private&rdquo; policy is usually the expensive answer.</li>
<li><strong>Compare five-year cost, not first-year cost.</strong> Include people, data egress, licences, support and hardware refresh. Large, steady 24x7 estates often cost 25 to 40 percent less on a well-run private cloud; spiky or short-lived work is usually cheaper in public cloud.</li>
<li><strong>Private cloud means self-service, not just virtualisation.</strong> OpenStack on KVM with Ceph gives teams an API and portal on hardware you own, with no hypervisor licence. It needs a small skilled team and a firm upgrade habit.</li>
<li><strong>Leave VMware in waves, with a way back.</strong> Move dependency groups together, test side by side, and keep the source VM intact until the application owner signs off.</li>
<li><strong>Build the guardrails before the workloads.</strong> One identity, a landing zone, central logging and mandatory tags take a few weeks up front, and far longer if retrofitted.</li>
</ol></div>''')

S('why-it-fails', 'Why cloud programmes disappoint', '''
<p>Cloud programmes rarely fail with an outage. They disappoint slowly: the bill beats the business case, the private platform is feared, or the migration stalls at 60 percent. The causes are familiar.</p>
''' + table(['What we find', 'What it leads to'], [
    ['Lift and shift with no right-sizing', 'VMs move as they were, sized for peak and running 24x7. The first annual bill is 1.5 to 2 times the estimate.'],
    ['A renewal date driving the plan', 'The renewal quote arrives months before the date. The exit is rushed, or three more years are signed with no plan.'],
    ['Accounts opened team by team', 'Nobody can say who has access to what, where the audit logs are, or whose costs are whose.'],
    ['A private cloud nobody can run', 'Installed by a vendor and handed over without runbooks. Upgrades are postponed until support ends.'],
    ['Data movement not costed', 'Applications that send large volumes out, or talk constantly across the link, cost more than their VMs.'],
    ['Hybrid without design', 'Connectivity, DNS and identity were assumed rather than designed. Applications break in confusing ways after migration.'],
]) + callout('In short:', 'most cloud problems are decisions that were never made explicitly: where each workload belongs, what it really costs, and who runs the platform afterwards.'))

S('concepts', 'Placement, cost and lock-in, explained properly', '''
<h3>What makes a private cloud a cloud</h3>
<p>A virtualised data centre is not a private cloud. The difference is self-service: teams create their own VMs, networks and volumes through a portal or an API, within quotas, without raising a ticket. Projects are isolated, usage is metered, and everything can be built from code. If you only need to run VMs reliably and nobody will use an API, a simpler KVM platform such as Proxmox VE is often the better choice.</p>
<h3>Workload shape decides cost</h3>
<p>Public cloud charges for every hour a resource exists. A VM that runs a few hours a day is cheap there. A database running 24x7 at steady load pays the provider&rsquo;s margin every hour for five years. Most enterprise estates are dominated by the second kind.</p>
<h3>Data gravity and egress</h3>
<p>Public clouds charge little to bring data in and charge per gigabyte to send it out. Large datasets also take days or weeks to copy. Keep data close to the applications that use it most, and cost every flow that crosses a cloud boundary.</p>
<h3>Four kinds of lock-in</h3>
''' + table(['Kind', 'Example', 'How to limit it'], [
    ['Licence', 'Hypervisor subscription bundles, per-core database licences', 'Open hypervisor (KVM); check terms before placing databases'],
    ['Data', 'Hundreds of terabytes in one provider&rsquo;s object storage', 'Keep a copy or an exit plan for critical data'],
    ['Service', 'Applications built on a provider-only queue, database or AI service', 'Use managed services where the value is worth the dependence'],
    ['Skills and tooling', 'Everything built by clicking in one console', 'Infrastructure as code; open monitoring and logging tools'],
], 'wp-compact') + callout('Some lock-in is a fair price.', 'A managed database you would never want to run yourself is worth some dependence. Choose lock-in knowingly.'))

S('patterns', 'The options compared', '''
<p>Most organisations end up using two or three of these models for different parts of the estate.</p>
''' + table(['Model', 'What it means', 'Strong at', 'Watch out for'], [
    ['Private cloud', 'Self-service cloud on hardware you own or lease', 'Steady workloads, data that must stay put, predictable cost over 3 to 5 years', 'Needs a team that can run and upgrade it; capacity must be bought ahead of demand'],
    ['Public cloud', 'AWS, Azure, OCI or similar, by the hour or on 1 to 3 year commitments', 'Spiky or uncertain load, fast start, managed databases, analytics and AI services', 'Cost grows quietly; egress and always-on VMs add up; governance must be built'],
    ['Hybrid cloud', 'Private and public joined by private links, one identity and DNS', 'Keeping core data at home while using public cloud where it is stronger', 'Connectivity, identity and DNS must be designed, not assumed'],
    ['Multi-cloud', 'More than one public cloud', 'A service only one provider offers well, or a customer requirement', 'Every extra cloud multiplies the guardrails, tools and skills to maintain'],
], 'wp-compact') + '''
<h3>Choosing the private platform</h3>
<p>For the private side, the right platform depends on how much self-service you need and what your team can operate.</p>
''' + table(['Platform', 'Best for', 'Trade-off'], [
    ['OpenStack on KVM with Ceph', 'Multi-tenant, API-driven cloud for several teams; 100 to several thousand VMs', 'The most capable option, and the most to learn; needs a disciplined upgrade process'],
    ['Proxmox VE', 'Running VMs reliably for one IT team, from a handful of hosts to a few dozen', 'Simple to run; limited multi-tenancy and self-service API'],
    ['OpenShift Virtualization', 'Teams standardised on Kubernetes wanting VMs and containers together', 'Subscription cost; VM operations follow Kubernetes patterns'],
    ['A small remaining vSphere island', 'Appliances and vendor applications only supported on VMware', 'Keeps a licence, so keep it small and review it every year'],
]))

S('choosing', 'Deciding what runs where', '''
<p>Decide placement per application, with a one-line reason agreed by its owner (&ldquo;private: steady load, payment data must stay in India&rdquo;). Five questions cover almost every case:</p>
<ol class="wp-steps">
<li><strong>What is the shape of the load?</strong> Steady and 24x7 points to private. Seasonal, short-lived or fast-growing points to public.</li>
<li><strong>How much data moves, and where to?</strong> If it sends many terabytes a month out, cost the egress first. Keep chatty applications next to the systems they talk to.</li>
<li><strong>What do regulators and contracts require?</strong> Some data must stay in India, some on infrastructure you control, some needs audit rights over the provider.</li>
<li><strong>Does it rely on managed services?</strong> An application built on a provider&rsquo;s managed database or AI service belongs there, unless you will rebuild it.</li>
<li><strong>Who will run it?</strong> A private platform needs Linux, networking and automation skills. Without them, public cloud or a managed private cloud is safer.</li>
</ol>
<p>A typical estate comes out mixed:</p>
''' + table(['Workload', 'Typical placement', 'Main reason'], [
    ['ERP, core banking, hospital information system', 'Private', 'Steady 24x7 load, regulated data, heavy integration'],
    ['Customer website and mobile back end', 'Public, or hybrid with data private', 'Spiky traffic, content delivery networks, fast release cycles'],
    ['Data warehouse and analytics', 'Depends on data volume', 'Managed analytics is attractive; moving large data out is not'],
    ['Development and test', 'Public, scheduled off out of hours', 'Needed about 60 hours a week, not 168'],
    ['Backup and long-term archive', 'Second site or public object storage', 'Cheap capacity, separate failure domain; cost the restore egress'],
    ['GPU training bursts', 'Public or GPU cloud, then private for the steady base', 'Learn real usage before buying hardware'],
]))

S('architecture', 'Reference architecture', '''
<p>The diagram shows a hybrid estate during a VMware exit. A private cloud on OpenStack, KVM and Ceph runs the steady core; a public cloud landing zone runs what belongs there; both use one directory for sign-in. VMware shrinks until the last wave is signed off.</p>
[[DIAGRAM]]
<p class="wp-caption">Numbered flows: (1) teams request VMs, networks and volumes through the portal, API or Terraform, signing in with their directory account; (2) the control plane places each VM on a compute node with room; (3) VM disks live on Ceph, not on the compute node, which makes live migration and fast recovery from a failed host possible; (4) backups go nightly to a separate, immutable target; (5) a private link such as Direct Connect, ExpressRoute or FastConnect joins the data centre to the cloud hub, with an IPsec VPN as backup; (6) VMs are converted from vSphere with virt-v2v and moved in waves.</p>
<h3>Starting sizes for a first private cloud</h3>
''' + table(['Role', 'Starting point', 'Why'], [
    ['Control nodes', '3', 'The database and queue need a majority to survive one node failing or being upgraded.'],
    ['Compute nodes', 'Sized from inventory, plus 1 spare', 'Lets you patch or lose one host without running out of room.'],
    ['Ceph storage nodes', '3 minimum, 5 or more preferred', 'Three copies need three nodes; more nodes mean gentler recovery after a failure.'],
    ['Networks', 'Management, storage, tenant overlay, external', 'Storage on its own network; 25 GbE to each server is a common baseline.'],
]) + '''
<h3>Decisions that make or break it</h3>
''' + ul(['<strong>Choose the deployment tool for the next five years.</strong> Kolla-Ansible, OpenStack-Ansible and commercial distributions all work, if your team can upgrade with them.',
          '<strong>Design networks before installing anything.</strong> VLAN ranges, overlay networks, external IP ranges, MTU and an IP plan that does not clash with the cloud are painful to change later.',
          '<strong>Size Ceph for recovery, not just capacity.</strong> When a node fails, Ceph rebuilds its copies onto the remaining nodes. Leave free space and network capacity for that to happen without hurting users.',
          '<strong>Add the services teams expect.</strong> Load balancing (Octavia), DNS (Designate), secrets (Barbican) and instance high availability (Masakari).',
          '<strong>Decide who owns it.</strong> A private cloud is a product, not a project. Someone must own upgrades, capacity and on-call from day one.']))

S('sizing', 'Sizing and five-year cost', '''
<div class="keep"><h3>Compute</h3>
<p>Size from the VM inventory, by processor and by memory, and take whichever needs more servers. Memory is rarely overcommitted; processor cores commonly are, at about three virtual CPUs per physical core.</p>
<div class="wp-formula">Compute nodes = max( total vCPU &divide; (cores per node &times; overcommit &times; 0.75), total VM RAM &divide; (usable RAM per node &times; 0.85) ) + 1 spare</div></div>
<div class="keep"><h3>Storage</h3>
<p>Ceph keeps three copies of each block, and must keep enough free space to rebuild a failed node&rsquo;s data onto the others before it reaches its 85 percent &ldquo;near full&rdquo; warning.</p>
<div class="wp-formula">Usable capacity = raw capacity &divide; 3 copies &times; fill target, where fill target &asymp; 0.85 &times; (storage nodes &minus; 1) &divide; storage nodes</div></div>
<h3>A worked example: 300 VMs</h3>
<p>An estate of 300 VMs averages 4 vCPU, 16 GB of memory and 150 GB of disk each: 1,200 vCPU, 4,800 GB of memory and 45 TB of provisioned disk. Compute nodes have 64 physical cores and 768 GB of memory, of which 704 GB is usable after the host&rsquo;s own needs.</p>
''' + table(['Item', 'Arithmetic', 'Result'], [
    ['Nodes by processor', '1,200 &divide; (64 &times; 3 &times; 0.75 = 144)', '8.3, so 9 nodes'],
    ['Nodes by memory', '4,800 &divide; (704 &times; 0.85 = 598)', '8.0, so 9 nodes'],
    ['Compute at go-live', '9 + 1 spare', '10 nodes, 12 by year three at 20% growth'],
    ['Storage needed', '45 TB provisioned + 30% growth', 'About 58 TB usable'],
    ['Ceph fill target, 6 nodes', '0.85 &times; 5 &divide; 6', 'About 0.71'],
    ['Ceph raw capacity', '6 nodes &times; 12 &times; 3.84 TB NVMe = 276 TB; 276 &divide; 3 &times; 0.71', 'About 65 TB usable'],
]) + '''
<h3>Five-year cost, both ways</h3>
<p>The same 300 VMs over five years. Planning ranges at typical Indian prices in 2026, not quotations.</p>
<div class="wp-formula">Five-year cost = upfront hardware + expansion + 5 &times; (space and power + support and licences + people + backup, DR and links)</div>
''' + table(['Cost line, five years', 'Private cloud (OpenStack, colocation)', 'Public cloud (3-year commitments)'], [
    ['Hardware: 3 control, 10 compute and 6 storage servers, network; 2 more compute nodes in year 3', '&#8377;3.5 to 5.5 crore', 'Included in hourly rates'],
    ['Compute and storage consumption', 'Included above', '&#8377;13 to 18 crore'],
    ['Space and power: about 4 racks', '&#8377;2.5 to 3.5 crore', 'Included'],
    ['Software support, hardware maintenance', '&#8377;1.5 to 3 crore', '&#8377;0.7 to 1.5 crore (support plan)'],
    ['Egress, NAT, load balancers, logging', 'Small', '&#8377;1.5 to 3 crore'],
    ['Backup, DR and network links', '&#8377;1 to 2 crore', '&#8377;1 to 2 crore'],
    ['People: platform or cloud operations team', '&#8377;4 to 5 crore (3 engineers)', '&#8377;2.5 to 3.5 crore (2 engineers plus FinOps)'],
    ['<strong>Five-year total</strong>', '<strong>&#8377;12.5 to 19 crore</strong>', '<strong>&#8377;18.7 to 28 crore</strong>'],
], 'wp-compact') + '''
<p>On these assumptions the private cloud costs roughly a third less over five years. The gap narrows quickly if the private platform runs half empty, if the team must be hired at senior rates, or if right-sizing removes 20 to 30 percent of the public cloud capacity. Run the model with your own inventory.</p>
<h3>Egress and licences: the lines most often missed</h3>
''' + ul(['<strong>Egress:</strong> at list prices of roughly &#8377;7 to 9 per GB, an application sending 20 TB a month out costs about 20,000 &times; &#8377;8 = &#8377;1.6 lakh a month, close to &#8377;20 lakh a year, before any VM is counted.',
          '<strong>Windows Server and SQL Server:</strong> per-core licences follow the physical cores of the host on any hypervisor. Check licence mobility rules before moving to public cloud.',
          '<strong>Oracle Database:</strong> licensing depends on how the hypervisor partitions processors; on many KVM platforms every host core can count. Check before a database moves.',
          '<strong>Hypervisor and cloud software:</strong> KVM, OpenStack and Ceph have no licence fee. A support subscription is optional but usually wise for production.']))

S('security', 'Landing zones, security and governance', '''
<p>A landing zone is the set of accounts, guardrails, networks and logging in place before the first workload arrives. Built first, from code, it takes a few weeks. Retrofitted after two years of ad hoc accounts, it is a project of its own. On the private cloud, projects and quotas play the role of accounts.</p>
''' + table(['Area', 'What good looks like'], [
    ['Identity', 'One sign-in through your directory, with roles in each cloud and in OpenStack. No local users or shared passwords; multi-factor everywhere; sealed break-glass accounts.'],
    ['Account structure', 'Production, non-production and sandbox in separate accounts (projects on OpenStack), so a sandbox mistake cannot reach production.'],
    ['Guardrails', 'Policies teams cannot switch off: approved regions, encryption and logging on, no public buckets, mandatory tags.'],
    ['Network', 'Hub and spoke with a firewall and shared egress in the hub, and an IP plan that does not overlap with the data centre.'],
    ['Logging', 'Audit logs and alerts from every account and cloud flow to one place teams cannot change.'],
    ['Cost', 'Owner, environment and cost-centre tags enforced at creation; budgets and alerts per account.'],
]) + '''
<h3>Regulation in practice</h3>
<p>Indian rules shape placement more than architecture. RBI requires payment system data to be stored in India and expects audit and access rights over outsourced IT, including cloud; IRDAI and SEBI set similar expectations. CERT-In requires incidents to be reported within six hours and logs kept for 180 days within India. The DPDP Act sets duties on how personal data is processed and secured. Residency is achievable in Indian public cloud regions or a private cloud; the real questions are audit rights, log retention and who holds the keys.</p>
''' + callout('Keys and secrets:', 'encrypt volumes and object storage on both sides, keep keys for sensitive data in a service you control (customer-managed keys in public cloud, Barbican with a hardware security module on the private side), and rotate certificates on a schedule.', 'warn'))

S('operations', 'Running it: day 2, upgrades and FinOps', '''
<p>Private clouds that disappoint were usually built well and then left without upgrades or capacity planning. Public cloud estates that disappoint never had an owner for cost. Both are fixed by a routine.</p>
''' + table(['Activity', 'How often', 'What good looks like'], [
    ['Health and alert review', 'Daily', 'Alerts that matter reach a person. Noise is tuned out, not ignored.'],
    ['Security patching', 'Monthly', 'Rolling host patching with live migration; no user downtime.'],
    ['Capacity review', 'Monthly', 'Forecast of when compute, storage and IP ranges run out, with time to buy.'],
    ['Restore test', 'Monthly', 'One real restore, timed and recorded.'],
    ['Cost review (public cloud)', 'Monthly', 'Idle and oversized resources removed; commitments matched to steady use.'],
    ['Platform upgrade', 'Once a year', 'Rehearsed on staging, rolled out with a written rollback plan.'],
]) + '''
<h3>Upgrades without fear</h3>
<p>OpenStack releases every six months. Since the 2023.1 release, every other release supports an upgrade that skips one, so a yearly cycle is practical. Keep a small staging cloud built from the same code, rehearse each upgrade on it, and never fall more than one upgrade step behind. Platforms that skip upgrades for two or three years end up needing a migration instead.</p>
<h3>FinOps for the public side</h3>
''' + ul(['<strong>Right-size first.</strong> Lifted VMs are often 30 to 50 percent larger than needed. Resize from four weeks of usage data before buying commitments.',
          '<strong>Commit to the steady base only.</strong> Reserved instances and savings plans cut 30 to 60 percent off compute for one or three years. Never commit to the peak.',
          '<strong>Schedule non-production.</strong> Off from 8 pm to 8 am and at weekends, development and test run 60 hours a week instead of 168, saving about 60 percent.',
          '<strong>Show cost by team every month.</strong> A report by owner tag changes behaviour faster than any policy.',
          '<strong>Watch data transfer.</strong> Egress, NAT gateway and cross-zone traffic are often the fastest-growing lines.']) + callout('Tooling:', 'Prometheus, Alertmanager and Grafana for metrics, OpenSearch or Loki for logs, Ansible and Terraform for change, with the whole platform kept as code in version control.'))

S('roadmap', 'Roadmap: leaving VMware in planned waves', '''
<p>For a few hundred VMs, a private cloud build and VMware exit typically takes six to nine months. The pace is set by application owners&rsquo; testing time, not conversion speed.</p>
''' + table(['Stage', 'Typical duration', 'Outcome'], [
    ['1. Assess', '3 to 4 weeks', 'Inventory (an RVTools export), dependency map, placement, five-year cost model, licence review.'],
    ['2. Design', '3 to 4 weeks', 'Architecture, network and IP plan, identity, bill of materials, wave plan, rollback rules.'],
    ['3. Build and prove', '6 to 10 weeks, after hardware arrives', 'Platform built from code and failure-tested; monitoring and backup working first.'],
    ['4. Pilot wave', '2 weeks', '10 to 20 low-risk VMs covering every operating system version.'],
    ['5. Production waves', '8 to 16 weeks', 'Waves of 20 to 60 VMs every one or two weeks, each tested side by side before cutover.'],
    ['6. Decommission', '2 to 4 weeks', 'Last sign-offs, VMware hosts retired, licences dropped.'],
]) + '''
<h3>How a wave works</h3>
<ol class="wp-steps">
<li><strong>Group by dependency.</strong> An application&rsquo;s web, application and database VMs move together, so a cutover never splits a live dependency across a WAN link.</li>
<li><strong>Convert and test side by side.</strong> virt-v2v copies each VM, replaces VMware drivers with virtio drivers and removes VMware Tools. Large VMs are pre-copied and synced in the window to keep cutover short.</li>
<li><strong>Cut over only after sign-off.</strong> The application owner tests on KVM while the VMware copy is still live. Users move only when the owner agrees.</li>
<li><strong>Keep the way back.</strong> Source VMs stay intact and powered off for an agreed period, typically two to four weeks. Rollback is a DNS or IP change and a power-on.</li>
</ol>
<h3>What usually catches teams out</h3>
''' + ul(['<strong>Drivers and boot.</strong> Windows VMs need virtio drivers before or during conversion, or they will not boot. Test every operating system version in the pilot.',
          '<strong>Network identity.</strong> MAC addresses usually change. Anything licensed against a MAC address, and static DHCP reservations, need attention.',
          '<strong>Vendor support.</strong> Some appliances and commercial applications are supported only on VMware. Check before planning their wave; a few may stay on a small vSphere island or move to public cloud.',
          '<strong>Features and storage.</strong> Automatic load balancing like DRS is more limited on KVM, and Ceph behaves differently from VMFS and vSAN. Keep headroom and design volumes for the new platform.']))

S('mistakes', 'Ten common mistakes', '<ol class="wp-steps">' + ''.join('<li>' + m + '</li>' for m in [
    '<strong>A blanket cloud policy.</strong> &ldquo;Cloud first&rdquo; or &ldquo;all private&rdquo; puts some workloads in the wrong place by design.',
    '<strong>Comparing first-year cost.</strong> Five years, with people, egress, licences and refresh, is the only fair comparison.',
    '<strong>Lifting VMs without right-sizing.</strong> You pay every hour for capacity nobody uses.',
    '<strong>Letting the renewal date set the plan.</strong> Start the exit assessment at least 12 months before the VMware renewal.',
    '<strong>Choosing OpenStack when Proxmox VE would do,</strong> or the reverse. Pick the smallest platform that meets the need.',
    '<strong>Skipping upgrades.</strong> A private cloud three releases behind needs a migration, not an upgrade.',
    '<strong>Converting VMs alphabetically.</strong> Waves must follow dependencies, or a cutover splits a live application.',
    '<strong>Decommissioning VMware too early.</strong> Keep the source VMs until the owner signs off, and the hosts until the last wave is done.',
    '<strong>Two identities.</strong> Two audit trails and a clean-up project nobody planned.',
    '<strong>No owner for cost.</strong> Without tags, budgets and a monthly report by team, public cloud cost only goes one way.']) + '</ol>')

CHECKLIST = [
  ('Strategy and placement', ['Every application has a written placement and a one-line reason',
                  'Placement agreed with each application owner',
                  'Residency and audit requirements listed per application',
                  'Dependencies mapped, so related systems are placed and moved together',
                  'A named owner for the private platform and for public cloud cost',
                  'Multi-cloud used only for a stated, specific need']),
  ('Cost and commercial', ['Five-year cost model built for private and public, from your own inventory and quotes',
                  'Egress and cross-boundary data transfer estimated per application',
                  'Database and operating system licences checked for the target platform',
                  'VMware renewal date known, and the exit assessment started at least 12 months before',
                  'Public cloud commitments limited to the steady base after right-sizing',
                  'Hardware refresh and expansion included in the private cost']),
  ('Platform design', ['Platform choice justified against need and team skills',
                  'Three control nodes and at least one spare compute node',
                  'Ceph fill target stays below near-full after losing a node',
                  'Separate networks for management, storage, tenant traffic and external access',
                  'IP plan that does not overlap between data centre and cloud',
                  'Deployment tool chosen for a five-year upgrade path, with a staging cloud']),
  ('Migration', ['Every VM assigned to a dependency-based wave',
                  'Pilot wave covering every operating system version in use',
                  'Monitoring and backup working on the target before the first production wave',
                  'Rollback rule agreed: source VMs kept intact for a stated period',
                  'Vendor support on KVM confirmed before each wave',
                  'Owner sign-off recorded before each cutover']),
  ('Security and governance', ['Single sign-on from one directory to OpenStack and every public cloud account',
                  'Separate accounts or projects for production, non-production and sandbox',
                  'Guardrails for regions, encryption, logging, public access and tags',
                  'Central audit logs kept for at least 180 days within India',
                  'Keys for sensitive data held in a service you control',
                  'Break-glass accounts sealed, monitored and tested']),
  ('Operations and FinOps', ['Runbooks for patching, upgrades, node replacement and certificate rotation',
                  'Monthly capacity forecast for compute, storage and IP ranges',
                  'Yearly upgrade rehearsed on staging before production',
                  'Monthly cost report by team, with budgets and alerts',
                  'Non-production environments scheduled off out of hours',
                  'Monthly restore test, timed and recorded']),
]
n_items = sum(len(i) for _, i in CHECKLIST)
S('checklist', 'Cloud readiness checklist (' + str(n_items) + ' points)',
  '<p>Use this list to score your current position. Anything you cannot tick with evidence is a gap worth closing.</p><div class="wp-check">' +
  ''.join('<div class="wp-check-group"><h3>' + g + '</h3><ul>' + ''.join('<li>' + i + '</li>' for i in items) + '</ul></div>' for g, items in CHECKLIST) + '</div>')

S('glossary', 'Glossary', table(['Term', 'Meaning'], [
    ['Private cloud', 'Self-service, multi-tenant infrastructure on hardware you own or lease, driven by a portal and API.'],
    ['OpenStack', 'Open-source cloud software: Nova (compute), Neutron (network), Cinder (block storage), Keystone (identity).'],
    ['KVM', 'The hypervisor built into Linux, used by OpenStack, Proxmox VE and most public clouds.'],
    ['Ceph', 'Open-source distributed storage providing block (RBD), object (RGW) and file storage across many servers.'],
    ['OVN', 'Open Virtual Network: the software-defined networking used by Neutron.'],
    ['virt-v2v', 'An open-source tool that converts VMware VMs to run on KVM, swapping in virtio drivers.'],
    ['Landing zone', 'The accounts, guardrails, network and logging set up before workloads arrive in a cloud.'],
    ['Egress', 'Data sent out of a public cloud, charged per gigabyte.'],
    ['FinOps', 'The practice of making cloud cost visible to the teams who create it, and managing it monthly.'],
]))
