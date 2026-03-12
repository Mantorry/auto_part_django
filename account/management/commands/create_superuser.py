from django.core.management.base import BaseCommand
from account.models import User


class Command(BaseCommand):
    help = 'Создать суперпользователя (администратора)'

    def handle(self, *args, **options):
        if User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.WARNING('Суперпользователь admin уже существует'))
            return
        user = User(
            full_name='Администратор Системы',
            username='admin',
            role='admin',
            is_superuser=True,
            is_active=True,
        )
        user.set_password('admin123')
        user.save()
        self.stdout.write(self.style.SUCCESS(
            'Суперпользователь создан: логин=admin, пароль=admin123'
        ))
