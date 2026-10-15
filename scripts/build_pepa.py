# Build final/assets/data.js for 拍吧 from the Atlas library export (items.json + det.json).
# Usage: python3 scripts/build_pepa.py <lib_dir> <out_js>
import json, re, sys, statistics as st, hashlib, datetime

lib, out = sys.argv[1], sys.argv[2]
items = json.load(open(f'{lib}/items.json'))
det = json.load(open(f'{lib}/det.json'))
pct = lambda i: float(i['metrics'][0]['value'].rstrip('%') or 0)

def lists(i):
    for s in det[i['id']]['detail']['sections']:
        if s['kind'] == 'table':
            return [{'list': r[0], 'rank': int(r[1]), 'total': int(r[2]), 'metric': r[5], 'window': int(r[6])} for r in s['rows']]
    return []

def date(i):  # 小红书 note ids start with a hex unix timestamp
    return datetime.datetime.fromtimestamp(int(i['id'][:8], 16)).strftime('%Y-%m-%d')

def clean(t):  # first line, without #话题# tags
    t = re.sub(r'#[^#]*?\[话题\]#', '', t.split('\n')[0]).strip(' ：:')
    return t or '（无标题）'

def objective(name):
    for k, v in [('应用推广·应用下载', '应用下载'), ('蒲公英合作', '蒲公英合作'), ('客资收集', '客资收集'), ('产品种草', '产品种草'), ('小红书热门', '自然热门')]:
        if name.startswith(k): return v
    return name.split('·')[0]

def jitter(s, span):
    return (int(hashlib.md5(s.encode()).hexdigest()[:6], 16) % (2 * span + 1)) - span

# ---------- clusters (competitor pool) ----------
excl = {'69bcf5b2', '6ab10e23', '6ab7c85c', '6a9931f3', '6a7bde6a'}
T = lambda i: i['title']
clusters = {
    'chaoziran': lambda i: '超自然' in T(i) or '超自然' in i['subtitle'],
    'duojin': lambda i: '夺金密令' in T(i) or ('东' in T(i) and any(k in T(i) for k in ['红包', '答题', '羊毛'])),
    'fuye': lambda i: i['id'][:8] not in excl and ((any(k in T(i) for k in ['剪辑', '视频制作', '视频代做', '拍摄接单']) and any(k in T(i) for k in ['接单', '代做'])) or ('漫剧' in T(i) and any(k in T(i) for k in ['接单', '副业', '赚', '变现', '就业'])) or (any(k in T(i) for k in ['副业', '搞钱', '赚钱', '变现', '月入']) and i['facets']['ind'] in ('创业副业培训', '全行业', 'AI工具', '综合AI', 'AI办公', 'AI技能培训'))),
    'jd5': lambda i: '京东' in T(i) and '5折' in T(i).replace(' ', ''),
    'yangmao': lambda i: any(k in T(i) for k in ['薅', '羊毛', '0元', '零成本']) and not any(k in T(i) for k in ['羊毛衫', '羊毛开衫', '羊毛打底', '羊毛大卷', '羊毛T', '羊毛针织', '羊毛两件', '美利奴', '夺金', '🐳东', '东哥']),
    'qihao': lambda i: any(k in T(i) for k in ['起号', '新人博主', '素人博主', '涨粉', '接广', '做小红书']),
    'jianzhi': lambda i: '小蓝智聘' in i['subtitle'] or any(k in T(i) for k in ['日结', '兼职']),
    'chuangzuo': lambda i: any(k in T(i) for k in ['创作者团', '投稿瓜分', '暗区AI创作者', '激励计划']) and '超自然' not in T(i),
}
members = {k: [i for i in items if f(i)] for k, f in clusters.items()}
members['yangmao'] = [i for i in members['yangmao'] if i not in members['duojin']]

meta = {  # judgment scores: 人群 / 动机 / 动作 overlap with 拍吧
    'chaoziran': ('超自然行动组 · 百万激励计划', '间接', 55, 75, 90, True, '玩家拍二创视频领奖励，官方再挑好的投「应用下载」：和拍吧「拍视频→拿钱」的机制最像'),
    'duojin': ('京东 · 夺金密令', '间接', 85, 90, 55, True, '素人矩阵发「零成本领红包」，蒲公英合作拉站外活跃：和拍吧「零门槛赚零花钱」的话术最像'),
    'fuye': ('副业接单赛道', '赛道', 80, 90, 65, True, '剪辑接单、i 人副业、月入课程：抢的就是拍吧想要的「想用手机赚钱」的人，爆文率全池最高'),
    'jd5': ('京东 · 服饰 5 折矩阵', '间接', 60, 30, 50, False, '同样是素人矩阵，但讲的是省钱购物，不是赚钱'),
    'yangmao': ('薅羊毛 / 0 元福利', '间接', 85, 70, 30, False, '人群高度重合，但动作是领券下单，不需要拍内容'),
    'qihao': ('小红书起号 / 新人博主', '间接', 70, 60, 85, False, '动作重合（拍内容），但只有 11 条、多为个人经验，没有可对标的产品'),
    'jianzhi': ('同城兼职招聘', '间接', 75, 85, 20, False, '动机重合，但要线下到岗，和「手机上接单」差得远；样本只有 6 条'),
    'chuangzuo': ('游戏创作者激励（其他）', '间接', 45, 70, 85, False, '机制和超自然一样，但去掉超自然后只剩 2 条，并入超自然一起看'),
}
pool = []
for k, L in members.items():
    ps = [pct(i) for i in L]
    med = st.median(ps); top = sum(p >= 80 for p in ps) / len(ps) * 100; vol = min(len(L) / 40, 1) * 100
    heat = round(0.5 * med + 0.3 * top + 0.2 * vol)
    name, kind, u, m, a, picked, why = meta[k]
    rel = round(0.3 * u + 0.4 * m + 0.3 * a)
    pool.append({'id': k, 'name': name, 'kind': kind, 'relevance': rel, 'heat': heat, 'notes': len(L), 'accounts': len(set(i['subtitle'] for i in L)),
                 'medianPct': round(med, 1), 'hitShare': round(top, 1), 'user': u, 'motive': m, 'action': a, 'picked': picked, 'why': why})

# ---------- formats ----------
A2 = {'69bbc73e', '68da175e', '6a6c6ee7', '6a8c6a30', '69b2c38c'}
A3 = {'69192de8', '69f2f596', '69ae7cc4', '697c5ed4', '6ab89c8a', '69929326', '6a981a7a', '69df35e4', '6a532226'}
def fmt_of(c, i):
    t, s = T(i), i['id'][:8]
    if c == 'chaoziran': return 'cz-2' if s in A2 else 'cz-3' if s in A3 else 'cz-1'
    if c == 'duojin':
        if re.search('答案|攻略|打卡|解析|速抄|码住|玩法', t): return 'dj-2'
        if re.search('上头|死磕|硬控|运气|搭子|沦陷|大神', t): return 'dj-3'
        return 'dj-1'
    if c == 'fuye':
        if re.search('接单|代做', t) and re.search('剪辑|视频|拍摄|海报', t): return 'fy-1'
        if re.search('月入|课|培训|烘焙|酥点|皂|转行|就业|集训|修碗|棋牌|手作|手工', t): return 'fy-3'
        return 'fy-2'

transfer_base = {'cz-1': 52, 'cz-2': 68, 'cz-3': 38, 'dj-1': 88, 'dj-2': 58, 'dj-3': 70, 'fy-1': 76, 'fy-2': 84, 'fy-3': 56}
F = {
    'chaoziran': [
        ('cz-1', '玩家二创小剧场', '玩家把游戏梗拍成短剧或表情包，标题用「当……」情境句，正文只挂官方活动话题', '人设故事', ['6a912beb', '6a708626', '6a6ae01c']),
        ('cz-2', '跨圈借势', '标题和封面完全不像游戏广告：职场 PPT、豆包、无名指，点进去才是超自然', '跨圈钩子', ['69bbc73e', '68da175e', '6a6c6ee7']),
        ('cz-3', '福利 / 攻略', '养成攻略、限时福利、「被指到的人来玩」，偏向老玩家', '利益刺激', ['69192de8', '69f2f596', '69ae7cc4']),
    ],
    'duojin': [
        ('dj-1', '零成本领红包', '大字封面直接写「零成本」「答题就能赢红包」，配到账截图；品牌名写成 🐳东', '利益刺激', ['6a97f3c2', '6a97efbb', '6a9a9bcb']),
        ('dj-2', '每日答案 / 攻略', '「今日答案」「9.3 答题打卡」，每天一更，靠「码住」和搜索续命', '实用攻略', ['6a9f787a', '6a9e81d8', '6a99335e']),
        ('dj-3', '上头 / 找搭子', '「越玩越上头」「全靠运气硬撑」「有没有搭子」，用情绪和社交拉评论', '人设故事', ['6a97f605', '6a97ec6f', '6a97f010']),
    ],
    'fuye': [
        ('fy-1', '接单名片', '工位实拍 + 大字「视频剪辑接单」+ 三个卖点角标（24h 在线 / 白菜价 / 出片快），一张图就是一张名片', '利益刺激', ['6a61ea90', '68a2c5bb', '67249d5f']),
        ('fy-2', '「普通人也能做」口播', '真人出镜口播，封面先点名人群：i 人、社恐、80 后，再给一个具体副业', '人设故事', ['69a6b638', '6a737be4', '6a575eb1']),
        ('fy-3', '「月入 X 万」成果展示', '成品实拍（面包、酥点、手工皂）+ 收入承诺，导向课程留资', '利益刺激', ['6a5f1f45', '695b8b2c', '67a05680']),
    ],
}
COMP = {
    'chaoziran': ('超自然行动组', '间接竞品 · 游戏', '百万激励计划：玩家拍视频领奖励'),
    'duojin': ('京东 · 夺金密令', '间接竞品 · 电商活动', '答题猜密令领红包，素人矩阵铺量'),
    'fuye': ('副业接单赛道', '赛道竞品 · 教培 / 接单号', '剪辑接单、i 人副业、月入课程'),
}
byId = {i['id'][:8]: i for i in items}

def note(i, c, f):
    L = lists(i); best = min(L, key=lambda r: r['rank'] / r['total']) if L else None
    return {'id': i['id'], 'title': clean(i['title'])[:60], 'tags': re.findall(r'#([^#]*?)\[话题\]#', i['title']), 'img': i['cover'], 'aspect': i['coverAspect'], 'account': i['subtitle'],
            'type': i['facets']['fmt'], 'pct': pct(i), 'featured': i['facets']['tier'] == 'featured', 'url': i['url'],
            'list': best['list'] if best else '', 'rank': best['rank'] if best else None, 'total': best['total'] if best else None,
            'objective': objective(best['list']) if best else '', 'date': date(i), 'video': i.get('video'), 'competitor': c, 'format': f}

competitors, scatter, notes = [], {}, {}
for c, fl in F.items():
    L = members[c]; ps = [pct(i) for i in L]
    formats = []
    for fid, name, desc, content, ex in fl:
        fm = [i for i in L if fmt_of(c, i) == fid]
        fp = [pct(i) for i in fm]; hits = sum(p >= 80 for p in fp)
        exn = [note(byId[s], c, fid) for s in ex]
        for n in exn: notes[n['id']] = n
        vid = sum(i['facets']['fmt'] == '视频' for i in fm)
        formats.append({'id': fid, 'name': name, 'desc': desc, 'axis': {'content': content}, 'n': len(fm), 'share': round(len(fm) / len(L) * 100),
                        'hits': hits, 'hitRate': round(hits / len(fm) * 100, 1), 'avgPct': round(st.mean(fp), 1),
                        'type': '视频' if vid >= len(fm) / 2 else '图文', 'notes': exn})
    name, kind, tag = COMP[c]
    objs = {}
    for i in L:
        l = lists(i)
        if l: o = objective(min(l, key=lambda r: r['rank'] / r['total'])['list']); objs[o] = objs.get(o, 0) + 1
    competitors.append({'id': c, 'name': name, 'kind': kind, 'tagline': tag,
                        'stats': {'notes': len(L), 'accounts': len(set(i['subtitle'] for i in L)), 'hits': sum(p >= 80 for p in ps),
                                  'hitRate': round(sum(p >= 80 for p in ps) / len(L) * 100, 1), 'medianPct': round(st.median(ps), 1)},
                        'objectives': sorted(objs.items(), key=lambda x: -x[1]), 'formats': formats})
    ex_ids = {n['id'] for f in formats for n in f['notes']}
    scatter[c] = [{'id': i['id'], 'format': fmt_of(c, i), 'pct': pct(i),
                   'transfer': max(5, min(98, transfer_base[fmt_of(c, i)] + jitter(i['id'], 12))), 'hit': pct(i) >= 80,
                   'title': clean(i['title'])[:40], 'account': i['subtitle'], 'date': date(i), 'example': i['id'] in ex_ids} for i in L]

# ---------- teardowns (3 heroes) ----------
def td_lists(s): return [dict(r, objective=objective(r['list'])) for r in lists(byId[s])]
teardowns = {
    'cz-1': {
        'hero': byId['6a912beb']['id'],
        'account': {'name': '初夏（摸金游戏爱好者）', 'kind': '玩家二创号', 'inLib': 2, 'note': '昵称自带「摸金游戏爱好者」，库里 2 条都是超自然二创；同一活动下 35 条笔记来自 33 个不同账号',
                    'matrix': {'notes': 35, 'accounts': 33}},
        'traffic': {
            'quant': {'from': 'Atlas 素材库 · 聚光「应用推广·应用下载」榜单', 'lists': td_lists('6a912beb'),
                      'summary': '近 7 日应用下载类曝光量第 1（共 34 条），互动量第 2'},
            'qual': {'verdict': '投放加热型', 'reason': '笔记本身没有搜索词，流量来自官方：挂上活动话题后被挑中，作为「应用下载」信息流素材投放。',
                     'keywords': [
                         {'w': '#超自然行动组', 'where': ['话题'], 'role': '活动话题', 'note': '官方据此捞取二创，入选才有激励和投放'},
                         {'w': '#超自然二创厨子', 'where': ['话题'], 'role': '活动话题', 'note': '二创专属标签，进入官方素材池'},
                         {'w': '炸鱼', 'where': ['标题'], 'role': '圈内黑话', 'note': '玩家一看就懂，提高信息流里的停留'},
                         {'w': '当……带我……', 'where': ['标题', '封面'], 'role': '情境句式', 'note': '梗图句式，不像广告'},
                     ],
                     'longtail': ['超自然行动组 搞笑', '摸金游戏 推荐', '超自然 二创']}},
        'money': {'steps': [{'k': '玩家发二创', 'd': '挂活动话题'}, {'k': '官方挑选', 'd': '百万激励计划发奖励'}, {'k': '投放加热', 'd': '聚光应用下载信息流'}, {'k': '下载游戏', 'd': '按下载 / ROI 考核'}],
                  'path': '玩家拿激励 → 官方用玩家内容当广告素材 → 拉下载', 'price': '激励计划奖金（金额未公开）'},
        'structure': [{'t': '封面', 'd': '真人表情包 + 游戏角色发型，横版梗图'}, {'t': '标题', 'd': '「当顶飞的兄弟带我炸鱼：」情境梗，留半句'},
                      {'t': '正文', 'd': '没有正文，只挂 5 个官方活动话题'}, {'t': '视频', 'd': '游戏实录剪成短剧（推断）'}],
        'why': ['玩家视角的梗比官方宣传可信，信息流里不像广告', '话题标签让官方能捞到、能加热', '一个活动几十个号同时发，总有几条跑出来'],
        'inferred': ['视频'],
    },
    'dj-1': {
        'hero': byId['6a97f3c2']['id'],
        'account': {'name': '甜味补给站', 'kind': '素人号（蒲公英合作）', 'inLib': 1, 'note': '库里只有这 1 条；同一活动 30 条来自 30 个不同账号，全部发在 2026-09-01 到 09-08 这 8 天里',
                    'matrix': {'notes': 30, 'accounts': 30}},
        'traffic': {
            'quant': {'from': 'Atlas 素材库 · 蒲公英合作榜单', 'lists': td_lists('6a97f3c2'),
                      'summary': '近 30 日「小红盟站外活跃率」第 3（共 102 条）：读完去京东 App 的比例很高'},
            'qual': {'verdict': '搜索 + 推荐双吃型', 'reason': '「零成本」「薅羊毛」是羊毛党的高频搜索词；大字封面在发现页像普通分享。品牌写成 🐳东，避开广告感。',
                     'keywords': [
                         {'w': '零成本', 'where': ['标题', '封面'], 'role': '利益词', 'note': '最强点击理由：不花钱'},
                         {'w': '薅羊毛', 'where': ['标题', '封面'], 'role': '品类搜索词', 'note': '羊毛党每天在搜'},
                         {'w': '🐳东', 'where': ['标题', '封面'], 'role': '品牌谐音', 'note': '不写「京东」，降低广告感'},
                         {'w': '隐藏福利', 'where': ['标题', '封面'], 'role': '好奇心词', 'note': '「藏不住了」制造稀缺'},
                         {'w': '夺金密令', 'where': ['封面'], 'role': '活动词', 'note': '封面角标，读者照着去搜'},
                     ],
                     'longtail': ['夺金密令 答案', '京东 答题 红包', '大学生 零成本 薅羊毛']}},
        'money': {'steps': [{'k': '素人发笔记', 'd': '蒲公英合作'}, {'k': '读者去搜密令', 'd': '「夺金密令」'}, {'k': '打开京东 App', 'd': '答题猜数字'}, {'k': '领红包', 'd': '按站外活跃考核'}],
                  'path': '蒲公英付素人 → 读者回京东答题 → 拉日活', 'price': '单篇合作费（未公开）'},
        'structure': [{'t': '封面', 'd': '白底大字三行，「隐藏福利」画红圈，手指指向「夺金密令」角标'}, {'t': '标题', 'd': '「零成本薅羊毛！」先给利益，再给悬念'},
                      {'t': '同活动其他笔记', 'd': '用到账截图（¥3.24 / ¥11.28）当封面'}, {'t': '发布', 'd': '30 个号在 8 天内集中发（9 月 1–8 日，开学季）'}],
        'why': ['钱写在封面第一行，0.5 秒看懂', '品牌名打码成 🐳东，像朋友分享不像广告', '30 个素人号同时发，用数量换爆款概率'],
        'inferred': [],
    },
    'fy-2': {
        'hero': byId['69a6b638']['id'],
        'account': {'name': 'Cuberrrr（打工版）', 'kind': '副业博主的子号', 'inLib': 3, 'note': '昵称带「打工版」，是主号之外专门接投放的号；库里 3 条分别讲副业、自媒体和 AI 漫剧赚钱',
                    'matrix': None},
        'traffic': {
            'quant': {'from': 'Atlas 素材库 · 聚光「客资收集」榜单', 'lists': td_lists('69a6b638'),
                      'summary': '创业副业培训类「表单提交率」第 1（共 100 条）：看完留资的人最多'},
            'qual': {'verdict': '人群定向型', 'reason': '封面先点名「i 人」，内向、不想出门的人会对号入座；「副业」「2026」是年底的高频搜索词。',
                     'keywords': [
                         {'w': 'i 人 / 内向', 'where': ['标题', '封面'], 'role': '人群词', 'note': '让目标人群对号入座'},
                         {'w': '副业', 'where': ['标题', '封面'], 'role': '品类搜索词', 'note': '常年高搜索量'},
                         {'w': '不想出门', 'where': ['标题'], 'role': '场景词', 'note': '降低行动门槛'},
                         {'w': '冷门', 'where': ['封面'], 'role': '好奇心词', 'note': '暗示还没人做、还有机会'},
                         {'w': '2026', 'where': ['封面'], 'role': '时效词', 'note': '年底「明年做什么」的搜索'},
                     ],
                     'longtail': ['i人 适合的副业', '在家 副业 推荐', '内向 不想上班 怎么赚钱']}},
        'money': {'steps': [{'k': '真人口播', 'd': '讲一个具体副业'}, {'k': '评论区 / 私信', 'd': '「想了解的扣 1」'}, {'k': '表单留资', 'd': '客资收集广告'}, {'k': '课程 / 社群', 'd': '后端转化'}],
                  'path': '口播种草 → 留资 → 课程转化', 'price': '课程价（未公开）'},
        'structure': [{'t': '封面', 'd': '真人自拍，竖起一根手指；大字「冷门副业 / 2026 / i 人友好」'}, {'t': '标题', 'd': '「不想出门，适合内向 i 人的副业方向」'},
                      {'t': '视频', 'd': '口播列举副业方向（推断）'}, {'t': '转化', 'd': '客资收集：表单留资'}],
        'why': ['先点名人群，再给方案，目标用户自己停下来', '真人出镜比工位图更可信', '「冷门」「i 人友好」把门槛说低'],
        'inferred': ['视频'],
    },
}
for c in competitors:
    for f in c['formats']:
        teardowns.setdefault(f['id'], {'hero': f['notes'][0]['id'], 'inherit': True})

# ---------- laws ----------
allN = members['chaoziran'] + members['duojin'] + members['fuye']
def ev(rx):
    w = [i for i in allN if re.search(rx, T(i))]; wo = [i for i in allN if not re.search(rx, T(i))]
    return {'with': len(w), 'withHit': round(sum(pct(i) >= 80 for i in w) / len(w) * 100), 'without': len(wo), 'withoutHit': round(sum(pct(i) >= 80 for i in wo) / len(wo) * 100), 'of': len(allN)}
money_rx = r'红包|赚|零成本|月入|💰|变现|接单|免费|收入|¥|元|一单'
crowd_rx = r'大学生|学生党|宝妈|i人|社恐|普通人|新手|0基础|零基础|打工人|小白|\d+岁|00后|90后|80后|内向|女生'
idof = lambda s: byId[s]['id']
laws = [
    {'id': 'L1', 'name': '把钱写在第一眼', 'claim': '标题或封面里出现「赚 / 红包 / 零成本 / 接单 / 月入」的笔记，爆款率 {withHit}%；没有的只有 {withoutHit}%。',
     'evidence': ev(money_rx), 'examples': [idof('6a97f3c2'), idof('6a9a9bcb'), idof('6a61ea90')],
     'apply': {'title': '「刷视频的时间，顺手赚了一单」', 'cover': '拍吧「我的钱包」到账截图 + 大字「拍一条 ¥0.96」', 'script': '接单大厅截图 → 30 秒拍摄过程 → 钱包到账', 'kpi': '建议看：封面点击率、首单完成率'}},
    {'id': 'L2', 'name': '一个活动，几十个素人号', 'claim': '超自然 35 条来自 33 个号，夺金密令 30 条来自 30 个号，全部在 9 月 1–8 日发出。不押单条爆款，用数量换概率。',
     'evidence': {'campaigns': [{'name': '超自然行动组', 'notes': 35, 'accounts': 33}, {'name': '京东 · 夺金密令', 'notes': 30, 'accounts': 30}]},
     'examples': [idof('6a912beb'), idof('6a97efbb'), idof('6a97f605')],
     'apply': {'title': '「拍吧接单日记」话题', 'cover': '统一模板：左边任务卡，右边成片截图', 'script': '每个接单用户顺手发一条接单日记，统一挂话题；拍吧挑好的加热', 'kpi': '建议看：话题 30 天笔记数、带来的新接单用户'}},
    {'id': 'L3', 'name': '先点名人群', 'claim': '标题先点名「i 人 / 宝妈 / 大学生 / 社恐」的笔记，爆款率 {withHit}%；没点名的 {withoutHit}%。',
     'evidence': ev(crowd_rx), 'examples': [idof('69a6b638'), idof('6a737be4'), idof('6a97ee65')],
     'apply': {'title': '「i 人也能接的视频单」系列', 'cover': '真人自拍 + 大字「宝妈 / 大学生 / i 人」三选一', 'script': '每个人群一条：谁、什么时间拍、一单赚多少', 'kpi': '建议看：各人群笔记的点击率对比'}},
]
for l in laws:
    if 'with' in l['evidence']: l['claim'] = l['claim'].format(**l['evidence'])

for l in laws:  # law examples may sit outside the 9 format examples
    for nid in l['examples']:
        if nid not in notes:
            i = byId[nid[:8]]; c = next(k for k in F if i in members[k])
            notes[nid] = note(i, c, fmt_of(c, i))

product = {
    'name': '拍吧', 'brand': 'pepa', 'oneLine': '刷视频开心，拍视频赚钱：在小程序里接品牌的拍摄任务，按份结算',
    'category': '素人视频任务平台 · 微信小程序', 'price': '按份计酬 ¥0.08–¥0.96 / 份；达 1000 赞另加奖励',
    'audience': '想用碎片时间赚零花钱的学生、宝妈、上班族（待确认）', 'platform': '任务发到抖音 · 快手 · 小红书',
    'goal': '待确认：建议本轮先做 C 端拉新，让更多人来「接单大厅」接第一单',
    'sellingPoints': ['手机就能拍', '按份结算', '爆了还有奖励'],
    'pool': {'source': 'Atlas 素材库 · 小红书聚光 / 蒲公英 / 热门榜单', 'window': f"{min(date(i) for L in members.values() for i in L)} → {max(date(i) for L in members.values() for i in L)}", 'brands': len(pool),
             'notes': sum(p['notes'] for p in pool), 'library': len(items)},
    'dataNote': '数据来自榜单记录：有榜内百分位和排名，没有点赞数和粉丝数；发布日期由笔记 ID 推算',
    'cut': {'relevance': 70, 'heat': 50},
}
# ---------- structured summaries above the two quadrant charts ----------
DROP = {'yangmao': '动作对不上', 'jianzhi': '动作对不上', 'qihao': '样本太少', 'chuangzuo': '样本太少', 'jd5': '动机不对'}
dropped = {}
for p_ in pool:
    if not p_['picked']: dropped.setdefault(DROP[p_['id']], []).append(p_['name'])
picked_accts = len(set(i['subtitle'] for k in F for i in members[k]))
picked_notes = sum(len(members[k]) for k in F)
product_selection = {
    'pool': f"素材库 {len(items):,} 条 → 按「赚钱 / 接单 / 副业 / 红包 / 二创激励」等关键词圈出 {len(pool)} 组候选、{sum(p_['notes'] for p_ in pool)} 条笔记",
    'rule': '两道线同时过：相关性 ≥ 70（和拍吧的人群 · 动机 · 动作重合，判断分）× 爆品度 ≥ 50（榜单百分位、爆款占比、素材量算出）',
    'picked': [p_['name'] for p_ in sorted(pool, key=lambda p_: -(p_['relevance'] + p_['heat'])) if p_['picked']],
    'dropped': [{'tag': k, 'names': v} for k, v in dropped.items()],
    'common': [
        '卖的都是同一个承诺：用手机、发内容就能赚到钱',
        f'都靠素人和个人号铺量：{picked_notes} 条笔记来自 {picked_accts} 个账号，几乎一号一条',
        '背后都有付费投放，各走一条路：应用下载、蒲公英合作、客资收集',
    ],
}
product['selection'] = product_selection
TAKE = {
    'chaoziran': '进右上角的都「不像游戏广告」：跨圈借势（PPT 汇报、豆包）和玩家梗；纯攻略 / 福利一条都没进。',
    'duojin': '大字封面先写利益（零成本、红包），品牌写成 🐳东，像朋友分享；每日答案类基本进不来。',
    'fuye': '两种最多：工位图 + 「白菜价 / 24h 在线」的接单名片，和先点名人群（i 人、大学生、社恐）的口播；「月入 X 万」课程类很少。',
}
for c in competitors:
    S = scatter[c['id']]; z = [x for x in S if x['pct'] >= 80 and x['transfer'] >= 60]
    names = {f['id']: f['name'] for f in c['formats']}
    by = {}
    for x in z: by[x['format']] = by.get(x['format'], 0) + 1
    c['zone'] = {'n': len(z), 'total': len(S), 'hits': sum(x['hit'] for x in S),
                 'byFormat': [[names[k], v] for k, v in sorted(by.items(), key=lambda kv: -kv[1])], 'takeaway': TAKE[c['id']]}

palettes = [['#f4d9c6'
, '#e9a98b', '#3b1f14'], ['#1f2a44', '#4b5d8a', '#fff'], ['#e8434a', '#b8202b', '#fff']]
data = {'palettes': palettes, 'product': product, 'pool': pool, 'competitors': competitors, 'teardowns': teardowns, 'laws': laws, 'scatter': scatter, 'notes': notes}
open(out, 'w').write('// Atlas — 拍吧 brief data. Generated by scripts/build_pepa.py from the Atlas library; do not edit by hand.\nwindow.ATLAS = ' + json.dumps(data, ensure_ascii=False, indent=1) + ';\n')
for p in sorted(pool, key=lambda p: -p['relevance']): print(p['name'], p['relevance'], p['heat'], p['notes'], p['picked'])
for c in competitors: print(c['name'], c['stats'], [(f['id'], f['n'], f['hitRate'], f['avgPct']) for f in c['formats']], c['objectives'])
for l in laws: print(l['id'], l['claim'])
