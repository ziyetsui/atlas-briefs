## 素材来源 ②：聚光「内容广场」直抓（v1 · 2026-10-15）

`data/library/` 是旧素材库的导出：13,749 条里大多是 AI / 全行业，食品零食几乎没有（「果干」1 条、「果脯」5 条），也没有点赞、粉丝这些真实数字。
新品类（第一个是橘子肉肉）改从聚光后台的内容广场直接抓：`https://ad.xiaohongshu.com/microapp/creativity/inspire`。

### 1. 能拿到什么

内容广场每个榜单 = 一个 **Top 100**（榜单 × 行业或关键词 × 排序指标 × 时间窗）。每条笔记带：

| 字段 | 说明 |
|---|---|
| 阅读 / 点赞 / 收藏 / 评论 | 真实数字（旧素材库没有） |
| 作者昵称、粉丝数、userId | 可以算账号量级、矩阵 |
| 发布时间 | 精确到秒，不用再从笔记 ID 推 |
| 是否推广（isAdNote）、是否蒲公英（bindType） | 区分投放笔记和自然笔记 |
| 全部图片（宽高） | 图文笔记能在页面里翻看 |
| 视频地址 + 时长 | 视频能在页面里播放 |
| 签名链接（带 xsec_token） | 「看原文」能直接打开 |

拿不到：**正文全文**（只有标题）、曝光量和阅读率的具体数（只用于排序，不返回）。
注意：图片和视频地址带签名，**约 1–2 天过期**，用到的必须当天转存到 R2（见 §4）。

### 2. 筛选维度（接口字段）

| 页面上 | 字段 | 取值 |
|---|---|---|
| 榜单 | `bizType` | 2 产品种草 · 7 种草直达 · 4 蒲公英合作 · 1 小红书热门 · 6 电商热门 · 5 客资收集 · 8 应用推广 |
| 时间 | `nd` | `"3"` `"7"` `"14"` `"30"` |
| 排序 | `orderBy` + `sort: "desc"` | 种草类：`premium_read_num` 阅读量 · `premium_engage_num` 互动量 · `premium_ctr` 阅读率 · `premium_engage_rate` 互动率；热门 / 蒲公英多一个 `premium_good_read_rate`；电商热门有 `premium_ecm_dgmv` 支付金额等 |
| 所属行业（种草 / 蒲公英 / 种草直达） | `spuIndustry` | 路径用 `#` 连接，例：`食品饮料#休闲零食#蜜饯果干` |
| 所属行业（电商热门） | `eCommerceIndustry` | 例：`零食/坚果/特产#蜜饯/枣类/梅/果干/冻干` |
| 类目（小红书热门） | `noteContentCategory` | 例：`所属行业#食品饮料#休闲零食#蜜饯果干` |
| 关键词 | `searchWord` | 语义搜索，会混进不相关的（搜「橘子」会出「橘子洲」），只当补充 |
| 内容类型 / 来源 / 流量场域 / 题材 | `noteType` / `contentType` / `premiumPlacement` / 题材 | 本轮没用 |

`platform` 固定为 2（聚光）。每页 34 条，3 页到底。

### 3. 怎么抓

前提：Chrome 已登录聚光、装好 OpenCLI 扩展（`opencli doctor` 显示 connected）。Claude 的 Chrome 扩展连不上也没关系，走 OpenCLI。

```sh
opencli browser jz open "https://ad.xiaohongshu.com/microapp/creativity/inspire"   # 打开一次，会话名 jz
python3 scripts/fetch_juguang.py data/fetch/jg_queries.json --pages 3              # 每个查询一个文件 → data/fetch/jg/<name>.json
python3 scripts/jg_library.py                                                      # 合并去重 → data/library-jg/（items.json + det.json）
python3 scripts/atlas_build.py <slug> --lib data/library-jg                        # 之后照 0003 手册走
python3 scripts/jg_media.py <slug>                                                 # 用到的笔记媒体转存 R2（§4），再跑一次上一行
```

- 抓取原理：在页面主环境里调用页面自己的接口 `POST edith.xiaohongshu.com/api/pgy_leona/content_square/search_note_v2`，用页面的 `window._webmsxyw` 签名（GET 接口不签名会返回 `code: -1`）。OpenCLI 的 `eval` 跑在隔离环境里，所以脚本插一个 `<script>` 进主环境，结果写回 DOM 属性再读出来。
- 查询清单 `data/fetch/jg_queries.json` 按「榜单 × 行业 × 排序 × 时间窗」展开，再加一批关键词。已经抓过的文件会跳过，断了可以接着跑。一个查询约 30 秒；要快可以再开一个会话从尾部反向跑：`opencli browser jz2 open <同一地址>`，等页面加载完（否则报 `_webmsxyw is not a function`），再 `JG_SESSION=jz2 python3 scripts/fetch_juguang.py data/fetch/jg_queries.json --pages 3 --reverse`。
- 关键词榜的总数是 1000（按相关度召回再按指标排），只取前 3 页；行业榜总数是 100，3 页到底。
- 筛选配置（榜单、排序字段、行业树）随时可能改，接口报「排序字段不合法 / 时间周期不合法」时，先重新取 `attribute/item/list?platform=2` 和 `attribute/item/detail?type=tree&itemKey=spuIndustry&platform=2` 看字段。

### 4. 换算成素材库格式

`scripts/jg_library.py` 输出和 `data/library/` 一样的结构，引擎不用改主体：
- 一条笔记在每个榜单里的名次 = 一行「榜单记录」，榜单名写成 `产品种草·蜜饯果干·阅读量·近30日`（关键词榜写 `产品种草·搜「橘子」·阅读量·近30日`）。
- **榜内百分位** = 最好那一行的 (总数 − 名次) / (总数 − 1)，和旧库同一把尺子；爆款仍是 ≥ 80。
- 真实数字放 `extra`（reads / likes / collects / comments / fans / published / ad / pgy / srcImages / srcVideo），引擎原样带进 `notes`，页面已有的「赞 · 藏 · 评」直接显示。
- 发布日期用 `date` 字段（真实发布时间），不再从 ID 推。
- **媒体转存**（`python3 scripts/jg_media.py <slug>`，在第一次 `atlas_build.py` 之后跑）：brief 里用到的笔记（例子、拆解主例、规律例子），把 `srcImages` / `srcVideo` 下载（视频本来就是 720p H.264，原样传），传到 R2 `atlas-media/atlas/briefs/<slug>/<笔记 ID>/`（账号 15bb…，公开域名和封面同一个），写 `site/<slug>/media.json`；再跑一次 `atlas_build.py`，引擎把封面、`video` / `images` 换成 R2 地址。不在 brief 里的笔记不转存。改了例子要重跑这一步，而且要在签名过期前。

### 5. 数据边界（页面上要写清）

- 来源 = 聚光内容广场榜单（Top 100），抓取日期写在页面上；榜单是滚动的，过几天再抓结果会变。
- 有阅读、点赞、收藏、评论、粉丝；没有曝光量、阅读率的具体值，没有正文全文。
- 行业是投放方选的 SPU 行业，不等于笔记在讲这个品类：「蜜饯果干」榜里会混进联名、生活方式、吃播笔记，圈竞品时要按标题再筛。
- 相关性、可迁移度仍是判断分；爆品度、爆款率、规律证据是算出来的。
