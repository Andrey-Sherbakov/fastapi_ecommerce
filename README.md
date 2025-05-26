# FastAPI Ecommerce

Асинхронный API интернет магазина разработанный на FastAPI.

## Особенности

* Авторизация и регистрация пользователей при помощи OAuth2 и JWT
* CRUD операции для товаров, категорий, пользователей и отзывов
* Реализована система ролей и уровней доступа
* Асинхронная работа с базой данной PostgreSQL при помощи драйвера asyncpg и ORM SQLAlchemy
* Реализовано логирование с помощью loguru
* Контейнеризация Docker для удобного развертывания

## Установка и запуск

### Docker

1. Клонировать репозиторий:
    ```shell
    git clone https://github.com/Andrey-Sherbakov/fastapi_ecommerce.git
    cd fastapi_ecommerce
    ```
2. Изменить данные в файле .sample.env на свои и переименовать его в .env
3. Запустить docker compose:
    ```shell
    docker compose up --build
    ```
   _вместе с основным контейнером поднимется также база данных PostgreSQL а также Adminer для
   управления ей по адресу http://127.0.0.1:8080/_
4. Применить миграции:
    ```shell
    docker compose exec fast alembic upgrade head
    ```

### Pip venv

1. Клонировать репозиторий:
    ```shell
    git clone https://github.com/Andrey-Sherbakov/fastapi_ecommerce.git
    cd fastapi_ecommerce
    ```
2. Изменить данные в файле .sample.env на свои и переименовать его в .env
3. Создать и активировать виртуальное окружение:
   ```shell
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   ```
4. Установить зависимости:
   ```shell
   pip install -r requirements.txt
   ```
5. Применить миграции:
   ```shell
   alembic upgrade head
   ```
6. Запустить приложение:
   ```shell
   uvicorn app.main:app --reload
   ```

## API

После запуска документация доступна по адресу http://127.0.0.1:8000/docs/
![image](https://drive.google.com/uc?id=12NK0NS9vbYMgWEyNZu-RFDBlpDRz9Q1y)

## Структура проекта

```
.
├── app
│     ├── backend
│     │     ├── db.py
│     │     └── db_depends.py
│     ├── fixtures
│     │     ├── categories.csv
│     │     ├── db.dumb
│     │     └── products.csv
│     ├── helpers
│     │     ├── auth.py
│     │     └── review.py
│     ├── migrations
│     │     ├── versions
│     │     │     └── ...
│     │     ├── README
│     │     ├── env.py
│     │     └── script.py.mako
│     ├── models
│     │     ├── category.py
│     │     ├── products.py
│     │     ├── review.py
│     │     └── user.py
│     ├── routers
│     │     ├── auth.py
│     │     ├── category.py
│     │     ├── permissions.py
│     │     ├── products.py
│     │     └── review.py
│     ├── main.py
│     ├── middleware.py
│     └── schemas.py
├── nginx
│     ├── Dockerfile
│     └── fastapi_ecommerce.conf
├── .sample.env
├── Dockerfile
├── Dockerfile.prod
├── LICENSE
├── README.md
├── alembic.ini
├── docker-compose.prod.yml
├── docker-compose.yml
├── info.log
└── requirements.txt
```