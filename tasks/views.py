from django.contrib.auth.models import User
from rest_framework import viewsets, views, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from tasks.models import Task
from tasks.serializers import TaskSerializer, RegisterSerializer, LoginSerializer
from tasks.services import analytics


class RegisterView(generics.CreateAPIView):
    """
    Представление для регистрации пользователей.

    Разрешает создание новых пользователей в системе.
    """

    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    """
    Представление для аутентификации пользователей.

    Принимает email и пароль, возвращает JWT-токены.
    """

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Выполняет аутентификацию пользователя и возвращает JWT-токены.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })


class TaskViewSet(viewsets.ModelViewSet):
    """
    Набор представлений для управления моделью Task.

    Предоставляет стандартные действия CRUD (создание, чтение, обновление, удаление).
    """

    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        """
        Получает список задач с возможностью фильтрации.
        Фильтрация доступна по статусу и приоритету.

        Returns:
            QuerySet: Отфильтрованный список задач.
        """
        queryset = Task.objects.all()

        status_list = self.request.query_params.getlist("status")
        priority_list = self.request.query_params.getlist("priority")

        if status_list:
            queryset = queryset.filter(status__in=status_list)
        if priority_list:
            queryset = queryset.filter(priority__in=priority_list)

        return queryset


class AnalyticsAPIView(views.APIView):
    """
    Представление для получения аналитики по задачам.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Возвращает статистику по задачам.

        Returns:
            Response: JSON с аналитическими данными.
        """
        return Response(analytics.get_task_statistics())
