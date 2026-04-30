# notebooklm-claude-workflows

[![License: MIT](https://img.shields.io/github/license/CreatmanCEO/notebooklm-claude-workflows?color=yellow)](LICENSE)
[![Stars](https://img.shields.io/github/stars/CreatmanCEO/notebooklm-claude-workflows?style=flat&color=yellow)](https://github.com/CreatmanCEO/notebooklm-claude-workflows/stargazers)
[![Validate](https://github.com/CreatmanCEO/notebooklm-claude-workflows/actions/workflows/validate.yml/badge.svg)](https://github.com/CreatmanCEO/notebooklm-claude-workflows/actions/workflows/validate.yml)
[![Built on notebooklm-mcp-cli](https://img.shields.io/badge/built%20on-notebooklm--mcp--cli-9d6cff)](https://github.com/jacob-bd/notebooklm-mcp-cli)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Opus%204.7%20%C2%B7%201M%20context-cc785c)](https://code.claude.com)
[![MCP](https://img.shields.io/badge/MCP-compatible-22c55e)](https://modelcontextprotocol.io)
[![platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-blue)](#prerequisites)

🇷🇺 Русский · [🇬🇧 English](README.md)

**Семь slash-команд Claude Code, которые превращают сырые MCP-вызовы NotebookLM в одну строку. Протестировано на форуме Telegram из 41K сообщений, YouTube research-пайплайнах и авто-документации для 30+ фреймворков.**

> **MCP-сервер = у Claude есть руки в NotebookLM.**
> **Workflow-команды = у Claude есть руки + чек-лист.**

![Архитектура pipeline: slash-команда → 3-фазный пайплайн → MCP tools → NotebookLM](docs/architecture.svg)

## Проблема

[notebooklm-mcp-cli](https://github.com/jacob-bd/notebooklm-mcp-cli) даёт Claude доступ к NotebookLM — но как сырые tool'ы. Создать ноутбук, добавить 5 источников, опросить, сгенерировать подкаст — это 10+ ручных tool-call'ов. Оркестрация падает на тебя.

**Этот проект решает это.** Slash-команды превращают многошаговые операции NotebookLM в однострочники:

```
/research AI agents 2026          → полный research-цикл с артефактами
/youtube-research LLM fine-tuning → YouTube видео → анализ → подкаст
/init-notebook next.js supabase   → ноутбук с документацией под твой стек
```

## Зачем команды, а не просто MCP?

Claude Code с MCP-сервером *может* сам сообразить что делать. Но между «может» и «делает надёжно» — пропасть:

| | Сырые MCP-tool'ы | С workflow-командами |
|---|---|---|
| Создаёт ноутбук | да | да |
| Добавляет источники с `wait=true` | иногда забывает | всегда |
| Multi-angle анализ (summary + patterns + contradictions) | обычно один вопрос | всегда полная серия |
| Предлагает артефакты (подкаст, mind map) | редко | всегда |
| Структурированный вывод с цитатами | непостоянно | стандартизировано |
| Работает одинаково каждый раз | зависит от контекста / настроения | детерминировано |

Команды — не костыль. Это **стандартизация процесса**. Разница между *«напиши мне deploy-скрипт»* и `make deploy`. Tool'ы у Claude те же — но команды гарантируют качество workflow каждый раз.

## Что возвращает `/research`

![Mock-up вывода /research: структурированные находки, паттерны, противоречия с цитатами на NotebookLM-источники](docs/output-mockup.svg)

Цитаты `[1]–[8]` ссылаются на твои NotebookLM-источники — клик в NotebookLM открывает точный фрагмент.

## Замеренное влияние

Реальные продакшн-сценарии с конкретными числами:

| Сценарий | Без workflow-команд | С workflow-командами |
|---|---|---|
| Research-pipeline (5 источников → анализ → подкаст) | 10+ ручных tool-call'ов, ~3 мин оркестрации | 1 промпт, автономно |
| Импорт Telegram forum-supergroup | Нерешаемо — один источник > лимита 500 KB | 41K сообщений · 12 топиков · 586K слов · 13 NotebookLM источников, **меньше 2 минут** |
| Сбор YouTube-транскриптов | YouTube transcript API возвращают HTTP 429 / заблокированы | 1–10 видео через нативный ingest NotebookLM, без API-ключей |
| Ноутбук с документацией стека | Вручную: найти URL × N, вставить × N | `/init-notebook fastapi postgres redis` — 30+ фреймворков предмаплены |
| Мониторинг куки авторизации | «Узнаёшь что куки истекли когда что-то ломается» | Дневная проверка, Windows toast-уведомление до того как сломается |

## Что внутри

### Slash-команды

| Команда | Что делает |
|---|---|
| `/research <тема>` | Полный цикл: сбор → авто-расширение через web search → multi-query анализ → Obsidian export → опциональные артефакты |
| `/deep-research <тема>` | Multi-iteration deep dive: строит дерево тем, задаёт 3–5 уточняющих вопросов на каждую, синтезирует комплексный отчёт |
| `/youtube-research <тема>` | Анализ YouTube-видео через NotebookLM. Заменяет ломающиеся transcript-API (429-ошибки). 1–10 видео → структурированный анализ с цитатами |
| `/init-notebook <стек>` | Авто-создание NotebookLM-ноутбука с официальной документацией. URL-подсказки для 30+ популярных фреймворков |
| `/telegram-to-notebook` | Импорт Telegram-чатов включая **forum-supergroups с топиками**. Авто-определение топиков, per-topic export, фильтрация стикеров/GIF/видео, оставляет текст/код/PDF |
| `/analytics-report` | Аналитические данные (CSV / JSON / API) → анализ через NotebookLM → инфографика, таблица, слайды или briefing-документ |
| `/edit-source` | Редактирование NotebookLM-источников через extract → edit → replace workaround. Поддерживает Drive sync для Google Docs |

### Когда какую research-команду выбрать

| Кейс | Команда |
|---|---|
| One-pass research с 3 углами (summary / patterns / contradictions) | `/research` |
| Глубокое погружение с 5 вопросами на топик и деревом знаний | `/deep-research` |
| Конкретно YouTube как первичные источники | `/youtube-research` |
| Telegram forum / supergroup ingestion | `/telegram-to-notebook` |

### Автоматизация

| Компонент | Что делает |
|---|---|
| `nlm-auth-check.sh` | Дневная проверка здоровья куки + Windows toast при истечении |
| `setup-nlm-scheduler.ps1` | One-click установка через Windows Task Scheduler |
| `config/CLAUDE.md` | Global-инструкции, чтобы Claude проактивно предлагал NotebookLM при работе с незнакомыми технологиями |

## Зависимости

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) установлен и работает
- [notebooklm-mcp-cli](https://github.com/jacob-bd/notebooklm-mcp-cli) установлен и авторизован:
  ```bash
  uv tool install notebooklm-mcp-cli
  nlm login
  nlm setup add claude-code
  ```
- Перезапусти Claude Code после MCP-настройки

## Установка

### Быстрая (одна команда)

Открой Claude Code и скажи:

```
Клонируй https://github.com/CreatmanCEO/notebooklm-claude-workflows и установи
```

Claude склонирует репо и положит команды в нужные места.

### Ручная

```bash
# Клон
git clone https://github.com/CreatmanCEO/notebooklm-claude-workflows.git ~/notebooklm-claude-workflows

# Скопировать slash-команды
cp ~/notebooklm-claude-workflows/commands/*.md ~/.claude/commands/

# (Опционально) NotebookLM-инструкции в global config
# Безопасный append — не дублируется
grep -q "notebooklm-claude-workflows" ~/.claude/CLAUDE.md 2>/dev/null || \
  cat ~/notebooklm-claude-workflows/config/CLAUDE.md >> ~/.claude/CLAUDE.md

# (Опционально) Auth monitoring — только Windows
mkdir -p ~/Documents/scripts
cp ~/notebooklm-claude-workflows/scripts/* ~/Documents/scripts/
chmod +x ~/Documents/scripts/nlm-auth-check.sh
powershell -ExecutionPolicy Bypass -File ~/Documents/scripts/setup-nlm-scheduler.ps1
```

Перезапусти Claude Code. Новые команды появятся автоматически.

## Детали команд

### /research — полный research-pipeline

Три фазы, полностью автономно:

**Фаза 1 — Сбор** · Создаёт NotebookLM-ноутбук, принимает любой микс источников (YouTube, веб-страницы, Google Drive, текст), добавляет с прогрессом. Опционально автоматически расширяет базу через `research_start`.

**Фаза 2 — Анализ** · Серия точечных запросов к ноутбуку — суммаризация, поиск паттернов, анализ противоречий + твои кастомные вопросы. Возвращает структурированный отчёт с цитатами из источников.

**Фаза 3 — Артефакты** · Опционально генерирует NotebookLM Studio контент:

| Артефакт | Формат | Use case |
|---|---|---|
| Audio Overview | MP3 | Подкаст с двумя AI-ведущими |
| Mind Map | JSON | Визуальная структура знаний |
| Flashcards | JSON / HTML | Карточки для запоминания |
| Briefing Doc | Markdown | Executive summary |
| Quiz | JSON / HTML | Тест по материалу |

### /youtube-research — YouTube без 429-ошибок

YouTube transcript API всё чаще блокируются (HTTP 429). NotebookLM нативно понимает YouTube — без API-ключей, без rate limits.

```
/youtube-research React Server Components

> Вставь 1–10 YouTube-ссылок:
https://youtu.be/abc123
https://youtu.be/def456
https://youtu.be/ghi789

→ Создаётся ноутбук, заливаются все видео
→ Структурированный анализ с per-video summary
→ Cross-video паттерны и инсайты
→ Опционально: подкаст из всех видео
```

### /init-notebook — документация под твой стек

Создаёт NotebookLM-ноутбук с предзагруженной официальной документацией:

```
/init-notebook fastapi postgresql redis

→ Создаётся "fastapi postgresql redis Docs"
→ Добавляются FastAPI docs, PostgreSQL docs, Redis docs
→ Готов к запросам: "Как настроить connection pooling FastAPI + PostgreSQL?"
```

URL-подсказки для 30+ фреймворков (Next.js, React, Supabase, Tailwind, Drizzle, Playwright, Electron и т.д.). Работает с любым URL — не ограничено встроенным списком.

### /telegram-to-notebook — форум-чаты с топиками

Единственный инструмент, который умеет в Telegram **forum-supergroups** (чаты с вложенными топиками / тредами). Авто-определение структуры топиков и три режима экспорта:

```
/telegram-to-notebook result.json

> Найдено 12 топиков:
  [598] Latest: 69 сообщений
  [599] Offtop RU: 10 627 сообщений
  [17296] Docker: 867 сообщений
  ...

> Режим экспорта?
  1. Per-topic (отдельный файл на топик) ← лучшее для точечного анализа
  2. Filtered (только конкретные топики)
  3. All together (один файл с заголовками топиков)
```

**Smart-фильтрация:** пропускает стикеры, GIF, видео. Оставляет текстовые сообщения, код, документы (PDF, JSON, YAML, Python, Go и т.д.). Оптимизировано под IT-комьюнити и research-каналы.

**Протестировано:** 41K сообщений, 12 топиков, 586K слов → 13 файлов в NotebookLM меньше чем за 2 минуты.

```bash
# Список топиков без экспорта
python scripts/telegram-chunker.py result.json --list-topics

# Экспорт всех топиков отдельно
python scripts/telegram-chunker.py result.json --per-topic

# Только Docker и FAQ
python scripts/telegram-chunker.py result.json --per-topic --topics "Docker,FAQ Remake"
```

## Auth monitoring

NotebookLM использует браузерные куки (нет официального API). Куки истекают. Auth-check скрипт работает каждый день и предупреждает заранее:

```
[2026-03-23 10:00:01] AUTH OK — 5 ноутбуков доступно
[2026-03-25 10:00:01] AUTH EXPIRED — запусти: nlm login
```

Windows: toast-уведомление при истечении. Linux/macOS: только лог-файл (PR на нативные уведомления приветствуются — см. [`CONTRIBUTING.md`](CONTRIBUTING.md)).

## Конфигурация

### Интеграция CLAUDE.md

`config/CLAUDE.md` учит Claude проактивно проверять NotebookLM при работе с незнакомыми библиотеками. Добавь в global config:

```bash
# Безопасный append
grep -q "notebooklm-claude-workflows" ~/.claude/CLAUDE.md 2>/dev/null || \
  cat ~/notebooklm-claude-workflows/config/CLAUDE.md >> ~/.claude/CLAUDE.md
```

До: ты должен помнить, чтобы попросить Claude использовать NotebookLM.
После: Claude сам предлагает, когда это поможет.

## Ограничения

Это workflow-слой над `notebooklm-mcp-cli`, который сам — обёртка над неофициальным браузерным API NotebookLM. Честные ограничения:

- **Истечение куки — реальное и регулярное.** У NotebookLM нет официального API; MCP-сервер работает через куки браузера, которые истекают по расписанию Google (обычно раз в несколько недель). Auth-check ловит это заранее, но `nlm login` всё равно нужен. Считай ~30 секунд friction раз в 2–3 недели.
- **500K слов на источник.** NotebookLM ограничивает каждый источник 500K слов. Telegram chunker по умолчанию делает 300K на чанк с запасом. Для очень больших корпусов планируй несколько чанков на топик.
- **`/edit-source` — workaround, не нативная фича.** У NotebookLM нет API для редактирования источника. Команда делает extract → edit → replace, что означает короткое окно когда источник отсутствует в ноутбуке. Не запускай посреди серии запросов.
- **Определение forum-supergroup — эвристика.** Telegram chunker определяет топики по полям `topic_message_id` и действиям `forum_topic_created`. Telegram уже менял формат экспорта; если экспорт из старой версии клиента — определение топиков может ошибиться. Сначала `--list-topics` для проверки.
- **Rate limits NotebookLM непрозрачны.** Google не публикует их. MCP-сервер ретраит на 429, но heavy-research сессии (50+ запросов подряд) иногда стопорятся. Workaround: разделяй на несколько ноутбуков.
- **Slash-команды — только Claude Code.** Claude Desktop получает сырые MCP-tool'ы без workflow-автоматизации — см. [notebooklm-mcp-cli](https://github.com/jacob-bd/notebooklm-mcp-cli) для Desktop setup.
- **Native-уведомления пока только Windows.** macOS `osascript` и Linux `notify-send` — открытые контрибы в [`CONTRIBUTING.md`](CONTRIBUTING.md).
- **Вся система зависит от upstream MCP-сервера.** Если `notebooklm-mcp-cli` ломается, ломаются все команды. Пинуй известно-рабочую версию MCP в продакшне.

## FAQ

**Q: Это MCP-сервер?**
Нет. Это workflow-слой поверх [notebooklm-mcp-cli](https://github.com/jacob-bd/notebooklm-mcp-cli). Думай как макросы + шаблоны для MCP-tool'ов. MCP-сервер должен быть установлен сначала.

**Q: Работает с Claude Desktop?**
Slash-команды специфичны для Claude Code. Desktop получает MCP-tool'ы напрямую, но без workflow-автоматизации. См. [notebooklm-mcp-cli docs](https://github.com/jacob-bd/notebooklm-mcp-cli) для Desktop.

**Q: Что делать с истечением куки?**
Скрипт auth monitoring проверяет ежедневно и уведомляет. Когда куки истекли — `nlm login` за 30 секунд.

**Q: Можно ли добавлять свои команды?**
Конечно. Положи любой `.md` в `~/.claude/commands/` в том же формате. См. существующие команды как примеры и [`CONTRIBUTING.md`](CONTRIBUTING.md) для приоритетов.

## Структура проекта

```
notebooklm-claude-workflows/
├── commands/
│   ├── research.md            # /research — полный pipeline
│   ├── deep-research.md       # /deep-research — multi-iteration deep dive
│   ├── youtube-research.md    # /youtube-research — YouTube через NotebookLM
│   ├── init-notebook.md       # /init-notebook — ноутбук под стек
│   ├── telegram-to-notebook.md # /telegram-to-notebook — forum-aware импорт
│   ├── analytics-report.md    # /analytics-report — данные → инфографика / отчёт
│   └── edit-source.md         # /edit-source — extract → edit → replace
├── scripts/
│   ├── telegram-chunker.py    # Telegram JSON → NotebookLM чанки (forum-aware)
│   ├── nlm-auth-check.sh      # Дневная проверка куки
│   └── setup-nlm-scheduler.ps1 # Windows Task Scheduler установщик
├── config/
│   └── CLAUDE.md              # Сниппет global-инструкций Claude Code
├── docs/
│   ├── architecture.svg       # Pipeline-диаграмма
│   └── output-mockup.svg      # Mock-up вывода /research
├── README.md
├── README.ru.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CLAUDE.md                  # Level 1 файл этого репо (eats own dog food)
├── LICENSE
└── .github/workflows/validate.yml
```

## Связанные проекты

- [notebooklm-mcp-cli](https://github.com/jacob-bd/notebooklm-mcp-cli) — MCP-сервер, на который опирается этот проект (обязателен)
- [Claude Code Anti-Regression Setup](https://github.com/CreatmanCEO/claude-code-antiregression-setup) — sister-репо, тот же автор. CLAUDE.md + субагенты + хуки чтобы Claude не сломал твой код пока крутит эти workflow.
- [ai-context-hierarchy](https://github.com/CreatmanCEO/ai-context-hierarchy) — sister-репо. Трёхуровневая система контекста; `config/CLAUDE.md` отсюда — Level 0 фрагмент, который натурально вливается в её иерархию.
- [claude-statusline](https://github.com/CreatmanCEO/claude-statusline) — sister-репо. Умная status-строка для Claude Code; дополняющий инструмент той же экосистемы.

## Контрибьют

PR приветствуются — см. [CONTRIBUTING.md](CONTRIBUTING.md). Текущие приоритеты: native-уведомления для Linux/macOS auth-check, расширение URL-словаря в `/init-notebook`, новые slash-команды (PDF research, podcast-to-notebook), переводы команд на другие локали.

## Автор

**Николай Подоляк (Nick Podolyak)** — Python-разработчик и цифровой архитектор в [CREATMAN](https://creatman.site)

- GitHub: [@CreatmanCEO](https://github.com/CreatmanCEO)
- Habr: [creatman](https://habr.com/ru/users/creatman/)
- dev.to: [@creatman](https://dev.to/creatman)

## Лицензия

[MIT](LICENSE) · Николай Подоляк
