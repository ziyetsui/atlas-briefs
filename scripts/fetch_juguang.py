# Pull notes from 聚光 内容广场 (ad.xiaohongshu.com/microapp/creativity/inspire) through the logged-in Chrome.
# Calls the page's own search API (search_note_v2) in the page's main world, signed with window._webmsxyw,
# via the OpenCLI browser bridge (session "jz", tab already on the inspire page).
# Usage: python3 scripts/fetch_juguang.py <queries.json> [--pages N]
#   queries.json: [{"name": "...", "body": {"bizType": 2, "nd": "30", "orderBy": "premium_read_num", ...}}, ...]
# Output: data/fetch/jg/<name>.json  (one file per query: every page's noteList + the request body)
import json, os, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'data/fetch/jg')
PAUSE = 1.5
SESSION = os.environ.get('JG_SESSION', 'jz')  # OpenCLI browser session; run a second worker with another session + --reverse

MW = r"""(async()=>{document.documentElement.removeAttribute('data-mw');const s=document.createElement('script');
s.textContent='(async()=>{const R=x=>document.documentElement.setAttribute("data-mw",x);try{'+%s+'}catch(e){R("ERR "+e)}})()';
document.documentElement.appendChild(s);s.remove();
for(let i=0;i<200;i++){const v=document.documentElement.getAttribute('data-mw');if(v!==null)return v;await new Promise(r=>setTimeout(r,500))}return 'timeout'})()"""

def search_all(body, pages):
    # one round trip: the page loops over pageNum itself, stopping at the list's end
    js = ("const p='/api/pgy_leona/content_square/search_note_v2';const base=%s;const out=[];"
          "for(let n=1;n<=%d;n++){const b=JSON.stringify(Object.assign({},base,{pageNum:n}));"
          "const sg=window._webmsxyw(p,JSON.parse(b));"
          "const r=await fetch('https://edith.xiaohongshu.com'+p,{method:'POST',credentials:'include',"
          "headers:{'content-type':'application/json;charset=UTF-8','x-s':sg['X-s'],'x-t':String(sg['X-t'])},body:b});"
          "const d=await r.json();if(!d.success){out.push({page:n,error:d.msg});break}"
          "const L=d.data.noteList||[];out.push({page:n,total:d.data.total,notes:L});"
          "if(L.length<base.pageSize||n*base.pageSize>=(d.data.total||0))break;"
          "await new Promise(r=>setTimeout(r,800))}"
          "R(JSON.stringify(out))") % (json.dumps(body, ensure_ascii=False), pages)
    r = subprocess.run(['opencli', 'browser', SESSION, 'eval', MW % json.dumps(js)], capture_output=True, text=True, timeout=120)
    out = r.stdout.strip().split('\n\n  Update available')[0].strip()
    try:
        res = json.loads(out)
    except ValueError:
        res = None
    return res if isinstance(res, list) else [{'page': 1, 'error': out[:300]}]  # tab navigated away, signer missing …

def run(q, pages):
    path = os.path.join(OUT, q['name'] + '.json')
    if os.path.exists(path): return
    base = dict({'searchWord': '', 'pageSize': 34, 'platform': 2, 'sort': 'desc'}, **q['body'])
    res = search_all(base, pages)
    got = [x for x in res if 'notes' in x]
    for x in res:
        if 'error' in x: print(f"  {q['name']} p{x['page']}: {x['error']}", flush=True)
    if not got: return
    total = got[-1]['total']
    json.dump({'query': q, 'body': base, 'total': total, 'pages': got}, open(path, 'w'), ensure_ascii=False)
    print(f"{q['name']}: total {total}, got {sum(len(x['notes']) for x in got)}", flush=True)
    time.sleep(PAUSE)

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    pages = int(sys.argv[sys.argv.index('--pages') + 1]) if '--pages' in sys.argv else 10
    Q = json.load(open(sys.argv[1]))
    for q in (Q[::-1] if '--reverse' in sys.argv else Q): run(q, pages)
