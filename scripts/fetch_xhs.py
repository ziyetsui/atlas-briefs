# Resolve signed 小红书 URLs (xsec_token) for brief notes, then download their media with OpenCLI.
# The library only stores bare /explore/<id> links, which 小红书 now refuses. A signed link comes from:
#   1. searching the note title, 2. searching the account name → that author's profile listing.
# Usage:
#   python3 scripts/fetch_xhs.py resolve [--limit N]   # fills data/fetch/signed.json
#   python3 scripts/fetch_xhs.py retry                 # second pass on misses: deeper profiles, fuzzy author match
#   python3 scripts/fetch_xhs.py download              # media → data/fetch/media/<id>/
#   python3 scripts/fetch_xhs.py grab                  # same, read from the page in a browser session (when download is rejected)
#   python3 scripts/fetch_xhs.py upload                # → R2 atlas-media/atlas/briefs/media/<id>/, writes data/fetch/media.json
import json, os, re, subprocess, sys, time
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FETCH = os.path.join(ROOT, 'data/fetch')
TARGETS = json.load(open(os.path.join(FETCH, 'targets.json')))
SIGNED_PATH = os.path.join(FETCH, 'signed.json')
signed = json.load(open(SIGNED_PATH)) if os.path.exists(SIGNED_PATH) else {}
PAUSE = 3  # seconds between requests; 小红书 throttles bursts

def cli(*args, timeout=120):
    r = subprocess.run(['opencli', 'xiaohongshu', *args, '-f', 'json'], capture_output=True, text=True, timeout=timeout)
    out = r.stdout
    start = min([i for i in (out.find('['), out.find('{')) if i >= 0], default=-1)
    if start < 0: return None
    try:
        return json.JSONDecoder().raw_decode(out[start:])[0]  # opencli appends an update notice after the JSON
    except ValueError:
        return None

def find(results, nid):
    for x in results or []:
        u = x.get('url') or ''
        if nid in u and 'xsec_token=' in u:
            return u.replace('/search_result/', '/explore/')
    return None

def core(name):  # account names often carry emoji / brackets: compare on the plain characters
    return re.sub(r'[^\w\u4e00-\u9fff]', '', re.sub(r'[（(].*?[）)]', '', name))

def resolve(limit=None, retry=False):
    todo = [t for t in TARGETS if not (t['type'] == '视频' and t['hasVideo'])
            and (t['id'] not in signed if not retry else (t['id'] in signed and not signed[t['id']]['url']))]
    depth = '200' if retry else '60'
    seen_users = {}
    for k, t in enumerate(todo[:limit]):
        nid, how = t['id'], None
        q = re.sub(r'[#\[\]【】|｜!！?？~～✨🔥]', ' ', t['title']).strip()[:24]
        url = find(cli('search', q), nid); how = 'title' if url else None
        time.sleep(PAUSE)
        if not url:
            res = cli('search', t['account']) or []
            time.sleep(PAUSE)
            want = core(t['account'])
            uids = {re.search(r'profile/(\w+)', x.get('author_url', '')).group(1)
                    for x in res if re.search(r'profile/(\w+)', x.get('author_url', ''))
                    and (x.get('author') == t['account'] or (retry and want and (want in core(x.get('author', '')) or core(x.get('author', '')) in want)))}
            for uid in uids:
                notes = seen_users.get(uid) or cli('user', uid, '--limit', depth, timeout=300) or []
                seen_users[uid] = notes
                time.sleep(PAUSE)
                url = find(notes, nid)
                if url: how = 'profile'; break
        signed[nid] = {'url': url, 'how': how}
        json.dump(signed, open(SIGNED_PATH, 'w'), ensure_ascii=False, indent=1)
        print(f"[{k + 1}/{len(todo)}] {'OK ' + how if url else 'miss'}  {t['brief']} {nid[:8]} {t['title'][:20]}", flush=True)
    got = sum(1 for v in signed.values() if v['url'])
    print(f'resolved {got}/{len(signed)}')

def download():
    for t in TARGETS:
        s = signed.get(t['id'])
        if not s or not s['url']: continue
        out = os.path.join(FETCH, 'media', t['id'])
        if os.path.isdir(out) and os.listdir(out): continue
        os.makedirs(out, exist_ok=True)
        r = subprocess.run(['opencli', 'xiaohongshu', 'download', s['url'], '--output', out, '-f', 'json'], capture_output=True, text=True, timeout=300)
        note = subprocess.run(['opencli', 'xiaohongshu', 'note', s['url'], '-f', 'json'], capture_output=True, text=True, timeout=180)
        open(os.path.join(out, 'note.json'), 'w').write(note.stdout)
        print(f"{t['id'][:8]} files={len(os.listdir(out))}", flush=True)
        time.sleep(PAUSE)

# `opencli xiaohongshu download/note` can fail with "Navigation rejected" while the page itself opens fine
# in a browser session. grab() opens the signed link there and reads the note straight from the page state.
STATE_JS = """(()=>{const m=window.__INITIAL_STATE__?.note?.noteDetailMap;const k=m&&Object.keys(m).find(x=>m[x].note&&m[x].note.noteId);
const n=k&&m[k].note;if(!n)return JSON.stringify({err:location.href});const v=n.video?.media?.stream;
const vs=v?[...(v.h264||[]),...(v.h265||[])]:[];
return JSON.stringify({desc:n.desc||'',likes:n.interactInfo?.likedCount,collects:n.interactInfo?.collectedCount,comments:n.interactInfo?.commentCount,
imgs:n.type==='video'?[]:(n.imageList||[]).map(i=>i.urlDefault||i.url),video:vs.length?vs[0].masterUrl:null,poster:(n.imageList||[])[0]?.urlDefault||null})})()"""

def browser(*args, timeout=120):
    r = subprocess.run(['opencli', 'browser', 'atlas', *args], capture_output=True, text=True, timeout=timeout)
    return r.stdout

def grab():
    for t in TARGETS:
        s = signed.get(t['id'])
        out = os.path.join(FETCH, 'media', t['id'])
        if not s or not s['url'] or (os.path.isdir(out) and [f for f in os.listdir(out) if f != 'note.json' and not os.path.isdir(os.path.join(out, f))]): continue
        os.makedirs(out, exist_ok=True)
        browser('open', s['url']); time.sleep(PAUSE)
        raw = browser('eval', STATE_JS)
        try:
            st = json.JSONDecoder().raw_decode(raw[raw.find('{'):])[0]
        except ValueError:
            st = {'err': raw[:200]}
        if st.get('err'):
            print(f"{t['id'][:8]} no note state ({st['err'][:60]})", flush=True); continue
        num = lambda v: str(v or '').replace(',', '')
        json.dump([{'field': 'content', 'value': st['desc']}, {'field': 'likes', 'value': num(st['likes'])},
                   {'field': 'collects', 'value': num(st['collects'])}, {'field': 'comments', 'value': num(st['comments'])}],
                  open(os.path.join(out, 'note.json'), 'w'), ensure_ascii=False)
        get = lambda u, f: subprocess.run(['curl', '-sfL', '--max-time', '300', '-H', 'Referer: https://www.xiaohongshu.com/', '-A', 'Mozilla/5.0', '-o', os.path.join(out, f), u.replace('http://', 'https://')])
        if st['video']:
            get(st['video'], f"{t['id']}.mp4")
            if st['poster']: get(st['poster'], f"{t['id']}_poster.jpg")
        for k, u in enumerate(st['imgs']):
            get(u, f'{k + 1:02d}.webp' if 'webp' in u else f'{k + 1:02d}.jpg')
        print(f"{t['id'][:8]} {'video' if st['video'] else str(len(st['imgs'])) + ' images'}", flush=True)
        time.sleep(PAUSE)

R2_ACCOUNT ='15bb2d33e765847ba3b774014e024dc5'   # the account whose atlas-media bucket already hosts the covers
R2_BUCKET = 'atlas-media'
R2_PUBLIC = 'https://pub-7f941743d5f647de9b5b927cda49ff7d.r2.dev'
R2_PREFIX = 'atlas/briefs/media'
MEDIA_JSON = os.path.join(FETCH, 'media.json')

def put(local, key, ctype):
    env = dict(os.environ, CLOUDFLARE_ACCOUNT_ID=R2_ACCOUNT)
    for attempt in range(3):  # R2 puts occasionally fail transiently
        r = subprocess.run(['npx', '-y', 'wrangler', 'r2', 'object', 'put', f'{R2_BUCKET}/{key}', '--file', local, '--content-type', ctype, '--remote'],
                           capture_output=True, text=True, env=env, timeout=600)
        if r.returncode == 0: return f'{R2_PUBLIC}/{key}'
        time.sleep(5 * (attempt + 1))
    raise RuntimeError(f'R2 put failed for {key}: {r.stderr[-300:]}')

def upload():
    media = json.load(open(MEDIA_JSON)) if os.path.exists(MEDIA_JSON) else {}
    for t in TARGETS:
        d = os.path.join(FETCH, 'media', t['id'])
        if t['id'] in media or not os.path.isdir(d): continue
        sub = os.path.join(d, t['id'])  # opencli download nests files in a folder named after the note
        if os.path.isdir(sub):
            for f in os.listdir(sub): os.replace(os.path.join(sub, f), os.path.join(d, f))
            os.rmdir(sub)
        files = sorted(f for f in os.listdir(d) if f != 'note.json')
        vids = [f for f in files if f.endswith('.mp4')]
        imgs = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        if not vids and not imgs: continue
        m = {}
        try:
            note = {r['field']: r['value'] for r in json.load(open(os.path.join(d, 'note.json')))}
        except Exception:
            note = {}
        if note.get('content'): m['body'] = note['content']
        for k in ('likes', 'collects', 'comments'):
            if str(note.get(k, '')).replace(',', '').isdigit(): m[k] = int(str(note[k]).replace(',', ''))
        key = lambda f: f'{R2_PREFIX}/{t["id"]}/{f}'
        if vids:
            v = os.path.join(d, vids[0])
            dur = float(subprocess.run(['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', '-of', 'csv=p=0', v], capture_output=True, text=True).stdout or 0)
            poster = imgs[0] if imgs else None
            if not poster:  # grab the first frame
                poster = vids[0].replace('.mp4', '_poster.jpg')
                subprocess.run(['ffmpeg', '-y', '-loglevel', 'quiet', '-i', v, '-frames:v', '1', os.path.join(d, poster)])
            m['video'] = {'src': put(v, key(vids[0]), 'video/mp4'), 'poster': put(os.path.join(d, poster), key(poster), 'image/jpeg'), 'durationSec': round(dur)}
        else:
            m['images'] = []
            for f in imgs:
                w, h = Image.open(os.path.join(d, f)).size
                ctype = 'image/png' if f.endswith('.png') else 'image/webp' if f.endswith('.webp') else 'image/jpeg'
                m['images'].append({'src': put(os.path.join(d, f), key(f), ctype), 'w': w, 'h': h})
        media[t['id']] = m
        json.dump(media, open(MEDIA_JSON, 'w'), ensure_ascii=False, indent=1)
        print(f"{t['id'][:8]} {'video' if vids else str(len(imgs)) + ' images'} uploaded", flush=True)

if __name__ == '__main__':
    cmd = sys.argv[1]
    limit = int(sys.argv[sys.argv.index('--limit') + 1]) if '--limit' in sys.argv else None
    {'resolve': lambda: resolve(limit), 'retry': lambda: resolve(limit, retry=True), 'download': download, 'grab': grab, 'upload': upload}[cmd]()
