import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from tasks.models import Task

User = get_user_model()


# Fixtures
@pytest.fixture
def api_client():
    """Фикстура для неаутентифицированного API-клиента."""
    client = APIClient()
    client.default_format = "json"
    return client


@pytest.fixture
def user(db):
    """Фикстура для создания тестового пользователя."""
    return User.objects.create_user(username="test_user", email="test@example.com", password="password123")


@pytest.fixture
def auth_tokens(user):
    """Фикстура, создающая Refresh и Access токены для пользователя."""
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@pytest.fixture
def auth_api_client(api_client, auth_tokens):
    """Фикстура API-клиента с аутентификацией по JWT."""
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_tokens['access']}")
    return api_client


@pytest.fixture
def task(user):
    """Создаёт тестовую задачу."""
    return Task.objects.create(
        title="Test Task",
        description="Test Description",
        deadline=timezone.now() + timezone.timedelta(days=7),
        status="new",
        priority="middle"
    )


# Authenticated tests
def test_register_user(api_client, db):
    """Тест регистрации нового пользователя."""
    data = {"username": "new_user", "email": "new_user@example.com", "password": "password123"}
    response = api_client.post("/api/v1/register/", data)

    assert response.status_code == 201
    assert "username" in response.data
    assert "email" in response.data

def test_login_user(api_client, user):
    """Тест аутентификации пользователя (получение токенов)."""
    data = {"email": user.email, "password": "password123"}
    response = api_client.post("/api/v1/login/", data)

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data

def test_protected_endpoint_unauthenticated(api_client):
    """Тест запроса к защищённому эндпоинту без токена."""
    response = api_client.get("/api/v1/tasks/")

    assert response.status_code == 401
    assert response.data.get("details").get("detail") == "Учетные данные не были предоставлены."

def test_protected_endpoint_authenticated(auth_api_client):
    """Тест запроса к защищённому эндпоинту с токеном."""
    response = auth_api_client.get("/api/v1/tasks/")

    assert response.status_code == 200

def test_refresh_token(auth_tokens, api_client):
    """Тест обновления access-токена."""
    response = api_client.post("/api/v1/token/refresh/", data={"refresh": auth_tokens["refresh"]})

    assert response.status_code == 200
    assert "access" in response.data


# CRUD tests
def test_create_task(auth_api_client):
    """Тест успешного создания задачи."""
    data = {
        "title": "New Task",
        "description": "Description",
        "deadline": (timezone.now() + timezone.timedelta(days=3)).isoformat(),
        "status": "new",
        "priority": "high"
    }
    response = auth_api_client.post("/api/v1/tasks/", data)

    assert response.status_code == 201
    assert response.data["title"] == "New Task"
    assert response.data["description"] == "Description"
    assert response.data["status"] == "new"
    assert response.data["priority"] == "high"

def test_list_tasks(auth_api_client, task):
    """Тест получения списка задач."""
    response = auth_api_client.get("/api/v1/tasks/")

    assert response.status_code == 200
    assert len(response.data) > 0
    assert isinstance(response.data[0], dict)
    assert response.data[0].get("title")
    assert response.data[0].get("description")
    assert response.data[0].get("deadline")
    assert response.data[0].get("status")
    assert response.data[0].get("priority")

def test_retrieve_task(auth_api_client, task):
    """Тест получения конкретной задачи по ID."""
    response = auth_api_client.get(f"/api/v1/tasks/{task.id}/")

    assert response.status_code == 200
    assert response.data.get("title") == task.title
    assert response.data.get("description") == task.description
    assert response.data.get("status") == task.status
    assert response.data.get("priority") == task.priority

def test_update_task(auth_api_client, task):
    """Тест обновления задачи."""
    updated_data = {
        "title": "Updated Task",
        "description": "Updated Description",
        "deadline": (timezone.now() + timezone.timedelta(days=5)).isoformat(),
        "status": "in_progress",
        "priority": "low"
    }
    response = auth_api_client.put(f"/api/v1/tasks/{task.id}/", updated_data)

    assert response.status_code == 200
    assert response.data.get("title") == "Updated Task"
    assert response.data.get("status") == "in_progress"


def test_partial_update_task(auth_api_client, task):
    """Тест частичного обновления задачи (только статус)."""
    response = auth_api_client.patch(f"/api/v1/tasks/{task.id}/", {"status": "completed"})

    assert response.status_code == 200
    assert response.data["status"] == "completed"

def test_delete_task(auth_api_client, task):
    """Тест удаления задачи."""
    response = auth_api_client.delete(f"/api/v1/tasks/{task.id}/")

    assert response.status_code == 204
    assert Task.objects.filter(id=task.id).exists() is False
