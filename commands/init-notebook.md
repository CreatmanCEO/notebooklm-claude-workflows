# /init-notebook — Создать NotebookLM ноутбук с документацией проекта

## Параметр
$ARGUMENTS — название проекта или список технологий (например: "next.js supabase deepgram")

## Действия

1. Создай NotebookLM ноутбук "$ARGUMENTS Docs" через `notebook_create`
2. Спроси пользователя какие технологии/библиотеки используются (если не указаны в $ARGUMENTS)
3. Для каждой технологии добавь официальную документацию через `source_add`:
   - `source_type`: "url"
   - `wait`: true
   - Используй getting-started / overview страницы документации
4. Покажи итог: название, ID ноутбука, количество загруженных источников
5. Предложи задать первый вопрос к ноутбуку через `notebook_query`

## Подсказки по URL документации (не ограничивайся этим списком)
- Next.js: https://nextjs.org/docs
- React: https://react.dev/reference/react
- Supabase: https://supabase.com/docs
- Deepgram: https://developers.deepgram.com/docs
- Suricata: https://docs.suricata.io/en/latest/
- n8n: https://docs.n8n.io/
- Drizzle ORM: https://orm.drizzle.team/docs/overview
- Tailwind CSS: https://tailwindcss.com/docs
- FastAPI: https://fastapi.tiangolo.com/
- Playwright: https://playwright.dev/docs/intro
- Electron: https://www.electronjs.org/docs/latest/
