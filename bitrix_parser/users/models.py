from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address', unique=True)
    uuid = models.PositiveIntegerField(verbose_name='Uuid', default=0)
    period_activation = models.DateField(
        verbose_name='period_activationи',
        help_text='Note:You are 4 hours ahead of server time',
        null=True, blank=True)
    status_activation = models.BooleanField(
        verbose_name='status_activation',
        default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def is_activated(self):
        if self.status_activation and self.date_activation and self.date_activation > timezone.now():
            return True
        else:
            return False

    is_activated.boolean = True
    is_activated.short_description = 'Activated'

    @property
    def activation_status_verbose(self):
        return "Активирован" if self.is_activated() else "Не активирован"


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['username', 'email'],
        #         name='unique_username_email'
        #     )
        # ]

    def __str__(self):
        return f'{self.username}'

