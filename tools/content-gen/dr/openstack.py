from tpl import *
body = f'''
        <div class="vk-wrap vk-hero">
            {crumb(("Home","/"),("Disaster Recovery","/portfolio/dr-solutions"),("DR on OpenStack",None))}
            <span class="vk-eyebrow">DR guide</span>
            <h1>Disaster recovery on OpenStack</h1>
            <p class="vk-lead">OpenStack has no single &ldquo;DR button&rdquo;. Site-level recovery is built from three things: storage replication to a second OpenStack deployment, the project's setup kept as code, and a runbook that brings instances up in the right order. This page explains how those pieces fit.</p>
        </div>

        <div class="vk-sec"><div class="vk-wrap"><div class="vk-prose">
            <div class="vk-note warn"><p><strong>HA is not DR.</strong> Features such as live migration or Masakari instance HA protect you when a server fails inside one site. They do not help if you lose the whole site. For that you need a second OpenStack deployment in another location.</p></div>
        </div></div></div>

        <div class="vk-sec"><div class="vk-wrap">
            <h2>What each OpenStack service needs for DR</h2>
            <div class="vk-table-wrap"><table>
                <thead><tr><th>Layer</th><th>Service</th><th>What we set up for DR</th></tr></thead>
                <tbody>
                    <tr><td>Volumes</td><td>Cinder on Ceph RBD</td><td>Ceph RBD mirroring to the DR Ceph cluster using the <code>rbd-mirror</code> daemon. Snapshot-based mirroring on a schedule for most volumes. Journal-based mirroring for the few volumes that need a lower RPO.</td></tr>
                    <tr><td>Images</td><td>Glance</td><td>The same images published at both sites from one image pipeline, so instances boot from identical templates.</td></tr>
                    <tr><td>Object data</td><td>Ceph RGW or Swift</td><td>Multi-site replication for application object data and backup targets.</td></tr>
                    <tr><td>Compute</td><td>Nova</td><td>Flavors, quotas and key pairs created at DR in advance. Instances are recreated from mirrored volumes, which is why we prefer boot-from-volume for protected workloads.</td></tr>
                    <tr><td>Networking</td><td>Neutron</td><td>Networks, subnets, routers and security groups recreated at DR from code. Decide early whether applications keep their IP addresses (which needs a stretched network or route changes) or get new ones with DNS updates. We usually recommend new IPs with DNS.</td></tr>
                    <tr><td>Identity</td><td>Keystone</td><td>A Keystone at each site with the same projects and roles, with users coming from a shared directory (AD or LDAP) so people log in the same way at both sites.</td></tr>
                    <tr><td>Automation</td><td>Heat or Terraform, plus Ansible</td><td>Templates that recreate each protected project, and playbooks that attach the mirrored volumes and start instances in dependency order.</td></tr>
                    <tr><td>Backup</td><td>Trilio for OpenStack or agent-based backup</td><td>Point-in-time copies kept separately from replication. Replication copies corruption and ransomware just as quickly as good data, so you need versions to go back to.</td></tr>
                </tbody>
            </table></div>
        </div></div>

        <div class="vk-sec"><div class="vk-wrap"><div class="vk-prose">
            <h2>A typical failover, step by step</h2>
            <ol class="vk-steps">
                <li><strong>Declare the disaster.</strong> One named person decides, based on criteria agreed in advance. Most delays happen here, not in the technology.</li>
                <li><strong>Promote the mirrored volumes at DR.</strong> If the primary site is unreachable, the DR copies have to be forced to primary:
                    <pre>rbd mirror image promote --force &lt;pool&gt;/&lt;image&gt;</pre>
                    In practice this runs from a playbook over every protected image, not by hand.</li>
                <li><strong>Recreate or verify the project at DR.</strong> Networks, security groups and ports come from the same code used to build them originally.</li>
                <li><strong>Start the tiers in order.</strong> Database first, check it is consistent, then application servers, then web servers.</li>
                <li><strong>Move users.</strong> Update DNS or the global load balancer to point at DR. Keep DNS TTLs short beforehand so this takes minutes, not hours.</li>
                <li><strong>Check with the application owners.</strong> A real user logs in and completes a real transaction before anyone announces that the service is back.</li>
            </ol>
            <p><strong>Failback</strong> is the reverse, done as a planned switchover in a maintenance window: resync data back to the original site, demote at DR, promote at the primary, and move users back.</p>
        </div></div></div>

        <div class="vk-sec"><div class="vk-wrap"><div class="vk-prose">
            <h2>What trips teams up</h2>
            <ul>
                <li><strong>Volumes are replicated but nothing else is.</strong> Flavors, ports, security groups and metadata are not in the volume. If they are not in code, someone rebuilds them by hand during the outage.</li>
                <li><strong>The two sites drift apart.</strong> Different OpenStack or Ceph versions at each site cause surprises on failover day. Upgrade both together.</li>
                <li><strong>Nobody watches replication lag.</strong> When bandwidth runs short, mirroring falls behind quietly. Monitor <code>rbd mirror pool status</code> and alert when lag passes your RPO.</li>
                <li><strong>Failback is never tested.</strong> Teams test failing over, then discover that getting back is the harder half. Test both directions.</li>
            </ul>
        </div></div></div>
{CTA}'''
page('solutions/dc-dr/openstack-mapping.html', 'Disaster Recovery on OpenStack: Ceph Mirroring, Neutron and Failover Runbooks | Vakratron Systems',
     'How to build site-level disaster recovery on OpenStack: Ceph RBD mirroring, Nova, Neutron and Keystone at the DR site, automation, and a step-by-step failover.', body)
