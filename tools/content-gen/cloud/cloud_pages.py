"""Cloud domain pages (Oct 2026 rewrite). Run from tools/content-gen/cloud/."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dr'))
from tpl import page, crumb
from refarch import render

def N(zone, row=None, col='full', title='', sub='', style='run', x=None, w=None):
    d = dict(zone=zone, title=title, sub=sub, style=style, col=col)
    if row is not None: d['row'] = row
    if x is not None: d['x'], d['w'] = x, w
    return d

def F(a, b, kind, n=None):
    return dict(a=a, b=b, kind=kind, n=n)

CTA = '''
        <div class="vk-sec"><div class="vk-wrap">
            <div class="vk-cta">
                <h2>Planning a cloud move or a VMware exit?</h2>
                <p class="vk-muted">Send us a VM inventory export (RVTools is fine) and a line on what is driving the change. We will come back with a plain first view: what could move where, in what order, and roughly what it would cost to run.</p>
                <div class="vk-actions">
                    <a class="vk-btn primary" href="/contact">Book a cloud review</a>
                    <a class="vk-btn" href="/portfolio/cloud-solutions">Back to cloud overview</a>
                </div>
            </div>
        </div></div>'''

HOME = ("Home", "/")
HUB = ("Cloud", "/portfolio/cloud-solutions")
SCRIPTS = ['/vk-cloud-tools.js']

def sec(inner, prose=False, sid=None):
    i = f' id="{sid}"' if sid else ''
    if prose:
        return f'\n        <div class="vk-sec"{i}><div class="vk-wrap"><div class="vk-prose">{inner}\n        </div></div></div>'
    return f'\n        <div class="vk-sec"{i}><div class="vk-wrap">{inner}\n        </div></div>'

def hero(crumbs, eyebrow, h1, lead, facts=None, actions=None):
    f = ''
    if facts:
        f = '<div class="vk-facts">' + ''.join(f'<div class="vk-fact"><span class="k">{k}</span><span class="v">{v}</span></div>' for k, v in facts) + '</div>'
    a = ''
    if actions:
        a = '<div class="vk-actions">' + ''.join(f'<a class="vk-btn{" primary" if i == 0 else ""}" href="{h}">{t}</a>' for i, (t, h) in enumerate(actions)) + '</div>'
    return f'''
        <div class="vk-wrap vk-hero">
            {crumb(*crumbs)}
            <span class="vk-eyebrow">{eyebrow}</span>
            <h1>{h1}</h1>
            <p class="vk-lead">{lead}</p>
            {f}{a}
        </div>'''

def table(head, rows):
    th = ''.join(f'<th>{h}</th>' for h in head)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<div class="vk-table-wrap"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'

def ul(items): return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
def steps(items): return '<ol class="vk-steps">' + ''.join(f'<li>{i}</li>' for i in items) + '</ol>'

def figure(diagram, label, caption, parts):
    svg = render(diagram, label)
    rows = ''.join(f'<tr><td>{(f"<span class=vk-num>{n}</span> " if n else "") + t}</td><td>{d}</td></tr>' for n, t, d in parts)
    return f'''<figure class="vk-fig vk-refarch"><span class="vk-scroll-hint">Scroll sideways to see the whole diagram &rarr;</span><div class="vk-refarch-scroll">{svg}</div>
                <figcaption>{caption}</figcaption></figure>
            <div class="vk-table-wrap"><table><thead><tr><th>Part</th><th>What it does</th></tr></thead><tbody>{rows}</tbody></table></div>'''

PAGES = [
    ('private-cloud-openstack', 'Private cloud on OpenStack'),
    ('vmware-to-kvm-migration', 'VMware to KVM migration'),
    ('hybrid-cloud', 'Hybrid cloud'),
    ('multi-cloud-landing-zone', 'Public and multi-cloud landing zones'),
    ('cloud-operations', 'Running the platform (Day 2)'),
    ('cloud-cost', 'Private vs public cloud cost'),
]

def related(current):
    cards = ''.join(f'<a class="vk-pill{" on" if s == current else ""}" href="/solutions/cloud/{s}">{n}</a>' for s, n in PAGES)
    return f'<div class="vk-pills">{cards}</div>'

def more(current):
    items = [(s, n) for s, n in PAGES if s != current]
    links = ' &middot; '.join(f'<a href="/solutions/cloud/{s}">{n}</a>' for s, n in items)
    return sec(f'<p class="vk-small"><strong>More cloud guides:</strong> {links} &middot; <a href="/solutions/cloud/faq">Cloud FAQ</a> &middot; <a href="/use_cases/cloud-vmware-exit">Use case: leaving VMware</a></p>')


# =================================================================== HUB
def hub():
    b = hero((HOME, ("Solutions", "/solutions"), ("Cloud", None)), 'Cloud solutions',
             'Cloud that fits the workload, not the other way round',
             'Some workloads belong in a public cloud. Some run better and cheaper on a private platform you control. Most organisations end up with both. We help you decide what goes where, then design, build and migrate it, including moving off VMware.',
             actions=[('Book a cloud review', '/contact'), ('Where should my workload run?', '#placer')])
    b += sec('''
            <span class="vk-eyebrow">What usually goes wrong</span>
            <h2>Four problems we see again and again</h2>
            <div class="vk-grid" style="margin-top:22px">
                <div class="vk-card"><h3>Lift and shift, then a big bill</h3><p class="vk-muted">VMs are moved to public cloud exactly as they were, sized for peak and running 24x7. The first full-year invoice is a shock.</p></div>
                <div class="vk-card"><h3>The VMware renewal arrives</h3><p class="vk-muted">Broadcom's move to subscription bundles has pushed renewal costs up sharply for many teams, and the renewal date leaves little time to plan an exit.</p></div>
                <div class="vk-card"><h3>Two clouds, two sets of rules</h3><p class="vk-muted">Each team opened its own cloud account. Nobody can say who has access to what, or where the audit logs are.</p></div>
                <div class="vk-card"><h3>Private cloud nobody can run</h3><p class="vk-muted">An OpenStack platform was installed by a vendor and handed over without runbooks. Upgrades are now feared and postponed.</p></div>
            </div>''')
    b += sec('''
            <span class="vk-eyebrow">The options in plain words</span>
            <h2>Four ways to run your workloads</h2>''' + table(
        ['Model', 'What it means', 'Strong at', 'Watch out for'],
        [['<a href="/solutions/cloud/private-cloud-openstack">Private cloud</a>', 'A self-service cloud on hardware you own or lease, often OpenStack on KVM.', 'Steady workloads, data that must stay put, predictable cost over 3 to 5 years.', 'You need the skills to run and upgrade it.'],
         ['<a href="/solutions/cloud/multi-cloud-landing-zone">Public cloud</a>', 'AWS, Azure, OCI or similar. You rent capacity by the hour.', 'Spiky load, fast start, managed services such as databases and analytics.', 'Cost grows quietly. Data transfer and always-on VMs add up.'],
         ['<a href="/solutions/cloud/hybrid-cloud">Hybrid cloud</a>', 'Private and public working together over private links, with one identity system.', 'Keeping core data at home while using cloud where it is stronger.', 'Connectivity, identity and DNS must be designed, not assumed.'],
         ['<a href="/solutions/cloud/multi-cloud-landing-zone">Multi-cloud</a>', 'More than one public cloud, usually for different workloads or by acquisition.', 'Using the best service from each provider, reducing dependence on one.', 'Every extra cloud multiplies governance and skills needed.']]), sid='which-model')
    b += sec('''
            <span class="vk-eyebrow">Try it</span>
            <h2>Where should this workload run?</h2>
            <p class="vk-prose">Answer five questions about one application. You will get a suggested starting point and the reasons behind it.</p>
            <div class="vk-tool vk-placer"></div>
            <noscript><p class="vk-muted">This tool needs JavaScript. The table above compares the same options.</p></noscript>''', sid='placer')
    cards = [
        ('private-cloud-openstack', 'Private cloud on OpenStack', 'How a production OpenStack platform is laid out, with sizing guidance and the decisions that matter.'),
        ('vmware-to-kvm-migration', 'VMware to KVM migration', 'A wave-by-wave method to leave VMware safely. Includes an animated migration simulation.'),
        ('hybrid-cloud', 'Hybrid cloud', 'Connectivity, identity and DNS between your data centre and a public cloud.'),
        ('multi-cloud-landing-zone', 'Public and multi-cloud landing zones', 'Accounts, guardrails, networking and logging set up before the first workload lands.'),
        ('cloud-operations', 'Running the platform (Day 2)', 'Monitoring, patching, upgrades, capacity and cost control after go-live.'),
        ('cloud-cost', 'Private vs public cloud cost', 'A calculator to compare five-year cost with your own numbers.'),
    ]
    c = ''.join(f'<a class="vk-card" href="/solutions/cloud/{s}"><h3>{t}</h3><p>{d}</p><span class="vk-go">Read the guide &rarr;</span></a>' for s, t, d in cards)
    c += '<a class="vk-card" href="/use_cases/cloud-vmware-exit"><h3>Use case: leaving VMware</h3><p>An illustrative scenario: 300 VMs moved to OpenStack in six waves.</p><span class="vk-go">Read the use case &rarr;</span></a>'
    c += '<a class="vk-card" href="/solutions/cloud/faq"><h3>Cloud questions, answered</h3><p>Lock-in, data residency, OpenStack skills, VMware licences and more.</p><span class="vk-go">Read the FAQ &rarr;</span></a>'
    b += sec(f'''
            <span class="vk-eyebrow">Go deeper</span>
            <h2>Guides and examples</h2>
            <div class="vk-grid" style="margin-top:22px">{c}</div>
            <p class="vk-muted vk-small" style="margin-top:18px">For the full technical reference, see the <a href="/solutions/cloud-solutions">cloud whitepaper</a>.</p>''')
    b += sec('''
            <span class="vk-eyebrow">How we work</span>
            <h2>How a cloud engagement runs</h2>''' + steps([
        '<strong>Inventory.</strong> We start from an export of your VMs, applications and dependencies, not from a product brochure.',
        '<strong>Placement.</strong> Each application is assigned to private, public or hybrid, with the reason written down and agreed.',
        '<strong>Design.</strong> Target architecture, network and identity design, bill of materials, and a cost model you can check.',
        '<strong>Build.</strong> Platform built from code (Ansible, Terraform), tested for failure before any workload moves.',
        '<strong>Migrate in waves.</strong> Groups of related applications move together, each with a tested rollback.',
        '<strong>Hand over.</strong> Runbooks, monitoring and an upgrade plan your team can own, with support if you want it.']), prose=True)
    b += CTA
    page('portfolio/cloud-solutions.html', 'Cloud Solutions: Private, Public, Hybrid and VMware Exit | Vakratron Systems',
         'Plain guidance on private, public, hybrid and multi-cloud: where each workload should run, OpenStack private cloud design, VMware to KVM migration, landing zones and cost.', b, scripts=SCRIPTS)


# =================================================================== PRIVATE CLOUD
def private():
    d = dict(panels=('Control plane (3 nodes)', 'Compute, storage and network'), rows=4, nodes={
        'users': N('G', title='Users and teams', sub='self-service portal and API', style='global', x=370, w=220),
        'api': N('P', 0, title='API and dashboard', sub='Horizon, Keystone, service APIs'),
        'svc': N('P', 1, title='Cloud services', sub='Nova, Neutron, Cinder, Glance'),
        'db': N('P', 2, title='Database and message queue', sub='MariaDB Galera, RabbitMQ'),
        'mon': N('P', 3, title='Monitoring and logs', sub='Prometheus, Grafana, OpenSearch'),
        'cmp': N('D', 0, title='Compute nodes', sub='KVM hypervisors, add more as you grow'),
        'ceph': N('D', 1, title='Ceph storage cluster', sub='block, image and object storage'),
        'bkp': N('D', 2, title='Backup target', sub='separate from Ceph', style='backup'),
        'gw': N('D', 3, title='Network gateways', sub='OVN routing to outside networks'),
        'ext': N('B', title='Outside networks', sub='internet, MPLS, data centre core', style='global', x=560, w=300),
    }, flows=[F('users', 'P', 'traffic'), F('svc', 'cmp', 'deploy', 1), F('cmp', 'ceph', 'stream', 2), F('ceph', 'bkp', 'batch', 3), F('ext', 'gw', 'traffic', 4)])
    b = hero((HOME, HUB, ("Private cloud on OpenStack", None)), 'Cloud guide', 'Private cloud on OpenStack',
             'OpenStack gives you AWS-style self-service on hardware you control: teams create their own VMs, networks and volumes through a portal or API, and you keep the data and the cost in your hands. Here is how a production platform is put together, and what decides whether it runs well.',
             facts=[('Hypervisor', 'KVM'), ('Smallest sensible start', '3 control + 3 compute + 3 storage nodes'), ('Typical storage', 'Ceph, three copies'), ('Best for', 'Steady workloads, data that stays put')])
    b = b.replace('<span class="vk-eyebrow">Cloud guide</span>', related('private-cloud-openstack') + '<span class="vk-eyebrow">Cloud guide</span>', 1)
    b += sec('''
            <span class="vk-eyebrow">Reference architecture</span>
            <h2>How the pieces fit together</h2>''' + figure(d, 'OpenStack private cloud reference architecture',
        'Numbered lines show the main flows. The control plane runs on three nodes so that one can fail or be upgraded without stopping the cloud.',
        [('', 'Control plane', 'Three nodes run the APIs, schedulers, database and message queue. Three is the minimum for the database and queue to keep a majority when one node is down.'),
         ('1', 'Scheduling', 'When a user asks for a VM, Nova picks a compute node with room, Neutron plugs it into the right network and Cinder attaches its disks.'),
         ('2', 'Storage traffic', 'VM disks live on Ceph, not on the compute node. That is what makes live migration and quick recovery from a failed host possible.'),
         ('3', 'Backup', 'Ceph keeps three copies, but replication is not backup. A separate backup target holds point-in-time copies.'),
         ('4', 'Outside access', 'OVN gateways route traffic between tenant networks and the internet, MPLS or the data centre core.')]))
    b += sec('<h2>Sizing a first platform</h2>' + table(['Role', 'Starting point', 'Why'],
        [['Control nodes', '3', 'Database and queue need a majority to survive one failure. Can share nodes with networking at small scale.'],
         ['Compute nodes', '3 or more, plus one spare', 'Lets you patch or lose one host without running out of capacity.'],
         ['Ceph storage nodes', '3 minimum, 5 or more preferred', 'Three copies need three nodes. More nodes means faster recovery when a disk or node fails.'],
         ['Networks', 'Management, storage, tenant overlay, external', 'Keeping storage traffic on its own network stops it from slowing down everything else. 25 GbE is a common baseline.']]) +
        '<p class="vk-small vk-muted">Starting points only. Real sizing comes from your VM inventory, growth plans and how much failure you need to absorb.</p>')
    b += sec('<h2>Decisions that make or break it</h2>' + ul([
        '<strong>Choose the deployment tool for the next five years, not the next five weeks.</strong> Kolla-Ansible, OpenStack-Ansible and vendor distributions all work. What matters is that your team can upgrade with it.',
        '<strong>Plan upgrades from day one.</strong> OpenStack releases twice a year. Platforms that fall several releases behind become hard to upgrade. Schedule upgrades like patching, not like projects.',
        '<strong>Design networks before installing anything.</strong> VLAN ranges, overlay networks, external IP ranges and MTU are painful to change later.',
        '<strong>Size Ceph for recovery, not just capacity.</strong> When a node fails, Ceph rebuilds copies onto the remaining nodes. Leave enough free space and network capacity for that to happen without hurting users.',
        '<strong>Decide who runs it.</strong> A private cloud is a product, not a project. Someone must own upgrades, capacity and on-call.']), prose=True)
    b += sec('<h2>Typical tools</h2>' + table(['Layer', 'Common choices'],
        [['Deployment', 'Kolla-Ansible, OpenStack-Ansible, Canonical OpenStack, Red Hat OpenStack Services on OpenShift'],
         ['Hypervisor', 'KVM with libvirt'], ['Networking', 'Neutron with OVN'], ['Storage', 'Ceph (RBD for block, RGW for object)'],
         ['Monitoring', 'Prometheus, Grafana, Alertmanager, OpenSearch or Loki for logs'], ['Automation', 'Ansible, Terraform with the OpenStack provider']]) +
        '<p class="vk-small vk-muted">Smaller environments that do not need multi-tenancy or a full API often do well with Proxmox VE instead. We will tell you if OpenStack is more than you need.</p>')
    b += sec('<p>Need the same platform protected against a site failure? See <a href="/solutions/dc-dr/openstack-mapping">disaster recovery on OpenStack</a>.</p>', prose=True)
    b += more('private-cloud-openstack') + CTA
    page('solutions/cloud/private-cloud-openstack.html', 'Private Cloud on OpenStack: Architecture, Sizing and Key Decisions | Vakratron Systems',
         'How a production OpenStack private cloud is laid out: control plane, KVM compute, Ceph storage and OVN networking, with sizing starting points and the decisions that matter.', b, scripts=SCRIPTS)


# =================================================================== VMWARE TO KVM
def vmware():
    d = dict(panels=('Today: VMware vSphere', 'Target: KVM (OpenStack or Proxmox)'), rows=4, nodes={
        'tool': N('G', title='Migration toolkit', sub='inventory, virt-v2v, wave tracker', style='global', x=370, w=220),
        'vc': N('P', 0, title='vCenter', sub='inventory exported with RVTools'),
        'esx': N('P', 1, title='ESXi hosts', sub='VMs grouped by dependency'),
        'ds': N('P', 2, title='VMFS / vSAN datastores', sub='source disks'),
        'vbk': N('P', 3, title='Existing backup', sub='kept until the last wave is signed off', style='idle'),
        'ctl': N('D', 0, title='Cloud control', sub='OpenStack or Proxmox cluster'),
        'kvm': N('D', 1, title='KVM compute nodes', sub='VMs with virtio drivers'),
        'st': N('D', 2, title='Ceph or NFS storage', sub='redesigned, not copied 1:1'),
        'kbk': N('D', 3, title='Backup for KVM', sub='working before wave one'),
    }, flows=[F('tool', 'P', 'deploy'), F('tool', 'D', 'deploy'), F('esx', 'kvm', 'batch', 1), F('ds', 'st', 'stream', 2)])
    b = hero((HOME, HUB, ("VMware to KVM migration", None)), 'Cloud guide', 'Moving off VMware to KVM, safely',
             'The pressure to leave VMware is real: subscription-only licensing has raised renewal costs for many organisations. But a rushed hypervisor migration can cause the outages that wipe out the savings. This is the wave-by-wave method we use to move VMs to KVM, on OpenStack or Proxmox, with a tested way back at every step.',
             facts=[('Core tool', 'virt-v2v'), ('Method', 'Waves by dependency group'), ('Safety net', 'VMware kept live until sign-off'), ('Typical pace', '20 to 60 VMs per wave')])
    b = b.replace('<span class="vk-eyebrow">Cloud guide</span>', related('vmware-to-kvm-migration') + '<span class="vk-eyebrow">Cloud guide</span>', 1)
    b += sec('''
            <span class="vk-eyebrow">See it working</span>
            <h2>A migration, one wave at a time</h2>
            <p class="vk-prose">Each coloured square is a VM, grouped by application. Run the waves to see how related VMs are converted, tested side by side on KVM, and only then cut over. In wave 3 a test fails, and you will see what a rollback looks like.</p>
            <div class="vk-tool vk-wavesim"></div>
            <noscript><p class="vk-muted">This simulation needs JavaScript. The steps below describe the same method.</p></noscript>''')
    b += sec('''
            <span class="vk-eyebrow">Reference architecture</span>
            <h2>Source, target and the path between</h2>''' + figure(d, 'VMware to KVM migration architecture',
        'Both environments run side by side for the length of the migration. Nothing on the VMware side is switched off until its replacement is signed off.',
        [('', 'Migration toolkit', 'An inventory (RVTools export plus dependency mapping), virt-v2v for conversion, and a simple tracker showing every VM, its wave and its status.'),
         ('1', 'Conversion', 'virt-v2v copies each VM, swaps VMware drivers for virtio drivers, removes VMware Tools and registers the VM on the target. Windows and Linux are both supported.'),
         ('2', 'Disk data', 'Disks are copied during conversion. Large VMs can be pre-copied and then synced in the maintenance window to keep cutover short.'),
         ('', 'Backup on both sides', 'The existing backup keeps protecting VMware. The new backup must already work on KVM before the first production wave.')]))
    b += sec('<h2>The method, step by step</h2>' + steps([
        '<strong>Inventory everything.</strong> Export from vCenter, then map which VMs talk to which. Converting VMs alphabetically is how migrations find unexpected outages.',
        '<strong>Group into waves by dependency.</strong> An application\'s web, app and database VMs move together, so a cutover never splits a live dependency.',
        '<strong>Build the target and its operations first.</strong> Monitoring, backup and automation for KVM must work before wave one, not after wave three.',
        '<strong>Run a pilot wave.</strong> A few low-risk VMs prove the tooling, the drivers and the runbook.',
        '<strong>Convert, test side by side, then cut over.</strong> Each wave is tested on KVM while the VMware copy is still live. Users move only after the application owner signs off.',
        '<strong>Keep VMware as the rollback.</strong> Source VMs stay intact, powered off, for an agreed period after each wave.',
        '<strong>Decommission last.</strong> Only when every wave is signed off is the VMware environment retired and its licences dropped.']), prose=True)
    b += sec('<h2>What usually catches teams out</h2>' + ul([
        '<strong>Drivers and boot.</strong> Windows VMs need virtio drivers before or during conversion, or they will not boot. Test every OS version you run in the pilot.',
        '<strong>Network identity.</strong> MAC addresses usually change. Anything licensed against a MAC address, and any static DHCP reservations, will need attention.',
        '<strong>Features you relied on.</strong> KVM platforms offer HA restart and live migration, but automatic load balancing like DRS is more limited. Plan capacity with some headroom.',
        '<strong>Vendor support.</strong> Some appliances and commercial applications are only supported on VMware. Check before you plan their wave. A few may need to stay on a small vSphere island or move to public cloud.',
        '<strong>Software licences.</strong> Moving to a new hypervisor can change how databases and some operating systems are licensed. Check the terms before cutover, not after.',
        '<strong>Storage design.</strong> A one-to-one copy of your datastores is rarely the right target. Ceph and NFS behave differently from VMFS and vSAN, so design for them.']), prose=True)
    b += sec('<h2>Typical tools</h2>' + table(['Stage', 'Common choices'],
        [['Inventory', 'RVTools, vCenter exports, dependency mapping from network flow data'],
         ['Conversion', 'virt-v2v (including direct output to OpenStack), Proxmox VE import wizard for ESXi, Migration Toolkit for Virtualization on OpenShift'],
         ['Target platform', 'OpenStack on KVM, Proxmox VE, OpenShift Virtualization'],
         ['Operations', 'Prometheus and Grafana, Ansible, backup software that supports your KVM platform']]))
    b += sec('<p>See this method applied end to end in the <a href="/use_cases/cloud-vmware-exit">use case: leaving VMware</a>, or compare the running cost with the <a href="/solutions/cloud/cloud-cost">cost calculator</a>.</p>', prose=True)
    b += more('vmware-to-kvm-migration') + CTA
    page('solutions/cloud/vmware-to-kvm-migration.html', 'VMware to KVM Migration: A Safe, Wave-by-Wave Method | Vakratron Systems',
         'How to move from VMware vSphere to KVM on OpenStack or Proxmox: inventory, dependency waves, virt-v2v conversion, side-by-side testing, rollback, and what catches teams out.', b, scripts=SCRIPTS)


# =================================================================== HYBRID
def hybrid():
    d = dict(panels=('On-premises', 'Public cloud landing zone'), rows=4, nodes={
        'users': N('G', title='Users and branches', sub='one login, one set of names', style='global', x=370, w=220),
        'core': N('P', 0, title='Core systems', sub='ERP, databases, legacy apps'),
        'ad': N('P', 1, title='Active Directory', sub='source of identity'),
        'dns': N('P', 2, title='DNS', sub='on-premises zones'),
        'data': N('P', 3, title='Data platform', sub='large datasets stay here'),
        'apps': N('D', 0, title='Cloud applications', sub='web, APIs, analytics'),
        'idp': N('D', 1, title='Cloud identity', sub='synced from AD, single sign-on'),
        'res': N('D', 2, title='DNS resolver', sub='forwards to on-premises zones'),
        'shared': N('D', 3, title='Shared services', sub='logging, security, backup'),
        'link': N('B', title='Private connectivity', sub='dedicated link, with VPN as backup', style='witness', x=330, w=300),
    }, flows=[F('users', 'P', 'traffic'), F('users', 'D', 'traffic'), F('core', 'apps', 'bi', 1), F('ad', 'idp', 'stream', 2), F('dns', 'res', 'bi', 3), F('data', 'shared', 'batch', 5), F('link', 'core', 'hb', 4), F('link', 'apps', 'hb')])
    b = hero((HOME, HUB, ("Hybrid cloud", None)), 'Cloud guide', 'Hybrid cloud that works like one environment',
             'Most hybrid projects do not fail with an outage. They stall at 60 percent, because connectivity, identity or data movement was assumed instead of designed. This guide covers the four things that have to be right before workloads start moving between your data centre and a public cloud.',
             facts=[('Connect with', 'Direct Connect, ExpressRoute, FastConnect'), ('Identity', 'One directory, synced'), ('DNS', 'Forwarding both ways'), ('Moves in', 'Waves, not big bang')])
    b = b.replace('<span class="vk-eyebrow">Cloud guide</span>', related('hybrid-cloud') + '<span class="vk-eyebrow">Cloud guide</span>', 1)
    b += sec('''
            <span class="vk-eyebrow">Reference architecture</span>
            <h2>How the two sides connect</h2>''' + figure(d, 'Hybrid cloud reference architecture',
        'Numbered lines show what crosses between the two environments. Everything crosses over the private link, never the open internet.',
        [('1', 'Application traffic', 'Cloud applications call core systems and the other way round. Keep these calls few and coarse: chatty traffic across a WAN link is slow and, in the cloud, billed.'),
         ('2', 'Identity sync', 'Users and groups are synced from Active Directory to the cloud identity service, so people use one account and one password everywhere.'),
         ('3', 'DNS forwarding', 'Each side can resolve the other\'s names. Without this, applications break in confusing ways after migration.'),
         ('4', 'Private connectivity', 'A dedicated link such as AWS Direct Connect, Azure ExpressRoute or OCI FastConnect, with an IPsec VPN as backup. Sized from measured traffic, not guessed.'),
         ('5', 'Data copies', 'Large datasets stay where they are used. Only what is needed is copied, on a schedule, with egress cost in mind.')]))
    b += sec('<h2>Four things to get right first</h2>' + ul([
        '<strong>Classify every workload.</strong> Decide for each application whether it stays, moves as-is, or is rebuilt for the cloud. Moving a VM unchanged is fine for some systems and expensive for others.',
        '<strong>Design connectivity early.</strong> A VPN added late becomes the bottleneck and single point of failure for every hybrid workload. Order dedicated links early: provisioning can take weeks.',
        '<strong>One identity, not two.</strong> If on-premises and cloud accounts are managed separately, you get two logins, two audit trails and a clean-up project nobody planned.',
        '<strong>Respect data gravity.</strong> Large databases cannot move overnight. Plan how data is synced, how long the first copy takes, and what the final cutover window looks like.']), prose=True)
    b += sec('<h2>Typical tools</h2>' + table(['Layer', 'Common choices'],
        [['Private links', 'AWS Direct Connect, Azure ExpressRoute, OCI FastConnect, IPsec VPN as backup'],
         ['Identity', 'Active Directory with Microsoft Entra Connect, AWS IAM Identity Center, OCI Identity Domains'],
         ['DNS', 'Route 53 Resolver endpoints, Azure DNS Private Resolver, conditional forwarders on-premises'],
         ['Landing zone', 'See <a href="/solutions/cloud/multi-cloud-landing-zone">landing zones</a>'],
         ['Migration', 'Cloud provider migration services, database replication, storage sync tools']]))
    b += more('hybrid-cloud') + CTA
    page('solutions/cloud/hybrid-cloud.html', 'Hybrid Cloud Architecture: Connectivity, Identity, DNS and Data | Vakratron Systems',
         'How to design hybrid cloud that works like one environment: private connectivity, one identity, DNS forwarding, data gravity, and a wave-based migration.', b, scripts=SCRIPTS)


# =================================================================== LANDING ZONE
def landing():
    d = dict(panels=('AWS', 'Azure'), rows=4, nodes={
        'idp': N('G', title='One identity provider', sub='single sign-on to every cloud', style='global', x=370, w=220),
        'org': N('P', 0, title='Organization and accounts', sub='one account per environment'),
        'scp': N('P', 1, title='Guardrails', sub='service control policies'),
        'hub': N('P', 2, title='Network hub', sub='Transit Gateway, shared egress'),
        'wl': N('P', 3, title='Workload accounts', sub='production, non-production, sandbox'),
        'mg': N('D', 0, title='Management groups', sub='one subscription per environment'),
        'pol': N('D', 1, title='Guardrails', sub='Azure Policy'),
        'hub2': N('D', 2, title='Network hub', sub='hub VNet, firewall'),
        'wl2': N('D', 3, title='Workload subscriptions', sub='production, non-production, sandbox'),
        'log': N('B', title='Central logging and security', sub='audit logs, alerts, cost reports in one place', style='witness', x=330, w=300),
    }, flows=[F('idp', 'P', 'deploy', 1), F('idp', 'D', 'deploy'), F('hub', 'hub2', 'bi', 2), F('log', 'wl', 'hb', 3), F('log', 'wl2', 'hb')])
    b = hero((HOME, HUB, ("Landing zones", None)), 'Cloud guide', 'Public and multi-cloud landing zones',
             'A landing zone is the set of accounts, guardrails, networks and logging that is put in place before the first workload arrives. Done first, it is a few weeks of work. Retrofitted after two years of ad hoc accounts, it is a painful project.',
             facts=[('Applies to', 'AWS, Azure, OCI'), ('Built with', 'Code (Terraform)'), ('First version', 'A few weeks'), ('Avoids', 'Sprawl, surprise bills, audit gaps')])
    b = b.replace('<span class="vk-eyebrow">Cloud guide</span>', related('multi-cloud-landing-zone') + '<span class="vk-eyebrow">Cloud guide</span>', 1)
    b += sec('''
            <span class="vk-eyebrow">Reference architecture</span>
            <h2>The same structure in every cloud</h2>''' + figure(d, 'Multi-cloud landing zone reference architecture',
        'Shown for AWS and Azure. OCI follows the same pattern with tenancies, compartments and policies.',
        [('1', 'One identity', 'People sign in once through your identity provider and get roles in each cloud. No local cloud users, no shared passwords.'),
         ('', 'Accounts per environment', 'Production, non-production and sandbox live in separate accounts or subscriptions. A mistake in a sandbox cannot touch production.'),
         ('', 'Guardrails', 'Policies that cannot be switched off by project teams: approved regions only, encryption on, logging on, no public storage buckets.'),
         ('2', 'Network hub', 'All workload networks connect through a hub with a firewall and shared internet egress. Clouds are linked privately only where there is a real need.'),
         ('3', 'Central logging', 'Audit logs and security alerts from every account and every cloud flow to one place that project teams cannot alter.')]))
    b += sec('<h2>What a first landing zone includes</h2>' + table(['Area', 'What we set up'],
        [['Accounts', 'Account or subscription structure, naming, and a request process for new ones'],
         ['Identity', 'Single sign-on, role design, break-glass accounts, multi-factor authentication everywhere'],
         ['Guardrails', 'Region limits, encryption, logging, tagging rules, blocked public access'],
         ['Network', 'Hub-and-spoke design, IP address plan that does not clash with on-premises, private links'],
         ['Security and logging', 'Central audit logs, threat detection, alert routing to your team'],
         ['Cost', 'Mandatory tags, budgets and alerts per account, monthly cost report by team']]))
    b += sec('<h2>Is multi-cloud right for you?</h2>' + ul([
        '<strong>Good reasons:</strong> a service only one provider offers well, a regulator or customer that requires a second provider, or an acquisition that arrived on a different cloud.',
        '<strong>Weak reasons:</strong> a general wish to avoid lock-in. Every extra cloud doubles the skills, tools and guardrails you have to maintain.',
        '<strong>Our usual advice:</strong> pick one primary public cloud, build the landing zone properly, and add a second only for a specific need.']), prose=True)
    b += sec('<h2>Typical tools</h2>' + table(['Cloud', 'Building blocks'],
        [['AWS', 'Organizations, Control Tower, service control policies, IAM Identity Center, Transit Gateway, CloudTrail, Security Hub'],
         ['Azure', 'Management groups, Azure landing zone accelerators, Azure Policy, Entra ID, hub VNet with Azure Firewall, Microsoft Defender for Cloud'],
         ['OCI', 'Tenancy and compartments, IAM policies, OCI landing zone templates, Cloud Guard'],
         ['All', 'Terraform for everything, so the landing zone is reviewed and versioned like code']]))
    b += more('multi-cloud-landing-zone') + CTA
    page('solutions/cloud/multi-cloud-landing-zone.html', 'Cloud Landing Zones for AWS, Azure and OCI: Accounts, Guardrails, Network, Logging | Vakratron Systems',
         'What a cloud landing zone is and what it includes: account structure, single sign-on, guardrails, hub networking and central logging across AWS, Azure and OCI.', b, scripts=SCRIPTS)


# =================================================================== OPERATIONS
def ops():
    b = hero((HOME, HUB, ("Running the platform", None)), 'Cloud guide', 'Running the platform after go-live',
             'A cloud platform is only as good as the way it is run. Most private clouds that disappoint were built well and then left without monitoring, upgrades or capacity planning. We design the day-to-day operating model with you, hand it over to your team with runbooks, and can support it on agreed terms if you want.',
             facts=[('Covers', 'Monitoring, patching, upgrades, capacity, cost'), ('Delivered as', 'Runbooks your team owns'), ('Support', 'Optional, on agreed terms'), ('Goal', 'No upgrade you are afraid of')])
    b = b.replace('<span class="vk-eyebrow">Cloud guide</span>', related('cloud-operations') + '<span class="vk-eyebrow">Cloud guide</span>', 1)
    b += sec('<h2>The Day-2 routine</h2>' + table(['Activity', 'How often', 'What good looks like'],
        [['Health and alert review', 'Daily', 'Alerts that matter reach a person. Noise is tuned out, not ignored.'],
         ['Security patching', 'Monthly', 'Hosts patched in rolling order with no VM downtime, using live migration.'],
         ['Capacity review', 'Monthly', 'A forecast of when compute, storage and IP ranges run out, with time to buy.'],
         ['Backup restore test', 'Monthly', 'One real restore, timed and recorded.'],
         ['Cost review (public cloud)', 'Monthly', 'Idle and oversized resources removed. Commitments matched to steady usage.'],
         ['Platform upgrade', 'Once or twice a year', 'Tested in a staging environment first, then rolled out with a rollback plan.'],
         ['DR test', 'Twice a year', 'See <a href="/solutions/dc-dr/best-practices">testing DR</a>.']]))
    b += sec('<h2>What we hand over</h2>' + ul([
        '<strong>Monitoring and alerting</strong> already wired up, with dashboards for the platform and for each tenant.',
        '<strong>Runbooks</strong> for the common tasks: adding a compute node, replacing a failed disk, rotating certificates, patching, upgrading.',
        '<strong>An upgrade plan</strong> that keeps you within one or two releases of current.',
        '<strong>A capacity model</strong> your team can update with real numbers each month.',
        '<strong>Cost controls</strong> for public cloud: tags, budgets, alerts and a monthly report.']), prose=True)
    b += sec('<h2>Tools we typically use</h2>' + table(['Area', 'Common choices'],
        [['Metrics and alerts', 'Prometheus, Alertmanager, Grafana'], ['Logs', 'OpenSearch or Grafana Loki'],
         ['Automation', 'Ansible, Terraform, GitLab CI or Jenkins'], ['Public cloud cost', 'Native cost tools, tagging policies, budgets and commitment planning']]))
    b += more('cloud-operations') + CTA
    page('solutions/cloud/cloud-operations.html', 'Cloud Operations (Day 2): Monitoring, Patching, Upgrades, Capacity and Cost | Vakratron Systems',
         'How to run a private or public cloud platform after go-live: daily, monthly and yearly routines, runbooks, upgrades, capacity planning and cost control.', b, scripts=SCRIPTS)


# =================================================================== COST
def cost():
    b = hero((HOME, HUB, ("Private vs public cost", None)), 'Cloud guide', 'Private vs public cloud: what it really costs',
             'Public cloud is cheap to start and can be expensive to keep. Private cloud costs more on day one and often less by year three, if the load is steady. The only honest way to compare is with your own numbers over the same period. This calculator lets you do that.',
             facts=[('Compare over', '3 to 5 years'), ('Public wins', 'Spiky, short-lived, fast-growing'), ('Private wins', 'Steady, 24x7, large'), ('Always add', 'People, egress, support')])
    b = b.replace('<span class="vk-eyebrow">Cloud guide</span>', related('cloud-cost') + '<span class="vk-eyebrow">Cloud guide</span>', 1)
    b += sec('''
            <span class="vk-eyebrow">Try it</span>
            <h2>Five-year cost calculator</h2>
            <p class="vk-prose">Every field is editable. The defaults are rough planning figures to get you started, not quotes. Replace them with your own prices.</p>
            <div class="vk-tool vk-tco"></div>
            <noscript><p class="vk-muted">This calculator needs JavaScript.</p></noscript>''')
    b += sec('<h2>Reading the result</h2>' + ul([
        '<strong>Steady load favours private.</strong> If VMs run around the clock for years, owned hardware usually costs less after the second or third year.',
        '<strong>Spiky or uncertain load favours public.</strong> Paying only for peak hours, or not knowing the size of next year\'s demand, is where public cloud earns its price.',
        '<strong>People are the biggest private cost.</strong> If you have no team to run a private cloud, add the cost of building one, or of outside support, before comparing.',
        '<strong>Commitments change the public picture.</strong> Reserved instances and savings plans can cut 30 to 60 percent off compute, in exchange for a one or three year commitment.',
        '<strong>Data transfer is the hidden public cost.</strong> Data leaving the cloud is charged. Applications that send a lot of data out can cost far more than their VMs.']), prose=True)
    b += sec('<h2>What the calculator leaves out</h2>' + ul([
        'Migration effort and any application changes.',
        'Network links between sites, and disaster recovery.',
        'Hardware refresh after about five years on the private side.',
        'Taxes, and discounts you may negotiate beyond list prices.']) +
        '<p>For a proper comparison we build a costed model from your VM inventory and real quotes. <a href="/contact">Ask for one</a>.</p>', prose=True)
    b += more('cloud-cost') + CTA
    page('solutions/cloud/cloud-cost.html', 'Private vs Public Cloud Cost: Five-Year Calculator | Vakratron Systems',
         'Compare private and public cloud cost over three to five years with your own numbers: VMs, storage, commitments, data transfer, hardware, colocation, support and people.', b, scripts=SCRIPTS)


# =================================================================== FAQ
def faq():
    qa = [
        ('Is OpenStack too complex for a mid-sized organisation?', '<p>It can be. OpenStack makes sense when you need multi-tenancy, self-service and an API that teams build on. If you mainly need to run VMs reliably, Proxmox VE or a smaller KVM platform is simpler to operate. We recommend the smallest platform that meets the need.</p>'),
        ('How long does a VMware to KVM migration take?', '<p>For a few hundred VMs, typically three to six months: a few weeks for inventory and design, a few weeks to build and test the target, then waves every week or two. The pace is usually set by application owners\' testing time, not by conversion speed.</p>'),
        ('Can we keep some VMs on VMware?', '<p>Yes. Some appliances and vendor applications are only supported on VMware. A small remaining vSphere cluster, or moving those few systems to public cloud, is often cheaper than forcing them onto KVM.</p>'),
        ('Will moving to public cloud save us money?', '<p>Sometimes. It usually saves money for spiky, short-lived or fast-growing workloads, and costs more for large, steady ones running 24x7. Use the <a href="/solutions/cloud/cloud-cost">cost calculator</a> with your own numbers.</p>'),
        ('Can our data stay in India?', '<p>Yes. Major public clouds have Indian regions, and a private cloud can sit in any data centre you choose. Check what your regulator or contracts require: some need data in India, some need it on infrastructure you control.</p>'),
        ('How do we avoid lock-in?', '<p>Build with open tools where you can (KVM, Ceph, Kubernetes, Terraform), keep infrastructure as code, and be deliberate about which managed services you depend on. Some lock-in is a fair price for a service you would not want to run yourself.</p>'),
        ('What skills does our team need to run a private cloud?', '<p>Linux, networking and automation (Ansible or similar) are the foundation. OpenStack and Ceph skills can be built over the first months with good runbooks and some support. We plan this handover as part of the project.</p>'),
        ('What do you need from us to start?', '<p>An export of your VM inventory (RVTools is ideal), a short list of your most important applications and their owners, and what is driving the change: cost, a renewal date, compliance or growth.</p>'),
    ]
    items = ''.join(f'<details><summary>{q}</summary><div>{a}</div></details>' for q, a in qa)
    b = hero((HOME, HUB, ("FAQ", None)), 'Cloud guide', 'Cloud questions, answered', 'Short answers to the questions IT heads ask us most often about private cloud, public cloud and leaving VMware.')
    b += sec(items, prose=True) + more('faq') + CTA
    page('solutions/cloud/faq.html', 'Cloud FAQ: OpenStack, VMware Exit, Public Cloud Cost, Data in India | Vakratron Systems',
         'Plain answers to common cloud questions: is OpenStack too complex, how long a VMware to KVM migration takes, public cloud cost, data residency in India, lock-in and skills.', b)


# =================================================================== USE CASE
def usecase():
    b = f'''
        <div class="vk-wrap vk-hero">
            {crumb(HOME, HUB, ("Use case: leaving VMware", None))}
            <div class="vk-label"><span>Illustrative scenario</span></div>
            <h1>Leaving VMware: 300 VMs to OpenStack in six waves</h1>
            <p class="vk-lead">How we would approach a VMware exit for a manufacturing company facing a sharp renewal increase, with a plant ERP that cannot afford a bad weekend.</p>
            <div class="vk-note"><p class="vk-small">This is a composite example built from requirements that are common in mid-sized enterprises. It is not a specific client engagement, and the figures are design targets for the scenario, not measured results.</p></div>
            <div class="vk-facts">
                <div class="vk-fact"><span class="k">Starting point</span><span class="v">300 VMs on vSphere</span></div>
                <div class="vk-fact"><span class="k">Driver</span><span class="v">Licence renewal</span></div>
                <div class="vk-fact"><span class="k">Target</span><span class="v">OpenStack on KVM, Ceph</span></div>
                <div class="vk-fact"><span class="k">Timeline</span><span class="v">About 5 months</span></div>
            </div>
        </div>'''
    b += sec('''<span class="vk-eyebrow">The situation</span><h2>A renewal quote and a fixed date</h2>
            <p>The company ran about 300 VMs on a six-host vSphere cluster: plant ERP, MES on the shop floor, email, file servers, HR and a long tail of small applications. The VMware renewal quote under the new subscription model was several times the previous support cost, and the renewal date was seven months away.</p>
            <p>The IT head had two constraints: the ERP could only be touched on a planned weekend, and the infrastructure team of four could not double in size to run a new platform.</p>''', prose=True)
    b += sec('''<span class="vk-eyebrow">What we found</span><h2>Most VMs were easy. A few were not.</h2>''' + ul([
        'About 85 percent of VMs were standard Linux and Windows servers with no special dependencies.',
        'Two vendor appliances were supported only on VMware.',
        'The MES system licensed itself against a MAC address.',
        'Several Windows VMs ran old versions that needed virtio drivers added before conversion.',
        'Dependency mapping showed the ERP talked to eleven other systems, four of which nobody had listed.']) + '<p>That last point alone justified two weeks of discovery before any conversion.</p>', prose=True)
    b += sec('<span class="vk-eyebrow">The design</span><h2>Target platform and waves</h2>' + table(['Component', 'Design'],
        [['Control plane', '3 nodes, also running network gateways'],
         ['Compute', '7 KVM hosts, sized for current load plus one spare and growth'],
         ['Storage', '5-node Ceph cluster, NVMe for databases, three copies of all data'],
         ['Deployment', 'Kolla-Ansible, so the in-house team can run upgrades'],
         ['Backup', 'New backup for KVM, tested before the pilot wave'],
         ['Kept on VMware', 'The two vendor appliances, on a small licensed host, until the vendor certifies KVM']]) +
        table(['Wave', 'What moves', 'Why in this order'],
        [['1 (pilot)', '15 test and tool VMs', 'Prove the tooling, drivers and runbook'],
         ['2', '40 file, print and intranet VMs', 'Simple workloads, quick wins'],
         ['3', '50 small business apps', 'Builds speed with low risk'],
         ['4', 'HR, email and collaboration', 'Business-visible, but well understood'],
         ['5', 'MES, after fixing the MAC licence binding', 'Plant-facing, so tested with shop-floor users'],
         ['6', 'ERP and the systems it depends on', 'Most critical last, on a planned weekend']]))
    b += sec('''<span class="vk-eyebrow">Rollback</span><h2>The safety net</h2>
            <p>Every wave was converted and tested on KVM while the VMware VMs stayed live. Only after the application owner signed off were users moved. The VMware copies stayed intact, powered off, for two weeks after each wave. The vSphere licence was kept for one extra month after the final wave, so a rollback remained possible right up to the end.</p>''', prose=True)
    b += sec('<span class="vk-eyebrow">What changes</span><h2>Before and after (design targets)</h2>' + table(['', 'Before', 'After (target)'],
        [['Hypervisor licence cost', 'Large renewal increase', 'Platform subscriptions and support only'],
         ['VMs on VMware', '300', '2 vendor appliances'],
         ['Upgrades', 'Done by the vendor partner', 'Run by the in-house team with runbooks'],
         ['New VM for a project', 'Ticket to IT, days', 'Self-service portal, minutes'],
         ['Rollback during migration', 'Not applicable', 'Available for every wave']]))
    b += sec('''<span class="vk-eyebrow">Trade-offs</span><h2>What we would flag</h2>''' + ul([
        '<strong>No automatic load balancing like DRS.</strong> Capacity is planned with more headroom and reviewed monthly.',
        '<strong>New skills for the team.</strong> Two engineers need OpenStack and Ceph training, and the first upgrade should be done together with us.',
        '<strong>Two platforms for a while.</strong> Until the appliances are certified for KVM, a small VMware footprint remains.',
        '<strong>Testing time is the real bottleneck.</strong> Application owners must make time to test each wave, or the plan slips.']), prose=True)
    b += sec('<p>See the method in detail on <a href="/solutions/cloud/vmware-to-kvm-migration">VMware to KVM migration</a>, including an animated wave simulation.</p>', prose=True)
    b += CTA
    page('use_cases/cloud-vmware-exit.html', 'Use Case: Leaving VMware, 300 VMs to OpenStack in Six Waves | Vakratron Systems',
         'An illustrative scenario: moving 300 VMs from VMware vSphere to OpenStack on KVM in six dependency-based waves, with rollback, platform design and trade-offs.', b)


if __name__ == '__main__':
    hub(); private(); vmware(); hybrid(); landing(); ops(); cost(); faq(); usecase()
