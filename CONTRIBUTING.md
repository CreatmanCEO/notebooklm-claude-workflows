# Contributing

Thanks for considering a contribution. The bar: real use case, deterministic workflow, MCP-tool calls visible in the command file, no hidden dependencies.

## Priorities (highest impact first)

1. **Native notifications for Linux and macOS** — `scripts/nlm-auth-check.sh` currently only fires Windows toast notifications. Add `osascript -e 'display notification ...'` for macOS and `notify-send` (with `dunstify` fallback) for Linux. Detect the platform via `uname -s` and branch.
2. **Expanded URL dictionary in `/init-notebook`** — current list covers 30+ frameworks. PRs welcome to extend with: Solid.js, SvelteKit, Astro, Hono, NestJS, Bun, Deno, tRPC, TanStack Query, Zod, Pydantic, SQLAlchemy, Polars, DuckDB, ClickHouse, Temporal, Hatchet, Convex.
3. **New slash commands** that map cleanly onto the three-phase pattern:
   - `/pdf-research <topic>` — PDF papers → NotebookLM → analysis
   - `/podcast-to-notebook <feed-url>` — podcast feed → episode transcripts (via NotebookLM) → topic-aware analysis
   - `/csv-research <file>` — CSV / TSV / Parquet → analytics queries against the data
4. **Translation of command files** — currently command bodies are bilingual where it matters but a few are Russian-only. Extract user-visible strings into a small translation table or duplicate each command with `.en.md` / `.ru.md` suffix.
5. **Telegram chunker improvements** — current chunker is forum-aware, but could also handle:
   - WhatsApp exports (different format)
   - Discord channel exports (also has thread structure)
   - Slack channel exports (per-channel JSON)

## What we will not merge

- Changes that introduce a non-stdlib dependency in `scripts/telegram-chunker.py`. The whole point is "drop-in script, zero install." If you need a non-stdlib lib, write a sister script.
- Changes that bypass `wait=true` semantics in command files. The deterministic workflow contract depends on it.
- Slash commands that wrap a single MCP tool call with no added value. If it is one-call, it is not a workflow — the user should call the MCP tool directly.
- Pull requests that rename existing commands without a CHANGELOG entry under "Breaking changes" and a deprecation alias kept for at least one minor version.

## Pull request checklist

- [ ] If you added a slash command: it has a clear `## Phase 1` / `## Phase 2` / `## Phase 3` structure (or a documented reason for fewer)
- [ ] If you touched `scripts/telegram-chunker.py`: `python -m py_compile` clean, stdlib-only, `--list-topics` smoke test passed locally
- [ ] If you touched `scripts/nlm-auth-check.sh`: `bash -n` clean, ShellCheck severity `error` clean
- [ ] `README.md` updated AND `README.ru.md` mirrored
- [ ] `CHANGELOG.md` entry added under Unreleased or a new minor version
- [ ] `validate.yml` workflow passes locally

## Style

- Command files: imperative voice (*"Create a notebook"*, *"Add each source"*). Phase headings are bold and numbered.
- Bash: `bash -n` and ShellCheck-error clean. `[[ ]]` over `[ ]`, `$()` over backticks, quoted variable expansions.
- Python: stdlib only, type hints on public functions, no print debugging in committed code.
- One feature per PR. Stack PRs if you have multiple.

## Author / maintainer

[@CreatmanCEO](https://github.com/CreatmanCEO) — Nick Podolyak. Open an issue first for anything larger than one command file or one chunker improvement.
