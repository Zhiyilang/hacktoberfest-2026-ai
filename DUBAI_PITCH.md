# GardenPlanner AI — Dubai Pitch Deck (12 slides, English)
## Create AI Agents Championship · Best Personal AI Agent

Deck title: **"The gardening agent that never phones home."**
Speaker notes in *italics*. Keep every number verbatim — judges verify.

---

**Slide 1 — Title**
- 🌱 GardenPlanner AI
- "The gardening agent that never phones home."
- Best Personal AI Agent · Create AI Agents Championship · Dubai
- *One sentence: a personal agent that plans your growing month — offline, private, free.*

**Slide 2 — The problem (30 seconds)**
- Growing food at home fails on knowledge, not motivation: *what* to sow *now*, what to plant *next to it*, what to *keep apart*, which *pests* to expect.
- Existing answers are either generic blog posts or apps that want your location, an account, and a subscription.
- Southern-hemisphere gardeners get seasonally wrong advice from northern-centric tools.
- *Personal stake: this is a monthly recurring decision every gardener makes.*

**Slide 3 — The agent (what it actually does)**
- Perceive: city (climate zone + hemisphere), growing space, skill level, month.
- Plan: structured agronomy knowledge base — companion (friends) / antagonist (foes) matrices, pest intelligence, seasonal task checklists.
- Explain: every recommendation carries its reasoning (why basil next to tomato, why keep potato from tomato).
- Act: a checklist you take outside — the agent's output is physical action, not more screen time.

**Slide 4 — Why "agentic", not a chatbot**
- Deterministic rule engine over a curated knowledge graph: same inputs → byte-identical plan (asserted in the test suite).
- A perceive → plan → explain → act loop with a receipt-style output, not a single prompt response.
- Optional local open-weight brain (Ollama) rewrites the plan in plain language — swappable by the user, no closed-API lock-in.
- *Contrast: a wrapper that stops working when the API is down.*

**Slide 5 — Privacy as architecture**
- Default path: **zero network calls**. Location and garden data never leave the device.
- This is not a privacy policy — it is the code path (no telemetry, no accounts, no keys in the default mode).
- The only network touchpoint is the *optional* model, which the user hosts themselves.
- *For a "personal" agent, the data is the person. This is the design centre.*

**Slide 6 — Who it serves (personal + societal)**
- Personal: balcony gardeners, beginners, elders, schools, community gardens.
- Societal spill-over: home food production, pollinator-friendly companion planting, climate-adapted growing (unknown cities get a *labelled* temperate fallback — never a hallucinated climate).
- Southern-hemisphere correctness: Sydney month 4 → northern month 10 autumn plan.
- *Inclusion angle: works on a decade-old laptop, offline, in two languages.*

**Slide 7 — Live demo (or demo video segment)**
- Terminal: `python main.py --city "Shanghai" --month 10 --space balcony --level easy` → full plan in under a second.
- Web UI (hosted): English-first, 中文 toggle, plan as cards.
- `python eval.py` → `Ran 43 tests ... OK`.
- *If live demo fails, play the video — never debug on stage.*

**Slide 8 — Engineering quality**
- Zero dependencies: pure Python standard library (CLI + web demo).
- 43 assertions covering hemisphere maths, plan determinism, data integrity, English-layer coverage, real-subprocess CLI, and **real-HTTP** endpoint round-trips.
- CI on Python 3.10 / 3.11 / 3.12, MIT licensed, bilingual docs.
- *The test suite is the product's spine: every claim in this deck is an assertion.*

**Slide 9 — What is deliberately NOT here (honesty slide)**
- Curated knowledge base: 15 plants, 17 cities — a small, correct, testable core over a large, unverified one.
- The Ollama rewrite is local; when absent, the rule engine emits the complete plan (graceful, asserted).
- Pre-commercial prototype built for this championship — not a shipped product.
- *Judges reward calibrated claims. State limits before they are asked.*

**Slide 10 — Roadmap (post-championship)**
- Community-extensible plant/city database with review (the schema is already tested).
- Photo-based plant ID (local model) → personalised pest alerts.
- Calendar integrations (ICS export) and printable balcony layouts.
- Regional knowledge packs (Gulf climate, high-altitude) with local agronomist review.

**Slide 11 — Why this can win "Best Personal AI Agent"**
- A monthly recurring personal decision, solved end-to-end.
- Agentic loop with explainable, cited-by-design output.
- Privacy by architecture — the differentiator no cloud agent can copy.
- Free, offline, bilingual, tested: useful to a gardener in Shanghai *and* one in São Paulo.
- *Tie back to the title: it never phones home — that is the product.*

**Slide 12 — Close / Q&A**
- Repo: github.com/Zhiyilang/hacktoberfest-2026-ai (MIT)
- Hosted demo URL: *(fill after Render deploy)*
- "Agents should amplify people, not extract from them. GardenPlanner plans your month — and keeps your garden yours."
- *Expected Q&A:*
  - *"Why not just use an LLM?"* → Determinism, privacy, and zero marginal cost; the LLM is an optional local enhancer, not a dependency.
  - *"How do you keep the knowledge base correct?"* → Schema assertions (month ranges, enums, unique names), companion-token coverage tests, and community PRs through review.
  - *"What is the business model?"* → None — it is a pre-commercial prototype; the championship is about the agent, not the revenue.
