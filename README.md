# Task Management API

## Описание
Task Management API — это RESTful API для управления задачами с поддержкой авторизации через JWT, логирование HTTP-запросов и аналитику задач.

## Технологии
- Python 3.11+
- Django 5.1+
- Django REST Framework (DRF)
- Simple JWT
- PostgreSQL

## Установка
1. Клонируйте репозиторий:
   ```sh
   git clone https://github.com/Atsamazik/task_manager.git
   cd task_manager
   ```
2. Установите зависимости:
   ```sh
   poetry install
   ```
3. Выполните миграции:
   ```sh
   poetry run python manage.py makemigrations
   poetry run python manage.py migrate
   ```
4. Запуск сервера:
   ```sh
   poetry run python manage.py runserver
   ```

## API-Эндпоинты
### Аутентификация
- **POST /api/register/** - регистрация нового пользователя
- **POST /api/login/** - вход (возвращает JWT)
- **POST /token/refresh/** - обновление токена

### Задачи
- **GET /api/v1/tasks/** - список задач
- **POST /api/v1/tasks/** - создание новой задачи
- **GET /api/v1/tasks/{id}/** - детали задачи
- **PUT /api/v1/tasks/{id}/** - обновление задачи
- **DELETE /api/v1/tasks/{id}/** - удаление задачи

### Аналитика
- **GET /api/v1/analytics/** - статистика по задачам

## Аутентификация
API использует JWT (токен добавляется в Authorization заголовок):
```sh
Authorization: Bearer your_access_token
```

## Логирование
Middleware логирует HTTP-запросы (метод, URL, статус).
Логи пишутся в `logs/`.

## Тесты
Запуск тестов:
```sh
pytest
```

