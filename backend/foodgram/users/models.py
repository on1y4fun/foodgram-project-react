from django.db import models
from django.contrib.auth.models import AbstractUser

from foodgram.settings import USER, ADMIN


CHOICES = (
    (USER, 'Пользователь'),
    (ADMIN, 'Администратор'),
)


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Логин',
        help_text='Введите логин',
    )
    email = models.EmailField(
        max_length=256,
        unique=True,
        verbose_name='Электронная почта',
        help_text='Введите электронную почту',
    )
    first_name = models.CharField(
        max_length=150,
        unique=False,
        verbose_name='Имя',
        help_text='Введите имя',
    )
    last_name = models.CharField(
        max_length=150,
        unique=False,
        verbose_name='Фамилия',
        help_text='Введите фамилию',
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='Биография',
        help_text='Напишите биографию',
    )
    role = models.CharField(
        choices=CHOICES,
        max_length=42,
        default=CHOICES[0][0],
        verbose_name='Роль',
        help_text='Укажите роль',
    )
    confirmation_code = models.CharField(max_length=32, blank=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ('username',)

    @property
    def is_admin(self):
        return (self.role == ADMIN or self.is_staff) and self.is_authenticated

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('username',)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('user',)
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'), name='follow_model'
            )
        ]

    def __str__(self):
        return f'{self.user} {self.author}'