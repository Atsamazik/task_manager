from django.db.models import Count, Avg, F

from tasks.models import Task


def get_task_statistics():
    """Возвращает статистику по задачам."""
    # Общее количество задач
    total_tasks = Task.objects.count()

    # Подсчет задач по статусам
    status_counts = (
        Task.objects.values("status")
        .annotate(count=Count("id"))
        .order_by("status")
    )

    # Средняя продолжительность выполнения задачи
    avg_duration = Task.objects.filter(
        status="completed",
        started_at__isnull=False,
        finished_at__isnull=False,
    ).aggregate(avg_completion=Avg(F("finished_at") - F("started_at")))["avg_completion"]

    # Преобразование timedelta в удобочитаемый формат
    if avg_duration:
        avg_seconds = avg_duration.total_seconds()
        avg_days = int(avg_seconds // 86400)
        avg_hours = int((avg_seconds % 86400) // 3600)
        avg_minutes = int((avg_seconds % 3600) // 60)

        parts = []
        if avg_days:
            parts.append(f"{avg_days} дн")
        if avg_hours or avg_days:
            parts.append(f"{avg_hours} ч")
        if avg_minutes or (not avg_days and not avg_hours):
            parts.append(f"{avg_minutes} мин")

        avg_duration_str = " ".join(parts)
    else:
        avg_duration_str = "Нет данных"


    response_data = {
        "total_tasks": total_tasks,
        "status_counts": list(status_counts),
        "average_completion_time": avg_duration_str,
    }

    return response_data
