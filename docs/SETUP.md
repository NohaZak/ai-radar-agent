# 🛠️ Setup Guide — AI Radar Agent

This documents the one-time setup completed when this agent was built. Useful as reference if anything needs to be re-created or rotated.

---

## Prerequisites

- [x] **Anthropic API key** with billing enabled
- [x] **Notion workspace** with a database and integration
- [x] **GitHub repo** with Actions enabled

---

## 1. Anthropic API setup

1. Sign up at [console.anthropic.com](https://console.anthropic.com)
2. Add billing — $5 of prepaid credit is enough for ~6 months of radar runs
3. Create an API key named `nozak-radar-agent`
4. Save the key in a password manager or Windows Credential Manager
5. Add it to GitHub Actions secrets as `ANTHROPIC_API_KEY` (see step 3 below)

---

## 2. Notion setup

### Create the database

The agent expects a Notion database with this schema:

| Property | Type | Notes |
|---|---|---|
| Title | Title | Item name |
| Score | Number | 0–100, set by Claude |
| Tier | Select | 🔥 Act Now / 👀 Watch / 📦 Archive |
| Project Match | Multi-select | Brands of Eden / lurniALP / Hykers / SE Job Hunt / Cross-cutting |
| Category | Select | AI Tool / GitHub Repo / Article / Newsletter / Launch / Other |
| Source | Select | Hacker News / Product Hunt / GitHub Trending / Bens Bites / TLDR AI / Reddit / Pega Community |
| URL | URL | Link |
| Summary | Rich text | 1–2 sentences |
| Why It Matters | Rich text | 1–2 sentences |
| Date Added | Date | Set by agent |
| Decision | Select | ⏳ Unreviewed / ✅ Adopt / 🔬 Evaluate / ❌ Skip |
| Reviewed | Checkbox | Marked after review |

Three default views:
- **🔥 Inbox** — filter `Reviewed = false`, sort by `Score` descending
- **📊 By Project** — board grouped by `Project Match`
- **📅 Archive** — filter `Reviewed = true`, sort by `Date Added` descending

### Create the integration

1. Go to [notion.so/profile/integrations](https://www.notion.so/profile/integrations)
2. **New integration** → name: `NoZak Radar Agent`, type: Internal
3. **Capabilities:** Read content, Update content, Insert content. User capabilities: **No user information** (least privilege).
4. Copy the integration token (starts with `ntn_` or `secret_`)
5. Save the token in a password manager or Credential Manager
6. **Connect the integration to the database:** open the database → `···` menu → Connections → search "NoZak Radar Agent" → connect

### Get the database ID

Open the database in your browser. The URL looks like:

```
https://www.notion.so/<DATABASE_ID>?v=...
```

The `<DATABASE_ID>` is the 32-character hex string. Hyphens are optional.

---

## 3. GitHub Actions secrets

In the repo: **Settings → Secrets and variables → Actions → New repository secret**

Add three secrets:

| Name | Value |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `NOTION_TOKEN` | Your Notion integration token |
| `NOTION_DATABASE_ID` | The database ID from above |

---

## 4. Verify the setup

### Manual test run

In the GitHub repo, go to **Actions → AI Radar Agent → Run workflow**. This triggers the agent immediately so you can confirm everything works without waiting for the scheduled time.

Check the workflow logs. You should see:

```
🛰️  Starting NoZak Labs Radar Agent
Step 1/3: Fetching from sources…
  Hacker News: N items
  Product Hunt: N items
  …
Step 2/3: Scoring with Claude…
  [1/N] Scoring: ...
Step 3/3: Writing outputs…
  Notion: N/N items written
  Wrote radar.md
✅ Radar run complete
```

Then check:
- The Notion database has new rows
- `radar.md` was updated and committed

---

## 5. Schedule

The workflow runs on cron `0 5 * * 1,5` — that's **05:00 UTC every Monday and Friday**, which equals **07:00 Cairo time (EET, UTC+2)**.

You can manually trigger a run anytime from the Actions tab.

---

## 6. Calendar blocks

Two 30-minute review blocks on Google Calendar (set these once, recurring weekly):

- **Monday 8:00–8:30 PM Cairo**
- **Friday 8:00–8:30 PM Cairo**

These are the only times to open the radar. Outside these slots, the radar stays closed.

---

## Cost expectations

| Item | Monthly cost |
|---|---|
| Anthropic API (Haiku 4.5, ~100 items × 2 runs/week) | $0.30–$1.00 |
| Notion (Free tier) | $0 |
| GitHub Actions (well within free 2000 min/month) | $0 |
| **Total** | **< $1/month** |

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `Missing required environment variables` | GitHub secret not set | Add all 3 secrets in repo settings |
| Notion writes return 401 | Integration not connected to DB | Open DB → ··· → Connections → add integration |
| Notion writes return 400 | Schema mismatch | Verify property names match exactly (case-sensitive) |
| All scores are 0 | Claude returned malformed JSON | Check workflow logs, may be rate-limited |
| `radar.md` not updating in repo | Workflow lacks write permission | Verify `permissions: contents: write` is in workflow |

---

## Rotating credentials

If a key is compromised:

1. Revoke the old key in the source console (Anthropic or Notion)
2. Generate a new key with the same name + `-v2`
3. Update the corresponding GitHub Actions secret
4. Update the password manager / Credential Manager entry
5. Log the rotation in the Notion Credentials Index page
