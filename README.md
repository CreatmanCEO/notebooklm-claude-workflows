<div align="center">

🌐 **Language / Язык**

[![English](https://img.shields.io/badge/English-blue?style=flat-square)](README.md) [![Русский](https://img.shields.io/badge/Русский-red?style=flat-square)](README.ru.md)

</div>

# notebooklm-claude-workflows

Ready-to-use [Claude Code](https://docs.anthropic.com/en/docs/claude-code) workflows for [Google NotebookLM](https://notebooklm.google.com) — research pipelines, YouTube analysis, project documentation, auth monitoring.

[![MIT](https://img.shields.io/github/license/CreatmanCEO/notebooklm-claude-workflows?style=flat-square&color=green)](LICENSE) [![Claude Code](https://img.shields.io/badge/Claude_Code-commands-blueviolet?style=flat-square&logo=anthropic&logoColor=white)]() [![platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-blue?style=flat-square)]()

**Stop calling MCP tools one by one. Say what you need — Claude does the rest.**

## The Problem

[notebooklm-mcp-cli](https://github.com/jacob-bd/notebooklm-mcp-cli) gives Claude access to NotebookLM — but as raw tools. Creating a notebook, adding 5 sources, querying, generating a podcast means 10+ manual tool calls. You end up doing the orchestration yourself.

**This project fixes that.** Three slash commands turn multi-step NotebookLM operations into one-liners:

```
/research AI agents 2025          → full research pipeline with artifacts
/youtube-research LLM fine-tuning → YouTube videos → analysis → podcast
/init-notebook next.js supabase   → docs notebook for your stack
```

## What's Inside

### Slash Commands

| Command | What it does |
|---------|-------------|
| `/research <topic>` | Full cycle: create notebook → collect sources (URLs, YouTube, Drive, text) → multi-query analysis → generate artifacts (podcast, mind map, flashcards, report) |
| `/youtube-research <topic>` | YouTube video analysis via NotebookLM. Replaces broken transcript APIs (429 errors). Feed videos → get structured analysis with citations |
| `/init-notebook <stack>` | Auto-create a NotebookLM notebook with official documentation for your tech stack. Knows URLs for 30+ popular frameworks |

### Automation

| Component | What it does |
|-----------|-------------|
| `nlm-auth-check.sh` | Daily cookie health check with Windows toast notifications when auth expires |
| `setup-nlm-scheduler.ps1` | One-click Windows Task Scheduler setup for the auth check |
| `CLAUDE.md` config | Global instructions so Claude proactively suggests NotebookLM when working with unfamiliar tech |

## How It Works

```
You: /research AI code assistants

Claude (autonomously):
  1. Creates notebook "Research: AI code assistants"
  2. Asks for sources → you paste URLs, YouTube links, text
  3. Adds each source to NotebookLM (with progress)
  4. Runs multi-angle analysis:
     - Key ideas summary
     - Cross-source patterns
     - Contradictions between sources
  5. Returns structured report with citations
  6. Offers to generate: podcast / mind map / flashcards / quiz
```

No manual tool calls. No context switching. No copy-pasting between tabs.

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and working
- [notebooklm-mcp-cli](https://github.com/jacob-bd/notebooklm-mcp-cli) installed and authenticated:
  ```bash
  uv tool install notebooklm-mcp-cli
  nlm login
  nlm setup add claude-code
  ```
- Restart Claude Code after MCP setup

## Installation

### Quick (one command)

Open Claude Code and say:

```
Clone https://github.com/CreatmanCEO/notebooklm-claude-workflows and install
```

Claude will clone the repo and copy commands to the right places.

### Manual

```bash
# Clone
git clone https://github.com/CreatmanCEO/notebooklm-claude-workflows.git ~/notebooklm-claude-workflows

# Copy slash commands
cp ~/notebooklm-claude-workflows/commands/*.md ~/.claude/commands/

# (Optional) Add NotebookLM instructions to global config
cat ~/notebooklm-claude-workflows/config/CLAUDE.md >> ~/.claude/CLAUDE.md

# (Optional) Auth monitoring — Windows only
mkdir -p ~/Documents/scripts
cp ~/notebooklm-claude-workflows/scripts/* ~/Documents/scripts/
chmod +x ~/Documents/scripts/nlm-auth-check.sh
powershell -ExecutionPolicy Bypass -File ~/Documents/scripts/setup-nlm-scheduler.ps1
```

Restart Claude Code. New commands appear automatically.

## Command Details

### /research — Full Research Pipeline

Three phases, fully autonomous:

**Phase 1 — Collect:** Creates a NotebookLM notebook, accepts any mix of sources (YouTube, web pages, Google Drive, raw text), adds them with progress tracking.

**Phase 2 — Analyze:** Runs a series of targeted queries against the notebook — summarization, pattern detection, contradiction analysis, plus your custom questions. Returns a structured report with citations from YOUR sources.

**Phase 3 — Artifacts:** Optionally generates NotebookLM studio content:

| Artifact | Format | Use case |
|----------|--------|----------|
| Audio Overview | MP3 | Podcast with two AI hosts discussing your sources |
| Mind Map | JSON | Visual knowledge structure |
| Flashcards | JSON/HTML | Study cards from source material |
| Briefing Doc | Markdown | Executive summary |
| Quiz | JSON/HTML | Test your understanding |

### /youtube-research — YouTube Without 429 Errors

YouTube transcript APIs are increasingly blocked (HTTP 429). NotebookLM ingests YouTube natively — no API keys, no rate limits.

```
/youtube-research React Server Components

> Paste 1-10 YouTube links:
https://youtu.be/abc123
https://youtu.be/def456
https://youtu.be/ghi789

→ Creates notebook, ingests all videos
→ Structured analysis with per-video summaries
→ Cross-video patterns and insights
→ Optional: generate podcast from all videos
```

### /init-notebook — Documentation for Your Stack

Creates a NotebookLM notebook pre-loaded with official docs for your technologies:

```
/init-notebook fastapi postgresql redis

→ Creates "fastapi postgresql redis Docs" notebook
→ Adds FastAPI docs, PostgreSQL docs, Redis docs
→ Ready for queries: "How do I set up connection pooling with FastAPI + PostgreSQL?"
```

Built-in URL hints for 30+ frameworks (Next.js, React, Supabase, Tailwind, Drizzle, Playwright, Electron, and more). Works with any URL — not limited to the built-in list.

Also integrates with `/init-project` — suggests creating a docs notebook when you start a new project.

## Auth Monitoring

NotebookLM uses browser cookies (no official API). Cookies expire. The auth check script runs daily and alerts you before things break:

```
[2026-03-23 10:00:01] AUTH OK — 5 notebooks accessible
[2026-03-25 10:00:01] AUTH EXPIRED — run: nlm login
```

On Windows: toast notification when cookies expire. On Linux/macOS: log file only (PRs welcome for native notifications).

## Configuration

### CLAUDE.md Integration

The included `config/CLAUDE.md` teaches Claude to proactively check NotebookLM when working with unfamiliar libraries. Append it to your global config:

```bash
cat ~/notebooklm-claude-workflows/config/CLAUDE.md >> ~/.claude/CLAUDE.md
```

Before: You have to remember to ask Claude to use NotebookLM.
After: Claude suggests it automatically when it would help.

## Project Structure

```
notebooklm-claude-workflows/
├── commands/
│   ├── youtube-research.md    # /youtube-research command
│   ├── init-notebook.md       # /init-notebook command
│   └── research.md            # /research command
├── scripts/
│   ├── nlm-auth-check.sh      # Daily auth cookie check
│   └── setup-nlm-scheduler.ps1 # Windows Task Scheduler setup
├── config/
│   └── CLAUDE.md              # Global Claude Code instructions
├── README.md
├── README.ru.md
├── LICENSE
└── .gitignore
```

## FAQ

**Q: Is this an MCP server?**
No. This is a workflow layer on top of [notebooklm-mcp-cli](https://github.com/jacob-bd/notebooklm-mcp-cli). Think of it as macros + templates for the MCP tools. You need the MCP server installed first.

**Q: Does this work with Claude Desktop?**
The slash commands are Claude Code specific. Claude Desktop users get the MCP tools directly but without the workflow automation. See [notebooklm-mcp-cli docs](https://github.com/jacob-bd/notebooklm-mcp-cli) for Desktop setup.

**Q: What about cookie expiration?**
The auth monitoring script checks daily and notifies you. When cookies expire, just run `nlm login` — takes 30 seconds.

**Q: Can I add my own commands?**
Absolutely. Drop any `.md` file into `~/.claude/commands/` following the same format. See the existing commands for examples.

## Related Projects

- [notebooklm-mcp-cli](https://github.com/jacob-bd/notebooklm-mcp-cli) — The MCP server this project builds on (required)
- [claude-statusline](https://github.com/CreatmanCEO/claude-statusline) — Smart status line for Claude Code (by the same author)

## License

MIT — [Nick Podolyak](https://github.com/CreatmanCEO) / CREATMAN Studio
