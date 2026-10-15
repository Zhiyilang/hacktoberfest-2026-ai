# GardenPlanner AI — Dubai Demo Video Storyboard (3:00, English)
## Create AI Agents Championship · Best Personal AI Agent

**Rendered video:** `gardenplanner_demo.mp4` (repo root) — the English CLI (`main.py --lang en`) planning a Shanghai October, the month's checklist, and `python eval.py` (45/45). Drop it into the submission; add a voiceover to the storyboard below if you want to submit the narrated version instead.

Format: screen recording (terminal + hosted web UI) with voiceover.
Total target: 2:50–3:00. Record at 1080p, terminal font ≥ 14pt.
No background music over the voiceover; keep room tone clean.

---

## 0:00–0:20 — Hook (face or title card + terminal)

**Visual:** Title card — 🌱 GardenPlanner AI — "The gardening agent that
never phones home." Cut to a terminal.

**VO:** "Every month, every gardener answers the same question: what do I
sow now, what do I plant next to it, what should I keep apart? Most tools
answer with a blog post — and want your location, an account, and a
subscription. GardenPlanner is a personal agent that answers in one
second — offline, private, and free."

## 0:20–0:55 — The agent loop (terminal)

**Visual:** Run the CLI, full-screen:

```bash
python main.py --city "Shanghai" --month 10 --space balcony --level easy
```

Scroll slowly through the output: 5 recommended plants with companions,
keep-apart, tips, pests, and the monthly checklist.

**VO:** "It perceives your city — climate zone and hemisphere — your
space, and your skill level. Then it plans against a curated agronomy
knowledge base: companion matrices, antagonist matrices, pest
intelligence, and a seasonal task checklist. Every recommendation carries
its reasoning — why basil beside tomato, why potato away from tomato."

## 0:55–1:20 — The detail that proves it's real (terminal)

**Visual:** Second run — the southern-hemisphere flip:

```bash
python main.py --city Sydney --month 4 --space balcony --level easy
```

Point at the header: month 4 in Sydney yields the northern month-10
autumn plan.

**VO:** "Sydney in April is autumn, not spring. The season flips
correctly — a detail most agronomy tools get wrong, and one our test
suite asserts explicitly."

## 1:20–1:50 — Hosted web demo (browser)

**Visual:** The hosted URL (Render). Switch language with the 中文
button; adjust city/month/space; show the card layout.

**VO:** "The same agent ships as a hosted web demo — English first, with
a Chinese toggle for my own community. The default path makes zero
network calls: your location and garden data never leave your machine.
That is not a privacy policy — it is the code path."

## 1:50–2:20 — Engineering proof (terminal)

**Visual:**

```bash
python eval.py
```

Let it run to `Ran 43 tests ... OK`. Quick montage: repo file tree,
CI badge (3.10/3.11/3.12 all green), MIT license.

**VO:** "Zero dependencies — pure Python standard library. Forty-three
assertions cover hemisphere mathematics, plan determinism, data
integrity, English-layer coverage, the CLI as a real subprocess, and the
web endpoints over real HTTP. Same inputs, byte-identical plans. CI runs
green on three Python versions. MIT licensed, bilingual documentation."

## 2:20–2:50 — Close (title card)

**Visual:** Title card with repo URL + hosted URL + the three Dubai
entries line: "GardenPlanner — Best Personal AI Agent".

**VO:** "Curated, not crowd-sourced: fifteen plants, seventeen cities —
a small, correct, testable core over a large, unverified one. This is a
pre-commercial prototype built for the championship. Agents should
amplify people, not extract from them. GardenPlanner plans your month —
and keeps your garden yours."

---

## Production checklist

- [ ] Terminal theme: light background, high contrast (readable on phones).
- [ ] Zoom the terminal to 110–125% during the plan scroll.
- [ ] Hosted demo deployed **before** recording (URL shown on the close card).
- [ ] Total runtime ≤ 3:00; voiceover recorded in one take if possible.
- [ ] Export 1080p MP4; upload unlisted (YouTube) or attach directly per platform rules.
- [ ] Video metadata: title "GardenPlanner AI — the gardening agent that never phones home (Dubai Create AI Agents entry)".

## Fallback plan

If the hosted demo is not deployed at recording time: record the CLI
segments only, keep the web segment as a still screenshot with VO, and
note "hosted demo: link in submission". Deploy before the December
submission deadline regardless — the entry form asks for a working
prototype link.
