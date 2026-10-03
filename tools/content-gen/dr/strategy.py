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


        <div class="vk-sec"><div class="vk-wrap">
            <h2>The five patterns side by side</h2>
            <div class="vk-table-wrap"><table>
                <thead><tr><th>Pattern</th><th>What is ready at the DR site</th><th>Typical RPO</th><th>Typical RTO</th><th>Relative cost</th><th>Usually fits</th></tr></thead>
                <tbody>
                    <tr><td><a href="/solutions/dc-dr/backup-restore">Backup &amp; restore</a></td><td>Backup copies only. Servers are rebuilt after the disaster.</td><td>Hours (time since last backup)</td><td>Hours to days</td><td>Low</td><td>Internal tools, archives, dev and test</td></tr>
                    <tr><td><a href="/solutions/dc-dr/pilot-light">Pilot light</a></td><td>Data is replicated. Core services such as the database and directory run small. Application servers are off.</td><td>Minutes</td><td>A few hours</td><td>Low to medium</td><td>Business systems that can be down for half a day</td></tr>
                    <tr><td><a href="/solutions/dc-dr/warm-standby">Warm standby</a></td><td>The full stack runs at reduced size and is scaled up on failover.</td><td>Seconds to minutes</td><td>Under an hour to a few hours</td><td>Medium to high</td><td>ERP, hospital systems, customer portals</td></tr>
                    <tr><td><a href="/solutions/dc-dr/active-passive">Active-passive</a></td><td>A full-size copy is ready to take over.</td><td>Near zero (synchronous) to minutes (asynchronous)</td><td>Minutes</td><td>High</td><td>Core banking, payments, billing</td></tr>
                    <tr><td><a href="/solutions/dc-dr/active-active">Active-active</a></td><td>Both sites serve users at the same time.</td><td>Near zero</td><td>Near zero for users</td><td>Very high, plus application changes</td><td>Services built for two sites from day one</td></tr>
                </tbody>
            </table></div>
            <p class="vk-muted vk-small">These are typical ranges. Your real numbers depend on the replication method, data volume, distance between sites, and how well the runbook has been rehearsed.</p>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <h2>Each pattern in detail</h2>
            <p class="vk-prose">Every pattern has its own page with an interactive disaster simulation, a reference architecture, a failover runbook and the tools typically used.</p>
            <div class="vk-grid" style="margin-top:18px">
                <a class="vk-card" href="/solutions/dc-dr/backup-restore"><span class="vk-muted vk-small">Pattern 1 &middot; cost 1 of 5</span><h3>Backup and restore</h3><p>Only backup copies at DR. Servers are rebuilt after the disaster.</p><span class="vk-go">See how it works &rarr;</span></a>
                <a class="vk-card" href="/solutions/dc-dr/pilot-light"><span class="vk-muted vk-small">Pattern 2 &middot; cost 2 of 5</span><h3>Pilot light</h3><p>Data and a small database run at DR. Servers start from templates.</p><span class="vk-go">See how it works &rarr;</span></a>
                <a class="vk-card" href="/solutions/dc-dr/warm-standby"><span class="vk-muted vk-small">Pattern 3 &middot; cost 3 of 5</span><h3>Warm standby</h3><p>The full stack runs at DR at reduced size and is scaled up on failover.</p><span class="vk-go">See how it works &rarr;</span></a>
                <a class="vk-card" href="/solutions/dc-dr/active-passive"><span class="vk-muted vk-small">Pattern 4 &middot; cost 4 of 5</span><h3>Active-passive</h3><p>A full-size synchronised copy takes over within minutes.</p><span class="vk-go">See how it works &rarr;</span></a>
                <a class="vk-card" href="/solutions/dc-dr/active-active"><span class="vk-muted vk-small">Pattern 5 &middot; cost 5 of 5</span><h3>Active-active</h3><p>Both sites serve users. Losing one is close to invisible.</p><span class="vk-go">See how it works &rarr;</span></a>
            </div>
        </div></div>

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
     'A plain comparison of the five common disaster recovery patterns: what each one keeps ready, typical RPO and RTO, relative cost, and where each one fits.', body)
