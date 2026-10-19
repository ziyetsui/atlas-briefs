# Copy template/brief.html into every site/<slug>/ that has a data.js, as site/<slug>/index.html.
# Usage: python3 scripts/sync_template.py
import hashlib, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
tpl = root / 'template' / 'brief.html'
# Version the shared assets so a returning browser never runs a stale ui.js / base.css against new markup.
html = tpl.read_text()
for a in ('ui.js', 'base.css'):
    v = hashlib.sha1((root / 'site' / 'assets' / a).read_bytes()).hexdigest()[:8]
    html = html.replace(f'../assets/{a}"', f'../assets/{a}?v={v}"')
for d in sorted((root / 'site').iterdir()):
    if d.is_dir() and (d / 'data.js').exists():
        (d / 'index.html').write_text(html)
        print(f'synced {d.relative_to(root)}/index.html')
