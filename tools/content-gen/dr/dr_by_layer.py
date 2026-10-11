"""DR guide: disaster recovery layer by layer (traffic, network, compute, database,
storage, messaging, operations), with on-prem and cloud equivalents.
Run from tools/content-gen/dr:  python3 dr_by_layer.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'deployments'))
from tpl import *
from diagram import render

N = lambda x, y, w, title, sub='', icon='server', tone='blue', **k: dict(x=x, y=y, w=w, title=title, sub=sub, icon=icon, tone=tone, **k)

DIAGRAM = dict(w=1120, h=765,
  zones=[
    dict(x=20, y=20, w=1080, h=100, title='Users and traffic steering', kind='ext'),
    dict(x=20, y=150, w=440, h=455, title='Primary site', kind='dc'),
    dict(x=660, y=150, w=440, h=455, title='DR site or cloud region', kind='dr'),
    dict(x=20, y=645, w=1080, h=100, title='Operations, outside both sites', kind='sec'),
  ],
  nodes={
    'users': N(60, 52, 220, 'Users and partners', 'branches, web, mobile, APIs', 'users', 'slate'),
    'gslb': N(440, 52, 280, 'Global traffic manager', 'DNS or GSLB with health checks', 'lb', 'pink'),
    'pnet': N(45, 190, 390, 'Network edge', 'firewalls, load balancers, WAN links', 'firewall', 'blue'),
    'papp': N(45, 275, 390, 'Application servers', 'VMs or containers, active', 'server', 'blue'),
    'pdb': N(45, 360, 390, 'Database', 'primary, takes all writes', 'storage', 'green'),
    'pst': N(45, 445, 390, 'Storage and backups', 'block, file, object, backup copies', 'archive', 'green'),
    'pq': N(45, 530, 390, 'Cache and messaging', 'Redis, Kafka, MQ', 'queue', 'blue'),
    'dnet': N(685, 190, 390, 'Network edge', 'same rules, pre-built and tested', 'firewall', 'violet'),
    'dapp': N(685, 275, 390, 'Application servers', 'warm, or built from images on demand', 'server', 'violet'),
    'ddb': N(685, 360, 390, 'Database standby', 'replica, promoted at failover', 'storage', 'violet'),
    'dst': N(685, 445, 390, 'Storage replica', 'plus an immutable backup copy', 'archive', 'violet'),
    'dq': N(685, 530, 390, 'Cache and messaging', 'mirrored, or rebuilt at failover', 'queue', 'violet'),
    'mon': N(45, 675, 300, 'Monitoring', 'replication lag, health, alerts', 'chart', 'pink'),
    'orch': N(410, 675, 300, 'DR orchestration', 'runbooks, ordered start-up', 'cog', 'pink'),
    'drift': N(775, 675, 300, 'Configuration drift check', 'is DR still the same as prod?', 'check', 'pink'),
  },
  flows=[
    dict(a='users', b='gslb', kind='traffic', n=1),
    dict(a='gslb', b='pnet', kind='traffic', sa='b', sb='t', via=[(580, 136), (240, 136)], n=2, lpos=(410, 136), label='active'),
    dict(a='gslb', b='dnet', kind='control', sa='b', sb='t', via=[(580, 136), (880, 136)], label='on failover', lpos=(760, 136)),
    dict(a='pnet', b='dnet', kind='traffic', label='DCI + backup VPN'),
    dict(a='papp', b='dapp', kind='batch', label='images, IaC'),
    dict(a='pdb', b='ddb', kind='data', label='log shipping', n=3),
    dict(a='pst', b='dst', kind='data', label='replication', n=4),
    dict(a='pq', b='dq', kind='data', label='mirroring'),
    dict(a='orch', b='dq', kind='control', sa='t', sb=('b', 0), via=[(560, 625), (880, 625)], n=5, lpos=(720, 625), label='start-up order'),
    dict(a='mon', b='pq', kind='mgmt', sa='t', sb='b', n=6, label='lag, health', lpos=(195, 625)),
  ])

CAPTION = ('1. Users reach the service through a global traffic manager that health-checks both sites. '
           '2. In normal running it sends everyone to the primary site; on failover it switches to the DR site. '
           '3. Database changes are shipped continuously to a standby that is promoted at failover. '
           '4. Storage and backups are replicated, with at least one copy that cannot be altered. '
           '5. An orchestration runbook starts the DR layers in the right order, bottom up. '
           '6. Monitoring and drift checks run outside both sites, so they still work when one site is lost.')

T = lambda rows: ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)

LAYERS = [
    ['Traffic steering', 'Send users to the healthy site automatically, or with one decision',
     'GSLB on F5 BIG-IP DNS or Citrix ADC; DNS failover with short TTLs',
     'Route 53 health-check failover; Global Accelerator',
     'Traffic Manager; Front Door',
     'DNS traffic management steering policies'],
    ['Network', 'DR has the same firewall rules, routes and partner connectivity, already in place',
     'Two diverse data-centre interconnects; MPLS or leased line with IPsec VPN backup; BGP',
     'Direct Connect with Site-to-Site VPN backup; Transit Gateway',
     'ExpressRoute with VPN Gateway backup; Virtual WAN',
     'FastConnect with IPsec VPN backup; Dynamic Routing Gateway'],
    ['Compute and applications', 'Servers exist at DR, or can be built from tested images within the RTO',
     'VM replication (vSphere Replication, Zerto, Veeam); OpenStack images with Heat or Terraform',
     'Elastic Disaster Recovery; AMIs with Auto Scaling groups',
     'Azure Site Recovery; VM images with scale sets',
     'Full Stack Disaster Recovery; custom images with instance pools'],
    ['Databases', 'A consistent copy within the RPO, and a tested way to promote it',
     'Oracle Data Guard; SQL Server Always On availability groups; PostgreSQL and MySQL replication',
     'RDS cross-region read replicas; Aurora Global Database; DynamoDB global tables',
     'SQL Database failover groups; SQL Managed Instance failover groups; Cosmos DB multi-region',
     'Autonomous Data Guard across regions; Base Database Data Guard'],
    ['Storage, files and backup', 'Data replicated to DR, plus a backup copy that ransomware cannot delete',
     'Array replication; Ceph RBD mirroring; backup copies to a second site and to immutable storage',
     'S3 Cross-Region Replication; AWS Backup cross-region copy with Vault Lock',
     'Geo-redundant storage; Azure Backup cross-region restore with immutable vaults',
     'Object Storage replication; block volume cross-region replication'],
    ['Cache and messaging', 'Queues and topics exist at DR; decide which in-flight messages may be lost',
     'Redis replicas; Kafka MirrorMaker 2; IBM MQ or RabbitMQ federation',
     'ElastiCache Global Datastore; MSK Replicator; SQS and SNS set up per region',
     'Azure Cache for Redis geo-replication; Service Bus geo-disaster recovery; Event Hubs geo-replication',
     'OCI Cache rebuilt at DR; Streaming handled at application level'],
    ['Operations', 'Monitoring, runbooks and access still work when the primary site is gone',
     'Monitoring and identity hosted outside the primary site; runbooks in an orchestration tool',
     'CloudWatch cross-account, cross-region dashboards; AWS Config; Systems Manager',
     'Azure Monitor; Azure Policy; Automation runbooks',
     'Monitoring; Cloud Guard; Resource Manager stacks'],
]

body = f'''
        <div class="vk-wrap vk-hero">
            {crumb(("Home","/"),("Disaster Recovery","/portfolio/dr-solutions"),("DR layer by layer",None))}
            <span class="vk-eyebrow">DR guide</span>
            <h1>Disaster recovery, layer by layer</h1>
            <p class="vk-lead">A DR plan usually starts with servers and storage, because that is where the money goes. But a site failover only works if every layer has its own answer: how users find the DR site, how the network reaches it, how each database is promoted, and how anyone runs the recovery when the primary site is gone. This guide walks through each layer, what has to be true at failover, and the common way to do it on premises and in AWS, Azure and Oracle Cloud.</p>
        </div>

        <div class="vk-sec"><div class="vk-wrap">
            <h2>The layers at a glance</h2>
            <figure class="vk-fig vk-refarch vk-dgfig"><span class="vk-scroll-hint">Scroll sideways to see the whole diagram &rarr;</span><div class="vk-refarch-scroll">{render(DIAGRAM, 'Disaster recovery layer by layer')}</div><figcaption>{CAPTION}</figcaption></figure>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <h2>What each layer needs, and how it is usually done</h2>
            <p class="vk-prose">Names change between platforms; the job of each layer does not. The right-hand columns are the usual building blocks, not the only options.</p>
            <div class="vk-table-wrap"><table>
                <thead><tr><th>Layer</th><th>What must be true at failover</th><th>On premises or private cloud</th><th>AWS</th><th>Azure</th><th>Oracle Cloud</th></tr></thead>
                <tbody>{T(LAYERS)}</tbody>
            </table></div>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap"><div class="vk-prose">
            <h2>The database decision: synchronous or asynchronous</h2>
            <p><strong>Synchronous replication</strong> confirms each write at both sites before telling the application it is done. Nothing committed is lost, so the RPO is zero. The cost is latency on every write, which is why it is only practical when the sites are close: in practice within a metro, with a round trip of a few milliseconds.</p>
            <p><strong>Asynchronous replication</strong> confirms the write locally and ships it to DR a moment later. Writes stay fast and the sites can be hundreds of kilometres apart, but anything still in flight when the primary fails is lost. The RPO is the replication lag, usually seconds to a few minutes, so that lag needs an alert.</p>
            <p>Many regulated environments use both: a synchronous copy in a near site for zero data loss, and an asynchronous copy in a far site for regional events. Our <a href="/deployments/core-banking-dr">core banking DR scenario</a> shows this three-site design in detail.</p>
        </div></div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <h2>What breaks failover that is not in any layer</h2>
            <p class="vk-prose">These are the items that most often stop a drill, because nobody owns them.</p>
            <div class="vk-grid" style="margin-top:18px">
                <div class="vk-card"><h3>Identity</h3><p class="vk-muted">Active Directory, SSO and privileged access must run at DR independently. If login depends on the primary site, nobody can start the recovery.</p></div>
                <div class="vk-card"><h3>DNS TTLs and hard-coded addresses</h3><p class="vk-muted">A 24-hour DNS TTL or an IP address written into a config file can add hours to an RTO measured in minutes.</p></div>
                <div class="vk-card"><h3>Certificates and licences</h3><p class="vk-muted">Certificates issued only for primary hostnames, and licence servers that exist only in production, fail quietly on the day.</p></div>
                <div class="vk-card"><h3>Partner allow-lists</h3><p class="vk-muted">Banks, payment gateways and SaaS providers often allow traffic only from known IP addresses. The DR addresses need to be on those lists before a disaster.</p></div>
                <div class="vk-card"><h3>Start-up order</h3><p class="vk-muted">Applications started before their database or message broker fail and need manual restarts. The runbook should start layers bottom up.</p></div>
                <div class="vk-card"><h3>Failback</h3><p class="vk-muted">Coming back to the primary site is a second migration. Plan how data written at DR returns, or the team stays at DR far longer than intended.</p></div>
            </div>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap"><div class="vk-prose">
            <h2>Keeping DR the same as production</h2>
            <p>A DR site that matched production on the day it was built drifts within months: new firewall rules, a new application server, a patched database version, a changed certificate. Each change made only in production is a failover problem waiting to be found.</p>
            <ul>
                <li><strong>Build both sites from the same code.</strong> Infrastructure as code (Terraform, Ansible, Heat or cloud templates) means a change is applied to both sites or to neither.</li>
                <li><strong>Compare configurations on a schedule.</strong> A weekly automated comparison of firewall rules, server versions and database parameters between the sites catches drift early.</li>
                <li><strong>Add &ldquo;and at DR?&rdquo; to change approval.</strong> One question on the change form prevents most drift.</li>
                <li><strong>Prove it with drills.</strong> See <a href="/solutions/dc-dr/best-practices">testing DR</a> for drill types and a checklist.</li>
            </ul>
        </div></div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <h2>Related guides</h2>
            <div class="vk-grid" style="margin-top:18px">
                <a class="vk-card" href="/solutions/dc-dr/strategy-selection"><h3>Choosing a DR pattern</h3><p>Backup and restore, pilot light, warm standby, active-passive and active-active.</p><span class="vk-go">Read the guide &rarr;</span></a>
                <a class="vk-card" href="/solutions/dc-dr/cost-comparison"><h3>What DR really costs</h3><p>Where the money goes, with planning ranges and a worked example.</p><span class="vk-go">Read the guide &rarr;</span></a>
                <a class="vk-card" href="/whitepapers/disaster-recovery-strategy"><h3>DR whitepaper</h3><p>Tiers, patterns, sizing, ransomware, testing and a 40-point checklist.</p><span class="vk-go">Read or download &rarr;</span></a>
            </div>
        </div></div>
{CTA}'''

if __name__ == '__main__':
    page('solutions/dc-dr/dr-by-layer.html',
         'Disaster Recovery Layer by Layer: Traffic, Network, Database, Storage | Vakratron Systems',
         'How disaster recovery works at each layer: traffic steering, network, compute, databases, storage, messaging and operations, with on-premises, AWS, Azure and Oracle Cloud equivalents.',
         body)
