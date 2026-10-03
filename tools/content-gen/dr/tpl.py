import os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'views')
def page(rel, title, desc, body):
    url = '/' + rel[:-5]
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <link rel="canonical" href="https://vakratronsys.com{url}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="/style.css">
    <link rel="stylesheet" href="/vk-content.css">
</head>
<body>
    <header></header>

    <main class="vk">
{body}
    </main>

    <footer></footer>
    <script src="/vakra-loader.js"></script>
</body>
</html>
'''
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8', newline='\n').write(html)
    print('wrote', rel, len(html))

CTA = '''
        <div class="vk-sec"><div class="vk-wrap">
            <div class="vk-cta">
                <h2>Not sure where your DR stands?</h2>
                <p class="vk-muted">Send us your application list and a short note on how backups work today. We will come back with a plain gap review: which systems are exposed, what a realistic recovery time looks like, and what it would take to close the gap.</p>
                <div class="vk-actions">
                    <a class="vk-btn primary" href="/contact">Book a DR review</a>
                    <a class="vk-btn" href="/portfolio/dr-solutions">Back to DR overview</a>
                </div>
            </div>
        </div></div>'''

def crumb(*items):
    parts = []
    for label, href in items:
        parts.append(f'<a href="{href}">{label}</a>' if href else f'<span>{label}</span>')
    return '<div class="vk-crumb">' + ' <span>/</span> '.join(parts) + '</div>'
