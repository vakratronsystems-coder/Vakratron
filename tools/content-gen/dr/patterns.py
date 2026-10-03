"""Generates one page per DR pattern: /solutions/dc-dr/<slug>.html"""
from tpl import page, crumb, CTA
from refarch import render

ORDER = ['backup-restore', 'pilot-light', 'warm-standby', 'active-passive', 'active-active']

def N(zone, row=None, col='full', title='', sub='', style='run', x=None, w=None):
    d = dict(zone=zone, title=title, sub=sub, style=style, col=col)
    if row is not None: d['row'] = row
    if x is not None: d['x'], d['w'] = x, w
    return d

def F(a, b, kind, n=None):
    return dict(a=a, b=b, kind=kind, n=n)

USERS = N('G', title='Users', sub='reach the service via DNS', style='global', x=390, w=180)

P = {}

# ---------------------------------------------------------------- BACKUP & RESTORE
P['backup-restore'] = dict(
    name='Backup and restore', short='Backup & restore', cost=1,
    title='Backup and Restore DR: How It Works, Architecture and When to Use It',
    desc='How backup-and-restore disaster recovery works: reference architecture, the 3-2-1 rule, immutable copies, restore-time maths, a recovery runbook, and when this pattern is enough.',
    lead='The simplest and cheapest form of disaster recovery. Copies of your data are kept somewhere safe, away from the main site. If the main site is lost, you build servers, restore the data and start the applications again.',
    facts=[('Data you could lose', 'Since the last good backup'), ('Time to recover', 'Hours to days'), ('Runs at DR every day', 'Storage only'), ('Relative cost', '1 of 5')],
    diagram=dict(
        panels=('Primary site', 'Offsite / DR location'), rows=3,
        nodes={
            'users': USERS,
            'apps': N('P', 0, title='Applications and databases', sub='production workloads'),
            'bkp': N('P', 1, title='Backup server', sub='runs scheduled backup jobs'),
            'repo': N('P', 2, title='Local backup repository', sub='fast restores, short retention'),
            'rec': N('D', 0, title='Recovery environment', sub='servers built or rented on the day', style='none'),
            'imm': N('D', 1, title='Immutable offsite copy', sub='cannot be changed or deleted', style='backup'),
            'off': N('D', 2, title='Offline copy (optional)', sub='tape or air-gapped disk', style='backup'),
        },
        flows=[F('users', 'P', 'traffic'), F('users', 'D', 'failover'),
               F('apps', 'bkp', 'stream', 1), F('bkp', 'repo', 'stream', 2), F('repo', 'imm', 'batch', 3),
               F('imm', 'off', 'batch', 4), F('imm', 'rec', 'ondemand', 5)]),
    parts=[
        ('1', 'Backup jobs', 'The backup server copies applications and databases on a schedule, usually every night, with database log backups more often if a lower RPO is needed.'),
        ('2', 'Local repository', 'The first copy lands on disk at the primary site. Most everyday restores, such as a deleted file or a corrupted VM, come from here because it is fast.'),
        ('3', 'Offsite copy', 'A copy job sends the backups to a second location. This copy is immutable: once written, it cannot be changed or deleted until its retention period ends, even by an administrator.'),
        ('4', 'Offline copy', 'Optionally, a periodic copy to tape or a disconnected disk. It is the last line of defence if both online copies are compromised.'),
        ('5', 'Restore on disaster day', 'After a disaster, servers are built at the recovery location and data is restored from the offsite copy, starting with the most important systems.'),
    ],
    how='''<p>Most teams follow the <strong>3-2-1 rule</strong>: three copies of the data, on two different types of storage, with one copy offsite. A common extension, 3-2-1-1-0, adds one copy that is immutable or offline, and zero errors in restore tests.</p>
<p>The weak point of this pattern is time. Nothing is running at the DR location, so everything has to be built and restored after the disaster. Restore speed is limited by bandwidth and disks: restoring 10 TB over a 1 Gbps link takes close to a full day even at full line speed, and real restores are often slower.</p>''',
    runbook=['Declare the disaster and confirm which backup point you will restore from.',
             'Get compute at the recovery location: a cloud account, spare hardware, or a pre-agreed rental contract.',
             'Rebuild the foundations first: network, firewall rules, Active Directory and DNS.',
             'Restore databases, then application servers, in the priority order agreed with the business.',
             'Have application owners test before users are let in.',
             'Point DNS at the recovered systems and announce the service is back.'],
    failback='Once the primary site is rebuilt, take a fresh backup at the recovery location and restore it to the primary in a planned maintenance window.',
    fits=['Development, test and training systems', 'File shares, archives and internal tools', 'Smaller organisations without a second data centre', 'The base layer under every other pattern: you always need backups, even with replication'],
    notfits=['Customer-facing or revenue systems that must be back within hours', 'Large databases where a full restore would take days', 'Systems where losing a day of data is unacceptable'],
    watch=['<strong>Restore speed.</strong> Test how long a full restore of your largest system really takes. That number, not the backup schedule, is your realistic RTO.',
           '<strong>The backup server itself.</strong> If the backup server and its catalogue are lost with the primary site, restores stall. Keep its configuration and catalogue offsite too.',
           '<strong>Ransomware.</strong> Attackers look for backups first. Use immutable storage and separate credentials: the backup administrator account should not be a domain administrator.',
           '<strong>Hardware on the day.</strong> If you plan to restore onto your own hardware, make sure it will actually be available. Lead times for servers can run into weeks.'],
    tools=[('Backup software', 'Veeam, Commvault, Veritas NetBackup, Bacula or Bareos (open source)'),
           ('Immutable storage', 'S3-compatible object storage with Object Lock, hardened Linux repositories'),
           ('Offline copies', 'LTO tape, rotated disks'),
           ('Rebuilding servers', 'VM templates, Terraform, Ansible')],
)

# ---------------------------------------------------------------- PILOT LIGHT
P['pilot-light'] = dict(
    name='Pilot light', short='Pilot light', cost=2,
    title='Pilot Light DR: How It Works, Architecture and When to Use It',
    desc='How pilot light disaster recovery works: a small always-on database replica, replicated storage and ready-to-start server templates. Reference architecture, runbook and trade-offs.',
    lead='Keep the parts that are hardest to rebuild, your data and your database, alive at the DR site all the time in a small form. Everything else exists as ready templates that are switched on only when needed.',
    facts=[('Data you could lose', 'Minutes'), ('Time to recover', 'A few hours'), ('Runs at DR every day', 'Small DB replica, storage, directory'), ('Relative cost', '2 of 5')],
    diagram=dict(
        panels=('Primary site', 'DR site'), rows=5,
        nodes={
            'users': USERS,
            'lb': N('P', 0, title='Load balancer'),
            'web': N('P', 1, 'l', 'Web servers', '4 running'), 'app': N('P', 1, 'r', 'App servers', '4 running'),
            'db': N('P', 2, title='Database', sub='primary, read-write'),
            'dir': N('P', 3, title='Active Directory and DNS', sub='identity and name services'),
            'vol': N('P', 4, title='Storage volumes', sub='application data'),
            'lb2': N('D', 0, title='Load balancer', sub='configured, switched off', style='off'),
            'web2': N('D', 1, 'l', 'Web servers', 'template, off', style='off'), 'app2': N('D', 1, 'r', 'App servers', 'template, off', style='off'),
            'db2': N('D', 2, title='Database replica', sub='small instance, read-only', style='idle'),
            'dir2': N('D', 3, title='Directory replica', sub='running', style='run'),
            'vol2': N('D', 4, title='Replicated volumes', sub='asynchronous copy', style='idle'),
        },
        flows=[F('users', 'P', 'traffic'), F('users', 'D', 'failover'),
               F('app', 'web2', 'batch', 1), F('db', 'db2', 'stream', 2), F('dir', 'dir2', 'stream', 3), F('vol', 'vol2', 'stream', 4)]),
    parts=[
        ('1', 'Server templates', 'Golden images of the web and application servers are refreshed at DR after every patch cycle or release. The servers themselves stay switched off.'),
        ('2', 'Database replication', 'Changes stream continuously from the primary database to a small replica at DR. The replica is read-only until it is promoted.'),
        ('3', 'Directory replication', 'A domain controller and DNS server run at DR all the time. Almost every application depends on them, and they are slow to rebuild from scratch.'),
        ('4', 'Storage replication', 'Application volumes are copied asynchronously to the DR storage, a few seconds to minutes behind production.'),
    ],
    how='''<p>The name comes from gas boilers: a small flame stays lit so the full burner can be started quickly. Here, the small flame is the replicated data and database. Because the data is already at DR and current to within minutes, recovery is mostly about starting servers, not restoring terabytes.</p>
<p>What decides the recovery time is how the stopped servers get started. If it is done by hand, it can take a day. With automation (Terraform, Heat or Ansible) and current templates, it is usually a few hours, most of which is testing.</p>''',
    runbook=['Declare the disaster.',
             'Promote the database replica to primary and increase its size to production capacity.',
             'Run the automation that starts web and application servers from the current templates.',
             'Attach the replicated volumes and start services in dependency order.',
             'Run health checks and a short test with application owners.',
             'Switch DNS or the global load balancer to the DR site.'],
    failback='Reverse the replication so the rebuilt primary catches up from DR, then do a planned switchover back in a maintenance window.',
    fits=['Core business systems that can be down for half a day, but cannot lose a day of data', 'ERP, HR and payroll, internal portals, e-commerce back office', 'Organisations that want real DR without paying for a second running copy'],
    notfits=['Systems that must be back within an hour', 'Applications that cannot be built automatically and need long manual set-up'],
    watch=['<strong>Stale templates.</strong> If the DR images miss last month\'s patches or configuration changes, servers start but applications fail. Refresh them as part of every release.',
           '<strong>Untested automation.</strong> Scripts that have never run in anger usually fail on the first try. Run them in every drill.',
           '<strong>Scaling the database.</strong> On-premises, the hardware to run the database at full size must already be at the DR site.',
           '<strong>Secrets and certificates.</strong> Make sure TLS certificates, keys and service passwords are available at DR, not only in the primary vault.'],
    tools=[('Database replication', 'Oracle Data Guard, SQL Server Always On (asynchronous), PostgreSQL streaming replication, MySQL replication'),
           ('Storage replication', 'Ceph RBD mirroring, storage-array asynchronous replication, cloud volume replication'),
           ('Templates and automation', 'Packer for images, Terraform, OpenStack Heat, Ansible'),
           ('Directory', 'Additional AD domain controller and DNS server at DR')],
)

# ---------------------------------------------------------------- WARM STANDBY
P['warm-standby'] = dict(
    name='Warm standby', short='Warm standby', cost=3,
    title='Warm Standby DR: How It Works, Architecture and When to Use It',
    desc='How warm standby disaster recovery works: a complete scaled-down copy of the application running at DR, scaled up on failover. Reference architecture, runbook and trade-offs.',
    lead='A complete, working copy of the application runs at the DR site every day, just at a smaller size. Because it is already running, you know it works. On failover you scale it up and send users to it.',
    facts=[('Data you could lose', 'Seconds to minutes'), ('Time to recover', 'Under an hour to a few hours'), ('Runs at DR every day', 'Full stack, about a quarter size'), ('Relative cost', '3 of 5')],
    diagram=dict(
        panels=('Primary site', 'DR site'), rows=4,
        nodes={
            'users': N('G', title='Users and global DNS', sub='health checks on both sites', style='global', x=370, w=220),
            'cicd': N('G', title='Release pipeline', sub='deploys to both sites', style='global', x=760, w=180),
            'lb': N('P', 0, title='Load balancer'),
            'web': N('P', 1, 'l', 'Web servers', '4 running'), 'app': N('P', 1, 'r', 'App servers', '4 running'),
            'db': N('P', 2, title='Database', sub='primary, read-write'),
            'vol': N('P', 3, title='Storage volumes', sub='application data'),
            'lb2': N('D', 0, title='Load balancer', sub='running', style='run'),
            'web2': N('D', 1, 'l', 'Web servers', '1 running', style='idle'), 'app2': N('D', 1, 'r', 'App servers', '1 running', style='idle'),
            'db2': N('D', 2, title='Database replica', sub='full size, read-only', style='idle'),
            'vol2': N('D', 3, title='Replicated volumes', sub='asynchronous copy', style='idle'),
        },
        flows=[F('users', 'P', 'traffic'), F('users', 'D', 'failover'), F('cicd', 'D', 'deploy', 3),
               F('db', 'db2', 'stream', 1), F('vol', 'vol2', 'stream', 2)]),
    parts=[
        ('1', 'Database replication', 'The DR database is a continuously updated replica. It is sized to take the full production load as soon as it is promoted.'),
        ('2', 'Storage replication', 'Application data is copied asynchronously, normally seconds to a few minutes behind.'),
        ('3', 'Release pipeline', 'Every release is deployed to both sites. This is what keeps the DR copy identical to production instead of drifting over time.'),
        ('', 'Health checks', 'The global DNS or load balancer checks the DR application continuously, so a broken standby is noticed on a normal Tuesday, not on disaster day.'),
    ],
    how='''<p>The difference from pilot light is that every tier is already running at DR. Nothing has to be built on the day, only enlarged. That removes the biggest source of surprises, and many teams send a small amount of real or test traffic to the DR copy to prove it works.</p>
<p>The trade-off is cost and discipline. You pay for a running environment every day, and every change must reach both sites or the standby slowly stops matching production.</p>''',
    runbook=['Declare the disaster.',
             'Promote the DR database replica to primary.',
             'Scale web and application tiers from one server to full size, from reserved capacity or an autoscaling group.',
             'Confirm health checks are green and run a short user test.',
             'Switch the global DNS or load balancer to the DR site.'],
    failback='Rebuild replication from DR back to the primary, let it catch up, then switch over in a planned window and scale DR back down.',
    fits=['Customer portals and citizen-facing services', 'Hospital information systems, large ERP platforms', 'Systems where the business can tolerate one to two hours of downtime at most'],
    notfits=['Systems that need recovery in minutes with near-zero data loss', 'Environments without a disciplined release process'],
    watch=['<strong>Capacity on the day.</strong> On-premises, the hardware for full size must exist at DR. In the cloud, reserve capacity or check quotas, because everyone scales up at once in a regional event.',
           '<strong>Release drift.</strong> If a release goes to production but not DR, failover brings up last month\'s application. Put DR in the pipeline, not in a manual checklist.',
           '<strong>Database size.</strong> A small DR database saves money but must be resized before it can take full write load. Decide whether you can afford that delay.',
           '<strong>Cost creep.</strong> Running DR instances tend to grow. Review their size every quarter.'],
    tools=[('Traffic switching', 'Global server load balancing (F5, Citrix ADC), cloud DNS failover with health checks'),
           ('Scaling', 'VM autoscaling groups, Kubernetes horizontal scaling, reserved capacity'),
           ('Release pipeline', 'GitLab CI, Jenkins, Argo CD deploying to both sites'),
           ('Replication', 'Database-native replication plus storage or volume replication')],
)

# ---------------------------------------------------------------- ACTIVE-PASSIVE
P['active-passive'] = dict(
    name='Active-passive', short='Active-passive', cost=4,
    title='Active-Passive DR: How It Works, Architecture and When to Use It',
    desc='How active-passive disaster recovery works: a full-size synchronised copy at DR, a witness to avoid split brain, and failover in minutes. Reference architecture, runbook and trade-offs.',
    lead='A full-size copy of production waits at the DR site, kept in step with the primary. If the primary fails, the passive site takes over within minutes, usually with most of the work automated.',
    facts=[('Data you could lose', 'Near zero (synchronous)'), ('Time to recover', 'Minutes'), ('Runs at DR every day', 'Full-size copy, not serving users'), ('Relative cost', '4 of 5')],
    diagram=dict(
        panels=('Primary site', 'DR site (passive)'), rows=4,
        nodes={
            'users': N('G', title='Users and global DNS', sub='health checks on both sites', style='global', x=370, w=220),
            'lb': N('P', 0, title='Load balancer'),
            'web': N('P', 1, 'l', 'Web servers', '4 running'), 'app': N('P', 1, 'r', 'App servers', '4 running'),
            'db': N('P', 2, title='Database', sub='primary, read-write'),
            'vol': N('P', 3, title='Storage', sub='primary copy'),
            'lb2': N('D', 0, title='Load balancer', sub='ready', style='idle'),
            'web2': N('D', 1, 'l', 'Web servers', '4 on standby', style='idle'), 'app2': N('D', 1, 'r', 'App servers', '4 on standby', style='idle'),
            'db2': N('D', 2, title='Database replica', sub='synchronous, full size', style='idle'),
            'vol2': N('D', 3, title='Storage', sub='synchronous copy', style='idle'),
            'wit': N('B', title='Witness', sub='third location, decides who is primary', style='witness', x=370, w=220),
        },
        flows=[F('users', 'P', 'traffic'), F('users', 'D', 'failover'),
               F('db', 'db2', 'sync', 1), F('vol', 'vol2', 'sync', 2), F('wit', 'db', 'hb', 3), F('wit', 'db2', 'hb')]),
    parts=[
        ('1', 'Synchronous database replication', 'A transaction is only confirmed to the user once it is written at both sites. That is what gives near-zero data loss.'),
        ('2', 'Synchronous storage replication', 'Storage arrays or software-defined storage mirror every write to the DR site in the same way.'),
        ('3', 'Witness', 'A small service at a third location that both sites can reach. If the sites lose contact with each other, the witness decides which one stays primary, so both never accept writes at once.'),
        ('', 'Global DNS', 'Health checks watch both sites and move users to DR when the primary stops responding.'),
    ],
    how='''<p>Synchronous replication has a physical limit. Every write waits for the other site to confirm, and light in fibre adds roughly one millisecond of round trip for every 100 km. That is why synchronous pairs are usually within about 100 km of each other.</p>
<p>That distance protects against a building, power or network failure, but not always against a regional event. Organisations that need both often add a third, distant site with asynchronous replication.</p>''',
    runbook=['Monitoring or the witness detects that the primary is lost.',
             'The DR database and storage are promoted to primary, automatically or with one approval.',
             'The standby application servers connect to the new primary database.',
             'Global DNS moves users to the DR site.',
             'Operations confirm transactions are flowing and notify the business.'],
    failback='Re-establish synchronous replication from DR to the repaired primary, wait until both are in sync, then switch back in a planned window, or simply keep running from the DR site.',
    fits=['Core banking, payments, billing and trading systems', 'Telecom and utility operations systems', 'Any system where a few minutes of downtime is the limit and data loss must be near zero'],
    notfits=['Sites more than about 100 km apart (use asynchronous replication instead)', 'Budgets that cannot carry a full idle copy of production'],
    watch=['<strong>Write latency.</strong> Every write now waits for the DR site. Test application performance with synchronous replication on before go-live.',
           '<strong>Split brain.</strong> Without a witness, a network cut between sites can leave both thinking they are primary. Always place a witness at a third location.',
           '<strong>Automation you never test.</strong> Automatic failover that has not been exercised can fail, or trigger when it should not. Test it at least twice a year.',
           '<strong>Regional events.</strong> Two sites close together can be hit by the same flood or grid failure. Consider a third, distant site for the most critical data.'],
    tools=[('Database', 'Oracle Data Guard (Maximum Availability), SQL Server Always On with synchronous commit, PostgreSQL synchronous replication with Patroni'),
           ('Storage', 'NetApp MetroCluster, Dell PowerMax SRDF, Pure Storage ActiveCluster, Ceph stretch clusters'),
           ('Traffic', 'Global server load balancing with health checks (F5 BIG-IP DNS, Citrix ADC)'),
           ('Network', 'Dark fibre or DWDM links with diverse paths between the sites')],
)

# ---------------------------------------------------------------- ACTIVE-ACTIVE
P['active-active'] = dict(
    name='Active-active', short='Active-active', cost=5,
    title='Active-Active DR: How It Works, Architecture and When to Use It',
    desc='How active-active disaster recovery works: two sites serving users at once, global load balancing, two-way data replication and what it takes from the application. Reference architecture and trade-offs.',
    lead='Both sites serve users all the time. If one site is lost, the other is already carrying live traffic and simply takes the full load. For users, recovery is close to instant.',
    facts=[('Data you could lose', 'Near zero'), ('Time to recover', 'Near zero for users'), ('Runs at DR every day', 'Two full sites at ~50% load'), ('Relative cost', '5 of 5')],
    diagram=dict(
        panels=('Site A', 'Site B'), rows=5,
        nodes={
            'glb': N('G', title='Global load balancer', sub='splits users across both sites', style='global', x=360, w=240),
            'lb': N('P', 0, title='Load balancer'), 'lb2': N('D', 0, title='Load balancer'),
            'web': N('P', 1, 'l', 'Web servers', 'stateless'), 'app': N('P', 1, 'r', 'App servers', 'stateless'),
            'web2': N('D', 1, 'l', 'Web servers', 'stateless'), 'app2': N('D', 1, 'r', 'App servers', 'stateless'),
            'ses': N('P', 2, title='Session store', sub='replicated cache'), 'ses2': N('D', 2, title='Session store', sub='replicated cache'),
            'db': N('P', 3, title='Database', sub='accepts writes'), 'db2': N('D', 3, title='Database', sub='accepts writes'),
            'obj': N('P', 4, title='Files and objects', sub='replicated both ways'), 'obj2': N('D', 4, title='Files and objects', sub='replicated both ways'),
        },
        flows=[F('glb', 'P', 'traffic'), F('glb', 'D', 'traffic'),
               F('ses', 'ses2', 'bi', 1), F('db', 'db2', 'bi', 2), F('obj', 'obj2', 'bi', 3)]),
    parts=[
        ('1', 'Session replication', 'User sessions are kept in a shared, replicated store rather than on one server, so a user moved to the other site does not have to log in again.'),
        ('2', 'Two-way database replication', 'Both sites accept writes. This needs a database designed for it, or an application that splits data so each record has one home site.'),
        ('3', 'File and object replication', 'Uploaded files and objects are copied in both directions so either site can serve them.'),
        ('', 'Global load balancer', 'Sends each user to a site by location or weight, and stops sending users to a site that fails its health checks.'),
    ],
    how='''<p>Active-active is as much an application design as an infrastructure design. Web and application servers must be stateless, every operation must be safe to retry, and the database must cope with writes arriving at two places at once.</p>
<p>In practice, many systems described as active-active run the web and application tiers active-active and keep the database active-passive. That gives most of the benefit with far less risk, and it is often the right choice.</p>''',
    runbook=['Health checks for one site fail.',
             'The global load balancer stops sending new users to that site. With DNS-based balancing, short TTLs keep this to seconds or minutes.',
             'The surviving site absorbs the full load, using the headroom it was sized with.',
             'No database promotion is needed if both sites already accept writes.',
             'When the failed site returns, it resynchronises and is added back gradually.'],
    failback='There is no separate failback. The repaired site catches up on data and the load balancer slowly returns users to it.',
    fits=['Large digital channels, SaaS platforms and internet-facing services', 'Applications built or rebuilt as stateless services', 'Organisations with mature operations and automated testing'],
    notfits=['Existing applications that keep state on the server or cannot be changed', 'Databases that cannot accept writes at two sites safely', 'Teams without the operational maturity to run two live sites'],
    watch=['<strong>Data conflicts.</strong> Two users changing the same record at two sites at the same moment must be handled by design, not discovered in production.',
           '<strong>Headroom.</strong> Each site must carry 100% of the load alone. In normal running each is at most half used.',
           '<strong>Hidden single points.</strong> A shared licence server, identity provider or payment gateway at one site quietly breaks the design. Map every dependency.',
           '<strong>Testing.</strong> Regularly drain one site completely during business hours to prove the other can carry everything.'],
    tools=[('Traffic', 'Global server load balancing, anycast, cloud global load balancers'),
           ('Application platform', 'Kubernetes clusters at both sites, managed with GitOps'),
           ('Data', 'Distributed SQL databases (CockroachDB, YugabyteDB), MariaDB Galera, or application-level data partitioning'),
           ('Sessions and messaging', 'Replicated Redis, Kafka with MirrorMaker 2')],
)


def facts_html(p):
    return ''.join(f'<div class="vk-fact"><span class="k">{k}</span><span class="v">{v}</span></div>' for k, v in p['facts'])


def build(slug):
    p = P[slug]
    i = ORDER.index(slug)
    prev_s = ORDER[i - 1] if i > 0 else None
    next_s = ORDER[i + 1] if i < len(ORDER) - 1 else None
    svg = render(p['diagram'], f"{p['name']} reference architecture")
    parts = ''.join(f'<tr><td>{(f"<span class=vk-num>{n}</span> " if n else "") + t}</td><td>{d}</td></tr>' for n, t, d in p['parts'])
    runbook = ''.join(f'<li>{s}</li>' for s in p['runbook'])
    fits = ''.join(f'<li>{s}</li>' for s in p['fits'])
    notfits = ''.join(f'<li>{s}</li>' for s in p['notfits'])
    watch = ''.join(f'<li>{s}</li>' for s in p['watch'])
    tools = ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in p['tools'])
    others = ''.join(
        f'<a class="vk-pill{" on" if s == slug else ""}" href="/solutions/dc-dr/{s}">{P[s]["short"]}</a>' for s in ORDER)
    nav = '<div class="vk-pager">'
    nav += (f'<a class="vk-card" href="/solutions/dc-dr/{prev_s}"><span class="vk-muted vk-small">&larr; Previous pattern</span><h3>{P[prev_s]["name"]}</h3></a>' if prev_s else '<span></span>')
    nav += (f'<a class="vk-card" style="text-align:right" href="/solutions/dc-dr/{next_s}"><span class="vk-muted vk-small">Next pattern &rarr;</span><h3>{P[next_s]["name"]}</h3></a>' if next_s else '<span></span>')
    nav += '</div>'

    body = f'''
        <div class="vk-wrap vk-hero">
            {crumb(("Home", "/"), ("Disaster Recovery", "/portfolio/dr-solutions"), ("DR patterns", "/solutions/dc-dr/strategy-selection"), (p["name"], None))}
            <div class="vk-pills">{others}</div>
            <span class="vk-eyebrow">DR pattern {i + 1} of 5</span>
            <h1>{p["name"]}</h1>
            <p class="vk-lead">{p["lead"]}</p>
            <div class="vk-facts">{facts_html(p)}</div>
        </div>

        <div class="vk-sec"><div class="vk-wrap">
            <span class="vk-eyebrow">See it working</span>
            <h2>What happens in a disaster</h2>
            <p class="vk-prose">This is what runs at each site on a normal day. Press <strong>Simulate a disaster</strong> to watch the primary site fail and the DR site take over, step by step.</p>
            <div class="vk-drsim" data-only="{slug}"></div>
            <noscript><p class="vk-muted">The interactive diagram needs JavaScript. The reference architecture below shows the same design.</p></noscript>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <span class="vk-eyebrow">Reference architecture</span>
            <h2>How the pieces fit together</h2>
            <figure class="vk-fig vk-refarch"><span class="vk-scroll-hint">Scroll sideways to see both sites &rarr;</span><div class="vk-refarch-scroll">{svg}</div>
                <figcaption>Numbered lines show how data moves between the sites. Solid boxes are running, faint boxes are on standby or reduced size, and dashed boxes are switched off or not yet built.{" The dashed grey line is the path users take after failover." if any(f["kind"] == "failover" for f in p["diagram"]["flows"]) else ""}</figcaption>
            </figure>
            <div class="vk-table-wrap"><table>
                <thead><tr><th>Part</th><th>What it does</th></tr></thead>
                <tbody>{parts}</tbody>
            </table></div>
            <div class="vk-prose">{p["how"]}</div>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <div class="vk-two">
                <div>
                    <span class="vk-eyebrow">Runbook</span>
                    <h2>How failover works</h2>
                    <ol class="vk-steps">{runbook}</ol>
                    <p><strong>Failback:</strong> {p["failback"]}</p>
                </div>
                <div>
                    <span class="vk-eyebrow">Fit</span>
                    <h2>When to use it</h2>
                    <ul>{fits}</ul>
                    <h3 style="margin-top:22px !important">When it is not enough</h3>
                    <ul>{notfits}</ul>
                </div>
            </div>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap"><div class="vk-prose">
            <span class="vk-eyebrow">Lessons from the field</span>
            <h2>What to watch out for</h2>
            <ul>{watch}</ul>
        </div></div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <span class="vk-eyebrow">Technology</span>
            <h2>Typical tools for this pattern</h2>
            <p class="vk-prose vk-muted">Examples only. We recommend tools based on what you already run, your team's skills and your licences.</p>
            <div class="vk-table-wrap"><table>
                <thead><tr><th>Layer</th><th>Common choices</th></tr></thead>
                <tbody>{tools}</tbody>
            </table></div>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap">
            {nav}
            <p class="vk-small vk-muted" style="margin-top:16px">Comparing options? See all five patterns side by side in the <a href="/solutions/dc-dr/strategy-selection">DR patterns guide</a>, or read <a href="/solutions/dc-dr/cost-comparison">what DR really costs</a>.</p>
        </div></div>
{CTA}'''
    page(f'solutions/dc-dr/{slug}.html', f'{p["title"]} | Vakratron Systems', p['desc'], body, scripts=['/vk-dr-sim.js'])


if __name__ == '__main__':
    for s in ORDER:
        build(s)
