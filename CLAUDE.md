# notebooklm-claude-workflows — CLAUDE.md (Level 1)

> Level 1 file for **this** repository. (`config/CLAUDE.md` is a snippet shipped to *downstream users* — different file, different audience.)

## Status: ACTIVE
Public Claude Code slash-command pack + automation for Google NotebookLM. MIT-licensed. Built on top of [`notebooklm-mcp-cli`](https://github.com/jacob-bd/notebooklm-mcp-cli) — no functionality without it.

## Architecture

The whole project is a workflow layer over a third-party MCP server. There is no runtime of our own:

- `commands/*.md` — Claude Code slash-command recipes. Each is a deterministic 2–3-phase pipeline of MCP tool calls (`notebook_create`, `source_add`, `notebook_query`, `studio_create`, `research_start`, `research_status`, `research_import`).
- `scripts/telegram-chunker.py` — Python utility for one specific pain point: turning Telegram forum-supergroup exports into NotebookLM-sized markdown chunks. Detects topics via `topic_message_id` + `forum_topic_created`. Output is plain markdown ready for `source_add`.
- `scripts/nlm-auth-check.sh` — Bash daily auth probe. Calls `nlm notebook list`, parses for `"id"` keys, logs to `~/Documents/scripts/nlm-auth.log`. On Windows, fires a BurntToast notification (with MessageBox fallback) when auth has expired.
- `scripts/setup-nlm-scheduler.ps1` — PowerShell installer that registers the auth probe as a Windows Task Scheduler job.
- `config/CLAUDE.md` — content fragment to be appended to a downstream user's `~/.claude/CLAUDE.md`. Teaches Claude to proactively use NotebookLM for unfamiliar libraries.

## Key files (when touching)

- `commands/research.md` — three-phase pipeline. The order matters: Phase 1 sources, Phase 2 queries, Phase 3 artifacts. Do not collapse phases.
- `commands/deep-research.md` — five-question-per-topic deep dive. Builds a topic tree first, then iterates. Distinct from `research.md`; both should remain.
- `commands/telegram-to-notebook.md` — references `scripts/telegram-chunker.py`. Keep paths consistent if you move the script.
- `scripts/telegram-chunker.py` — 13 KB, pure stdlib. No third-party deps by design (so it runs anywhere Python 3.10+ is available).
- `scripts/nlm-auth-check.sh` — `bash`-portable, no `set -euo pipefail` because the failure path is the whole point. If you add `set -e`, the toast-notification logic stops working when `nlm notebook list` fails.

## CRITICAL RULES — when editing this repo

- **NEVER** introduce a hard dependency on a specific `notebooklm-mcp-cli` version unless you also pin it in README and `CHANGELOG.md`. Upstream is third-party — pinning is a real cost.
- **NEVER** silently drop the `wait=true` semantics in any command. The whole "deterministic vs raw MCP" value prop hinges on `wait=true` being applied consistently.
- **NEVER** rename a slash command without updating the README's command tables (English AND Russian) and adding a `CHANGELOG.md` "Breaking changes" entry. Users have shell aliases / scripts referencing the names.
- **ALWAYS** mirror customer-facing changes between `README.md` and `README.ru.md`. They have feature parity and must stay parity.
- **ALWAYS** update `CHANGELOG.md` for any change visible to users (new command, removed command, output-format change, breaking workflow change).
- **ALWAYS** keep `scripts/telegram-chunker.py` stdlib-only. The whole point is "drop-in script with zero install"; adding `pip install` requirements breaks that contract.
- **ALWAYS** flag commands that depend on a not-yet-released MCP tool with a clear note in the command file ("requires notebooklm-mcp-cli ≥ X.Y").

## Commands (for me)

- `python -m py_compile scripts/telegram-chunker.py` — syntax check
- `bash -n scripts/nlm-auth-check.sh` — syntax check
- `python scripts/telegram-chunker.py result.json --list-topics` — quick smoke test against a real export
- `nlm notebook list` — confirm auth still valid before running any command file by hand

## Key patterns

1. **Three-phase pipeline.** Every research command follows Collect → Analyse → Artifacts. Distinct phases let Claude show progress and let users abort cleanly between phases.
2. **`wait=true` discipline.** Every `source_add` call uses `wait=true` so subsequent `notebook_query` calls actually have content to query. This is invisible discipline that distinguishes "raw MCP" from "workflow command".
3. **Sequential queries with `conversation_id`.** Multi-question deep-research uses the same `conversation_id` across queries so NotebookLM keeps context. Drop this and the analyses become decontextualised.
4. **Filter at chunk boundaries.** `telegram-chunker.py` filters stickers / GIFs / video at message-extract time, not at chunk-write time, so chunk word counts reflect actual signal.

## External dependencies

- [`notebooklm-mcp-cli`](https://github.com/jacob-bd/notebooklm-mcp-cli) — required. If upstream breaks, every command in this repo breaks.
- Claude Code (Opus 4.7 / 1M context recommended for `/deep-research`).
- Python 3.10+ for `telegram-chunker.py`.
- Bash 4+ and `nlm` CLI on PATH for `nlm-auth-check.sh`.
- Windows + PowerShell for `setup-nlm-scheduler.ps1` and BurntToast notifications.

## Sister repos (same author)

- [Claude Code Anti-Regression Setup](https://github.com/CreatmanCEO/claude-code-antiregression-setup) — pairs with this: anti-regression keeps Claude from breaking code while running these workflows.
- [ai-context-hierarchy](https://github.com/CreatmanCEO/ai-context-hierarchy) — `config/CLAUDE.md` here is a Level 0 fragment that fits naturally into that hierarchy.
- [claude-statusline](https://github.com/CreatmanCEO/claude-statusline) — Claude Code statusline; complementary tool from the same ecosystem.

## Recent changes

See [CHANGELOG.md](CHANGELOG.md).
