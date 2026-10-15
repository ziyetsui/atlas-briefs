# Re-host the media of every note a brief shows (examples, teardown heroes, law examples) on R2, so videos play and
# image posts flip in the page after the signed 小红书 URLs expire (~1–2 days). specs/0004 §4.
# Usage: python3 scripts/jg_media.py <slug> [--lib data/library-jg]
#   reads site/<slug>/data.js (run atlas_build.py first), downloads cover / images / video from the library's `extra`,
#   uploads to R2 atlas-media/atlas/briefs/<slug>/<note id>/, writes site/<slug>/media.json; then rerun atlas_build.py.
import json, os, subprocess, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
slug = sys.argv[1]
lib = sys.argv[sys.argv.index('--lib') + 1] if '--lib' in sys.argv else os.path.join(ROOT, 'data/library-jg')
BUCKET, ACCOUNT = 'atlas-media', '15bb2d33e765847ba3b774014e024dc5'
PUBLIC = 'https://pub-7f941743d5f647de9b5b927cda49ff7d.r2.dev'
CACHE = os.path.join(ROOT, 'data/fetch/jg-media', slug)

src = open(os.path.join(ROOT, 'site', slug, 'data.js')).read()
notes = json.loads(src[src.index('=') + 1:].rstrip().rstrip(';'))['notes']
items = {i['id']: i for i in json.load(open(os.path.join(lib, 'items.json')))}
out_path = os.path.join(ROOT, 'site', slug, 'media.json')
media = json.load(open(out_path)) if os.path.exists(out_path) else {}

def fetch(url, path):
    if not os.path.exists(path):
        req = urllib.request.Request(url.replace('http://', 'https://'), headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=120) as r, open(path, 'wb') as f: f.write(r.read())
    return path

def put(path, key, ctype):
    subprocess.run(['npx', '--no-install', 'wrangler', 'r2', 'object', 'put', f'{BUCKET}/{key}', '--file', path,
                    '--content-type', ctype, '--remote'], check=True, capture_output=True, env=dict(os.environ, CLOUDFLARE_ACCOUNT_ID=ACCOUNT))
    return f'{PUBLIC}/{key}'

for nid in notes:
    if nid in media or nid not in items: continue
    x = items[nid]['extra']
    d = os.path.join(CACHE, nid); os.makedirs(d, exist_ok=True)
    base = f'atlas/briefs/{slug}/{nid}'
    m = {'images': []}
    for k, im in enumerate(x['srcImages']):
        p = fetch(im['src'], os.path.join(d, f'{k}.jpg'))
        m['images'].append({'src': put(p, f'{base}/{k}.jpg', 'image/jpeg'), 'w': im['w'], 'h': im['h']})
    m['img'] = m['images'][0]['src'] if m['images'] else None
    if x.get('srcVideo'):
        p = fetch(x['srcVideo']['src'], os.path.join(d, 'video.mp4'))
        m['video'] = {'src': put(p, f'{base}/video.mp4', 'video/mp4'), 'poster': m['img'], 'durationSec': x['srcVideo']['durationSec']}
        m.pop('images')  # a video note opens the player, not a gallery
    media[nid] = m
    json.dump(media, open(out_path, 'w'), ensure_ascii=False, indent=1)
    print(f"{nid[:8]} {'video' if 'video' in m else str(len(m['images'])) + ' images'}", flush=True)
print(f'{len(media)} notes in {os.path.relpath(out_path, ROOT)}')
