# 🛰️ AI Radar Agent

An autonomous agent that filters the AI/tech firehose into a curated, scored, project-aware digest — so a builder can stay informed without getting distracted.

Built by [Noha Zak](https://github.com/NohaZak) for **NoZak Labs** to defend focus while staying current.

---

## What it does

Twice a week (Mon + Fri at 7:00 AM Cairo), this agent:

1. **Fetches** items from 7 sources: Hacker News, Product Hunt, GitHub Trending, Ben's Bites, TLDR AI, Reddit (r/MachineLearning + r/SideProject), and Pega Community
2. **Dedupes** by URL and filters to the last 4 days
3. **Scores** every item against the NoZak Labs project context using **Claude Haiku 4.5**
4. **Tags** items with project relevance (Brands of Eden, lurniALP, Hykers, SE Job Hunt, Cross-cutting)
5. **Writes** scored items into a **Notion database** for filterable review
6. **Updates** `radar.md` in this repo and commits it back

Total weekly cost: **~$0.25 in Claude API usage.** Runs on GitHub Actions free tier.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  GitHub Actions (scheduled: Mon + Fri, 05:00 UTC)           │
└────────────────────────┬────────────────────────────────────┘
                         ▼
        ┌────────────────────────────────────┐
        │  src/sources.py                    │
        │  Fetches from 7 sources via        │
        │  RSS + REST APIs                   │
        └────────────────┬───────────────────┘
                         ▼
        ┌────────────────────────────────────┐
        │  src/scorer.py                     │
        │  Claude Haiku 4.5 scores each item │
        │  against NoZak Labs context        │
        └────────────────┬───────────────────┘
                         ▼
        ┌────────────────────────────────────┐
        │  src/outputs.py                    │
        │  Writes to Notion DB + radar.md    │
        └────────────────────────────────────┘
```

---

## Why this exists

The problem: dozens of new AI tools, GitHub repos, and launches drop every day. Trying to track them all destroys focus. Ignoring them entirely means missing genuinely useful tools.

The solution: a personal agent that knows what I'm building (three client projects + an active job search) and scores every item by relevance — so I check the radar twice a week during dedicated 30-min slots, not every five minutes during deep work.

---

## Scoring rubric

| Score | Tier | What it means |
|---|---|---|
| 90–100 | 🔥 Act Now | Directly unblocks or significantly improves a Tier 1 project this week |
| 75–89 | 🔥 Act Now | Strong relevance to a Tier 1 project — worth evaluating |
| 50–74 | 👀 Watch | Tangential relevance or strong relevance to cross-cutting interests |
| 25–49 | 📦 Archive | Weak relevance — kept for searchability only |
| 0–24 | _Dropped_ | Noise or hits an explicit noise filter |

The rubric and the full project context live in [`src/context.py`](src/context.py).

---

## Tech stack

- **Python 3.11**
- **Anthropic Claude Haiku 4.5** for scoring
- **Notion API** for the database backend
- **GitHub Actions** for scheduling and execution
- **feedparser + requests** for source fetching

---

## Project structure

```
ai-radar-agent/
├── .github/workflows/
│   └── radar.yml              # GitHub Actions schedule + workflow
├── src/
│   ├── __init__.py
│   ├── context.py             # NoZak Labs project priorities (the agent's "brain")
│   ├── sources.py             # Fetchers for each source
│   ├── scorer.py              # Claude scoring engine
│   ├── outputs.py             # Notion + radar.md writers
│   └── main.py                # Orchestrator
├── docs/
│   └── SETUP.md               # Step-by-step setup instructions
├── radar.md                   # Auto-updated digest (don't edit manually)
├── requirements.txt
└── README.md
```

---

## Local development

```bash
# Install dependencies
pip install -r requirements.txt

# Set env vars (use a .env file or your shell)
export ANTHROPIC_API_KEY=sk-ant-...
export NOTION_TOKEN=ntn_...
export NOTION_DATABASE_ID=624bb437-73da-4bfe-a66e-1c192cfed053

# Run the agent
python -m src.main
```

---

## Updating priorities

Project priorities live in `src/context.py`. Edit the `PROJECTS`, `CROSS_CUTTING`, or `NOISE_FILTERS` blocks, commit, and the next scheduled run will use the updated context. No other code changes needed.

---

## License

MIT
