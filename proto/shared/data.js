// Atlas proto — sample brief data. Fictional brand + fictional competitors; numbers are illustrative.
// Shape is the contract the real crawl/research pipeline will fill later.

(function () {
  const palettes = [
    ['#f4d9c6', '#e9a98b', '#3b1f14'], // peach film
    ['#1f2a44', '#4b5d8a', '#fff'],    // night blue
    ['#f7efe2', '#d9c7a6', '#2d2418'], // cream
    ['#e8434a', '#b8202b', '#fff'],    // xhs red
    ['#d9e6dc', '#9fbfa8', '#1b2b20'], // sage
    ['#2a2320', '#5b4b40', '#f6e7d4'], // espresso
    ['#ffd84d', '#f7b733', '#2a1d00'], // marigold
    ['#e9e3f5', '#b9a8e0', '#251a45'], // lilac
    ['#0f0f10', '#2b2b2e', '#ffe3c2'], // black glossy
    ['#cfe6f5', '#86b9dd', '#0d2536'], // sky
  ];

  const product = {
    name: '拾光 AI 写真',
    oneLine: '上传 6 张自拍，3 分钟出一套 30 张风格写真',
    category: 'AI 影像 · 虚拟产品',
    price: '¥19.9 首单 / ¥99 年卡',
    audience: '18–30 岁女性，学生与一二线白领',
    platform: '小红书（主）· 抖音（辅）',
    goal: '30 天内把聚光投放 CPA 从 ¥38 压到 ¥25',
    sellingPoints: ['不用去影楼', '风格模板周更', '像本人，不像网红脸'],
    pool: { source: '小红书聚光 · 行业「AI 影像」+ 抖音创意中心', window: '2026-07-01 → 2026-09-30', brands: 14, notes: 3862 },
  };

  // Competitor pool. relevance = 用户·场景·价格 重合度加权; heat = 爆文率·投放增速·素材量 加权.
  const pool = [
    { id: 'jingyu', name: '镜屿 AI 写真', kind: '直接', relevance: 92, heat: 86, notes: 612, user: 95, scene: 94, price: 86, picked: true, why: '同价位、同人群、同「自拍→写真」路径，投放量第一' },
    { id: 'xiangsu', name: '像素照相馆', kind: '直接', relevance: 84, heat: 78, notes: 431, user: 88, scene: 82, price: 81, picked: true, why: '小程序形态，主打证件照/毕业照，价格锚点打得最狠' },
    { id: 'lumi', name: 'Lumi 修图', kind: '间接', relevance: 66, heat: 91, notes: 958, user: 80, scene: 58, price: 55, picked: true, why: '通用修图工具，AI 风格化功能的爆文率全池最高，内容可迁移' },
    { id: 'miaopai', name: '妙拍写真馆', kind: '直接', relevance: 88, heat: 41, notes: 120, user: 90, scene: 92, price: 80, picked: false, why: '高度重合，但近 90 天几乎没有爆文，参考价值低' },
    { id: 'yanzhi', name: '颜值实验室', kind: '直接', relevance: 79, heat: 52, notes: 204, user: 84, scene: 78, price: 72, picked: false, why: '素材量中等，爆文集中在 7 月，已衰退' },
    { id: 'huanying', name: '幻影 AI', kind: '间接', relevance: 58, heat: 74, notes: 377, user: 62, scene: 60, price: 50, picked: false, why: '偏 AI 视频特效，与静态写真场景偏离' },
    { id: 'kuaixiu', name: '快修相机', kind: '间接', relevance: 61, heat: 63, notes: 289, user: 72, scene: 55, price: 52, picked: false, why: '人群重合但以免费滤镜为主，不打付费转化' },
    { id: 'daka', name: '打卡相机', kind: '间接', relevance: 44, heat: 82, notes: 506, user: 58, scene: 36, price: 38, picked: false, why: '爆款多但是旅行打卡场景，迁移成本高' },
    { id: 'huashi', name: '画室 AIGC 课', kind: '间接', relevance: 31, heat: 70, notes: 188, user: 35, scene: 28, price: 30, picked: false, why: '卖课，用户与动机都不同' },
    { id: 'zhengjian', name: '证件照大师', kind: '直接', relevance: 72, heat: 34, notes: 97, user: 70, scene: 80, price: 66, picked: false, why: '场景单一，爆文率低' },
    { id: 'yingzhi', name: '影志胶片', kind: '间接', relevance: 49, heat: 57, notes: 142, user: 60, scene: 45, price: 40, picked: false, why: '胶片滤镜 App，与「撕拉片」风格有交集' },
    { id: 'meitu', name: '某头部修图 App', kind: '间接', relevance: 55, heat: 88, notes: 1240, user: 70, scene: 50, price: 42, picked: false, why: '体量过大，内容以品牌活动为主，难以对标' },
    { id: 'tuzhi', name: '兔子写真', kind: '直接', relevance: 76, heat: 61, notes: 233, user: 80, scene: 76, price: 70, picked: false, why: '可作为候补：重合度高、爆文率中等' },
    { id: 'aipai', name: 'AI 拍立得', kind: '间接', relevance: 38, heat: 45, notes: 76, user: 48, scene: 34, price: 30, picked: false, why: '硬件周边，场景不同' },
  ];

  // note: { id, title, cover, account, followers, likes, collects, comments, type, person, pal, date }
  const N = (id, title, cover, account, followers, likes, collects, comments, type, person, pal, date) =>
    ({ id, title, cover, account, followers, likes, collects, comments, type, person, pal, date });

  const competitors = [
    {
      id: 'jingyu', name: '镜屿 AI 写真', kind: '直接竞品', tagline: '自拍 → 写真，¥29.9 起',
      stats: { notes: 612, hits: 74, hitRate: 12.1, medianLikes: 1840 },
      formats: [
        {
          id: 'jy-1', name: '撕拉片前后对比', axis: { content: '产品效果', data: 'high' },
          desc: '左边随手自拍，右边撕拉片风格成片；封面一句「这是我？」',
          share: 38, hits: 28, avgLikes: 8600, hitRate: 21.4, type: '图文',
          notes: [
            N('jy-1a', '全网赞爆的撕拉片，我用 AI 拍了一套', '这是我？<br>撕拉片 AI 写真', '月半', 12400, 23600, 9800, 1120, '图文', true, 0, '2026-08-12'),
            N('jy-1b', '自拍 6 张换来的胶片感，值了', '6 张自拍<br>换一套胶片', '是小柚子呀', 3100, 11200, 5400, 640, '图文', true, 2, '2026-08-30'),
            N('jy-1c', '男朋友说这不是我，我当场急了', '他说这不是我', '阿九啊_', 860, 7800, 2100, 930, '视频', true, 5, '2026-09-06'),
          ],
        },
        {
          id: 'jy-2', name: '素人翻车 → 大片', axis: { content: '人设故事', data: 'high' },
          desc: '先晒最丑的证件照/素颜，再给 AI 成片，评论区自发晒图',
          share: 27, hits: 20, avgLikes: 6200, hitRate: 17.0, type: '视频',
          notes: [
            N('jy-2a', '证件照像通缉犯，AI 救了我', '证件照翻车<br>到大片', '小鹿脸不圆', 5600, 18400, 6100, 2300, '视频', true, 3, '2026-07-28'),
            N('jy-2b', '素颜 vs AI 写真，差距有点大', '素颜 vs AI', '薇薇的选择', 2200, 6900, 2400, 780, '视频', true, 9, '2026-08-19'),
            N('jy-2c', '35 岁宝妈第一次拍写真', '35 岁<br>第一次拍写真', '橙子妈妈', 940, 4100, 1900, 410, '图文', true, 4, '2026-09-14'),
          ],
        },
        {
          id: 'jy-3', name: '节日模板合集', axis: { content: '产品效果', data: 'mid' },
          desc: '七夕/中秋/毕业季限定模板 9 宫格，收藏率高、互动低',
          share: 21, hits: 16, avgLikes: 3900, hitRate: 9.8, type: '图文',
          notes: [
            N('jy-3a', '七夕限定 9 套，闺蜜说想抄作业', '七夕限定<br>9 套写真', '镜屿官方', 48000, 5200, 7400, 260, '图文', false, 7, '2026-08-08'),
            N('jy-3b', '中秋月光写真，模板直接拿', '中秋<br>月光写真', '今天 AI 出什么片', 15100, 3800, 5100, 190, '图文', false, 1, '2026-09-10'),
            N('jy-3c', '毕业季不想穿学士服？', '毕业照<br>不穿学士服', '镜屿官方', 48000, 2700, 3300, 150, '图文', true, 6, '2026-06-28'),
          ],
        },
      ],
    },
    {
      id: 'xiangsu', name: '像素照相馆', kind: '直接竞品', tagline: '小程序，证件照 ¥9.9',
      stats: { notes: 431, hits: 41, hitRate: 9.5, medianLikes: 1210 },
      formats: [
        {
          id: 'xs-1', name: '价格对比：影楼 vs AI', axis: { content: '价格锚点', data: 'high' },
          desc: '封面直接写「影楼 ¥899 / AI ¥9.9」，正文晒对比图',
          share: 41, hits: 17, avgLikes: 7100, hitRate: 18.2, type: '图文',
          notes: [
            N('xs-1a', '别再花 899 拍职业照了', '影楼 ¥899<br>AI ¥9.9', '打工人小林', 6800, 15800, 11200, 1480, '图文', true, 3, '2026-08-03'),
            N('xs-1b', '一杯奶茶钱的毕业照', '一杯奶茶钱<br>的毕业照', '大四在逃', 1900, 8800, 6000, 720, '图文', true, 6, '2026-06-20'),
            N('xs-1c', '求职照省了 600，HR 夸好看', '求职照<br>省了 600', '职场小白 Tina', 3300, 5600, 4400, 380, '视频', true, 2, '2026-09-02'),
          ],
        },
        {
          id: 'xs-2', name: '闺蜜合照联名', axis: { content: '人设故事', data: 'mid' },
          desc: '两人各上传自拍，生成「同框」写真，强社交传播',
          share: 29, hits: 12, avgLikes: 4800, hitRate: 11.0, type: '视频',
          notes: [
            N('xs-2a', '异地闺蜜终于同框了', '异地闺蜜<br>终于同框', '一勺舒芙蕾', 2600, 9300, 3900, 1650, '视频', true, 7, '2026-08-22'),
            N('xs-2b', '和奶奶拍了第一张合照', '和奶奶的<br>第一张合照', '江南小满', 780, 12600, 4100, 2280, '视频', true, 0, '2026-09-09'),
            N('xs-2c', '室友 4 人 AI 写真，宿舍封神', '宿舍 4 人<br>写真封神', '大学生日常', 4100, 3900, 1600, 520, '图文', true, 4, '2026-09-18'),
          ],
        },
        {
          id: 'xs-3', name: '三家横评', axis: { content: '价格锚点', data: 'mid' },
          desc: '博主「自费」横评 3 家 AI 写真，结论偏向自家',
          share: 18, hits: 7, avgLikes: 3300, hitRate: 7.6, type: '图文',
          notes: [
            N('xs-3a', '测了 3 家 AI 写真，只推荐这个', '测了 3 家<br>只推荐 1 个', '买手阿雯', 22000, 4600, 6800, 890, '图文', false, 8, '2026-08-15'),
            N('xs-3b', 'AI 证件照哪家最像本人', '哪家<br>最像本人', '测评君', 9400, 3100, 4200, 610, '图文', true, 9, '2026-07-30'),
            N('xs-3c', '花 100 块测完所有 AI 写真', '花 100 块<br>测完所有', '省钱研究所', 31000, 2400, 3500, 330, '视频', false, 5, '2026-09-21'),
          ],
        },
      ],
    },
    {
      id: 'lumi', name: 'Lumi 修图', kind: '间接竞品', tagline: '通用修图 App，AI 风格化爆火',
      stats: { notes: 958, hits: 118, hitRate: 12.3, medianLikes: 2260 },
      formats: [
        {
          id: 'lm-1', name: '30 秒录屏教程', axis: { content: '产品效果', data: 'high' },
          desc: '手机录屏 + 大字幕，教「一键出氛围感」，结尾露出 App',
          share: 44, hits: 52, avgLikes: 9400, hitRate: 19.6, type: '视频',
          notes: [
            N('lm-1a', '30 秒学会拯救逆光废片', '逆光废片<br>30 秒救回', '一口橙汁', 18800, 26400, 21000, 1340, '视频', false, 9, '2026-08-07'),
            N('lm-1b', '博主同款高清磨皮怎么 P', '博主同款<br>怎么 P', '修图课代表', 41000, 19200, 16800, 980, '视频', false, 8, '2026-07-25'),
            N('lm-1c', '一键把普通自拍变胶片', '一键变胶片', '陶特斯', 7700, 8100, 7300, 420, '视频', true, 0, '2026-09-11'),
          ],
        },
        {
          id: 'lm-2', name: '一张图 20 种风格', axis: { content: '产品效果', data: 'mid' },
          desc: '同一张自拍跑 20 个风格，九宫格/轮播，靠「选择困难」引评论',
          share: 31, hits: 37, avgLikes: 6800, hitRate: 14.2, type: '图文',
          notes: [
            N('lm-2a', '一张自拍跑了 20 种风格，选一个', '1 张自拍<br>20 种风格', '小林快去画画', 11000, 14700, 5800, 3900, '图文', true, 7, '2026-08-26'),
            N('lm-2b', '你最喜欢第几张？我选 7', '你选第几张？', '智多星侦探', 2600, 6400, 2200, 2700, '图文', true, 1, '2026-09-04'),
            N('lm-2c', '把甄姬海报改成穆夏风', '穆夏风<br>也太绝了', '好厨子爱吃拌饭', 1200, 5100, 3000, 460, '图文', false, 2, '2026-07-19'),
          ],
        },
        {
          id: 'lm-3', name: '情绪文案氛围片', axis: { content: '人设故事', data: 'mid' },
          desc: '一句情绪文案 + 氛围大片，弱产品露出，靠共鸣涨粉',
          share: 17, hits: 21, avgLikes: 5200, hitRate: 10.4, type: '图文',
          notes: [
            N('lm-3a', '那些无法复刻的瞬间', '无法复刻<br>的瞬间', '萤火回声', 9900, 13800, 6200, 1210, '图文', true, 1, '2026-08-17'),
            N('lm-3b', '恰似一场蔷薇色的梦', '蔷薇色的梦', '月半', 12400, 4300, 1800, 260, '图文', true, 7, '2026-09-15'),
            N('lm-3c', '25 岁，给自己拍一套', '25 岁<br>给自己拍一套', '一只阿鹿', 1500, 3600, 1400, 390, '视频', true, 5, '2026-09-26'),
          ],
        },
      ],
    },
  ];

  // Teardown per format: account / traffic / monetization / structure / why it works.
  const teardowns = {
    'jy-1': {
      hero: 'jy-1a',
      account: { name: '月半', followers: 12400, kind: 'KOC · 素人写真号', posts: '每周 3 篇', note: '非品牌号，但置顶链接指向镜屿，疑似长期合作', mix: [{ k: '写真作品', v: 62 }, { k: '日常穿搭', v: 24 }, { k: '合作广告', v: 14 }] },
      traffic: { sources: [{ k: '发现页推荐', v: 58 }, { k: '搜索', v: 27 }, { k: '聚光信息流', v: 11 }, { k: '其他', v: 4 }], keywords: ['撕拉片', 'AI 写真', '胶片感', '拍写真'], curve: [2, 9, 31, 64, 82, 91, 96, 98, 99, 100], peak: '发布后第 3 天', boost: '第 2 天追投薯条约 ¥500' },
      money: { steps: [{ k: '曝光', v: 412000 }, { k: '阅读', v: 61800 }, { k: '评论区问链接', v: 3100 }, { k: '进小程序', v: 1900 }, { k: '¥29.9 下单', v: 310 }], price: '¥29.9 → ¥129 年卡', path: '评论区置顶「搜：镜屿」→ 小程序首单 → 7 天内推年卡' },
      structure: [{ t: '封面', d: '左右对比 + 「这是我？」一句话，反差先行' }, { t: 'P2–P4', d: '3 组前后对比，每组换一个风格' }, { t: 'P5', d: '操作截图：上传 6 张 → 选风格 → 等 3 分钟' }, { t: '正文', d: '口语化、不提价格，末尾「想要同款的评论区扣 1」' }],
      why: ['反差是最便宜的钩子：前后对比 0.5 秒看懂', '素人号背书，降低广告感', '把转化放进评论区，避开限流'],
    },
    'xs-1': {
      hero: 'xs-1a',
      account: { name: '打工人小林', followers: 6800, kind: 'KOC · 职场号', posts: '每周 2 篇', note: '职场干货号，广告占比低，人设可信', mix: [{ k: '职场干货', v: 71 }, { k: '省钱攻略', v: 19 }, { k: '合作广告', v: 10 }] },
      traffic: { sources: [{ k: '搜索', v: 49 }, { k: '发现页推荐', v: 38 }, { k: '聚光信息流', v: 9 }, { k: '其他', v: 4 }], keywords: ['职业照', '求职照', '证件照 便宜', 'AI 证件照'], curve: [4, 12, 26, 41, 55, 67, 76, 84, 91, 100], peak: '长尾，第 10 天仍在增长', boost: '聚光搜索词「职业照」竞价' },
      money: { steps: [{ k: '曝光', v: 268000 }, { k: '阅读', v: 52400 }, { k: '点击小程序卡', v: 4800 }, { k: '¥9.9 下单', v: 1260 }, { k: '加购精修', v: 190 }], price: '¥9.9 → ¥39 精修', path: '笔记挂小程序卡 → ¥9.9 低门槛 → 加购精修' },
      structure: [{ t: '封面', d: '两个价格并排，红色大字，价格就是标题' }, { t: 'P2', d: '影楼报价单截图（真实感）' }, { t: 'P3–P5', d: 'AI 成片 + HR 反馈聊天截图' }, { t: '正文', d: '列 3 条「省钱理由」，结尾挂小程序' }],
      why: ['价格锚点写在封面，决策成本直接降到 0', '搜索流量占一半，吃的是刚需词', '¥9.9 门槛让转化率翻倍'],
    },
    'lm-1': {
      hero: 'lm-1a',
      account: { name: '一口橙汁', followers: 18800, kind: '垂类 · 修图教程号', posts: '每周 4 篇', note: '纯教程号，Lumi 只在第 25 秒出现', mix: [{ k: '修图教程', v: 82 }, { k: '拍照技巧', v: 13 }, { k: '合作广告', v: 5 }] },
      traffic: { sources: [{ k: '发现页推荐', v: 51 }, { k: '搜索', v: 41 }, { k: '聚光信息流', v: 3 }, { k: '其他', v: 5 }], keywords: ['逆光', '废片', '修图教程', '氛围感'], curve: [3, 15, 38, 59, 72, 81, 88, 93, 97, 100], peak: '发布后第 2 天', boost: '无付费，自然流' },
      money: { steps: [{ k: '曝光', v: 530000 }, { k: '完播', v: 118000 }, { k: '收藏', v: 21000 }, { k: '搜索 App', v: 6400 }, { k: '付费会员', v: 420 }], price: '免费 → ¥68 年会员', path: '教程收藏 → 搜索下载 App → 风格包付费' },
      structure: [{ t: '0–3 秒', d: '废片原图 + 「还能救吗？」' }, { t: '3–20 秒', d: '录屏 4 步，每步一行大字幕' }, { t: '20–27 秒', d: '成片对比，停留 2 秒' }, { t: '27–30 秒', d: '「工具在这」一闪，不口播' }],
      why: ['教程=收藏，收藏=长尾搜索流量', '产品藏在工具链里，零广告感', '30 秒以内完播率高'],
    },
  };
  // Lighter teardowns for the other formats, so every hit can be opened.
  for (const c of competitors) for (const f of c.formats) {
    if (!teardowns[f.id]) teardowns[f.id] = { hero: f.notes[0].id, inherit: true };
  }

  // Laws distilled across all hits; each backed by 3 examples and an application to 拾光.
  const laws = [
    {
      id: 'L1', name: '反差先行', claim: '封面先给「前」，再给「后」。前后对比的爆文率是纯成片展示的 2.3 倍。',
      evidence: { hits: 19, of: 27 }, examples: ['jy-1a', 'jy-2a', 'lm-1a'],
      apply: { title: '「这是我？」系列', cover: '左：地铁里的随手自拍 / 右：拾光胶片写真', script: '3 组对比 + 第 5 张放上传界面截图', kpi: '封面点击率 ≥ 12%' },
    },
    {
      id: 'L2', name: '价格写进封面', claim: '把参照价格放到封面上：「影楼 ¥899 / AI ¥9.9」。搜索流量带来的爆文里有 71% 这样做。',
      evidence: { hits: 12, of: 27 }, examples: ['xs-1a', 'xs-1b', 'xs-3c'],
      apply: { title: '「一杯奶茶钱的写真」', cover: '¥19.9 vs 影楼 ¥699，红底大字', script: '影楼报价单 → 拾光成片 → 首单入口', kpi: '搜索流量占比 ≥ 40%' },
    },
    {
      id: 'L3', name: '素人感压过精致感', claim: '真人、不完美背景、口语标题。官方号同题材的互动只有素人号的 1/3。',
      evidence: { hits: 16, of: 27 }, examples: ['jy-2c', 'xs-2b', 'lm-3c'],
      apply: { title: '「第一次拍写真」素人征集', cover: '真实用户 + 一句自述', script: '招募 20 位 KOC，每人 1 篇，统一挂评论区口令', kpi: 'CPA ≤ ¥25' },
    },
  ];

  // Background scatter for the hit matrix: every note of each picked competitor (deterministic).
  let seed = 7;
  const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
  const scatter = {};
  for (const c of competitors) {
    scatter[c.id] = [];
    const total = 46;
    for (let i = 0; i < total; i++) {
      const f = c.formats[i % 3];
      const hit = rnd() < 0.24;
      scatter[c.id].push({
        format: f.id,
        likes: Math.round(hit ? 3000 + rnd() * 24000 : 80 + rnd() * 2600),
        transfer: Math.round(Math.min(98, Math.max(6, (f.axis.content === '人设故事' ? 55 : f.axis.content === '价格锚点' ? 72 : 64) + (rnd() - 0.5) * 50))),
        hit,
      });
    }
    for (const f of c.formats) for (const n of f.notes) scatter[c.id].push({ format: f.id, likes: n.likes, transfer: 60 + Math.round(rnd() * 34), hit: true, note: n.id });
  }

  const allNotes = {};
  for (const c of competitors) for (const f of c.formats) for (const n of f.notes) allNotes[n.id] = { ...n, competitor: c.id, format: f.id };

  window.ATLAS = { palettes, product, pool, competitors, teardowns, laws, scatter, notes: allNotes };
})();
