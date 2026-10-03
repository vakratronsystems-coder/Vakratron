from tpl import *
body = f'''
        <div class="vk-wrap vk-hero">
            {crumb(("Home","/"),("Solutions","/solutions"),("Disaster Recovery",None))}
            <span class="vk-eyebrow">Disaster Recovery &amp; Business Continuity</span>
            <h1>Disaster recovery that has actually been tested</h1>
            <p class="vk-lead">Most organisations have a DR site. Far fewer know how long it really takes to bring their applications back, or whether it works at all. We help you decide what needs protection and how fast it must recover, then design and build it and run the first drill with your team.</p>
            <div class="vk-actions">
                <a class="vk-btn primary" href="/contact">Book a DR review</a>
                <a class="vk-btn" href="#see-it-work">See how DR patterns work</a>
            </div>
        </div>

        <div class="vk-sec"><div class="vk-wrap">
            <span class="vk-eyebrow">What usually goes wrong</span>
            <h2>Four problems we see again and again</h2>
            <div class="vk-grid" style="margin-top:22px">
                <div class="vk-card">
                    <h3>The DR site has never really been used</h3>
                    <p class="vk-muted">Replication shows green on the dashboard. But nobody has started the applications at the DR site and checked that a user can log in and complete a transaction.</p>
                </div>
                <div class="vk-card">
                    <h3>Everything gets the same protection</h3>
                    <p class="vk-muted">A test server gets the same treatment as the core database. The DR bill goes up, and the systems that matter are still not fast enough to recover.</p>
                </div>
                <div class="vk-card">
                    <h3>Backups sit next to production</h3>
                    <p class="vk-muted">If ransomware, fire or a long power failure hits the main site, the backup copy is lost along with it.</p>
                </div>
                <div class="vk-card">
                    <h3>The runbook lives in one person's head</h3>
                    <p class="vk-muted">Recovery depends on one engineer remembering the order things start in. When that person is on leave, recovery slows down or stops.</p>
                </div>
            </div>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap"><div class="vk-prose">
            <span class="vk-eyebrow">The two numbers that matter</span>
            <h2>Start with RPO and RTO, not hardware</h2>
            <p><strong>RPO (Recovery Point Objective)</strong> is how much data you can afford to lose, measured in time. An RPO of 15 minutes means that in the worst case you lose the last 15 minutes of transactions.</p>
            <p><strong>RTO (Recovery Time Objective)</strong> is how long a service can stay down before the damage becomes serious. An RTO of 2 hours means users must be working again within 2 hours of someone declaring a disaster.</p>
            <p>Lower numbers cost more. Moving from a 24-hour RPO to 15 minutes usually means replacing nightly backups with continuous replication, which changes the network, the storage and often the software licences. That is why we set these numbers application by application, with the business owner in the room, before anyone talks about servers.</p>
        </div></div></div>


        <div class="vk-sec" id="see-it-work"><div class="vk-wrap">
            <span class="vk-eyebrow">See it working</span>
            <h2>What happens to each pattern in a disaster</h2>
            <p class="vk-prose">Pick a pattern to see what is running at the DR site on a normal day. Then press <strong>Simulate a disaster</strong> to watch the primary site go down and the DR site take over, step by step. Notice how much longer the cheaper patterns take to recover.</p>
            <div class="vk-drsim" data-start="pilot-light"></div>
            <noscript><p class="vk-muted">This interactive diagram needs JavaScript. The <a href="/solutions/dc-dr/strategy-selection">DR patterns guide</a> compares the same five patterns in a table.</p></noscript>
        </div></div>
        <div class="vk-sec"><div class="vk-wrap"><div class="vk-prose">
            <span class="vk-eyebrow">How we work</span>
            <h2>How a DR engagement runs</h2>
            <ol class="vk-steps">
                <li><strong>List the applications and what they depend on.</strong> Databases, Active Directory, DNS, file shares, licence servers, integrations, and who owns each application. Missing dependencies are the most common reason a failover stalls.</li>
                <li><strong>Agree RPO and RTO for each application.</strong> We sort applications into three or four tiers with the business owners. In most environments only a small share of applications truly needs recovery within a few hours.</li>
                <li><strong>Pick a DR pattern for each tier.</strong> Backup and restore, pilot light, warm standby, active-passive or active-active. <a href="/solutions/dc-dr/strategy-selection">See how they compare.</a></li>
                <li><strong>Size the DR site and the network.</strong> Replication bandwidth comes from your real daily change rate, not a guess. We show the assumptions so your team can check them.</li>
                <li><strong>Build it and write the runbook.</strong> Step-by-step recovery for each tier: who does what, in which order, and how to tell that a step worked.</li>
                <li><strong>Run the first drill.</strong> A timed failover of at least one tier. Every issue gets logged and fixed, and you get a drill schedule to keep going.</li>
            </ol>
        </div></div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <div class="vk-two">
                <div>
                    <span class="vk-eyebrow">Deliverables</span>
                    <h2>What you get at the end</h2>
                    <ul>
                        <li>Application inventory with dependencies and tiers</li>
                        <li>RPO and RTO sheet signed off by business owners</li>
                        <li>Target DR architecture and bill of materials</li>
                        <li>Bandwidth and storage sizing, with the assumptions shown</li>
                        <li>Recovery runbook for each tier</li>
                        <li>Drill report with measured recovery times</li>
                    </ul>
                </div>
                <div>
                    <span class="vk-eyebrow">Where it runs</span>
                    <h2>Platforms we design for</h2>
                    <ul>
                        <li>VMware, KVM and OpenStack private clouds</li>
                        <li>DR from on-premises into AWS, Azure or OCI</li>
                        <li>Two data centres, or a data centre plus a colocation rack</li>
                        <li>Kubernetes workloads, including persistent volumes</li>
                        <li>Database-level replication for Oracle, SQL Server, PostgreSQL and MySQL</li>
                    </ul>
                </div>
            </div>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <span class="vk-eyebrow">Go deeper</span>
            <h2>Guides and examples</h2>
            <div class="vk-grid" style="margin-top:22px">
                <a class="vk-card" href="/solutions/dc-dr/strategy-selection"><h3>Choosing a DR pattern</h3><p>Five ways to set up DR, what each costs, and where each one fits.</p><span class="vk-go">Read the guide &rarr;</span></a>
                <a class="vk-card" href="/solutions/dc-dr/cost-comparison"><h3>What DR really costs</h3><p>Where the money goes, rough planning ranges, and a worked example.</p><span class="vk-go">Read the guide &rarr;</span></a>
                <a class="vk-card" href="/solutions/dc-dr/openstack-mapping"><h3>DR on OpenStack</h3><p>How Ceph, Cinder, Neutron and automation fit together for a site failover.</p><span class="vk-go">Read the guide &rarr;</span></a>
                <a class="vk-card" href="/solutions/dc-dr/best-practices"><h3>Testing DR</h3><p>Types of drill, how often to run them, and a checklist for the day.</p><span class="vk-go">Read the guide &rarr;</span></a>
                <a class="vk-card" href="/use_cases/dr-hospital-group"><h3>Use case: hospital group DR</h3><p>An illustrative scenario: tiered DR for HIS, lab and imaging systems.</p><span class="vk-go">Read the use case &rarr;</span></a>
                <a class="vk-card" href="/solutions/dc-dr/faq"><h3>DR questions, answered</h3><p>Backup vs DR, site distance, cloud DR, ransomware and more.</p><span class="vk-go">Read the FAQ &rarr;</span></a>
            </div>
            <p class="vk-muted vk-small" style="margin-top:18px">For the full technical reference, see the <a href="/solutions/master_dc-dr">DC-DR whitepaper</a>.</p>
        </div></div>
{CTA}'''
page('portfolio/dr-solutions.html', 'Disaster Recovery (DC-DR) Design and Testing | Vakratron Systems',
     'We help organisations decide what needs disaster recovery and how fast it must come back, then design, build and test it. Plain guidance on RPO, RTO, DR patterns and cost.', body, scripts=['/vk-dr-sim.js'])
