# Task Management API

## Описание
Task Management API — это RESTful API для управления задачами с поддержкой авторизации через JWT, логирование HTTP-запросов и аналитику задач.

## Технологии
- Python 3.11+
- Django 5.1+
- Django REST Framework (DRF)
- Simple JWT
- PostgreSQL
- Docker + Docker Compose

## Запуск с Docker Compose

! Перед запуском убедитесь, что порты 5432 и 8000 не заняты

1. Клонируйте репозиторий:
   ```sh
   git clone https://github.com/Atsamazik/task_manager.git
   cd task_manager
   ```

2. Создайте файл `.env` в корневой папке и добавьте в него следующее содержимое:
   ```sh
   SECRET_KEY=<вставьте сюда ключ>
   DEBUG=False
   DATABASE_NAME=postgres
   DATABASE_USER=postgres
   DATABASE_PASSWORD=postgres
   DATABASE_HOST=db
   DATABASE_PORT=5432
   ALLOWED_HOSTS=*
   ```
3. Добавьте SECRET_KEY в .env
4. Соберите и запустите контейнеры:
   ```sh
   docker-compose up --build -d
   ```

5. API будет доступен по адресу:
   ```sh
   http://0.0.0.0:8000/
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

### Документация
- **GET /api/docs/** - Swagger
- **GET /api/redoc/** - Redoc

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
docker-compose exec web pytest
```

