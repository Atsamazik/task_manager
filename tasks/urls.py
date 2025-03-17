from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from tasks import views

router = routers.SimpleRouter()
router.register(r'tasks', views.TaskViewSet, basename="task")

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('analytics/', views.AnalyticsAPIView.as_view(), name="analytics"),
]