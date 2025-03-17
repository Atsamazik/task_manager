from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


def custom_exception_handler(exc, context):
    """
    Кастомный обработчик исключений для DRF.

    Возвращает ошибки в едином JSON-формате.
    """
    response = exception_handler(exc, context)

    if isinstance(exc, Http404):
        return Response(
            {"error": "Страница не найдена."},
            status=status.HTTP_404_NOT_FOUND
        )

    if response is not None:
        custom_data = {
            "error": "Произошла ошибка.",
            "details": response.data
        }
        return Response(custom_data, status=response.status_code)

    return Response(
        {"error": "Внутренняя ошибка сервера."},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
