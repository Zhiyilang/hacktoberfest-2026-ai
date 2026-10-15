# GardenPlanner AI — Dubai "Create AI Agents Championship" Entry Pack
## Category: Best Personal AI Agent

> Working title: **"The gardening agent that never phones home."**
> An offline-first personal agent that plans what you sow, plant, pair and
> protect — every month, for your climate — without an account, a network
> connection, or a single byte leaving your machine.

---

## 1. Why this entry fits "Best Personal AI Agent"

| Official judging lens | How GardenPlanner answers it |
|---|---|
| **Personal usefulness** | A concrete, recurring personal task — "what do I grow this month, in *my* space, at *my* skill level?" — answered in seconds, every month, for life. |
| **Agentic behaviour** | A real perceive → plan → explain loop: perceives city/climate/space/skill, plans against a structured agronomy knowledge base (companion + antagonist matrices, pest intelligence, seasonal task checklists), and explains *why* each pairing works. |
| **Autonomy with control** | Three autonomy levels in the CLI; the optional local open-weight model (Ollama) rewrites the plan in plain language — the user swaps the brain locally, no closed-API lock-in. |
| **Privacy by architecture** | Zero network in the default path. Location and garden data never leave the device. This is not a policy promise; it is the code path. |
| **Inclusive & accessible** | Zero cost, zero accounts, works on a decade-old laptop; southern-hemisphere users get correctly flipped seasons (a detail most agronomy tools get wrong). |

Societal spill-over (supports the "agent for good" narrative): home food
production, pollinator-friendly companion planting knowledge, reduced
screen time, and climate-adapted growing for cities the original knowledge
base never mentioned (graceful temperate fallback, clearly labelled).

## 2. Deliverables checklist (official requirements)

Official requirement (verified from dubaichamberdigital.com/en/create-ai-agents):
working prototype + **English pitch deck** + **English demo video**;
commercialised products are ineligible (pre-commercial prototypes are fine).

| Deliverable | Status | File |
|---|---|---|
| Working prototype (public repo, MIT) | ✅ live | github.com/Zhiyilang/hacktoberfest-2026-ai |
| Hosted, clickable demo | ⬜ one-click Render deploy | `render.yaml` + `app.py` (ready) |
| English pitch deck | ✅ 12-page outline written | `DUBAI_PITCH.md` |
| English demo video (≤3 min) | ✅ storyboard written | `DUBAI_DEMO_SCRIPT.md` |
| Bilingual product (EN/中文) | ✅ English web UI + 中文 CLI | `i18n.py`, `app.py` |
| Test evidence | ✅ 43 assertions, CI 3.10/3.11/3.12 | `eval.py` |

## 3. Registration & submission actions (your side)

- [ ] **P1.** Register at dubaichamberdigital.com/en/create-ai-agents (registration open; **December deadline**). One registration can submit **multiple** proposals — submit this alongside the ClauseGuard (Best Societal) and AirPilot (Best Business) entries.
- [ ] **P2.** Deploy the hosted demo: Render → New → Blueprint → pick `Zhiyilang/hacktoberfest-2026-ai` (the repo's `render.yaml` builds and starts `python app.py` with no dependencies). Paste the live URL into the entry form.
- [ ] **P3.** Record the demo video per `DUBAI_DEMO_SCRIPT.md` (3 min, English, terminal + hosted UI).
- [ ] **P4.** Turn `DUBAI_PITCH.md` into the deck (12 slides; any tool — Google Slides / PowerPoint / reveal.js). Keep the numbers verbatim: 43 assertions, 15 plants, 17 cities, 2 hemispheres, 0 network calls.
- [ ] **P5.** Submit before the December deadline; keep the repo public and MIT-licensed (judges verify).

## 4. Proof points judges can verify in < 2 minutes

```bash
git clone https://github.com/Zhiyilang/hacktoberfest-2026-ai
cd hacktoberfest-2026-ai
python eval.py                 # -> Ran 43 tests ... OK
python main.py --city Sydney --month 4 --space balcony --level easy
python app.py                  # hosted bilingual UI
```

- **Southern-hemisphere correctness**: Sydney month 4 → northern month 10
  autumn plan (season flip is the kind of detail that separates a real
  agronomy engine from a prompt wrapper).
- **Determinism**: same inputs → byte-identical plans (asserted in eval).
- **Graceful unknown-city fallback**: unknown cities get a clearly
  labelled temperate default instead of a hallucinated climate.

## 5. Honesty notes (say these before judges ask)

- The knowledge base is **curated, not crowd-sourced** — 15 plants, 17
  cities. Scope is deliberate: a small, correct, testable core over a
  large, unverified one.
- The optional Ollama rewrite is a **local** model; if it is absent the
  rule engine emits the complete plan (no degradation).
- This is a **pre-commercial prototype** built for the championship —
  not a shipped product.
