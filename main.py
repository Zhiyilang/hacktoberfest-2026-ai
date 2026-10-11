#!/usr/bin/env python3
"""GardenPlanner AI — 离线优先的园艺规划命令行工具（Hacktoberfest 2026）。

核心理念（贴合 Hacktoberfest 2026 主题 *Touch Grass*）：
用**开源 / 开放权重（open-weight）**模型，帮人放下屏幕、走进自然。

本工具完全本地运行：
- 内置一份轻量农艺知识库，零网络、零付费 API、零账号即可给出当月种植计划。
- 内置**伴生（friends）/ 相克（foes）**矩阵与**病虫害贴士（pests）**。
- 生成**当月任务清单**（播种 / 定植 / 采收 / 养护）。
- 可选接入本地 Ollama 开放权重模型，把计划改写成更口语的自然语言建议；
  没有模型环境时，规则引擎照样产出完整计划（开箱即用）。

设计原则：隐私可控（数据不离本机）、零成本（纯 Python 标准库）、可换模型。
"""
from __future__ import annotations

import argparse
import datetime as _dt
import shutil
import subprocess
import sys

# ---------------------------------------------------------------------------
# 内置城市气候参考：(气候带 1-10, 是否南半球)
# 用于把温带（北半球）的播种窗口按地区做平移/翻转。
# ---------------------------------------------------------------------------
CITIES: dict[str, tuple[int, bool]] = {
    "shanghai": (8, False), "beijing": (6, False), "guangzhou": (10, False),
    "chengdu": (8, False), "harbin": (4, False), "kunming": (9, False),
    "shenzhen": (10, False), "wuhan": (8, False),
    "london": (8, False), "paris": (8, False), "new york": (6, False),
    "san francisco": (9, False), "tokyo": (8, False), "moscow": (4, False),
    "sydney": (10, True), "auckland": (10, True), "sao paulo": (11, True),
}

# ---------------------------------------------------------------------------
# 植物知识库（北半球温带基准：播种月份 1-12）
# space: balcony(阳台) / garden(庭院) / indoor(室内)
# level: easy / medium / hard
# friends: 伴生（相邻种植互利）  foes: 相克（应避免相邻）  pests: 病虫害贴士
# ---------------------------------------------------------------------------
PLANTS: list[dict] = [
    {"name": "番茄", "sow": [2, 3, 4], "space": "garden", "level": "medium",
     "friends": ["罗勒", "胡萝卜", " marigold金盏花"], "foes": ["玉米", "白菜/甘蓝"],
     "note": "喜温，霜冻后定植，需支架。",
     "pests": "基部浇水防早疫病；金盏花驱线虫；发现蚜虫用肥皂水喷叶背。"},
    {"name": "黄瓜", "sow": [3, 4, 5], "space": "garden", "level": "easy",
     "friends": ["豆类", "玉米", "菜豆"], "foes": ["番茄", "马铃薯"],
     "note": "攀援生长，需搭架与充足水分。",
     "pests": "白粉病用牛奶水（1:9）喷施；避免叶面积水。"},
    {"name": "生菜", "sow": [2, 3, 8, 9, 10], "space": "balcony", "level": "easy",
     "friends": ["胡萝卜", "草莓", "葱蒜"], "foes": ["芹菜"],
     "note": "速生叶菜，凉爽季节品质最佳。",
     "pests": "蚜虫用黄板诱捕；高湿易烂心，控水通风。"},
    {"name": "菠菜", "sow": [2, 3, 9, 10, 11], "space": "balcony", "level": "easy",
     "friends": ["草莓", "豌豆", "生菜"], "foes": ["甜菜"],
     "note": "耐寒，秋播越冬，早春采收。",
     "pests": "潜叶蝇挂黄板；霜霉病选抗病种、避免密植。"},
    {"name": "胡萝卜", "sow": [2, 3, 7, 8, 9], "space": "garden", "level": "easy",
     "friends": ["生菜", "番茄", "葱蒜"], "foes": ["香菜/芹菜", "茼蒿"],
     "note": "深翻土，避免新鲜粪肥（易分叉）。",
     "pests": "胡萝卜蝇用防虫网+葱蒜驱避；根裂因水分剧变。"},
    {"name": "土豆", "sow": [1, 2, 3], "space": "garden", "level": "easy",
     "friends": ["豆类", "卷心菜", "玉米"], "foes": ["番茄", "南瓜"],
     "note": "块茎作物，忌连作。",
     "pests": "晚疫病雨季挖沟排水；甲虫手工摘除。"},
    {"name": "辣椒", "sow": [2, 3], "space": "balcony", "level": "medium",
     "friends": ["罗勒", "番茄", "葱蒜"], "foes": ["豆类", "茴香"],
     "note": "喜热，育苗期长，结果期需肥。",
     "pests": "红蛛蛛干燥时发生，增湿+喷水；蚜虫肥皂水。"},
    {"name": "罗勒", "sow": [3, 4, 5], "space": "balcony", "level": "easy",
     "friends": ["番茄", "辣椒", "胡椒"], "foes": ["茴香", "芸香"],
     "note": "香草，驱虫且提味，温暖避风。",
     "pests": "几乎无虫害；花前采收风味最佳。"},
    {"name": "豌豆", "sow": [1, 2, 3, 9, 10], "space": "garden", "level": "easy",
     "friends": ["菠菜", "胡萝卜", "玉米"], "foes": ["葱蒜", "番茄"],
     "note": "固氮，冷凉季播种，搭矮架。",
     "pests": "白粉病选通风地块；苗期防鸟啄（覆网）。"},
    {"name": "南瓜", "sow": [3, 4, 5], "space": "garden", "level": "medium",
     "friends": ["玉米", "豆类", "大葱"], "foes": ["土豆", "番茄"],
     "note": "占地大，三姐妹种植法经典搭配。",
     "pests": "瓜实蝇套袋；白粉病牛奶水喷施。"},
    {"name": "草莓", "sow": [8, 9], "space": "balcony", "level": "medium",
     "friends": ["生菜", "菠菜", "葱蒜"], "foes": ["甘蓝", "番茄"],
     "note": "多年生，秋植翌年春收，需日照。",
     "pests": "灰霉病控湿；蛞蝓夜间啤酒陷阱诱杀。"},
    {"name": "大蒜", "sow": [9, 10, 11], "space": "balcony", "level": "easy",
     "friends": ["草莓", "番茄", "几乎所有蔬菜"], "foes": ["豆类", "豌豆"],
     "note": "秋播越冬，天然抑菌，几乎零维护。",
     "pests": "几乎无；轮作防土传病害。"},
    {"name": "香菜", "sow": [3, 4, 8, 9, 10], "space": "balcony", "level": "easy",
     "friends": ["菠菜", "生菜"], "foes": ["胡萝卜", "茴香"],
     "note": "耐寒香草，高温易抽薹。",
     "pests": "蚜虫黄板；抽薹即老，勤采嫩叶。"},
    {"name": "豆芽", "sow": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "space": "indoor", "level": "easy",
     "friends": [], "foes": [],
     "note": "全年室内水培，3-5 天即可采收，零门槛。",
     "pests": "无土栽培避免污染；每日换水防黏滑。"},
    {"name": "薄荷", "sow": [3, 4, 5, 9], "space": "balcony", "level": "easy",
     "friends": ["番茄", "白菜"], "foes": ["所有香草（侵略性）"],
     "note": "侵略性强，建议盆栽限根。",
     "pests": "几乎无；盆栽防走茎泛滥。"},
]

# 当月通用任务清单（按北半球季节给出建议动作）
TASKS: dict[int, list[str]] = {
    1: ["规划全年轮作", "室内育苗（番茄/辣椒）", "整理工具与堆肥"],
    2: ["移栽耐寒叶菜", "开始土豆/豌豆播种", "育苗补光"],
    3: ["早春播种高峰", "定植洋葱/大蒜", "架设为攀援作物搭架"],
    4: ["晚霜后定植番茄", "播种豆类/玉米", "防治蚜虫"],
    5: ["夏季蔬菜定植", "覆盖地膜保墒", "定时浇水"],
    6: ["高温季遮阴", "采收樱桃番茄", "防白粉病"],
    7: ["盛夏养护", "秋播育苗准备", "节水灌溉"],
    8: ["秋播叶菜（生菜/菠菜）", "采收大蒜/洋葱", "扦插香草"],
    9: ["秋季播种高峰", "定植草莓", "收集堆肥"],
    10: ["秋植大蒜/小麦", "采收晚熟作物", "覆盖越冬 mulch"],
    11: ["清理枯秆", "翻地施底肥", "保护幼苗防寒"],
    12: ["设施保温", "规划来年", "室内芽苗菜"],
}


def _adjust_month(month: int, southern: bool) -> int:
    """南半球季节相反：月份整体平移 6 个月。"""
    if southern:
        return ((month + 5) % 12) + 1
    return month


def build_plan(city: str, month: int, space: str, level: str) -> dict:
    ckey = city.strip().lower()
    zone, southern = CITIES.get(ckey, (8, False))
    target = _adjust_month(month, southern)

    picks = []
    for p in PLANTS:
        if target not in p["sow"]:
            continue
        if space != "any" and p["space"] != space and not (space == "balcony" and p["space"] == "indoor"):
            continue
        if level == "easy" and p["level"] != "easy":
            continue
        picks.append(p)

    season = {12: "隆冬", 1: "隆冬", 2: "晚冬", 3: "早春", 4: "仲春", 5: "晚春",
             6: "初夏", 7: "盛夏", 8: "夏末", 9: "初秋", 10: "中秋", 11: "深秋"}.get(target, "当季")
    return {
        "city": city, "zone": zone, "southern": southern,
        "month": month, "target_month": target, "season": season,
        "picks": picks,
        "tasks": TASKS.get(target, []),
    }


def render(plan: dict) -> str:
    lines = []
    hemi = "南半球" if plan["southern"] else "北半球"
    lines.append(f"🌱 {plan['city']} · 第 {plan['target_month']} 月（{plan['season']}）")
    lines.append(f"   气候带 ~{plan['zone']} / {hemi}")
    lines.append("")
    if not plan["picks"]:
        lines.append("   本月没有特别匹配的播种项，可养护已有作物或规划下月。")
    else:
        lines.append(f"   推荐播种 / 栽植（{len(plan['picks'])} 项）：")
        for p in plan["picks"]:
            friends = "、".join(x.strip() for x in p["friends"]) if p["friends"] else "—"
            foes = "、".join(x.strip() for x in p["foes"]) if p["foes"] else "—"
            lines.append(f"   • {p['name']} ［{p['level']}｜{p['space']}］")
            lines.append(f"     搭档(伴生): {friends}")
            lines.append(f"     相克(避免相邻): {foes}")
            lines.append(f"     贴士: {p['note']}")
            lines.append(f"     病虫害: {p['pests']}")
    lines.append("")
    lines.append("   📋 当月任务清单：")
    for t in plan["tasks"]:
        lines.append(f"     ☐ {t}")
    return "\n".join(lines)


def maybe_enhance_with_model(plan_text: str, model: str) -> str:
    """可选：用本地 Ollama 开放权重模型把计划改写成自然语言。无模型则原样返回。"""
    if not shutil.which("ollama"):
        return plan_text
    try:
        proc = subprocess.run(
            ["ollama", "run", model,
             "把下面的园艺计划用亲切的口语改写给新手看：\n" + plan_text],
            capture_output=True, text=True, timeout=60,
        )
        return proc.stdout.strip() or plan_text
    except Exception:
        return plan_text


def main() -> int:
    p = argparse.ArgumentParser(
        description="离线园艺规划 CLI（Hacktoberfest 2026 · Touch Grass）")
    p.add_argument("--city", default="Shanghai", help="城市，如 Shanghai / London / Sydney")
    p.add_argument("--month", type=int, default=_dt.datetime.now().month,
                   help="月份 1-12，默认当前月")
    p.add_argument("--space", default="any",
                   choices=["any", "balcony", "garden", "indoor"],
                   help="种植空间，默认 any")
    p.add_argument("--level", default="any",
                   choices=["any", "easy", "medium", "hard"],
                   help="难度过滤，默认 any")
    p.add_argument("--ollama", metavar="MODEL", default=None,
                   help="可选：本地 Ollama 模型名（如 llama3.2），做自然语言增强")
    args = p.parse_args()

    if not 1 <= args.month <= 12:
        print("月份需在 1-12 之间", file=sys.stderr)
        return 2

    plan = build_plan(args.city, args.month, args.space, args.level)
    text = render(plan)
    if args.ollama:
        text = maybe_enhance_with_model(text, args.ollama)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
