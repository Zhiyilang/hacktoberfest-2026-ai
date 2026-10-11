# 🌱 GardenPlanner AI — Hacktoberfest 2026

> 参赛项目：**Hacktoberfest 2026 Open-Source AI Challenge**（DEV 平台，每周一期，共 5 周，$2,450 奖金池 / 17 位获奖者）。
> 主题方向：**Touch Grass** —— 用**开源 / 开放权重（open-weight）**模型，帮人离开屏幕、走进自然。

## 这是什么

一个**完全本地离线运行**的园艺规划命令行工具。输入你所在的城市、种植空间和难度偏好，它根据内置的农艺知识库，给出「这个月该种什么、和谁种在一起、注意什么」的实用计划。

- **核心推理默认用内置规则引擎**（零依赖、零网络、零账号），开箱即用。
- **可选接入本地 Ollama 开放权重模型**，把计划改写成更口语的自然语言建议——这体现了本项目的「open-weight 为核心」主张。
- 你的位置、花园数据**不离开本机**，隐私可控；技术栈**纯 Python 标准库**，零成本。

## 为什么是「开源创新 / Touch Grass」

- **让人放下屏幕**：输出是一份要去户外动手的种植清单，而不是又一个让人刷屏的 App。
- **开放权重优先**：模型可本地替换（Ollama / GGUF），Agent 行为完全由你掌控，不绑定任何闭源商业 API。
- **零云端依赖**：断网也能跑，适合阳台、庭院、社区花园等真实场景。

## 快速开始

```bash
# 需要 Python 3.10+
python main.py --city "Shanghai" --month 10 --space balcony --level easy
```

可选参数：

| 参数 | 说明 | 默认 |
|---|---|---|
| `--city` | 城市（内置气候参考，如 Shanghai/London/Sydney） | Shanghai |
| `--month` | 月份 1-12 | 当前月 |
| `--space` | `balcony` / `garden` / `indoor` / `any` | any |
| `--level` | `easy` / `medium` / `hard` / `any` | any |
| `--ollama MODEL` | 可选：本地 Ollama 模型名，做自然语言增强 | 关闭 |

示例输出：

```
🌱 Shanghai · 第 10 月（中秋）
   气候带 ~8 / 北半球

   推荐播种 / 栽植（5 项）：
   • 生菜 ［easy｜balcony］
     搭档：胡萝卜、草莓
     贴士：速生叶菜，凉爽季节品质最佳。
   • 菠菜 ［easy｜balcony］
     搭档：草莓、豌豆
     贴士：耐寒，秋播越冬，早春采收。
   • 大蒜 ［easy｜balcony］
     搭档：草莓、番茄
     贴士：秋播越冬，天然抑菌，几乎零维护。
   • 香菜 ［easy｜balcony］
     搭档：菠菜
     贴士：耐寒香草，高温易抽薹。
   • 豆芽 ［easy｜indoor］
     搭档：—
     贴士：全年室内水培，3-5 天即可采收，零门槛。
```

南半球城市（如 Sydney）会自动翻转季节：输入 4 月会得到北半球 10 月的秋播计划。

## 用本地开放权重模型增强（可选）

```bash
# 先本地装好 Ollama 并拉一个模型，例如：
ollama pull llama3.2
# 再让工具用模型改写计划：
python main.py --city "London" --month 3 --ollama llama3.2
```

没有 Ollama 也完全不影响使用——规则引擎会直接输出完整计划。

## 参与 Hacktoberfest / 贡献

欢迎提交 PR：补充更多城市气候数据、扩展植物知识库、增加病虫害提醒、做 Web/移动端封装等。
所有贡献遵循 Hacktoberfest 的 `hacktoberfest-accepted` 标签约定。

> 许可证：MIT（开源）
