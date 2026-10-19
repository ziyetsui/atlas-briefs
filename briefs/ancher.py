# Ancher（ancher.ai）brief config — judgment only; scripts/atlas_build.py computes the rest.
# Built 2026-10-15 from the Atlas ad-creative library following specs/0003-brief-runbook.md.
import re

T = lambda i: i['title']
TS = lambda i: i['title'] + ' ' + i['subtitle']
VIDEO_GEN = r'Vidu|OiiOii|即梦|可灵|海螺'

PRODUCT = {
    'name': 'Ancher', 'brand': 'ancher.ai', 'oneLine': '把刷到、存下的内容一键变成视频、网页、播客、图片、文章：面向创作者的爆款工具',
    'category': 'AI 知识库 + 多格式内容生成 · Web / App / 浏览器插件', 'price': 'Free $0（100 credits）· Digest $5 / 月 · Pro $15 / 月',
    'audience': '小红书 / 抖音创作者、知识博主、自媒体人（待确认）', 'platform': 'Web · 移动 App · 浏览器插件；可从浏览器、Slack、Telegram、邮件保存',
    'goal': '待确认：建议本轮先做中文创作者拉新，让创作者把收藏夹变成第一条爆款',
    'sellingPoints': ['收藏不吃灰', '一份素材出 5 种成品', '按你的口吻写'],
    'copy': {'transferDef': '创作者能不能照着做、和 Ancher「收藏 → 一键出成品」的叙事是否一致'},
}
CUT = {'relevance': 70, 'heat': 50, 'hit': 80, 'transfer': 60}

# ---------- 1. pool (scores = 人群 / 动机 / 动作 overlap with Ancher, 0–100) ----------
CLUSTERS = {
    'aiflow': {'match': lambda i: bool(re.search(r'(AI|ai).{0,12}(爆款|起号|涨粉|博主|自媒体)|(爆款|起号|涨粉|自媒体).{0,12}(AI|ai)', TS(i))) and not re.search(VIDEO_GEN, TS(i)) and i['id'][:8] != '69e98f42',
               'name': 'AI 自媒体爆款工作流', 'kind': '赛道', 'scores': (90, 90, 80), 'picked': True,
               'why': '教创作者用 AI 复刻爆款、搭工作台、出封面：人群和「做爆款」的动机跟 Ancher 几乎一样'},
    'qianwen': {'match': lambda i: bool(re.search(r'千问|Qwen|通义', TS(i))),
                'name': '千问', 'kind': '直接', 'scores': (70, 65, 80), 'picked': True,
                'why': '「一个 App 什么都能做」的全能 AI，投放量全池最大：和 Ancher「Create anything」正面撞'},
    'pptweb': {'match': lambda i: bool(re.search(r'PPT|ppt|做网站|网页|秒哒', TS(i))) and bool(re.search(r'AI|ai|一键|生成|网站|网页|秒哒|分钟|效率|教程|教你', TS(i))) and not re.search(r'千问|Qwen|超自然|接中|接单|白菜|爬虫|课件', TS(i)),
               'name': 'AI 一键成品（PPT / 网页）', 'kind': '间接', 'scores': (75, 70, 85), 'picked': True,
               'why': '把资料一键变成 PPT、网页：Ancher 的输出端，爆文率高、几乎全在投应用下载'},
    'videogen': {'match': lambda i: bool(re.search(VIDEO_GEN, TS(i))),
                 'name': 'AI 视频生成（Vidu / OiiOii）', 'kind': '间接', 'scores': (75, 75, 55), 'picked': False, 'drop': '只做单一输出',
                 'why': '爆文率高，但多是官方号的模型演示；只管「生成视频」，不碰收藏和知识'},
    'kb': {'match': lambda i: bool(re.search(r'知识库|第二大脑|知识管理|碎片知识|稍后读', TS(i))),
           'name': 'AI 知识库 / 第二大脑', 'kind': '直接', 'scores': (85, 60, 75), 'picked': False, 'drop': '样本太少',
           'why': '和 Ancher「Remember everything」最像，但库里只有个位数笔记，还没形成投放打法'},
    'agent': {'match': lambda i: bool(re.search(r'扣子|Coze|智能体|Agent|agent', TS(i))) and not re.search(r'千问|Qwen', TS(i)),
              'name': '智能体 / Agent', 'kind': '间接', 'scores': (55, 60, 65), 'picked': False, 'drop': '人群不对',
              'why': '讲「AI 帮你干活」，但多是企业获客和自动化，面向老板不是创作者'},
    'doubao': {'match': lambda i: '豆包' in TS(i) and '超自然' not in TS(i),
               'name': '豆包', 'kind': '直接', 'scores': (60, 45, 55), 'picked': False, 'drop': '动机不对',
               'why': '国民级 AI 助手，但笔记多是聊天梗和生活问答，不讲创作'},
    'podcast': {'match': lambda i: bool(re.search(r'播客|录音转|录音纪要|AI ?录音|录音卡|转文字', TS(i))) and not re.search(r'千问', TS(i)),
                'name': 'AI 录音 / 转文字', 'kind': '间接', 'scores': (60, 50, 70), 'picked': False, 'drop': '样本太少',
                'why': '会议纪要、录音卡：输入端相近，但只有个位数笔记，且偏职场办公'},
    'jianying': {'match': lambda i: bool(re.search(r'剪映|开拍', TS(i))),
                 'name': '剪映 / 开拍（剪辑模板）', 'kind': '间接', 'scores': (80, 75, 50), 'picked': False, 'drop': '账号太集中',
                 'why': '创作者都在用，但库里 10 条几乎全来自 1 个官方教程号，看不出打法'},
}
SELECTION = {
    'keywords': 'AI 自媒体 / 爆款 / 千问 / PPT / 网页 / 知识库 / 视频生成',
    'common': [
        '卖的都是「一个地方搞定」：一个工作台、一个 App、一个软件，从素材直接到成品',
        '都靠个人号和人设号铺量：{picked_notes} 条笔记来自 {picked_accts} 个账号',
        '投放以「应用下载」为主：千问和 AI 做 PPT 几乎全在投下载，按付费率和 7 日 ROI 考核',
    ],
}

# ---------- 2. competitors ----------
def fmt_aiflow(i):
    if re.search('图片|封面|首图|大片', T(i)): return 'af-3'
    if re.search('工作台|SOP|思路|不露脸|自媒体|小说|Obsidian', T(i)): return 'af-2'
    return 'af-1'

def fmt_qianwen(i):
    if re.search('办公|Skill|skill|Agent|云栖|Qwen3|Flash|数据分析|文档|教程|token|AI眼镜', TS(i)): return 'qw-3'
    if re.search('生图|出图|画|Live|Wan|创作|封面|拼豆|废片|滤镜|女书|宝球|童年', TS(i)): return 'qw-2'
    return 'qw-1'

def fmt_pptweb(i):
    if re.search('做网站|网页|秒哒|游戏|桌宠|软件', T(i)): return 'pw-3'
    if re.search('手把手|教程|教学|流程|教你|学会|组会|讲课|必修|互动', T(i)): return 'pw-2'
    return 'pw-1'

COMPETITORS = {
    'aiflow': {
        'name': 'AI 自媒体爆款工作流', 'short': 'AI 自媒体', 'kind': '赛道竞品 · 创作者教程号', 'tagline': '用 AI 复刻爆款、搭工作台、出封面',
        'fmt': fmt_aiflow,
        'formats': [
            ('af-1', '「AI 复刻爆款」教程', '真人 + 爆款截图做封面，大字「AI 复刻」「爆款视频」，教你逐帧拉片、照着做一条', '实用攻略', ['6abb5e4a', '6a882d4a', '6a8fff80']),
            ('af-2', '自媒体 AI 工作台', '把一堆 AI 工具包装成一个「工作台」：封面放工作台截图，标题写「保姆级」「附提示词」「资源包」', '实用攻略', ['6a93d33b', '6a9f8966', '6aa3f7cd']),
            ('af-3', '「我拍的 vs AI 生成的」配图', '同一场景左右对比，或直接晒「一键出首图 / 封面」的成品，图文为主', '效果展示', ['6a8fc744', '6a8d658e', '6a96ad86']),
        ],
        'transfer': {'af-1': 70, 'af-2': 88, 'af-3': 72},
        'takeaway': '三种都有（复刻爆款 4、工作台 3、AI 配图 2）。共同点是封面先给结果：爆款截图、工作台截图、AI 成品；标题再给「教程 / 附提示词」当收藏理由。',
    },
    'qianwen': {
        'name': '千问', 'short': '千问', 'kind': '直接竞品 · 全能 AI 助手', 'tagline': '阿里 AI 助手：一个 App 解决生活、学习、办公、创作',
        'fmt': fmt_qianwen,
        'formats': [
            ('qw-1', '生活难题一键解决', '一个具体场景 + 「千问一键搞定」：手抄报、旅行、辞职信、发型、体检报告，人设号分场景铺', '场景种草', ['69dde04c', '694510af', '6944f001']),
            ('qw-2', '生图 / 创作效果', '先给成品：古诗变画、废片变大片、设计出图，before / after 一眼看懂', '效果展示', ['69412c65', '69420d27', '6a680118']),
            ('qw-3', '千问办公 / 官方活动', '官方号和合作号讲办公 Skill、云栖大会、新模型限免；老年大学学 AI 这类话题出圈', '品牌活动', ['6a9d1bc5', '6ab3f2ed', '6aa263ed']),
        ],
        'transfer': {'qw-1': 58, 'qw-2': 72, 'qw-3': 40},
        'takeaway': '一半以上是「生图 / 创作效果」：先晒成品（古诗变画、废片变大片、设计出图）；官方办公和活动类一条都没进。',
    },
    'pptweb': {
        'name': 'AI 一键成品（PPT / 网页）', 'short': 'AI 做 PPT', 'kind': '间接竞品 · AI 办公 / 建站', 'tagline': '把资料一键变成 PPT、网页、小工具',
        'fmt': fmt_pptweb,
        'formats': [
            ('pw-1', '「最好用的 AI PPT 网站」推荐', '「目前用过最好用的」「终于被我找到了」：推荐口吻 + 成品 PPT 截图', '效果展示', ['6a697303', '6aa3ab49', '6a622b22']),
            ('pw-2', '学姐 / 老师手把手', '真人出镜指着软件 logo，大字「一键做 PPT」「1 分钟完成」，点名大学生、老师，几乎全在投应用下载', '实用攻略', ['69f20db8', '694fc76d', '69bd29df']),
            ('pw-3', 'AI 做网页 / 小工具', '一张图变交互网页、宠物做成桌宠、零基础做可变现的小产品：vibe coding 的成品展示', '效果展示', ['6a9148cb', '6a8d85e3', '6a5bc1ab']),
        ],
        'transfer': {'pw-1': 74, 'pw-2': 82, 'pw-3': 66},
        'takeaway': '全是 PPT：学姐 / 老师手把手最多，「最好用的 AI PPT 网站」推荐其次；做网页 / 小工具的一条都没进。',
    },
}

# ---------- 3. teardowns ----------
TEARDOWNS = {
    'af-2': {
        'hero': '6a93d33b',
        'account': {'name': '猫叔成长笔记', 'kind': '自媒体干货博主', 'inLib': 1,
                    'note': '库里只有这 1 条；这个赛道 22 条来自 21 个号，没有官方号，全是个人博主在教「怎么用 AI 做自媒体」',
                    'matrix': {'notes': 22, 'accounts': 21}},
        'traffic': {
            'quant': {'from': 'Atlas 素材库 · 聚光「产品种草」+ 热门榜单', 'lists': 'auto',
                      'summary': '「产品种草」AI 技能培训类近 30 日曝光量第 12（共 100 条）；自然热门榜里阅读量第 47'},
            'qual': {'verdict': '搜索长尾 + 收藏型', 'reason': '「自媒体」「AI 工作台」「保姆级教程」「附提示词」都是创作者会主动搜、会先收藏的词；封面把工作台截图摆出来，结果先给。',
                     'keywords': [
                         {'w': '自媒体', 'where': ['标题', '封面'], 'role': '人群词', 'note': '创作者对号入座'},
                         {'w': 'AI 工作台', 'where': ['标题', '封面'], 'role': '新概念词', 'note': '把零散工具包装成一个系统'},
                         {'w': '保姆级教程', 'where': ['标题', '封面'], 'role': '承诺词', 'note': '降低门槛，收藏理由'},
                         {'w': '附提示词', 'where': ['标题'], 'role': '收藏钩子', 'note': '先存再说，长期带搜索'},
                         {'w': '一键生成知识图卡', 'where': ['封面'], 'role': '结果词', 'note': '直接说产出物'},
                     ],
                     'longtail': ['自媒体 AI 工具 推荐', 'AI 工作台 怎么搭', '小红书 知识卡片 生成']}},
        'money': {'steps': [{'k': '教程种草', 'd': '录屏演示搭工作台'}, {'k': '评论区要提示词', 'd': '「附提示词」引互动'}, {'k': '私信 / 社群', 'd': '引到私域'}, {'k': '课程 / 工具会员', 'd': '后端变现（推断）'}],
                  'path': '教程引流 → 私域 → 课程或工具分成（推断）', 'price': '未公开'},
        'structure': [{'t': '封面', 'd': '黑底大字「自媒体 AI 工作台搭建」，中间放思维导图式的工作台截图，底部黄字「保姆级教程」，角标「一键生成知识图卡」'},
                      {'t': '标题', 'd': '「自媒体 AI 工作台搭建保姆级教程（附提示词）」：人群 + 新概念 + 承诺 + 赠品'},
                      {'t': '视频', 'd': '录屏演示从素材到知识图卡的搭建过程（推断）'}],
        'why': ['「AI 工作台」把一堆工具说成一个系统：创作者要的是流程，不是又一个工具', '「保姆级」+「附提示词」= 收藏理由，长期吃搜索', '封面直接放工作台截图，结果先给'],
        'inferred': ['视频'],
    },
    'qw-1': {
        'hero': '694510af',
        'account': {'name': '问问我的旅游搭子', 'kind': '场景人设号（千问投放矩阵）', 'inLib': 2,
                    'note': '昵称就是场景人设；库里另一条讲出国翻译。千问 84 条来自 65 个号，按旅行、教师、宝妈、职场分人设铺量',
                    'matrix': {'notes': 84, 'accounts': 65}},
        'traffic': {
            'quant': {'from': 'Atlas 素材库 · 聚光「应用推广·应用下载」榜单', 'lists': 'auto',
                      'summary': '综合 AI 类「7 日 ROI（下载）」第 4（共 100 条）：带来的下载最值钱'},
            'qual': {'verdict': '投放驱动型', 'reason': '图文本身是场景种草，流量主要靠应用下载信息流；「旅行神器」「一个 APP 搞定」是出行前的高频搜索词。',
                     'keywords': [
                         {'w': '一个 APP 搞定', 'where': ['标题', '封面'], 'role': '承诺词', 'note': '把「全能」说成一个具体好处'},
                         {'w': '旅行 / 旅游', 'where': ['标题', '封面'], 'role': '场景词', 'note': '寒假出行季的刚需'},
                         {'w': '旅行神器', 'where': ['封面'], 'role': '品类搜索词', 'note': '出行前会搜'},
                         {'w': '赢麻了', 'where': ['标题', '封面'], 'role': '情绪词', 'note': '口语化，像真人分享'},
                         {'w': '千问', 'where': ['标题', '封面'], 'role': '品牌词', 'note': '品牌名直接上封面'},
                     ],
                     'longtail': ['旅行 攻略 APP', '出国 翻译 神器', 'AI 规划 旅行 路线']}},
        'money': {'steps': [{'k': '场景种草', 'd': '人设号发图文'}, {'k': '下载千问', 'd': '应用下载信息流'}, {'k': '用 AI 规划行程', 'd': '激活'}, {'k': '留存 / 付费', 'd': '按 7 日 ROI 考核'}],
                  'path': '应用下载投放 → 激活 → 7 日 ROI', 'price': 'App 免费，按下载效果投放'},
        'structure': [{'t': '封面', 'd': '9 宫格旅行目的地拼图，大字「一个 APP 搞定旅游」「真正的旅行神器」「千问赢麻了」'},
                      {'t': '标题', 'd': '「一个APP搞定全程旅行？千问真的赢麻了🧳」：疑问句 + 情绪词'},
                      {'t': '正文', 'd': '多图展示用千问规划行程的截图（推断）'},
                      {'t': '发布', 'd': '2025-12-19，寒假出行季'}],
        'why': ['用一个具体生活场景卖「全能」，比讲功能好懂', '账号名就是场景人设（旅游搭子），像真人分享', '按场景分号铺量：旅行、教师、宝妈、职场各有一批'],
        'inferred': ['正文'],
    },
    'pw-2': {
        'hero': '69f20db8',
        'account': {'name': '💖粥粥学姐💖', 'kind': '学姐人设号', 'inLib': 1,
                    'note': '「学姐」人设 + 真人出镜；这一组 24 条来自 23 个号，「手把手」教程里 6 条有视频，几乎都在投应用下载',
                    'matrix': {'notes': 24, 'accounts': 23}},
        'traffic': {
            'quant': {'from': 'Atlas 素材库 · 聚光「应用推广·应用下载」榜单', 'lists': 'auto',
                      'summary': 'AI 办公类「付费率（下载）」第 5（共 86 条），7 日 ROI 第 6：看完会下载，还会付费'},
            'qual': {'verdict': '投放 + 人群定向型', 'reason': '封面写「一键做 ppt」「1 分钟完成」，标题点名「大学生」：人群 + 时间承诺；「做 PPT」是学生和职场人的高频刚需搜索。',
                     'keywords': [
                         {'w': '一键做 ppt', 'where': ['封面'], 'role': '结果词', 'note': '直接说产出物'},
                         {'w': '1 分钟', 'where': ['标题', '封面'], 'role': '时间承诺', 'note': '把门槛压到最低'},
                         {'w': '大学生', 'where': ['标题'], 'role': '人群词', 'note': '开学、期末季精准命中'},
                         {'w': '手把手', 'where': ['标题'], 'role': '教程词', 'note': '收藏理由'},
                         {'w': '全程一个软件搞定', 'where': ['封面'], 'role': '降门槛词', 'note': '不用切换工具'},
                     ],
                     'longtail': ['AI 做 PPT 免费', '一键生成 PPT 软件', '大学生 PPT 怎么做快']}},
        'money': {'steps': [{'k': '学姐口播种草', 'd': '真人 + 录屏'}, {'k': '点击下载', 'd': '应用下载信息流'}, {'k': '一键生成 PPT', 'd': '激活'}, {'k': '会员付费', 'd': '按付费率考核'}],
                  'path': '应用下载 → 生成 → 付费', 'price': '会员订阅（金额未公开）'},
        'structure': [{'t': '封面', 'd': '真人学姐双手指向软件 logo，大字「一键做 ppt」「1 分钟完成」，绿勾「全程一个软件搞定」「ppt 万能模版 + 自动美化」'},
                      {'t': '标题', 'd': '「‼️手把手教你1分钟出ppt‼️大学生不看必后悔」：教程 + 时间承诺 + 人群 + 损失厌恶'},
                      {'t': '视频', 'd': '真人口播 + 录屏演示一键生成（素材库有视频，可直接看）'}],
        'why': ['真人学姐出镜，比工具截图可信', '「1 分钟」「一个软件搞定」把门槛压到最低', '点名大学生，开学和期末季精准命中'],
        'inferred': [],
    },
}

# ---------- 4. laws ----------
LAWS = [
    {'id': 'L1', 'name': '说「一个地方全搞定」', 'claim': '标题里有「一个 APP / 一个软件搞定 / 工作台 / 全流程」的笔记，爆款率 {withHit}%；没有的只有 {withoutHit}%。',
     'evidence': {'rx': r'工作台|SOP|系统|全流程|流程|一个(APP|软件|网站)|全程|全搞定|搞定'}, 'examples': ['694510af', '6a93d33b', '69dde04c'],
     'mock': {'cover': '收藏夹<br>变工作台', 'pal': 1, 'person': True, 'type': '图文'},
     'apply': {'title': '「我的收藏夹，就是我的内容工作台」', 'cover': '左：收藏夹里 200 条吃灰链接；右：Ancher 一键生成的视频、网页、播客、图片、文章 5 宫格', 'script': '展示收藏 → 选 3 条 → 一次生成 5 种成品 → 挑一个发出去', 'kpi': '建议看：收藏率、注册转化'}},
    {'id': 'L2', 'name': '给一个时间承诺', 'claim': '标题写「1 分钟 / 3 步 / 一键」的笔记，爆款率 {withHit}%；没有的 {withoutHit}%。',
     'evidence': {'rx': r'\d+ ?(分钟|秒|步)|一键|秒变|秒出|快到|几分钟|三步|分钟'}, 'examples': ['69f20db8', '6a8fc744', '6aae2af2'],
     'mock': {'cover': '3 分钟<br>收藏变播客', 'pal': 0, 'person': False, 'type': '视频'},
     'apply': {'title': '「3 分钟，把收藏的 10 篇文章变成一期播客」', 'cover': '计时器 + 播客封面', 'script': '倒计时录屏：粘贴链接 → 选「播客」→ 3 分钟出音频', 'kpi': '建议看：完播率、点击「生成」的比例'}},
    {'id': 'L3', 'name': '别喊爆款，直接给成品', 'claim': '标题喊「爆款 / 神器 / 封神」的笔记，爆款率只有 {withHit}%；不喊的 {withoutHit}%。创作者见多了，看得见的成品更有说服力。',
     'evidence': {'rx': r'爆款|涨粉|万赞|赢麻|封神|绝了|yyds|离谱|神器'}, 'examples': ['69412c65', '6a8d85e3', '6a8d658e'],
     'mock': {'cover': '1 条收藏<br>5 种成品', 'pal': 2, 'person': False, 'type': '图文'},
     'apply': {'title': '「同一条收藏，我做了 5 种成品」', 'cover': '5 宫格：视频截图 / 网页 / 播客波形 / 配图 / 文章', 'script': '一条素材 → 5 个成品逐个展示，最后问「你选哪个」', 'kpi': '建议看：评论数、保存率'}},
]
