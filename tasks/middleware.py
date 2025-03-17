import logging

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('requests_logger')


class RequestLoggingMiddleware(MiddlewareMixin):
    """Middleware для логирования HTTP-запросов."""

    def process_response(self, request, response):
        logger.info(
            f"{request.method} {request.get_full_path()} {response.status_code}",
            extra={
                'method': request.method,
                'url': request.get_full_path(),
                'status': response.status_code,
            },
        )
        return response
