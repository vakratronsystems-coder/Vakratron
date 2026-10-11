"""Three DR guides: HA vs FT vs DR, DR in the public cloud, keeping DR the same as
production (configuration drift).  Run from tools/content-gen/dr:  python3 dr_guides2.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'deployments'))
from tpl import *
from diagram import render

N = lambda x, y, w, title, sub='', icon='server', tone='blue', **k: dict(x=x, y=y, w=w, title=title, sub=sub, icon=icon, tone=tone, **k)
T = lambda rows: ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)

def fig(d, label, caption):
    return ('<figure class="vk-fig vk-refarch vk-dgfig"><span class="vk-scroll-hint">Scroll sideways to see the whole diagram &rarr;</span>'
            '<div class="vk-refarch-scroll">' + render(d, label) + '</div><figcaption>' + caption + '</figcaption></figure>')

def related(*cards):
    return ('''
        <div class="vk-sec"><div class="vk-wrap">
            <h2>Related guides</h2>
            <div class="vk-grid" style="margin-top:18px">''' +
            ''.join(f'<a class="vk-card" href="{h}"><h3>{t}</h3><p>{p}</p><span class="vk-go">Read the guide &rarr;</span></a>' for h, t, p in cards) +
            '''</div>
        </div></div>''')

R_LAYER = ('/solutions/dc-dr/dr-by-layer', 'DR layer by layer', 'Traffic, network, databases, storage and messaging, with on-premises and cloud equivalents.')
R_PATTERN = ('/solutions/dc-dr/strategy-selection', 'Choosing a DR pattern', 'Backup and restore, pilot light, warm standby, active-passive and active-active.')
R_COST = ('/solutions/dc-dr/cost-comparison', 'What DR really costs', 'Where the money goes, with planning ranges and a worked example.')
R_TEST = ('/solutions/dc-dr/best-practices', 'Testing DR', 'Drill types, how often to run them, and a drill-day checklist.')
R_HA = ('/solutions/dc-dr/ha-ft-dr', 'HA, fault tolerance and DR', 'What each one protects against, and why you usually need all three.')
R_CLOUD = ('/solutions/dc-dr/cloud-dr', 'DR in the public cloud', 'Using a cloud region as your DR site: patterns, cost and the catches.')
R_DRIFT = ('/solutions/dc-dr/config-drift', 'Keeping DR the same as production', 'How DR sites drift away from production, and how to catch it.')


# ------------------------------------------------------------------ 1. HA vs FT vs DR
D_HA = dict(w=1120, h=330,
  zones=[
    dict(x=20, y=20, w=350, h=290, title='High availability: one site', kind='dc'),
    dict(x=385, y=20, w=350, h=290, title='Fault tolerance: no interruption', kind='ai'),
    dict(x=750, y=20, w=350, h=290, title='Disaster recovery: second site', kind='dr'),
  ],
  nodes={
    'lb': N(105, 60, 180, 'Load balancer', 'health checks', 'lb', 'blue'),
    'a1': N(35, 150, 150, 'App server A', 'rack 1', 'server', 'blue'),
    'a2': N(205, 150, 150, 'App server B', 'rack 2', 'server', 'blue'),
    'd1': N(35, 235, 150, 'Database', 'primary', 'storage', 'green'),
    'd2': N(205, 235, 150, 'Database', 'replica', 'storage', 'green'),
    'fa': N(415, 60, 290, 'Primary VM', 'runs the workload', 'vm', 'violet'),
    'fb': N(415, 150, 290, 'Shadow VM', 'repeats every step, other host', 'vm', 'violet'),
    'fs': N(415, 235, 290, 'Shared storage', 'both see the same disks', 'storage', 'green'),
    'p': N(780, 60, 290, 'Primary site', 'your main data centre', 'building', 'blue'),
    'r': N(780, 150, 290, 'DR site, far away', 'standby copy, different risk zone', 'building', 'violet'),
    'b': N(780, 235, 290, 'Offline backups', 'point in time, immutable', 'archive', 'green'),
  },
  flows=[
    dict(a='lb', b='a1', kind='traffic', n=1),
    dict(a='lb', b='a2', kind='traffic'),
    dict(a='d1', b='d2', kind='sync', label='sync'),
    dict(a='fa', b='fb', kind='sync', label='lockstep', n=2),
    dict(a='p', b='r', kind='data', label='replication', n=3),
  ])

CAP_HA = ('1. High availability spreads one service across racks or zones in the same site, so a single failed server or rack is absorbed in seconds to minutes. '
          '2. Fault tolerance runs a mirrored copy in lockstep, so a failed host causes no interruption at all, at a high cost per workload. '
          '3. Disaster recovery keeps a copy in a second site far enough away not to share the same fire, flood or power failure, plus backups that survive data corruption.')

body_ha = f'''
        <div class="vk-wrap vk-hero">
            {crumb(("Home","/"),("Disaster Recovery","/portfolio/dr-solutions"),("HA, fault tolerance and DR",None))}
            <span class="vk-eyebrow">DR guide</span>
            <h1>High availability, fault tolerance and disaster recovery</h1>
            <p class="vk-lead">The three terms are often used as if they mean the same thing. They do not. Each one protects against a different kind of failure, at a different cost, and a design that has only one of them has a gap. This guide explains the difference in plain terms and shows where each belongs.</p>
        </div>

        <div class="vk-sec"><div class="vk-wrap">
            <h2>The three, side by side</h2>
            {fig(D_HA, 'High availability, fault tolerance and disaster recovery', CAP_HA)}
        </div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <h2>How they compare</h2>
            <div class="vk-table-wrap"><table>
                <thead><tr><th></th><th>High availability (HA)</th><th>Fault tolerance (FT)</th><th>Disaster recovery (DR)</th></tr></thead>
                <tbody>{T([
                    ['Protects against', 'A failed server, disk, rack or availability zone', 'A failed host, with zero interruption', 'Loss of a whole site: fire, flood, long power failure, ransomware, regional outage'],
                    ['Typical downtime', 'Seconds to a few minutes', 'None', 'Minutes to hours, set by the RTO'],
                    ['Typical data loss', 'None', 'None', 'Zero to a few minutes, set by the RPO'],
                    ['Where the copy lives', 'Same site, different rack or zone', 'Same site, different host', 'Different site, far enough away to avoid the same event'],
                    ['Cost', 'Moderate: roughly double the critical components', 'High: every workload runs twice, often with licence limits', 'Varies widely with the pattern, from backups only to a full second site'],
                    ['Typical examples', 'Clustered databases, load-balanced app servers, dual power and network', 'VMware vSphere Fault Tolerance, lockstep hardware, some telecom and control systems', 'Database replication to a second site, cloud DR, backups held off site'],
                ])}</tbody>
            </table></div>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap"><div class="vk-prose">
            <h2>Why you usually need all three</h2>
            <p>Most outages are small: a disk, a server, a switch. High availability handles those without anyone noticing, and that is where it earns its cost. But HA lives inside one site. If the site loses power for a day, every redundant server in it goes down together.</p>
            <p>Disaster recovery covers the large, rare event. It is slower and involves a decision to fail over, but it is the only thing that helps when the whole site is gone.</p>
            <p>Fault tolerance is the narrow case: a small number of workloads where even a few seconds of interruption is unacceptable. Using it everywhere is expensive and rarely needed.</p>
            <p>And none of the three replaces backups. Replication copies corruption and ransomware encryption to the other side within seconds. A backup from yesterday, held where an attacker cannot delete it, is what lets you go back to before the problem started.</p>
        </div></div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <h2>Four common mistakes</h2>
            <div class="vk-grid" style="margin-top:18px">
                <div class="vk-card"><h3>Calling HA &ldquo;our DR&rdquo;</h3><p class="vk-muted">Two clustered servers in the same room are high availability. They share the same building, power and network, so one event takes both down.</p></div>
                <div class="vk-card"><h3>Treating replication as backup</h3><p class="vk-muted">Replication copies mistakes as faithfully as data. A deleted table or encrypted volume reaches the DR site almost at once.</p></div>
                <div class="vk-card"><h3>Fault tolerance for everything</h3><p class="vk-muted">Running every workload twice in lockstep doubles cost for systems that could tolerate a minute of interruption. Keep it for the few that cannot.</p></div>
                <div class="vk-card"><h3>A DR site too close</h3><p class="vk-muted">A DR site across the road shares the same flood plain, substation and fibre routes. Distance should match the risks you are protecting against.</p></div>
            </div>
        </div></div>
{related(R_LAYER, R_PATTERN, R_TEST)}
{CTA}'''


# ------------------------------------------------------------------ 2. DR in the public cloud
D_CLOUD = dict(w=1120, h=500,
  zones=[
    dict(x=20, y=20, w=430, h=455, title='Your data centre (primary)', kind='dc'),
    dict(x=670, y=20, w=430, h=455, title='Cloud region in India (DR)', kind='cloud'),
  ],
  nodes={
    'pv': N(45, 60, 380, 'Application VMs', 'running, serving users', 'server', 'blue'),
    'pa': N(45, 145, 380, 'Replication agent', 'block-level, continuous', 'cog', 'blue'),
    'pd': N(45, 230, 380, 'Databases', 'primary, takes all writes', 'storage', 'green'),
    'pb': N(45, 315, 380, 'Backups', 'daily, kept on site', 'archive', 'green'),
    'pn': N(45, 400, 380, 'Network edge', 'firewalls, WAN, internet', 'firewall', 'blue'),
    'cc': N(695, 60, 380, 'Recovery servers', 'not running until a drill or disaster', 'server', 'amber', state='off', tag='OFF'),
    'cs': N(695, 145, 380, 'Staging storage', 'low-cost disks, always on', 'storage', 'amber'),
    'cd': N(695, 230, 380, 'Database replica', 'small instance, always on', 'storage', 'amber'),
    'cb': N(695, 315, 380, 'Backup copy', 'object storage, locked', 'archive', 'amber'),
    'cn': N(695, 400, 380, 'Cloud network', 'pre-built, same rules as primary', 'firewall', 'amber'),
  },
  flows=[
    dict(a='pa', b='cs', kind='data', label='continuous', n=1),
    dict(a='pd', b='cd', kind='data', label='log shipping', n=2),
    dict(a='pb', b='cb', kind='batch', label='daily copy', n=3),
    dict(a='pn', b='cn', kind='traffic', label='VPN or private link'),
    dict(a='cs', b='cc', kind='control', n=4),
  ])

CAP_CLOUD = ('1. A replication agent copies each server&rsquo;s disks continuously to low-cost staging storage in the cloud region. '
             '2. Databases ship their logs to a small replica that is always running, so the RPO stays in minutes. '
             '3. Backups are copied daily to object storage with a lock, so they survive ransomware at the primary site. '
             '4. Recovery servers do not run day to day. At a drill or a disaster they are launched from the staging storage, which is why the standing cost is low.')

COST_ROWS = [
    ['Staging storage for replicated disks', '20 TB &times; &#8377;5&ndash;8 per GB per month', '&#8377;1.0&ndash;1.6 lakh'],
    ['DR tooling, per protected server', '40 servers &times; &#8377;1,500&ndash;2,500', '&#8377;0.6&ndash;1.0 lakh'],
    ['Small database replica, always on', 'One modest instance with storage', '&#8377;0.4&ndash;0.8 lakh'],
    ['Backup copy in locked object storage', '30 TB with retention &times; &#8377;1.5&ndash;2.5 per GB', '&#8377;0.45&ndash;0.75 lakh'],
    ['Connectivity', 'Site-to-site VPN or a small private link', '&#8377;0.3&ndash;0.8 lakh'],
    ['<strong>Standing cost per month</strong>', 'Sum of the above', '<strong>about &#8377;3&ndash;5 lakh</strong>'],
    ['Compute during a drill or disaster', '40 servers &times; &#8377;300&ndash;600 per day', '&#8377;12,000&ndash;24,000 per day'],
    ['Failback data transfer', '20 TB &times; &#8377;7&ndash;9 per GB out of the cloud', '&#8377;1.4&ndash;1.8 lakh, once'],
]

body_cloud = f'''
        <div class="vk-wrap vk-hero">
            {crumb(("Home","/"),("Disaster Recovery","/portfolio/dr-solutions"),("DR in the public cloud",None))}
            <span class="vk-eyebrow">DR guide</span>
            <h1>Disaster recovery in the public cloud</h1>
            <p class="vk-lead">Building a second data centre just for DR means buying hardware that sits idle most of the year. A public cloud region can act as the DR site instead: you pay to keep data copied there all the time, and pay for servers only when you test or actually fail over. For many organisations that changes DR from a capital project into a modest monthly cost. It also brings its own catches, which this guide covers.</p>
        </div>

        <div class="vk-sec"><div class="vk-wrap">
            <h2>Three ways to use the cloud for DR</h2>
            <div class="vk-table-wrap"><table>
                <thead><tr><th>Setup</th><th>What it means</th><th>Good for</th><th>Watch out for</th></tr></thead>
                <tbody>{T([
                    ['On premises to cloud', 'Production stays in your data centre; a cloud region is the DR site', 'Organisations without a second data centre, or replacing an ageing one', 'Bandwidth for replication, licences at DR, and the cost of bringing data back'],
                    ['Cloud region to cloud region', 'Production runs in one cloud region, DR in another region of the same provider', 'Workloads already in the cloud', 'Both regions share the same provider, account and identity system'],
                    ['Cloud to a different provider or back on premises', 'DR outside the provider that runs production', 'Regulated sectors worried about dependence on one provider', 'Two platforms to run and test, and services that do not translate one to one'],
                ])}</tbody>
            </table></div>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <h2>The most common design: on premises to a cloud region</h2>
            {fig(D_CLOUD, 'On-premises primary with DR in a cloud region', CAP_CLOUD)}
        </div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <h2>A worked example</h2>
            <p class="vk-prose">Forty servers, 20 TB of data, an RPO of 15 minutes and an RTO of four hours, with DR in an Indian cloud region. These are planning ranges to show where the money goes, not a quote. Prices vary by provider, region, commitment and discounts.</p>
            <div class="vk-table-wrap"><table>
                <thead><tr><th>Item</th><th>Basis</th><th>Planning figure</th></tr></thead>
                <tbody>{T(COST_ROWS)}</tbody>
            </table></div>
            <p class="vk-small vk-muted" style="margin-top:14px">For comparison, a warm-standby second data centre for the same estate typically needs &#8377;1.5&ndash;3 crore of hardware up front, plus &#8377;3&ndash;6 lakh a month for colocation, power and connectivity. Cloud DR is usually cheaper for this size of estate. It becomes less attractive when DR servers must run all the time, or when large volumes of data move out of the cloud often.</p>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <h2>The catches</h2>
            <div class="vk-grid" style="margin-top:18px">
                <div class="vk-card"><h3>Where the data may live</h3><p class="vk-muted">Some data must stay in India, for example payment data under RBI rules. Choose an Indian region (Mumbai, Hyderabad, Pune, Chennai or Delhi, depending on the provider) and check your sector regulator&rsquo;s rules before you start.</p></div>
                <div class="vk-card"><h3>Capacity on the day</h3><p class="vk-muted">In a regional event, many customers fail over at once. For critical tiers, reserve capacity or keep a small footprint always running rather than assuming servers will be available.</p></div>
                <div class="vk-card"><h3>Licences at DR</h3><p class="vk-muted">Oracle, Microsoft SQL Server and Windows licences have specific rules for DR and for running in a public cloud. Check them during design, not after the first drill.</p></div>
                <div class="vk-card"><h3>Getting data back</h3><p class="vk-muted">Data leaving the cloud is charged per GB. After a real failover, bringing tens of terabytes back to the primary site is a real cost and takes time. Plan failback as carefully as failover.</p></div>
                <div class="vk-card"><h3>Bandwidth for replication</h3><p class="vk-muted">The link has to carry your daily change rate within the RPO. Measure the real change rate first; a guess here is the most common reason a cloud DR design misses its RPO.</p></div>
                <div class="vk-card"><h3>One account, one key</h3><p class="vk-muted">If an attacker gets into the cloud account, both the DR servers and the backups are at risk. Keep backups in a separate account with locked retention and separate administrator credentials.</p></div>
            </div>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <h2>Common building blocks by provider</h2>
            <div class="vk-table-wrap"><table>
                <thead><tr><th>Need</th><th>AWS</th><th>Azure</th><th>Oracle Cloud</th></tr></thead>
                <tbody>{T([
                    ['Server replication and recovery', 'Elastic Disaster Recovery', 'Azure Site Recovery', 'Full Stack Disaster Recovery'],
                    ['Locked backups', 'AWS Backup with Vault Lock', 'Azure Backup with immutable vaults', 'Object Storage retention rules'],
                    ['Private connectivity', 'Direct Connect, Site-to-Site VPN', 'ExpressRoute, VPN Gateway', 'FastConnect, Site-to-Site VPN'],
                    ['Indian regions', 'Mumbai, Hyderabad', 'Pune, Chennai, Mumbai', 'Mumbai, Hyderabad'],
                ])}</tbody>
            </table></div>
            <p class="vk-small vk-muted" style="margin-top:14px">Third-party tools such as Veeam and Zerto also replicate on-premises servers into these clouds, and are often the better choice when you want the same tool across several platforms.</p>
        </div></div>
{related(R_LAYER, R_COST, R_HA)}
{CTA}'''


# ------------------------------------------------------------------ 3. Config drift
D_DRIFT = dict(w=1120, h=400,
  zones=[
    dict(x=20, y=20, w=320, h=360, title='Single source of truth', kind='ent'),
    dict(x=400, y=20, w=320, h=160, title='Production', kind='dc'),
    dict(x=400, y=220, w=320, h=160, title='DR site', kind='dr'),
    dict(x=780, y=20, w=320, h=360, title='Checks, outside both sites', kind='sec'),
  ],
  nodes={
    'git': N(35, 60, 290, 'Code repository', 'IaC, images, firewall rules', 'git', 'green'),
    'pipe': N(35, 175, 290, 'Deployment pipeline', 'applies each change to both sites', 'flow', 'green'),
    'chg': N(35, 290, 290, 'Change approval', 'asks: and at DR?', 'check', 'green'),
    'ps': N(415, 60, 290, 'Production', 'servers, network, databases', 'server', 'blue'),
    'ds': N(415, 260, 290, 'DR site', 'should match production', 'server', 'violet'),
    'scan': N(795, 60, 290, 'Drift scanner', 'compares both sites weekly', 'search', 'pink'),
    'rep': N(795, 175, 290, 'Drift report', 'each gap with an owner and date', 'doc', 'pink'),
    'kpi': N(795, 290, 290, 'DR readiness figures', 'lag, open drift, last drill', 'chart', 'pink'),
  },
  flows=[
    dict(a='git', b='pipe', kind='control', n=1),
    dict(a='chg', b='pipe', kind='control'),
    dict(a='pipe', b='ps', kind='control', n=2, label='apply', lpos=(378, 200)),
    dict(a='pipe', b='ds', kind='control'),
    dict(a='ps', b='scan', kind='mgmt', n=3),
    dict(a='ds', b='scan', kind='mgmt'),
    dict(a='scan', b='rep', kind='alert', n=4),
    dict(a='rep', b='kpi', kind='mgmt', n=5),
  ])

CAP_DRIFT = ('1. Infrastructure, images and firewall rules are defined as code in one repository. '
             '2. A pipeline applies every approved change to production and DR together, so the two cannot diverge through normal work. '
             '3. A scanner outside both sites reads the actual configuration of each site on a schedule. '
             '4. Any difference becomes a report item with an owner and a date. '
             '5. Open drift, replication lag and the date of the last successful drill are reported as DR readiness figures.')

body_drift = f'''
        <div class="vk-wrap vk-hero">
            {crumb(("Home","/"),("Disaster Recovery","/portfolio/dr-solutions"),("Keeping DR the same as production",None))}
            <span class="vk-eyebrow">DR guide</span>
            <h1>Keeping DR the same as production</h1>
            <p class="vk-lead">A DR site that matched production on the day it was built starts to drift within weeks. A firewall rule is added in production only. A server is patched in one place. A new application goes live without a DR copy. None of these shows up on a replication dashboard, and each one becomes a failure on the day you need DR. This guide covers where drift comes from and how to catch it before a drill or a disaster does.</p>
        </div>

        <div class="vk-sec"><div class="vk-wrap">
            <h2>How it fits together</h2>
            {fig(D_DRIFT, 'Keeping DR the same as production', CAP_DRIFT)}
        </div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <h2>What drifts, and how to catch it</h2>
            <div class="vk-table-wrap"><table>
                <thead><tr><th>What drifts</th><th>How it usually happens</th><th>How to catch it</th></tr></thead>
                <tbody>{T([
                    ['Firewall and network rules', 'An urgent rule is added in production during an incident and never copied', 'Compare rule sets between sites weekly; keep rules in code'],
                    ['Server and OS versions', 'Patching runs in production first and DR is forgotten', 'Patch both sites in the same change; report version differences'],
                    ['Database parameters and versions', 'Tuning or an upgrade is done on the primary only', 'Compare parameters and versions between primary and standby'],
                    ['New applications', 'A new system goes live with no DR tier assigned', 'Make a DR tier a go-live requirement; list systems with no DR copy'],
                    ['Certificates and secrets', 'A certificate is renewed for production hostnames only', 'Track expiry dates for both sites in one place'],
                    ['Capacity', 'Production grows; DR is still sized for last year', 'Compare CPU, memory and storage between sites each quarter'],
                    ['Access and identities', 'New administrators or service accounts exist only in production', 'Compare privileged accounts and groups between sites'],
                ])}</tbody>
            </table></div>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap"><div class="vk-prose">
            <h2>Four habits that prevent most drift</h2>
            <ol class="vk-steps">
                <li><strong>Build both sites from the same code.</strong> Terraform, Ansible, Heat or cloud templates mean a change is applied to both sites or to neither. Golden images do the same for servers.</li>
                <li><strong>Add one question to change approval.</strong> &ldquo;And at DR?&rdquo; on every change form catches most drift at the source, at almost no cost.</li>
                <li><strong>Compare automatically, on a schedule.</strong> A weekly comparison of rules, versions, parameters and accounts, run from outside both sites, finds what slipped through.</li>
                <li><strong>Report DR readiness like any other service measure.</strong> Three numbers are enough: replication lag against the RPO, open drift items, and days since the last successful drill.</li>
            </ol>
        </div></div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <h2>A monthly DR readiness check</h2>
            <div class="vk-grid" style="margin-top:18px">
                <div class="vk-card"><h3>Replication</h3><ul><li>Lag within RPO for every tier</li><li>No paused or failed replication jobs</li><li>Backup copies completed and locked</li></ul></div>
                <div class="vk-card"><h3>Configuration</h3><ul><li>No open drift items older than 30 days</li><li>Every production system has a DR tier</li><li>Certificates valid at both sites</li></ul></div>
                <div class="vk-card"><h3>People and process</h3><ul><li>Runbooks updated after the last change</li><li>Contact list checked</li><li>Next drill booked</li></ul></div>
            </div>
        </div></div>
{related(R_LAYER, R_TEST, R_CLOUD)}
{CTA}'''


if __name__ == '__main__':
    page('solutions/dc-dr/ha-ft-dr.html',
         'High Availability vs Fault Tolerance vs Disaster Recovery | Vakratron Systems',
         'The difference between high availability, fault tolerance and disaster recovery: what each protects against, downtime, data loss, cost, and why most organisations need all three.',
         body_ha)
    page('solutions/dc-dr/cloud-dr.html',
         'Disaster Recovery in the Public Cloud: Patterns, Cost and Catches | Vakratron Systems',
         'Using a public cloud region in India as your DR site: the three setups, a worked cost example in rupees, data residency, licences, capacity and failback.',
         body_cloud)
    page('solutions/dc-dr/config-drift.html',
         'Keeping DR the Same as Production: Configuration Drift | Vakratron Systems',
         'How DR sites drift away from production, what drifts most often, how to catch it with infrastructure as code and automated comparison, and a monthly DR readiness check.',
         body_drift)
