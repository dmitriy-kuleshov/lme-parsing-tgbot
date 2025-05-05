# LME Parsing Bot

Этот проект — Telegram-бот для парсинга и обработки данных, связанных с LME (London Metal Exchange).

## 📁 Структура проекта

```
lme-parsing-bot/
├── .venv/                  # Виртуальное окружение
├── src/
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── handlers.py     # Обработка сообщений/команд
│   │   └── keyboards.py    # Кастомные клавиатуры Telegram
│   ├── lme_parser/
│   │   ├── __init__.py
│   │   ├── full_parser.py  # Основная логика парсинга
│   │   └── generate_file.py# Генерация файлов на основе данных
│   ├── config.py           # Конфигурация проекта (токены и пр.)
│   ├── requirements.txt    # Зависимости
│   └── main.py             # Точка входа, запуск бота
```

## 🚀 Установка и запуск

1. Клонируйте репозиторий:

```
git clone https://github.com/yourusername/lme-parsing-bot.git
cd lme-parsing-bot
```

2. Создайте и активируйте виртуальное окружение (опционально):

```
python -m venv .venv
source .venv/bin/activate     # Для Linux/Mac
.venv\Scripts\activate      # Для Windows
```

3. Установите зависимости:

```
pip install -r src/requirements.txt
```

4. Настройте файл `config.py`:

Убедитесь, что в `src/config.py` указаны нужные параметры, такие как токен Telegram бота и другие настройки.

5. Запустите бота:

```
python src/main.py
```


