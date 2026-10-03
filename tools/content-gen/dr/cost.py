from tpl import *
body = f'''
        <div class="vk-wrap vk-hero">
            {crumb(("Home","/"),("Disaster Recovery","/portfolio/dr-solutions"),("What DR costs",None))}
            <span class="vk-eyebrow">DR guide</span>
            <h1>What disaster recovery really costs</h1>
            <p class="vk-lead">DR cost comes down to one question: how much of your production setup has to be running at the DR site before a disaster happens? Answer that for each application and most of the budget follows.</p>
        </div>

        <div class="vk-sec"><div class="vk-wrap"><div class="vk-prose">
            <h2>Where the money goes</h2>
            <ul>
                <li><strong>Space and power at the DR site.</strong> Your own second data centre, a colocation rack, or a cloud account.</li>
                <li><strong>Compute that runs every day.</strong> Servers kept powered on for databases, directory services and any warm or active tiers.</li>
                <li><strong>Storage.</strong> A full copy of protected data, plus snapshots and backup versions. Plan for more than one copy's worth of capacity.</li>
                <li><strong>Network links.</strong> Replication bandwidth between sites, ideally from two different providers.</li>
                <li><strong>Software licences.</strong> Databases, hypervisors, backup and replication tools. Some vendors charge in full for a standby copy and some do not, so read the contract.</li>
                <li><strong>People and drills.</strong> Time to write and maintain runbooks and to run tests at least once or twice a year.</li>
            </ul>
        </div></div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <h2>Rough planning ranges</h2>
            <p class="vk-prose">For a first conversation it helps to express DR running cost as a share of what the production infrastructure costs. These are the ranges we use to compare options before detailed sizing.</p>
            <div class="vk-table-wrap"><table>
                <thead><tr><th>Pattern</th><th>DR running cost vs production</th><th>Why</th></tr></thead>
                <tbody>
                    <tr><td>Backup &amp; restore</td><td>About 10&ndash;20%</td><td>Mostly storage and backup software. Almost no compute runs at DR.</td></tr>
                    <tr><td>Pilot light</td><td>About 20&ndash;35%</td><td>Replicated storage plus a small set of always-on core servers.</td></tr>
                    <tr><td>Warm standby</td><td>About 40&ndash;60%</td><td>The whole stack runs, at reduced size.</td></tr>
                    <tr><td>Active-passive</td><td>About 80&ndash;100%</td><td>A full-size copy that mostly sits idle.</td></tr>
                    <tr><td>Active-active</td><td>100% or more</td><td>Two full sites, plus the cost of changing the application.</td></tr>
                </tbody>
            </table></div>
            <div class="vk-note warn"><p>These are planning ranges, not a quote. Use them to compare options early, and replace them with real sizing before a budget is approved.</p></div>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap"><div class="vk-prose">
            <h2>A worked example</h2>
            <p>Say production has 40 virtual machines and 30 TB of data. After talking to the business owners, 8 of those VMs are critical (tier 1), 20 are important (tier 2), and 12 can wait a day or two (tier 3).</p>
            <h3>Option A: protect everything the same way</h3>
            <p>Build a full active-passive copy. The DR site needs hardware for all 40 VMs, running all the time, plus a full replicated copy of the 30 TB.</p>
            <h3>Option B: protect by tier</h3>
            <ul>
                <li>Tier 1 (8 VMs) on warm standby at about half size.</li>
                <li>Tier 2 (20 VMs) on pilot light: databases running small, application servers off.</li>
                <li>Tier 3 (12 VMs) on backup and restore.</li>
            </ul>
            <p>Day to day, Option B runs the equivalent of roughly 7 VMs at the DR site instead of 40. Tier 1 still recovers just as fast as it would under Option A.</p>
            <p>There is a catch, and it depends on where the DR site is:</p>
            <ul>
                <li><strong>On-premises or colocation:</strong> you still need hardware for tiers 1 and 2 (28 VMs) ready to start, because you cannot buy servers on the day of a disaster. The saving is in power, licences and the tier 3 capacity, not in all the hardware.</li>
                <li><strong>Cloud DR:</strong> you pay only for the small always-on footprint and the storage. Full capacity is created on drill day or disaster day. This is where the tiered approach saves the most.</li>
            </ul>
        </div></div></div>

        <div class="vk-sec"><div class="vk-wrap"><div class="vk-prose">
            <h2>Costs people forget</h2>
            <ul>
                <li><strong>Getting data back.</strong> After a cloud failover, moving data back to your own data centre can carry large egress charges. Plan failback before you need it.</li>
                <li><strong>The first copy.</strong> Seeding tens of terabytes over a WAN link can take weeks. It is often faster to ship encrypted disks for the first copy.</li>
                <li><strong>Drill time.</strong> A full failover test takes several people most of a day, plus preparation. Budget for it every year.</li>
                <li><strong>Keeping DR current.</strong> Patching DR templates, renewing certificates and updating firewall rules at the DR site is ongoing work.</li>
                <li><strong>Licence clauses.</strong> Running a standby database or hypervisor may need its own licence, depending on the vendor and how the standby is used.</li>
            </ul>
        </div></div></div>
{CTA}'''
page('solutions/dc-dr/cost-comparison.html', 'What Disaster Recovery Costs: Planning Ranges and a Worked Example | Vakratron Systems',
     'Where disaster recovery money goes, rough cost ranges for each DR pattern, a worked tiering example, and the costs teams usually forget.', body)
