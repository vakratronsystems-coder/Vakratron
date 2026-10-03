from tpl import *
def box(x,y,w,h,lines,stroke):
    t=''.join(f'<text x="{x+w/2}" y="{y+h/2 + (i-(len(lines)-1)/2)*17 + 5}" text-anchor="middle" font-size="13" fill="#e2e8f0">{l}</text>' for i,l in enumerate(lines))
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#111a2e" stroke="{stroke}" stroke-width="1.5"/>{t}'
def arrow(y,lines,color,dash=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    t=''.join(f'<text x="480" y="{y-22+i*15}" text-anchor="middle" font-size="11.5" fill="#94a3b8">{l}</text>' for i,l in enumerate(lines))
    return f'<line x1="382" y1="{y}" x2="574" y2="{y}" stroke="{color}" stroke-width="2"{d} marker-end="url(#ah)"/>{t}'
T1,T2,T3='#C2185B','#38bdf8','#94a3b8'
rows=[(140,T1,'Tier 1 &#183; HIS and lab &#183; RPO 15 min &#183; RTO 2 h'),(255,T2,'Tier 2 &#183; Imaging (PACS) &#183; RPO 1 h &#183; RTO 8 h'),(370,T3,'Tier 3 &#183; Email, files, others &#183; RPO 24 h &#183; RTO 48 h')]
svg = ['<svg viewBox="0 0 960 490" role="img" aria-labelledby="dgt"><title id="dgt">Tiered DR design: primary hospital data centre replicating to a colocation DR site in another city</title>',
 '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#cbd5e1"/></marker></defs>',
 '<g font-family="Inter, sans-serif">',
 box(380,12,200,46,['Doctors, nurses, lab staff'],'#475569'),
 '<path d="M430,58 L430,74 L210,74 L210,90" fill="none" stroke="#cbd5e1" stroke-width="1.5" marker-end="url(#ah)"/>',
 '<path d="M530,58 L530,74 L750,74 L750,90" fill="none" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#ah)"/>',
 '<text x="640" y="68" font-size="11.5" fill="#94a3b8">DNS switch on failover</text>',
 '<rect x="20" y="92" width="362" height="388" rx="12" fill="#0b1224" stroke="#334155"/>',
 '<rect x="578" y="92" width="362" height="388" rx="12" fill="#0b1224" stroke="#334155"/>',
 '<text x="201" y="118" text-anchor="middle" font-size="14" font-weight="600" fill="#fff">Primary: main hospital data centre</text>',
 '<text x="759" y="118" text-anchor="middle" font-size="14" font-weight="600" fill="#fff">DR: colocation rack, another city</text>']
for y,c,label in rows:
    svg.append(f'<text x="36" y="{y-2}" font-size="11.5" font-weight="600" fill="{c}">{label}</text>')
svg += [box(36,148,160,62,['HIS and lab','app servers (6)'],T1), box(208,148,160,62,['HIS and lab','databases'],T1),
        box(592,148,160,62,['Standby','databases'],T1), box(764,148,160,62,['App servers: 2 on,','scale to 6'],T1),
        arrow(179,['Database replication','async, lag under 15 min'],T1),
        box(36,263,332,62,['PACS image storage','about 40 TB, growing about 1 TB a month'],T2),
        box(592,263,332,62,['Last 90 days of images ready','older images on object storage'],T2),
        arrow(294,['Image replication','every 15 to 60 min'],T2),
        box(36,378,160,62,['Email, file shares,','other servers'],T3), box(208,378,160,62,['Backup server','(local copy)'],T3),
        box(592,378,332,62,['Immutable backup copy','servers restored when needed'],T3),
        arrow(409,['Nightly backup copy'],T3,'6 4'),
        '</g></svg>']
svg=''.join(svg)

body = f'''
        <div class="vk-wrap vk-hero">
            {crumb(("Home","/"),("Disaster Recovery","/portfolio/dr-solutions"),("Use case: hospital group",None))}
            <div class="vk-label"><span>Illustrative scenario</span></div>
            <h1>Tiered disaster recovery for a hospital group</h1>
            <p class="vk-lead">How we would approach DR for a three-hospital group whose only copy of its data sat in the same building as production.</p>
            <div class="vk-note"><p class="vk-small">This is a composite example built from requirements that are common in hospital IT. It is not a specific client engagement, and the figures are design targets for the scenario, not measured results. It shows how we think through a DR problem from start to finish.</p></div>
            <div class="vk-facts">
                <div class="vk-fact"><span class="k">Organisation</span><span class="v">3 hospitals, ~600 beds</span></div>
                <div class="vk-fact"><span class="k">Key systems</span><span class="v">HIS, lab, PACS imaging</span></div>
                <div class="vk-fact"><span class="k">Data</span><span class="v">~40 TB, mostly images</span></div>
                <div class="vk-fact"><span class="k">Pattern used</span><span class="v">Three tiers</span></div>
            </div>
        </div>

        <div class="vk-sec"><div class="vk-wrap"><div class="vk-prose">
            <span class="vk-eyebrow">The situation</span>
            <h2>One server room, one copy, no tested plan</h2>
            <p>All clinical systems ran from a server room at the main hospital: the hospital information system (HIS) for admissions, billing and patient records, the lab system, and PACS for X-ray, CT and MRI images. Backups ran every night to a disk appliance in the same room.</p>
            <p>A UPS failure took the room down for nine hours. Wards went back to paper, the lab phoned results through, and radiologists could not see previous scans. Nobody could say how long a full restore would take, because a full restore had never been tried.</p>
            <p>The management team asked a simple question: <em>if the server room is lost tomorrow, how long until doctors can work normally again, and how much data do we lose?</em></p>
        </div></div></div>

        <div class="vk-sec"><div class="vk-wrap"><div class="vk-prose">
            <span class="vk-eyebrow">What we found</span>
            <h2>Not every system needs the same protection</h2>
            <p>We sat with the medical director, the lab head, the radiology head and finance, and asked the same two questions about each system: how much data can you afford to lose, and how long can you work without it?</p>
            <ul>
                <li><strong>HIS and lab</strong> were critical. Admissions, medication orders and lab results flow through them all day. Staff could re-enter about 15 minutes of work from paper. Two hours of downtime was the most they could manage safely.</li>
                <li><strong>PACS</strong> was important, but in a specific way. Radiologists needed recent scans quickly. Images older than about three months were rarely needed on the first day.</li>
                <li><strong>Email, file shares and the remaining servers</strong> could wait a day or two.</li>
                <li>The only backup copy was in the same room as production, so it offered no protection against fire, flood or a long power failure.</li>
            </ul>
        </div></div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <span class="vk-eyebrow">The design</span>
            <h2>Three tiers, one DR site</h2>
            <p class="vk-prose">A colocation rack in another city, far enough away not to share the same power grid, flood risk or local disruption. Each tier uses the cheapest pattern that still meets its targets.</p>
            <div class="vk-table-wrap"><table>
                <thead><tr><th>Tier</th><th>Systems</th><th>RPO / RTO target</th><th>Pattern</th><th>How</th></tr></thead>
                <tbody>
                    <tr><td>1</td><td>HIS, lab</td><td>15 min / 2 h</td><td>Warm standby</td><td>Database replication to standby databases at DR. Two application servers run at DR and scale to six on failover.</td></tr>
                    <tr><td>2</td><td>PACS</td><td>1 h / 8 h</td><td>Pilot light</td><td>Recent images replicated on a schedule. Older images kept on object storage at DR. Viewer servers started on failover.</td></tr>
                    <tr><td>3</td><td>Email, files, others</td><td>24 h / 48 h</td><td>Backup &amp; restore</td><td>Nightly backup copied to immutable storage at DR. Servers restored only when needed.</td></tr>
                </tbody>
            </table></div>
            <figure class="vk-fig">{svg}<figcaption>Solid lines: continuous or scheduled replication. Dashed lines: backup copy, and the user path after failover.</figcaption></figure>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap"><div class="vk-prose">
            <span class="vk-eyebrow">Sizing</span>
            <h2>How much bandwidth does this need?</h2>
            <p>Replication bandwidth comes from how much data changes each day, not from total data size. For this scenario:</p>
            <ul>
                <li>HIS and lab database changes: about 30 GB a day</li>
                <li>New imaging studies: about 35 GB a day</li>
                <li>Other backup data sent across: about 10 GB a day</li>
            </ul>
            <p>That is about 75 GB a day, which works out to roughly 7 Mbps if spread evenly over 24 hours. Hospital traffic is not spread evenly. If 60% of it arrives during a five-hour morning outpatient peak, the link needs to carry around 20 Mbps at peak without falling behind.</p>
            <p>We would recommend <strong>two 100 Mbps links from different providers</strong>. Each one can carry the peak alone with plenty of headroom, so losing one link does not break the RPO.</p>
            <div class="vk-note"><p><strong>The first copy is a separate problem.</strong> Sending 40 TB of existing images over a 200 Mbps link would take about 18 days. Shipping encrypted disks to the DR site for the first copy, then replicating only changes over the network, is faster and safer.</p></div>
        </div></div></div>

        <div class="vk-sec"><div class="vk-wrap"><div class="vk-prose">
            <span class="vk-eyebrow">Rollout</span>
            <h2>How it would be delivered</h2>
            <ol class="vk-steps">
                <li><strong>Weeks 1&ndash;3:</strong> application inventory, dependency mapping, and RPO/RTO sign-off with clinical and finance heads.</li>
                <li><strong>Weeks 3&ndash;5:</strong> DR site selection, network links ordered, bill of materials finalised.</li>
                <li><strong>Build:</strong> tier 3 backups first (quickest win), then tier 1 replication, then PACS seeding and replication.</li>
                <li><strong>Runbooks:</strong> one per tier, written with the people who will run them, including the paper downtime procedure for wards.</li>
                <li><strong>First drill:</strong> isolated failover of tier 1 on a Sunday morning. Measured recovery time and replication lag recorded against the targets, every issue fixed and retested.</li>
            </ol>
        </div></div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <span class="vk-eyebrow">What changes</span>
            <h2>Before and after (design targets)</h2>
            <div class="vk-table-wrap"><table>
                <thead><tr><th></th><th>Before</th><th>After (target)</th><th>How it is checked</th></tr></thead>
                <tbody>
                    <tr><td>HIS data lost if the site is lost</td><td>Up to 24 hours (since last backup)</td><td>Up to 15 minutes</td><td>Replication lag monitored with alerts</td></tr>
                    <tr><td>HIS back in service</td><td>Unknown. Nine hours in the UPS incident</td><td>Within 2 hours</td><td>Timed in each drill</td></tr>
                    <tr><td>Where the backup copy lives</td><td>Same room as production</td><td>Another city, plus an immutable copy</td><td>Monthly restore test</td></tr>
                    <tr><td>Recovery instructions</td><td>In one engineer's head</td><td>Written runbook for each tier</td><td>Tabletop review every quarter</td></tr>
                    <tr><td>DR running footprint</td><td>None</td><td>Roughly a third of production compute</td><td>Tier 1 runs at reduced size; tiers 2 and 3 are mostly off</td></tr>
                </tbody>
            </table></div>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap"><div class="vk-prose">
            <span class="vk-eyebrow">Trade-offs</span>
            <h2>What we would flag to the hospital</h2>
            <ul>
                <li><strong>Up to 15 minutes of HIS data can still be lost.</strong> Replication is asynchronous because the sites are far apart. Wards need a paper downtime form and a clear re-entry step after failover.</li>
                <li><strong>Older images come back slowly.</strong> Scans older than 90 days restore from object storage over hours, not minutes. Radiology agreed this was acceptable for the first day.</li>
                <li><strong>Database licences matter.</strong> Built-in replication features are not included in every database edition. For example, Oracle Data Guard requires Enterprise Edition. If the HIS runs on a lower edition, the replication method and its cost change.</li>
                <li><strong>DR only stays useful if it is tested.</strong> The budget should include two drills a year, or the setup will drift out of date within months.</li>
            </ul>
        </div></div></div>
{CTA}'''
page('use_cases/dr-hospital-group.html', 'Use Case: Tiered Disaster Recovery for a Hospital Group | Vakratron Systems',
     'An illustrative scenario: how to design tiered disaster recovery for a three-hospital group, covering HIS, lab and PACS imaging, with RPO/RTO targets, bandwidth sizing and trade-offs.', body)
