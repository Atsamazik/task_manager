from datetime import timedelta

from django.db import models
from django.utils import timezone


class Task(models.Model):
    """
   Модель задачи в системе управления задачами.

    Атрибуты:
        title (str): Заголовок задачи. Обязательное поле.
        description (str, optional): Описание задачи. Может быть пустым.
        deadline (datetime): Крайний срок выполнения задачи.
        status (str): Текущий статус задачи. Выбирается из предопределённых значений.
        priority (str): Приоритет задачи. Выбирается из предопределённых значений.
        created_at (datetime): Дата и время создания задачи.
        updated_at (datetime): Дата и время последнего обновления задачи.
        started_at (datetime, optional): Время, когда задача была переведена в статус "В работе".
        finished_at (datetime, optional): Время, когда задача была в статус "Завершена".

    Константы:
        STATUS_CHOICES (list[tuple]): Доступные статусы задачи:
            - "new" (Новая)
            - "in_progress" (В работе)
            - "completed" (Завершена)
        PRIORITY_CHOICES (list[tuple]): Доступные приоритеты задачи:
            - "low" (Низкий)
            - "middle" (Средний)
            - "high" (Высокий)
    """

    STATUS_CHOICES = [("new", "Новая"), ("in_progress", "В работе"), ("completed", "Завершена")]
    PRIORITY_CHOICES = [("low", "Низкий"), ("middle", "Средний"), ("high", "Высокий")]

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    deadline = models.DateTimeField(verbose_name="Крайний срок")
    status = models.CharField(max_length=31, choices=STATUS_CHOICES, default="new", verbose_name="Статус")
    priority = models.CharField(max_length=31, choices=PRIORITY_CHOICES, default="middle", verbose_name="Приоритет")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменена")
    started_at = models.DateTimeField(null=True, blank=True, verbose_name="Начата")
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name="Завершена")

    def update_status_timestamps(self, previous_status: str):
        """Обновляет timestamps в зависимости от изменения статуса."""
        status_transitions = {
            ("new", "in_progress"): lambda: self._set_started,
            ("new", "completed"): lambda: self._set_started_and_finished,
            ("in_progress", "completed"): lambda: setattr(self, "finished_at", self.finished_at or timezone.now()),
            ("completed", "new"): lambda: self._reset_started_and_finished(),
            ("completed", "in_progress"): lambda: setattr(self, "finished_at", None),
            ("in_progress", "new"): lambda: setattr(self, "started_at", None),
            (None, "in_progress"): self._set_started,
            (None, "completed"): self._set_started_and_finished
        }

        action = status_transitions.get((previous_status, self.status))
        if action:
            action()

    def _set_started(self):
        """Устанавливает started_at, если его нет"""
        if not self.started_at:
            self.started_at = timezone.now()

    def _set_started_and_finished(self):
        """Устанавливает started_at и finished_at, если их нет."""
        if not self.started_at:
            self.started_at = timezone.now()
        if not self.finished_at:
            self.finished_at = self.started_at + timedelta(seconds=1)

    def _reset_started_and_finished(self):
        """Сбрасывает started_at и finished_at в None."""
        self.started_at = None
        self.finished_at = None

    def save(self, *args, **kwargs):
        """Сохранение объекта с обновлением timestamps."""
        previous_status = None

        if self.pk:
            previous_status = Task.objects.filter(pk=self.pk).values_list("status", flat=True).first()

        self.update_status_timestamps(previous_status)

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Возвращает строковое представление задачи."""
        return self.title

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["-deadline"]
