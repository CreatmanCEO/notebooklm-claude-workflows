# /telegram-to-notebook — Импорт Telegram-чата в NotebookLM

Загружает экспорт Telegram-чата в NotebookLM. Поддерживает форум-чаты с темами (topics).
Фильтрует стикеры, GIF, видео. Сохраняет текст, код, PDF, документы.

## Параметр
$ARGUMENTS — путь к JSON-файлу экспорта Telegram ИЛИ название чата

## Предварительный шаг (пользователь делает сам)
1. В Telegram Desktop: чат → три точки → Export chat history
2. Формат: JSON (Machine-readable)
3. Медиа — можно не снимать, скрипт сам отфильтрует

## Действия

### Шаг 1: Определи тип чата
1. Запусти скрипт с `--list-topics` чтобы определить структуру:
   ```bash
   python ~/notebooklm-claude-toolkit/scripts/telegram-chunker.py "$ARGUMENTS" --list-topics
   ```
2. Если чат содержит топики (форум) — предложи варианты:
   - **По темам** (`--per-topic`): отдельный файл на каждую тему — лучше для целевого анализа
   - **Выборочно** (`--per-topic --topics "Docker,FAQ"`): только конкретные темы
   - **Всё вместе** (без флагов): один файл с заголовками тем — лучше для общего обзора

### Шаг 2: Конвертация
3. Запусти скрипт с выбранным режимом:
   ```bash
   # Все темы по отдельности
   python ~/notebooklm-claude-toolkit/scripts/telegram-chunker.py "$ARGUMENTS" --per-topic

   # Конкретные темы
   python ~/notebooklm-claude-toolkit/scripts/telegram-chunker.py "$ARGUMENTS" --per-topic --topics "Docker,Feature requests"

   # Всё вместе (обычный чат или общий обзор)
   python ~/notebooklm-claude-toolkit/scripts/telegram-chunker.py "$ARGUMENTS"
   ```
4. Скрипт выведет: количество сообщений, слов, пропущенных (стикеры/GIF/видео), созданных файлов

### Шаг 3: Загрузка в NotebookLM
5. Создай ноутбук "Telegram: [название чата]" через `notebook_create`
6. Для каждого файла из output-dir:
   - Прочитай содержимое файла
   - Добавь через `source_add`:
     - `source_type`: "text"
     - `text`: содержимое файла
     - `title`: имя файла (например "Telemt_Docker")
     - `wait`: true
7. Показывай прогресс: "Загружено 3/13 файлов..."
8. Покажи итог: название ноутбука, ID, количество источников, слов
9. Предложи задать вопрос через `notebook_query`

## Примеры
```
/telegram-to-notebook C:\Users\creat\Downloads\ChatExport\result.json
/telegram-to-notebook чат про Docker
```
