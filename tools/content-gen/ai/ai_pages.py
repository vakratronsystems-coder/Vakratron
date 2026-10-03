"""AI infrastructure and GPU cloud pages (Oct 2026 rewrite). Run from tools/content-gen/ai/."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'dr'))
sys.path.insert(0, os.path.join(HERE, '..', 'cloud'))
from tpl import page, crumb
from cloud_pages import N, F, sec, hero, table, ul, steps, figure

HOME = ("Home", "/")
HUB = ("AI infrastructure", "/portfolio/ai-gpu-cloud")
SCRIPTS = ['/vk-ai-tools.js']
CTA = '''
        <div class="vk-sec"><div class="vk-wrap">
            <div class="vk-cta">
                <h2>Planning a GPU cluster?</h2>
                <p class="vk-muted">Tell us the models you want to run or train, how many users, and where it will be hosted. We will come back with a first sizing: GPUs, servers, network, storage, and the power and cooling your data centre will need.</p>
                <div class="vk-actions">
                    <a class="vk-btn primary" href="/contact">Book a GPU sizing review</a>
                    <a class="vk-btn" href="/portfolio/ai-gpu-cloud">Back to AI infrastructure</a>
                </div>
            </div>
        </div></div>'''

PAGES = [
    ('gpu-training-cluster', 'Training cluster'),
    ('gpu-inference-platform', 'Inference platform'),
    ('ai-network-fabric', 'GPU network fabric'),
    ('ai-storage', 'Storage for AI'),
    ('power-and-cooling', 'Power and cooling'),
]

def related(cur):
    return '<div class="vk-pills">' + ''.join(f'<a class="vk-pill{" on" if s == cur else ""}" href="/solutions/ai-infra/{s}">{n}</a>' for s, n in PAGES) + '</div>'

def more(cur):
    links = ' &middot; '.join(f'<a href="/solutions/ai-infra/{s}">{n}</a>' for s, n in PAGES if s != cur)
    return sec(f'<p class="vk-small"><strong>More AI infrastructure guides:</strong> {links} &middot; <a href="/solutions/ai-infra/faq">FAQ</a> &middot; <a href="/use_cases/private-llm-gpu-platform">Use case: private LLM platform</a></p>')

def guide_hero(slug, title, lead, facts, crumbname):
    b = hero((HOME, HUB, (crumbname, None)), 'AI infrastructure guide', title, lead, facts=facts)
    return b.replace('<span class="vk-eyebrow">AI infrastructure guide</span>', related(slug) + '<span class="vk-eyebrow">AI infrastructure guide</span>', 1)


# ------------------------------------------------------------------ rail-optimised fabric diagram
def rail_svg():
    cols = ['#38bdf8', '#f472b6', '#a78bfa', '#fbbf24', '#34d399', '#fb923c', '#60a5fa', '#e879f9']
    o = ['<svg viewBox="0 0 960 440" role="img" aria-label="Rail-optimised GPU fabric: GPU N of every server connects to leaf switch N"><g font-family="Inter, sans-serif">']
    spines = [100 + j * 210 for j in range(4)]
    leaves = [30 + i * 115 for i in range(8)]
    nodes = [30 + k * 240 for k in range(4)]
    for lx in leaves:
        for sx in spines:
            o.append(f'<line x1="{lx+47}" y1="150" x2="{sx+70}" y2="70" stroke="#334155" stroke-width="1"/>')
    for k, nx in enumerate(nodes):
        for i in range(8):
            gx = nx + 12 + i * 23 + 8
            o.append(f'<line x1="{gx}" y1="300" x2="{leaves[i]+47}" y2="192" stroke="{cols[i]}" stroke-width="1.6" opacity="0.75"/>')
    for j, sx in enumerate(spines):
        o.append(f'<rect x="{sx}" y="28" width="140" height="42" rx="8" fill="#111a2e" stroke="#94a3b8"/><text x="{sx+70}" y="54" text-anchor="middle" font-size="13" font-weight="600" fill="#e2e8f0">Spine {j+1}</text>')
    for i, lx in enumerate(leaves):
        o.append(f'<rect x="{lx}" y="150" width="95" height="42" rx="8" fill="#0f172a" stroke="{cols[i]}" stroke-width="1.6"/><text x="{lx+47}" y="176" text-anchor="middle" font-size="12.5" font-weight="600" fill="#e2e8f0">Rail {i+1} leaf</text>')
    for k, nx in enumerate(nodes):
        o.append(f'<rect x="{nx}" y="300" width="210" height="96" rx="10" fill="#0b1224" stroke="#38bdf8"/>')
        o.append(f'<text x="{nx+105}" y="322" text-anchor="middle" font-size="13" font-weight="600" fill="#fff">8-GPU server {k+1}</text>')
        for i in range(8):
            gx = nx + 12 + i * 23
            o.append(f'<rect x="{gx}" y="334" width="17" height="17" rx="3" fill="{cols[i]}" opacity="0.85"/>')
        o.append(f'<text x="{nx+105}" y="376" text-anchor="middle" font-size="11" fill="#94a3b8">NVLink inside the server</text>')
    o.append('<text x="480" y="428" text-anchor="middle" font-size="12" fill="#94a3b8">GPU 1 of every server connects to rail 1, GPU 2 to rail 2, and so on. Every leaf connects to every spine.</text>')
    o.append('</g></svg>')
    return ''.join(o)


# =================================================================== HUB
def hub():
    b = hero((HOME, ("Solutions", "/solutions"), ("AI infrastructure", None)), 'AI infrastructure and GPU cloud',
             'GPU clusters that are busy, not waiting',
             'GPUs are the most expensive part of an AI platform, and also the easiest to waste. They sit idle when the network is too slow, when storage cannot feed them data, or when the data centre cannot power and cool them. We design the whole stack around the GPUs: servers, fabric, storage, scheduling, power and cooling.',
             actions=[('Book a GPU sizing review', '/contact'), ('How many GPUs do I need?', '#gpucalc')])
    b += sec('''
            <span class="vk-eyebrow">What usually goes wrong</span>
            <h2>Why GPU projects disappoint</h2>
            <div class="vk-grid" style="margin-top:22px">
                <div class="vk-card"><h3>The data centre is not ready</h3><p class="vk-muted">One 8-GPU server draws about 10 kW. Many enterprise racks are built for 5 to 10 kW in total. The servers arrive and there is nowhere to plug them in.</p></div>
                <div class="vk-card"><h3>GPUs wait on the network</h3><p class="vk-muted">Training across servers exchanges data after every step. On ordinary data-centre networking, GPUs spend much of their time waiting.</p></div>
                <div class="vk-card"><h3>Storage cannot keep up</h3><p class="vk-muted">Loading data and writing checkpoints on general-purpose storage leaves expensive GPUs idle for minutes at a time.</p></div>
                <div class="vk-card"><h3>Nobody can see utilisation</h3><p class="vk-muted">Without GPU-aware scheduling and monitoring, shared clusters run well below capacity while teams queue for access.</p></div>
            </div>''')
    b += sec('''
            <span class="vk-eyebrow">Try it</span>
            <h2>How many GPUs do I need?</h2>
            <p class="vk-prose">Pick a model size and what you want to do with it. The estimate shows GPU memory, number of GPUs and servers, and roughly how much power they draw.</p>
            <div class="vk-tool vk-gpucalc"></div>
            <noscript><p class="vk-muted">This calculator needs JavaScript.</p></noscript>''', sid='gpucalc')
    b += sec('<span class="vk-eyebrow">The building blocks</span><h2>Six layers of a GPU platform</h2>' + table(
        ['Layer', 'What it is', 'What goes wrong if it is weak'],
        [['GPU servers', '8-GPU servers (HGX H100, H200 and similar), or PCIe servers with L40S-class GPUs for lighter work', 'Wrong GPU for the job: paying for training-class GPUs to serve small models, or the reverse'],
         ['<a href="/solutions/ai-infra/ai-network-fabric">GPU fabric</a>', 'A dedicated network between GPUs, usually 400 Gb/s per GPU over InfiniBand or RoCE Ethernet', 'Multi-server training runs at a fraction of its potential speed'],
         ['<a href="/solutions/ai-infra/ai-storage">Storage</a>', 'A fast parallel file system for datasets and checkpoints, plus object storage for raw data', 'GPUs idle while data loads or checkpoints write'],
         ['Scheduling', 'Slurm for training, Kubernetes with the NVIDIA GPU Operator for serving, or both', 'Queues, idle GPUs and arguments about who gets access'],
         ['Monitoring', 'GPU health and utilisation (DCGM), job metrics and cost per team', 'Failing GPUs and wasted capacity go unnoticed'],
         ['<a href="/solutions/ai-infra/power-and-cooling">Power and cooling</a>', 'High-density racks, often 30 kW or more, with rear-door or liquid cooling', 'The cluster cannot be installed, or runs throttled because it overheats']]), sid='layers')
    cards = [('gpu-training-cluster', 'Training cluster', 'How a multi-server training cluster is laid out, with an animated job that survives a node failure.'),
             ('gpu-inference-platform', 'Inference platform', 'Serving models to users: GPU choice, model servers, sharing GPUs and scaling.'),
             ('ai-network-fabric', 'GPU network fabric', 'InfiniBand or Ethernet, rail-optimised design, and how many switches you need.'),
             ('ai-storage', 'Storage for AI', 'Parallel file systems, checkpoint sizes and how fast storage really needs to be.'),
             ('power-and-cooling', 'Power and cooling', 'kW per server and per rack, air vs liquid cooling, and checking your data centre.')]
    c = ''.join(f'<a class="vk-card" href="/solutions/ai-infra/{s}"><h3>{t}</h3><p>{d}</p><span class="vk-go">Read the guide &rarr;</span></a>' for s, t, d in cards)
    c += '<a class="vk-card" href="/use_cases/private-llm-gpu-platform"><h3>Use case: private LLM platform</h3><p>An illustrative scenario: 32 GPUs for inference and fine-tuning, sized end to end.</p><span class="vk-go">Read the use case &rarr;</span></a>'
    c += '<a class="vk-card" href="/solutions/ai-infra/faq"><h3>GPU questions, answered</h3><p>Buy or rent, H100 vs H200 vs L40S, lead times, InfiniBand and more.</p><span class="vk-go">Read the FAQ &rarr;</span></a>'
    b += sec(f'<span class="vk-eyebrow">Go deeper</span><h2>Guides and examples</h2><div class="vk-grid" style="margin-top:22px">{c}</div><p class="vk-muted vk-small" style="margin-top:18px">For the full technical reference, see the <a href="/solutions/master_gpu-cluster">GPU cluster whitepaper</a>.</p>')
    b += sec('<span class="vk-eyebrow">Ways to get GPUs</span><h2>Buy, host or rent</h2>' + table(['Option', 'Good for', 'Trade-off'],
        [['Buy and host in your own data centre', 'Steady, long-term use; data that must stay on your premises', 'Large upfront cost, lead times, and your data centre must handle the power'],
         ['Buy and place in a colocation facility', 'Same as above when your own data centre cannot take the power density', 'Colocation contract and remote hands; still a capital purchase'],
         ['Rent from a GPU cloud', 'Short projects, experiments, bursts of training', 'Highest cost per GPU-hour over time; capacity can be limited at busy times']]) +
        '<p class="vk-small vk-muted">Many organisations start in a GPU cloud to learn their real usage, then buy for the steady part.</p>')
    b += sec('<span class="vk-eyebrow">How we work</span><h2>How a GPU engagement runs</h2>' + steps([
        '<strong>Workload first.</strong> Which models, training or inference, how many users, what latency. This decides everything else.',
        '<strong>Sizing.</strong> GPUs, servers, fabric, storage and software, with the assumptions written down.',
        '<strong>Data-centre readiness.</strong> Power per rack, cooling, floor loading and cabling, checked before anything is ordered.',
        '<strong>Bill of materials.</strong> Vendor-neutral, with alternatives where lead times or budget require them.',
        '<strong>Build and burn-in.</strong> Installation, fabric validation and stress tests before users get access.',
        '<strong>Handover.</strong> Scheduler, monitoring and runbooks in place, with your team trained to run them.']), prose=True)
    b += CTA
    page('portfolio/ai-gpu-cloud.html', 'AI Infrastructure and GPU Clusters: Sizing, Fabric, Storage, Power | Vakratron Systems',
         'Design GPU clusters that stay busy: GPU sizing calculator, training and inference platforms, InfiniBand and RoCE fabrics, AI storage, and data-centre power and cooling.', b, scripts=SCRIPTS)


# =================================================================== TRAINING CLUSTER
def training():
    d = dict(panels=('GPU compute', 'Scheduling, storage and monitoring'), rows=4, nodes={
        'users': N('G', title='Data scientists and pipelines', sub='submit training jobs', style='global', x=370, w=220),
        'n1': N('P', 0, 'l', 'GPU servers 1-2', '8x H100 or H200 each'), 'n2': N('P', 0, 'r', 'GPU servers 3-4', '8x H100 or H200 each'),
        'nvl': N('P', 1, title='NVLink and NVSwitch', sub='GPU-to-GPU inside each server'),
        'fab': N('P', 2, title='Compute fabric', sub='400 Gb/s per GPU, InfiniBand or RoCE'),
        'nic': N('P', 3, title='Storage and management networks', sub='kept separate from the compute fabric'),
        'sch': N('D', 0, title='Scheduler', sub='Slurm, or Kubernetes with GPU Operator'),
        'pfs': N('D', 1, title='Parallel file system', sub='datasets and checkpoints'),
        'obj': N('D', 2, title='Object storage', sub='raw data and model registry'),
        'mon': N('D', 3, title='Monitoring', sub='DCGM, Prometheus, Grafana'),
        'pwr': N('B', title='Power and cooling', sub='~10 kW per 8-GPU server', style='witness', x=60, w=300),
    }, flows=[F('users', 'D', 'traffic'), F('sch', 'n2', 'deploy', 1), F('nic', 'pfs', 'bi', 2), F('obj', 'pfs', 'batch', 3)])
    b = guide_hero('gpu-training-cluster', 'GPU training cluster',
                   'Training a model across several GPU servers turns them into one machine: every GPU works on its own slice of data, then all of them share results before the next step. That only works if the servers, the fabric between them and the storage behind them are designed together.',
                   [('Typical building block', '8-GPU server'), ('GPU fabric', '400 Gb/s per GPU'), ('Scheduler', 'Slurm or Kubernetes'), ('Must have', 'Regular checkpoints')], 'Training cluster')
    b += sec('''
            <span class="vk-eyebrow">See it working</span>
            <h2>A training job, and what happens when a server fails</h2>
            <p class="vk-prose">Watch the cycle: load data (storage lights up), compute (GPUs light up), synchronise (fabric lights up). Then fail a node. Because every GPU depends on every other GPU at each step, the whole job stops and restarts from the last checkpoint. Try different checkpoint intervals and compare how much work is lost.</p>
            <div class="vk-tool vk-trainsim"></div>
            <noscript><p class="vk-muted">This simulation needs JavaScript.</p></noscript>''')
    b += sec('<span class="vk-eyebrow">Reference architecture</span><h2>How the pieces fit together</h2>' + figure(d, 'GPU training cluster reference architecture',
        'Numbered lines show the main flows. Compute, storage and management traffic each have their own network.',
        [('1', 'Scheduling', 'The scheduler places each job on whole servers, so GPUs that need to talk are close together on the fabric.'),
         ('', 'Inside a server', 'NVLink and NVSwitch connect the 8 GPUs inside a server at very high speed. Most communication stays here when a job fits in one server.'),
         ('', 'Between servers', 'The compute fabric gives each GPU its own 400 Gb/s port. This is what lets 32 or 256 GPUs train as one.'),
         ('2', 'Data and checkpoints', 'Training data is read from, and checkpoints are written to, a parallel file system over a separate storage network.'),
         ('3', 'Staging', 'Raw data and finished models live in cheaper object storage and are staged to the fast tier when needed.'),
         ('', 'Monitoring', 'GPU temperature, errors and utilisation are tracked per GPU, because one failing GPU slows or stops the whole job.')]))
    b += sec('<h2>Getting it right</h2>' + ul([
        '<strong>Size checkpoints, not just storage capacity.</strong> A checkpoint of a 70-billion-parameter model with optimizer state is around 1 TB. If writing it takes 10 minutes, GPUs are idle for those 10 minutes every time.',
        '<strong>Plan for failure.</strong> In large clusters, a GPU, cable or server will fail during long runs. Checkpoint often enough that a failure costs minutes, not days, and keep a spare server ready.',
        '<strong>Burn in before handover.</strong> Run stress tests and fabric bandwidth tests (such as NCCL tests) on every server. Weak links found later cost much more.',
        '<strong>Keep the fabric only for GPUs.</strong> Storage and management traffic on the compute fabric slows training in ways that are hard to diagnose.',
        '<strong>Choose the scheduler for how people work.</strong> Research teams used to batch jobs often prefer Slurm. Platform teams running mixed workloads lean towards Kubernetes. Some clusters run both.']), prose=True)
    b += sec('<h2>Typical tools</h2>' + table(['Layer', 'Common choices'],
        [['Servers', 'NVIDIA HGX H100, H200 or B200-based servers from major OEMs; DGX systems'],
         ['Scheduling', 'Slurm, Kubernetes with NVIDIA GPU Operator, Run:ai-style quota management'],
         ['Communication', 'NCCL over InfiniBand or RoCE'], ['Frameworks', 'PyTorch with FSDP or DeepSpeed, NVIDIA NeMo'],
         ['Monitoring', 'NVIDIA DCGM exporter, Prometheus, Grafana']]))
    b += more('gpu-training-cluster') + CTA
    page('solutions/ai-infra/gpu-training-cluster.html', 'GPU Training Cluster Architecture: Servers, Fabric, Storage, Checkpoints | Vakratron Systems',
         'How a multi-server GPU training cluster works, with an animated job that survives a node failure: 8-GPU servers, NVLink, 400 Gb/s fabric, parallel storage, scheduling and checkpoints.', b, scripts=SCRIPTS)


# =================================================================== INFERENCE
def inference():
    d = dict(panels=('Serving layer', 'Platform'), rows=4, nodes={
        'users': N('G', title='Users and applications', sub='chat, search, internal tools', style='global', x=370, w=220),
        'gw': N('P', 0, title='API gateway', sub='sign-in, rate limits, usage per team'),
        'rt': N('P', 1, title='Model router', sub='sends each request to the right model'),
        'ms': N('P', 2, title='Model servers', sub='70B on 2-4 GPUs, 8B on a GPU slice'),
        'as': N('P', 3, title='Autoscaler', sub='adds replicas when queues grow'),
        'obs': N('D', 0, title='Monitoring', sub='latency, tokens per second, cost per team'),
        'reg': N('D', 1, title='Model registry', sub='approved, versioned models'),
        'pool': N('D', 2, title='GPU servers', sub='H100 / H200 for large, L40S for small'),
        'k8s': N('D', 3, title='Kubernetes with GPU Operator', sub='drivers, GPU sharing, scheduling'),
    }, flows=[F('users', 'P', 'traffic'), F('rt', 'ms', 'stream', 1), F('reg', 'rt', 'batch', 2), F('ms', 'pool', 'bi'), F('as', 'k8s', 'deploy', 3), F('gw', 'obs', 'hb', 4)])
    b = guide_hero('gpu-inference-platform', 'GPU inference platform',
                   'Inference is where a model meets its users, and where most of the GPU budget ends up over time. The goals are different from training: steady low latency, many users at once, and as many requests per GPU as possible without making anyone wait.',
                   [('Measure in', 'Tokens per second, latency'), ('Model servers', 'vLLM, Triton, TensorRT-LLM'), ('Share GPUs with', 'MIG, time-slicing'), ('Scales on', 'Queue depth')], 'Inference platform')
    b += sec('<span class="vk-eyebrow">Reference architecture</span><h2>How requests are served</h2>' + figure(d, 'GPU inference platform reference architecture',
        'Numbered lines show the main flows from a user request to a GPU and back.',
        [('', 'API gateway', 'Every request is signed in, rate-limited and counted per team, so cost can be charged back and one team cannot starve another.'),
         ('1', 'Routing', 'Simple questions go to a small, cheap model. Hard ones go to a large model. This alone can cut GPU needs sharply.'),
         ('2', 'Model registry', 'Only approved, versioned models are served. Rolling back a bad model is a configuration change, not an emergency.'),
         ('3', 'Autoscaling', 'Replicas are added when request queues grow and removed when they shrink, within the GPUs available.'),
         ('4', 'Monitoring', 'Time to first token, tokens per second, GPU utilisation and cost per team, on one dashboard.')]))
    b += sec('<h2>Choosing GPUs for inference</h2>' + table(['Model size', 'Fits on', 'Notes'],
        [['~8B', 'One L40S (48 GB) or a slice of an H100', 'Cheapest to serve. Often good enough for classification, extraction and simple chat.'],
         ['~70B', '2 to 4 x H100 80 GB at 16-bit; 1 to 2 x H100 at 8-bit; 1 x H200 at 8-bit', 'The sweet spot for many enterprise assistants. 8-bit precision usually costs little quality.'],
         ['~400B', 'One full 8-GPU H200 server at 8-bit, or more', 'Rarely needed for enterprise use. Consider whether a 70B model with good retrieval does the job.']]) +
        '<p class="vk-small vk-muted">Memory is only the start. Many concurrent users with long contexts need extra memory for the KV cache. Use the <a href="/portfolio/ai-gpu-cloud#gpucalc">GPU calculator</a> to see the effect.</p>')
    b += sec('<h2>Getting it right</h2>' + ul([
        '<strong>Batch requests.</strong> Model servers such as vLLM serve many users on one GPU by batching continuously. Serving one request at a time wastes most of the GPU.',
        '<strong>Share GPUs for small models.</strong> MIG splits an H100 into up to seven isolated slices. Small models do not need a whole GPU each.',
        '<strong>Quantise with care.</strong> 8-bit weights roughly halve memory with little quality loss for most models. Test 4-bit on your own tasks before relying on it.',
        '<strong>Set latency targets per use case.</strong> A chat assistant needs a fast first token. An overnight document job does not. Size for the strictest case only where it applies.',
        '<strong>Plan capacity for peaks.</strong> Usage often doubles at the start of the working day. Size for the peak hour or set a clear queueing policy.']), prose=True)
    b += sec('<h2>Typical tools</h2>' + table(['Layer', 'Common choices'],
        [['Model servers', 'vLLM, NVIDIA Triton with TensorRT-LLM, Text Generation Inference'],
         ['Platform', 'Kubernetes with NVIDIA GPU Operator, KServe'],
         ['Gateway', 'An API gateway with authentication and per-team quotas'],
         ['Monitoring', 'Prometheus and Grafana, DCGM, request tracing']]))
    b += sec('<p>Connecting a model to your own documents? See <a href="/portfolio/rag-solutions">RAG solutions</a>. Choosing the model itself? See <a href="/portfolio/enterprise-llm">enterprise LLM</a>.</p>', prose=True)
    b += more('gpu-inference-platform') + CTA
    page('solutions/ai-infra/gpu-inference-platform.html', 'GPU Inference Platform: Serving LLMs at Scale | Vakratron Systems',
         'How to serve LLMs to many users efficiently: GPU choice by model size, model servers, routing, GPU sharing with MIG, autoscaling and monitoring.', b, scripts=SCRIPTS)


# =================================================================== FABRIC
def fabric():
    b = guide_hero('ai-network-fabric', 'GPU network fabric',
                   'When a training job spans several servers, the GPUs exchange results after every step. The network that carries this traffic decides whether 32 GPUs behave like 32, or like 12. It is a separate network, built only for GPU-to-GPU traffic.',
                   [('Speed per GPU', '400 Gb/s'), ('Options', 'InfiniBand or RoCE Ethernet'), ('Layout', 'Rail-optimised'), ('Needed for', 'Multi-server training')], 'GPU network fabric')
    b += sec('<span class="vk-eyebrow">How it is wired</span><h2>Rail-optimised design</h2><figure class="vk-fig vk-refarch"><span class="vk-scroll-hint">Scroll sideways to see the whole diagram &rarr;</span><div class="vk-refarch-scroll">' + rail_svg() +
             '</div><figcaption>Each colour is a rail. Traffic between the same-numbered GPUs on different servers crosses just one leaf switch, which keeps latency low and predictable.</figcaption></figure>' +
             ul(['Each GPU has its own network port, so an 8-GPU server has 8 fabric ports: 3.2 Tb/s per server.',
                 'Leaf switches are grouped into rails. GPU 1 of every server goes to rail 1, GPU 2 to rail 2, and so on.',
                 'Every leaf connects to every spine, so any GPU can still reach any other.',
                 'The fabric is non-blocking: as much bandwidth up to the spines as down to the GPUs.']))
    b += sec('<h2>InfiniBand or Ethernet?</h2>' + table(['', 'InfiniBand (NDR 400G)', 'RoCE Ethernet (400G)'],
        [['How it works', 'Purpose-built for HPC, lossless by design', 'Standard Ethernet tuned to be lossless (PFC, ECN)'],
         ['Strengths', 'Proven at large scale for training, predictable performance, simpler to tune', 'Familiar to network teams, wider vendor choice, one technology across the data centre'],
         ['Watch out for', 'Separate skills and tooling, mostly one vendor', 'Needs careful configuration and testing to match InfiniBand under load'],
         ['Usually fits', 'Dedicated training clusters', 'Mixed environments and teams with strong Ethernet skills']]) +
        '<p>Both work. The right choice depends more on your team and your existing network than on benchmark numbers. For inference-only platforms, a high-speed fabric is often not needed at all.</p>')
    b += sec('<h2>How many switches?</h2>' + table(['Cluster size', 'GPU ports', 'Typical fabric'],
        [['4 servers (32 GPUs)', '32 x 400G', 'A single 64-port 400G switch can connect them all, with room to grow'],
         ['16 servers (128 GPUs)', '128 x 400G', 'Rail-optimised leaves plus spines in two tiers'],
         ['32 servers (256 GPUs)', '256 x 400G', 'A standard "scalable unit": 8 rail leaves and a spine layer']]) +
        '<p class="vk-small vk-muted">Based on 64-port 400G switches such as the NVIDIA Quantum-2 family. Cable count and lengths matter as much as switch count: plan the rack layout at the same time.</p>')
    b += sec('<h2>The other networks</h2>' + ul([
        '<strong>Storage network:</strong> 100 to 400 Gb/s Ethernet or InfiniBand to the parallel file system, separate from the GPU fabric.',
        '<strong>In-band management:</strong> ordinary Ethernet for logins, scheduling and software updates.',
        '<strong>Out-of-band management:</strong> a separate network to every server\'s BMC, so failed servers can be reached and restarted.']), prose=True)
    b += more('ai-network-fabric') + CTA
    page('solutions/ai-infra/ai-network-fabric.html', 'GPU Network Fabric: InfiniBand vs RoCE, Rail-Optimised Design | Vakratron Systems',
         'How GPU clusters are networked: 400 Gb/s per GPU, rail-optimised leaf and spine design, InfiniBand vs RoCE Ethernet, switch counts and the other networks a cluster needs.', b)


# =================================================================== STORAGE
def storage():
    b = guide_hero('ai-storage', 'Storage for AI',
                   'GPUs can only work as fast as data reaches them. Storage for AI has two jobs: feed training data quickly, and absorb very large checkpoints without stopping the GPUs for long. General-purpose file servers are rarely up to either.',
                   [('Fast tier', 'Parallel file system'), ('Capacity tier', 'Object storage'), ('Biggest writes', 'Checkpoints'), ('Network', 'Separate from GPU fabric')], 'Storage for AI')
    b += sec('<h2>Three tiers</h2>' + table(['Tier', 'Holds', 'Typical technology'],
        [['Local NVMe in each server', 'Scratch space and cached data', 'NVMe drives inside the GPU servers'],
         ['Parallel file system', 'Active datasets and checkpoints', 'Lustre, IBM Storage Scale (GPFS), WEKA, VAST, DDN'],
         ['Object storage', 'Raw data, archives, finished models', 'S3-compatible storage such as Ceph RGW or MinIO']]))
    b += sec('<h2>Checkpoint maths</h2>' + '''
            <p>During training, the full state of the model is saved regularly so a failure does not lose days of work. With mixed-precision training and the Adam optimizer, that state is roughly <strong>16 bytes per parameter</strong>.</p>''' +
        table(['Model', 'Checkpoint size (approx.)', 'Time to write at 10 GB/s', 'At 50 GB/s'],
              [['8B', '~130 GB', '~13 seconds', '~3 seconds'], ['70B', '~1.1 TB', '~2 minutes', '~22 seconds'], ['405B', '~6.5 TB', '~11 minutes', '~2 minutes']]) +
        '<p>Multiply the write time by how often you checkpoint, and you have GPU time spent waiting. That number, more than capacity, is what decides how fast the storage needs to be.</p>', prose=True)
    b += sec('<h2>Getting it right</h2>' + ul([
        '<strong>Size for throughput first, then capacity.</strong> A small, fast tier in front of large, cheap object storage is usually better value than a large fast tier.',
        '<strong>Use asynchronous checkpointing where your framework supports it.</strong> The GPUs carry on while the checkpoint is written in the background.',
        '<strong>Keep many small files out of the fast tier.</strong> Pack datasets into larger shards. Millions of tiny files slow any file system down.',
        '<strong>Back up what matters.</strong> Datasets and final models need backup. Intermediate checkpoints usually do not.']), prose=True)
    b += more('ai-storage') + CTA
    page('solutions/ai-infra/ai-storage.html', 'Storage for AI: Parallel File Systems, Checkpoints and Throughput | Vakratron Systems',
         'How to design storage for GPU clusters: local NVMe, parallel file systems and object storage, checkpoint sizes and write times, and what really decides storage speed.', b)


# =================================================================== POWER
def power():
    b = guide_hero('power-and-cooling', 'Power and cooling for GPU clusters',
                   'This is where many GPU projects stall. Modern GPU servers draw far more power than the racks most data centres were built for, and all of that power becomes heat. Checking the facility early saves months.',
                   [('8-GPU H100 server', 'up to ~10.2 kW'), ('Typical enterprise rack', '5 to 10 kW'), ('GPU racks', '30 to 40 kW+'), ('Above ~40 kW', 'Liquid cooling')], 'Power and cooling')
    b += sec('<h2>Power figures to plan with</h2>' + table(['System', 'Approximate maximum power'],
        [['8-GPU A100 server (DGX A100 class)', '~6.5 kW'], ['8-GPU H100 or H200 server (DGX H100 class)', '~10.2 kW'], ['8-GPU B200 server (DGX B200 class)', '~14.3 kW'],
         ['Rack-scale GB200 NVL72 system', 'around 120 kW per rack, liquid-cooled'], ['Single L40S GPU', '~350 W']]) +
        '<p class="vk-small vk-muted">Vendor maximum figures. Real draw under training load is close to the maximum, so plan with these numbers, not with averages.</p>')
    b += sec('<h2>A quick worked example</h2>' + '''
            <p>Four 8-GPU H100 servers draw about 41 kW. Add network switches, storage and management servers and the total is around 47 kW.</p>
            <ul><li>In a data centre built for 8 kW racks, that is six racks mostly empty, and cooling may still not cope with the hot spots.</li>
            <li>In racks rated for 25 kW with rear-door heat exchangers, it fits in two racks.</li>
            <li>With direct liquid cooling, the same servers can be packed even tighter, but the facility needs water connections to the racks.</li></ul>''', prose=True)
    b += sec('<h2>Cooling options</h2>' + table(['Option', 'Practical rack density', 'Notes'],
        [['Air with hot and cold aisle containment', 'Up to about 20 to 25 kW', 'Works for small clusters if the room has spare cooling'],
         ['Rear-door heat exchangers', 'Roughly 30 to 50 kW', 'Chilled water at the rack door; servers stay air-cooled'],
         ['Direct liquid cooling', '50 kW to 100 kW and more', 'Coolant to the chips; needed for the newest rack-scale systems']]))
    b += sec('<h2>Data-centre readiness checklist</h2>' + ul([
        'Power per rack available, and on which circuits (A and B feeds)',
        'Total spare power and cooling capacity in the room, not just per rack',
        'Floor loading: fully loaded GPU racks are heavy',
        'Chilled water availability if rear-door or liquid cooling is needed',
        'Space for cable trays: a 32-server cluster has hundreds of fabric cables',
        'Lead time for any facility upgrades, which is often longer than for the servers']), prose=True)
    b += more('power-and-cooling') + CTA
    page('solutions/ai-infra/power-and-cooling.html', 'Power and Cooling for GPU Clusters: kW per Rack, Air vs Liquid | Vakratron Systems',
         'Plan power and cooling for GPU clusters: kW per 8-GPU server and per rack, a worked example, air vs rear-door vs direct liquid cooling, and a data-centre readiness checklist.', b)


# =================================================================== FAQ
def faq():
    qa = [('Should we buy GPUs or rent them from a GPU cloud?', '<p>Rent while you learn your real usage, or for short projects. Buy when you have steady, long-term demand, or when data must stay on your premises. Many organisations do both: own the steady base, rent for peaks.</p>'),
          ('H100, H200 or L40S?', '<p>H100 and H200 are built for training and large-model serving; H200 has much more memory (141 GB vs 80 GB), which helps large models and long contexts. L40S is a cheaper PCIe GPU that serves small and mid-size models well but is not designed for multi-server training.</p>'),
          ('Do we need InfiniBand?', '<p>For training across several servers, you need a high-speed GPU fabric: InfiniBand or well-tuned RoCE Ethernet. For inference where each model fits in one server, standard data-centre networking is usually enough.</p>'),
          ('How long do GPU servers take to arrive?', '<p>It varies with demand and model. Lead times of several weeks to a few months are common. Facility upgrades for power and cooling can take longer, so start that check first.</p>'),
          ('Can our existing data centre host a GPU cluster?', '<p>Often only partly. One 8-GPU server draws about 10 kW, more than many enterprise racks are built for. We check power, cooling and floor loading before anything is ordered. See <a href="/solutions/ai-infra/power-and-cooling">power and cooling</a>.</p>'),
          ('How do we keep GPUs busy?', '<p>A scheduler that understands GPUs, quotas per team, GPU sharing (MIG) for small workloads, and monitoring that shows utilisation per team. Clusters without these often run far below capacity.</p>'),
          ('Can we run training and inference on the same cluster?', '<p>Yes, with care. Inference needs steady capacity during working hours; training can use what is left, especially at night. Kubernetes or a scheduler with priorities and pre-emption makes this work.</p>'),
          ('What do you need from us to start?', '<p>The models you plan to use, training or inference, rough user numbers, and where the hardware will live. We will start from that and the data-centre details.</p>')]
    items = ''.join(f'<details><summary>{q}</summary><div>{a}</div></details>' for q, a in qa)
    b = hero((HOME, HUB, ("FAQ", None)), 'AI infrastructure guide', 'GPU and AI infrastructure questions, answered', 'Short answers to the questions we hear most often when organisations plan GPU infrastructure.')
    b += sec(items, prose=True) + more('faq') + CTA
    page('solutions/ai-infra/faq.html', 'GPU and AI Infrastructure FAQ: Buy or Rent, H100 vs H200, InfiniBand, Power | Vakratron Systems',
         'Plain answers on GPU infrastructure: buying vs renting GPUs, H100 vs H200 vs L40S, InfiniBand, lead times, data-centre power, utilisation and mixing training with inference.', b)


# =================================================================== USE CASE
def usecase():
    b = f'''
        <div class="vk-wrap vk-hero">
            {crumb(HOME, HUB, ("Use case: private LLM platform", None))}
            <div class="vk-label"><span>Illustrative scenario</span></div>
            <h1>A private LLM platform on 32 GPUs</h1>
            <p class="vk-lead">How we would size a GPU platform for a financial-services group that wants an internal AI assistant for 2,000 staff, plus regular fine-tuning, without sending data outside its own infrastructure.</p>
            <div class="vk-note"><p class="vk-small">This is a composite example built from requirements common in regulated enterprises. It is not a specific client engagement, and the figures are design estimates for the scenario, not measured results.</p></div>
            <div class="vk-facts">
                <div class="vk-fact"><span class="k">Users</span><span class="v">~2,000 staff</span></div>
                <div class="vk-fact"><span class="k">Models</span><span class="v">70B and 8B class</span></div>
                <div class="vk-fact"><span class="k">GPUs</span><span class="v">32 x H200</span></div>
                <div class="vk-fact"><span class="k">Power</span><span class="v">~47 kW, 2 racks</span></div>
            </div>
        </div>'''
    b += sec('''<span class="vk-eyebrow">The situation</span><h2>Useful AI, but no data leaving the building</h2>
            <p>The group wanted an assistant that could answer questions on policies, products and internal procedures, and summarise long documents. Its risk team ruled out sending customer or internal data to an external AI service. It also wanted to fine-tune models on its own terminology every quarter.</p>''', prose=True)
    b += sec('''<span class="vk-eyebrow">Sizing</span><h2>Working out how many GPUs</h2>''' + table(['Workload', 'Assumption', 'GPUs'],
        [['Assistant (70B-class model, 8-bit)', 'Peak 200 people asking at once, up to 8,000 tokens of context each', '8 GPUs: 4 replicas of 2 x H200'],
         ['Quick tasks (8B-class model)', 'Classification, extraction, short answers', '4 GPUs, shared'],
         ['Fine-tuning', 'LoRA on the 70B model, full fine-tune of the 8B model, quarterly', '8 GPUs (one server), idle between runs for burst inference'],
         ['Headroom and failover', 'One server can fail without losing the service', '12 GPUs'],
         ['Total', '', '<strong>32 GPUs in 4 servers</strong>']]) +
        '<p class="vk-small vk-muted">KV cache for 200 users at 8,000 tokens on a 70B-class model at 8-bit is roughly 250 GB, spread across the replicas. H200\'s 141 GB per GPU leaves room for it alongside the weights.</p>')
    b += sec('<span class="vk-eyebrow">The design</span><h2>What gets built</h2>' + table(['Component', 'Design'],
        [['GPU servers', '4 x 8-GPU H200 servers'],
         ['GPU fabric', 'One 64-port 400G InfiniBand switch: 32 ports used, room to double'],
         ['Front-end and storage network', '100/200 Gb/s Ethernet, separate from the GPU fabric'],
         ['Storage', 'About 300 TB all-flash parallel file system, plus object storage for documents and models'],
         ['Platform', 'Kubernetes with GPU Operator, vLLM model servers, API gateway with per-department quotas'],
         ['Facility', '~47 kW across 2 racks at ~24 kW each, with rear-door heat exchangers']]))
    b += sec('''<span class="vk-eyebrow">Trade-offs</span><h2>What we would flag</h2>''' + ul([
        '<strong>H200 costs more per GPU than H100.</strong> Its extra memory means fewer GPUs per model replica, so the total can come out similar. Compare complete configurations, not unit prices.',
        '<strong>The data centre decides the timeline.</strong> If the facility needs new power or chilled water for two 24 kW racks, that work starts before the order is placed.',
        '<strong>Peak usage drives cost.</strong> Most demand comes in the first hours of the working day. A short queue at peak can save several GPUs.',
        '<strong>The model is only half of it.</strong> Answers about internal policies need good retrieval from internal documents. See <a href="/portfolio/rag-solutions">RAG solutions</a>.']), prose=True)
    b += CTA
    page('use_cases/private-llm-gpu-platform.html', 'Use Case: Sizing a Private LLM Platform on 32 GPUs | Vakratron Systems',
         'An illustrative scenario: sizing a private LLM platform for 2,000 staff with inference and fine-tuning on 32 H200 GPUs, including fabric, storage, power and trade-offs.', b)


if __name__ == '__main__':
    hub(); training(); inference(); fabric(); storage(); power(); faq(); usecase()
