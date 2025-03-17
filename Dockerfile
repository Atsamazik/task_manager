# Используем официальный образ Python
FROM python:3.11

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1 \
    POETRY_HOME="/opt/poetry" \
    PATH="/opt/poetry/bin:$PATH"

# Устанавливаем Poetry 2+
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry --version

# Создаём рабочую директорию
WORKDIR /app

# Копируем файлы Poetry
COPY pyproject.toml poetry.lock ./

# Настраиваем Poetry (отключаем виртуальное окружение)
RUN poetry config virtualenvs.create false

# Устанавливаем зависимости
RUN poetry install --no-interaction --no-ansi --no-root

# Копируем весь проект
COPY . .

# Открываем порт для Django
EXPOSE 8000

# Запускаем сервер
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
