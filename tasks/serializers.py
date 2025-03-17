from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Task.

    Автоматически импортирует все атрибуты модели.
    """

    class Meta:
        model = Task
        fields = ("title", "description", "deadline", "status", "priority")

    def validate_deadline(self, value):
        """
        Проверяет, что дедлайн задачи не установлен в прошлом.
        """
        if self.instance is None:
            if value < timezone.now() - timedelta(seconds=59):
                raise serializers.ValidationError("Дедлайн не может быть в прошлом.")
        return value


class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User.

    Позволяет создать нового пользователя с уникальным username, email и паролем.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        """
        Создаёт нового пользователя с хэшированным паролем.
        """
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """
    Сериализатор для аутентификации пользователей.

    Проверяет email и пароль, возвращает объект пользователя при успешной аутентификации.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Проверяет корректность email и пароля.
        """
        email = data.get("email")
        password = data.get("password")
        user = User.objects.filter(email=email).first()

        if not user or not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        return user
