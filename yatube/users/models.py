from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    subscriptions = models.ManyToManyField(
        'self',
        through='posts.Follow',
        through_fields=('user', 'author'),
        symmetrical=False,
        blank=True,
        related_name='subscribers',
        verbose_name=_('подписки')
    )
    
    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')
        swappable = 'AUTH_USER_MODEL'
    
    def __str__(self):
        return self.get_full_name() or self.username