# Atlas · 拍吧 竞品爆款 Brief

给品牌方的「竞品 + 爆款」brief 模板，第一份实例是 **拍吧（pepa）**：刷视频开心，拍视频赚钱。

一页从上往下读：我的产品 → 锁定竞品（相关性 × 爆品度）→ 竞品爆款（榜内百分位 × 可迁移度）→ 爆款拆解（账号 / 流量定量 + 定性 / 变现 / 结构）→ 规律与落地。

## 目录

| 路径 | 内容 |
|---|---|
| `final/` | 发布的页面（GitHub Pages 从这里部署） |
| `final/assets/data.js` | brief 数据，由脚本生成，不要手改 |
| `scripts/build_pepa.py` | 从 Atlas 素材库导出生成 `data.js` |
| `proto/` | 选型时的 5 页 × 4 方向原型 |
| `specs/` | 需求和定稿决策 |

## 重新生成数据

```sh
python3 scripts/build_pepa.py data/library final/assets/data.js
```

`data/library/`（items.json + det.json）是素材库导出，体积较大，没有放进仓库。

## 数据边界

数据来自小红书聚光 / 蒲公英 / 热门榜单记录：有榜内百分位、排名和投放目标，没有点赞数和粉丝数；发布日期由笔记 ID 推算。相关性和可迁移度是判断分，爆品度由榜单数据计算。
