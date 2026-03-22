# NotebookLM + Claude Toolkit

Набор команд, скриптов и конфигураций для интеграции Google NotebookLM с Claude Code / Claude Desktop через MCP.

## Что внутри

### Commands (Claude Code slash-commands)
- `/youtube-research` — анализ YouTube видео через NotebookLM (замена сломанным transcript API)
- `/init-notebook` — создание NotebookLM ноутбука с документацией для tech-стека
- `/research` — полный цикл исследования: сбор источников → анализ → артефакты

### Scripts
- `nlm-auth-check.sh` — проверка auth cookies с Windows-уведомлением
- `setup-nlm-scheduler.ps1` — регистрация ежедневной проверки в Task Scheduler

### Config
- `CLAUDE.md` — глобальные инструкции для Claude Code по использованию NotebookLM

## Зависимости

- [notebooklm-mcp-cli](https://github.com/jacob-bd/notebooklm-mcp-cli) — `uv tool install notebooklm-mcp-cli`
- Claude Code с подключённым `notebooklm-mcp`

## Установка

```bash
# 1. Скопировать commands в Claude Code
cp commands/*.md ~/.claude/commands/

# 2. Добавить содержимое CLAUDE.md в глобальный ~/.claude/CLAUDE.md

# 3. Скопировать скрипты
cp scripts/* ~/Documents/scripts/
chmod +x ~/Documents/scripts/nlm-auth-check.sh

# 4. (Опционально) Настроить Task Scheduler
powershell -ExecutionPolicy Bypass -File ~/Documents/scripts/setup-nlm-scheduler.ps1
```

---
<sub>*Сделано с заботой и вниманием к внутреннему миру человека.*</sub>
