# Kittygram Backend

Учебный Django REST API для каталога котов. Пользователи регистрируются через Djoser, получают токен и управляют своими котами. Чтение котов и достижений доступно без входа; менять кота может его владелец.

## Локальный запуск

Нужен Python 3.9 и зависимости из `requirements.txt`.

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python manage.py migrate
.venv/Scripts/python manage.py runserver
```

В Linux/macOS используйте `.venv/bin/python`. `.env.example` содержит примеры переменных окружения; файл `.env` Django сам не загружает, задайте значения в оболочке перед запуском. Для локальной разработки есть временные значения по умолчанию; для внешнего доступа задайте `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0`, `DJANGO_ALLOWED_HOSTS` и подходящий `DJANGO_CORS_ALLOWED_ORIGINS`. По умолчанию разрешены адреса фронтенда `localhost:3000` и `127.0.0.1:3000`. `DJANGO_DB_PATH` позволяет выбрать другую SQLite базу. Личные `db.sqlite3` и `media/` остаются локальными.

API: `/api/cats/`, `/api/achievements/`, `/api/users/`, `/api/token/login/`, `/api/token/logout/`. Изображение кота можно передать как `data:image/jpeg;base64,...`. Клиент находится в отдельном проекте `kittygram_frontend`.

Проверка: `python manage.py check` и `python manage.py test`. Секрет, ранее записанный в истории Git, при реальном развёртывании надо заменить и удалить из истории отдельно.
