from django.core.management.base import BaseCommand
from catalog.models import Category, Subcategory


CATALOG_DATA = {
    'BMW': ['M2', 'M3', 'M4', 'M5', 'X3', 'X5', 'E30', 'E46', 'E60', 'F30'],
    'Mercedes-Benz': ['C-Class', 'E-Class', 'S-Class', 'GLC', 'GLE', 'A-Class', 'AMG GT'],
    'Audi': ['A3', 'A4', 'A6', 'Q3', 'Q5', 'Q7', 'RS4', 'RS6', 'TT'],
    'Volkswagen': ['Golf', 'Passat', 'Tiguan', 'Polo', 'Touareg', 'Jetta', 'Arteon'],
    'Toyota': ['Camry', 'Corolla', 'RAV4', 'Land Cruiser', 'Hilux', 'Yaris', 'Supra'],
    'Honda': ['Civic', 'Accord', 'CR-V', 'HR-V', 'Jazz', 'Legend', 'NSX'],
    'Ford': ['Focus', 'Mondeo', 'Fiesta', 'Mustang', 'Explorer', 'Kuga', 'Ranger'],
    'Nissan': ['Qashqai', 'X-Trail', 'Juke', 'Patrol', 'GT-R', 'Leaf', '370Z'],
    'Hyundai': ['Tucson', 'Santa Fe', 'Sonata', 'i30', 'i40', 'Creta', 'Elantra'],
    'Kia': ['Sportage', 'Sorento', 'Rio', 'Cerato', 'Stinger', 'Telluride', 'EV6'],
    'Запчасти (общее)': [
        'Двигатель', 'Трансмиссия', 'Тормозная система', 'Подвеска',
        'Электрика', 'Кузовные детали', 'Выхлопная система', 'Охлаждение',
        'Рулевое управление', 'Топливная система',
    ],
}


def slugify_ru(text):
    import re
    text = text.lower()
    text = re.sub(r'[^a-z0-9а-яё\s-]', '', text)
    text = re.sub(r'[\s]+', '-', text)
    text = text.replace('а', 'a').replace('е', 'e').replace('о', 'o').replace('и', 'i')
    text = re.sub(r'[^a-z0-9-]', '', text)
    return text or 'item'


class Command(BaseCommand):
    help = 'Заполнить категории и подкатегории автозапчастей'

    def handle(self, *args, **options):
        created_cats = 0
        created_subs = 0
        for cat_name, subcats in CATALOG_DATA.items():
            slug = slugify_ru(cat_name)
            # ensure unique slug
            base_slug = slug
            i = 1
            while Category.objects.filter(slug=slug).exclude(name=cat_name).exists():
                slug = f'{base_slug}-{i}'
                i += 1
            cat, created = Category.objects.get_or_create(name=cat_name, defaults={'slug': slug})
            if created:
                created_cats += 1
                self.stdout.write(f'  Категория: {cat_name}')
            for sub_name in subcats:
                sub_slug = slugify_ru(sub_name)
                base_sub_slug = sub_slug
                j = 1
                while Subcategory.objects.filter(category=cat, slug=sub_slug).exclude(name=sub_name).exists():
                    sub_slug = f'{base_sub_slug}-{j}'
                    j += 1
                sub, sub_created = Subcategory.objects.get_or_create(
                    category=cat, name=sub_name, defaults={'slug': sub_slug}
                )
                if sub_created:
                    created_subs += 1
        self.stdout.write(self.style.SUCCESS(
            f'Готово! Создано категорий: {created_cats}, подкатегорий: {created_subs}'
        ))
