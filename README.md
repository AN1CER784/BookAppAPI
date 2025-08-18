
# BookAppAPI

REST-API для управления библиотекой книг с отзывами, голосами, системой рекомендаций и прогрессом чтения.

---

## ​ Основной функционал

- **CRUD для книг, авторов, жанров, ссылок** на скачивание.
- **Отзывы и реплаи** — можно оставлять отзывы и отвечать на ответы. Доступны лайки/дизлайки на отзывы и реплаи, обобщённое через GenericFK.
- **Рекомендательная система** — на основе предпочтений пользователя (авторы, жанры) строятся рекомендуемые книги.
- **Swagger UI** — документация API доступна через `/swagger/` (используется drf-spectacular).
- **Асинхронные задачи** — через Celery можно запускать сервис рекомендательной системы.

---

##  Установка и запуск

1. Склонируйте репозиторий:
    ```bash
    git clone https://github.com/AN1CER784/BookAppAPI.git
    cd BookAppAPI
    ```

2. Установи зависимости:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Mac/Linux
    venv\Scripts\activate     # Windows
    pip install -r requirements.txt
    ```
3. Запустите docker конфигурации для бд и редис:
    ```bash
    docker compose up --build
    ```

4. Создайте и примените миграции:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
5. Спарсите данные о книгах:
    ```bash
    python manage.py fetchdata
    ```
6. Создать суперпользователя:
    ```bash
    python manage.py createsuperuser
    ```

7. Запустить сервер разработки:
    ```bash
    python manage.py runserver
    ```
    http://localhost:8000/api/v1/swagger/

---

##  Настройка и запуск Celery

### (Опционально для работы рекомендательной системы) Запусти beat (periodic tasks):

```bash
celery -A BookAppAPI beat --loglevel=info
```
---

## Документация API

Swagger UI: `/swagger/`
OpenAPI JSON/YAML (raw): `/api/v1/schema/`

