# Changelog

All notable changes to this project will be documented in this file.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) · [SemVer](https://semver.org/spec/v2.0.0.html).

## [0.2.0] — 2026-04-30

### Added

- `docs/architecture.svg` — pipeline diagram showing how a single slash command (e.g. `/research`) drives a deterministic three-phase recipe (Collect → Analyse → Artifacts) over the upstream `notebooklm-mcp-cli` MCP tools.
- `docs/output-mockup.svg` — visual mock-up of what a typical `/research` response looks like: structured findings / patterns / contradictions with inline citations linking to NotebookLM sources.
- `CLAUDE.md` for this repository — Level 1 file documenting the architecture, key files, CRITICAL RULES, commands, patterns. Pairs with the [ai-context-hierarchy](https://github.com/CreatmanCEO/ai-context-hierarchy) sister repo.
- `CHANGELOG.md` (this file)
- `CONTRIBUTING.md` with a priority list for community submissions
- `.github/workflows/validate.yml` — CI that runs `bash -n` on shell scripts, `python -m py_compile` on Python scripts, ShellCheck (severity error), confirms every `docs/*` asset referenced from README exists, and validates that all internal Markdown links resolve from `README.md` / `README.ru.md` / `CHANGELOG.md` / `CONTRIBUTING.md` / `CLAUDE.md`
- `Limitations` section to both READMEs — cookie expiry rhythm, 500 K word source cap, `/edit-source` workaround caveat, forum-detection heuristic, opaque NotebookLM rate limits, Claude Code-only, Windows-only native notifications, upstream-MCP dependency
- `Measured impact` section with concrete numbers (research-pipeline tool-call savings, 41 K-message Telegram forum tested in <2 min, YouTube 429 workaround, 30+ frameworks, daily auth check)
- `When to use which research command` decision helper distinguishing `/research`, `/deep-research`, `/youtube-research`, `/telegram-to-notebook`
- `Related` cross-links to all three sister repos: [claude-code-antiregression-setup](https://github.com/CreatmanCEO/claude-code-antiregression-setup), [ai-context-hierarchy](https://github.com/CreatmanCEO/ai-context-hierarchy), [claude-statusline](https://github.com/CreatmanCEO/claude-statusline)
- Six new badges: License, Stars, Validate CI, Built on `notebooklm-mcp-cli`, Claude Code Opus 4.7, MCP-compatible

### Changed

- README hero rewritten to lead with concrete production proof (41 K-message Telegram, 30+ frameworks, 7 commands) instead of an abstract feature list
- The flagship value-prop quote (*"MCP server = Claude has hands · workflow commands = Claude has hands + a checklist"*) elevated to a callout under the hero
- Project structure tree now matches the actual filesystem (was missing `docs/`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CLAUDE.md`, `.github/workflows/`)
- Author signature expanded with Habr / dev.to profile links

### Notes

- Topics on GitHub applied separately via `gh api` after merge.
- No companion article published yet for this repo specifically. Tracked as a P3 follow-up: a Habr / dev.to article along the lines of *"How I turned NotebookLM into a 7-command research assistant for Claude Code"* is the natural next traffic-driver, mirroring what was done for [claude-code-antiregression-setup](https://habr.com/ru/articles/1013330/) and [claude-statusline](https://habr.com/ru/articles/1013414/).

## [0.1.0] — 2026-04-05

### Added

- Initial release with five core slash commands:
  - `/research` — full research pipeline with auto-expand and Obsidian export
  - `/deep-research` — multi-iteration deep dive with topic tree
  - `/youtube-research` — YouTube video analysis via NotebookLM (workaround for HTTP 429 on transcript APIs)
  - `/init-notebook` — auto-create a docs notebook for a tech stack, with URL hints for 30+ popular frameworks
  - `/telegram-to-notebook` — import Telegram exports including forum supergroups with topic detection
- Two additional commands:
  - `/analytics-report` — analytics data → NotebookLM analysis → infographic / report
  - `/edit-source` — workaround for editing NotebookLM sources (extract → edit → replace)
- `scripts/telegram-chunker.py` — Python utility for splitting Telegram JSON exports into NotebookLM-compatible chunks. Handles forum-supergroup topic detection, filters stickers / GIFs / video, keeps text / code / PDFs. Tested on a 41 K-message corpus (12 topics, 586 K words → 13 NotebookLM sources, under 2 minutes).
- `scripts/nlm-auth-check.sh` — daily auth probe with Windows toast notification (BurntToast preferred, MessageBox fallback)
- `scripts/setup-nlm-scheduler.ps1` — one-click Windows Task Scheduler installer
- `config/CLAUDE.md` — global instruction snippet teaching Claude to proactively use NotebookLM for unfamiliar libraries
- Bilingual README (English + Russian)
- MIT license
