GardenPlanner AI is an offline-first gardening planner built for the Hacktoberfest 2026 Open-Source AI Challenge (theme: Touch Grass). The idea is simple: use open-weight models to help people step away from screens and into nature, not pull them deeper in.

Most gardening apps send your location and garden data to a cloud and lock the brain behind a paid API. This tool does the opposite. It runs 100% offline on pure Python standard library, no network, no account, no cost. It optionally rewrites the plan with a local Ollama model; without it, the built-in rule engine still produces a complete plan. Your city and garden data never leave your machine, and the output is a hands-on planting checklist you act on outside.

How to run it:

```bash
python main.py --city "Shanghai" --month 10 --space balcony --level easy
```

It returns a personalized monthly planting plan with companion plants and tips, and flips seasons for the Southern Hemisphere automatically. You can also enhance it with a local model:

```bash
ollama pull llama3.2
python main.py --city "London" --month 3 --ollama llama3.2
```

The repository is here: https://github.com/Zhiyilang/hacktoberfest-2026-ai

Contributions are welcome for Hacktoberfest: more city climate data, an expanded plant database, pest reminders, or web/mobile wrappers. Look for the hacktoberfest-accepted label. Let's touch grass, with open source.
