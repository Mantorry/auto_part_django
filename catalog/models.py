from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField()

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        ordering = ['name']
        unique_together = ['category', 'slug']

    def __str__(self):
        return f'{self.category.name} — {self.name}'


class Product(models.Model):
    name = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    image = models.ImageField('Изображение', upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField('Остаток на складе', default=0)
    sold_count = models.PositiveIntegerField('Продано', default=0)
    price = models.DecimalField('Цена продажи', max_digits=12, decimal_places=2)
    discount = models.DecimalField('Скидка (%)', max_digits=5, decimal_places=2, default=0)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return self.price

    @property
    def low_stock(self):
        return self.stock < 3
