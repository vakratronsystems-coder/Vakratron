from tpl import *
def pattern(pid, name, how, fit, watch):
    w = ''.join(f'<li>{x}</li>' for x in watch)
    return f'''
            <div id="{pid}" style="scroll-margin-top:110px; margin-top:34px">
                <h3>{name}</h3>
                <p>{how}</p>
                <p><strong>Good fit:</strong> {fit}</p>
                <p><strong>Watch out for:</strong></p>
                <ul>{w}</ul>
            </div>'''
body = f'''
        <div class="vk-wrap vk-hero">
            {crumb(("Home","/"),("Disaster Recovery","/portfolio/dr-solutions"),("Choosing a DR pattern",None))}
            <span class="vk-eyebrow">DR guide</span>
            <h1>Choosing a DR pattern</h1>
            <p class="vk-lead">There are five common ways to set up disaster recovery. They differ in how much data you can lose, how quickly you come back, and how much you pay to keep the DR site ready. Most organisations end up using two or three of them at once, one for each tier of applications.</p>
        </div>


        <div class="vk-sec" id="see-it-work"><div class="vk-wrap">
            <span class="vk-eyebrow">See it working</span>
            <h2>What happens to each pattern in a disaster</h2>
            <p class="vk-prose">Pick a pattern to see what is running at the DR site on a normal day. Then press <strong>Simulate a disaster</strong> to watch the primary site go down and the DR site take over, step by step. Notice how much longer the cheaper patterns take to recover.</p>
            <div class="vk-drsim" data-start="backup-restore"></div>
            <noscript><p class="vk-muted">This interactive diagram needs JavaScript. The table below compares the same five patterns.</p></noscript>
        </div></div>
        <div class="vk-sec"><div class="vk-wrap">
            <h2>The five patterns side by side</h2>
            <div class="vk-table-wrap"><table>
                <thead><tr><th>Pattern</th><th>What is ready at the DR site</th><th>Typical RPO</th><th>Typical RTO</th><th>Relative cost</th><th>Usually fits</th></tr></thead>
                <tbody>
                    <tr><td><a href="#backup-restore">Backup &amp; restore</a></td><td>Backup copies only. Servers are rebuilt after the disaster.</td><td>Hours (time since last backup)</td><td>Hours to days</td><td>Low</td><td>Internal tools, archives, dev and test</td></tr>
                    <tr><td><a href="#pilot-light">Pilot light</a></td><td>Data is replicated. Core services such as the database and directory run small. Application servers are off.</td><td>Minutes</td><td>A few hours</td><td>Low to medium</td><td>Business systems that can be down for half a day</td></tr>
                    <tr><td><a href="#warm-standby">Warm standby</a></td><td>The full stack runs at reduced size and is scaled up on failover.</td><td>Seconds to minutes</td><td>Under an hour to a few hours</td><td>Medium to high</td><td>ERP, hospital systems, customer portals</td></tr>
                    <tr><td><a href="#active-passive">Active-passive</a></td><td>A full-size copy is ready to take over.</td><td>Near zero (synchronous) to minutes (asynchronous)</td><td>Minutes</td><td>High</td><td>Core banking, payments, billing</td></tr>
                    <tr><td><a href="#active-active">Active-active</a></td><td>Both sites serve users at the same time.</td><td>Near zero</td><td>Near zero for users</td><td>Very high, plus application changes</td><td>Services built for two sites from day one</td></tr>
                </tbody>
            </table></div>
            <p class="vk-muted vk-small">These are typical ranges. Your real numbers depend on the replication method, data volume, distance between sites, and how well the runbook has been rehearsed.</p>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap"><div class="vk-prose">
            <h2>How each pattern works</h2>
            {pattern("backup-restore","Backup and restore",
              "Data is backed up on a schedule and a copy is kept away from the main site. After a disaster you build or rent servers, restore the data and start the applications. Nothing runs at the DR site until you need it.",
              "Systems where a day or two of downtime is acceptable, and the cheapest layer of protection for everything else.",
              ["Restore time grows with data size. Restoring 20 TB over a 1 Gbps link takes roughly two days before you even start the applications.",
               "Ransomware. Keep at least one copy that is immutable or offline, so an attacker who reaches your backup server cannot delete it.",
               "Restores that have never been tried. Test a full restore of one system every month."])}
            {pattern("pilot-light","Pilot light",
              "Data is replicated continuously. The pieces that take longest to rebuild, usually the database and directory services, run at the DR site in a small configuration. Application and web servers exist as templates and are started only during a failover.",
              "Important business systems that can tolerate a few hours of downtime but not a day of lost data.",
              ["Templates going stale. The application server images at DR must get the same patches and configuration changes as production.",
               "Manual start-up steps. Use automation such as Terraform, Heat or Ansible to start the stopped tiers, or failover will be slow and error-prone.",
               "Licences. Check whether your software vendor allows a standby copy without a full licence."])}
            {pattern("warm-standby","Warm standby",
              "A complete, working copy of the application runs at the DR site at reduced size, for example two application servers instead of eight. On failover you scale it up and point users to it.",
              "Customer-facing and operations-critical systems where recovery has to happen within an hour or two.",
              ["The scale-up step. If DR runs at a quarter of production size, you must be sure the extra capacity is actually available on the day.",
               "Configuration drift. Because DR is running, people sometimes change it directly. Manage both sites from the same code."])}
            {pattern("active-passive","Active-passive",
              "A full-size copy of production sits at the DR site, kept in sync with storage or database replication. If the primary fails, the passive site takes over.",
              "Systems where even an hour of downtime causes serious financial, regulatory or safety impact.",
              ["Distance and latency. Synchronous replication, which gives near-zero data loss, needs low latency between sites. In practice that usually means the sites are within about 100 km. Beyond that, replication is asynchronous and a few seconds to minutes of data can be lost.",
               "Split brain. If the two sites lose contact, both may try to act as primary. Use a witness or quorum at a third location.",
               "Paying for idle capacity. The passive site is full-size and mostly unused. Some teams run reporting or test workloads there to make use of it."])}
            {pattern("active-active","Active-active",
              "Both sites serve live users at the same time. If one site fails, the other carries the full load.",
              "Applications designed for multiple sites, typically stateless web and API tiers with a database built for multi-site writes.",
              ["The database. Writing to the same data from two sites at once is hard. Many setups described as active-active are active-active for the web and application tiers and active-passive for the database. That is often the right call.",
               "Capacity. Each site must be able to carry the full load alone, so in normal running each is at most half used.",
               "Application changes. Most existing applications need rework before they can run safely at two sites at once."])}
        </div></div></div>

        <div class="vk-sec"><div class="vk-wrap"><div class="vk-prose">
            <h2>Four questions to pick the right one</h2>
            <ol class="vk-steps">
                <li><strong>What does one hour of downtime cost?</strong> Lost revenue, penalties, patient safety, citizen services. If nobody can put a number or a consequence on it, it probably does not need the expensive patterns.</li>
                <li><strong>How much recent data can be re-entered by hand?</strong> If staff can re-key the last 30 minutes from paper or email, an asynchronous pattern is usually enough.</li>
                <li><strong>Does a regulator or contract set the number?</strong> Banks, insurers, market intermediaries and many government systems have business continuity requirements written down. Start from those.</li>
                <li><strong>Can the application be changed?</strong> If not, active-active is usually off the table, and active-passive or warm standby is the realistic ceiling.</li>
            </ol>
            <div class="vk-note"><p>Most organisations land on three tiers: active-passive or warm standby for a handful of critical systems, pilot light for important business applications, and backup and restore for everything else. The <a href="/use_cases/dr-hospital-group">hospital group use case</a> shows what that looks like in practice.</p></div>
        </div></div></div>
{CTA}'''
page('solutions/dc-dr/strategy-selection.html', 'Choosing a DR Pattern: Backup, Pilot Light, Warm Standby, Active-Passive, Active-Active | Vakratron Systems',
     'A plain comparison of the five common disaster recovery patterns: what each one keeps ready, typical RPO and RTO, relative cost, and where each one fits.', body, scripts=['/vk-dr-sim.js'])
