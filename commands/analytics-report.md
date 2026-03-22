# /analytics-report — Аналитика → NotebookLM → Инфографика/Отчёт

Загружает данные аналитики (CSV, JSON, текст) в NotebookLM и генерирует визуальные артефакты.

## Параметр
$ARGUMENTS — описание данных или путь к файлу

## Действия

### Фаза 1: Сбор данных

1. Определи тип входных данных:
   - **Файл** (CSV, JSON, TXT) — прочитай и подготовь как текстовый источник
   - **YouTube аналитика** — спроси у пользователя данные или путь к экспорту
   - **Произвольные данные** — прими текст/таблицу от пользователя
2. Создай ноутбук "Analytics: $ARGUMENTS" через `notebook_create`
3. Загрузи данные через `source_add`:
   - Файлы: `source_type=file` если PDF, или `source_type=text` для CSV/JSON (преобразуй в читаемый текст)
   - URL: `source_type=url`
   - Всегда `wait=true`

### Фаза 2: Анализ

4. Выполни серию `notebook_query`:
   - "Какие ключевые метрики и показатели содержатся в данных?"
   - "Выдели топ-5 трендов и аномалий"
   - "Какие actionable выводы можно сделать на основе этих данных?"
5. Если пользователь задал конкретный вопрос — задай его тоже

### Фаза 3: Генерация артефактов

6. Предложи на выбор (или сгенерируй все по запросу):
   - **Инфографика** — `studio_create`, `artifact_type=infographic`, `confirm=true`, предложи выбрать стиль:
     - `professional` — для презентаций
     - `sketch_note` — для заметок
     - `bento_grid` — модный grid-макет
     - и другие (editorial, instructional, bricks, clay, anime, kawaii, scientific)
   - **Data Table** — `studio_create`, `artifact_type=data_table`, `confirm=true`
   - **Briefing Doc** — `studio_create`, `artifact_type=report`, `confirm=true`
   - **Презентация** — `studio_create`, `artifact_type=slide_deck`, `confirm=true`
7. Проверяй готовность через `studio_status`
8. Скачивай через `download_artifact`, указав полный `output_path` (например `~/Downloads/analytics-infographic.png`), а не только директорию
9. Покажи путь к скачанным файлам
