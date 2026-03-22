# /research — Полный цикл исследования через NotebookLM

## Параметр
$ARGUMENTS — тема исследования

## Фаза 1: Сбор источников

1. Создай NotebookLM ноутбук "Research: $ARGUMENTS" через `notebook_create`
2. Спроси пользователя об источниках. Принимай любые комбинации:
   - YouTube ссылки
   - Веб-страницы / документация
   - Google Drive документы (нужен document_id)
   - Текст напрямую
3. Добавляй каждый источник через `source_add`:
   - YouTube и веб-ссылки: `source_type=url`
   - Google Drive: `source_type=drive`, `document_id=...`
   - Текст: `source_type=text`, `title=...`
   - Всегда `wait=true`
4. Показывай прогресс: "Загружено 3/7 источников..."

## Фаза 2: Анализ

5. Выполни серию `notebook_query` к созданному ноутбуку:
   - "Суммаризируй ключевые идеи из всех источников"
   - "Какие паттерны и общие темы прослеживаются?"
   - "Какие противоречия или расхождения есть между источниками?"
6. Если пользователь задал конкретный вопрос — задай его тоже
7. Выведи структурированный отчёт:
   - Обзор темы
   - Ключевые находки (с цитатами)
   - Паттерны и тренды
   - Противоречия (если есть)
   - Выводы и рекомендации

## Фаза 3: Артефакты (по запросу)

8. Предложи сгенерировать на выбор:
   - **Audio Overview** (подкаст) — `studio_create`, `artifact_type=audio`
   - **Mind Map** — `studio_create`, `artifact_type=mind_map`
   - **Flashcards** — `studio_create`, `artifact_type=flashcards`
   - **Briefing Doc** — `studio_create`, `artifact_type=report`
   - **Quiz** — `studio_create`, `artifact_type=quiz`
9. После запуска генерации проверяй статус через `studio_status`
10. Скачивай готовые артефакты через `download_artifact` в `~/Downloads/`
