<div align="center">

🌐 **Language / Язык**

[![English](https://img.shields.io/badge/English-blue?style=flat-square)](README.md) [![Русский](https://img.shields.io/badge/Русский-red?style=flat-square)](README.ru.md)

</div>

# notebooklm-claude-workflows

Готовые рабочие процессы [Claude Code](https://docs.anthropic.com/en/docs/claude-code) для [Google NotebookLM](https://notebooklm.google.com) — пайплайны исследований, анализ YouTube, документация проектов, мониторинг авторизации.

[![MIT](https://img.shields.io/github/license/CreatmanCEO/notebooklm-claude-workflows?style=flat-square&color=green)](LICENSE) [![Claude Code](https://img.shields.io/badge/Claude_Code-commands-blueviolet?style=flat-square&logo=anthropic&logoColor=white)]() [![platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-blue?style=flat-square)]()

**Хватит вызывать MCP-инструменты по одному. Скажи что нужно — Claude сделает сам.**

## Проблема

[notebooklm-mcp-cli](https://github.com/jacob-bd/notebooklm-mcp-cli) даёт Claude доступ к NotebookLM — но в виде сырых инструментов. Создать ноутбук, добавить 5 источников, задать вопросы, сгенерировать подкаст — это 10+ ручных вызовов. Оркестрацию приходится делать самому.

**Этот проект решает проблему.** Три slash-команды превращают многошаговые операции с NotebookLM в однострочники:

```
/research AI агенты 2025            → полный пайплайн исследования с артефактами
/youtube-research fine-tuning LLM   → YouTube видео → анализ → подкаст
/init-notebook next.js supabase     → ноутбук с документацией твоего стека
```

## Зачем команды, если есть MCP?

Claude Code с MCP-сервером *может* сам разобраться что делать. Но между "может" и "делает стабильно" — пропасть:

| | Сырые MCP-инструменты | С командами workflow |
|---|---|---|
| Создаёт ноутбук | Да | Да |
| Добавляет источники с `wait=true` | Иногда забывает | Всегда |
| Многоракурсный анализ (резюме + паттерны + противоречия) | Обычно задаёт 1 вопрос | Всегда полная серия |
| Предлагает артефакты (подкаст, mind map) | Редко | Всегда |
| Структурированный вывод с цитатами | Как повезёт | Стандартизирован |
| Работает одинаково каждый раз | Зависит от контекста и настроения | Детерминировано |

Команды — не костыль, а **стандартизация процесса**. Разница между "напиши мне скрипт деплоя" и `make deploy`. У Claude есть инструменты в обоих случаях, но команды гарантируют качество рабочего процесса каждый раз.

Проще говоря:
- **MCP-сервер** = у Claude есть руки в NotebookLM
- **Команды workflow** = у Claude есть руки + чеклист

## Что внутри

### Slash-команды

| Команда | Что делает |
|---------|-----------|
| `/research <тема>` | Полный цикл: сбор источников → авто-расширение через веб-поиск → многоракурсный анализ → экспорт в Obsidian → генерация артефактов |
| `/deep-research <тема>` | Глубокое многоитерационное погружение: строит дерево тем, задаёт 3-5 вопросов по каждой, синтезирует комплексный отчёт с иерархией знаний |
| `/youtube-research <тема>` | Анализ YouTube видео через NotebookLM. Замена сломанным transcript API (ошибки 429). Загрузи видео → получи структурированный анализ с цитатами |
| `/init-notebook <стек>` | Автоматическое создание NotebookLM ноутбука с официальной документацией для твоего стека. Знает URL для 30+ популярных фреймворков |
| `/telegram-to-notebook` | Импорт Telegram-чатов в NotebookLM. Автоматическая разбивка больших JSON на чанки (300K слов) под лимиты NotebookLM |
| `/analytics-report` | Данные аналитики (CSV, JSON, API) → анализ в NotebookLM → инфографика, таблица, слайды или briefing doc |
| `/edit-source` | Редактирование источников NotebookLM (обходной путь: извлечь → редактировать → заменить). Поддержка Drive sync для Google Docs |

### Автоматизация

| Компонент | Что делает |
|-----------|-----------|
| `nlm-auth-check.sh` | Ежедневная проверка cookies с Windows-уведомлениями при истечении |
| `setup-nlm-scheduler.ps1` | Настройка Windows Task Scheduler в один клик |
| `CLAUDE.md` конфиг | Глобальные инструкции, чтобы Claude сам предлагал NotebookLM при работе с незнакомыми технологиями |

## Как это работает

```
Ты: /research AI-ассистенты для кода

Claude (автономно):
  1. Создаёт ноутбук "Research: AI-ассистенты для кода"
  2. Спрашивает источники → ты вставляешь URL, YouTube ссылки, текст
  3. Добавляет каждый источник в NotebookLM (с прогрессом)
  4. Запускает многоракурсный анализ:
     - Суммаризация ключевых идей
     - Паттерны между источниками
     - Противоречия между источниками
  5. Возвращает структурированный отчёт с цитатами
  6. Предлагает сгенерировать: подкаст / mind map / карточки / квиз
```

Никаких ручных вызовов инструментов. Никакого переключения контекста. Никакого копирования между вкладками.

## Требования

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) установлен и работает
- [notebooklm-mcp-cli](https://github.com/jacob-bd/notebooklm-mcp-cli) установлен и авторизован:
  ```bash
  uv tool install notebooklm-mcp-cli
  nlm login
  nlm setup add claude-code
  ```
- Перезапуск Claude Code после настройки MCP

## Установка

### Быстрая (одна команда)

Открой Claude Code и скажи:

```
Склонируй https://github.com/CreatmanCEO/notebooklm-claude-workflows и установи
```

Claude сам склонирует репо и скопирует команды в нужные места.

### Ручная

```bash
# Клонировать
git clone https://github.com/CreatmanCEO/notebooklm-claude-workflows.git ~/notebooklm-claude-workflows

# Скопировать slash-команды
cp ~/notebooklm-claude-workflows/commands/*.md ~/.claude/commands/

# (Опционально) Добавить инструкции NotebookLM в глобальный конфиг
# Безопасное добавление — не дублирует при повторном запуске
grep -q "notebooklm-claude-workflows" ~/.claude/CLAUDE.md 2>/dev/null || \
  cat ~/notebooklm-claude-workflows/config/CLAUDE.md >> ~/.claude/CLAUDE.md

# (Опционально) Мониторинг авторизации — только Windows
mkdir -p ~/Documents/scripts
cp ~/notebooklm-claude-workflows/scripts/* ~/Documents/scripts/
chmod +x ~/Documents/scripts/nlm-auth-check.sh
powershell -ExecutionPolicy Bypass -File ~/Documents/scripts/setup-nlm-scheduler.ps1
```

Перезапусти Claude Code. Новые команды появятся автоматически.

## Детали команд

### /research — Полный пайплайн исследования

Три фазы, полностью автономно:

**Фаза 1 — Сбор:** Создаёт NotebookLM ноутбук, принимает любой микс источников (YouTube, веб-страницы, Google Drive, текст), добавляет с отслеживанием прогресса.

**Фаза 2 — Анализ:** Серия целевых запросов к ноутбуку — суммаризация, поиск паттернов, анализ противоречий, плюс твои вопросы. Возвращает структурированный отчёт с цитатами из ТВОИХ источников.

**Фаза 3 — Артефакты:** Опционально генерирует контент через NotebookLM Studio:

| Артефакт | Формат | Для чего |
|----------|--------|----------|
| Audio Overview | MP3 | Подкаст с двумя AI-ведущими, обсуждающими твои источники |
| Mind Map | JSON | Визуальная структура знаний |
| Flashcards | JSON/HTML | Карточки для запоминания из материалов |
| Briefing Doc | Markdown | Краткое резюме для руководства |
| Quiz | JSON/HTML | Тест на понимание материала |

### /youtube-research — YouTube без ошибок 429

YouTube transcript API всё чаще блокируется (HTTP 429). NotebookLM принимает YouTube нативно — без API-ключей, без лимитов.

```
/youtube-research React Server Components

> Вставь 1-10 YouTube ссылок:
https://youtu.be/abc123
https://youtu.be/def456
https://youtu.be/ghi789

→ Создаёт ноутбук, загружает все видео
→ Структурированный анализ с резюме по каждому видео
→ Паттерны и инсайты между видео
→ Опционально: сгенерировать подкаст из всех видео
```

### /init-notebook — Документация для твоего стека

Создаёт NotebookLM ноутбук с предзагруженной официальной документацией:

```
/init-notebook fastapi postgresql redis

→ Создаёт ноутбук "fastapi postgresql redis Docs"
→ Добавляет документацию FastAPI, PostgreSQL, Redis
→ Готов к запросам: "Как настроить connection pooling с FastAPI + PostgreSQL?"
```

Встроенные подсказки URL для 30+ фреймворков (Next.js, React, Supabase, Tailwind, Drizzle, Playwright, Electron и другие). Работает с любым URL — не ограничен встроенным списком.

Интегрирован с `/init-project` — предлагает создать ноутбук с документацией при старте нового проекта.

## Мониторинг авторизации

NotebookLM работает через cookies браузера (официального API нет). Cookies истекают. Скрипт проверки запускается ежедневно и предупреждает заранее:

```
[2026-03-23 10:00:01] AUTH OK — 5 notebooks accessible
[2026-03-25 10:00:01] AUTH EXPIRED — run: nlm login
```

На Windows: всплывающее уведомление при истечении cookies. На Linux/macOS: только лог-файл (PR с нативными уведомлениями приветствуются).

## Конфигурация

### Интеграция с CLAUDE.md

Включённый `config/CLAUDE.md` учит Claude проактивно проверять NotebookLM при работе с незнакомыми библиотеками. Добавь в глобальный конфиг:

```bash
# Безопасное добавление — не дублирует при повторном запуске
grep -q "notebooklm-claude-workflows" ~/.claude/CLAUDE.md 2>/dev/null || \
  cat ~/notebooklm-claude-workflows/config/CLAUDE.md >> ~/.claude/CLAUDE.md
```

До: Нужно самому помнить попросить Claude использовать NotebookLM.
После: Claude предлагает это автоматически, когда это полезно.

## Структура проекта

```
notebooklm-claude-workflows/
├── commands/
│   ├── youtube-research.md    # команда /youtube-research
│   ├── research.md            # команда /research (с авто-расширением + Obsidian)
│   ├── deep-research.md       # команда /deep-research
│   ├── init-notebook.md       # команда /init-notebook
│   ├── telegram-to-notebook.md # команда /telegram-to-notebook
│   ├── analytics-report.md    # команда /analytics-report
│   └── edit-source.md         # команда /edit-source
├── scripts/
│   ├── nlm-auth-check.sh      # ежедневная проверка cookies
│   ├── setup-nlm-scheduler.ps1 # настройка Task Scheduler
│   └── telegram-chunker.py    # Telegram JSON → чанки для NotebookLM
├── config/
│   └── CLAUDE.md              # глобальные инструкции Claude Code
├── README.md
├── README.ru.md
├── LICENSE
└── .gitignore
```

## FAQ

**Q: Это MCP-сервер?**
Нет. Это слой рабочих процессов поверх [notebooklm-mcp-cli](https://github.com/jacob-bd/notebooklm-mcp-cli). Думай об этом как о макросах и шаблонах для MCP-инструментов. MCP-сервер нужно установить отдельно.

**Q: Работает с Claude Desktop?**
Slash-команды специфичны для Claude Code. Пользователи Claude Desktop получают MCP-инструменты напрямую, но без автоматизации рабочих процессов. См. [документацию notebooklm-mcp-cli](https://github.com/jacob-bd/notebooklm-mcp-cli) для настройки Desktop.

**Q: Что с истечением cookies?**
Скрипт мониторинга проверяет ежедневно и уведомляет. Когда cookies истекают — просто запусти `nlm login`, это 30 секунд.

**Q: Могу добавить свои команды?**
Конечно. Положи любой `.md` файл в `~/.claude/commands/` в том же формате. Используй существующие команды как пример.

## Связанные проекты

- [notebooklm-mcp-cli](https://github.com/jacob-bd/notebooklm-mcp-cli) — MCP-сервер, на котором строится этот проект (обязателен)
- [claude-statusline](https://github.com/CreatmanCEO/claude-statusline) — Умная статус-строка для Claude Code (от того же автора)

## Лицензия

MIT — [Nick Podolyak](https://github.com/CreatmanCEO) / CREATMAN Studio
