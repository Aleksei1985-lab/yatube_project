from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(
        'Название мероприятия',
        max_length=200,
        help_text='Не более 200 символов'
    )
    start_at = models.DateTimeField(
        'Дата и время проведения'
    )
    description = models.TextField(
        'Описание мероприятия'
    )
    contact = models.EmailField(
        'Контактный email'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='events',
        verbose_name='Организатор'
    )
    location = models.CharField(
        'Место проведения',
        max_length=400,
        help_text='Не более 400 символов'
    )
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        'Дата обновления',
        auto_now=True
    )

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ['-start_at']

    def __str__(self):
        return f'{self.name} ({self.start_at:%d.%m.%Y})'
