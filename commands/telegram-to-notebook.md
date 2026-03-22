# /telegram-to-notebook — Импорт Telegram-чата в NotebookLM

Загружает экспорт Telegram-чата в NotebookLM, автоматически разбивая на чанки.

## Параметр
$ARGUMENTS — путь к JSON-файлу экспорта Telegram ИЛИ название чата

## Предварительный шаг (пользователь делает сам)
1. В Telegram Desktop: чат → три точки → Export chat history
2. Формат: JSON
3. Снять галочки с медиа (фото, видео, голосовые) — нужен только текст

## Действия

### Вариант A: Пользователь уже имеет JSON файл
1. Запусти скрипт разбивки:
   ```bash
   python ~/notebooklm-claude-toolkit/scripts/telegram-chunker.py "$ARGUMENTS" --output-dir /tmp/tg-chunks
   ```
2. Скрипт выведет: количество сообщений, слов, созданных чанков

### Вариант B: Пользователь указал только название
1. Спроси путь к JSON-файлу экспорта

### Загрузка в NotebookLM
3. Создай ноутбук "Telegram: [название чата]" через `notebook_create`
4. Для каждого чанка из output-dir:
   - Прочитай содержимое файла
   - Добавь как текстовый источник через `source_add`:
     - `source_type`: "text"
     - `text`: содержимое файла
     - `title`: имя файла (например "ChatName_part001")
     - `wait`: true
5. Показывай прогресс: "Загружено 3/7 чанков..."
6. После загрузки всех чанков покажи итог:
   - Название ноутбука и ID
   - Количество загруженных источников
   - Общее количество сообщений и слов
7. Предложи задать первый вопрос к чату через `notebook_query`

## Примеры использования
```
/telegram-to-notebook C:\Users\creat\Downloads\ChatExport\result.json
/telegram-to-notebook чат владельцев Geely Tugella
```
