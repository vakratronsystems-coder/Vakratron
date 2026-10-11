"""Whitepaper content: Disaster recovery strategy (pilot, Oct 2026).
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
DIAGRAM = dict(w=1120, h=455,
  zones=[
    dict(x=20, y=20, w=1080, h=106, title='Users and traffic steering', kind='ext'),
    dict(x=20, y=140, w=505, h=305, title='Primary data centre', kind='dc'),
    dict(x=545, y=140, w=345, h=305, title='DR site', kind='dr'),
    dict(x=905, y=140, w=195, h=305, title='Backup vault', kind='sec'),
  ],
  nodes={
    'users': N(60, 56, 220, 'Users and partners', 'branches, staff, customers', 'users', 'slate'),
    'gslb': N(440, 56, 260, 'Global DNS or load balancer', 'short TTL, health checks', 'globe', 'slate'),
    't1': N(40, 185, 225, 'Tier 1: critical apps', 'core banking, ERP, HIS', 'server', 'blue'),
    't2': N(280, 185, 225, 'Tier 2: business apps', 'portals, MIS, email', 'server', 'blue'),
    't3': N(40, 270, 225, 'Tier 3: other systems', 'dev, archives, tools', 'server', 'slate'),
    'db': N(280, 270, 225, 'Databases', 'clustered, logs shipped', 'storage', 'green'),
    'st': N(40, 355, 465, 'Primary storage', 'volumes, files and objects, with snapshots', 'storage', 'green'),
    't1d': N(560, 185, 155, 'Tier 1 warm', 'half size, running', 'server', 'violet'),
    't2d': N(725, 185, 150, 'Tier 2 pilot', 'templates, off', 'server', 'slate', state='off'),
    'dbd': N(560, 270, 315, 'Database replica', 'asynchronous, minutes behind', 'storage', 'violet'),
    'std': N(560, 355, 315, 'Storage replica', 'snapshot mirroring on a schedule', 'storage', 'violet'),
    'rb': N(915, 185, 175, 'Runbooks', 'tested every quarter', 'doc', 'pink'),
    'cr': N(915, 270, 175, 'Clean restore', 'isolated and scanned', 'check', 'pink'),
    'bk': N(915, 355, 175, 'Immutable backups', 'object lock, 35 days', 'lock', 'pink'),
  },
  flows=[
    dict(a='users', b='gslb', kind='traffic', label='HTTPS'),
    dict(a='gslb', b='t1', kind='traffic', sa=('b', -60), via=[(510, 133), (30, 133), (30, 214)], sb='l'),
    dict(a='gslb', b='t1d', kind='control', sa=('b', 75), sb=('t', 67), label='on failover', lpos=(645, 133)),
    dict(a='db', b='dbd', kind='data', n=1, lpos=(532, 256)),
    dict(a='st', b='std', kind='data', n=2, lpos=(532, 342)),
    dict(a='std', b='bk', kind='batch', n=3, lpos=(895, 342)),
    dict(a='bk', b='cr', kind='batch', label='restore test'),
  ])

META = dict(
    slug='disaster-recovery-strategy',
    title='Disaster Recovery That Works on the Day',
    subtitle='Choosing, building and proving a DR strategy for enterprise and government IT',
    topic='dr',
    area='Data centre and disaster recovery',
    version='Version 1.0, October 2026',
    pages='Approx. 16 pages',
    minutes=22,
    audience='CIOs, IT heads, infrastructure architects, risk and compliance teams',
    audience_web='CIOs, IT heads, infrastructure architects, and risk and compliance teams',
    pdf_name='Vakratron-Disaster-Recovery-Strategy.pdf',
    help_title='How we can help with disaster recovery',
    help_items=['<strong>DR review:</strong> an independent gap review of your current set-up in two to three weeks, with a ranked list of what to fix.',
                '<strong>DR design:</strong> tiering, pattern per tier, reference architecture, sizing and a cost model you can take to vendors.',
                '<strong>Drill support:</strong> planning and running your first isolated or full failover, with measured RPO and RTO.'],
    help_links=[('Ask for a DR review', '/advisory#review'), ('DR solutions', '/portfolio/dr-solutions'), ('See a worked DR design', '/deployments/core-banking-dr')],
    desc='A practical whitepaper on disaster recovery: setting RPO and RTO by business tier, the five DR patterns compared, a decision framework, reference architecture, sizing and cost ranges, ransomware recovery, testing, and a 40-point readiness checklist.',
    inside=['How to set RPO and RTO per application tier, from business impact rather than guesswork',
            'The five DR patterns compared on recovery time, data loss and running cost',
            'A four-question decision framework, and why most organisations need three tiers',
            'Bandwidth, storage and cost formulas with a worked example',
            'Why replication is not ransomware protection, and what is',
            'A testing programme that turns DR from a document into evidence',
            'A 40-point readiness checklist you can use tomorrow'],
)

SECTIONS = []
def S(id, title, html):
    SECTIONS.append(dict(id=id, title=title, html=html))

S('summary', 'Executive summary', '''
<p>Most organisations have a disaster recovery plan. Far fewer have disaster recovery that works when it is needed. The gap is rarely the technology. It is that recovery targets were never agreed with the business, every application was protected the same way, backups shared the same failure as production, and the plan was never rehearsed end to end.</p>
<p>This paper sets out a practical way to close that gap. It is written for the people who have to make DR decisions and defend them: CIOs and IT heads, infrastructure architects, and the risk and compliance teams who sign off.</p>
<div class="wp-keys"><h3>Five things to take away</h3><ol>
<li><strong>Set targets per tier, not per company.</strong> Agree recovery time (RTO) and acceptable data loss (RPO) for each group of applications, starting from what an hour of downtime actually costs.</li>
<li><strong>Use two or three DR patterns, not one.</strong> A handful of critical systems need a warm or hot copy. Most applications do not. Tiering typically cuts DR running cost by 40 to 60 percent against protecting everything the same way.</li>
<li><strong>Replication is not backup.</strong> Replication copies ransomware and mistakes as fast as good data. You need immutable, versioned backups that attackers cannot reach.</li>
<li><strong>The runbook is part of the architecture.</strong> Most of the time lost in a real disaster is spent deciding, finding people and fixing what was never written down.</li>
<li><strong>Only a tested recovery counts.</strong> Measure RPO and RTO in drills, report them against targets, and fix what breaks. Untested DR is a guess.</li>
</ol></div>''')

S('why-dr-fails', 'Why DR fails in practice', '''
<p>Power failures, storage faults, network outages, fire, flooding, ransomware and plain human error all take data centres down. None of these are rare across a five-year horizon. The cost shows up as lost revenue, penalties, customer dissatisfaction, compliance findings and damage to reputation, and it grows with every hour of downtime.</p>
<p>When we review DR set-ups, the same failure modes appear again and again:</p>
''' + table(['What we find', 'What happens on the day'], [
    ['Targets nobody agreed', 'IT built for 4 hours; the business assumed 30 minutes. The argument happens during the outage.'],
    ['Everything protected the same way', 'Either the budget runs out before critical systems are covered, or money is wasted keeping test servers hot.'],
    ['Backups in the same failure domain', 'Backup server in the same room, on the same power feed, or reachable with the same admin password as production.'],
    ['Replication treated as backup', 'Ransomware-encrypted files replicate to DR within minutes. Both sites are now encrypted.'],
    ['Only the data is copied', 'Volumes are at DR, but firewall rules, certificates, DNS, licence servers and identity are not.'],
    ['No one decides', 'There is no named person or agreed criteria for declaring a disaster. Hours pass before failover starts.'],
    ['Never tested end to end', 'The first full failover happens during a real disaster, and it is also the first time failback is attempted.'],
]) + callout('In short:', 'DR fails at the seams between business, technology and people. A good design addresses all three.'))

S('rpo-rto', 'RPO and RTO, set properly', '''
<p><strong>Recovery Point Objective (RPO)</strong> is the maximum amount of data, measured in time, the business can afford to lose. If data is replicated every five minutes, up to five minutes of work can be lost. <strong>Recovery Time Objective (RTO)</strong> is how long a service can be unavailable before the impact becomes unacceptable. An RPO of 15 minutes and an RTO of 2 hours means: lose at most the last 15 minutes of work, and be running again within 2 hours.</p>
<p>Two rules of thumb follow. A lower RPO generally requires more replication and more bandwidth. A lower RTO generally requires more infrastructure running at the DR site. Both cost money, so the targets must come from business impact, not from preference.</p>
<h3>A short business impact analysis</h3>
<p>For each application, ask its business owner four questions and write the answers down:</p>
''' + ul(['What does one hour of downtime cost? Revenue, penalties, patient or citizen impact, regulatory exposure.',
          'How much recent data can be re-entered by hand from paper, email or another system?',
          'Does a regulator, contract or customer SLA set a number?',
          'What else depends on this system, and what does it depend on?']) + '''
<p>Then group applications into tiers. Three tiers are enough for most organisations:</p>
''' + table(['Tier', 'Typical systems', 'RPO target', 'RTO target'], [
    ['Tier 1: critical', 'Core banking, payments, ERP transactions, hospital information system, citizen-facing portals', 'Near zero to 15 minutes', '15 minutes to 2 hours'],
    ['Tier 2: important', 'Customer portals, MIS, email, document management, HR and payroll', '15 minutes to 4 hours', '4 to 12 hours'],
    ['Tier 3: deferrable', 'Development and test, archives, analytics sandboxes, internal tools', '24 hours', '1 to 3 days'],
]) + callout('Watch the dependencies.', 'A tier 1 application that relies on a tier 3 directory or licence server is really a tier 3 application. Map dependencies before you assign tiers.', 'warn'))

S('patterns', 'The five DR patterns', '''
<p>There are five common ways to set up disaster recovery. They differ in what is already running at the DR site before a disaster, and therefore in recovery time, data loss and cost.</p>
''' + table(['Pattern', 'What is ready at DR', 'Typical RPO', 'Typical RTO', 'DR running cost vs production'], [
    ['Backup and restore', 'Backup copies only. Servers are rebuilt after the disaster.', 'Hours (time since last backup)', 'Hours to days', 'About 10 to 20%'],
    ['Pilot light', 'Data replicated. Core services such as database and directory run small. Application servers are off.', 'Minutes', 'A few hours', 'About 20 to 35%'],
    ['Warm standby', 'The full stack runs at reduced size and is scaled up on failover.', 'Seconds to minutes', 'Under an hour to a few hours', 'About 40 to 60%'],
    ['Active-passive', 'A full-size copy is ready to take over.', 'Near zero (synchronous) to minutes', 'Minutes', 'About 80 to 100%'],
    ['Active-active', 'Both sites serve users at the same time.', 'Near zero', 'Near zero for users', '100% or more, plus application changes'],
], 'wp-compact') + '''
<h3>Backup and restore</h3>
<p>Scheduled backups or volume snapshots are copied to storage at another site, ideally object storage with immutability. After a disaster, infrastructure is rebuilt and data restored. Cheap to run, slow to recover, and the RPO is the time since the last good backup. Right for tier 3 and for long-term retention behind every other pattern.</p>
<h3>Pilot light</h3>
<p>The data layer is kept live at the DR site: database replication, for example asynchronous log shipping or a Galera or Always On replica, and storage mirroring on a schedule. Application and web servers exist only as templates and are started on failover. Recovery takes hours because servers must boot, attach data and be checked, but running cost stays low.</p>
<h3>Warm standby</h3>
<p>A scaled-down copy of the whole stack runs continuously at DR, with continuous block or database replication. On failover it is scaled up and traffic is redirected. Because everything is already running, it can be tested without disruption, which is the pattern&rsquo;s biggest practical advantage.</p>
<h3>Active-passive</h3>
<p>A full-size copy stands ready. With synchronous replication, every write is confirmed at both sites, which gives near-zero data loss but limits the distance between sites to roughly 100 km and adds write latency. Network gateways and load balancers are pre-configured so failover is a decision, not a build.</p>
<h3>Active-active</h3>
<p>Both sites serve users at the same time behind a global load balancer, and the loss of one is close to invisible. It is the most expensive pattern and usually needs application changes, because two sites writing to the same data must avoid conflicts and split-brain. Worth it only for services designed for it from day one.</p>''')

S('choosing', 'Choosing a strategy: a four-question framework', '''
<p>The choice of pattern follows from four questions, asked per tier:</p>
<ol class="wp-steps">
<li><strong>What does an hour of downtime cost?</strong> If nobody can put a number or a consequence on it, the system probably does not need the expensive patterns.</li>
<li><strong>How much recent data can be re-entered?</strong> If staff can re-key the last 30 minutes, asynchronous replication is usually enough and synchronous replication is not needed.</li>
<li><strong>Does a regulator or contract set the number?</strong> Banks, insurers, market intermediaries and many government systems have written continuity requirements. Start from those.</li>
<li><strong>Can the application be changed?</strong> If not, active-active is off the table, and active-passive or warm standby is the realistic ceiling.</li>
</ol>
<p>Most organisations land on the same shape: active-passive or warm standby for a handful of critical systems, pilot light for important business applications, and backup and restore for everything else, with immutable backups behind all three.</p>
''' + table(['Sector', 'Typical tier 1 pattern', 'What drives it'], [
    ['Banking and financial services', 'Active-passive, sometimes three sites', 'Round-the-clock transactions, regulator DR drills, near-zero data loss'],
    ['Government services', 'Warm standby or active-passive', 'Citizen services during emergencies, data residency, audit trail'],
    ['Healthcare', 'Warm standby', 'Clinical systems need fast recovery; records must stay on-premises'],
    ['Manufacturing', 'Pilot light, with warm standby for MES', 'Plant continuity at balanced cost; plants often keep running locally'],
    ['AI and GPU platforms', 'Backup of data and checkpoints; warm standby for inference', 'GPUs are too costly to duplicate idle; training restarts from checkpoints'],
]))

S('architecture', 'Reference architecture', '''
<p>The diagram shows the tiered design most organisations end up with. Users reach applications through a global DNS or load balancer with short time-to-live values, so traffic can be moved in minutes. Tier 1 runs warm at the DR site, tier 2 is a pilot light, and tier 3 relies on backups.</p>
[[DIAGRAM]]
<p class="wp-caption">Numbered flows: (1) database changes replicate asynchronously to the DR replica, (2) storage is mirrored on a schedule, with a shorter interval for tier 1 volumes, (3) immutable backups are written nightly to a vault that production credentials cannot reach. Restores from the vault are tested regularly in an isolated area.</p>
<h3>What must exist at the DR site besides data</h3>
''' + ul(['Identity: a directory controller and the same roles and groups, so people can log in.',
          'Network: firewall rules, VPN and partner links, IP plan or DNS changes, all kept as code.',
          'Certificates and secrets: renewed at both sites on the same schedule.',
          'Licences: licence servers and any standby licence entitlements, checked against contracts.',
          'Monitoring and logging: so the team can see what is happening after failover.',
          'Runbooks and contact lists: stored somewhere reachable when the primary site is not.']) + callout('On OpenStack and Ceph:', 'site-level DR is built from Ceph RBD mirroring between clusters (snapshot-based for most volumes, journal-based for the few that need a lower RPO), images published to both sites from one pipeline, projects and networks recreated from Heat or Terraform, and Ansible playbooks that promote volumes and start instances in dependency order. High availability inside one site, such as live migration or instance HA, is not DR.'))

S('sizing', 'Sizing and cost', '''
<div class="keep"><h3>Replication bandwidth</h3>
<p>Bandwidth is driven by how much data changes, not by how much data exists. A useful first estimate:</p>
<div class="wp-formula">Required bandwidth (Mbps) = daily change (GB) &times; 8,000 &divide; seconds in the busy window &times; 1.3 headroom</div></div>
<p>For example, 400 GB of changes a day, most of it in a 10-hour business window, needs about 400 &times; 8,000 &divide; 36,000 &times; 1.3, or roughly 115 Mbps of sustained replication bandwidth. Measure change rates from storage or database logs over at least two weeks, including month end, before buying links. Provision two links from different providers.</p>
<h3>Storage</h3>
''' + ul(['DR replica: at least one full copy of protected data, plus room for snapshots at the DR site.',
          'Backups: retention multiplied by daily change, after deduplication. A 30-day retention commonly needs 1.5 to 3 times the protected data.',
          'Seeding: tens of terabytes can take weeks over a WAN link. Shipping encrypted disks for the first copy is often faster.']) + '''
<h3>A worked example</h3>
<p>Production has 40 virtual machines and 30 TB of data. After business impact analysis, 8 VMs are tier 1, 20 are tier 2 and 12 are tier 3.</p>
''' + table(['', 'Option A: everything active-passive', 'Option B: protected by tier'], [
    ['What runs at DR every day', 'All 40 VMs at full size', 'About 7 VM-equivalents: tier 1 at half size, tier 2 databases small'],
    ['Tier 1 recovery', 'Minutes', 'Same: minutes'],
    ['Tier 2 recovery', 'Minutes', 'A few hours'],
    ['Tier 3 recovery', 'Minutes', 'One to two days from backup'],
    ['DR running cost vs production', 'About 80 to 100%', 'About 35 to 50%'],
]) + '''
<p>Where the DR site is on-premises or in colocation, hardware for tiers 1 and 2 must still be ready, because servers cannot be bought on the day; the saving is in power, licences and tier 3 capacity. In cloud DR, full capacity is created only on drill or disaster day, which is where tiering saves the most.</p>
<h3>Costs that are often missed</h3>
''' + ul(['Failback: moving data back after a cloud failover can carry large egress charges.',
          'Licences: some vendors charge in full for a standby database or hypervisor. Read the contract.',
          'Drills: a full failover test takes several people most of a day, every year.',
          'Keeping DR current: patching templates, renewing certificates and updating firewall rules at DR is ongoing work.']))

S('ransomware', 'Ransomware changes the design', '''
<p>Classic DR assumes the primary site is lost but the data is good. Ransomware breaks that assumption: the data itself is the problem, and attackers deliberately go after backups and DR systems first. Replication makes it worse, because encrypted files replicate to the DR site within minutes.</p>
<p>A design that survives ransomware adds four things:</p>
''' + table(['Control', 'Why it matters'], [
    ['Immutable backups', 'Object lock or write-once storage, so backups cannot be changed or deleted for the retention period, even by an administrator.'],
    ['Separate credentials and management', 'Backup and DR systems use their own accounts and multi-factor authentication, not the production directory.'],
    ['An isolated copy', 'At least one copy in a vault that opens only for scheduled replication windows, or offline media.'],
    ['Clean restore points and a clean room', 'Backups are scanned, and restores happen first into an isolated environment where identity and critical apps are rebuilt and checked before reconnecting.'],
]) + callout('Plan the order:', 'after ransomware, identity usually has to be rebuilt first, then core infrastructure services, then tier 1 applications. Write that order into the runbook and rehearse it.', 'warn'))

S('testing', 'Testing: turning a plan into evidence', '''
<p>DR that has never been tested is a guess. Most problems appear the first time someone actually fails over: a missing firewall rule, an expired certificate, a licence server that only exists in production. Testing finds these while there is no real disaster.</p>
''' + table(['Test', 'What happens', 'Suggested frequency'], [
    ['Tabletop walk-through', 'The team reads the runbook step by step and checks every step, name and phone number.', 'Every quarter'],
    ['Restore test', 'Restore one server or database from backup and confirm it works.', 'Every month, rotating systems'],
    ['Isolated failover', 'Bring a tier up at DR on an isolated network, without touching production users.', 'Twice a year for each tier'],
    ['Full failover and failback', 'Move real users to DR for an agreed window, then move back.', 'Once a year for tier 1, or as a regulator requires'],
]) + '''
<h3>On drill day</h3>
''' + ul(['Before: freeze changes, confirm replication lag is within RPO, tell users and the helpdesk, and write down what success means.',
          'During: time every step, record every manual fix however small, have the application owner test, and agree a hard stop for rolling back.',
          'After: report measured RPO and RTO against targets, turn every issue into a fix with an owner and a date, update the runbook that week, and book the next drill.']) + '''
<h3>Keeping DR working between drills</h3>
''' + ul(['Alert on replication lag. Lag that quietly grows past the RPO is the most common silent failure.',
          'Add &ldquo;and at DR?&rdquo; to every change: new applications, firewall changes, certificate renewals.',
          'Patch DR on the same schedule as production, and upgrade both sites together.',
          'Review tiers once a year. Last year&rsquo;s tier 3 system may now be critical.']))

S('roadmap', 'A practical roadmap', '''
<p>For a mid-sized environment, a DR programme typically runs in four stages. Procurement of links, hardware and DR site space usually sets the pace.</p>
''' + table(['Stage', 'Typical duration', 'Outcome'], [
    ['1. Assess', '3 to 6 weeks', 'Application inventory, dependencies, business impact analysis, agreed tiers and targets, gap report.'],
    ['2. Design', '3 to 4 weeks', 'Pattern per tier, reference architecture, sizing, bandwidth, cost model, runbook outline.'],
    ['3. Build', '6 to 16 weeks', 'DR site, links, replication, backup vault, automation, monitoring of replication lag.'],
    ['4. Prove', '2 to 4 weeks, then ongoing', 'First isolated failover per tier, first full drill for tier 1, evidence pack, test calendar.'],
]))

S('mistakes', 'Ten common mistakes', '<ol class="wp-steps">' + ''.join('<li>' + m + '</li>' for m in [
    '<strong>One RPO and RTO for the whole company.</strong> Either too expensive or not protective enough.',
    '<strong>Choosing a product before agreeing targets.</strong> The product then defines the targets.',
    '<strong>Treating replication as backup.</strong> It copies ransomware and mistakes just as fast.',
    '<strong>DR site sharing risks with production.</strong> Same building, power feed, flood zone or admin accounts.',
    '<strong>Copying data but not configuration.</strong> Networks, certificates and licences rebuilt by hand under pressure.',
    '<strong>No named decision-maker.</strong> Hours lost before anyone declares the disaster.',
    '<strong>Long DNS time-to-live values.</strong> Failover is done but users keep going to the dead site for hours.',
    '<strong>Never testing failback.</strong> Getting back is often the harder half.',
    '<strong>Not monitoring replication lag.</strong> The RPO is silently missed for weeks.',
    '<strong>Letting the two sites drift.</strong> Different software versions cause surprises on failover day.']) + '</ol>')

CHECKLIST = [
  ('Governance', ['A named owner for DR and a named person who can declare a disaster',
                  'Agreed criteria for declaring a disaster',
                  'RPO and RTO agreed and signed off per tier by business owners',
                  'Regulatory and contractual DR requirements listed',
                  'DR included in change management (&ldquo;and at DR?&rdquo;)']),
  ('Applications and data', ['Complete application inventory with owners',
                  'Dependencies mapped, including directory, DNS, licences and integrations',
                  'Every application assigned to a tier',
                  'Data classification and residency constraints known for each tier',
                  'Start-up order documented for every tier 1 and tier 2 service']),
  ('Infrastructure', ['DR site does not share building, power feed or flood zone with production',
                  'Two network links from different providers between sites',
                  'Replication method chosen per tier and matched to RPO',
                  'Replication bandwidth sized from measured change rates',
                  'Identity, DNS and certificates available at the DR site',
                  'Firewall rules and network configuration kept as code for both sites',
                  'Licences for standby systems checked against contracts',
                  'Monitoring and logging available at DR']),
  ('Backup and ransomware', ['Immutable backups with defined retention',
                  'Backup and DR systems use separate admin accounts with multi-factor authentication',
                  'At least one isolated or offline copy',
                  'Backups scanned and clean restore points recorded',
                  'Clean-room procedure for rebuilding identity and tier 1 applications',
                  'Restore tested from the isolated copy at least twice a year']),
  ('Runbooks and people', ['Runbook per tier, stored where it is reachable without the primary site',
                  'Contact list with alternates, checked every quarter',
                  'Communication plan for staff, customers and regulators',
                  'Failback procedure written and rehearsed',
                  'Short DNS time-to-live values on services that fail over']),
  ('Testing and evidence', ['Quarterly tabletop walk-through',
                  'Monthly restore test on rotating systems',
                  'Isolated failover for each tier twice a year',
                  'Annual full failover and failback for tier 1',
                  'Measured RPO and RTO reported against targets after every drill',
                  'Issues from drills tracked to closure with owners and dates']),
  ('Operations', ['Alert when replication lag exceeds the RPO',
                  'DR patched on the same schedule as production',
                  'Both sites upgraded together',
                  'Tiers reviewed once a year',
                  'DR costs reviewed once a year']),
]
n_items = sum(len(i) for _, i in CHECKLIST)
S('checklist', 'DR readiness checklist (' + str(n_items) + ' points)',
  '<p>Use this list to score your current position. Anything you cannot tick with evidence is a gap worth closing.</p><div class="wp-check">' +
  ''.join('<div class="wp-check-group"><h3>' + g + '</h3><ul>' + ''.join('<li>' + i + '</li>' for i in items) + '</ul></div>' for g, items in CHECKLIST) + '</div>')

S('glossary', 'Glossary', table(['Term', 'Meaning'], [
    ['RPO', 'Recovery Point Objective: maximum acceptable data loss, measured in time.'],
    ['RTO', 'Recovery Time Objective: maximum acceptable downtime for a service.'],
    ['Synchronous replication', 'Each write is confirmed at both sites before it completes. Near-zero data loss, distance-limited.'],
    ['Asynchronous replication', 'Writes are copied to the second site shortly after. Small possible data loss, any distance.'],
    ['Failover / failback', 'Moving service to the DR site, and later moving it back.'],
    ['Immutable backup', 'A backup that cannot be changed or deleted for its retention period.'],
    ['Split-brain', 'Both sites believe they are primary and accept writes, causing conflicting data.'],
    ['Tabletop exercise', 'A walk-through of the runbook without touching systems.'],
]))
