# Skill: Scrapling Release Watcher

This skill watches GitHub release pages for the tracked projects, extracts new release notes using Scrapling, summarizes features, and updates `src/pages/releases.astro` (and optionally a data file) with the latest features.

## Prerequisites
- Install Scrapling with extras: `pip install "scrapling[all]"`
- Ensure Playwright/Chromium is installed (`scrapling install` if needed).
- Repos watched:
  - openclaw/openclaw
  - qwibitai/nanoclaw
  - HKUDS/nanobot
  - sipeed/picoclaw
  - badlogic/pi-mono
  - nearai/ironclaw
  - zeroclaw-labs/zeroclaw

## How to run
1) Create a working dir (e.g., `scripts/releases/`).
2) For each repo, fetch the latest release page (HTML):
```bash
scrapling extract fetch "https://github.com/<repo>/releases/latest" latest.html --css-selector "main" --impersonate chrome
```
3) Parse release body text:
```python
from scrapling.parser import Selector
html = open("latest.html").read()
page = Selector(html)
title = page.css("h1, h2").get_text(strip=True)
items = [li.get_text(strip=True) for li in page.css("li")]
```
4) Summarize features (manual or LLM-assisted). Keep concise bullet points.

## Data to update
- Add/append a small JSON file `src/content/releases.json` with entries:
```json
{
  "repo": "openclaw/openclaw",
  "version": "v2026.2.26",
  "released": "2026-02-27",
  "features": [
    "Feature one",
    "Feature two"
  ]
}
```
- Update `src/pages/releases.astro` to render this data (table or list).

## Automation loop (cron/CI)
- Run daily via GitHub Actions or a local cron:
  - Fetch latest release tag via GitHub API.
  - If new tag, fetch release page with Scrapling, extract bullets, write JSON, and commit.

## Safety
- Respect GitHub rate limits (use GH token if needed).
- Store tokens in environment variables; never commit them.
