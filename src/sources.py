"""
Source fetchers — one function per source, all return the same shape:

    {
        "title": str,
        "url": str,
        "summary": str,           # short description if available, else ""
        "source": str,            # e.g. "Hacker News"
        "category": str,          # AI Tool / GitHub Repo / Article / Newsletter / Launch
        "raw_date": datetime,     # when the item was published (UTC)
    }

Each fetcher is defensive — if a source is down, it logs and returns an empty
list. The agent should never crash because one source had a bad day.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

import feedparser
import requests
from dateutil import parser as date_parser

log = logging.getLogger(__name__)

# Universal request timeout. RSS feeds and APIs sometimes hang.
REQUEST_TIMEOUT = 15

# How far back to look. We run once a week on Sunday, so 7 days is the baseline.
# We use 8 for a safety margin, then dedupe.
LOOKBACK_DAYS = 8


# ─── HELPERS ─────────────────────────────────────────────────────────────────


def _within_lookback(dt: datetime) -> bool:
    """True if dt is within the lookback window."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    cutoff = datetime.now(timezone.utc) - timedelta(days=LOOKBACK_DAYS)
    return dt >= cutoff


def _safe_parse_date(raw: Any) -> datetime:
    """Best-effort date parsing — returns now() if parsing fails."""
    try:
        if isinstance(raw, datetime):
            return raw if raw.tzinfo else raw.replace(tzinfo=timezone.utc)
        if isinstance(raw, str):
            return date_parser.parse(raw)
        if hasattr(raw, "tm_year"):  # time.struct_time
            return datetime(*raw[:6], tzinfo=timezone.utc)
    except (ValueError, TypeError) as e:
        log.warning(f"Date parse failed for {raw!r}: {e}")
    return datetime.now(timezone.utc)


def _normalize(
    title: str,
    url: str,
    summary: str,
    source: str,
    category: str,
    raw_date: Any,
) -> dict:
    """Build the canonical item shape."""
    return {
        "title": (title or "").strip()[:300],
        "url": (url or "").strip(),
        "summary": (summary or "").strip()[:1000],
        "source": source,
        "category": category,
        "raw_date": _safe_parse_date(raw_date),
    }


# ─── HACKER NEWS ─────────────────────────────────────────────────────────────


def fetch_hacker_news(min_score: int = 100) -> list[dict]:
    """Top stories from HN. Filter to stories with ≥ min_score points."""
    items: list[dict] = []
    try:
        # Get top story IDs
        ids_resp = requests.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            timeout=REQUEST_TIMEOUT,
        )
        ids_resp.raise_for_status()
        story_ids = ids_resp.json()[:50]  # top 50 only

        for story_id in story_ids:
            try:
                story_resp = requests.get(
                    f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                    timeout=REQUEST_TIMEOUT,
                )
                story = story_resp.json()
                if not story or story.get("type") != "story":
                    continue
                if (story.get("score") or 0) < min_score:
                    continue
                if not story.get("url"):
                    continue
                raw_date = datetime.fromtimestamp(story["time"], tz=timezone.utc)
                if not _within_lookback(raw_date):
                    continue
                items.append(_normalize(
                    title=story.get("title", ""),
                    url=story["url"],
                    summary=f"HN score: {story.get('score')}, comments: {story.get('descendants', 0)}",
                    source="Hacker News",
                    category="Article",
                    raw_date=raw_date,
                ))
            except Exception as e:
                log.warning(f"HN item {story_id} failed: {e}")
                continue
        log.info(f"Hacker News: {len(items)} items")
    except Exception as e:
        log.error(f"Hacker News fetcher failed: {e}")
    return items


# ─── PRODUCT HUNT ────────────────────────────────────────────────────────────


def fetch_product_hunt() -> list[dict]:
    """Product Hunt daily via their RSS feed (no API key required)."""
    items: list[dict] = []
    try:
        feed = feedparser.parse("https://www.producthunt.com/feed?category=undefined")
        for entry in feed.entries[:30]:
            raw_date = _safe_parse_date(entry.get("published_parsed"))
            if not _within_lookback(raw_date):
                continue
            items.append(_normalize(
                title=entry.get("title", ""),
                url=entry.get("link", ""),
                summary=entry.get("summary", ""),
                source="Product Hunt",
                category="Launch",
                raw_date=raw_date,
            ))
        log.info(f"Product Hunt: {len(items)} items")
    except Exception as e:
        log.error(f"Product Hunt fetcher failed: {e}")
    return items


# ─── GITHUB TRENDING ─────────────────────────────────────────────────────────


def fetch_github_trending() -> list[dict]:
    """GitHub Trending via an unofficial RSS mirror (no auth needed)."""
    items: list[dict] = []
    # Topics relevant to NoZak Labs work
    languages = ["python", "typescript", "javascript"]
    for lang in languages:
        try:
            url = f"https://github-trending-api.de.a9sapp.eu/repositories?language={lang}&since=weekly"
            resp = requests.get(url, timeout=REQUEST_TIMEOUT)
            if resp.status_code != 200:
                # Fallback: use trendshift or skip
                continue
            for repo in resp.json()[:10]:
                items.append(_normalize(
                    title=f"{repo.get('author', '')}/{repo.get('name', '')}",
                    url=repo.get("url", ""),
                    summary=repo.get("description", ""),
                    source="GitHub Trending",
                    category="GitHub Repo",
                    raw_date=datetime.now(timezone.utc),
                ))
        except Exception as e:
            log.warning(f"GitHub Trending ({lang}) failed: {e}")
            continue
    log.info(f"GitHub Trending: {len(items)} items")
    return items


# ─── RSS FEEDS (Newsletters, Reddit, Pega) ───────────────────────────────────


RSS_SOURCES = [
    {
        "url": "https://bensbites.beehiiv.com/feed",
        "source": "Bens Bites",
        "category": "Newsletter",
    },
    {
        "url": "https://tldr.tech/api/rss/ai",
        "source": "TLDR AI",
        "category": "Newsletter",
    },
    {
        "url": "https://www.reddit.com/r/MachineLearning/top/.rss?t=week",
        "source": "Reddit",
        "category": "Article",
    },
    {
        "url": "https://www.reddit.com/r/SideProject/top/.rss?t=week",
        "source": "Reddit",
        "category": "Article",
    },
    {
        "url": "https://community.pega.com/rss.xml",
        "source": "Pega Community",
        "category": "Article",
    },
]


def fetch_rss_feeds() -> list[dict]:
    """Fetch all configured RSS feeds."""
    items: list[dict] = []
    headers = {"User-Agent": "NoZak-Radar-Agent/1.0"}
    for src in RSS_SOURCES:
        try:
            # feedparser supports request_headers as a positional kwarg
            feed = feedparser.parse(src["url"], request_headers=headers)
            count_before = len(items)
            for entry in feed.entries[:20]:
                raw_date = _safe_parse_date(
                    entry.get("published_parsed") or entry.get("updated_parsed")
                )
                if not _within_lookback(raw_date):
                    continue
                items.append(_normalize(
                    title=entry.get("title", ""),
                    url=entry.get("link", ""),
                    summary=entry.get("summary", ""),
                    source=src["source"],
                    category=src["category"],
                    raw_date=raw_date,
                ))
            log.info(f"{src['source']}: {len(items) - count_before} items")
        except Exception as e:
            log.warning(f"RSS source {src['url']} failed: {e}")
            continue
    return items


# ─── ORCHESTRATOR ────────────────────────────────────────────────────────────


def fetch_all_sources() -> list[dict]:
    """Run every fetcher and return a flat, deduped list."""
    all_items: list[dict] = []
    all_items.extend(fetch_hacker_news())
    all_items.extend(fetch_product_hunt())
    all_items.extend(fetch_github_trending())
    all_items.extend(fetch_rss_feeds())

    # Dedupe on URL
    seen: set[str] = set()
    unique: list[dict] = []
    for item in all_items:
        url = item.get("url", "")
        if not url or url in seen:
            continue
        seen.add(url)
        unique.append(item)

    log.info(f"Total unique items: {len(unique)} (from {len(all_items)} raw)")
    return unique
