from django.db import models
from django.contrib.auth.hashers import make_password, check_password


ROLE_CHOICES = [
    ('admin', 'Администратор'),
    ('seller', 'Продавец'),
    ('sorter', 'Сортировщик'),
]


class User(models.Model):
    full_name = models.CharField('ФИО', max_length=255)
    username = models.CharField('Логин', max_length=150, unique=True)
    password = models.CharField('Пароль', max_length=255)
    role = models.CharField('Роль', max_length=20, choices=ROLE_CHOICES, default='seller')
    is_active = models.BooleanField('Активен', default=True)
    is_superuser = models.BooleanField('Суперпользователь', default=False)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    theme = models.CharField('Тема', max_length=10, default='light')
    notifications_enabled = models.BooleanField('Уведомления', default=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.full_name} ({self.get_role_display()})'

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
