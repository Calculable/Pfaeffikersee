"""Check built routes, assets, canonical URLs and the pre-launch indexing lock."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re
from source_html import parse

root = Path(__file__).resolve().parents[1]
dist = root / 'dist'
errors = []
indexable = bool(re.search(r'indexable:\s*true', (root / 'src/site.ts').read_text()))
expected_host = 'www.pfäffikersee.org'.encode('idna').decode()
for page in sorted(dist.rglob('*.html')):
    doc = parse(page.read_text())
    label = str(page.relative_to(dist))
    if len(doc.all(lambda n: n.tag == 'h1')) != 1:
        errors.append(f'{label}: expected exactly one h1')
    robots = doc.all(lambda n: n.tag == 'meta' and n.attrs.get('name') == 'robots')
    expected = 'index, follow' if indexable and page.name != '404.html' else 'noindex, nofollow'
    if not robots or robots[0].attrs.get('content') != expected:
        errors.append(f'{label}: wrong indexing directive')
    canonical = doc.all(lambda n: n.tag == 'link' and n.attrs.get('rel') == 'canonical')
    if not canonical or urlsplit(canonical[0].attrs['href']).hostname != expected_host:
        errors.append(f'{label}: wrong canonical domain')
    if doc.all(lambda n: n.tag == 'iframe'):
        errors.append(f'{label}: external iframe loaded before a click')
    if not indexable and 'gc.zgo.at' in page.read_text():
        errors.append(f'{label}: analytics active before launch')
    for node in doc.all(lambda n: n.tag in ('img', 'script', 'link', 'a')):
        url = node.attrs.get('src') or node.attrs.get('href', '')
        parts = urlsplit(url)
        if not url or url.startswith('#'):
            continue
        if parts.netloc or parts.scheme:
            if node.tag in ('img', 'script') and any(h in parts.netloc for h in ('squarespace', 'sqspcdn')):
                errors.append(f'{label}: Squarespace dependency {url}')
            continue
        target = dist / unquote(parts.path).lstrip('/')
        if not target.is_file() and not (target / 'index.html').is_file():
            errors.append(f'{label}: broken local link {url}')
for source in (root / 'src/content/pages').glob('*/index.md'):
    route = re.search(r'^path: "([^"]+)"', source.read_text(), re.M).group(1)
    if not (dist / route.strip('/') / 'index.html').is_file():
        errors.append(f'Missing route: {route}')
print(f'Checked {len(list(dist.rglob("*.html")))} HTML pages; indexing enabled: {indexable}.')
for error in errors:
    print(error)
raise SystemExit(bool(errors))
