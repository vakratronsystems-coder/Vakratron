from tpl import *
body = f'''
        <div class="vk-wrap vk-hero">
            {crumb(("Home","/"),("Disaster Recovery","/portfolio/dr-solutions"),("Testing DR",None))}
            <span class="vk-eyebrow">DR guide</span>
            <h1>Testing DR and keeping it working</h1>
            <p class="vk-lead">DR that has never been tested is a guess. Most problems only appear the first time someone actually fails over: a missing firewall rule, an expired certificate at the DR site, a licence server that only exists in production. Testing finds these while there is no real disaster.</p>
        </div>

        <div class="vk-sec"><div class="vk-wrap">
            <h2>Four kinds of test</h2>
            <div class="vk-table-wrap"><table>
                <thead><tr><th>Test</th><th>What happens</th><th>Suggested frequency</th></tr></thead>
                <tbody>
                    <tr><td>Tabletop walk-through</td><td>The team reads the runbook step by step and checks that every step, name and phone number is still correct.</td><td>Every quarter</td></tr>
                    <tr><td>Restore test</td><td>Restore one server or database from backup and confirm it works.</td><td>Every month, rotating systems</td></tr>
                    <tr><td>Isolated failover</td><td>Bring a tier up at DR on an isolated network, without touching production users.</td><td>Twice a year for each tier</td></tr>
                    <tr><td>Full failover</td><td>Move real users to DR for an agreed window, then fail back.</td><td>Once a year for tier 1</td></tr>
                </tbody>
            </table></div>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <h2>Drill-day checklist</h2>
            <div class="vk-grid" style="margin-top:18px">
                <div class="vk-card"><h3>Before</h3><ul>
                    <li>Freeze changes for the systems in scope</li>
                    <li>Confirm replication lag is within RPO</li>
                    <li>Tell users and the helpdesk</li>
                    <li>Write down what &ldquo;success&rdquo; means, for example: users can log in and the last transaction is within the RPO</li>
                </ul></div>
                <div class="vk-card"><h3>During</h3><ul>
                    <li>Time every step</li>
                    <li>Write down every manual fix, however small</li>
                    <li>Have the application owner test, not only IT</li>
                    <li>Agree a hard stop time for rolling back</li>
                </ul></div>
                <div class="vk-card"><h3>After</h3><ul>
                    <li>Report measured RPO and RTO against the targets</li>
                    <li>Turn every issue into a fix with an owner and a date</li>
                    <li>Update the runbook the same week</li>
                    <li>Book the next drill</li>
                </ul></div>
            </div>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap"><div class="vk-prose">
            <h2>Keeping DR working between drills</h2>
            <ul>
                <li><strong>Alert on replication lag.</strong> Lag that quietly grows past the RPO is the most common silent failure.</li>
                <li><strong>Make DR part of change management.</strong> Every new application, firewall change or certificate renewal should include the question &ldquo;and at DR?&rdquo;.</li>
                <li><strong>Patch DR the same as production.</strong> Templates and standby servers fall behind fast.</li>
                <li><strong>Keep immutable backups.</strong> At least one copy that cannot be changed or deleted from the network.</li>
                <li><strong>Review the tiers once a year.</strong> Applications change in importance. Last year's tier 3 system may now be critical.</li>
            </ul>
        </div></div></div>
{CTA}'''
page('solutions/dc-dr/best-practices.html', 'Testing Disaster Recovery: Drill Types, Frequency and Checklist | Vakratron Systems',
     'How to test disaster recovery: tabletop, restore, isolated and full failover tests, how often to run them, a drill-day checklist, and how to keep DR working between drills.', body)

faqs = [
 ("What is the difference between backup and disaster recovery?",
  "<p>A backup is a copy of your data. Disaster recovery is the plan and the infrastructure that let you run your services somewhere else when the main site is lost. You need both. Replication on its own copies mistakes and ransomware just as fast as good data, so backups with older versions are still essential.</p>"),
 ("What do RPO and RTO mean?",
  "<p><strong>RPO</strong> is how much data you can afford to lose, measured in time. <strong>RTO</strong> is how long the service can be down. An RPO of 15 minutes and an RTO of 2 hours means: lose at most the last 15 minutes of work, and be running again within 2 hours.</p>"),
 ("Do we need a second data centre?",
  "<p>Not always. A colocation rack, a cloud account, or a well-powered room at another office can all work as a DR site, depending on the tier. What matters is that it does not share the same risks as the main site: same building, same power feed, same flood zone.</p>"),
 ("How far apart should the two sites be?",
  "<p>It is a trade-off. Synchronous replication, which gives near-zero data loss, generally needs the sites within about 100 km because every write waits for the other site. Protection against regional events such as floods or a grid failure needs more distance, which means asynchronous replication and a small amount of possible data loss. Some organisations use both: a nearby site in sync and a distant site behind it.</p>"),
 ("Can our DR site be in the public cloud?",
  "<p>For many workloads, yes. Check three things first: whether the data is allowed to sit with that provider and in that region, what it will cost to move data back after a failover, and whether your applications run properly on the cloud's virtual machines without changes.</p>"),
 ("Does DR protect us from ransomware?",
  "<p>Replication alone does not. Encrypted files replicate to DR like any other change. Ransomware protection needs immutable or offline backups, separate admin credentials for the DR and backup systems, and a tested way to restore from a point before the attack.</p>"),
 ("How often should we test?",
  "<p>A tabletop review every quarter, a restore test every month, an isolated failover for each tier twice a year, and a full failover of the critical systems once a year. See <a href='/solutions/dc-dr/best-practices'>Testing DR</a> for details.</p>"),
 ("How long does a DR project take?",
  "<p>For a mid-sized environment, the assessment and design usually take three to six weeks. The build depends mostly on procurement: hardware lead times, network links and the DR site contract. The first drill normally follows a few weeks after the build.</p>"),
 ("What do you need from us to start?",
  "<p>A list of your applications and their owners, a short description of how backups work today, a network diagram if you have one, and any regulatory or contractual DR requirements. That is enough for a first gap review.</p>"),
]
items = ''.join(f'<details><summary>{q}</summary><div>{a}</div></details>' for q,a in faqs)
body = f'''
        <div class="vk-wrap vk-hero">
            {crumb(("Home","/"),("Disaster Recovery","/portfolio/dr-solutions"),("FAQ",None))}
            <span class="vk-eyebrow">DR guide</span>
            <h1>Disaster recovery questions, answered</h1>
            <p class="vk-lead">Short answers to the questions IT heads and business owners ask us most often about DR.</p>
        </div>
        <div class="vk-sec"><div class="vk-wrap"><div class="vk-prose">{items}</div></div></div>
{CTA}'''
page('solutions/dc-dr/faq.html', 'Disaster Recovery FAQ: RPO, RTO, Site Distance, Cloud DR and Ransomware | Vakratron Systems',
     'Plain answers to common disaster recovery questions: backup vs DR, RPO and RTO, how far apart sites should be, cloud DR, ransomware, testing and project timelines.', body)
