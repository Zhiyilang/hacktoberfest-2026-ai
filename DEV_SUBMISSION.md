# GardenPlanner AI — W4 提交清单（DEV 现金挑战）

> 赛事：Hacktoberfest 2026 Open-Source AI Challenge（DEV 平台）
> 周池：**$2,450 / 17 位获奖者**；W4 窗口 **2026-10-26 ~ 10-31**（美东时间）
> 仓库：https://github.com/Zhiyilang/hacktoberfest-2026-ai

## 硬性资格（缺一即废）

- [ ] **必须同时打两个标签**：`#devchallenge` **和** `#hf26challenge`（只打一个不计入奖金评选，官方多次强调）
- [ ] 文章**发布日落在 W4 窗口内**（10-26~10-31）。早发或晚发都不算 W4
- [ ] 公开仓库 + MIT 许可证（已就绪）
- [ ] 内容是**原创**且与 Touch Grass / open-weight 主题相关（已就绪：本地开放权重优先）

## 发布步骤（用户侧，约 10 分钟）

1. 登录 DEV.to → New Post
2. 标题用：
   `GardenPlanner AI: an offline-first Touch Grass planner (open-weight, zero dependencies)`
3. 正文粘贴 `DEV_ARTICLE.md` 全文（已写好，含仓库链接与运行命令）
4. 标签（Tags）**必须包含**：`devchallenge`、`hf26challenge`，另可加 `ai`、`python`、`opensource`、`hacktoberfest`
5. 封面色图：用 `python main.py --city Shanghai --month 10` 的终端截图（真实输出最有说服力）
6. Publish，然后把文章 URL 贴回给我登记

## 内容卖点（已在文章中）

- 反潮流定位：别家园艺 App 上传位置+付费 API；本项目 100% 离线、纯标准库
- open-weight 为核心：可选 Ollama 本地改写，不绑定闭源 API
- 工程可信度：**43 断言 eval**（含 Web 端点真实 HTTP 往返）+ 三版本 CI（文章已提，仓库徽标可见）
- **新增可点 demo**：`app.py` 零依赖 Web 界面（英文优先 + 中文切换）+ `render.yaml` 一键部署——文章里放活链接，评委/读者可直接体验
- 南半球自动季节翻转 + 伴生/相克矩阵 + 当月任务清单

## 时间线提醒

| 日期(北京) | 事项 |
|---|---|
| 10-19~25 | W3 窗口：ScrubPilot 已就绪（仓已推 github.com/Zhiyilang/scrubpilot，eval 57/57）——若要发 W3 用 `scrubpilot/DEV_POST.md`，与本文错开（一项目一周一发更稳） |
| **10-26** | **W4 开启 → 立即发本文**（周池先到先得不假，但窗口只有 6 天，别拖到最后一天） |
| 10-31 | W4 截止 |

## 备注

- Hacktoberfest 2026 起 PR 不再计奖励（2026-08 废除），现金只在 DEV 周赛；本文是现金线，与贴纸线无关
- 若 W4 已发过别的项目（一项目一周一发更稳），保留本文给 W5（10-26~10-31 之后的窗口以官方为准）
