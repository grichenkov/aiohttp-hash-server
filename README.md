## aiohttp-hash-server

Этот проект представляет собой приложение для хэширования строк с использованием aiohttp.


## Техническое задание

Приложение должно предоставлять следующие возможности:
- Принимать POST-запросы с JSON-объектом, содержащим строку для хэширования.
- Возвращать хэш SHA-256 для принятой строки в виде JSON-ответа.
- Предоставлять эндпоинт для проверки доступности (healthcheck).

## Локальная установка

Создать виртуальное окружение:

```bash
python -m venv venv
```

Активировать виртуальное окружение:

```bash
source venv/bin/activate
```

Установить Poetry

```bash
pip install poetry
```

Установить зависимости проекта:

```bash
poetry install
```

## Локальный запуск приложения

```bash
poetry run aiohttp-hash-server --host 0.0.0.0 --port 8080
```

## Локальный запуск тестов

```bash
poetry run pytest tests
```

## Запуск контейнера

Собрать Docker-образ:

```bash
docker build -t my-app .
```

Запустить контейнер:

```bash
docker run -d -p 8080:8080 -e HOST=0.0.0.0 -e PORT=8080 my-app
```

## Проверка линтеров и форматтеров

```bash
black app
black tests
```

```bash
mypy app
mypy tests
```

```bash
flake8 app
flake8 tests
```
