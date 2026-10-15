"""GardenPlanner AI — English knowledge layer for the web demo.

The CLI (main.py) ships a Chinese agronomy knowledge base. The hosted web
demo and the international hackathon entries need the same knowledge in
English, so this module carries a parallel English map for every plant,
tip, pest, task and label, plus ``en_plan()`` which converts a plan dict
produced by ``main.build_plan()`` into English.

Invariant enforced by eval.py: every plant, every monthly task and every
companion token in main.PLANTS / main.TASKS has an English entry here —
the maps can never silently drift from the knowledge base.
"""
from __future__ import annotations

import main as _gp

# ---------------------------------------------------------------------------
# plant names (zh -> en)
# ---------------------------------------------------------------------------
EN_PLANT = {
    "番茄": "Tomato", "黄瓜": "Cucumber", "生菜": "Lettuce", "菠菜": "Spinach",
    "胡萝卜": "Carrot", "土豆": "Potato", "辣椒": "Chili pepper",
    "罗勒": "Basil", "豌豆": "Pea", "南瓜": "Pumpkin", "草莓": "Strawberry",
    "大蒜": "Garlic", "香菜": "Coriander", "豆芽": "Bean sprouts",
    "薄荷": "Mint",
}

# companion / antagonist tokens (zh -> en). Covers every token referenced by
# any friends/foes list in main.PLANTS, including composite entries.
EN_COMPANION = {
    "罗勒": "basil", "胡萝卜": "carrot", "marigold金盏花": "marigold",
    "玉米": "corn", "白菜/甘蓝": "cabbage", "豆类": "beans", "菜豆": "green beans",
    "番茄": "tomato", "马铃薯": "potato", "草莓": "strawberry", "葱蒜": "alliums",
    "芹菜": "celery", "豌豆": "pea", "菠菜": "spinach", "甜菜": "beet",
    "香菜/芹菜": "coriander / celery", "茼蒿": "garland chrysanthemum",
    "卷心菜": "cabbage", "南瓜": "pumpkin", "胡椒": "pepper", "茴香": "fennel",
    "芸香": "rue", "大葱": "welsh onion", "甘蓝": "cabbage",
    "几乎所有蔬菜": "almost all vegetables", "所有香草（侵略性）": "all herbs (invasive)",
    "白菜": "chinese cabbage", "黄瓜": "cucumber", "生菜": "lettuce",
    "辣椒": "chili pepper", "土豆": "potato", "大蒜": "garlic",
    "香菜": "coriander", "豆芽": "bean sprouts", "薄荷": "mint",
}

# ---------------------------------------------------------------------------
# tips & pests (zh plant name -> en)
# ---------------------------------------------------------------------------
EN_TIPS = {
    "番茄": "Warm-season crop; transplant after the last frost and provide support.",
    "黄瓜": "Vining growth; needs a trellis and steady water.",
    "生菜": "Fast leafy green; best quality in cool seasons.",
    "菠菜": "Cold-hardy; autumn sowing overwinters for an early-spring harvest.",
    "胡萝卜": "Loosen deep soil; avoid fresh manure (causes forking).",
    "土豆": "Tuber crop; do not follow itself in rotation.",
    "辣椒": "Loves heat; long seedling stage, feed heavily while fruiting.",
    "罗勒": "Aromatic herb that repels pests; keep warm and sheltered from wind.",
    "豌豆": "Fixes nitrogen; sow in cool months on a low trellis.",
    "南瓜": "Space-hungry; the classic Three Sisters companion.",
    "草莓": "Perennial; plant in autumn for a spring harvest, needs sun.",
    "大蒜": "Autumn-sown, overwinters; naturally antibacterial, near-zero care.",
    "香菜": "Cold-tolerant herb; bolts quickly in heat.",
    "豆芽": "Year-round indoor water culture; harvest in 3-5 days, zero skill.",
    "薄荷": "Aggressive spreader; keep it potted to contain the roots.",
}

EN_PESTS = {
    "番茄": "Water at the base to prevent early blight; marigolds deter nematodes; soapy water on leaf undersides for aphids.",
    "黄瓜": "Spray powdery mildew with 1:9 milk-water; avoid wetting the leaves.",
    "生菜": "Yellow sticky traps for aphids; control water and ventilate in high humidity.",
    "菠菜": "Hang yellow boards for leafminers; choose resistant varieties and avoid dense sowing for downy mildew.",
    "胡萝卜": "Insect netting plus alliums deter carrot fly; cracking comes from erratic watering.",
    "土豆": "Dig drainage channels in rainy spells for late blight; hand-pick beetles.",
    "辣椒": "Spider mites appear in dry weather — raise humidity and mist; soapy water for aphids.",
    "罗勒": "Almost pest-free; harvest before flowering for the best flavour.",
    "豌豆": "Pick airy spots against powdery mildew; net seedlings against birds.",
    "南瓜": "Bag the fruit against fruit fly; milk-water spray for powdery mildew.",
    "草莓": "Control humidity against grey mould; beer traps at night for slugs.",
    "大蒜": "Almost none; rotate crops to prevent soil-borne disease.",
    "香菜": "Yellow boards for aphids; bolting means it is done — pick young leaves often.",
    "豆芽": "Soilless culture avoids contamination; change water daily against slime.",
    "薄荷": "Almost none; potting prevents runner sprawl.",
}

# ---------------------------------------------------------------------------
# monthly task checklist (northern-hemisphere month -> en tasks)
# ---------------------------------------------------------------------------
EN_TASKS = {
    1: ["Plan the year's rotations", "Start tomato/chili seedlings indoors", "Tidy tools and the compost pile"],
    2: ["Transplant cold-hardy greens", "Sow potato/pea", "Supplementary light for seedlings"],
    3: ["Peak early-spring sowing", "Plant out onion/garlic", "Set up trellises for climbers"],
    4: ["Transplant tomato after late frost", "Sow beans/corn", "Watch for aphids"],
    5: ["Plant out summer vegetables", "Lay mulch to hold moisture", "Set a watering rhythm"],
    6: ["Shade in the heat wave", "Harvest cherry tomatoes", "Prevent powdery mildew"],
    7: ["Peak-summer care", "Prepare for autumn sowing", "Water-saving irrigation"],
    8: ["Sow autumn greens (lettuce/spinach)", "Harvest garlic/onion", "Take herb cuttings"],
    9: ["Peak autumn sowing", "Plant out strawberry", "Gather compost"],
    10: ["Plant autumn garlic/wheat", "Harvest late crops", "Mulch for winter"],
    11: ["Clear spent stalks", "Turn soil and add base fertilizer", "Protect seedlings from cold"],
    12: ["Insulate the growing space", "Plan next year", "Indoor sprout tray"],
}

# ---------------------------------------------------------------------------
# labels
# ---------------------------------------------------------------------------
EN_SEASON = {
    "隆冬": "deep winter", "晚冬": "late winter", "早春": "early spring",
    "仲春": "mid spring", "晚春": "late spring", "初夏": "early summer",
    "盛夏": "midsummer", "夏末": "late summer", "初秋": "early autumn",
    "中秋": "mid autumn", "深秋": "late autumn", "当季": "in season",
}
EN_LABELS = {
    "recommended": "Recommended sowing / planting",
    "companions": "Companions",
    "foes": "Keep apart",
    "tip": "Tip",
    "pests": "Pests",
    "tasks": "This month's checklist",
    "hemisphere_n": "Northern Hemisphere",
    "hemisphere_s": "Southern Hemisphere",
    "zone": "Hardiness zone",
    "no_picks": "Nothing matches this month exactly — tend what you have or plan ahead.",
    "unknown_city": "unknown city (temperate default applied)",
}


def companion_en(token: str) -> str:
    """Translate one friends/foes token; raises KeyError on unknown tokens."""
    return EN_COMPANION[token.strip()]


def en_plan(plan: dict) -> dict:
    """Convert a main.build_plan() dict into an English-structured dict."""
    picks = []
    for p in plan["picks"]:
        picks.append({
            "name": EN_PLANT[p["name"]],
            "name_zh": p["name"],
            "level": p["level"],
            "space": p["space"],
            "companions": [companion_en(x) for x in p["friends"]],
            "foes": [companion_en(x) for x in p["foes"]],
            "tip": EN_TIPS[p["name"]],
            "pests": EN_PESTS[p["name"]],
        })
    return {
        "city": plan["city"],
        "zone": plan["zone"],
        "southern": plan["southern"],
        "month": plan["month"],
        "target_month": plan["target_month"],
        "season": EN_SEASON.get(plan["season"], plan["season"]),
        "hemisphere": EN_LABELS["hemisphere_s"] if plan["southern"] else EN_LABELS["hemisphere_n"],
        "city_note": "" if plan["city"].strip().lower() in _gp.CITIES else EN_LABELS["unknown_city"],
        "picks": picks,
        "tasks": list(EN_TASKS.get(plan["target_month"], [])),
        "labels": {k: EN_LABELS[k] for k in
                   ("recommended", "companions", "foes", "tip", "pests", "tasks", "no_picks")},
    }
