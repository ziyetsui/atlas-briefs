# Atlas · 竞品爆款 Brief

给品牌方的「竞品 + 爆款」brief 模板。现有两份：

- **拍吧（pepa）**：刷视频开心，拍视频赚钱
- **Ancher（ancher.ai）**：把刷到、存下的内容一键变成视频、网页、播客、图片、文章

一页从上往下读：我的产品 → 锁定竞品（相关性 × 爆品度）→ 竞品爆款（榜内百分位 × 可迁移度）→ 爆款拆解（账号 / 流量定量 + 定性 / 变现 / 结构）→ 规律与落地。

## 目录

| 路径 | 内容 |
|---|---|
| `site/` | 发布的站点（GitHub Pages 从这里部署）：首页列出所有 brief |
| `site/<slug>/` | 一份 brief：`index.html`（模板副本）+ `data.js`（脚本生成，不要手改） |
| `site/assets/` | 所有 brief 共用的样式和组件 |
| `site/briefs.js` | 首页的 brief 列表 |
| `template/brief.html` | 通用 brief 页面；改它，再跑 `scripts/sync_template.py` 同步到每个 brief |
| `briefs/<slug>.py` | 品牌配置：候选池、打分、形式规则、例子、拆解、规律（所有判断都在这里） |
| `scripts/atlas_build.py` | 引擎：读配置 + 素材库，算出统计、散点、证据，写 `site/<slug>/data.js` |
| `scripts/sync_template.py` | 把模板复制到每个 brief |
| `proto/` | 选型时的 5 页 × 4 方向原型 |
| `specs/` | 需求、定稿决策、制作手册（`0003-brief-runbook.md`） |

## 做一份新 brief

按 `specs/0003-brief-runbook.md` 写 `briefs/<slug>.py`，然后：

```sh
python3 scripts/atlas_build.py <slug>   # 例：pepa / ancher
python3 scripts/sync_template.py
```

再在 `site/briefs.js` 加一行。

`data/library/`（items.json + det.json）是素材库导出，体积较大，没有放进仓库。

## 数据边界

数据来自小红书聚光 / 蒲公英 / 热门榜单记录：有榜内百分位、排名和投放目标，没有点赞数和粉丝数；发布日期由笔记 ID 推算。相关性和可迁移度是判断分，爆品度由榜单数据计算。
