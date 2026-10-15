# 🌱 GardenPlanner AI — Hacktoberfest 2026

[![CI](https://github.com/Zhiyilang/hacktoberfest-2026-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/Zhiyilang/hacktoberfest-2026-ai/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

> Entry for the **Hacktoberfest 2026 Open-Source AI Challenge** (DEV, weekly, 5 weeks, $2,450 pool / 17 winners).
> Theme: **Touch Grass** — use open-weight models to help people step away from screens and into nature.

**中文说明见 [README.zh.md](README.zh.md)。**

## What is this

An **offline-first gardening planner CLI**. Tell it your city, growing space, and skill level; it returns a monthly plan from a built-in agronomy knowledge base: *what to sow now, what to plant next to it, what to keep apart, which pests to watch, and what chores the month demands*.

- **Rule engine by default** — zero dependencies, zero network, zero accounts. Works out of the box.
- Built-in **companion (friends) / antagonistic (foes)** matrices, plus **pest tips** and a **monthly task checklist**.
- **Optional local Ollama open-weight model** rewrites the plan in friendly plain language — the project's core claim is *open-weight first*: swap the model locally, no closed-source API lock-in.
- Your location and garden data **never leave your machine**. Pure Python standard library, zero cost.

## Why it fits "Touch Grass"

- **Gets you off the screen**: the output is a hands-on planting checklist you act on outdoors, not another feed to scroll.
- **Open-weight first**: model is locally replaceable (Ollama / GGUF); behavior is fully under your control.
- **No cloud dependency**: runs disconnected — balcony, backyard, or community garden.

## Quick start

```bash
# Python 3.10+
python main.py --city "Shanghai" --month 10 --space balcony --level easy
```

| Flag | Meaning | Default |
|---|---|---|
| `--city` | city with built-in climate reference (Shanghai/London/Sydney/...) | Shanghai |
| `--month` | month 1-12 | current month |
| `--space` | `balcony` / `garden` / `indoor` / `any` | any |
| `--level` | `easy` / `medium` / `hard` / `any` | any |
| `--ollama MODEL` | optional local Ollama model for plain-language rewrite | off |

Sample output (truncated):

```
🌱 Shanghai · Month 10 (Mid-Autumn)
   Hardiness zone ~8 / Northern Hemisphere

   Recommended sowing / planting (5):
   • Lettuce ［easy｜balcony］
     Companions: carrot, strawberry, alliums
     Avoid nearby: celery
     Tip: fast leafy green, best in cool seasons.
     Pests: yellow sticky traps for aphids; control water in high humidity.
   ...
   📋 Monthly task checklist:
     ☐ Plant autumn garlic/wheat
     ☐ Harvest late-season crops
     ☑ Mulch for winter
```

Southern-hemisphere cities (e.g. Sydney) flip the seasons automatically: month 4 yields the northern-hemisphere month-10 autumn sowing plan.

## Hosted demo (web)

A zero-dependency web UI (pure standard library) ships alongside the CLI:

```bash
python app.py            # reads PORT (default 10000), binds 0.0.0.0
```

- English-first UI with a 中文 toggle; the plan renders as cards
  (companions / keep-apart / tip / pests) plus the monthly checklist.
- One-click deploy via `render.yaml` (Render Blueprint, free plan).
- The CLI remains the primary interface; the web layer is presentation
  only — the knowledge base lives in `main.py` and the English map in
  `i18n.py`.

## Tests & quality

```bash
python eval.py   # 43 assertions: hemisphere maths, plan determinism,
                 # data integrity, English-layer coverage, real-subprocess
                 # CLI, and real-HTTP web endpoint round-trips
```

CI runs the same suite on Python 3.10 / 3.11 / 3.12 (`.github/workflows/ci.yml`).

## Optional: enhance with a local open-weight model

```bash
ollama pull llama3.2
python main.py --city "London" --month 3 --ollama llama3.2
```

Without Ollama nothing breaks — the rule engine emits the complete plan.

## Hacktoberfest contributions

PRs welcome: more city climate data, an expanded plant database, pest reminders, web/mobile wrappers. Follow the `hacktoberfest-accepted` label convention.

> License: MIT
